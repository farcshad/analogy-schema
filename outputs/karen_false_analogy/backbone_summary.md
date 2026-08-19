# Causal Backbone: karen_false_analogy

## Narrative Anchors
- **Central Problem**: Karen dislikes school and is doing poorly
- **Central Goal**: Graduate from school
- **Intervention Events**: ['NE3']
- **Focal Outcomes**: ['NE6']
- **Contingent Outcomes**: ['NE7']
- **Downstream Reactions (Excluded from Anchoring)**: []

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N1: pre-existing deficit state
- **Role**: `BACKGROUND`
- **Intervention Phase**: `PRE_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen dislikes school and is doing poorly
  - *Level 1 (Domain)*: Student has negative attitude and low performance
  - *Level 2 (Functional)*: pre-existing deficit state
  - *Level 3 (Schema)*: BACKGROUND_DEFICIT
- **Underlying Macro-Node**: `M1` (pre-existing academic disengagement)
- **Source Normalized Events**: ['NE1', 'NE2']
- **Textual Provenance Spans**: ['Karen dislikes school and is doing poorly', 'is doing poorly', 'Karen dislikes school']

### N2: conditional incentive introduced `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Intervention Phase**: `AT_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Father promises Hawaii trip if Karen graduates
  - *Level 1 (Domain)*: Parent offers conditional reward for academic success
  - *Level 2 (Functional)*: conditional incentive introduced
  - *Level 3 (Schema)*: INTERVENTION_INCENTIVE
- **Underlying Macro-Node**: `M2` (conditional incentive offered)
- **Source Normalized Events**: ['NE3']
- **Textual Provenance Spans**: ['if she graduates', 'Her father promises a Hawaii trip if she graduates']

### N3: incentive uptake
- **Role**: `ACTION_RESPONSE`
- **Intervention Phase**: `AT_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen receives the incentive
  - *Level 1 (Domain)*: Student accepts the conditional reward
  - *Level 2 (Functional)*: incentive uptake
  - *Level 3 (Schema)*: ACTION_RESPONSE_ACCEPTANCE
- **Underlying Macro-Node**: `M3` (incentive received)
- **Source Normalized Events**: ['NE4']
- **Textual Provenance Spans**: ['receiving the incentive']

### N4: goal displacement leading to task neglect
- **Role**: `CAUSAL_ANTECEDENT`
- **Intervention Phase**: `POST_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen neglects studying to dream about and prepare for Hawaii trip
  - *Level 1 (Domain)*: Student prioritizes trip preparation over studying
  - *Level 2 (Functional)*: goal displacement leading to task neglect
  - *Level 3 (Schema)*: CAUSAL_ANTECEDENT_DISTRACTION
- **Underlying Macro-Node**: `M4` (task neglect due to distraction)
- **Source Normalized Events**: ['NE5']
- **Textual Provenance Spans**: ['After receiving the incentive, she spends the remaining weeks dreaming about Hawaii and preparing for the trip instead of studying', 'she spends the remaining weeks dreaming about Hawaii', 'instead of studying', 'preparing for the trip']

### N5: failure to achieve target outcome `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Intervention Phase**: `POST_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen fails to graduate
  - *Level 1 (Domain)*: Student does not meet graduation requirements
  - *Level 2 (Functional)*: failure to achieve target outcome
  - *Level 3 (Schema)*: FOCAL_OUTCOME_FAILURE
- **Underlying Macro-Node**: `M5` (failure to meet graduation criteria)
- **Source Normalized Events**: ['NE6']
- **Textual Provenance Spans**: ['She then fails to graduate']

### N6: contingent reward not realized `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Intervention Phase**: `POST_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen does not go to Hawaii
  - *Level 1 (Domain)*: Student does not receive the promised trip
  - *Level 2 (Functional)*: contingent reward not realized
  - *Level 3 (Schema)*: CONTINGENT_OUTCOME_FORFEITURE
- **Underlying Macro-Node**: `M6` (forfeited reward)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['does not go to Hawaii']

## Backbone Edges (Typed Relational Backbone with Provenance)
- **`N2` (conditional incentive introduced)** `--CAUSES-->` **`N3` (incentive uptake)**
  - *Underlying Rich Relations*: `['R2']`
  - *Justification*: The father's promise of a Hawaii trip if Karen graduates directly leads to Karen receiving that incentive.
- **`N3` (incentive uptake)** `--MOTIVATES-->` **`N4` (goal displacement leading to task neglect)**
  - *Underlying Rich Relations*: `['R3']`
  - *Justification*: Receiving the incentive motivates Karen to focus on dreaming about and preparing for the trip instead of studying.
- **`N4` (goal displacement leading to task neglect)** `--CAUSES-->` **`N5` (failure to achieve target outcome)**
  - *Underlying Rich Relations*: `['R4']`
  - *Justification*: Neglecting studying directly causes Karen to fail to graduate, as studying is necessary for graduation.
- **`N5` (failure to achieve target outcome)** `--RESULTS_IN-->` **`N6` (contingent reward not realized)**
  - *Underlying Rich Relations*: `['R5']`
  - *Justification*: Failing to graduate results in the consequence that Karen does not go to Hawaii, as the trip was conditional on graduation.
- **`N2` (conditional incentive introduced)** `--CONDITIONAL_ON-->` **`N5` (failure to achieve target outcome)**
  - *Underlying Rich Relations*: `['R6']`
  - *Justification*: The promise of a Hawaii trip is conditional on Karen graduating; thus, graduation is a condition for the trip.