# Causal Backbone: story_target_04

## Narrative Anchors & Contracts
- **Central Problem**: Arthur is a resident confined indoors in a psychiatric hospital
- **Central Goal**: Arthur must help scrub the recreation hall floors before gingerbread is distributed
- **Intervention Events**: ['NE2', 'NE3']
- **Focal Outcomes**: ['NE7', 'NE8']
- **Contingent Outcomes**: ['NE11']
- **Downstream Reactions (Excluded from Anchoring)**: ['NE9', 'NE10']
- **Incentive Contracts**:
  - Reward: `fresh gingerbread` | Requirement: `help scrub recreation hall floors before gingerbread distribution` (Polarity: positive)

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N2: conditional incentive `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: The ward matron announced that fresh gingerbread from the local bakery had arrived for the patients.
  - *Level 1 (Domain)*: incentive introduction
  - *Level 2 (Functional)*: conditional incentive
  - *Level 3 (Schema)*: incentive offer
- **Underlying Macro-Node**: `M2` (incentive announcement)
- **Source Normalized Events**: ['NE2']
- **Textual Provenance Spans**: ['fresh gingerbread from the local bakery had arrived for the patients', 'The ward matron announced that fresh gingerbread from the local bakery had arrived for the patients']

### N3: task assignment `[INTERVENTION]`
- **Role**: `GOAL`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`INTERVAL`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur was asked to help the cleaning staff scrub the recreation hall floors before the dessert was distributed.
  - *Level 1 (Domain)*: assigned cleaning task
  - *Level 2 (Functional)*: task assignment
  - *Level 3 (Schema)*: goal setting
- **Underlying Macro-Node**: `M3` (task assignment)
- **Source Normalized Events**: ['NE3']
- **Textual Provenance Spans**: ['scrub the recreation hall floors', 'before the dessert was distributed', 'Arthur was asked to help the cleaning staff scrub the recreation hall floors before the dessert was distributed']

### N4: task neglect
- **Role**: `CAUSAL_ANTECEDENT`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur became distracted daydreaming about the gingerbread while working.
  - *Level 1 (Domain)*: distraction during task
  - *Level 2 (Functional)*: task neglect
  - *Level 3 (Schema)*: attention failure
- **Underlying Macro-Node**: `M4` (task neglect)
- **Source Normalized Events**: ['NE4']
- **Textual Provenance Spans**: ['While working, Arthur became distracted daydreaming about the gingerbread', 'daydreaming about the gingerbread']

### N5: accidental action
- **Role**: `ACTION_RESPONSE`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur accidentally spills bucket of soapy water across clean floor.
  - *Level 1 (Domain)*: accidental spill
  - *Level 2 (Functional)*: accidental action
  - *Level 3 (Schema)*: unintended action
- **Underlying Macro-Node**: `M5` (accidental spill)
- **Source Normalized Events**: ['NE5']
- **Textual Provenance Spans**: ['accidentally spilled a bucket of soapy water across the clean floor']

### N6: cleanup action
- **Role**: `ACTION_RESPONSE`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`INTERVAL`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Mess is mopped up.
  - *Level 1 (Domain)*: spill cleanup
  - *Level 2 (Functional)*: cleanup action
  - *Level 3 (Schema)*: remedial action
- **Underlying Macro-Node**: `M6` (cleanup)
- **Source Normalized Events**: ['NE6']
- **Textual Provenance Spans**: ['the mess was mopped up']

### N7: criteria failure `[FOCAL_OUTCOME]`
- **Role**: `PROBLEM_STATE`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Inspection of recreation hall is delayed.
  - *Level 1 (Domain)*: inspection delay
  - *Level 2 (Functional)*: criteria failure
  - *Level 3 (Schema)*: schedule disruption
- **Underlying Macro-Node**: `M7` (inspection delay)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['the inspection of the recreation hall was delayed']

### N8: resource shortage `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Gingerbread distributed to other patients, Arthur misses out.
  - *Level 1 (Domain)*: resource distribution exclusion
  - *Level 2 (Functional)*: resource shortage
  - *Level 3 (Schema)*: outcome deprivation
- **Underlying Macro-Node**: `M8` (resource shortage)
- **Source Normalized Events**: ['NE8']
- **Textual Provenance Spans**: ['the gingerbread had already been distributed to the other patients']

### N9: missed opportunity `[CONTINGENT_OUTCOME]`
- **Role**: `DOWNSTREAM_REACTION`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur missed out on gingerbread.
  - *Level 1 (Domain)*: missed reward opportunity
  - *Level 2 (Functional)*: missed opportunity
  - *Level 3 (Schema)*: outcome deprivation
- **Underlying Macro-Node**: `M9` (missed opportunity)
- **Source Normalized Events**: ['NE11']
- **Textual Provenance Spans**: ['having missed out on the gingerbread']

## Explanatory Causal Edges (Mechanisms, Motivations, Consequences)
- **`N4` (task neglect)** `--CAUSES-->` **`N5` (accidental action)**
  - *Underlying Rich Relations*: `['R1']`
  - *Justification*: Arthur became distracted daydreaming about the gingerbread while working and accidentally spilled a bucket of soapy water across the clean floor.
- **`N5` (accidental action)** `--CAUSES-->` **`N6` (cleanup action)**
  - *Underlying Rich Relations*: `['R2']`
  - *Justification*: The spill of soapy water necessitated mopping up the mess.
- **`N6` (cleanup action)** `--CAUSES-->` **`N7` (criteria failure)**
  - *Underlying Rich Relations*: `['R3']`
  - *Justification*: Mopping the mess took time, which delayed the inspection of the recreation hall.
- **`N7` (criteria failure)** `--CAUSES-->` **`N8` (resource shortage)**
  - *Underlying Rich Relations*: `['R4']`
  - *Justification*: The delay in inspection meant the gingerbread distribution occurred before Arthur could get any, causing him to miss out.
- **`N8` (resource shortage)** `--RESULTS_IN-->` **`N9` (missed opportunity)**
  - *Underlying Rich Relations*: `['R7']`
  - *Justification*: The gingerbread being distributed to other patients directly resulted in Arthur missing out on the gingerbread.

## Minimal Temporal Constraints (Non-Redundant BEFORE Constraints)
- **`N3` (task assignment)** `--BEFORE-->` **`N4` (task neglect)**
  - *Underlying Rich Relations*: `['R8']`
  - *Justification*: Arthur was asked to help scrub floors before he became distracted while working.
- **`N2` (conditional incentive)** `--BEFORE-->` **`N3` (task assignment)**
  - *Underlying Rich Relations*: `['R9']`
  - *Justification*: The announcement of gingerbread occurred before Arthur was asked to help scrub floors.

## Pruned Events (Audit Trail)
- **`NE9`**: Arthur's fury is a secondary emotional reaction to missing the gingerbread. Even if he had not become furious, the focal outcome (inspection delayed, gingerbread distributed to others) and the contingent outcome (Arthur missed out) would still be fully explained by the preceding causal chain. Thus, NE9 is not causally necessary.
- **`NE10`**: Slamming the dining hall door is a downstream collateral action expressing anger. Its removal does not alter the explanation of how the inspection was delayed, how the gingerbread was distributed to others, or why Arthur missed out. The causal backbone remains intact without this reaction.
- **`NE1`**: Pruned during final minimality pass: isolated BACKGROUND node 'confinement state' without explanatory connection to focal outcomes.