import pytest
from analogy_schema.models.events import NormalizedEvent
from analogy_schema.models.relations import EventRelation, RelationType
from analogy_schema.models.graph import RichEventGraph
from analogy_schema.utils.graph_utils import rich_graph_to_nx, get_backward_causal_ancestors, validate_dag_consistency


def test_rich_graph_backward_reachability():
    ne1 = NormalizedEvent(norm_id="NE1", predicate_name="NEGLECT_TASK", summary_label="neglect")
    ne2 = NormalizedEvent(norm_id="NE2", predicate_name="FALL_BEHIND", summary_label="behind")
    ne3 = NormalizedEvent(norm_id="NE3", predicate_name="FAIL_INSPECTION", summary_label="fail")
    ne4 = NormalizedEvent(norm_id="NE4", predicate_name="WITHHOLD_REWARD", summary_label="withhold")
    
    relations = [
        EventRelation(relation_id="R1", source_id="NE1", target_id="NE2", relation_type=RelationType.CAUSES),
        EventRelation(relation_id="R2", source_id="NE2", target_id="NE3", relation_type=RelationType.RESULTS_IN),
        EventRelation(relation_id="R3", source_id="NE3", target_id="NE4", relation_type=RelationType.RESULTS_IN),
    ]
    
    graph = RichEventGraph(
        graph_id="g1",
        story_id="s1",
        normalized_events={"NE1": ne1, "NE2": ne2, "NE3": ne3, "NE4": ne4},
        relations=relations
    )
    
    nx_g = rich_graph_to_nx(graph)
    validation = validate_dag_consistency(nx_g)
    assert validation["is_dag"] is True
    assert validation["cycle_count"] == 0
    
    ancestors = get_backward_causal_ancestors(nx_g, ["NE4"])
    assert "NE1" in ancestors
    assert "NE2" in ancestors
    assert "NE3" in ancestors
    assert "NE4" in ancestors
