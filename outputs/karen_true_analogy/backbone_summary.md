# Causal Backbone: karen_true_analogy

## Narrative Anchors
- **Central Problem**: Karen is doing poorly in high school because she daydreams about Hawaii
- **Central Goal**: Improve enough to graduate high school
- **Intervention Events**: ['NE3']
- **Focal Outcomes**: ['NE6']
- **Contingent Outcomes**: ['NE7']
- **Downstream Reactions (Excluded from Anchoring)**: ['NE4']

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N1: Deficit state caused by neglect of duty.
- **Role**: `CAUSAL_ANTECEDENT`
- **Intervention Phase**: `PRE_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen is doing poorly in high school because she spends her time daydreaming about Hawaii.
  - *Level 1 (Domain)*: Student neglects academic tasks due to distraction, leading to poor performance.
  - *Level 2 (Functional)*: Deficit state caused by neglect of duty.
  - *Level 3 (Schema)*: Neglect leads to deficit.
- **Underlying Macro-Node**: `M1` (poor academic performance due to daydreaming)
- **Source Normalized Events**: ['NE1', 'NE2']
- **Textual Provenance Spans**: ['she spends her time daydreaming about Hawaii', 'Karen is doing poorly in high school', 'because she spends her time daydreaming about Hawaii']

### N2: Introduction of external incentive to motivate behavior change. `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Intervention Phase**: `AT_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Father promises Hawaii trip if Karen improves enough to graduate.
  - *Level 1 (Domain)*: Authority figure offers conditional reward for performance improvement.
  - *Level 2 (Functional)*: Introduction of external incentive to motivate behavior change.
  - *Level 3 (Schema)*: Incentive intervention.
- **Underlying Macro-Node**: `M2` (father introduces incentive)
- **Source Normalized Events**: ['NE3']
- **Textual Provenance Spans**: ['if she improves enough to graduate', 'Near graduation', 'her father promises to pay for a Hawaii trip if she improves enough to graduate']

### N3: Pre-existing deficit prevents goal attainment despite intervention.
- **Role**: `CONSTRAINT`
- **Intervention Phase**: `POST_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen is already too far behind in her classes to recover.
  - *Level 1 (Domain)*: Student's academic deficit is insurmountable within remaining time.
  - *Level 2 (Functional)*: Pre-existing deficit prevents goal attainment despite intervention.
  - *Level 3 (Schema)*: Irreversible constraint.
- **Underlying Macro-Node**: `M3` (irrecoverable academic deficit)
- **Source Normalized Events**: ['NE5']
- **Textual Provenance Spans**: ['She is already too far behind in her classes to recover']

### N4: Failure to achieve the required outcome. `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Intervention Phase**: `POST_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen fails enough classes that she does not graduate.
  - *Level 1 (Domain)*: Student fails to meet graduation criteria.
  - *Level 2 (Functional)*: Failure to achieve the required outcome.
  - *Level 3 (Schema)*: Goal failure.
- **Underlying Macro-Node**: `M4` (failure to graduate)
- **Source Normalized Events**: ['NE6']
- **Textual Provenance Spans**: ['that she does not graduate', 'She fails enough classes']

### N5: Contingent reward is withheld after failure. `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Intervention Phase**: `POST_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen does not receive the Hawaii trip.
  - *Level 1 (Domain)*: Conditional reward is not delivered due to unmet condition.
  - *Level 2 (Functional)*: Contingent reward is withheld after failure.
  - *Level 3 (Schema)*: Withheld reward.
- **Underlying Macro-Node**: `M5` (forfeited reward)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['She therefore does not receive the Hawaii trip']

## Backbone Edges (Typed Relational Backbone with Provenance)
- **`N3` (Pre-existing deficit prevents goal attainment despite intervention.)** `--CAUSES-->` **`N4` (Failure to achieve the required outcome.)**
  - *Underlying Rich Relations*: `['R3']`
  - *Justification*: Being too far behind in classes to recover directly leads to failing enough classes to not graduate.
- **`N4` (Failure to achieve the required outcome.)** `--RESULTS_IN-->` **`N5` (Contingent reward is withheld after failure.)**
  - *Underlying Rich Relations*: `['R4']`
  - *Justification*: Failing to graduate results in not receiving the Hawaii trip, as the trip was conditional on graduation.
- **`N2` (Introduction of external incentive to motivate behavior change.)** `--CONDITIONAL_ON-->` **`N4` (Failure to achieve the required outcome.)**
  - *Underlying Rich Relations*: `['R5']`
  - *Justification*: The promise of the trip is conditional on Karen improving enough to graduate, which she fails to do.
- **`N3` (Pre-existing deficit prevents goal attainment despite intervention.)** `--BEFORE-->` **`N2` (Introduction of external incentive to motivate behavior change.)**
  - *Underlying Rich Relations*: `['R6']`
  - *Justification*: Karen's being too far behind is a pre-existing state before the father's promise, but the promise does not cause the deficit.
- **`N1` (Deficit state caused by neglect of duty.)** `--CAUSES-->` **`N3` (Pre-existing deficit prevents goal attainment despite intervention.)**
  - *Underlying Rich Relations*: `['R7']`
  - *Justification*: Daydreaming causing poor performance over time leads to being too far behind to recover.

## Pruned Events (Audit Trail)
- **`NE4`**: Karen's happiness about the incentive is a secondary emotional reaction that does not causally affect whether she improves, fails, or receives the trip. If she had been unhappy, the causal chain from the offer to her inability to recover and failure would remain unchanged.