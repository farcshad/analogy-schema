# Causal Backbone: karen_true_analogy

## Narrative Anchors
- **Central Problem**: Karen is doing poorly in high school because she spends her time daydreaming about Hawaii
- **Central Goal**: Karen needs to improve enough to graduate
- **Intervention**: Father promises to pay for a Hawaii trip if Karen improves enough to graduate
- **Terminal Outcomes**: Karen fails enough classes that she does not graduate, Karen does not receive the Hawaii trip

## Backbone Nodes (Level 2 Functional Roles)
### N1: baseline deficiency / distraction
- **Role**: initial_state
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen is doing poorly in high school because she spends her time daydreaming about Hawaii
  - *Level 1 (Domain)*: student has poor grades due to distraction
  - *Level 2 (Functional)*: baseline deficiency / distraction
  - *Level 3 (Schema)*: pre-existing weakness
- **Underlying Macro-Node**: `M1` (poor academic performance / daydreaming)
- **Source Events**: ['NE1', 'NE2']
- **Textual Provenance Spans**: ['she spends her time daydreaming about Hawaii', 'Karen is doing poorly in high school', 'because she spends her time daydreaming about Hawaii']

### N2: conditional incentive offer `[INTERVENTION]`
- **Role**: intervention
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Father promises to pay for Hawaii trip if Karen improves enough to graduate
  - *Level 1 (Domain)*: parent offers conditional reward for academic improvement
  - *Level 2 (Functional)*: conditional incentive offer
  - *Level 3 (Schema)*: intervention
- **Underlying Macro-Node**: `M2` (offer incentive)
- **Source Events**: ['NE3']
- **Textual Provenance Spans**: ['Near graduation, her father promises to pay for a Hawaii trip if she improves enough to graduate', 'if she improves enough to graduate']

### N3: positive affective response
- **Role**: motivational_response
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen is happy about the incentive
  - *Level 1 (Domain)*: student feels positive about reward
  - *Level 2 (Functional)*: positive affective response
  - *Level 3 (Schema)*: motivation
- **Underlying Macro-Node**: `M3` (positive reaction to incentive)
- **Source Events**: ['NE4']
- **Textual Provenance Spans**: ['She is happy about the incentive']

### N4: irrecoverable deficit
- **Role**: blocking_condition
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen is already too far behind in her classes to recover
  - *Level 1 (Domain)*: student cannot catch up academically
  - *Level 2 (Functional)*: irrecoverable deficit
  - *Level 3 (Schema)*: constraint
- **Underlying Macro-Node**: `M4` (insufficient time to recover)
- **Source Events**: ['NE5']
- **Textual Provenance Spans**: ['She is already too far behind in her classes to recover']

### N5: condition not met
- **Role**: failure_to_meet_condition
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen fails enough classes that she does not graduate
  - *Level 1 (Domain)*: student fails to graduate
  - *Level 2 (Functional)*: condition not met
  - *Level 3 (Schema)*: failure
- **Underlying Macro-Node**: `M5` (fail requirement / not graduate)
- **Source Events**: ['NE6']
- **Textual Provenance Spans**: ['She fails enough classes that she does not graduate', 'she does not graduate']

### N6: incentive not delivered `[OUTCOME]`
- **Role**: terminal_outcome
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen does not receive the Hawaii trip
  - *Level 1 (Domain)*: reward is withheld
  - *Level 2 (Functional)*: incentive not delivered
  - *Level 3 (Schema)*: outcome
- **Underlying Macro-Node**: `M6` (withhold reward)
- **Source Events**: ['NE7']
- **Textual Provenance Spans**: ['She therefore does not receive the Hawaii trip']

## Backbone Edges (Typed Relational Backbone)
- **`N1` (baseline deficiency / distraction)** `--MOTIVATES-->` **`N2` (conditional incentive offer)**
  - *Justification*: The poor performance and distraction create the context that motivates the father to offer an incentive.
- **`N2` (conditional incentive offer)** `--CAUSES-->` **`N3` (positive affective response)**
  - *Justification*: The offer of the incentive directly causes Karen's positive emotional reaction.
- **`N1` (baseline deficiency / distraction)** `--CAUSES-->` **`N4` (irrecoverable deficit)**
  - *Justification*: The initial poor performance and daydreaming lead to being too far behind to recover.
- **`N4` (irrecoverable deficit)** `--CAUSES-->` **`N5` (condition not met)**
  - *Justification*: Being too far behind to recover causes Karen to fail enough classes and not graduate.
- **`N3` (positive affective response)** `--BLOCKS-->` **`N5` (condition not met)**
  - *Justification*: Despite positive motivation, the irrecoverable deficit blocks the possibility of meeting the graduation requirement.
- **`N5` (condition not met)** `--RESULTS_IN-->` **`N6` (incentive not delivered)**
  - *Justification*: Failing to graduate results in the withholding of the Hawaii trip.
- **`N2` (conditional incentive offer)** `--CONDITIONAL_ON-->` **`N6` (incentive not delivered)**
  - *Justification*: The reward is conditional on graduation; since the condition is not met, the reward is not given.