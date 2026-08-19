from typing import Set, Dict, Any, List
from analogy_schema.models.graph import RichEventGraph
from analogy_schema.models.backbone import NarrativeAnchors
from analogy_schema.utils.graph_utils import rich_graph_to_nx, get_backward_causal_ancestors


def run_stage_e_backward_causal_tracing(
    graph: RichEventGraph,
    anchors: NarrativeAnchors
) -> Dict[str, Any]:
    """
    Stage E: Deterministic backward causal tracing from terminal outcomes.
    Finds all upstream events that causally explain the terminal outcomes and anchor events.
    """
    nx_graph = rich_graph_to_nx(graph)
    
    # Target anchor nodes in graph
    target_nodes = set()
    for anchor_id in anchors.anchor_event_ids:
        if anchor_id in nx_graph:
            target_nodes.add(anchor_id)
            
    # Also find nodes matching outcome keywords if anchor_event_ids was incomplete
    if not target_nodes:
        for nid, data in nx_graph.nodes(data=True):
            lbl = data.get("label", "").lower()
            pred = data.get("predicate", "").lower()
            if any(term in lbl or term in pred for term in ["fail", "withhold", "punish", "outcome", "loss"]):
                target_nodes.add(nid)
                
    # Backward reachability
    explanatory_ancestors = get_backward_causal_ancestors(nx_graph, list(target_nodes))
    
    return {
        "target_nodes": list(target_nodes),
        "explanatory_ancestors": list(explanatory_ancestors),
        "total_nodes": nx_graph.number_of_nodes(),
        "retained_candidate_count": len(explanatory_ancestors)
    }
