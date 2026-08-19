from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from analogy_schema.models.story import Story
from analogy_schema.models.graph import RichEventGraph
from analogy_schema.models.events import NormalizedEvent, AtomicEvent, Explicitness
from analogy_schema.models.relations import RelationType
from analogy_schema.models.backbone import (
    AbstractionLadder,
    MacroNode,
    BackboneNode,
    BackboneEdge,
    NarrativeAnchors,
    CausalBackbone,
)
from analogy_schema.llm.base import BaseLLMProvider
from analogy_schema.prompts.registry import PromptRegistry


class GeneratedMacroNode(BaseModel):
    macro_id: str
    label: str
    source_normalized_ids: List[str]
    functional_role: str
    temporal_order: int
    abstraction_level_0: str
    abstraction_level_1: str
    abstraction_level_2: str
    abstraction_level_3: str
    is_intervention: bool = False
    is_terminal_outcome: bool = False


class GeneratedBackboneEdge(BaseModel):
    edge_id: str
    source_macro_id: str
    target_macro_id: str
    relation_type: RelationType
    justification: str


class MacroAbstractionOutput(BaseModel):
    macro_nodes: List[GeneratedMacroNode] = Field(default_factory=list)
    backbone_edges: List[GeneratedBackboneEdge] = Field(default_factory=list)


def run_stage_g_and_h_macro_and_abstraction(
    story: Story,
    graph: RichEventGraph,
    retained_events: List[NormalizedEvent],
    anchors: NarrativeAnchors,
    pruned_ids: List[str],
    pruned_reasons: Dict[str, str],
    llm: BaseLLMProvider
) -> CausalBackbone:
    """
    Stages G & H: Form Macro-Nodes, construct 4-Level Abstraction Ladders, and compile the CausalBackbone.
    """
    prompt = PromptRegistry.render(
        "macro_abstraction",
        story=story,
        retained_events=retained_events
    )
    system_prompt = "You are an abstract schema induction engineer creating multi-level causal event graphs."
    
    result = llm.generate_structured(
        prompt=prompt,
        response_model=MacroAbstractionOutput,
        system_prompt=system_prompt
    )
    
    nodes_dict: Dict[str, BackboneNode] = {}
    macro_to_backbone_id: Dict[str, str] = {}
    
    for i, gmn in enumerate(result.macro_nodes, start=1):
        node_id = f"N{i}"
        macro_to_backbone_id[gmn.macro_id] = node_id
        
        # Collect underlying atomic IDs and provenance spans
        source_atomic_ids = []
        provenance_spans = []
        for item_id in gmn.source_normalized_ids:
            if item_id in graph.normalized_events:
                ne = graph.normalized_events[item_id]
                for aid in ne.atomic_event_ids:
                    source_atomic_ids.append(aid)
                    if aid in graph.atomic_events:
                        provenance_spans.append(graph.atomic_events[aid].text_span)
            elif item_id in graph.atomic_events:
                source_atomic_ids.append(item_id)
                provenance_spans.append(graph.atomic_events[item_id].text_span)
                        
        macro_obj = MacroNode(
            macro_id=gmn.macro_id,
            label=gmn.label,
            source_normalized_ids=gmn.source_normalized_ids,
            source_atomic_ids=source_atomic_ids,
            functional_role=gmn.functional_role,
            temporal_order=gmn.temporal_order
        )
        
        ladder = AbstractionLadder(
            level_0_raw=gmn.abstraction_level_0,
            level_1_domain=gmn.abstraction_level_1,
            level_2_functional=gmn.abstraction_level_2,
            level_3_schema=gmn.abstraction_level_3
        )
        
        backbone_node = BackboneNode(
            node_id=node_id,
            macro_node=macro_obj,
            abstraction=ladder,
            functional_role=gmn.functional_role,
            is_intervention=gmn.is_intervention,
            is_terminal_outcome=gmn.is_terminal_outcome,
            provenance_text_spans=list(set(provenance_spans)),
            confidence=1.0,
            explicitness=Explicitness.EXPLICIT
        )
        nodes_dict[node_id] = backbone_node
        
    backbone_edges: List[BackboneEdge] = []
    for i, gbe in enumerate(result.backbone_edges, start=1):
        src_id = macro_to_backbone_id.get(gbe.source_macro_id, gbe.source_macro_id)
        dst_id = macro_to_backbone_id.get(gbe.target_macro_id, gbe.target_macro_id)
        
        # Look for underlying relations in rich graph
        underlying_rids = []
        for rel in graph.relations:
            # check if source/target match underlying norm ids
            src_node = nodes_dict.get(src_id)
            dst_node = nodes_dict.get(dst_id)
            if src_node and dst_node:
                if (rel.source_id in src_node.macro_node.source_normalized_ids and
                    rel.target_id in dst_node.macro_node.source_normalized_ids):
                    underlying_rids.append(rel.relation_id)
                    
        backbone_edges.append(BackboneEdge(
            edge_id=f"BE{i}",
            source_id=src_id,
            target_id=dst_id,
            relation_type=gbe.relation_type,
            justification=gbe.justification,
            confidence=1.0,
            underlying_relation_ids=underlying_rids
        ))
        
    return CausalBackbone(
        backbone_id=f"backbone_{story.story_id}",
        story_id=story.story_id,
        nodes=nodes_dict,
        edges=backbone_edges,
        anchors=anchors,
        pruned_node_ids=pruned_ids,
        pruned_reasons=pruned_reasons,
        metadata={"total_backbone_nodes": len(nodes_dict), "total_backbone_edges": len(backbone_edges)}
    )
