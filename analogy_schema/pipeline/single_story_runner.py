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
from analogy_schema.utils.graph_utils import validate_dag_consistency


@dataclass
class SingleStoryPipelineResult:
    story: Story
    rich_graph: RichEventGraph
    anchors: NarrativeAnchors
    backward_trace_info: Dict[str, Any]
    backbone: CausalBackbone
    dag_validation: Dict[str, Any]


class SingleStoryPipeline:
    """
    End-to-end discrete pipeline for single story causal-event graph induction.
    Strictly independent processing with explicit provenance at every layer.
    """

    def __init__(self, llm: BaseLLMProvider):
        self.llm = llm

    def run(self, story: Story) -> SingleStoryPipelineResult:
        # Stage A: Atomic extraction
        atomic_events = run_stage_a_atomic_extraction(story, self.llm)

        # Stage B: Semantic normalization
        normalized_events = run_stage_b_semantic_normalization(story, atomic_events, self.llm)

        # Stage C: Typed relation extraction
        rich_graph = run_stage_c_relation_extraction(story, atomic_events, normalized_events, self.llm)

        # Stage D: Goal & outcome identification
        anchors = run_stage_d_goal_outcome_identification(story, normalized_events, self.llm)

        # Stage E: Backward causal tracing (deterministic graph traversal)
        backward_trace_info = run_stage_e_backward_causal_tracing(rich_graph, anchors)

        # Stage F: Backbone selection & counterfactual pruning
        backbone_selection_result = run_stage_f_backbone_selection(
            story=story,
            graph=rich_graph,
            anchors=anchors,
            llm=self.llm,
            backward_trace_candidates=backward_trace_info.get("explanatory_ancestors", [])
        )

        # Stages G & H: Macro-node formation and 4-Level Abstraction Ladder induction
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
        from analogy_schema.utils.graph_utils import backbone_to_nx
        nx_bb = backbone_to_nx(backbone)
        dag_validation = validate_dag_consistency(nx_bb)

        return SingleStoryPipelineResult(
            story=story,
            rich_graph=rich_graph,
            anchors=anchors,
            backward_trace_info=backward_trace_info,
            backbone=backbone,
            dag_validation=dag_validation
        )
