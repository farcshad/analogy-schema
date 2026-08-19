from typing import Dict, Any
from jinja2 import Template

ATOMIC_EXTRACTION_PROMPT = """You are a scientific NLP system specializing in causal narrative extraction.

Extract all atomic events, states, actions, goals, constraints, and consequential outcomes from the narrative.

Methodological Guidelines:
1. High recall: Extract all propositions, actions, and states rather than pre-filtering.
2. Textual Grounding: Every event must have an exact or near-exact `text_span` directly from the narrative.
3. Explicitness: Label as "explicit" (directly asserted), "strongly_inferred" (necessary presupposition), or "speculative".
4. Identify participants, event_type (action, state, event, goal, constraint, outcome, emotion_reaction), polarity (positive, negative), and narrative temporal order (`temporal_rank`).

Story ID: {{ story.story_id }}

Narrative Text:
\"\"\"
{{ story.text }}
\"\"\"

Numbered Sentences:
{% for s in story.sentences %}
[{{ s.sentence_id }}] {{ s.text }}
{% endfor %}
"""

SEMANTIC_NORMALIZATION_PROMPT = """You are a semantic parser for causal narrative analysis.

Convert the extracted atomic events into normalized semantic predicate-argument representations.

Methodological Guidelines:
1. Maintain direct provenance by listing the `atomic_event_ids` that comprise each normalized event.
2. Retain story-specific arguments in `arguments` (e.g., actor, object, task, target).
3. Standardize predicate names into standardized uppercase predicates (e.g., `DEFICIT_STATE`, `INITIATE_PLAN`, `INTRODUCE_INCENTIVE`, `RESOURCE_SHORTAGE`, `FAIL_CRITERIA`, `CONSEQUENCE_ENACTED`).
4. Temporal Grounding: Disambiguate textual mention location from true story-world onset time:
   - `mention_phase`: Position where event is mentioned relative to the intervention sentence (`PRE_INTERVENTION`, `AT_INTERVENTION`, `POST_INTERVENTION`, `UNANCHORED`).
   - `onset_phase`: When the event/state actually began in the story world (`PRE_INTERVENTION`, `AT_INTERVENTION`, `POST_INTERVENTION`, `UNANCHORED`).
   - `holds_at_intervention`: True if this state existed and remained active when the intervention occurred (e.g., a backlog or deficit existing prior to and during the intervention).
   - `temporal_extent`: `POINT` (instantaneous), `PERSISTENT_STATE` (ongoing condition), or `INTERVAL` (extended duration).
5. Summary label: Provide an atomic description of the state or action without embedding causal clauses.

Story ID: {{ story.story_id }}

Narrative Text:
\"\"\"
{{ story.text }}
\"\"\"

Atomic Events:
{% for e in atomic_events %}
- {{ e.event_id }}: "{{ e.text_span }}" | Predicate: {{ e.predicate }} | Sentence: {{ e.sentence_id }}
{% endfor %}
"""

RELATION_EXTRACTION_PROMPT = """You are a causal relation analyst. Extract evidence-grounded typed relations between the normalized events.

Allowed Relation Types and Directional Semantics:
- `CAUSES`: Source brings about or causes Target (e.g., Server Overload --CAUSES--> Request Latency).
  * EVIDENCE RULE: A causal relation must NOT be justified using generic world knowledge (e.g. 'negative feelings often cause distraction'). Require explicit narrative causal language, direct mechanistic dependency, or necessary local inference from stated events. Otherwise downgrade to `BEFORE` or omit.
- `RESULTS_IN`: Source directly produces consequential outcome Target (e.g., Missing Compliance Deadline --RESULTS_IN--> License Revocation; Failing Requirement --RESULTS_IN--> Reward Withheld).
- `BEFORE`: Source occurs strictly before Target in narrative time, but Source did NOT causally produce Target (e.g., System Update --BEFORE--> Hardware Fault).
- `ENABLES`: Source creates necessary preconditions making Target possible (e.g., Security Clearance --ENABLES--> Server Room Access).
- `BLOCKS`: Source prevents, obstructs, or renders impossible Target (e.g., Network Partition --BLOCKS--> Database Replication).
- `PREVENTS`: Source actively stops or counteracts Target (e.g., Circuit Breaker Trip --PREVENTS--> Transformer Damage).
- `MOTIVATES`: Source provides intentional reason, goal, or incentive for an agent to attempt Target (e.g., Audit Notice --MOTIVATES--> Reconciliation Attempt).
  * EVIDENCE RULE: `MOTIVATES` requires textual evidence of intentional motivational causation (e.g. agent acting in order to achieve the goal). Mere 'after X, agent did Y' is strictly `BEFORE`, NOT `MOTIVATES`.
- `REQUIRES`: Source requires condition Target to be fulfilled in order to succeed/occur (e.g., Firmware Upgrade --REQUIRES--> System Reboot).

CRITICAL METHODOLOGICAL INVARIANTS:
1. Temporal order vs. Causality: Never use `CAUSES` for events that merely precede each other. If event A existed prior to an intervention B, B does not cause A.
2. Conservative Motivation: Do not use `MOTIVATES` for incidental actions that follow an event unless explicit motivational causation is present; otherwise use `BEFORE`.
3. Directionality: Adhere strictly to `source_id` -> `target_id` conventions.
4. Ground each relation with an `evidence` explanation citing direct narrative mechanism.

Story ID: {{ story.story_id }}

Narrative Text:
\"\"\"
{{ story.text }}
\"\"\"

Normalized Events:
{% for ne in normalized_events %}
- {{ ne.norm_id }}: {{ ne.summary_label }} [{{ ne.predicate_name }}] (Onset: {{ ne.temporal_grounding.onset_phase }}, HoldsAtIntervention: {{ ne.temporal_grounding.holds_at_intervention }})
{% endfor %}
"""

GOAL_OUTCOME_PROMPT = """You are a narrative structure and anchor analyzer.

Identify the central narrative anchors and structured incentive contracts:
1. `central_problem`: The primary difficulty, failure, deficit, or obstacle described.
2. `central_goal`: The focal objective, standard, or requirement to be achieved.
3. `intervention_event_ids`: Event IDs of any external incentive, assistance, nudge, or plan introduced.
4. `focal_outcome_ids`: Event IDs of the primary success or failure of the central goal/requirement.
5. `contingent_outcome_ids`: Event IDs of consequences contingent upon the focal outcome (e.g., reward granted, reward withheld, penalty applied).
6. `downstream_reaction_ids`: Event IDs of secondary emotional outbursts, reactions, or incidental collateral actions that do NOT explain why the focal outcome occurred.
   * INVARIANT: Any event that causally explains the focal outcome MUST NOT be marked as a downstream reaction.
7. `contracts`: Structured incentive contracts if an incentive was offered (promised_reward, contingent_requirement, condition_polarity).

Story ID: {{ story.story_id }}

Narrative Text:
\"\"\"
{{ story.text }}
\"\"\"

Normalized Events:
{% for ne in normalized_events %}
- {{ ne.norm_id }}: {{ ne.summary_label }} [{{ ne.predicate_name }}]
{% endfor %}
"""

BACKBONE_SELECTION_PROMPT = """You are a causal reasoning engine performing explanatory backbone selection.

Your objective is to identify which normalized events are causally necessary to explain the narrative's central problem, intervention, and focal/contingent outcomes.

Retention Principles:
- Retain events that form the explanatory mechanism of:
  1. How the specific deficit or problem state originated.
  2. The introduction of any intervention or plan.
  3. The immediate causal or blocking condition preventing/enabling goal fulfillment.
  4. The focal outcome (success/failure) and direct contingent consequences.

Pruning Principles:
- Prune chronic past history, static character traits, and background settings (e.g., long-term institutional status or habitual past record) that do not explain the specific focal episode.
- Prune secondary emotional reactions and downstream collateral actions.
- For every pruned event, provide a clear counterfactual explanation of why its removal does not damage the explanation of the focal outcome.

Narrative Text:
\"\"\"
{{ story.text }}
\"\"\"

Normalized Events:
{% for ne in normalized_events %}
- {{ ne.norm_id }}: {{ ne.summary_label }} [{{ ne.predicate_name }}] (Onset: {{ ne.temporal_grounding.onset_phase }})
{% endfor %}

Anchors:
- Central Problem: {{ anchors.central_problem }}
- Central Goal: {{ anchors.central_goal }}
- Interventions: {{ anchors.intervention_event_ids }}
- Focal Outcomes: {{ anchors.focal_outcome_ids }}
- Contingent Outcomes: {{ anchors.contingent_outcome_ids }}
- Downstream Reactions: {{ anchors.downstream_reaction_ids }}
"""

MACRO_GROUPING_PROMPT = """You are an abstract schema induction parser.

Group the retained normalized events into functional Macro-Nodes and assign 4-Level Abstraction Ladders.

STRICT METHODOLOGICAL CONSTRAINTS:
1. DO NOT merge events that have a causal, consequential, blocking, motivational, or temporal relation between them (e.g., do NOT merge a causal antecedent and its resulting deficit state into one node; keep them separate).
2. Level-2 Functional Labels: Must be pure atomic event or state descriptions (e.g., "task neglect", "performance deficit", "conditional incentive", "insufficient remaining resources", "requirement failure", "reward withheld").
   STRICTLY AVOID relational phrases such as "caused by", "due to", "leading to", "results in", "because of", "prevents", or "despite intervention".
3. Assign a controlled functional role from the generic ontology:
   `BACKGROUND`, `CAUSAL_ANTECEDENT`, `PROBLEM_STATE`, `GOAL`, `INTERVENTION`, `ACTION_RESPONSE`, `CONSTRAINT`, `FOCAL_OUTCOME`, `CONTINGENT_OUTCOME`, `DOWNSTREAM_REACTION`.
4. Construct the 4-Level Abstraction Ladder for each MacroNode:
   - Level 0 (Raw): Exact narrative phrasing.
   - Level 1 (Domain): Domain-specific semantic predicate.
   - Level 2 (Functional): Atomic functional causal role / relational state (target operating level).
   - Level 3 (Schema): High-level abstract schema label.

Note: DO NOT generate graph edges here. Graph edges are derived deterministically from the underlying rich relations.

Story ID: {{ story.story_id }}

Narrative Text:
\"\"\"
{{ story.text }}
\"\"\"

Retained Normalized Events:
{% for e in retained_events %}
- {{ e.norm_id }}: {{ e.summary_label }} [{{ e.predicate_name }}] (Onset: {{ e.temporal_grounding.onset_phase }}, HoldsAtIntervention: {{ e.temporal_grounding.holds_at_intervention }})
{% endfor %}

Existing Rich Relations between Retained Events:
{% for r in rich_relations %}
- {{ r.source_id }} --{{ r.relation_type }}--> {{ r.target_id }}
{% endfor %}
"""


class PromptRegistry:
    """Manages versioned, domain-neutral prompt templates."""

    _TEMPLATES: Dict[str, str] = {
        "atomic_extraction": ATOMIC_EXTRACTION_PROMPT,
        "semantic_normalization": SEMANTIC_NORMALIZATION_PROMPT,
        "relation_extraction": RELATION_EXTRACTION_PROMPT,
        "goal_outcome": GOAL_OUTCOME_PROMPT,
        "backbone_selection": BACKBONE_SELECTION_PROMPT,
        "macro_grouping": MACRO_GROUPING_PROMPT,
    }

    @classmethod
    def render(cls, template_name: str, **kwargs) -> str:
        if template_name not in cls._TEMPLATES:
            raise KeyError(f"Template '{template_name}' not found in registry.")
        template = Template(cls._TEMPLATES[template_name])
        return template.render(**kwargs)
