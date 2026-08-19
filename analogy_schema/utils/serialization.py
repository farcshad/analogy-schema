import json
from typing import Any, Dict
from pydantic import BaseModel
from analogy_schema.models.backbone import CausalBackbone
from analogy_schema.models.graph import RichEventGraph


def to_json(model: BaseModel, indent: int = 2) -> str:
    """Serializes any Pydantic model to formatted JSON string."""
    return model.model_dump_json(indent=indent)


def save_json(model: BaseModel, filepath: str) -> None:
    """Saves a model to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(to_json(model))


def load_json(cls, filepath: str):
    """Loads a Pydantic model from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return cls.model_validate(data)


def export_backbone_markdown(backbone: CausalBackbone) -> str:
    """Generates an inspectable markdown summary of the causal backbone with provenance."""
    lines = [
        f"# Causal Backbone: {backbone.story_id}",
        "",
        "## Narrative Anchors",
        f"- **Central Problem**: {backbone.anchors.central_problem}",
        f"- **Central Goal**: {backbone.anchors.central_goal}",
        f"- **Intervention**: {backbone.anchors.intervention}",
        f"- **Terminal Outcomes**: {', '.join(backbone.anchors.terminal_outcomes)}",
        "",
        "## Backbone Nodes (Level 2 Functional Roles)",
    ]
    
    for nid, node in backbone.nodes.items():
        intervention_tag = " `[INTERVENTION]`" if node.is_intervention else ""
        outcome_tag = " `[OUTCOME]`" if node.is_terminal_outcome else ""
        lines.append(f"### {nid}: {node.abstraction.level_2_functional}{intervention_tag}{outcome_tag}")
        lines.append(f"- **Role**: {node.functional_role}")
        lines.append(f"- **Abstraction Ladder**:")
        lines.append(f"  - *Level 0 (Raw)*: {node.abstraction.level_0_raw}")
        lines.append(f"  - *Level 1 (Domain)*: {node.abstraction.level_1_domain}")
        lines.append(f"  - *Level 2 (Functional)*: {node.abstraction.level_2_functional}")
        lines.append(f"  - *Level 3 (Schema)*: {node.abstraction.level_3_schema}")
        lines.append(f"- **Underlying Macro-Node**: `{node.macro_node.macro_id}` ({node.macro_node.label})")
        lines.append(f"- **Source Events**: {node.macro_node.source_normalized_ids or node.macro_node.source_atomic_ids}")
        lines.append(f"- **Textual Provenance Spans**: {node.provenance_text_spans}")
        lines.append("")
        
    lines.append("## Backbone Edges (Typed Relational Backbone)")
    for edge in backbone.edges:
        src = backbone.nodes.get(edge.source_id)
        dst = backbone.nodes.get(edge.target_id)
        src_lbl = src.abstraction.level_2_functional if src else edge.source_id
        dst_lbl = dst.abstraction.level_2_functional if dst else edge.target_id
        lines.append(f"- **`{edge.source_id}` ({src_lbl})** `--{edge.relation_type.value}-->` **`{edge.target_id}` ({dst_lbl})**")
        if edge.justification:
            lines.append(f"  - *Justification*: {edge.justification}")
            
    if backbone.pruned_node_ids:
        lines.append("")
        lines.append("## Pruned Events (Audit Trail)")
        for pid in backbone.pruned_node_ids:
            reason = backbone.pruned_reasons.get(pid, "Non-essential narrative decoration / non-explanatory")
            lines.append(f"- **`{pid}`**: {reason}")
            
    return "\n".join(lines)
