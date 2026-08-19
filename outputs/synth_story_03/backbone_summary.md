# Causal Backbone: synth_story_03

## Narrative Anchors & Contracts
- **Central Problem**: Karen dislikes school and has barely passing grades
- **Central Goal**: Pass all classes
- **Intervention Events**: ['NE3']
- **Focal Outcomes**: ['NE6']
- **Contingent Outcomes**: ['NE7']
- **Downstream Reactions (Excluded from Anchoring)**: ['NE8']
- **Incentive Contracts**:
  - Reward: `trip to Hawaii` | Requirement: `pass all classes` (Polarity: positive)

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N3: conditional incentive `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Father promises Hawaii trip if Karen passes all classes
  - *Level 1 (Domain)*: parent promises conditional reward
  - *Level 2 (Functional)*: conditional incentive
  - *Level 3 (Schema)*: contingent reward offer
- **Underlying Macro-Node**: `M3` (promise Hawaii trip conditional on passing)
- **Source Normalized Events**: ['NE3']
- **Textual Provenance Spans**: ['if she passed all of her classes', 'her father promised to take her to Hawaii if she passed all of her classes']

### N4: receives conditional incentive
- **Role**: `ACTION_RESPONSE`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen hears the promise
  - *Level 1 (Domain)*: student receives communication
  - *Level 2 (Functional)*: receives conditional incentive
  - *Level 3 (Schema)*: information reception
- **Underlying Macro-Node**: `M4` (hears the promise)
- **Source Normalized Events**: ['NE4']
- **Textual Provenance Spans**: ['After hearing this promise']

### N5: task neglect
- **Role**: `ACTION_RESPONSE`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`INTERVAL`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen daydreams about Hawaii instead of studying
  - *Level 1 (Domain)*: student daydreams instead of studying
  - *Level 2 (Functional)*: task neglect
  - *Level 3 (Schema)*: counterproductive behavior
- **Underlying Macro-Node**: `M5` (daydreams about Hawaii instead of studying)
- **Source Normalized Events**: ['NE5']
- **Textual Provenance Spans**: ['Karen spent the rest of the year daydreaming about going to Hawaii instead of studying', 'instead of studying', 'daydreaming about going to Hawaii']

### N6: performance deficit `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Karen fails her classes
  - *Level 1 (Domain)*: student fails classes
  - *Level 2 (Functional)*: performance deficit
  - *Level 3 (Schema)*: failure to meet criteria
- **Underlying Macro-Node**: `M6` (fails classes)
- **Source Normalized Events**: ['NE6']
- **Textual Provenance Spans**: ['she failed her classes']

### N7: reward withheld `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Father does not take Karen to Hawaii
  - *Level 1 (Domain)*: parent withholds promised reward
  - *Level 2 (Functional)*: reward withheld
  - *Level 3 (Schema)*: consequence enactment
- **Underlying Macro-Node**: `M7` (father does not take Karen to Hawaii)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['her father did not take her to Hawaii', 'did not get to go to Hawaii']

## Explanatory Causal Edges (Mechanisms, Motivations, Consequences)
- **`N4` (receives conditional incentive)** `--MOTIVATES-->` **`N5` (task neglect)**
  - *Underlying Rich Relations*: `['R2']`
  - *Justification*: The promise of a Hawaii trip provides an incentive that leads Karen to daydream about Hawaii instead of studying, as stated: 'After hearing this promise, Karen spent the rest of the year daydreaming about going to Hawaii instead of studying.' The promise is the intentional reason for her daydreaming.
- **`N5` (task neglect)** `--CAUSES-->` **`N6` (performance deficit)**
  - *Underlying Rich Relations*: `['R3']`
  - *Justification*: The narrative explicitly states 'As a result, she failed her classes', indicating that daydreaming instead of studying directly caused her failure.
- **`N6` (performance deficit)** `--RESULTS_IN-->` **`N7` (reward withheld)**
  - *Underlying Rich Relations*: `['R4']`
  - *Justification*: The narrative states 'she failed her classes and did not get to go to Hawaii', showing that failing classes directly resulted in the father not taking her.

## Minimal Temporal Constraints (Non-Redundant BEFORE Constraints)
- **`N3` (conditional incentive)** `--BEFORE-->` **`N4` (receives conditional incentive)**
  - *Underlying Rich Relations*: `['R1']`
  - *Justification*: The narrative states 'After hearing this promise', indicating temporal sequence from the promise being made to Karen hearing it.

## Pruned Events (Audit Trail)
- **`NE8`**: Karen's disappointment and crying is a downstream emotional reaction to the focal outcome (NE6) and contingent outcome (NE7). Removing NE8 does not alter the causal explanation of why she failed or why the trip was withheld; it is a collateral effect, not a cause of the central problem, intervention, or outcomes.
- **`NE1`**: Pruned during final minimality pass: isolated BACKGROUND node 'dislike school' without explanatory connection to focal outcomes.
- **`NE2`**: Pruned during final minimality pass: isolated PROBLEM_STATE node 'barely passing grades' without explanatory connection to focal outcomes.