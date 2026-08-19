# Causal Backbone: william_surface_similar

## Narrative Anchors & Contracts
- **Central Problem**: Arthur dislikes bedroom inspections
- **Central Goal**: Arthur cleans the dining tables before the cake is served
- **Intervention Events**: ['NE5']
- **Focal Outcomes**: ['NE6']
- **Contingent Outcomes**: ['NE7']
- **Downstream Reactions (Excluded from Anchoring)**: ['NE8', 'NE9', 'NE11', 'NE12', 'NE13', 'NE14', 'NE15']
- **Incentive Contracts**:
  - Reward: `cake served` | Requirement: `clean the dining tables before the cake is served` (Polarity: positive)

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N1: task assignment `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Matron asks Arthur to clean the dining tables
  - *Level 1 (Domain)*: authority assigns cleaning task
  - *Level 2 (Functional)*: task assignment
  - *Level 3 (Schema)*: directive intervention
- **Underlying Macro-Node**: `M1` (task assignment)
- **Source Normalized Events**: ['NE5']
- **Textual Provenance Spans**: ['The matron asked Arthur to clean the dining tables']

### N2: task execution `[FOCAL_OUTCOME]`
- **Role**: `ACTION_RESPONSE`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`INTERVAL`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur cleans the dining tables
  - *Level 1 (Domain)*: patient performs assigned cleaning
  - *Level 2 (Functional)*: task execution
  - *Level 3 (Schema)*: compliant action
- **Underlying Macro-Node**: `M2` (task execution)
- **Source Normalized Events**: ['NE6']
- **Textual Provenance Spans**: ['Arthur to clean the dining tables']

### N3: reward service `[CONTINGENT_OUTCOME]`
- **Role**: `CONTINGENT_OUTCOME`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Cake is served
  - *Level 1 (Domain)*: special cake served in recreation hall
  - *Level 2 (Functional)*: reward service
  - *Level 3 (Schema)*: contingent reward delivery
- **Underlying Macro-Node**: `M3` (reward service)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['before the cake was served']

## Backbone Edges (Typed Relational Backbone with Provenance)
- **`N1` (task assignment)** `--CAUSES-->` **`N2` (task execution)**
  - *Underlying Rich Relations*: `['R1']`
  - *Justification*: The matron asked Arthur to clean the dining tables, and Arthur performed the cleaning as a direct result of that request.
- **`N2` (task execution)** `--BEFORE-->` **`N3` (reward service)**
  - *Underlying Rich Relations*: `['R2']`
  - *Justification*: Arthur cleaned the tables before the cake was served, as stated in the narrative.

## Pruned Events (Audit Trail)
- **`NE4`**: The bakery delivering a cake is a background event that sets the context but is not causally necessary for the focal outcome; the cake being served (NE7) is retained as a contingent outcome.
- **`NE10`**: The matron conducting checks elsewhere is a background condition that allows the nap but is not part of the minimal causal chain; the nap is pruned.
- **`NE3`**: Arthur disliking inspections is a habitual state that does not causally drive the specific episode of missing the cake; the problem is resolved by the intervention and subsequent events.
- **`NE1`**: Arthur being a patient is a static background setting; removing it does not affect the causal explanation of why he missed the cake, as the focal mechanism involves his nap and the matron's task assignment.
- **`NE11`**: Taking a nap is a downstream reaction to fatigue; its removal does not damage the explanation because the focal outcome (cleaning tables) and contingent outcome (cake served) are already captured, and the nap is not causally required for the missed cake—the timing of the party conclusion suffices.
- **`NE14`**: Tables being cleared by staff is a collateral action after the cake is served; it does not explain why Arthur missed the cake.
- **`NE12`**: Waking up is a trivial consequence of the nap; removing it does not affect the causal explanation of the missed cake.
- **`NE8`**: Arthur eating a large meal is a secondary action that leads to fatigue but is not part of the minimal explanatory backbone; the nap (NE11) is pruned as a downstream reaction, and the fatigue state (NE9) is also pruned.
- **`NE2`**: The matron managing the ward is a chronic institutional role; its removal does not change the causal chain from the task assignment to the missed cake.
- **`NE13`**: The party concluding is a downstream event that is implied by the cake being eaten and tables cleared; it is not causally necessary for the focal outcome.
- **`NE15`**: The cake being eaten is a downstream consequence of the party; the contingent outcome (cake served) is retained, and the eating is not causally necessary for the focal outcome.
- **`NE9`**: Feeling tired is an internal state that mediates the nap but is not causally necessary; the nap itself is pruned as a downstream reaction.