import json
import pytest
from pathlib import Path
from analogy_schema.models.story import Story
from analogy_schema.models.events import (
    NormalizedEvent,
    BackboneRole,
    InterventionPhase,
    TemporalGrounding,
)
from analogy_schema.models.relations import EventRelation, RelationType
from analogy_schema.models.graph import RichEventGraph
from analogy_schema.pipeline.stage_g_macro import (
    GeneratedMacroNode,
    enforce_anti_merging_constraints,
    sanitize_level_2_label,
)
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
        "daydream", "daydreaming", "gingerbread", "nurse",
        "psychiatric", "hospital", "cookie", "plaster", "sulk", "sulking",
        "slam", "slamming", "hawaii", "karen", "william"
    ]
    for tname, template_text in PromptRegistry._TEMPLATES.items():
        text_lower = template_text.lower()
        for term in forbidden_terms:
            assert term not in text_lower, f"Forbidden benchmark term '{term}' leaked into prompt template '{tname}'!"


def test_anti_merging_constraint_preserves_structural_edges():
    """Validates Point 2: Events with rich relations (e.g. CAUSES) must never be merged into one node."""
    ne1 = NormalizedEvent(norm_id="NE1", predicate_name="NEGLECT_TASK", summary_label="task neglect")
    ne2 = NormalizedEvent(norm_id="NE2", predicate_name="DEFICIT_STATE", summary_label="performance deficit")
    
    # NE1 --CAUSES--> NE2
    rel = EventRelation(relation_id="R1", source_id="NE1", target_id="NE2", relation_type=RelationType.CAUSES)
    graph = RichEventGraph(
        graph_id="g1",
        story_id="s1",
        normalized_events={"NE1": ne1, "NE2": ne2},
        relations=[rel]
    )
    
    # Proposed bad merge combining NE1 and NE2 into one macro node
    bad_merged_macro = GeneratedMacroNode(
        macro_id="M_merged",
        label="Deficit state caused by neglect of duty",
        source_normalized_ids=["NE1", "NE2"],
        functional_role=BackboneRole.PROBLEM_STATE,
        temporal_order=1,
        abstraction_level_0="raw",
        abstraction_level_1="domain",
        abstraction_level_2="Deficit state caused by neglect of duty",
        abstraction_level_3="schema"
    )
    
    # Enforce programmatic constraint
    sanitized = enforce_anti_merging_constraints([bad_merged_macro], graph)
    
    # Must be split into 2 separate nodes!
    assert len(sanitized) == 2
    assert sanitized[0].source_normalized_ids == ["NE1"]
    assert sanitized[1].source_normalized_ids == ["NE2"]


def test_label_sanitizer_removes_relational_clauses():
    """Validates Point 3: Level-2 labels strip embedded relational connective phrases."""
    raw_label = "Deficit state caused by neglect of duty"
    cleaned = sanitize_level_2_label(raw_label)
    assert cleaned == "Deficit state"
    
    raw_label2 = "Failure to meet criteria due to resource shortage"
    cleaned2 = sanitize_level_2_label(raw_label2)
    assert cleaned2 == "Failure to meet criteria"


def test_william_backbone_pruning_and_provenance_invariants():
    """Validates Points 2, 3, 4, 5, 8 on William's canonical story."""
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
        
    # 4. William's deficit state exists before/spans the intervention with holds_at_intervention=True
    deficit_nodes = [n for n in backbone.nodes.values() if n.functional_role == BackboneRole.PROBLEM_STATE]
    assert len(deficit_nodes) >= 1
    assert deficit_nodes[0].onset_phase in (InterventionPhase.PRE_INTERVENTION, InterventionPhase.SPANS_INTERVENTION)
    assert deficit_nodes[0].holds_at_intervention is True
    
    # 5. Invariant checks pass with 0 warnings
    warnings = backbone.validate_invariants()
    assert len(warnings) == 0


def test_all_six_benchmark_fixtures_exist():
    """Validates Point 7: All 6 benchmark story fixtures are present and valid."""
    fixtures_dir = Path(__file__).parent.parent / "analogy_schema" / "fixtures" / "stories"
    expected_files = [
        "william_base.json",
        "karen_true_analogy.json",
        "karen_false_analogy.json",
        "william_literally_similar.json",
        "william_surface_similar.json",
        "william_mere_appearance.json",
    ]
    for fname in expected_files:
        fpath = fixtures_dir / fname
        assert fpath.exists(), f"Missing benchmark fixture: {fname}"
        with open(fpath, "r") as f:
            data = json.load(f)
        assert "text" in data and len(data["text"]) > 50
