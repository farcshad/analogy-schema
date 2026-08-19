import pytest
from analogy_schema.models.story import Story
from analogy_schema.models.events import (
    AtomicEvent,
    NormalizedEvent,
    EventType,
    Polarity,
    Explicitness,
    InterventionPhase,
    TemporalExtent,
    TemporalGrounding,
    BackboneRole,
)
from analogy_schema.models.relations import EventRelation, RelationType
from analogy_schema.models.graph import RichEventGraph
from analogy_schema.models.backbone import (
    AbstractionLadder,
    MacroNode,
    BackboneNode,
    BackboneEdge,
    CausalBackbone,
    NarrativeAnchors,
    IncentiveContract,
)
from analogy_schema.utils.serialization import to_json


def test_story_creation_and_llm_input():
    text = "William was a patient. He hated inspections."
    story = Story.from_text(story_id="test_1", text=text, title="Test", metadata={"label": "ground_truth_label"})
    assert story.story_id == "test_1"
    assert len(story.sentences) == 2
    
    llm_input = story.to_llm_input()
    assert llm_input.story_id == "test_1"
    assert hasattr(llm_input, "text")
    assert not hasattr(llm_input, "metadata")


def test_atomic_and_normalized_events_with_temporal_grounding():
    atomic = AtomicEvent(
        event_id="E1",
        text_span="He spent time daydreaming",
        sentence_id=1,
        predicate="daydreams",
        event_type=EventType.ACTION,
        explicitness=Explicitness.EXPLICIT
    )
    assert atomic.event_id == "E1"
    
    tg = TemporalGrounding(
        mention_phase=InterventionPhase.PRE_INTERVENTION,
        onset_phase=InterventionPhase.PRE_INTERVENTION,
        holds_at_intervention=True,
        temporal_extent=TemporalExtent.INTERVAL
    )
    norm = NormalizedEvent(
        norm_id="NE1",
        predicate_name="NEGLECT_TASK",
        arguments={"actor": "William", "task": "cleaning"},
        atomic_event_ids=["E1"],
        summary_label="task neglect",
        temporal_grounding=tg
    )
    assert norm.norm_id == "NE1"
    assert norm.onset_phase == InterventionPhase.PRE_INTERVENTION
    assert norm.temporal_phase == InterventionPhase.PRE_INTERVENTION
    assert norm.holds_at_intervention is True
    assert "E1" in norm.atomic_event_ids


def test_relations_and_backbone_serialization():
    ladder = AbstractionLadder(
        level_0_raw="daydreams about food",
        level_1_domain="neglects cleaning",
        level_2_functional="task neglect",
        level_3_schema="inaction"
    )
    tg = TemporalGrounding(
        mention_phase=InterventionPhase.PRE_INTERVENTION,
        onset_phase=InterventionPhase.PRE_INTERVENTION,
        holds_at_intervention=True
    )
    macro = MacroNode(
        macro_id="M1",
        label="task neglect",
        source_normalized_ids=["NE1"],
        functional_role=BackboneRole.CAUSAL_ANTECEDENT,
        temporal_grounding=tg
    )
    node1 = BackboneNode(
        node_id="N1",
        macro_node=macro,
        abstraction=ladder,
        functional_role=BackboneRole.CAUSAL_ANTECEDENT,
        temporal_grounding=tg
    )
    node2 = node1.model_copy(update={
        "node_id": "N2",
        "abstraction": AbstractionLadder(
            level_0_raw="room is messy",
            level_1_domain="messy room",
            level_2_functional="accumulated deficit",
            level_3_schema="deficit"
        ),
        "functional_role": BackboneRole.PROBLEM_STATE
    })
    edge = BackboneEdge(
        edge_id="BE1",
        source_id="N1",
        target_id="N2",
        relation_type=RelationType.CAUSES,
        underlying_relation_ids=["R1"]
    )
    backbone = CausalBackbone(
        backbone_id="bb_1",
        story_id="test_1",
        nodes={"N1": node1, "N2": node2},
        explanatory_edges=[edge],
        anchors=NarrativeAnchors(
            central_problem="problem",
            contracts=[
                IncentiveContract(
                    intervention_event_id="NE3",
                    promised_reward="reward",
                    contingent_requirement="requirement"
                )
            ]
        )
    )
    
    json_str = to_json(backbone)
    assert "task neglect" in json_str
    assert "CAUSES" in json_str
    assert "PRE_INTERVENTION" in json_str
    assert "underlying_relation_ids" in json_str
    assert "explanatory_edges" in json_str
    
    warnings = backbone.validate_invariants()
    assert len(warnings) == 0
