# Causal Backbone: william_base

## Narrative Anchors
- **Central Problem**: William never passes monthly room inspections and his room is a mess before the April inspection.
- **Central Goal**: To pass the April room inspection.
- **Intervention**: The nurse offers William gingerbread as an incentive to clean his room.
- **Terminal Outcomes**: William fails to pass the inspection, William does not get any gingerbread, William sulks all day, William slams door causing plaster to crack

## Backbone Nodes (Level 2 Functional Roles)
### N1: restrictive environment
- **Role**: background condition
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William is a patient in a psychiatric hospital who is confined indoors almost all the time
  - *Level 1 (Domain)*: psychiatric patient confined indoors
  - *Level 2 (Functional)*: restrictive environment
  - *Level 3 (Schema)*: setting constraints
- **Underlying Macro-Node**: `M1` (confinement and patient status)
- **Source Events**: ['E1', 'E2']
- **Textual Provenance Spans**: ['William was a patient in a psychiatric hospital', 'who was confined indoors almost all the time']

### N2: distraction causes inaction
- **Role**: causal antecedent
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William daydreams about food and neglects cleaning room due to daydreaming
  - *Level 1 (Domain)*: daydreaming leads to task neglect
  - *Level 2 (Functional)*: distraction causes inaction
  - *Level 3 (Schema)*: cognitive disengagement
- **Underlying Macro-Node**: `M2` (daydreaming and neglect)
- **Source Events**: ['E5', 'E7']
- **Textual Provenance Spans**: ['since he had done nothing but daydream', 'He spent most of his time daydreaming about food']

### N3: unmet condition
- **Role**: intermediate state
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William's room is a mess before April inspection
  - *Level 1 (Domain)*: room in disarray before inspection
  - *Level 2 (Functional)*: unmet condition
  - *Level 3 (Schema)*: state deficiency
- **Underlying Macro-Node**: `M3` (room is a mess)
- **Source Events**: ['E6']
- **Textual Provenance Spans**: ["A few days before the April inspection William's room was still a mess"]

### N4: external motivation `[INTERVENTION]`
- **Role**: intervention attempt
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Nurse offers William gingerbread as incentive for cleaning room
  - *Level 1 (Domain)*: nurse offers reward for cleaning
  - *Level 2 (Functional)*: external motivation
  - *Level 3 (Schema)*: incentive intervention
- **Underlying Macro-Node**: `M4` (offer of incentive)
- **Source Events**: ['E8', 'E9', 'E10']
- **Textual Provenance Spans**: ['the nurse promised him some gingerbread from the cookie shop', 'To provide William with an incentive', 'if he scrubbed his room and put it in order once and for all']

### N5: temporal constraint
- **Role**: blocking condition
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William has insufficient time to clean room before inspection
  - *Level 1 (Domain)*: time shortage prevents cleaning
  - *Level 2 (Functional)*: temporal constraint
  - *Level 3 (Schema)*: resource limitation
- **Underlying Macro-Node**: `M5` (insufficient time)
- **Source Events**: ['E12']
- **Textual Provenance Spans**: ['But there was no longer enough time for him to put it in order']

### N6: non-compliance consequence
- **Role**: negative outcome
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William never passes monthly room inspections and fails to pass the inspection
  - *Level 1 (Domain)*: fails room inspection
  - *Level 2 (Functional)*: non-compliance consequence
  - *Level 3 (Schema)*: failure event
- **Underlying Macro-Node**: `M6` (failure to pass inspection)
- **Source Events**: ['E3', 'E13']
- **Textual Provenance Spans**: ['he did not pass the inspection', 'He could never pass the monthly room inspections']

### N7: negative reinforcement `[OUTCOME]`
- **Role**: terminal outcome
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William does not get any gingerbread and sulks all day
  - *Level 1 (Domain)*: reward withheld, sulking
  - *Level 2 (Functional)*: negative reinforcement
  - *Level 3 (Schema)*: deprivation and emotional response
- **Underlying Macro-Node**: `M7` (withholding reward and sulking)
- **Source Events**: ['E14', 'E17', 'E15']
- **Textual Provenance Spans**: ['and did not get any gingerbread', 'William sulked all day', "but he still didn't get any gingerbread"]

### N8: aggressive venting
- **Role**: reactive behavior
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: William slams door causing plaster to crack
  - *Level 1 (Domain)*: slams door in frustration
  - *Level 2 (Functional)*: aggressive venting
  - *Level 3 (Schema)*: displaced aggression
- **Underlying Macro-Node**: `M8` (door slamming)
- **Source Events**: ['E16']
- **Textual Provenance Spans**: ['and slammed his door so hard the plaster cracked']

## Backbone Edges (Typed Relational Backbone)
- **`N1` (restrictive environment)** `--ENABLES-->` **`N2` (distraction causes inaction)**
  - *Justification*: Confinement and patient status provide the environment where daydreaming and neglect occur.
- **`N2` (distraction causes inaction)** `--CAUSES-->` **`N3` (unmet condition)**
  - *Justification*: Daydreaming and neglect directly cause the room to remain a mess.
- **`N3` (unmet condition)** `--MOTIVATES-->` **`N4` (external motivation)**
  - *Justification*: The messy room motivates the nurse to offer an incentive.
- **`N4` (external motivation)** `--BEFORE-->` **`N5` (temporal constraint)**
  - *Justification*: The offer occurs before the realization of insufficient time.
- **`N5` (temporal constraint)** `--CAUSES-->` **`N6` (non-compliance consequence)**
  - *Justification*: Insufficient time leads to failure to pass the inspection.
- **`N6` (non-compliance consequence)** `--RESULTS_IN-->` **`N7` (negative reinforcement)**
  - *Justification*: Failing the inspection results in withholding the reward and subsequent sulking.
- **`N7` (negative reinforcement)** `--CAUSES-->` **`N8` (aggressive venting)**
  - *Justification*: Sulking and frustration cause William to slam the door.

## Pruned Events (Audit Trail)
- **`NE4`**: Emotional reaction (hating inspections) is not causally necessary to explain the problem, intervention, or outcome.
- **`NE9`**: Emotional reaction (overjoyed) is a narrative decoration; it does not affect the causal chain of incentive, time, or failure.