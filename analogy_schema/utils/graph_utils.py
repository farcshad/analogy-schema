from typing import List, Set, Dict, Any, Optional
import networkx as nx
from analogy_schema.models.graph import RichEventGraph
from analogy_schema.models.backbone import CausalBackbone, BackboneNode, BackboneEdge
from analogy_schema.models.relations import RelationType


def rich_graph_to_nx(graph: RichEventGraph) -> nx.DiGraph:
    """Converts a RichEventGraph into a NetworkX DiGraph for graph-theoretic algorithms."""
    G = nx.DiGraph()
    
    # Add nodes (prefer normalized events, fall back to atomic)
    if graph.normalized_events:
        for nid, ne in graph.normalized_events.items():
            G.add_node(
                nid,
                label=ne.summary_label,
                predicate=ne.predicate_name,
                arguments=ne.arguments,
                atomic_ids=ne.atomic_event_ids,
                confidence=ne.confidence
            )
    else:
        for eid, ae in graph.atomic_events.items():
            G.add_node(
                eid,
                label=ae.predicate,
                text_span=ae.text_span,
                participants=ae.participants,
                confidence=ae.confidence
            )
            
    for rel in graph.relations:
        G.add_edge(
            rel.source_id,
            rel.target_id,
            relation_type=rel.relation_type.value if hasattr(rel.relation_type, "value") else str(rel.relation_type),
            confidence=rel.confidence,
            explicitness=rel.explicitness.value if hasattr(rel.explicitness, "value") else str(rel.explicitness),
            evidence=rel.evidence
        )
        
    return G


def backbone_to_nx(backbone: CausalBackbone) -> nx.DiGraph:
    """Converts a CausalBackbone to a NetworkX DiGraph."""
    G = nx.DiGraph()
    for nid, node in backbone.nodes.items():
        G.add_node(
            nid,
            label=node.abstraction.level_2_functional,
            level_0=node.abstraction.level_0_raw,
            level_1=node.abstraction.level_1_domain,
            level_2=node.abstraction.level_2_functional,
            level_3=node.abstraction.level_3_schema,
            role=node.functional_role,
            is_intervention=node.is_intervention,
            is_terminal_outcome=node.is_terminal_outcome,
            provenance_spans=node.provenance_text_spans
        )
        
    for edge in backbone.edges:
        G.add_edge(
            edge.source_id,
            edge.target_id,
            relation_type=edge.relation_type.value if hasattr(edge.relation_type, "value") else str(edge.relation_type),
            confidence=edge.confidence,
            justification=edge.justification
        )
    return G


def get_backward_causal_ancestors(
    G: nx.DiGraph,
    target_nodes: List[str],
    allowed_relations: Optional[Set[str]] = None
) -> Set[str]:
    """
    Traces backward along explanatory edges from target outcome nodes.
    By default, considers CAUSES, RESULTS_IN, ENABLES, BLOCKS, MOTIVATES, CONDITIONAL_ON.
    """
    if allowed_relations is None:
        allowed_relations = {
            RelationType.CAUSES.value,
            RelationType.RESULTS_IN.value,
            RelationType.ENABLES.value,
            RelationType.BLOCKS.value,
            RelationType.MOTIVATES.value,
            RelationType.CONDITIONAL_ON.value,
        }
        
    # Subgraph with only explanatory relations
    explanatory_edges = [
        (u, v) for u, v, d in G.edges(data=True)
        if d.get("relation_type") in allowed_relations
    ]
    subG = nx.DiGraph()
    subG.add_nodes_from(G.nodes(data=True))
    subG.add_edges_from(explanatory_edges)
    
    ancestors = set()
    for t in target_nodes:
        if t in subG:
            ancestors.add(t)
            ancestors.update(nx.ancestors(subG, t))
            
    return ancestors


def validate_dag_consistency(G: nx.DiGraph) -> Dict[str, Any]:
    """Checks DAG properties, cycle presence, and connected components."""
    is_dag = nx.is_directed_acyclic_graph(G)
    cycles = list(nx.simple_cycles(G)) if not is_dag else []
    return {
        "is_dag": is_dag,
        "cycle_count": len(cycles),
        "cycles": cycles,
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
    }
