# Causal Backbone: story_base_01

## Narrative Anchors & Contracts
- **Central Problem**: William's room is a mess and he never passes monthly room inspections.
- **Central Goal**: Pass the April inspection by cleaning his room.
- **Intervention Events**: ['NE7']
- **Focal Outcomes**: ['NE10']
- **Contingent Outcomes**: ['NE11']
- **Downstream Reactions (Excluded from Anchoring)**: ['NE12', 'NE13']
- **Incentive Contracts**:
  - Reward: `gingerbread from the cookie shop` | Requirement: `scrub his room and put it in order once and for all` (Polarity: positive)

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N2: conditional incentive `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Nurse promises William gingerbread if he cleans his room
  - *Level 1 (Domain)*: conditional reward offer
  - *Level 2 (Functional)*: conditional incentive
  - *Level 3 (Schema)*: Incentive Intervention
- **Underlying Macro-Node**: `M2` (conditional incentive)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['the nurse promised him some gingerbread from the cookie shop', 'if he scrubbed his room and put it in order once and for all', 'To provide William with an incentive']

### N3: insufficient remaining resources
- **Role**: `CONSTRAINT`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Not enough time for William to clean room
  - *Level 1 (Domain)*: time shortage
  - *Level 2 (Functional)*: insufficient remaining resources
  - *Level 3 (Schema)*: Resource Constraint
- **Underlying Macro-Node**: `M3` (insufficient time)
- **Source Normalized Events**: ['NE9']
- **Textual Provenance Spans**: ['But there was no longer enough time for him to put it in order']

### N4: requirement failure `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William does not pass inspection
  - *Level 1 (Domain)*: failed room inspection
  - *Level 2 (Functional)*: requirement failure
  - *Level 3 (Schema)*: Outcome Failure
- **Underlying Macro-Node**: `M4` (inspection failure)
- **Source Normalized Events**: ['NE10']
- **Textual Provenance Spans**: ['he did not pass the inspection']

### N5: reward withheld `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William does not get gingerbread
  - *Level 1 (Domain)*: reward not delivered
  - *Level 2 (Functional)*: reward withheld
  - *Level 3 (Schema)*: Contingent Outcome
- **Underlying Macro-Node**: `M5` (reward withheld)
- **Source Normalized Events**: ['NE11']
- **Textual Provenance Spans**: ['and did not get any gingerbread', "but he still didn't get any gingerbread"]

## Explanatory Causal Edges (Mechanisms, Motivations, Consequences)
- **`N3` (insufficient remaining resources)** `--CAUSES-->` **`N4` (requirement failure)**
  - *Underlying Rich Relations*: `['R2', 'R10']`
  - *Justification*: But there was no longer enough time for him to put it in order. As a result, he did not pass the inspection; Temporal order: not enough time precedes failing inspection, but causal link already captured in R2. [Adjudicated between BEFORE, CAUSES: prioritized CAUSES.]
- **`N4` (requirement failure)** `--RESULTS_IN-->` **`N5` (reward withheld)**
  - *Underlying Rich Relations*: `['R3']`
  - *Justification*: he did not pass the inspection and did not get any gingerbread.

## Minimal Temporal Constraints (Non-Redundant BEFORE Constraints)
- **`N2` (conditional incentive)** `--BEFORE-->` **`N3` (insufficient remaining resources)**
  - *Underlying Rich Relations*: `['R9']`
  - *Justification*: A few days before the April inspection... the nurse promised him... But there was no longer enough time

## Pruned Events (Audit Trail)
- **`NE1`**: William being a patient in a psychiatric hospital is a static background setting. Removing it does not affect the explanation of why his room was messy or why the incentive failed, as the specific deficit (NE6) and resource shortage (NE9) already capture the causal mechanism.
- **`NE5`**: Daydreaming about food is a specific neglect behavior that leads to the messy room (NE6), but NE6 already captures the deficit state. Pruning NE5 does not remove the causal link because NE6 is retained and directly explains the need for intervention.
- **`NE2`**: William being confined indoors is a chronic condition that does not directly cause the specific failure to clean or the lack of time. Its removal does not alter the causal chain from the messy room to the failed inspection.
- **`NE3`**: The general fact that William never passes inspections is a habitual past record. The focal outcome (NE10) is specifically about the April inspection; the immediate cause is the messy room (NE6) and insufficient time (NE9), not the past record.
- **`NE12`**: Sulking all day is a downstream emotional reaction to the failure. It is not causally necessary to explain the focal outcome (NE10) or contingent outcome (NE11).
- **`NE4`**: William hating inspections is an emotional state that does not causally explain the failure to clean or the outcome. Removing it does not break the explanation of why he failed or why he did not get gingerbread.
- **`NE8`**: William being overjoyed is a secondary emotional reaction to the incentive. It does not causally affect the outcome (failure due to lack of time). Removing it does not damage the explanation of why the incentive failed.
- **`NE13`**: Slamming the door is a collateral aggressive action that does not affect the causal chain from the incentive to the failure. Its removal does not alter the explanation of why William did not get gingerbread.
- **`NE6`**: Pruned during final minimality pass: isolated PROBLEM_STATE node 'task neglect' without explanatory connection to focal outcomes.