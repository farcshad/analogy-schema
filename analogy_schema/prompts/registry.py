from typing import Dict, Any
from jinja2 import Template

ATOMIC_EXTRACTION_PROMPT = """You are a scientific NLP system specializing in causal narrative extraction.

Extract all atomic events, states, actions, goals, constraints, and consequential outcomes from the narrative.

Methodological Guidelines:
1. High recall: Extract all propositions and states rather than pre-filtering.
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
4. Identify if a state is persistent across story events (`is_persistent_state`).
5. Temporal Grounding: If an external intervention or plan is present, assign the occurrence or persistence relative to it:
   - `PRE_INTERVENTION`: Occurred or initiated strictly before the intervention.
   - `AT_INTERVENTION`: Part of the intervention event itself.
   - `POST_INTERVENTION`: Initiated after the intervention.
   - `SPANS_INTERVENTION`: Began prior to the intervention and persisted through or past it.
   - `UNANCHORED`: Contextual setting or stories without an intervention.

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
- `BEFORE`: Source occurs strictly before Target in narrative time, but Source did NOT causally produce Target (e.g., System Update --BEFORE--> Hardware Fault).
- `ENABLES`: Source creates necessary preconditions making Target possible (e.g., Security Clearance --ENABLES--> Server Room Access).
- `BLOCKS`: Source prevents, obstructs, or renders impossible Target (e.g., Network Partition --BLOCKS--> Database Replication).
- `MOTIVATES`: Source provides reason, goal, or incentive for an agent to attempt Target (e.g., Financial Audit Notice --MOTIVATES--> Reconciliation Attempt).
- `REQUIRES`: Source requires condition Target to be fulfilled in order to succeed/occur (e.g., Firmware Upgrade --REQUIRES--> System Reboot).
- `CONDITIONAL_ON`: Source outcome depends on Target condition being satisfied (e.g., Bonus Payout --CONDITIONAL_ON--> Exceeding Performance Quota).
- `RESULTS_IN`: Source directly produces consequential outcome Target (e.g., Missing Compliance Deadline --RESULTS_IN--> License Revocation).
- `PREVENTS`: Source actively stops or counteracts Target (e.g., Circuit Breaker Trip --PREVENTS--> Transformer Damage).

CRITICAL METHODOLOGICAL INVARIANTS:
1. Temporal order vs. True Causality: Never use `CAUSES` for events that merely precede each other temporally. If event A existed prior to an intervention B, B does not cause A.
2. Directionality: Strictly adhere to the defined `source_id` -> `target_id` conventions.
3. Explicitness: Assign explicit, strongly_inferred, or speculative.
4. Ground each relation with an `evidence` explanation citing the narrative mechanism.

Story ID: {{ story.story_id }}

Narrative Text:
\"\"\"
{{ story.text }}
\"\"\"

Normalized Events:
{% for ne in normalized_events %}
- {{ ne.norm_id }}: {{ ne.summary_label }} [{{ ne.predicate_name }}] (Args: {{ ne.arguments }})
{% endfor %}
"""

GOAL_OUTCOME_PROMPT = """You are a narrative structure and anchor analyzer.

Identify the central narrative anchors:
1. `central_problem`: The primary difficulty, failure, deficit, or obstacle described.
2. `central_goal`: The focal objective, standard, or requirement to be achieved.
3. `intervention_event_ids`: Event IDs of any external incentive, assistance, nudge, or plan introduced to alter the trajectory.
4. `focal_outcome_ids`: Event IDs of the primary success or failure of the central goal/requirement.
5. `contingent_outcome_ids`: Event IDs of consequences contingent upon the focal outcome (e.g., reward granted, reward withheld, penalty applied).
6. `downstream_reaction_ids`: Event IDs of secondary emotional outbursts, reactions, or incidental collateral actions that do NOT explain why the focal outcome occurred.

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
  1. How the problem or deficit originated.
  2. The introduction of any intervention or plan.
  3. The immediate causal or blocking condition preventing/enabling goal fulfillment.
  4. The focal outcome (success/failure) and direct contingent consequences.

Pruning Principles:
- Prune background setting details, static character descriptions, secondary emotional reactions, and incidental collateral actions that do not causally explain the focal outcome.
- For every pruned event, provide a clear counterfactual reason explaining why its removal does not break the causal explanation of the focal outcome.

Narrative Text:
\"\"\"
{{ story.text }}
\"\"\"

Normalized Events:
{% for ne in normalized_events %}
- {{ ne.norm_id }}: {{ ne.summary_label }} [{{ ne.predicate_name }}] (Phase: {{ ne.temporal_phase }})
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

Methodological Constraints:
1. Macro-Node Grouping:
   - Merge events ONLY if they occupy the same functional stage in the narrative progression.
   - DO NOT merge a causal antecedent and its resulting deficit into a single node (e.g., keep the triggering action separate from the resulting state).
   - Node labels must describe states or events, NOT embedded causal relations (e.g., prefer "deferred maintenance" or "insufficient buffer" over "lack of time causes failure").
2. Assign a controlled functional role from the generic ontology:
   `BACKGROUND`, `CAUSAL_ANTECEDENT`, `PROBLEM_STATE`, `GOAL`, `INTERVENTION`, `ACTION_RESPONSE`, `CONSTRAINT`, `FOCAL_OUTCOME`, `CONTINGENT_OUTCOME`, `DOWNSTREAM_REACTION`.
3. Assign the story-grounded temporal phase relative to any intervention:
   `PRE_INTERVENTION`, `AT_INTERVENTION`, `POST_INTERVENTION`, `SPANS_INTERVENTION`, `UNANCHORED`.
4. Construct the 4-Level Abstraction Ladder for each MacroNode:
   - Level 0 (Raw): Exact narrative phrasing.
   - Level 1 (Domain): Domain-specific semantic predicate.
   - Level 2 (Functional): Functional causal role / relational state (target operating level).
   - Level 3 (Schema): High-level abstract schema label.

Note: DO NOT generate graph edges here. Graph edges are derived deterministically from the underlying rich relations.

Story ID: {{ story.story_id }}

Narrative Text:
\"\"\"
{{ story.text }}
\"\"\"

Retained Normalized Events:
{% for e in retained_events %}
- {{ e.norm_id }}: {{ e.summary_label }} [{{ e.predicate_name }}] (Phase: {{ ne_phase_map.get(e.norm_id, 'UNANCHORED') }})
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
