from typing import Dict, Any
from jinja2 import Template

ATOMIC_EXTRACTION_PROMPT = """You are a scientific NLP extractor specializing in causal narrative analysis.

Extract all atomic events, states, actions, goals, constraints, and consequential outcomes from the narrative.
Guidelines:
1. Prefer high-recall over premature pruning.
2. Maintain strict provenance: every event must be grounded in an exact `text_span` from the story.
3. Distinguish explicitness: "explicit" vs "strongly_inferred" vs "speculative".
4. Identify participants and event type (action, state, event, goal, constraint, outcome, emotion_reaction).
5. Assign a coarse `temporal_rank` based on narrative occurrence order.

Story ID: {{ story.story_id }}
Full Narrative:
\"\"\"
{{ story.text }}
\"\"\"

Numbered Sentences:
{% for s in story.sentences %}
[{{ s.sentence_id }}] {{ s.text }}
{% endfor %}
"""

SEMANTIC_NORMALIZATION_PROMPT = """You are a semantic parser for causal event graphs.

Convert the following atomic events into normalized semantic predicates with structured arguments.
Guidelines:
1. Do not abstract too aggressively yet (e.g., maintain domain specificity like `clean_room`, `gingerbread`, `room_inspection`).
2. Retain direct provenance by citing the `atomic_event_ids` mapped to each normalized event.
3. Standardize predicate names (e.g., `NEGLECT_TASK`, `INSUFFICIENT_TIME`, `OFFER_INCENTIVE`, `FAIL_REQUIREMENT`, `WITHHOLD_REWARD`).

Story ID: {{ story.story_id }}

Atomic Events:
{% for e in atomic_events %}
- {{ e.event_id }}: "{{ e.text_span }}" | Predicate: {{ e.predicate }} | Sentence: {{ e.sentence_id }}
{% endfor %}
"""

RELATION_EXTRACTION_PROMPT = """You are a narrative causal analyst constructing an evidence-grounded typed relation graph.

Given the normalized events of a story, extract typed relations between them.
Allowed relation types:
- CAUSES: Source directly brings about or causes target.
- BEFORE: Source occurs strictly before target in story time (pure temporal, NOT causal).
- ENABLES: Source creates necessary preconditions for target.
- BLOCKS: Source prevents or obstructs target from succeeding.
- MOTIVATES: Source gives an agent a goal/incentive to attempt target.
- CONDITIONAL_ON: Target is contingent upon source condition being met.
- RESULTS_IN: Target is the consequential outcome or resulting state of source.
- PREVENTS: Source counteracts or stops target.

CRITICAL METHODOLOGICAL RULES:
1. Keep temporal order and causality STRICTLY DISTINCT. Do not mark an edge as CAUSES if it is merely BEFORE.
2. For example, an incentive offered does not cause an agent to already be behind; prior inaction does.
3. Provide clear `evidence` explaining the causal/relational justification.
4. Distinguish `explicitness`: explicit, strongly_inferred, or speculative.

Story ID: {{ story.story_id }}
Narrative:
\"\"\"
{{ story.text }}
\"\"\"

Normalized Events:
{% for ne in normalized_events %}
- {{ ne.norm_id }}: {{ ne.summary_label }} [{{ ne.predicate_name }}] (Args: {{ ne.arguments }})
{% endfor %}
"""

GOAL_OUTCOME_PROMPT = """You are a narrative goal and outcome analyzer.

Analyze the narrative to identify:
1. Central Problem: The core obstacle, failure, or deficit faced.
2. Central Goal: The target objective or requirement.
3. Intervention: Any external incentive, help, nudge, or plan introduced to alter the outcome.
4. Terminal Outcomes: The final consequential outcomes and states.
5. Anchor Event IDs: The normalized event IDs corresponding directly to these anchors.

Story ID: {{ story.story_id }}
Narrative:
\"\"\"
{{ story.text }}
\"\"\"

Normalized Events:
{% for ne in normalized_events %}
- {{ ne.norm_id }}: {{ ne.summary_label }} [{{ ne.predicate_name }}]
{% endfor %}
"""

BACKBONE_SELECTION_PROMPT = """You are an expert causal reasoning system performing causal backbone extraction.

Your objective is to identify the minimal causal backbone required to explain the story's problem, intervention, and terminal outcomes.

CRITERIA FOR RETENTION:
- Keep events that are causally necessary to explain:
  1. The central problem / backlog / neglect.
  2. How the intervention (incentive/help) entered the timeline.
  3. Why the requirement failed or succeeded (e.g. insufficient time / obstruction).
  4. The final outcome (requirement failure, reward withheld/received).

CRITERIA FOR PRUNING:
- Prune narrative decorations, emotional reactions, and incidental physical details that do not explain the core causal mechanism (e.g., sulking, slamming doors, cracking plaster, room decor).
- Provide an explicit reason for every pruned event.

Narrative:
\"\"\"
{{ story.text }}
\"\"\"

Normalized Events:
{% for ne in normalized_events %}
- {{ ne.norm_id }}: {{ ne.summary_label }} [{{ ne.predicate_name }}]
{% endfor %}

Anchors:
- Central Problem: {{ anchors.central_problem }}
- Central Goal: {{ anchors.central_goal }}
- Intervention: {{ anchors.intervention }}
- Terminal Outcomes: {{ anchors.terminal_outcomes }}
"""

MACRO_ABSTRACTION_PROMPT = """You are an abstract schema induction engineer.

Convert the causal backbone into Macro-Nodes with 4-Level Abstraction Ladders and typed backbone edges.

Guidelines:
1. Merge events that belong to the exact same causal stage into a single MacroNode (e.g., "daydreams" + "does not clean" -> "task neglect / inaction"). Do NOT merge events across different causal stages.
2. For each node, construct an Abstraction Ladder:
   - Level 0 (Raw): Exact story-grounded phrasing.
   - Level 1 (Domain): Domain-specific semantic predicate.
   - Level 2 (Functional): Functional causal role / relational label (target operating level).
   - Level 3 (Schema): High-level abstract schema label.
3. Connect the backbone nodes with typed edges (CAUSES, BEFORE, ENABLES, BLOCKS, MOTIVATES, CONDITIONAL_ON, RESULTS_IN, PREVENTS).
4. Maintain strict provenance to source normalized and atomic event IDs.

Backbone Retained Events:
{% for e in retained_events %}
- {{ e.norm_id }}: {{ e.summary_label }} [{{ e.predicate_name }}] (Atomic IDs: {{ e.atomic_event_ids }})
{% endfor %}

Narrative Text:
\"\"\"
{{ story.text }}
\"\"\"
"""


class PromptRegistry:
    """Manages prompt templates and rendering."""

    _TEMPLATES: Dict[str, str] = {
        "atomic_extraction": ATOMIC_EXTRACTION_PROMPT,
        "semantic_normalization": SEMANTIC_NORMALIZATION_PROMPT,
        "relation_extraction": RELATION_EXTRACTION_PROMPT,
        "goal_outcome": GOAL_OUTCOME_PROMPT,
        "backbone_selection": BACKBONE_SELECTION_PROMPT,
        "macro_abstraction": MACRO_ABSTRACTION_PROMPT,
    }

    @classmethod
    def render(cls, template_name: str, **kwargs) -> str:
        if template_name not in cls._TEMPLATES:
            raise KeyError(f"Template '{template_name}' not found in registry.")
        template = Template(cls._TEMPLATES[template_name])
        return template.render(**kwargs)
