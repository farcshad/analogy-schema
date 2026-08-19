import json
import pytest
from pathlib import Path
from analogy_schema.models.story import Story
from analogy_schema.models.relations import RelationType
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
    mock_llm.register_response("MacroAbstractionOutput", get_william_mock_stage_gh())
    
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
    assert result.backward_trace_info["retained_candidate_count"] >= 6
    assert "NE1" in result.backward_trace_info["explanatory_ancestors"]
    
    # 6. Verify Causal Backbone
    backbone = result.backbone
    assert len(backbone.nodes) == 6
    assert "NE7" in backbone.pruned_node_ids
    assert "door slamming" in backbone.pruned_reasons["NE7"] or "reaction" in backbone.pruned_reasons["NE7"]
    
    # 7. Check Level 2 Functional Roles
    level_2_labels = [node.abstraction.level_2_functional for node in backbone.nodes.values()]
    assert "task neglect / inaction" in level_2_labels
    assert "conditional reward offered as incentive" in level_2_labels
    assert "requirement failure" in level_2_labels
    assert "reward withheld" in level_2_labels
    
    # 8. Check Backbone Edges
    edge_types = [e.relation_type for e in backbone.edges]
    assert RelationType.CAUSES in edge_types
    assert RelationType.BEFORE in edge_types
    assert RelationType.RESULTS_IN in edge_types
    
    # 9. Verify DAG Property
    assert result.dag_validation["is_dag"] is True
    assert result.dag_validation["cycle_count"] == 0
    
    # 10. Verify Inspectable Markdown and JSON
    md_output = export_backbone_markdown(backbone)
    assert "Causal Backbone: william_base" in md_output
    assert "task neglect / inaction" in md_output
    assert "Pruned Events" in md_output
    
    json_output = to_json(backbone)
    assert "level_2_functional" in json_output
    assert "william_base" in json_output
