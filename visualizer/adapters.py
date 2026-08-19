import json
from pathlib import Path
from typing import Dict, Any, List, Optional


def load_story_text(output_id: str, outputs_dir: Path) -> Optional[str]:
    """Attempts to find the narrative text for this output from fixtures or rich graph."""
    # 1. Check fixtures
    fixtures_dir = Path("analogy_schema/fixtures/stories")
    for ext in [".json", ".txt"]:
        candidate = fixtures_dir / f"{output_id}{ext}"
        if candidate.exists():
            try:
                if ext == ".json":
                    with open(candidate, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        return data.get("text", "")
                else:
                    return candidate.read_text(encoding="utf-8")
            except Exception:
                pass
                
    # 2. Reconstruct from atomic events in rich_event_graph.json if available
    rich_path = outputs_dir / output_id / "rich_event_graph.json"
    if rich_path.exists():
        try:
            with open(rich_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            atomic = data.get("atomic_events", {})
            if atomic:
                sorted_events = sorted(atomic.values(), key=lambda e: (e.get("sentence_id", 0), e.get("temporal_rank", 0)))
                # Combine unique sentences or spans
                spans = [e.get("text_span", "") for e in sorted_events if e.get("text_span")]
                return " ".join(spans)
        except Exception:
            pass
            
    return None


def adapt_causal_backbone_to_vis(backbone_data: Dict[str, Any], output_id: str, outputs_dir: Path) -> Dict[str, Any]:
    """
    Transforms raw causal_backbone.json into normalized visualization model.
    Handles schema evolutions gracefully (both legacy 'edges' and new 'explanatory_edges' / 'temporal_constraints').
    """
    nodes_raw = backbone_data.get("nodes", {})
    vis_nodes = []
    
    for nid, n in nodes_raw.items():
        macro = n.get("macro_node", {})
        abstr = n.get("abstraction", {})
        tg = n.get("temporal_grounding", {}) or macro.get("temporal_grounding", {})
        
        vis_nodes.append({
            "id": nid,
            "label": abstr.get("level_2_functional") or macro.get("label") or nid,
            "role": n.get("functional_role") or macro.get("functional_role") or "PROBLEM_STATE",
            "is_intervention": bool(n.get("is_intervention")),
            "is_focal_outcome": bool(n.get("is_focal_outcome")),
            "is_contingent_outcome": bool(n.get("is_contingent_outcome")),
            "temporal_grounding": {
                "mention_phase": tg.get("mention_phase", "UNANCHORED"),
                "onset_phase": tg.get("onset_phase", "UNANCHORED"),
                "holds_at_intervention": tg.get("holds_at_intervention", False),
                "temporal_extent": tg.get("temporal_extent", "POINT")
            },
            "abstraction": {
                "level_0_raw": abstr.get("level_0_raw", ""),
                "level_1_domain": abstr.get("level_1_domain", ""),
                "level_2_functional": abstr.get("level_2_functional", ""),
                "level_3_schema": abstr.get("level_3_schema", "")
            },
            "macro_id": macro.get("macro_id", ""),
            "macro_label": macro.get("label", ""),
            "source_normalized_ids": macro.get("source_normalized_ids", []),
            "source_atomic_ids": macro.get("source_atomic_ids", []),
            "provenance_text_spans": n.get("provenance_text_spans", []),
            "confidence": n.get("confidence", 1.0),
            "explicitness": n.get("explicitness", "explicit")
        })
        
    vis_edges = []
    
    # 1. Explanatory edges
    raw_explanatory = backbone_data.get("explanatory_edges", [])
    for e in raw_explanatory:
        vis_edges.append({
            "id": e.get("edge_id", f"{e.get('source_id')}_{e.get('target_id')}"),
            "source": e.get("source_id"),
            "target": e.get("target_id"),
            "label": e.get("relation_type", "CAUSES"),
            "category": "explanatory",
            "is_temporal": False,
            "justification": e.get("justification", ""),
            "confidence": e.get("confidence", 1.0),
            "explicitness": e.get("explicitness", "explicit"),
            "underlying_relation_ids": e.get("underlying_relation_ids", [])
        })
        
    # 2. Temporal constraints
    raw_temporal = backbone_data.get("temporal_constraints", [])
    for e in raw_temporal:
        vis_edges.append({
            "id": e.get("edge_id", f"{e.get('source_id')}_{e.get('target_id')}"),
            "source": e.get("source_id"),
            "target": e.get("target_id"),
            "label": e.get("relation_type", "BEFORE"),
            "category": "temporal",
            "is_temporal": True,
            "justification": e.get("justification", ""),
            "confidence": e.get("confidence", 1.0),
            "explicitness": e.get("explicitness", "explicit"),
            "underlying_relation_ids": e.get("underlying_relation_ids", [])
        })
        
    # 3. Fallback for legacy single-array 'edges'
    if not vis_edges and "edges" in backbone_data:
        for e in backbone_data["edges"]:
            rel = e.get("relation_type", "CAUSES")
            is_temp = rel == "BEFORE"
            vis_edges.append({
                "id": e.get("edge_id", f"{e.get('source_id')}_{e.get('target_id')}"),
                "source": e.get("source_id"),
                "target": e.get("target_id"),
                "label": rel,
                "category": "temporal" if is_temp else "explanatory",
                "is_temporal": is_temp,
                "justification": e.get("justification", ""),
                "confidence": e.get("confidence", 1.0),
                "explicitness": e.get("explicitness", "explicit"),
                "underlying_relation_ids": e.get("underlying_relation_ids", [])
            })

    anchors_raw = backbone_data.get("anchors", {})
    contracts_raw = anchors_raw.get("contracts", [])
    
    pruned_ids = backbone_data.get("pruned_node_ids", [])
    pruned_reasons = backbone_data.get("pruned_reasons", {})
    pruned_events = [
        {"id": pid, "reason": pruned_reasons.get(pid, "Pruned during counterfactual necessity selection")}
        for pid in pruned_ids
    ]
    
    metadata = backbone_data.get("metadata", {})
    validation_warnings = metadata.get("validation_warnings", [])
    story_text = load_story_text(output_id, outputs_dir)
    
    return {
        "story_id": backbone_data.get("story_id", output_id),
        "view_type": "backbone",
        "nodes": vis_nodes,
        "edges": vis_edges,
        "anchors": {
            "central_problem": anchors_raw.get("central_problem", ""),
            "central_goal": anchors_raw.get("central_goal", ""),
            "intervention_event_ids": anchors_raw.get("intervention_event_ids", []),
            "focal_outcome_ids": anchors_raw.get("focal_outcome_ids", []),
            "contingent_outcome_ids": anchors_raw.get("contingent_outcome_ids", []),
            "downstream_reaction_ids": anchors_raw.get("downstream_reaction_ids", []),
            "explanation": anchors_raw.get("explanation", "")
        },
        "contracts": contracts_raw,
        "pruned_events": pruned_events,
        "validation_warnings": validation_warnings,
        "metadata": metadata,
        "story_text": story_text
    }


def adapt_rich_event_graph_to_vis(rich_data: Dict[str, Any], output_id: str, outputs_dir: Path) -> Dict[str, Any]:
    """
    Transforms raw rich_event_graph.json into normalized visualization model.
    """
    norm_events = rich_data.get("normalized_events", {})
    atomic_events = rich_data.get("atomic_events", {})
    relations = rich_data.get("relations", [])
    
    vis_nodes = []
    
    if norm_events:
        for nid, ne in norm_events.items():
            tg = ne.get("temporal_grounding", {})
            atom_ids = ne.get("atomic_event_ids", [])
            spans = [atomic_events[aid].get("text_span", "") for aid in atom_ids if aid in atomic_events]
            
            vis_nodes.append({
                "id": nid,
                "label": f"{nid}: {ne.get('summary_label', nid)}",
                "predicate": ne.get("predicate_name", ""),
                "summary": ne.get("summary_label", ""),
                "arguments": ne.get("arguments", {}),
                "atomic_event_ids": atom_ids,
                "provenance_text_spans": spans,
                "polarity": ne.get("polarity", "positive"),
                "confidence": ne.get("confidence", 1.0),
                "temporal_grounding": {
                    "mention_phase": tg.get("mention_phase", "UNANCHORED"),
                    "onset_phase": tg.get("onset_phase", "UNANCHORED"),
                    "holds_at_intervention": tg.get("holds_at_intervention", False),
                    "temporal_extent": tg.get("temporal_extent", "POINT")
                },
                "node_type": "normalized_event"
            })
    else:
        for eid, ae in atomic_events.items():
            vis_nodes.append({
                "id": eid,
                "label": f"{eid}: {ae.get('predicate', eid)}",
                "predicate": ae.get("predicate", ""),
                "text_span": ae.get("text_span", ""),
                "participants": ae.get("participants", []),
                "event_type": ae.get("event_type", ""),
                "polarity": ae.get("polarity", "positive"),
                "confidence": ae.get("confidence", 1.0),
                "sentence_id": ae.get("sentence_id", 0),
                "provenance_text_spans": [ae.get("text_span", "")],
                "node_type": "atomic_event"
            })
            
    vis_edges = []
    for r in relations:
        rel_type = r.get("relation_type", "CAUSES")
        is_temp = rel_type == "BEFORE"
        vis_edges.append({
            "id": r.get("relation_id", f"{r.get('source_id')}_{r.get('target_id')}"),
            "source": r.get("source_id"),
            "target": r.get("target_id"),
            "label": rel_type,
            "category": "temporal" if is_temp else "explanatory",
            "is_temporal": is_temp,
            "evidence": r.get("evidence", ""),
            "provenance_span": r.get("provenance_span", ""),
            "confidence": r.get("confidence", 1.0),
            "explicitness": r.get("explicitness", "explicit")
        })
        
    story_text = load_story_text(output_id, outputs_dir)
    
    return {
        "story_id": rich_data.get("story_id", output_id),
        "view_type": "rich",
        "nodes": vis_nodes,
        "edges": vis_edges,
        "metadata": rich_data.get("metadata", {}),
        "story_text": story_text
    }
