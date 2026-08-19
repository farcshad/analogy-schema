# Causal Backbone: william_mere_appearance

## Narrative Anchors & Contracts
- **Central Problem**: Cake crumbs contaminate the white paint
- **Central Goal**: Remove Arthur from the recreation room to prevent further contamination
- **Intervention Events**: ['NE9']
- **Focal Outcomes**: ['NE10']
- **Contingent Outcomes**: []
- **Downstream Reactions (Excluded from Anchoring)**: ['NE11']

## Backbone Nodes (Level 2 Functional Roles & Temporal Phases)
### N1: food consumption
- **Role**: `BACKGROUND`
- **Temporal Grounding**: onset=`PRE_INTERVENTION`, holds_at_intervention=`True`, mention=`PRE_INTERVENTION`, extent=`INTERVAL`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur was eating a piece of cake from the bakery while watching the painters.
  - *Level 1 (Domain)*: Arthur eats cake
  - *Level 2 (Functional)*: food consumption
  - *Level 3 (Schema)*: preparatory action
- **Underlying Macro-Node**: `M1` (eating cake)
- **Source Normalized Events**: ['NE3']
- **Textual Provenance Spans**: ['Arthur was eating a piece of cake from the bakery']

### N2: proximity to hazard
- **Role**: `CAUSAL_ANTECEDENT`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`PRE_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: As he leaned over the open paint bucket to inspect the color, cake crumbs fell into the white paint.
  - *Level 1 (Domain)*: Arthur leans over open paint bucket
  - *Level 2 (Functional)*: proximity to hazard
  - *Level 3 (Schema)*: risk-taking behavior
- **Underlying Macro-Node**: `M2` (leaning over paint bucket)
- **Source Normalized Events**: ['NE5']
- **Textual Provenance Spans**: ['he leaned over the open paint bucket to inspect the color']

### N3: contamination event
- **Role**: `PROBLEM_STATE`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`PRE_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Cake crumbs fall into and contaminate the white paint
  - *Level 1 (Domain)*: Cake crumbs contaminate paint
  - *Level 2 (Functional)*: contamination event
  - *Level 3 (Schema)*: unintended consequence
- **Underlying Macro-Node**: `M3` (cake crumbs contaminate paint)
- **Source Normalized Events**: ['NE7']
- **Textual Provenance Spans**: ['cake crumbs fell into the white paint']

### N4: detection of problem `[FOCAL_OUTCOME]`
- **Role**: `FOCAL_OUTCOME`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Matron notices the crumbs in the paint
  - *Level 1 (Domain)*: Matron notices contamination
  - *Level 2 (Functional)*: detection of problem
  - *Level 3 (Schema)*: awareness
- **Underlying Macro-Node**: `M4` (matron notices contamination)
- **Source Normalized Events**: ['NE8']
- **Textual Provenance Spans**: ['The matron noticed the crumbs']

### N5: removal request `[INTERVENTION]`
- **Role**: `INTERVENTION`
- **Temporal Grounding**: onset=`AT_INTERVENTION`, holds_at_intervention=`False`, mention=`AT_INTERVENTION`, extent=`POINT`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Matron asks Arthur to step outside into the courtyard
  - *Level 1 (Domain)*: Matron requests Arthur's removal
  - *Level 2 (Functional)*: removal request
  - *Level 3 (Schema)*: corrective intervention
- **Underlying Macro-Node**: `M5` (matron requests removal)
- **Source Normalized Events**: ['NE9']
- **Textual Provenance Spans**: ['asked Arthur to step outside into the courtyard']

### N6: compliance with removal request `[FOCAL_OUTCOME]`
- **Role**: `ACTION_RESPONSE`
- **Temporal Grounding**: onset=`POST_INTERVENTION`, holds_at_intervention=`False`, mention=`POST_INTERVENTION`, extent=`INTERVAL`
- **Abstraction Ladder**:
  - *Level 0 (Raw)*: Arthur walks to his bedroom (compliance with request to step outside)
  - *Level 1 (Domain)*: Arthur walks to bedroom
  - *Level 2 (Functional)*: compliance with removal request
  - *Level 3 (Schema)*: compliant action
- **Underlying Macro-Node**: `M6` (Arthur complies with request)
- **Source Normalized Events**: ['NE10']
- **Textual Provenance Spans**: ['Arthur walked to his bedroom', 'to step outside into the courtyard']

## Backbone Edges (Typed Relational Backbone with Provenance)
- **`N1` (food consumption)** `--ENABLES-->` **`N2` (proximity to hazard)**
  - *Underlying Rich Relations*: `['R1']`
  - *Justification*: Arthur was eating cake (NE3) while watching painters, which provides the cake crumbs that later fall when he leans over.
- **`N2` (proximity to hazard)** `--CAUSES-->` **`N3` (contamination event)**
  - *Underlying Rich Relations*: `['R3', 'R8']`
  - *Justification*: Leaning over the open paint bucket (NE5) causes cake crumbs to fall into the paint (NE7).; Leaning over (NE5) occurs before the crumbs fall (NE7) in narrative time. [Adjudicated between BEFORE, CAUSES: prioritized CAUSES.]
- **`N3` (contamination event)** `--CAUSES-->` **`N4` (detection of problem)**
  - *Underlying Rich Relations*: `['R4']`
  - *Justification*: The contamination of the paint (NE7) causes the matron to notice the crumbs (NE8).
- **`N4` (detection of problem)** `--MOTIVATES-->` **`N5` (removal request)**
  - *Underlying Rich Relations*: `['R5', 'R10']`
  - *Justification*: Noticing the crumbs (NE8) motivates the matron to ask Arthur to step outside (NE9).; Noticing (NE8) occurs before the request (NE9) in narrative time. [Adjudicated between BEFORE, MOTIVATES: prioritized MOTIVATES.]
- **`N5` (removal request)** `--CAUSES-->` **`N6` (compliance with removal request)**
  - *Underlying Rich Relations*: `['R6', 'R11']`
  - *Justification*: The matron's request (NE9) causes Arthur to comply by walking to his bedroom (NE10).; The request (NE9) occurs before Arthur walks to his bedroom (NE10). [Adjudicated between BEFORE, CAUSES: prioritized CAUSES.]

## Pruned Events (Audit Trail)
- **`NE4`**: Arthur watching painters is a secondary activity; the contamination is caused by leaning over the bucket, not by watching.
- **`NE1`**: Matron's location in the institution is a static background setting; removing it does not affect the causal explanation of the contamination or removal.
- **`NE11`**: Workers stirring paint is a downstream collateral action after the focal outcome (Arthur's removal); it does not explain the central problem or goal fulfillment.
- **`NE6`**: Inspecting the color is a detail of the leaning action; the contamination occurs from leaning regardless of inspection.
- **`NE2`**: Supervising painting is a chronic task context; the contamination and removal are explained without it.