import json
import pytest
from pathlib import Path
from analogy_schema.models.story import Story
from analogy_schema.models.relations import RelationType
from analogy_schema.models.events import BackboneRole, InterventionPhase
from analogy_schema.llm.mock_provider import MockLLMProvider
from analogy_schema.pipeline.single_story_runner import SingleStoryPipeline
from analogy_schema.utils.serialization import export_backbone_markdown, to_json
from analogy_schema.fixtures.mock_responses import (
    get_william_mock_stage_a,
    get_william_mock_stage_b,
    get_william_mock_stage_c,
    get_william_mock_stage_d,
    get_william_mock_stage_f,
    get_william_mock_stage_gh,
)


def test_william_pipeline_vertical_slice():
    # 1. Load canonical story
    fixture_path = Path(__file__).parent.parent / "analogy_schema" / "fixtures" / "stories" / "william_base.json"
    with open(fixture_path, "r") as f:
        data = json.load(f)
    story = Story.from_text(
        story_id=data["story_id"],
        text=data["text"],
        title=data["title"],
        metadata=data["metadata"]
    )
    
    # 2. Setup MockLLMProvider with registered stage outputs
    mock_llm = MockLLMProvider()
    mock_llm.register_response("AtomicExtractionOutput", get_william_mock_stage_a())
    mock_llm.register_response("NormalizationOutput", get_william_mock_stage_b())
    mock_llm.register_response("RelationExtractionOutput", get_william_mock_stage_c())
    mock_llm.register_response("GoalOutcomeOutput", get_william_mock_stage_d())
    mock_llm.register_response("BackboneSelectionOutput", get_william_mock_stage_f())
    mock_llm.register_response("MacroGroupingOutput", get_william_mock_stage_gh())
    
    # 3. Execute full pipeline
    pipeline = SingleStoryPipeline(llm=mock_llm)
    result = pipeline.run(story)
    
    # 4. Verify Rich Graph
    assert len(result.rich_graph.atomic_events) >= 12
    assert len(result.rich_graph.normalized_events) == 7
    assert len(result.rich_graph.relations) == 7
    
    # Verify critical ontological fact: NE2 (backlog) is BEFORE NE3 (incentive), NOT caused by it
    temporal_edge = next((r for r in result.rich_graph.relations if r.source_id == "NE2" and r.target_id == "NE3"), None)
    assert temporal_edge is not None
    assert temporal_edge.relation_type == RelationType.BEFORE
    
    # 5. Verify Backward Causal Tracing
    assert "NE1" in result.backward_trace_info["causal_outcome_ancestors"] or "NE1" in result.backward_trace_info["candidate_ancestors"]
    assert "NE7" in result.anchors.downstream_reaction_ids
    
    # 6. Verify Causal Backbone
    backbone = result.backbone
    assert len(backbone.nodes) == 6
    assert "NE7" in backbone.pruned_node_ids
    
    # 7. Check Level 2 Functional Roles and Generic Roles
    level_2_labels = [node.abstraction.level_2_functional for node in backbone.nodes.values()]
    assert "task neglect / inaction" in level_2_labels
    assert "conditional reward offered as incentive" in level_2_labels
    assert "requirement failure" in level_2_labels
    assert "reward withheld" in level_2_labels
    
    roles = [node.functional_role for node in backbone.nodes.values()]
    assert BackboneRole.CAUSAL_ANTECEDENT in roles
    assert BackboneRole.INTERVENTION in roles
    assert BackboneRole.FOCAL_OUTCOME in roles
    assert BackboneRole.CONTINGENT_OUTCOME in roles
    
    # 8. Check Deterministic Edge Lifting and Provenance Invariant
    assert len(backbone.edges) > 0
    for edge in backbone.edges:
        assert len(edge.underlying_relation_ids) > 0, f"Edge {edge.edge_id} missing rich-edge provenance!"
    
    # 9. Verify DAG Property and Invariant validation
    assert result.dag_validation["is_dag"] is True
    assert result.dag_validation["cycle_count"] == 0
    assert len(result.validation_warnings) == 0
    
    # 10. Verify Markdown and JSON serialization
    md_output = export_backbone_markdown(backbone)
    assert "Causal Backbone: william_base" in md_output
    assert "Underlying Rich Relations" in md_output
    assert "task neglect / inaction" in md_output
    
    json_output = to_json(backbone)
    assert "PRE_INTERVENTION" in json_output
    assert "underlying_relation_ids" in json_output
