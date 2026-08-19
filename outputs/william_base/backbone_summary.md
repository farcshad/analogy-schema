# Causal Backbone: william_base

## Narrative Anchors & Contracts
- **Central Problem**: William never passes monthly room inspections and his room is a mess a few days before the April inspection.
- **Central Goal**: Pass the April room inspection by cleaning the room.
- **Intervention Events**: ['NE7']
- **Focal Outcomes**: ['NE10']
- **Contingent Outcomes**: ['NE11']
- **Downstream Reactions (Excluded from Anchoring)**: ['NE12', 'NE13']
- **Incentive Contracts**:
  - Reward: `gingerbread from the cookie shop` | Requirement: `scrub his room and put it in order once and for all` (Polarity: positive)

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N1: task neglect
- **Role**: `BACKGROUND`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`PRE_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William spends time daydreaming about food instead of cleaning
  - *Level 1 (Domain)*: Patient daydreams about food
  - *Level 2 (Functional)*: task neglect
  - *Level 3 (Schema)*: Neglect of Required Task
- **Underlying Macro-Node**: `M1` (William's confinement and daydreaming)
- **Source Normalized Events**: ['NE5']
- **Textual Provenance Spans**: ['he had done nothing but daydream', 'He spent most of his time daydreaming about food']

### N2: deficit state
- **Role**: `PROBLEM_STATE`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`PRE_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William's room is a mess a few days before the April inspection
  - *Level 1 (Domain)*: Room is untidy before inspection
  - *Level 2 (Functional)*: deficit state
  - *Level 3 (Schema)*: Unresolved Deficit
- **Underlying Macro-Node**: `M2` (William's room is a mess)
- **Source Normalized Events**: ['NE6']
- **Textual Provenance Spans**: ["A few days before the April inspection William's room was still a mess"]

### N3: conditional incentive `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Nurse promises William gingerbread if he cleans his room
  - *Level 1 (Domain)*: Nurse offers conditional reward
  - *Level 2 (Functional)*: conditional incentive
  - *Level 3 (Schema)*: Conditional Incentive Offer
- **Underlying Macro-Node**: `M3` (Nurse promises gingerbread as incentive)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['the nurse promised him some gingerbread from the cookie shop', 'if he scrubbed his room', 'To provide William with an incentive', 'and put it in order once and for all']

### N4: insufficient remaining resources
- **Role**: `CONSTRAINT`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: There is no longer enough time for William to clean his room
  - *Level 1 (Domain)*: Time runs out for cleaning
  - *Level 2 (Functional)*: insufficient remaining resources
  - *Level 3 (Schema)*: Resource Constraint
- **Underlying Macro-Node**: `M4` (Insufficient time to clean)
- **Source Normalized Events**: ['NE9']
- **Textual Provenance Spans**: ['But there was no longer enough time for him to put it in order']

### N5: requirement failure `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William does not pass the April inspection
  - *Level 1 (Domain)*: Patient fails inspection
  - *Level 2 (Functional)*: requirement failure
  - *Level 3 (Schema)*: Failure to Meet Requirement
- **Underlying Macro-Node**: `M5` (William fails inspection)
- **Source Normalized Events**: ['NE10']
- **Textual Provenance Spans**: ['he did not pass the inspection']

### N6: reward withheld `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William does not get any gingerbread
  - *Level 1 (Domain)*: Reward withheld
  - *Level 2 (Functional)*: reward withheld
  - *Level 3 (Schema)*: Withheld Contingent Reward
- **Underlying Macro-Node**: `M6` (William does not get gingerbread)
- **Source Normalized Events**: ['NE11']
- **Textual Provenance Spans**: ["he still didn't get any gingerbread", 'and did not get any gingerbread']

### N7: chronic failure
- **Role**: `BACKGROUND`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`PRE_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William never passes monthly room inspections
  - *Level 1 (Domain)*: Patient chronically fails inspections
  - *Level 2 (Functional)*: chronic failure
  - *Level 3 (Schema)*: Chronic Failure Pattern
- **Underlying Macro-Node**: `M7` (William never passes inspections)
- **Source Normalized Events**: ['NE3']
- **Textual Provenance Spans**: ['He could never pass the monthly room inspections']

## Backbone Edges (Typed Relational Backbone with Provenance)
- **`N1` (task neglect)** `--CAUSES-->` **`N2` (deficit state)**
  - *Underlying Rich Relations*: `['R3']`
  - *Justification*: William's daydreaming instead of cleaning directly results in his room being a mess a few days before the April inspection.
- **`N2` (deficit state)** `--MOTIVATES-->` **`N3` (conditional incentive)**
  - *Underlying Rich Relations*: `['R4']`
  - *Justification*: The mess in William's room motivates the nurse to promise gingerbread as an incentive for him to clean.
- **`N2` (deficit state)** `--CAUSES-->` **`N4` (insufficient remaining resources)**
  - *Underlying Rich Relations*: `['R6']`
  - *Justification*: The room being a mess and the lateness of the intervention imply that there is no longer enough time for William to clean it before the inspection.
- **`N4` (insufficient remaining resources)** `--CAUSES-->` **`N5` (requirement failure)**
  - *Underlying Rich Relations*: `['R7']`
  - *Justification*: Because there is no longer enough time to clean, William does not pass the April inspection.
- **`N5` (requirement failure)** `--CAUSES-->` **`N6` (reward withheld)**
  - *Underlying Rich Relations*: `['R8']`
  - *Justification*: Failing the inspection directly leads to William not getting any gingerbread, as the promise was conditional on passing.
- **`N3` (conditional incentive)** `--BEFORE-->` **`N4` (insufficient remaining resources)**
  - *Underlying Rich Relations*: `['R13']`
  - *Justification*: The promise occurs before the realization that there is no longer enough time, but the promise does not cause the time shortage.

## Pruned Events (Audit Trail)
- **`NE4`**: William hating inspections is a secondary emotional reaction to his chronic failure. It does not causally explain the origin of the deficit, the intervention, or the failure outcome. Even if he were indifferent, the same events (messy room, incentive, time shortage) would lead to the same outcome. Thus, NE4 is pruned.
- **`NE1`**: William being a patient in a psychiatric hospital is a static background setting. Even if he were not a patient (e.g., a resident in a group home), the specific deficit (messy room) and incentive (gingerbread) would still explain the failure. Thus, removing NE1 does not damage the explanation of the focal outcome.
- **`NE12`**: William sulking all day is a downstream emotional reaction to the failure and does not causally explain the focal outcome or contingent consequence. The failure and lack of gingerbread are already explained without this reaction. Thus, NE12 is pruned.
- **`NE8`**: William being overjoyed is a transient emotional reaction to the incentive. It does not causally affect the subsequent resource shortage or failure. Removing NE8 does not break the explanatory chain from the incentive to the lack of time to the failure.
- **`NE2`**: William being confined indoors almost all the time is a chronic background condition. The narrative's focal episode is about a specific inspection and incentive; confinement does not causally explain why he failed to clean in time. Removing NE2 does not alter the causal chain from deficit to intervention to resource shortage to failure.
- **`NE13`**: William slamming his door is a collateral aggressive action after the outcome. It does not causally explain why he failed or why he did not get gingerbread. Removing NE13 does not affect the explanation of the focal or contingent outcomes.