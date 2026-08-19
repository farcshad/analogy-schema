# Causal Backbone: karen_false_analogy

## Narrative Anchors
- **Central Problem**: Karen dislikes school and is doing poorly.
- **Central Goal**: Graduate from school.
- **Intervention**: Father promises a Hawaii trip if Karen graduates.
- **Terminal Outcomes**: Karen fails to graduate, Karen does not go to Hawaii

## Backbone Nodes (Level 2 Functional Roles)
### N1: Initial negative academic state
- **Role**: initial_relevant_state
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen dislikes school and is doing poorly
  - *Level 1 (Domain)*: Dislike_school + perform_poorly
  - *Level 2 (Functional)*: Initial negative academic state
  - *Level 3 (Schema)*: Precondition_FAILURE
- **Underlying Macro-Node**: `M1` (Pre-existing negative academic state)
- **Source Events**: ['NE1', 'NE2']
- **Textual Provenance Spans**: ['Karen dislikes school', 'is doing poorly']

### N2: Motivating intervention accepted
- **Role**: motivating_intervention
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Father promises Hawaii trip if Karen graduates. Karen receives the incentive.
  - *Level 1 (Domain)*: Offer_incentive + receive_incentive
  - *Level 2 (Functional)*: Motivating intervention accepted
  - *Level 3 (Schema)*: INTERVENTION_OFFER_RECEIVE
- **Underlying Macro-Node**: `M2` (Incentive offer and acceptance)
- **Source Events**: ['NE3', 'NE4']
- **Textual Provenance Spans**: ['if she graduates', 'Her father promises a Hawaii trip if she graduates', 'After receiving the incentive']

### N3: Task neglect / inaction
- **Role**: counterproductive_response
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen neglects studying
  - *Level 1 (Domain)*: Neglect_task
  - *Level 2 (Functional)*: Task neglect / inaction
  - *Level 3 (Schema)*: FAILURE_BEHAVIOR
- **Underlying Macro-Node**: `M3` (Task neglect / inaction)
- **Source Events**: ['NE7']
- **Textual Provenance Spans**: ['instead of studying']

### N4: Failure to meet requirement
- **Role**: immediate_failure_result
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen fails to graduate
  - *Level 1 (Domain)*: Fail_requirement
  - *Level 2 (Functional)*: Failure to meet requirement
  - *Level 3 (Schema)*: FAILURE_OUTCOME
- **Underlying Macro-Node**: `M4` (Failure outcome)
- **Source Events**: ['NE8']
- **Textual Provenance Spans**: ['She then fails to graduate']

### N5: Loss of promised reward
- **Role**: terminal_negative_outcome
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen does not go to Hawaii
  - *Level 1 (Domain)*: Withhold_reward
  - *Level 2 (Functional)*: Loss of promised reward
  - *Level 3 (Schema)*: TERMINAL_LOSS
- **Underlying Macro-Node**: `M5` (Final negative consequence)
- **Source Events**: ['NE9']
- **Textual Provenance Spans**: ['does not go to Hawaii']

## Backbone Edges (Typed Relational Backbone)
- **`N1` (Initial negative academic state)** `--MOTIVATES-->` **`N2` (Motivating intervention accepted)**
  - *Justification*: The pre-existing negative academic state motivates the father to offer an incentive to change behavior.
- **`N2` (Motivating intervention accepted)** `--CAUSES-->` **`N3` (Task neglect / inaction)**
  - *Justification*: Receiving the incentive causes Karen to daydream about the trip instead of studying, leading to neglect.
- **`N3` (Task neglect / inaction)** `--CAUSES-->` **`N4` (Failure to meet requirement)**
  - *Justification*: Neglect of studying directly causes failure to graduate.
- **`N4` (Failure to meet requirement)** `--RESULTS_IN-->` **`N5` (Loss of promised reward)**
  - *Justification*: Failure to graduate results in not going to Hawaii (the promised reward is withheld).
- **`N1` (Initial negative academic state)** `--CONDITIONAL_ON-->` **`N5` (Loss of promised reward)**
  - *Justification*: The final loss is conditional on the initial negative state combined with the subsequent actions.

## Pruned Events (Audit Trail)
- **`NE6`**: Preparing for the trip is an incidental activity; the failure is directly caused by neglecting studying, not by preparing per se.
- **`NE5`**: Dreaming about Hawaii is a reaction to the incentive but does not causally explain the failure; the core mechanism is neglecting studying.