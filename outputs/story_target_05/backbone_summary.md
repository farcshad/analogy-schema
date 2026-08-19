# Causal Backbone: story_target_05

## Narrative Anchors & Contracts
- **Central Problem**: Arthur's gingerbread is contaminated by plaster dust, making it spoiled and inedible.
- **Central Goal**: Arthur should discard the spoiled food and step into the courtyard for fresh air.
- **Intervention Events**: ['NE9']
- **Focal Outcomes**: ['NE10', 'NE11']
- **Contingent Outcomes**: []
- **Downstream Reactions (Excluded from Anchoring)**: ['NE12', 'NE13', 'NE14']

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N1: ongoing maintenance activity
- **Role**: `BACKGROUND`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`PRE_INTERVENTION`, extent=`INTERVAL`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Painters apply fresh plaster to hallway walls
  - *Level 1 (Domain)*: Apply material to walls
  - *Level 2 (Functional)*: ongoing maintenance activity
  - *Level 3 (Schema)*: BACKGROUND_ACTIVITY
- **Underlying Macro-Node**: `M1` (background preparation)
- **Source Normalized Events**: ['NE5']
- **Textual Provenance Spans**: ['painters applied fresh plaster to the hallway walls']

### N2: door opening event
- **Role**: `CAUSAL_ANTECEDENT`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Orderly opens heavy door
  - *Level 1 (Domain)*: Open door
  - *Level 2 (Functional)*: door opening event
  - *Level 3 (Schema)*: TRIGGER_EVENT
- **Underlying Macro-Node**: `M2` (door opening)
- **Source Normalized Events**: ['NE6']
- **Textual Provenance Spans**: ['an orderly opened the heavy door']

### N3: dust dispersion event
- **Role**: `CAUSAL_ANTECEDENT`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Draft blows plaster dust across room
  - *Level 1 (Domain)*: Blow dust across room
  - *Level 2 (Functional)*: dust dispersion event
  - *Level 3 (Schema)*: CONTAMINATION_VECTOR
- **Underlying Macro-Node**: `M3` (dust dispersion)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['a draft of wind blew plaster dust across the room']

### N4: food contamination event
- **Role**: `CAUSAL_ANTECEDENT`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Plaster dust contaminates Arthur's gingerbread
  - *Level 1 (Domain)*: Contaminate food
  - *Level 2 (Functional)*: food contamination event
  - *Level 3 (Schema)*: CONTAMINATION_EVENT
- **Underlying Macro-Node**: `M4` (food contamination)
- **Source Normalized Events**: ['NE8']
- **Textual Provenance Spans**: ["contaminating Arthur's gingerbread"]

### N5: food spoiled state
- **Role**: `PROBLEM_STATE`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Food is spoiled
  - *Level 1 (Domain)*: Food spoiled
  - *Level 2 (Functional)*: food spoiled state
  - *Level 3 (Schema)*: PROBLEM_STATE
- **Underlying Macro-Node**: `M5` (food spoiled state)
- **Source Normalized Events**: ['NE16']
- **Textual Provenance Spans**: ['the spoiled food']

### N6: instruction to discard and relocate `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Head nurse instructs Arthur to discard food and go to courtyard
  - *Level 1 (Domain)*: Instruct to discard and relocate
  - *Level 2 (Functional)*: instruction to discard and relocate
  - *Level 3 (Schema)*: INTERVENTION_INSTRUCTION
- **Underlying Macro-Node**: `M6` (instruction to discard and go outside)
- **Source Normalized Events**: ['NE9']
- **Textual Provenance Spans**: ['The head nurse told Arthur to discard the spoiled food']

### N7: discard spoiled food action `[FOCAL_OUTCOME]`
- **Role**: `ACTION_RESPONSE`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur discards spoiled food
  - *Level 1 (Domain)*: Discard spoiled food
  - *Level 2 (Functional)*: discard spoiled food action
  - *Level 3 (Schema)*: COMPLIANT_ACTION
- **Underlying Macro-Node**: `M7` (discard spoiled food)
- **Source Normalized Events**: ['NE10']
- **Textual Provenance Spans**: ['discard the spoiled food']

### N8: relocation to courtyard `[FOCAL_OUTCOME]`
- **Role**: `ACTION_RESPONSE`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur steps into courtyard
  - *Level 1 (Domain)*: Move to courtyard
  - *Level 2 (Functional)*: relocation to courtyard
  - *Level 3 (Schema)*: COMPLIANT_ACTION
- **Underlying Macro-Node**: `M8` (move to courtyard)
- **Source Normalized Events**: ['NE11']
- **Textual Provenance Spans**: ['step into the courtyard for fresh air']

## Explanatory Causal Edges (Mechanisms, Motivations, Consequences)
- **`N2` (door opening event)** `--CAUSES-->` **`N3` (dust dispersion event)**
  - *Underlying Rich Relations*: `['R1']`
  - *Justification*: When an orderly opened the heavy door, a draft of wind blew plaster dust across the room
- **`N3` (dust dispersion event)** `--CAUSES-->` **`N4` (food contamination event)**
  - *Underlying Rich Relations*: `['R2']`
  - *Justification*: a draft of wind blew plaster dust across the room, contaminating Arthur's gingerbread
- **`N4` (food contamination event)** `--RESULTS_IN-->` **`N5` (food spoiled state)**
  - *Underlying Rich Relations*: `['R3']`
  - *Justification*: contaminating Arthur's gingerbread. The head nurse told Arthur to discard the spoiled food
- **`N6` (instruction to discard and relocate)** `--CAUSES-->` **`N7` (discard spoiled food action)**
  - *Underlying Rich Relations*: `['R4']`
  - *Justification*: The head nurse told Arthur to discard the spoiled food and step into the courtyard for fresh air. Arthur sulked as he walked outside
- **`N6` (instruction to discard and relocate)** `--CAUSES-->` **`N8` (relocation to courtyard)**
  - *Underlying Rich Relations*: `['R5']`
  - *Justification*: The head nurse told Arthur to discard the spoiled food and step into the courtyard for fresh air. Arthur sulked as he walked outside
- **`N1` (ongoing maintenance activity)** `--ENABLES-->` **`N3` (dust dispersion event)**
  - *Underlying Rich Relations*: `['R10']`
  - *Justification*: Painters applied fresh plaster to hallway walls, which provided the plaster dust that was later blown by the draft.

## Minimal Temporal Constraints (Non-Redundant BEFORE Constraints)
- *(No independent temporal constraints)*

## Pruned Events (Audit Trail)
- **`NE1`**: Removing NE1 does not damage the explanation of the focal outcome because the preparation of the dining hall is a background setting that does not causally contribute to the contamination of Arthur's gingerbread or the subsequent intervention and outcomes.
- **`NE15`**: Removing NE15 does not damage the explanation because the repair of the cracked wall is a background activity that does not causally interact with the contamination of the gingerbread or the intervention; it is a separate, unrelated event.
- **`NE14`**: Removing NE14 does not damage the explanation because watching maintenance workers is a downstream collateral action that does not causally explain the central problem, intervention, or focal outcomes; it is an incidental observation after the main events.
- **`NE17`**: Removing NE17 does not damage the explanation because the cracked wall is a static background condition that does not causally contribute to the contamination or the intervention; the plaster dust comes from the painters' work (NE5), not from the crack itself.
- **`NE2`**: Removing NE2 does not damage the explanation because Arthur's preference for gingerbread is a static character trait that does not causally explain why the contamination occurred or why the intervention was necessary; the central problem is about the contamination itself, not his preference.
- **`NE3`**: Removing NE3 does not damage the explanation because Arthur's sitting in the corner is a spatial detail that does not causally affect the contamination event or the intervention; the contamination would occur regardless of his exact location within the room.
- **`NE12`**: Removing NE12 does not damage the explanation because Arthur's sulking is a downstream emotional reaction that does not causally affect the focal outcomes (discarding food and stepping into courtyard); it is a collateral consequence, not part of the explanatory mechanism.
- **`NE4`**: Removing NE4 does not damage the explanation because the fact that Arthur was eating a snack is not causally necessary for the contamination; the contamination of the gingerbread is the key event, and the eating activity is a secondary detail that does not alter the causal chain.
- **`NE13`**: Removing NE13 does not damage the explanation because 'walks outside' is redundant with NE11 (steps into courtyard) and is a secondary action detail; the focal outcome is captured by NE11, and removing NE13 does not break the causal chain.