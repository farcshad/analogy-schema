# Causal Backbone: william_literally_similar

## Narrative Anchors & Contracts
- **Central Problem**: Arthur's bedroom is cluttered because he spent days daydreaming instead of tidying, and he regularly fails monthly bedroom checks.
- **Central Goal**: Arthur must tidy his bedroom thoroughly to pass the bedroom check.
- **Intervention Events**: ['NE8']
- **Focal Outcomes**: ['NE11']
- **Contingent Outcomes**: ['NE12', 'NE15']
- **Downstream Reactions (Excluded from Anchoring)**: ['NE13', 'NE14']
- **Incentive Contracts**:
  - Reward: `a slice of cake from the bakery` | Requirement: `tidying his bedroom thoroughly` (Polarity: positive)

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N1: task neglect
- **Role**: `CAUSAL_ANTECEDENT`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`False`, mention=`PRE_INTERVENTION`, extent=`INTERVAL`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur spent days daydreaming instead of tidying
  - *Level 1 (Domain)*: inmate neglects task due to daydreaming
  - *Level 2 (Functional)*: task neglect
  - *Level 3 (Schema)*: neglect antecedent
- **Underlying Macro-Node**: `M1` (task neglect)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['he had spent the days daydreaming']

### N2: deficit state
- **Role**: `PROBLEM_STATE`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`PRE_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur's bedroom is cluttered shortly before inspection
  - *Level 1 (Domain)*: bedroom cluttered before inspection
  - *Level 2 (Functional)*: deficit state
  - *Level 3 (Schema)*: resource deficit
- **Underlying Macro-Node**: `M2` (deficit state)
- **Source Normalized Events**: ['NE6']
- **Textual Provenance Spans**: ["Shortly before the scheduled inspection Arthur's bedroom was cluttered"]

### N3: conditional incentive `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Matron offers Arthur cake if he tidies bedroom thoroughly
  - *Level 1 (Domain)*: conditional reward offered for compliance
  - *Level 2 (Functional)*: conditional incentive
  - *Level 3 (Schema)*: contingent motivation
- **Underlying Macro-Node**: `M3` (conditional incentive)
- **Source Normalized Events**: ['NE8']
- **Textual Provenance Spans**: ['To motivate Arthur', 'To motivate Arthur, the matron offered him a slice of cake from the bakery if he tidied his bedroom thoroughly', 'if he tidied his bedroom thoroughly']

### N4: insufficient remaining resources
- **Role**: `CONSTRAINT`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Insufficient time remains for Arthur to finish cleaning
  - *Level 1 (Domain)*: time shortage prevents completion
  - *Level 2 (Functional)*: insufficient remaining resources
  - *Level 3 (Schema)*: resource constraint
- **Underlying Macro-Node**: `M4` (insufficient remaining resources)
- **Source Normalized Events**: ['NE10']
- **Textual Provenance Spans**: ['insufficient time remained for him to finish cleaning']

### N5: requirement failure `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur fails the bedroom check
  - *Level 1 (Domain)*: fails criteria of bedroom check
  - *Level 2 (Functional)*: requirement failure
  - *Level 3 (Schema)*: failure outcome
- **Underlying Macro-Node**: `M5` (requirement failure)
- **Source Normalized Events**: ['NE11']
- **Textual Provenance Spans**: ['he failed the bedroom check']

### N6: Arthur is denied the cake `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur is denied the cake
  - *Level 1 (Domain)*: Arthur is denied the cake
  - *Level 2 (Functional)*: Arthur is denied the cake
  - *Level 3 (Schema)*: consequence denial
- **Underlying Macro-Node**: `M6_split_1` (Arthur is denied the cake)
- **Source Normalized Events**: ['NE12']
- **Textual Provenance Spans**: ['was denied the cake']

### N7: Arthur receives no cake `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur receives no cake
  - *Level 1 (Domain)*: Arthur receives no cake
  - *Level 2 (Functional)*: Arthur receives no cake
  - *Level 3 (Schema)*: consequence denial
- **Underlying Macro-Node**: `M6_split_2` (Arthur receives no cake)
- **Source Normalized Events**: ['NE15']
- **Textual Provenance Spans**: ['he received no cake']

### N8: upset reaction
- **Role**: `DOWNSTREAM_REACTION`
- **Temporal Grounding**: onset=`UNANCHORED`, holds_at_intervention=`False`, mention=`UNANCHORED`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur became upset and kicked the wall
  - *Level 1 (Domain)*: patient reacts with anger and physical outburst
  - *Level 2 (Functional)*: upset reaction
  - *Level 3 (Schema)*: emotional response
- **Underlying Macro-Node**: `M7` (upset reaction)
- **Source Normalized Events**: []
- **Textual Provenance Spans**: []

## Backbone Edges (Typed Relational Backbone with Provenance)
- **`N1` (task neglect)** `--CAUSES-->` **`N2` (deficit state)**
  - *Underlying Rich Relations*: `['R1']`
  - *Justification*: Arthur spent days daydreaming instead of tidying, which directly caused his bedroom to be cluttered shortly before inspection.
- **`N3` (conditional incentive)** `--MOTIVATES-->` **`N2` (deficit state)**
  - *Underlying Rich Relations*: `['R3']`
  - *Justification*: The offer of cake was intended to motivate Arthur to tidy his bedroom, which would address the clutter.
- **`N4` (insufficient remaining resources)** `--CAUSES-->` **`N5` (requirement failure)**
  - *Underlying Rich Relations*: `['R4']`
  - *Justification*: Insufficient time remaining caused Arthur to fail the bedroom check.
- **`N5` (requirement failure)** `--CAUSES-->` **`N6` (Arthur is denied the cake)**
  - *Underlying Rich Relations*: `['R5']`
  - *Justification*: Failing the bedroom check directly resulted in Arthur being denied the cake.
- **`N6` (Arthur is denied the cake)** `--RESULTS_IN-->` **`N7` (Arthur receives no cake)**
  - *Underlying Rich Relations*: `['R8']`
  - *Justification*: Being denied the cake resulted in Arthur receiving no cake.
- **`N2` (deficit state)** `--MOTIVATES-->` **`N3` (conditional incentive)**
  - *Underlying Rich Relations*: `['R11']`
  - *Justification*: The cluttered bedroom motivated the matron to offer the incentive to Arthur.
- **`N3` (conditional incentive)** `--BEFORE-->` **`N4` (insufficient remaining resources)**
  - *Underlying Rich Relations*: `['R12']`
  - *Justification*: The offer occurred before the realization of insufficient time, but did not cause the time shortage.
- **`N4` (insufficient remaining resources)** `--BEFORE-->` **`N6` (Arthur is denied the cake)**
  - *Underlying Rich Relations*: `['R13']`
  - *Justification*: Insufficient time preceded the denial of cake, but the denial was directly caused by the failed check, not the time shortage itself.

## Pruned Events (Audit Trail)
- **`NE4`**: Secondary emotional reaction; removing it does not change the causal chain from clutter to intervention to failure.
- **`NE1`**: Chronic background state; removing it does not affect the explanation of why the bedroom was cluttered or why the intervention failed.
- **`NE14`**: Downstream collateral action; removing it does not alter the explanation of why Arthur failed and was denied cake.
- **`NE5`**: Background fantasy; not causally necessary for the clutter or the intervention's failure.
- **`NE2`**: Chronic background state; not causally necessary for the specific episode of failing the check due to insufficient time.
- **`NE13`**: Downstream emotional reaction; not causally necessary for the denial of cake or the final outcome.
- **`NE3`**: Habitual past record; the focal failure is explained by the immediate clutter and time shortage, not by prior failures.
- **`NE9`**: Secondary emotional reaction; Arthur's delight does not causally affect the time shortage or the outcome.