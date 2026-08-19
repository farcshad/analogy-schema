# Causal Backbone: story_target_01

## Narrative Anchors & Contracts
- **Central Problem**: Karen is struggling academically and at risk of not graduating due to neglecting coursework for months, with grades far below the graduation requirement.
- **Central Goal**: Karen must study diligently and pass all remaining courses to graduate.
- **Intervention Events**: ['NE7']
- **Focal Outcomes**: ['NE11', 'NE12']
- **Contingent Outcomes**: ['NE13', 'NE15']
- **Downstream Reactions (Excluded from Anchoring)**: ['NE14']
- **Incentive Contracts**:
  - Reward: `all-expenses-paid trip to Hawaii` | Requirement: `study diligently and pass all remaining courses` (Polarity: positive)

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N1: task neglect
- **Role**: `CAUSAL_ANTECEDENT`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`False`, mention=`PRE_INTERVENTION`, extent=`INTERVAL`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen neglects coursework for months
  - *Level 1 (Domain)*: student neglects academic tasks
  - *Level 2 (Functional)*: task neglect
  - *Level 3 (Schema)*: antecedent neglect
- **Underlying Macro-Node**: `M1` (task neglect)
- **Source Normalized Events**: ['NE4']
- **Textual Provenance Spans**: ['she had neglected her coursework for months']

### N2: performance deficit
- **Role**: `PROBLEM_STATE`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`PRE_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen's grades are far below graduation requirement
  - *Level 1 (Domain)*: grades below requirement
  - *Level 2 (Functional)*: performance deficit
  - *Level 3 (Schema)*: deficit state
- **Underlying Macro-Node**: `M2` (performance deficit)
- **Source Normalized Events**: ['NE6']
- **Textual Provenance Spans**: ['A few weeks before final exams, her grades were far below the graduation requirement']

### N3: cumulative deficit too severe
- **Role**: `PROBLEM_STATE`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`POST_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Cumulative academic deficit is too severe
  - *Level 1 (Domain)*: cumulative deficit exceeds threshold
  - *Level 2 (Functional)*: cumulative deficit too severe
  - *Level 3 (Schema)*: irreversible deficit
- **Underlying Macro-Node**: `M3` (cumulative deficit too severe)
- **Source Normalized Events**: ['NE9']
- **Textual Provenance Spans**: ['the cumulative academic deficit was already too severe']

### N4: insufficient remaining resources
- **Role**: `CONSTRAINT`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`POST_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Not enough time left to catch up
  - *Level 1 (Domain)*: insufficient time to remediate
  - *Level 2 (Functional)*: insufficient remaining resources
  - *Level 3 (Schema)*: resource constraint
- **Underlying Macro-Node**: `M4` (insufficient remaining resources)
- **Source Normalized Events**: ['NE10']
- **Textual Provenance Spans**: ['there was not enough time left in the semester to catch up on the coursework']

### N5: conditional incentive `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Father promises Hawaii trip if Karen studies and passes courses
  - *Level 1 (Domain)*: conditional reward offered for performance
  - *Level 2 (Functional)*: conditional incentive
  - *Level 3 (Schema)*: incentive intervention
- **Underlying Macro-Node**: `M5` (conditional incentive)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['if she studied diligently', 'To encourage her to pass', 'passed all her remaining courses', 'her father promised to pay for an all-expenses-paid trip to Hawaii']

### N6: requirement failure `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen fails final exams
  - *Level 1 (Domain)*: student fails exams
  - *Level 2 (Functional)*: requirement failure
  - *Level 3 (Schema)*: outcome failure
- **Underlying Macro-Node**: `M6` (requirement failure)
- **Source Normalized Events**: ['NE11']
- **Textual Provenance Spans**: ['Karen failed her final exams']

### N7: graduation failure `[FOCAL_OUTCOME]` `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen does not graduate
  - *Level 1 (Domain)*: student does not graduate
  - *Level 2 (Functional)*: graduation failure
  - *Level 3 (Schema)*: contingent outcome
- **Underlying Macro-Node**: `M7` (graduation failure)
- **Source Normalized Events**: ['NE12']
- **Textual Provenance Spans**: ['did not graduate with her class']

### N8: reward withheld `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen does not receive the trip to Hawaii
  - *Level 1 (Domain)*: reward not delivered
  - *Level 2 (Functional)*: reward withheld
  - *Level 3 (Schema)*: contingent outcome
- **Underlying Macro-Node**: `M8` (reward withheld)
- **Source Normalized Events**: ['NE13']
- **Textual Provenance Spans**: ['did not receive the trip to Hawaii']

### N9: consequence enacted `[CONTINGENT_OUTCOME]`
- **Role**: `DOWNSTREAM_REACTION`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Father does not purchase plane tickets
  - *Level 1 (Domain)*: father withholds reward
  - *Level 2 (Functional)*: consequence enacted
  - *Level 3 (Schema)*: downstream reaction
- **Underlying Macro-Node**: `M9` (consequence enacted)
- **Source Normalized Events**: ['NE15']
- **Textual Provenance Spans**: ['her father did not purchase the plane tickets']

## Explanatory Causal Edges (Mechanisms, Motivations, Consequences)
- **`N1` (task neglect)** `--CAUSES-->` **`N2` (performance deficit)**
  - *Underlying Rich Relations*: `['R1']`
  - *Justification*: Karen neglected her coursework for months, which directly caused her grades to be far below the graduation requirement.
- **`N3` (cumulative deficit too severe)** `--CAUSES-->` **`N4` (insufficient remaining resources)**
  - *Underlying Rich Relations*: `['R4']`
  - *Justification*: The cumulative academic deficit being too severe caused there not to be enough time left to catch up.
- **`N4` (insufficient remaining resources)** `--CAUSES-->` **`N6` (requirement failure)**
  - *Underlying Rich Relations*: `['R5']`
  - *Justification*: Not having enough time to catch up caused Karen to fail her final exams.
- **`N6` (requirement failure)** `--RESULTS_IN-->` **`N7` (graduation failure)**
  - *Underlying Rich Relations*: `['R6']`
  - *Justification*: Failing final exams directly resulted in not graduating.
- **`N7` (graduation failure)** `--RESULTS_IN-->` **`N8` (reward withheld)**
  - *Underlying Rich Relations*: `['R7']`
  - *Justification*: Not graduating resulted in not receiving the trip to Hawaii.
- **`N8` (reward withheld)** `--RESULTS_IN-->` **`N9` (consequence enacted)**
  - *Underlying Rich Relations*: `['R9']`
  - *Justification*: Karen not receiving the trip resulted in the father not purchasing plane tickets.

## Minimal Temporal Constraints (Non-Redundant BEFORE Constraints)
- **`N5` (conditional incentive)** `--BEFORE-->` **`N6` (requirement failure)**
  - *Underlying Rich Relations*: `['R11']`
  - *Justification*: The father's promise occurred before the final exams, but did not cause the failure; the deficit caused the failure.
- **`N2` (performance deficit)** `--BEFORE-->` **`N3` (cumulative deficit too severe)**
  - *Underlying Rich Relations*: `['R13']`
  - *Justification*: The grades being far below requirement is a state that persisted and is later described as a cumulative deficit, but the narrative does not explicitly state a causal link between the two descriptions.

## Pruned Events (Audit Trail)
- **`NE1`**: Karen being a high school student is a static background setting. Removing it does not affect the causal explanation of the focal outcomes because the academic deficit and risk are already captured by NE4, NE6, NE9, and NE10.
- **`NE5`**: Daydreaming about Hawaii is a specific habitual behavior that explains why Karen neglected coursework, but the neglect itself (NE4) is sufficient to explain the deficit. Removing NE5 does not break the causal path to failure.
- **`NE14`**: Crying in the bedroom is a downstream emotional reaction to the focal outcomes. It is not causally necessary to explain the failure or the contingent outcomes. Removing it does not affect the causal backbone.
- **`NE2`**: Struggling academically is a chronic state that is redundant with the more specific deficit states (NE6, NE9) and neglect (NE4). Its removal does not damage the explanation of failure.
- **`NE3`**: Being at risk of not graduating is a summary of the deficit and time shortage. It is causally downstream of NE4, NE6, NE9, NE10 and upstream of NE11/NE12, but not necessary as a separate node; the causal chain from deficit to failure is complete without it.
- **`NE8`**: Karen being thrilled is a secondary emotional reaction to the intervention. It does not causally affect the outcome because the deficit and time shortage are immutable. Removing it does not alter the explanation of failure.