from dataclasses import dataclass
from typing import Dict, Any, Optional
from analogy_schema.models.story import Story
from analogy_schema.models.graph import RichEventGraph
from analogy_schema.models.backbone import CausalBackbone, NarrativeAnchors
from analogy_schema.llm.base import BaseLLMProvider
from analogy_schema.pipeline.stage_a_atomic import run_stage_a_atomic_extraction
from analogy_schema.pipeline.stage_b_normalize import run_stage_b_semantic_normalization
from analogy_schema.pipeline.stage_c_relations import run_stage_c_relation_extraction
from analogy_schema.pipeline.stage_d_goals import run_stage_d_goal_outcome_identification
from analogy_schema.pipeline.stage_e_backward_trace import run_stage_e_backward_causal_tracing
from analogy_schema.pipeline.stage_f_backbone import run_stage_f_backbone_selection
from analogy_schema.pipeline.stage_g_macro import run_stage_g_and_h_macro_and_abstraction
from analogy_schema.utils.graph_utils import validate_dag_consistency, backbone_to_nx


@dataclass
class SingleStoryPipelineResult:
    story: Story
    rich_graph: RichEventGraph
    anchors: NarrativeAnchors
    backward_trace_info: Dict[str, Any]
    backbone: CausalBackbone
    dag_validation: Dict[str, Any]
    validation_warnings: list


class SingleStoryPipeline:
    """
    Scientifically stabilized discrete pipeline for single story causal-event graph induction.
    Strictly independent processing with explicit provenance and deterministic edge lifting.
    """

    def __init__(self, llm: BaseLLMProvider):
        self.llm = llm

    def run(self, story: Story) -> SingleStoryPipelineResult:
        # Stage A: Atomic event extraction
        atomic_events = run_stage_a_atomic_extraction(story, self.llm)

        # Stage B: Semantic predicate normalization with temporal phase tagging
        normalized_events = run_stage_b_semantic_normalization(story, atomic_events, self.llm)

        # Stage C: Typed evidence-grounded relation extraction
        rich_graph = run_stage_c_relation_extraction(story, atomic_events, normalized_events, self.llm)

        # Stage D: Structured narrative anchor identification (focal vs contingent vs downstream reactions)
        anchors = run_stage_d_goal_outcome_identification(story, normalized_events, self.llm)

        # Stage E: Multi-track backward causal and intervention tracing
        backward_trace_info = run_stage_e_backward_causal_tracing(rich_graph, anchors)

        # Stage F: Counterfactual backbone selection & pruning (ancestors are candidates; focal anchors protected)
        backbone_selection_result = run_stage_f_backbone_selection(
            story=story,
            graph=rich_graph,
            anchors=anchors,
            llm=self.llm,
            candidate_ancestors=backward_trace_info.get("candidate_ancestors", [])
        )

        # Stages G & H: Functional Macro-node grouping and deterministic Rich-Relation edge lifting
        backbone = run_stage_g_and_h_macro_and_abstraction(
            story=story,
            graph=rich_graph,
            retained_events=backbone_selection_result["retained_events"],
            anchors=anchors,
            pruned_ids=backbone_selection_result["pruned_ids"],
            pruned_reasons=backbone_selection_result["pruned_reasons"],
            llm=self.llm
        )

        # DAG Validation
        nx_bb = backbone_to_nx(backbone)
        dag_validation = validate_dag_consistency(nx_bb)
        warnings = backbone.validate_invariants()

        return SingleStoryPipelineResult(
            story=story,
            rich_graph=rich_graph,
            anchors=anchors,
            backward_trace_info=backward_trace_info,
            backbone=backbone,
            dag_validation=dag_validation,
            validation_warnings=warnings
        )
