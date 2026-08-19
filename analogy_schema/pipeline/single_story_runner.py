import asyncio
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from analogy_schema.models.story import Story
from analogy_schema.models.graph import RichEventGraph
from analogy_schema.models.backbone import CausalBackbone, NarrativeAnchors
from analogy_schema.llm.base import BaseLLMProvider
from analogy_schema.pipeline.stage_a_atomic import run_stage_a_atomic_extraction, run_stage_a_atomic_extraction_async
from analogy_schema.pipeline.stage_b_normalize import run_stage_b_semantic_normalization, run_stage_b_semantic_normalization_async
from analogy_schema.pipeline.stage_c_relations import run_stage_c_relation_extraction, run_stage_c_relation_extraction_async
from analogy_schema.pipeline.stage_d_goals import run_stage_d_goal_outcome_identification, run_stage_d_goal_outcome_identification_async
from analogy_schema.pipeline.stage_e_backward_trace import run_stage_e_backward_causal_tracing
from analogy_schema.pipeline.stage_f_backbone import run_stage_f_backbone_selection, run_stage_f_backbone_selection_async
from analogy_schema.pipeline.stage_g_macro import run_stage_g_and_h_macro_and_abstraction, run_stage_g_and_h_macro_and_abstraction_async
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
    Asynchronous and synchronous pipeline for single story causal-event graph induction.
    Executes independent stages (Stage C & Stage D) concurrently for high throughput.
    """

    def __init__(self, llm: BaseLLMProvider):
        self.llm = llm

    async def arun(self, story: Story) -> SingleStoryPipelineResult:
        """Asynchronous pipeline execution with internal Stage C and Stage D concurrency."""
        # Stage A: Atomic event extraction
        atomic_events = await run_stage_a_atomic_extraction_async(story, self.llm)

        # Stage B: Semantic normalization with temporal grounding
        normalized_events = await run_stage_b_semantic_normalization_async(story, atomic_events, self.llm)

        # INTRA-PIPELINE CONCURRENCY:
        # Stage C (Relation Extraction) and Stage D (Goal & Anchor Identification)
        # both depend strictly on normalized_events and run concurrently in parallel.
        rich_graph, anchors = await asyncio.gather(
            run_stage_c_relation_extraction_async(story, atomic_events, normalized_events, self.llm),
            run_stage_d_goal_outcome_identification_async(story, normalized_events, self.llm),
        )

        # Stage E: Multi-track backward causal tracing (deterministic graph traversal)
        backward_trace_info = run_stage_e_backward_causal_tracing(rich_graph, anchors)

        # Stage F: Counterfactual backbone selection & pruning
        backbone_selection_result = await run_stage_f_backbone_selection_async(
            story=story,
            graph=rich_graph,
            anchors=anchors,
            llm=self.llm,
            candidate_ancestors=backward_trace_info.get("candidate_ancestors", [])
        )

        # Stages G & H: Macro-node grouping and deterministic Rich-Relation edge lifting
        backbone = await run_stage_g_and_h_macro_and_abstraction_async(
            story=story,
            graph=rich_graph,
            retained_events=backbone_selection_result["retained_events"],
            anchors=anchors,
            pruned_ids=backbone_selection_result["pruned_ids"],
            pruned_reasons=backbone_selection_result["pruned_reasons"],
            llm=self.llm
        )

        # DAG Validation & Invariant verification
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

    def run(self, story: Story) -> SingleStoryPipelineResult:
        """Synchronous execution wrapper."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import nest_asyncio
                nest_asyncio.apply()
                return loop.run_until_complete(self.arun(story))
            else:
                return loop.run_until_complete(self.arun(story))
        except RuntimeError:
            return asyncio.run(self.arun(story))
