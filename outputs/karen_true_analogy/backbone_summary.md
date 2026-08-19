# Causal Backbone: karen_true_analogy

## Narrative Anchors & Contracts
- **Central Problem**: Karen is doing poorly in high school because she spends her time daydreaming about Hawaii.
- **Central Goal**: Karen must improve enough to graduate.
- **Intervention Events**: ['NE3']
- **Focal Outcomes**: ['NE7']
- **Contingent Outcomes**: ['NE8']
- **Downstream Reactions (Excluded from Anchoring)**: ['NE4']
- **Incentive Contracts**:
  - Reward: `Hawaii trip` | Requirement: `improve enough to graduate` (Polarity: positive)

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N1: task neglect
- **Role**: `CAUSAL_ANTECEDENT`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`PRE_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen spends time daydreaming about Hawaii
  - *Level 1 (Domain)*: student daydreams about reward
  - *Level 2 (Functional)*: task neglect
  - *Level 3 (Schema)*: causal distracter
- **Underlying Macro-Node**: `M1` (daydreaming neglect)
- **Source Normalized Events**: ['NE2']
- **Textual Provenance Spans**: ['she spends her time daydreaming about Hawaii']

### N2: performance deficit
- **Role**: `PROBLEM_STATE`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`PRE_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen is doing poorly in high school
  - *Level 1 (Domain)*: student underperforms academically
  - *Level 2 (Functional)*: performance deficit
  - *Level 3 (Schema)*: baseline failure state
- **Underlying Macro-Node**: `M2` (poor performance state)
- **Source Normalized Events**: ['NE1']
- **Textual Provenance Spans**: ['Karen is doing poorly in high school']

### N3: insufficient remaining resources
- **Role**: `CONSTRAINT`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`POST_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen is too far behind in her classes to recover
  - *Level 1 (Domain)*: student is beyond remediation threshold
  - *Level 2 (Functional)*: insufficient remaining resources
  - *Level 3 (Schema)*: unrecoverable gap
- **Underlying Macro-Node**: `M3` (irrecoverable deficit)
- **Source Normalized Events**: ['NE5']
- **Textual Provenance Spans**: ['She is already too far behind in her classes to recover']

### N4: conditional incentive `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Father promises to pay for Hawaii trip if Karen improves enough to graduate
  - *Level 1 (Domain)*: father offers conditional reward for graduation
  - *Level 2 (Functional)*: conditional incentive
  - *Level 3 (Schema)*: motivational intervention
- **Underlying Macro-Node**: `M4` (conditional incentive promise)
- **Source Normalized Events**: ['NE3']
- **Textual Provenance Spans**: ['Near graduation, her father promises to pay for a Hawaii trip if she improves enough to graduate', 'her father promises to pay for a Hawaii trip']

### N5: Karen fails enough classes `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`INTERVAL`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen fails enough classes
  - *Level 1 (Domain)*: Karen fails enough classes
  - *Level 2 (Functional)*: Karen fails enough classes
  - *Level 3 (Schema)*: goal failure
- **Underlying Macro-Node**: `M5_split_1` (Karen fails enough classes)
- **Source Normalized Events**: ['NE6']
- **Textual Provenance Spans**: ['She fails enough classes that she does not graduate']

### N6: Karen does not graduate `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen does not graduate
  - *Level 1 (Domain)*: Karen does not graduate
  - *Level 2 (Functional)*: Karen does not graduate
  - *Level 3 (Schema)*: goal failure
- **Underlying Macro-Node**: `M5_split_2` (Karen does not graduate)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['she does not graduate']

### N7: reward withheld `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen does not receive the Hawaii trip
  - *Level 1 (Domain)*: student does not receive promised trip
  - *Level 2 (Functional)*: reward withheld
  - *Level 3 (Schema)*: contingent forfeiture
- **Underlying Macro-Node**: `M6` (reward withheld)
- **Source Normalized Events**: ['NE8']
- **Textual Provenance Spans**: ['She therefore does not receive the Hawaii trip']

## Backbone Edges (Typed Relational Backbone with Provenance)
- **`N1` (task neglect)** `--CAUSES-->` **`N2` (performance deficit)**
  - *Underlying Rich Relations*: `['R1']`
  - *Justification*: The narrative states 'Karen is doing poorly in high school because she spends her time daydreaming about Hawaii', directly indicating that daydreaming causes poor performance.
- **`N3` (insufficient remaining resources)** `--CAUSES-->` **`N5` (Karen fails enough classes)**
  - *Underlying Rich Relations*: `['R3']`
  - *Justification*: Being too far behind to recover directly leads to failing enough classes, as the narrative implies that the deficit prevents improvement.
- **`N5` (Karen fails enough classes)** `--RESULTS_IN-->` **`N6` (Karen does not graduate)**
  - *Underlying Rich Relations*: `['R4']`
  - *Justification*: Failing enough classes results in not graduating, as stated: 'She fails enough classes that she does not graduate.'
- **`N6` (Karen does not graduate)** `--RESULTS_IN-->` **`N7` (reward withheld)**
  - *Underlying Rich Relations*: `['R5']`
  - *Justification*: Not graduating leads to not receiving the Hawaii trip, as stated: 'She therefore does not receive the Hawaii trip.'
- **`N4` (conditional incentive)** `--BEFORE-->` **`N5` (Karen fails enough classes)**
  - *Underlying Rich Relations*: `['R6']`
  - *Justification*: The father's promise occurs before the failing, but the promise does not cause the failing; the pre-existing deficit is the cause.
- **`N2` (performance deficit)** `--BEFORE-->` **`N3` (insufficient remaining resources)**
  - *Underlying Rich Relations*: `['R7']`
  - *Justification*: The poor performance state precedes and is consistent with being too far behind; they are co-temporal states but the narrative order implies the deficit state leads to the realization of being too far behind.

## Pruned Events (Audit Trail)
- **`NE4`**: Karen's happiness about the incentive is a downstream emotional reaction that does not causally affect her ability to catch up or the outcome. If she were unhappy but still too far behind, the same failure would occur.