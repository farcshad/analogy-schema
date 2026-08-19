# Causal Backbone: synth_story_01

## Narrative Anchors & Contracts
- **Central Problem**: William's room is a mess and he never passes monthly room inspections due to neglect and daydreaming.
- **Central Goal**: William must pass the April room inspection.
- **Intervention Events**: ['NE8']
- **Focal Outcomes**: ['NE11']
- **Contingent Outcomes**: ['NE12', 'NE15']
- **Downstream Reactions (Excluded from Anchoring)**: ['NE13', 'NE14']
- **Incentive Contracts**:
  - Reward: `gingerbread from the cookie shop` | Requirement: `scrub his room and put it in order once and for all` (Polarity: positive)

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N3: conditional incentive `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Nurse promises William gingerbread if he cleans his room
  - *Level 1 (Domain)*: nurse offers conditional reward
  - *Level 2 (Functional)*: conditional incentive
  - *Level 3 (Schema)*: intervention
- **Underlying Macro-Node**: `M3` (conditional incentive)
- **Source Normalized Events**: ['NE8']
- **Textual Provenance Spans**: ['if he scrubbed his room and put it in order once and for all', 'To provide William with an incentive', 'the nurse promised him some gingerbread from the cookie shop']

### N4: insufficient remaining resources
- **Role**: `CONSTRAINT`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: There is no longer enough time for William to clean his room
  - *Level 1 (Domain)*: time shortage prevents cleaning
  - *Level 2 (Functional)*: insufficient remaining resources
  - *Level 3 (Schema)*: constraint
- **Underlying Macro-Node**: `M4` (insufficient remaining resources)
- **Source Normalized Events**: ['NE10']
- **Textual Provenance Spans**: ['But there was no longer enough time for him to put it in order']

### N5: requirement failure `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William does not pass the inspection
  - *Level 1 (Domain)*: inspection failure
  - *Level 2 (Functional)*: requirement failure
  - *Level 3 (Schema)*: focal outcome
- **Underlying Macro-Node**: `M5` (requirement failure)
- **Source Normalized Events**: ['NE11']
- **Textual Provenance Spans**: ['he did not pass the inspection']

### N6: reward withheld `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William does not get any gingerbread
  - *Level 1 (Domain)*: reward not delivered
  - *Level 2 (Functional)*: reward withheld
  - *Level 3 (Schema)*: contingent outcome
- **Underlying Macro-Node**: `M6` (reward withheld)
- **Source Normalized Events**: ['NE12', 'NE15']
- **Textual Provenance Spans**: ["but he still didn't get any gingerbread", 'and did not get any gingerbread']

## Explanatory Causal Edges (Mechanisms, Motivations, Consequences)
- **`N4` (insufficient remaining resources)** `--CAUSES-->` **`N5` (requirement failure)**
  - *Underlying Rich Relations*: `['R3']`
  - *Justification*: There being no longer enough time to clean (NE10) causes William to not pass the inspection (NE11) as stated: 'But there was no longer enough time for him to put it in order. As a result, he did not pass the inspection'
- **`N5` (requirement failure)** `--RESULTS_IN-->` **`N6` (reward withheld)**
  - *Underlying Rich Relations*: `['R4']`
  - *Justification*: Not passing the inspection (NE11) results in William not getting any gingerbread (NE12) as stated: 'he did not pass the inspection and did not get any gingerbread'

## Minimal Temporal Constraints (Non-Redundant BEFORE Constraints)
- **`N3` (conditional incentive)** `--BEFORE-->` **`N4` (insufficient remaining resources)**
  - *Underlying Rich Relations*: `['R9']`
  - *Justification*: The nurse's promise (NE8) occurs before the realization that there is no longer enough time (NE10) as stated: 'But there was no longer enough time'

## Pruned Events (Audit Trail)
- **`NE4`**: William hating inspections is a secondary emotional state. Even if he did not hate them, the room would still be messy and time would still be insufficient, leading to the same outcome.
- **`NE2`**: Being confined indoors almost all the time is a chronic condition that does not causally explain why the room was messy or why time ran out. Removing it does not affect the explanation of the focal outcome.
- **`NE14`**: Slamming the door is an aggressive collateral action. Removing it does not change the fact that William failed the inspection and did not get gingerbread.
- **`NE1`**: William being a patient in a psychiatric hospital is a static background setting. Even if he were not a patient, the specific deficit (messy room) and intervention (gingerbread incentive) would still explain the failure to pass inspection and lack of gingerbread.
- **`NE3`**: The fact that William never passes monthly inspections is a past record, not a causal mechanism for this specific episode. The immediate cause of failure is the lack of time to clean, not his history.
- **`NE5`**: Daydreaming about food most of the time is a habitual state. The specific neglect (NE7) already captures the causal inaction; removing this does not alter the explanation.
- **`NE9`**: William being overjoyed is a transient emotional reaction to the intervention. Even if he were not overjoyed, the incentive was offered and the time constraint still prevented cleaning, so the outcome remains unchanged.
- **`NE13`**: Sulking all day is a downstream emotional reaction to the failure. It does not causally affect the focal outcome or contingent consequences.
- **`NE7`**: Pruned during final minimality pass: isolated CAUSAL_ANTECEDENT node 'task neglect' without explanatory connection to focal outcomes.
- **`NE6`**: Pruned during final minimality pass: isolated PROBLEM_STATE node 'performance deficit' without explanatory connection to focal outcomes.