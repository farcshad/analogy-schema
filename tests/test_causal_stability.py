import json
import pytest
from pathlib import Path
from analogy_schema.models.story import Story
from analogy_schema.models.events import BackboneRole, InterventionPhase
from analogy_schema.models.relations import RelationType
from analogy_schema.pipeline.single_story_runner import SingleStoryPipeline
from analogy_schema.llm.mock_provider import MockLLMProvider
from analogy_schema.prompts.registry import PromptRegistry
from analogy_schema.fixtures.mock_responses import (
    get_william_mock_stage_a,
    get_william_mock_stage_b,
    get_william_mock_stage_c,
    get_william_mock_stage_d,
    get_william_mock_stage_f,
    get_william_mock_stage_gh,
)


def test_prompts_contain_no_benchmark_leakage():
    """Validates Point 1: No William/Karen domain terms exist in generic prompt templates."""
    forbidden_terms = [
        "daydream", "daydreaming", "clean", "cleaning", "gingerbread", "nurse",
        "psychiatric", "hospital", "cookie", "plaster", "sulk", "sulking",
        "slam", "slamming", "door", "hawaii", "karen", "william"
    ]
    for tname, template_text in PromptRegistry._TEMPLATES.items():
        text_lower = template_text.lower()
        for term in forbidden_terms:
            assert term not in text_lower, f"Forbidden benchmark term '{term}' leaked into prompt template '{tname}'!"


def test_william_backbone_pruning_and_provenance_invariants():
    """Validates Points 2, 3, 4, 7, 8 on William's canonical story."""
    fixture_path = Path(__file__).parent.parent / "analogy_schema" / "fixtures" / "stories" / "william_base.json"
    with open(fixture_path, "r") as f:
        data = json.load(f)
    story = Story.from_text(story_id=data["story_id"], text=data["text"])
    
    mock_llm = MockLLMProvider()
    mock_llm.register_response("AtomicExtractionOutput", get_william_mock_stage_a())
    mock_llm.register_response("NormalizationOutput", get_william_mock_stage_b())
    mock_llm.register_response("RelationExtractionOutput", get_william_mock_stage_c())
    mock_llm.register_response("GoalOutcomeOutput", get_william_mock_stage_d())
    mock_llm.register_response("BackboneSelectionOutput", get_william_mock_stage_f())
    mock_llm.register_response("MacroGroupingOutput", get_william_mock_stage_gh())
    
    pipeline = SingleStoryPipeline(llm=mock_llm)
    result = pipeline.run(story)
    backbone = result.backbone
    
    # 1. William's final backbone excludes emotional reaction / door slamming / plaster cracking
    all_node_text = " ".join(
        n.abstraction.level_0_raw + " " + n.abstraction.level_2_functional + " " + n.macro_node.label
        for n in backbone.nodes.values()
    ).lower()
    assert "sulk" not in all_node_text
    assert "slam" not in all_node_text
    assert "plaster" not in all_node_text
    assert "NE7" in backbone.pruned_node_ids
    
    # 2. William's requirement failure and reward withholding remain
    focal_nodes = [n for n in backbone.nodes.values() if n.functional_role == BackboneRole.FOCAL_OUTCOME]
    contingent_nodes = [n for n in backbone.nodes.values() if n.functional_role == BackboneRole.CONTINGENT_OUTCOME]
    assert len(focal_nodes) >= 1
    assert len(contingent_nodes) >= 1
    
    # 3. No final backbone edge exists without rich-edge provenance
    assert len(backbone.edges) > 0
    for edge in backbone.edges:
        assert len(edge.underlying_relation_ids) > 0, f"Edge {edge.edge_id} has no rich-edge provenance!"
        
    # 4. William's deficit state exists before/spans the intervention
    deficit_nodes = [n for n in backbone.nodes.values() if n.functional_role == BackboneRole.PROBLEM_STATE]
    assert len(deficit_nodes) >= 1
    assert deficit_nodes[0].temporal_phase in (InterventionPhase.PRE_INTERVENTION, InterventionPhase.SPANS_INTERVENTION)
    
    # 5. Invariant checks pass with 0 warnings
    warnings = backbone.validate_invariants()
    assert len(warnings) == 0
