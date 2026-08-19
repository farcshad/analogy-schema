# Causal Backbone: story_target_03

## Narrative Anchors & Contracts
- **Central Problem**: Arthur frequently fails monthly living-quarters evaluations and his quarters are disorganized due to neglect.
- **Central Goal**: Arthur must sanitize and organize his quarters completely to pass the upcoming inspection.
- **Intervention Events**: ['NE7']
- **Focal Outcomes**: ['NE10']
- **Contingent Outcomes**: ['NE11']
- **Downstream Reactions (Excluded from Anchoring)**: ['NE12']
- **Incentive Contracts**:
  - Reward: `a box of pastries from the local bakery` | Requirement: `sanitize and organize his quarters completely` (Polarity: positive)

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N2: task neglect
- **Role**: `CAUSAL_ANTECEDENT`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`PRE_INTERVENTION`, extent=`INTERVAL`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur's quarters were completely disorganized because he had spent the preceding days daydreaming instead of tidying up.
  - *Level 1 (Domain)*: neglects cleaning due to daydreaming
  - *Level 2 (Functional)*: task neglect
  - *Level 3 (Schema)*: antecedent neglect
- **Underlying Macro-Node**: `M2` (task neglect)
- **Source Normalized Events**: ['NE5']
- **Textual Provenance Spans**: ["Arthur's quarters were completely disorganized", 'Several days before the upcoming inspection', 'he had spent the preceding days daydreaming instead of tidying up']

### N3: conditional incentive `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Seeking to motivate him, the supervising nurse offered him a box of pastries from the local bakery if he sanitized and organized his quarters completely.
  - *Level 1 (Domain)*: nurse offers pastries conditional on cleaning
  - *Level 2 (Functional)*: conditional incentive
  - *Level 3 (Schema)*: incentive intervention
- **Underlying Macro-Node**: `M3` (conditional incentive)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['if he sanitized and organized his quarters completely', 'the supervising nurse offered him a box of pastries from the local bakery if he sanitized and organized his quarters completely']

### N4: insufficient remaining resources
- **Role**: `CONSTRAINT`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: there was insufficient time remaining before the inspection for him to complete the cleaning.
  - *Level 1 (Domain)*: insufficient time to complete cleaning
  - *Level 2 (Functional)*: insufficient remaining resources
  - *Level 3 (Schema)*: resource constraint
- **Underlying Macro-Node**: `M4` (insufficient remaining resources)
- **Source Normalized Events**: ['NE9']
- **Textual Provenance Spans**: ['there was insufficient time remaining before the inspection for him to complete the cleaning']

### N5: performance deficit `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`PRE_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur frequently failed the monthly living-quarters evaluations; he failed the evaluation.
  - *Level 1 (Domain)*: fails living-quarters evaluation
  - *Level 2 (Functional)*: performance deficit
  - *Level 3 (Schema)*: outcome failure
- **Underlying Macro-Node**: `M5` (performance deficit)
- **Source Normalized Events**: ['NE2', 'NE10']
- **Textual Provenance Spans**: ['He frequently failed the monthly living-quarters evaluations', 'he failed the evaluation']

### N6: reward withheld `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur did not receive the pastries; the pastries were withheld.
  - *Level 1 (Domain)*: pastries withheld
  - *Level 2 (Functional)*: reward withheld
  - *Level 3 (Schema)*: contingent consequence
- **Underlying Macro-Node**: `M6` (reward withheld)
- **Source Normalized Events**: ['NE11']
- **Textual Provenance Spans**: ['the pastries were withheld', 'did not receive the pastries']

## Explanatory Causal Edges (Mechanisms, Motivations, Consequences)
- **`N2` (task neglect)** `--CAUSES-->` **`N5` (performance deficit)**
  - *Underlying Rich Relations*: `['R1']`
  - *Justification*: Arthur's quarters were disorganized because he daydreamed instead of tidying up; the narrative states 'Consequently, he failed the evaluation' linking the disorganization directly to the failure.
- **`N4` (insufficient remaining resources)** `--CAUSES-->` **`N5` (performance deficit)**
  - *Underlying Rich Relations*: `['R2']`
  - *Justification*: The narrative states 'there was insufficient time remaining before the inspection for him to complete the cleaning. Consequently, he failed the evaluation' showing insufficient time directly caused the failure.
- **`N5` (performance deficit)** `--RESULTS_IN-->` **`N6` (reward withheld)**
  - *Underlying Rich Relations*: `['R3']`
  - *Justification*: The narrative states 'he failed the evaluation and did not receive the pastries' showing failure directly resulted in the pastries being withheld.

## Minimal Temporal Constraints (Non-Redundant BEFORE Constraints)
- **`N3` (conditional incentive)** `--BEFORE-->` **`N2` (task neglect)**
  - *Underlying Rich Relations*: `['R7']`
  - *Justification*: The offer occurs after Arthur's quarters are already disorganized; the narrative describes the disorganization before the offer.
- **`N2` (task neglect)** `--BEFORE-->` **`N4` (insufficient remaining resources)**
  - *Underlying Rich Relations*: `['R8']`
  - *Justification*: The disorganization existed before the insufficient time is noted; the narrative implies the disorganization contributed to the time shortage but does not state direct causation.

## Pruned Events (Audit Trail)
- **`NE3`**: Arthur's frustration with staff is a secondary emotional reaction to chronic failure and does not causally explain the focal episode. Even if he were not frustrated, the sequence of neglect, incentive, time shortage, and failure would still occur unchanged.
- **`NE12`**: Shouting and kicking the door is a downstream emotional outburst after the outcome. It does not causally explain the failure (NE10) or the withholding of pastries (NE11). Removing it does not affect the explanatory backbone of how the problem, intervention, and outcome unfolded.
- **`NE4`**: Fantasizing about sweets is a background preference that explains motivation for the incentive but is not causally essential. If Arthur did not fantasize, the nurse's offer of pastries (NE7) could still motivate him via general desire for a treat; the outcome does not depend on his specific fantasies.
- **`NE8`**: Arthur being ecstatic is an emotional reaction to the offer, not a necessary cause of subsequent events. Even if he were only moderately pleased, he would still attempt to clean; the insufficient time (NE9) and failure (NE10) are independent of his emotional intensity.
- **`NE6`**: The nurse seeking to motivate is an internal mental state that is redundant with the actual offer (NE7). The offer itself is the intervention; removing NE6 does not break the causal chain because NE7 implies the intention.
- **`NE1`**: Pruned during final minimality pass: isolated BACKGROUND node 'restricted inpatient' without explanatory connection to focal outcomes.

## Validation Warnings
- ⚠️ Temporal-Causal Inversion: Node N4 (onset=POST_INTERVENTION) is asserted to CAUSES N5 (onset=PRE_INTERVENTION).