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
    derive_atomic_functional_level_2,
    apply_backbone_minimality_pass,
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


def test_anti_merging_constraint_derives_functional_level_2_abstractions():
    """Validates Point 2: Split child nodes receive valid cross-domain Level-2 functional labels."""
    ne1 = NormalizedEvent(norm_id="NE1", predicate_name="NEGLECT_TASK", summary_label="Karen neglects homework")
    ne2 = NormalizedEvent(norm_id="NE2", predicate_name="DEFICIT_STATE", summary_label="Failing enough classes")
    
    # NE1 --CAUSES--> NE2
    rel = EventRelation(relation_id="R1", source_id="NE1", target_id="NE2", relation_type=RelationType.CAUSES)
    graph = RichEventGraph(
        graph_id="g1",
        story_id="s1",
        normalized_events={"NE1": ne1, "NE2": ne2},
        relations=[rel]
    )
    
    bad_merged_macro = GeneratedMacroNode(
        macro_id="M_merged",
        label="Neglecting classes causing deficit",
        source_normalized_ids=["NE1", "NE2"],
        functional_role=BackboneRole.PROBLEM_STATE,
        temporal_order=1,
        abstraction_level_0="raw",
        abstraction_level_1="domain",
        abstraction_level_2="Neglecting classes causing deficit",
        abstraction_level_3="schema"
    )
    
    sanitized = enforce_anti_merging_constraints([bad_merged_macro], graph)
    
    assert len(sanitized) == 2
    assert sanitized[0].abstraction_level_2 == "task neglect"
    assert sanitized[1].abstraction_level_2 in ("performance deficit", "prerequisite failure")


def test_backbone_minimality_pass_prunes_isolated_background_nodes():
    """Validates Point 3: Isolated background nodes without explanatory paths are removed."""
    from analogy_schema.models.backbone import BackboneNode, MacroNode, AbstractionLadder, BackboneEdge, NarrativeAnchors
    
    n_chronic = BackboneNode(
        node_id="N1",
        macro_node=MacroNode(macro_id="M1", label="habitual failure", source_normalized_ids=["NE_old"]),
        abstraction=AbstractionLadder(level_0_raw="old", level_1_domain="old", level_2_functional="habitual failure", level_3_schema="history"),
        functional_role=BackboneRole.BACKGROUND
    )
    n_cause = BackboneNode(
        node_id="N2",
        macro_node=MacroNode(macro_id="M2", label="task neglect", source_normalized_ids=["NE1"]),
        abstraction=AbstractionLadder(level_0_raw="daydream", level_1_domain="neglect", level_2_functional="task neglect", level_3_schema="inaction"),
        functional_role=BackboneRole.CAUSAL_ANTECEDENT
    )
    n_outcome = BackboneNode(
        node_id="N3",
        macro_node=MacroNode(macro_id="M3", label="requirement failure", source_normalized_ids=["NE5"]),
        abstraction=AbstractionLadder(level_0_raw="fails", level_1_domain="fails", level_2_functional="requirement failure", level_3_schema="failure"),
        functional_role=BackboneRole.FOCAL_OUTCOME,
        is_focal_outcome=True
    )
    
    edge = BackboneEdge(
        edge_id="BE1",
        source_id="N2",
        target_id="N3",
        relation_type=RelationType.CAUSES,
        underlying_relation_ids=["R1"]
    )
    
    nodes_dict = {"N1": n_chronic, "N2": n_cause, "N3": n_outcome}
    surviving_nodes, exp_edges, temp_edges, pruned_ids, pruned_reasons = apply_backbone_minimality_pass(
        nodes_dict=nodes_dict,
        explanatory_edges=[edge],
        temporal_constraints=[],
        anchors=NarrativeAnchors(focal_outcome_ids=["NE5"]),
        pruned_ids=[],
        pruned_reasons={}
    )
    
    # N1 (isolated background) should be pruned
    assert "N1" not in surviving_nodes
    assert "N2" in surviving_nodes
    assert "N3" in surviving_nodes
    assert "NE_old" in pruned_ids


def test_anchor_role_consistency_validator_catches_downstream_causal_conflict():
    """Validates Point 5 & 8: Downstream reaction on causal path raises validation warning."""
    from analogy_schema.models.backbone import BackboneNode, MacroNode, AbstractionLadder, BackboneEdge, NarrativeAnchors, CausalBackbone
    
    n_reaction = BackboneNode(
        node_id="N1",
        macro_node=MacroNode(macro_id="M1", label="task neglect", source_normalized_ids=["NE1"]),
        abstraction=AbstractionLadder(level_0_raw="daydream", level_1_domain="neglect", level_2_functional="task neglect", level_3_schema="inaction"),
        functional_role=BackboneRole.DOWNSTREAM_REACTION
    )
    n_outcome = BackboneNode(
        node_id="N2",
        macro_node=MacroNode(macro_id="M2", label="requirement failure", source_normalized_ids=["NE5"]),
        abstraction=AbstractionLadder(level_0_raw="fails", level_1_domain="fails", level_2_functional="requirement failure", level_3_schema="failure"),
        functional_role=BackboneRole.FOCAL_OUTCOME,
        is_focal_outcome=True
    )
    edge = BackboneEdge(
        edge_id="BE1",
        source_id="N1",
        target_id="N2",
        relation_type=RelationType.CAUSES,
        underlying_relation_ids=["R1"]
    )
    
    backbone = CausalBackbone(
        backbone_id="bb_test",
        story_id="test",
        nodes={"N1": n_reaction, "N2": n_outcome},
        explanatory_edges=[edge]
    )
    
    warnings = backbone.validate_invariants()
    assert any("Anchor Role Conflict" in w for w in warnings)


def test_all_anonymous_benchmark_fixtures_exist():
    """Validates Point 9: All 6 exact benchmark story fixtures and evaluation manifest exist."""
    fixtures_dir = Path(__file__).parent.parent / "analogy_schema" / "fixtures" / "stories"
    expected_files = [
        "story_base_01.json",
        "story_target_01.json",
        "story_target_02.json",
        "story_target_03.json",
        "story_target_04.json",
        "story_target_05.json",
        "synth_story_01.json",
        "synth_story_02.json",
        "synth_story_03.json",
    ]
    for fname in expected_files:
        fpath = fixtures_dir / fname
        assert fpath.exists(), f"Missing fixture: {fname}"
        with open(fpath, "r") as f:
            data = json.load(f)
        assert "text" in data and len(data["text"]) > 50
        assert "title" not in data or data.get("title") is None or "analogy" not in data.get("title", "").lower()
        
    manifest_path = Path(__file__).parent.parent / "analogy_schema" / "fixtures" / "benchmark_manifest.json"
    assert manifest_path.exists()
