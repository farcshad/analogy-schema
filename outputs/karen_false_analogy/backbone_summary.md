# Causal Backbone: karen_false_analogy

## Narrative Anchors & Contracts
- **Central Problem**: Karen dislikes school and is doing poorly
- **Central Goal**: Karen graduates
- **Intervention Events**: ['NE3']
- **Focal Outcomes**: ['NE6']
- **Contingent Outcomes**: ['NE7']
- **Downstream Reactions (Excluded from Anchoring)**: ['NE5']
- **Incentive Contracts**:
  - Reward: `Hawaii trip` | Requirement: `Karen graduates` (Polarity: positive)

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N1: Karen dislikes school
- **Role**: `PROBLEM_STATE`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`PRE_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen dislikes school
  - *Level 1 (Domain)*: Karen dislikes school
  - *Level 2 (Functional)*: Karen dislikes school
  - *Level 3 (Schema)*: baseline deficiency
- **Underlying Macro-Node**: `M1_split_1` (Karen dislikes school)
- **Source Normalized Events**: ['NE1']
- **Textual Provenance Spans**: ['Karen dislikes school and is doing poorly', 'Karen dislikes school']

### N2: Karen is doing poorly in school
- **Role**: `PROBLEM_STATE`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`PRE_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen is doing poorly in school
  - *Level 1 (Domain)*: Karen is doing poorly in school
  - *Level 2 (Functional)*: Karen is doing poorly in school
  - *Level 3 (Schema)*: baseline deficiency
- **Underlying Macro-Node**: `M1_split_2` (Karen is doing poorly in school)
- **Source Normalized Events**: ['NE2']
- **Textual Provenance Spans**: ['is doing poorly', 'Karen dislikes school and is doing poorly']

### N3: conditional incentive `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Father promises Hawaii trip if Karen graduates.
  - *Level 1 (Domain)*: parental conditional reward promise
  - *Level 2 (Functional)*: conditional incentive
  - *Level 3 (Schema)*: incentive intervention
- **Underlying Macro-Node**: `M2` (conditional incentive introduction)
- **Source Normalized Events**: ['NE3']
- **Textual Provenance Spans**: ['Her father promises a Hawaii trip if she graduates']

### N4: incentive reception
- **Role**: `ACTION_RESPONSE`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen receives the incentive.
  - *Level 1 (Domain)*: student receives promised reward
  - *Level 2 (Functional)*: incentive reception
  - *Level 3 (Schema)*: reward uptake
- **Underlying Macro-Node**: `M3` (incentive reception)
- **Source Normalized Events**: ['NE4']
- **Textual Provenance Spans**: ['After receiving the incentive', 'After receiving the incentive, she spends the remaining weeks dreaming about Hawaii and preparing for the trip instead of studying']

### N5: task neglect
- **Role**: `ACTION_RESPONSE`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`INTERVAL`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen spends time dreaming about Hawaii and preparing for trip instead of studying.
  - *Level 1 (Domain)*: student engages in reward-related activities instead of studying
  - *Level 2 (Functional)*: task neglect
  - *Level 3 (Schema)*: goal displacement
- **Underlying Macro-Node**: `M4` (task neglect)
- **Source Normalized Events**: ['NE5']
- **Textual Provenance Spans**: ['preparing for the trip', 'she spends the remaining weeks dreaming about Hawaii', 'instead of studying', 'After receiving the incentive, she spends the remaining weeks dreaming about Hawaii and preparing for the trip instead of studying']

### N6: requirement failure `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen fails to graduate.
  - *Level 1 (Domain)*: student fails to meet graduation requirement
  - *Level 2 (Functional)*: requirement failure
  - *Level 3 (Schema)*: outcome failure
- **Underlying Macro-Node**: `M5` (requirement failure)
- **Source Normalized Events**: ['NE6']
- **Textual Provenance Spans**: ['She then fails to graduate and does not go to Hawaii', 'She then fails to graduate']

### N7: reward withheld `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen does not go to Hawaii.
  - *Level 1 (Domain)*: student does not receive promised trip
  - *Level 2 (Functional)*: reward withheld
  - *Level 3 (Schema)*: contingent consequence
- **Underlying Macro-Node**: `M6` (reward withheld)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['She then fails to graduate and does not go to Hawaii', 'does not go to Hawaii']

## Backbone Edges (Typed Relational Backbone with Provenance)
- **`N1` (Karen dislikes school)** `--CAUSES-->` **`N2` (Karen is doing poorly in school)**
  - *Underlying Rich Relations*: `['R1']`
  - *Justification*: Karen's dislike of school is a plausible cause for her poor academic performance, as negative attitude often leads to lack of effort.
- **`N3` (conditional incentive)** `--CAUSES-->` **`N4` (incentive reception)**
  - *Underlying Rich Relations*: `['R2']`
  - *Justification*: The father's promise directly results in Karen receiving the incentive, as the promise is the mechanism of delivery.
- **`N4` (incentive reception)** `--MOTIVATES-->` **`N5` (task neglect)**
  - *Underlying Rich Relations*: `['R3']`
  - *Justification*: Receiving the incentive motivates Karen to dream about Hawaii and prepare for the trip, but she misdirects her effort away from studying.
- **`N5` (task neglect)** `--CAUSES-->` **`N6` (requirement failure)**
  - *Underlying Rich Relations*: `['R4']`
  - *Justification*: Neglecting studying directly leads to failing to graduate, as studying is necessary to meet graduation requirements.
- **`N6` (requirement failure)** `--CAUSES-->` **`N7` (reward withheld)**
  - *Underlying Rich Relations*: `['R5']`
  - *Justification*: Failing to graduate triggers the consequence of not going to Hawaii, as the trip was conditional on graduation.
- **`N1` (Karen dislikes school)** `--BEFORE-->` **`N5` (task neglect)**
  - *Underlying Rich Relations*: `['R6']`
  - *Justification*: Karen's dislike of school exists before she neglects studying, but it does not directly cause the neglect; the incentive is the immediate trigger.
- **`N2` (Karen is doing poorly in school)** `--BEFORE-->` **`N5` (task neglect)**
  - *Underlying Rich Relations*: `['R7']`
  - *Justification*: Karen's poor performance precedes her neglect of studying, but the neglect is a new behavior triggered by the incentive, not caused by prior poor performance.
- **`N3` (conditional incentive)** `--BEFORE-->` **`N5` (task neglect)**
  - *Underlying Rich Relations*: `['R8']`
  - *Justification*: The promise occurs before the neglect, but the neglect is a response to receiving the incentive, not directly to the promise itself.
- **`N4` (incentive reception)** `--BEFORE-->` **`N6` (requirement failure)**
  - *Underlying Rich Relations*: `['R9']`
  - *Justification*: Receiving the incentive occurs before failing to graduate, but the failure is caused by neglect, not directly by receiving the incentive.
- **`N5` (task neglect)** `--BEFORE-->` **`N7` (reward withheld)**
  - *Underlying Rich Relations*: `['R10']`
  - *Justification*: Neglect precedes the consequence of not going to Hawaii, but the direct cause is failing to graduate.