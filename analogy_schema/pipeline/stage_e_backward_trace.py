from typing import Set, Dict, Any, List
from analogy_schema.models.graph import RichEventGraph
from analogy_schema.models.backbone import NarrativeAnchors
from analogy_schema.models.relations import RelationType
from analogy_schema.utils.graph_utils import rich_graph_to_nx, get_backward_causal_ancestors


def run_stage_e_backward_causal_tracing(
    graph: RichEventGraph,
    anchors: NarrativeAnchors
) -> Dict[str, Any]:
    """
    Stage E: Multi-track backward causal and intervention tracing.
    1. Causal Outcome Path: Traces strictly backward from focal outcomes and contingent outcomes
       along causal mechanisms (CAUSES, RESULTS_IN, BLOCKS, PREVENTS, ENABLES).
    2. Intervention Context Path: Traces motivation and precursors to the intervention (MOTIVATES).
    Downstream reactions (emotional outbursts, incidental damage) are strictly excluded from anchoring.
    """
    nx_graph = rich_graph_to_nx(graph)
    
    # 1. Causal Outcome Tracing (Focal & Contingent outcomes only)
    focal_target_nodes = [nid for nid in (anchors.focal_outcome_ids + anchors.contingent_outcome_ids) if nid in nx_graph]
    
    # Strictly causal explanatory relations for failure/outcome path
    causal_relations = {
        RelationType.CAUSES.value,
        RelationType.RESULTS_IN.value,
        RelationType.BLOCKS.value,
        RelationType.PREVENTS.value,
        RelationType.ENABLES.value,
    }
    causal_outcome_ancestors = get_backward_causal_ancestors(nx_graph, focal_target_nodes, allowed_relations=causal_relations)
    
    # 2. Intervention Context Tracing
    intervention_target_nodes = [nid for nid in anchors.intervention_event_ids if nid in nx_graph]
    intervention_context_relations = {
        RelationType.MOTIVATES.value,
        RelationType.ENABLES.value,
        RelationType.CAUSES.value,
    }
    intervention_ancestors = get_backward_causal_ancestors(nx_graph, intervention_target_nodes, allowed_relations=intervention_context_relations)
    
    all_candidate_ancestors = causal_outcome_ancestors.union(intervention_ancestors).union(set(intervention_target_nodes)).union(set(focal_target_nodes))
    
    return {
        "focal_target_nodes": focal_target_nodes,
        "intervention_target_nodes": intervention_target_nodes,
        "causal_outcome_ancestors": list(causal_outcome_ancestors),
        "intervention_ancestors": list(intervention_ancestors),
        "candidate_ancestors": list(all_candidate_ancestors),
        "downstream_reactions_excluded": anchors.downstream_reaction_ids,
        "total_nodes": nx_graph.number_of_nodes(),
    }
