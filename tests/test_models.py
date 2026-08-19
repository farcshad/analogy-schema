import pytest
from analogy_schema.models.story import Story
from analogy_schema.models.events import AtomicEvent, NormalizedEvent, EventType, Polarity, Explicitness
from analogy_schema.models.relations import EventRelation, RelationType
from analogy_schema.models.graph import RichEventGraph
from analogy_schema.models.backbone import AbstractionLadder, MacroNode, BackboneNode, BackboneEdge, CausalBackbone, NarrativeAnchors
from analogy_schema.utils.serialization import to_json


def test_story_creation():
    text = "William was a patient. He hated inspections."
    story = Story.from_text(story_id="test_1", text=text, title="Test")
    assert story.story_id == "test_1"
    assert len(story.sentences) == 2
    assert story.sentences[0].text == "William was a patient."
    assert story.sentences[1].text == "He hated inspections."


def test_atomic_and_normalized_events():
    atomic = AtomicEvent(
        event_id="E1",
        text_span="He spent time daydreaming",
        sentence_id=1,
        predicate="daydreams",
        event_type=EventType.ACTION,
        explicitness=Explicitness.EXPLICIT
    )
    assert atomic.event_id == "E1"
    
    norm = NormalizedEvent(
        norm_id="NE1",
        predicate_name="NEGLECT_TASK",
        arguments={"actor": "William", "task": "cleaning"},
        atomic_event_ids=["E1"],
        summary_label="William neglects cleaning"
    )
    assert norm.norm_id == "NE1"
    assert "E1" in norm.atomic_event_ids


def test_relations_and_backbone_serialization():
    ladder = AbstractionLadder(
        level_0_raw="daydreams about food",
        level_1_domain="neglects cleaning",
        level_2_functional="task neglect / inaction",
        level_3_schema="failure to pursue goal"
    )
    macro = MacroNode(
        macro_id="M1",
        label="Daydreaming",
        source_normalized_ids=["NE1"],
        functional_role="cause"
    )
    node = BackboneNode(
        node_id="N1",
        macro_node=macro,
        abstraction=ladder,
        functional_role="cause"
    )
    edge = BackboneEdge(
        edge_id="BE1",
        source_id="N1",
        target_id="N2",
        relation_type=RelationType.CAUSES
    )
    backbone = CausalBackbone(
        backbone_id="bb_1",
        story_id="test_1",
        nodes={"N1": node},
        edges=[edge],
        anchors=NarrativeAnchors(central_problem="problem")
    )
    
    json_str = to_json(backbone)
    assert "task neglect / inaction" in json_str
    assert "CAUSES" in json_str
