# Causal Backbone: synth_story_02

## Narrative Anchors & Contracts
- **Central Problem**: Karen was failing classes and would not graduate because she spent all her study time daydreaming.
- **Central Goal**: Karen must pass all her classes to graduate.
- **Intervention Events**: ['NE5']
- **Focal Outcomes**: ['NE8']
- **Contingent Outcomes**: ['NE9']
- **Downstream Reactions (Excluded from Anchoring)**: ['NE10', 'NE11']
- **Incentive Contracts**:
  - Reward: `trip to Hawaii` | Requirement: `pass all classes` (Polarity: positive)

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N2: task neglect
- **Role**: `CAUSAL_ANTECEDENT`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`PRE_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: She spent most of her time daydreaming about going to Hawaii.
  - *Level 1 (Domain)*: daydreaming instead of studying
  - *Level 2 (Functional)*: task neglect
  - *Level 3 (Schema)*: self-indulgent distraction
- **Underlying Macro-Node**: `M2` (task neglect)
- **Source Normalized Events**: ['NE3']
- **Textual Provenance Spans**: ['because she had spent all her study time daydreaming', 'She spent most of her time daydreaming about going to Hawaii']

### N3: performance deficit
- **Role**: `PROBLEM_STATE`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`PRE_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: A few weeks before the end of the year Karen was failing enough classes that she was not going to graduate, because she had spent all her study time daydreaming.
  - *Level 1 (Domain)*: failing classes and at risk of not graduating
  - *Level 2 (Functional)*: performance deficit
  - *Level 3 (Schema)*: critical failure risk
- **Underlying Macro-Node**: `M3` (performance deficit)
- **Source Normalized Events**: ['NE4']
- **Textual Provenance Spans**: ['A few weeks before the end of the year Karen was failing enough classes', 'she was not going to graduate']

### N4: conditional incentive `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: To encourage Karen, her father promised to take her to Hawaii if she passed all of her classes.
  - *Level 1 (Domain)*: father promises Hawaii trip conditional on passing all classes
  - *Level 2 (Functional)*: conditional incentive
  - *Level 3 (Schema)*: motivational intervention
- **Underlying Macro-Node**: `M4` (conditional incentive)
- **Source Normalized Events**: ['NE5']
- **Textual Provenance Spans**: ['To encourage Karen', 'To encourage Karen, her father promised to take her to Hawaii if she passed all of her classes', 'if she passed all of her classes']

### N5: insufficient remaining resources
- **Role**: `CONSTRAINT`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`PERSISTENT_STATE`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: However, there was no longer enough time for her to learn the material and pass.
  - *Level 1 (Domain)*: insufficient time to learn material and pass
  - *Level 2 (Functional)*: insufficient remaining resources
  - *Level 3 (Schema)*: resource shortage
- **Underlying Macro-Node**: `M5` (insufficient remaining resources)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['there was no longer enough time for her to learn the material and pass']

### N6: requirement failure `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Consequently, Karen failed her classes and did not get to go to Hawaii.
  - *Level 1 (Domain)*: failed classes
  - *Level 2 (Functional)*: requirement failure
  - *Level 3 (Schema)*: goal failure
- **Underlying Macro-Node**: `M6` (requirement failure)
- **Source Normalized Events**: ['NE8']
- **Textual Provenance Spans**: ['Consequently, Karen failed her classes']

### N7: reward withheld `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen was deeply disappointed and cried in her room, but she didn't get to go to Hawaii.
  - *Level 1 (Domain)*: did not go to Hawaii
  - *Level 2 (Functional)*: reward withheld
  - *Level 3 (Schema)*: contingent consequence
- **Underlying Macro-Node**: `M7` (reward withheld)
- **Source Normalized Events**: ['NE9']
- **Textual Provenance Spans**: ["she didn't get to go to Hawaii", 'did not get to go to Hawaii']

## Explanatory Causal Edges (Mechanisms, Motivations, Consequences)
- **`N2` (task neglect)** `--CAUSES-->` **`N3` (performance deficit)**
  - *Underlying Rich Relations*: `['R1']`
  - *Justification*: Narrative states: 'she had spent all her study time daydreaming' directly causing her to fail classes and not graduate.
- **`N5` (insufficient remaining resources)** `--CAUSES-->` **`N6` (requirement failure)**
  - *Underlying Rich Relations*: `['R3']`
  - *Justification*: Narrative states: 'there was no longer enough time for her to learn the material and pass. Consequently, Karen failed her classes'
- **`N6` (requirement failure)** `--RESULTS_IN-->` **`N7` (reward withheld)**
  - *Underlying Rich Relations*: `['R4']`
  - *Justification*: Narrative states: 'Karen failed her classes and did not get to go to Hawaii' as a direct consequence of failing.
- **`N2` (task neglect)** `--CAUSES-->` **`N5` (insufficient remaining resources)**
  - *Underlying Rich Relations*: `['R8']`
  - *Justification*: Daydreaming instead of studying led to insufficient time to learn material, as implied by the narrative sequence.
- **`N3` (performance deficit)** `--MOTIVATES-->` **`N4` (conditional incentive)**
  - *Underlying Rich Relations*: `['R10']`
  - *Justification*: Narrative states: 'To encourage Karen, her father promised to take her to Hawaii if she passed all of her classes.' The father's intentional motivation is explicitly stated.

## Minimal Temporal Constraints (Non-Redundant BEFORE Constraints)
- **`N4` (conditional incentive)** `--BEFORE-->` **`N5` (insufficient remaining resources)**
  - *Underlying Rich Relations*: `['R7']`
  - *Justification*: The promise occurs before the realization of insufficient time, but the promise does not cause the time shortage.

## Pruned Events (Audit Trail)
- **`NE10`**: Deep disappointment is a downstream emotional reaction to the failure and not getting to go to Hawaii. It does not explain the focal outcome or contingent consequence; removing it leaves the causal explanation intact.
- **`NE11`**: Crying in her room is a collateral behavioral expression of disappointment. It is not causally necessary to explain why she failed or did not go to Hawaii; removing it does not affect the explanatory backbone.
- **`NE2`**: Karen's hatred of school is a static emotional state that does not causally explain the specific deficit or the failure. Even if she did not hate school, she still daydreamed and failed; removing it does not break the causal chain from daydreaming to failing.
- **`NE6`**: Karen's thrill is a secondary emotional reaction to the intervention. It does not causally affect the outcome; even if she were not thrilled, the incentive was still introduced and the time shortage still prevented success.
- **`NE1`**: Pruned during final minimality pass: isolated BACKGROUND node 'poor academic performance' without explanatory connection to focal outcomes.