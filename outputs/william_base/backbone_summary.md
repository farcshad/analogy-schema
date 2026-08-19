# Causal Backbone: william_base

## Narrative Anchors
- **Central Problem**: William never passes monthly room inspections because he daydreams about food instead of cleaning.
- **Central Goal**: Pass the April room inspection.
- **Intervention Events**: ['NE6']
- **Focal Outcomes**: ['NE9']
- **Contingent Outcomes**: ['NE10']
- **Downstream Reactions (Excluded from Anchoring)**: ['NE11', 'NE12']

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N1: Chronic failure to meet institutional standards
- **Role**: `BACKGROUND`
- **Intervention Phase**: `PRE_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William never passes monthly room inspections
  - *Level 1 (Domain)*: Patient fails recurring cleanliness criteria
  - *Level 2 (Functional)*: Chronic failure to meet institutional standards
  - *Level 3 (Schema)*: Persistent non-compliance
- **Underlying Macro-Node**: `M1` (William confined and failing inspections)
- **Source Normalized Events**: ['NE2']
- **Textual Provenance Spans**: ['He could never pass the monthly room inspections']

### N2: Task neglect due to competing desire
- **Role**: `CAUSAL_ANTECEDENT`
- **Intervention Phase**: `PRE_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William daydreams about food instead of cleaning
  - *Level 1 (Domain)*: Patient engages in wishful thinking over task
  - *Level 2 (Functional)*: Task neglect due to competing desire
  - *Level 3 (Schema)*: Goal displacement
- **Underlying Macro-Node**: `M2` (William daydreams instead of cleaning)
- **Source Normalized Events**: ['NE4']
- **Textual Provenance Spans**: ['he had done nothing but daydream', 'He spent most of his time daydreaming about food']

### N3: Deficit state before deadline
- **Role**: `PROBLEM_STATE`
- **Intervention Phase**: `PRE_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William's room is a mess before April inspection
  - *Level 1 (Domain)*: Patient's room fails pre-inspection standard
  - *Level 2 (Functional)*: Deficit state before deadline
  - *Level 3 (Schema)*: Pre-deficit condition
- **Underlying Macro-Node**: `M3` (Room is messy before inspection)
- **Source Normalized Events**: ['NE5']
- **Textual Provenance Spans**: ["A few days before the April inspection William's room was still a mess"]

### N4: Incentive-based intervention `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Intervention Phase**: `AT_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Nurse promises gingerbread if William cleans room
  - *Level 1 (Domain)*: Caregiver introduces contingent reward for task completion
  - *Level 2 (Functional)*: Incentive-based intervention
  - *Level 3 (Schema)*: Contingent reward
- **Underlying Macro-Node**: `M4` (Nurse offers incentive for cleaning)
- **Source Normalized Events**: ['NE6']
- **Textual Provenance Spans**: ['if he scrubbed his room and put it in order once and for all', 'the nurse promised him some gingerbread from the cookie shop', 'To provide William with an incentive']

### N5: Resource shortage prevents action
- **Role**: `CONSTRAINT`
- **Intervention Phase**: `POST_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Not enough time for William to clean room
  - *Level 1 (Domain)*: Time resource insufficient for task completion
  - *Level 2 (Functional)*: Resource shortage prevents action
  - *Level 3 (Schema)*: Temporal constraint
- **Underlying Macro-Node**: `M5` (Insufficient time to clean)
- **Source Normalized Events**: ['NE8']
- **Textual Provenance Spans**: ['But there was no longer enough time for him to put it in order']

### N6: Failure to meet evaluation criteria `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Intervention Phase**: `POST_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William does not pass inspection
  - *Level 1 (Domain)*: Patient fails cleanliness assessment
  - *Level 2 (Functional)*: Failure to meet evaluation criteria
  - *Level 3 (Schema)*: Outcome failure
- **Underlying Macro-Node**: `M6` (William fails inspection)
- **Source Normalized Events**: ['NE9']
- **Textual Provenance Spans**: ['he did not pass the inspection']

### N7: Contingent reward withheld due to non-performance `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Intervention Phase**: `POST_INTERVENTION`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William does not get gingerbread
  - *Level 1 (Domain)*: Patient does not receive promised reward
  - *Level 2 (Functional)*: Contingent reward withheld due to non-performance
  - *Level 3 (Schema)*: Unfulfilled contingency
- **Underlying Macro-Node**: `M7` (William does not receive reward)
- **Source Normalized Events**: ['NE10']
- **Textual Provenance Spans**: ['did not get any gingerbread', "he still didn't get any gingerbread"]

## Backbone Edges (Typed Relational Backbone with Provenance)
- **`N2` (Task neglect due to competing desire)** `--CAUSES-->` **`N3` (Deficit state before deadline)**
  - *Underlying Rich Relations*: `['R1']`
  - *Justification*: William daydreams about food instead of cleaning, which directly results in his room being a mess before the April inspection.
- **`N4` (Incentive-based intervention)** `--BEFORE-->` **`N5` (Resource shortage prevents action)**
  - *Underlying Rich Relations*: `['R3']`
  - *Justification*: The nurse's promise occurs before the realization that there is not enough time to clean, but does not cause the time shortage.
- **`N5` (Resource shortage prevents action)** `--CAUSES-->` **`N6` (Failure to meet evaluation criteria)**
  - *Underlying Rich Relations*: `['R4']`
  - *Justification*: The lack of enough time to clean directly causes William to not pass the inspection.
- **`N6` (Failure to meet evaluation criteria)** `--CAUSES-->` **`N7` (Contingent reward withheld due to non-performance)**
  - *Underlying Rich Relations*: `['R5']`
  - *Justification*: Failing the inspection directly results in William not getting gingerbread, as the incentive was conditional on passing.
- **`N4` (Incentive-based intervention)** `--CONDITIONAL_ON-->` **`N6` (Failure to meet evaluation criteria)**
  - *Underlying Rich Relations*: `['R9']`
  - *Justification*: The nurse's promise of gingerbread is conditional on William passing the inspection, which he fails to do.
- **`N2` (Task neglect due to competing desire)** `--CAUSES-->` **`N1` (Chronic failure to meet institutional standards)**
  - *Underlying Rich Relations*: `['R10']`
  - *Justification*: William's consistent daydreaming instead of cleaning leads to his failure to pass monthly inspections, as implied by the narrative pattern.

## Pruned Events (Audit Trail)
- **`NE7`**: Incidental emotional response: William being overjoyed is a transient reaction to the incentive but does not causally affect the outcome (lack of time). Removing it does not break the causal explanation of failure.
- **`NE3`**: Secondary emotional reaction: William hating inspections is a subjective feeling that does not causally contribute to the failure or the intervention's effect. Its removal does not alter the explanation of why he failed.
- **`NE1`**: Background setting: William being a confined patient is a static description that does not causally explain the failure to pass inspections or the outcome. Removing it does not break the causal chain because the relevant deficit (messy room, daydreaming) is captured by NE4 and NE5.
- **`NE12`**: Incidental collateral action: Slamming the door and cracking plaster is an aggressive reaction that does not causally explain the failure or the lack of gingerbread. Removing it does not break the causal chain.
- **`NE11`**: Downstream reaction: Sulking is a consequence of failure, not a cause of the focal outcome or contingent outcome. Its removal does not affect the causal backbone explaining why he did not get gingerbread.