# Causal Backbone: story_target_02

## Narrative Anchors & Contracts
- **Central Problem**: Karen is a high school student who dislikes school and maintains barely passing grades.
- **Central Goal**: Earn top marks on final graduation requirements.
- **Intervention Events**: ['NE2']
- **Focal Outcomes**: ['NE8']
- **Contingent Outcomes**: ['NE9', 'NE10', 'NE12']
- **Downstream Reactions (Excluded from Anchoring)**: ['NE11']
- **Incentive Contracts**:
  - Reward: `vacation to Hawaii` | Requirement: `earn top marks on final graduation requirements` (Polarity: positive)

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N1: conditional incentive `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Father promises Hawaii vacation conditional on top marks
  - *Level 1 (Domain)*: conditional reward offer
  - *Level 2 (Functional)*: conditional incentive
  - *Level 3 (Schema)*: conditional reward offer
- **Underlying Macro-Node**: `M1` (conditional incentive)
- **Source Normalized Events**: ['NE2']
- **Textual Provenance Spans**: ['if she earned top marks on her final graduation requirements', 'her father promised to pay for a vacation to Hawaii', 'A few weeks before the end of the term, her father promised to pay for a vacation to Hawaii if she earned top marks']

### N2: incentive reception
- **Role**: `ACTION_RESPONSE`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen receives the promise
  - *Level 1 (Domain)*: incentive reception
  - *Level 2 (Functional)*: incentive reception
  - *Level 3 (Schema)*: incentive reception
- **Underlying Macro-Node**: `M2` (incentive reception)
- **Source Normalized Events**: ['NE3']
- **Textual Provenance Spans**: ['After receiving this exciting promise']

### N3: obsessive preoccupation
- **Role**: `DOWNSTREAM_REACTION`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen becomes obsessed with Hawaii
  - *Level 1 (Domain)*: obsessive preoccupation
  - *Level 2 (Functional)*: obsessive preoccupation
  - *Level 3 (Schema)*: obsessive preoccupation
- **Underlying Macro-Node**: `M3` (obsessive preoccupation)
- **Source Normalized Events**: ['NE4']
- **Textual Provenance Spans**: ['Karen became so obsessed with the prospect of Hawaii']

### N4: task neglect
- **Role**: `ACTION_RESPONSE`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`INTERVAL`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen neglects studying to engage in vacation-related activities
  - *Level 1 (Domain)*: task neglect
  - *Level 2 (Functional)*: task neglect
  - *Level 3 (Schema)*: task neglect
- **Underlying Macro-Node**: `M4` (task neglect)
- **Source Normalized Events**: ['NE5']
- **Textual Provenance Spans**: ['instead of studying for her exams', 'making travel itineraries', 'daydreaming about the beach', 'she spent the remaining weeks shopping for summer clothes']

### N6: performance deficit
- **Role**: `PROBLEM_STATE`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen is unprepared for exams
  - *Level 1 (Domain)*: performance deficit
  - *Level 2 (Functional)*: performance deficit
  - *Level 3 (Schema)*: performance deficit
- **Underlying Macro-Node**: `M6` (performance deficit)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['she was completely unprepared']

### N7: requirement failure `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen fails final tests
  - *Level 1 (Domain)*: requirement failure
  - *Level 2 (Functional)*: requirement failure
  - *Level 3 (Schema)*: requirement failure
- **Underlying Macro-Node**: `M7` (requirement failure)
- **Source Normalized Events**: ['NE8']
- **Textual Provenance Spans**: ['Karen failed her final tests']

### N8: graduation denial `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen is denied graduation
  - *Level 1 (Domain)*: graduation denial
  - *Level 2 (Functional)*: graduation denial
  - *Level 3 (Schema)*: graduation denial
- **Underlying Macro-Node**: `M8` (graduation denial)
- **Source Normalized Events**: ['NE9']
- **Textual Provenance Spans**: ['was denied graduation']

### N9: reward withheld `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen does not receive the Hawaii trip
  - *Level 1 (Domain)*: reward withheld
  - *Level 2 (Functional)*: reward withheld
  - *Level 3 (Schema)*: reward withheld
- **Underlying Macro-Node**: `M9` (reward withheld)
- **Source Normalized Events**: ['NE10']
- **Textual Provenance Spans**: ['did not receive the trip to Hawaii']

### N10: vacation cancellation `[CONTINGENT_OUTCOME]`
- **Role**: `DOWNSTREAM_REACTION`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Vacation is canceled
  - *Level 1 (Domain)*: vacation cancellation
  - *Level 2 (Functional)*: vacation cancellation
  - *Level 3 (Schema)*: vacation cancellation
- **Underlying Macro-Node**: `M10` (vacation cancellation)
- **Source Normalized Events**: ['NE12']
- **Textual Provenance Spans**: ['the vacation was canceled']

## Explanatory Causal Edges (Mechanisms, Motivations, Consequences)
- **`N1` (conditional incentive)** `--CAUSES-->` **`N2` (incentive reception)**
  - *Underlying Rich Relations*: `['R1']`
  - *Justification*: Father promises Hawaii vacation conditional on top marks; Karen receives the promise.
- **`N2` (incentive reception)** `--CAUSES-->` **`N3` (obsessive preoccupation)**
  - *Underlying Rich Relations*: `['R2']`
  - *Justification*: After receiving this exciting promise, Karen became so obsessed with the prospect of Hawaii.
- **`N3` (obsessive preoccupation)** `--CAUSES-->` **`N4` (task neglect)**
  - *Underlying Rich Relations*: `['R3']`
  - *Justification*: Karen became so obsessed with the prospect of Hawaii that she spent the remaining weeks shopping for summer clothes, making travel itineraries, and daydreaming about the beach instead of studying for her exams.
- **`N4` (task neglect)** `--CAUSES-->` **`N6` (performance deficit)**
  - *Underlying Rich Relations*: `['R4']`
  - *Justification*: Karen neglected studying to engage in vacation-related activities, leading to being unprepared for exams.
- **`N6` (performance deficit)** `--CAUSES-->` **`N7` (requirement failure)**
  - *Underlying Rich Relations*: `['R6']`
  - *Justification*: Karen was completely unprepared for exams, and as a result failed her final tests.
- **`N7` (requirement failure)** `--RESULTS_IN-->` **`N8` (graduation denial)**
  - *Underlying Rich Relations*: `['R7']`
  - *Justification*: Karen failed her final tests, and was denied graduation.
- **`N7` (requirement failure)** `--RESULTS_IN-->` **`N9` (reward withheld)**
  - *Underlying Rich Relations*: `['R8']`
  - *Justification*: Karen failed her final tests, and did not receive the trip to Hawaii.
- **`N9` (reward withheld)** `--RESULTS_IN-->` **`N10` (vacation cancellation)**
  - *Underlying Rich Relations*: `['R10']`
  - *Justification*: Karen did not receive the trip, and the vacation was canceled.

## Minimal Temporal Constraints (Non-Redundant BEFORE Constraints)
- *(No independent temporal constraints)*

## Pruned Events (Audit Trail)
- **`NE11`**: Karen's angry argument with her father is a downstream emotional reaction and collateral action, not causally necessary to explain the focal outcomes (failure, denied graduation, canceled trip). Removing it does not affect the explanatory mechanism of how the intervention led to failure.
- **`NE1`**: Karen's chronic poor academic engagement and low grades are a background state that does not causally explain the specific focal episode. The intervention (promise of Hawaii) and subsequent obsession directly cause the neglect of studying, leading to failure. Removing NE1 does not damage the explanation because the causal chain from incentive to neglect to failure is sufficient.
- **`NE6`**: Pruned during final minimality pass: isolated CONSTRAINT node 'exam arrival' without explanatory connection to focal outcomes.

## Validation Warnings
- ⚠️ Anchor Role Conflict: Node N3 marked DOWNSTREAM_REACTION has outgoing explanatory edge(s) ['BE3'] to N4.