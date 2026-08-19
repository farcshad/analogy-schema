from typing import List, Dict, Any, Optional, Set
from collections import defaultdict
from pydantic import BaseModel, Field
from analogy_schema.models.story import Story
from analogy_schema.models.graph import RichEventGraph
from analogy_schema.models.events import NormalizedEvent, Explicitness, BackboneRole, InterventionPhase
from analogy_schema.models.relations import RelationType, EventRelation
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
    macro_id: str = Field(description="Temporary ID, e.g., M1, M2")
    label: str = Field(description="Neutral state or event label")
    source_normalized_ids: List[str] = Field(description="Retained normalized event IDs mapped to this macro node")
    functional_role: BackboneRole = Field(description="Controlled generic role")
    temporal_phase: InterventionPhase = Field(default=InterventionPhase.UNANCHORED, description="Temporal phase relative to intervention")
    temporal_order: int = Field(default=0)
    abstraction_level_0: str
    abstraction_level_1: str
    abstraction_level_2: str
    abstraction_level_3: str


class MacroGroupingOutput(BaseModel):
    macro_nodes: List[GeneratedMacroNode] = Field(default_factory=list)


def lift_rich_relations_to_backbone_edges(
    graph: RichEventGraph,
    nodes_dict: Dict[str, BackboneNode],
    ne_to_backbone_id: Dict[str, str]
) -> List[BackboneEdge]:
    """
    Deterministic Edge Lifting Algorithm.
    Projects Stage-C Rich Graph relations onto MacroNodes.
    Enforces invariant: Every BackboneEdge must be grounded in underlying rich relation IDs.
    """
    # Map pair (src_node_id, dst_node_id) -> list of EventRelation
    projected: Dict[Tuple[str, str], List[EventRelation]] = defaultdict(list)
    
    for rel in graph.relations:
        src_bb = ne_to_backbone_id.get(rel.source_id)
        dst_bb = ne_to_backbone_id.get(rel.target_id)
        
        # Check if relation connects two distinct retained backbone nodes
        if src_bb and dst_bb and src_bb != dst_bb:
            projected[(src_bb, dst_bb)].append(rel)
            
    # Priority rank for adjudicating multiple relations between same pair
    relation_priority = {
        RelationType.RESULTS_IN: 10,
        RelationType.CAUSES: 9,
        RelationType.BLOCKS: 8,
        RelationType.PREVENTS: 8,
        RelationType.ENABLES: 7,
        RelationType.REQUIRES: 6,
        RelationType.CONDITIONAL_ON: 6,
        RelationType.MOTIVATES: 5,
        RelationType.BEFORE: 1,
    }
    
    backbone_edges: List[BackboneEdge] = []
    edge_idx = 1
    
    for (src_id, dst_id), rel_list in projected.items():
        # Sort relations by priority
        rel_list_sorted = sorted(
            rel_list,
            key=lambda r: relation_priority.get(r.relation_type, 0),
            reverse=True
        )
        primary_rel = rel_list_sorted[0]
        
        # Collect all underlying relation IDs
        underlying_ids = [r.relation_id for r in rel_list]
        evidence_snippets = [r.evidence for r in rel_list if r.evidence]
        justification = "; ".join(evidence_snippets) if evidence_snippets else primary_rel.evidence
        
        # Check if there is an adjudicated conflict (e.g. BEFORE + CAUSES)
        types_present = set(r.relation_type for r in rel_list)
        if len(types_present) > 1:
            conflict_desc = f"Adjudicated between {', '.join(t.value for t in types_present)}: prioritized {primary_rel.relation_type.value}."
            justification = f"{justification} [{conflict_desc}]" if justification else conflict_desc
            
        edge = BackboneEdge(
            edge_id=f"BE{edge_idx}",
            source_id=src_id,
            target_id=dst_id,
            relation_type=primary_rel.relation_type,
            justification=justification,
            confidence=min(r.confidence for r in rel_list),
            explicitness=primary_rel.explicitness,
            underlying_relation_ids=underlying_ids
        )
        backbone_edges.append(edge)
        edge_idx += 1
        
    return backbone_edges


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
    Stages G & H:
    1. LLM groups retained events into MacroNodes with 4-Level Abstraction Ladders.
    2. Backbone edges are strictly and deterministically lifted from Stage-C Rich Graph relations.
    3. Invariants are validated and attached to metadata.
    """
    ne_phase_map = {ne.norm_id: ne.temporal_phase.value for ne in retained_events}
    prompt = PromptRegistry.render(
        "macro_grouping",
        story=story,
        retained_events=retained_events,
        ne_phase_map=ne_phase_map
    )
    system_prompt = "You are a scientific abstract schema induction parser grouping events into functional macro-nodes."
    
    result = llm.generate_structured(
        prompt=prompt,
        response_model=MacroGroupingOutput,
        system_prompt=system_prompt
    )
    
    nodes_dict: Dict[str, BackboneNode] = {}
    macro_to_backbone_id: Dict[str, str] = {}
    ne_to_backbone_id: Dict[str, str] = {}
    
    intervention_set = set(anchors.intervention_event_ids)
    focal_outcome_set = set(anchors.focal_outcome_ids)
    contingent_outcome_set = set(anchors.contingent_outcome_ids)
    
    for i, gmn in enumerate(result.macro_nodes, start=1):
        node_id = f"N{i}"
        macro_to_backbone_id[gmn.macro_id] = node_id
        
        # Collect source atomic IDs and provenance spans
        source_atomic_ids = []
        provenance_spans = []
        is_intervention = False
        is_focal = False
        is_contingent = False
        
        # Determine temporal phase from source events or model
        phases = []
        for item_id in gmn.source_normalized_ids:
            ne_to_backbone_id[item_id] = node_id
            if item_id in intervention_set:
                is_intervention = True
            if item_id in focal_outcome_set:
                is_focal = True
            if item_id in contingent_outcome_set:
                is_contingent = True
                
            if item_id in graph.normalized_events:
                ne = graph.normalized_events[item_id]
                phases.append(ne.temporal_phase)
                for aid in ne.atomic_event_ids:
                    source_atomic_ids.append(aid)
                    if aid in graph.atomic_events:
                        provenance_spans.append(graph.atomic_events[aid].text_span)
            elif item_id in graph.atomic_events:
                source_atomic_ids.append(item_id)
                provenance_spans.append(graph.atomic_events[item_id].text_span)
                
        # Resolve temporal phase
        if gmn.temporal_phase and gmn.temporal_phase != InterventionPhase.UNANCHORED:
            node_phase = gmn.temporal_phase
        elif phases:
            if InterventionPhase.SPANS_INTERVENTION in phases:
                node_phase = InterventionPhase.SPANS_INTERVENTION
            elif InterventionPhase.PRE_INTERVENTION in phases:
                node_phase = InterventionPhase.PRE_INTERVENTION
            elif InterventionPhase.POST_INTERVENTION in phases:
                node_phase = InterventionPhase.POST_INTERVENTION
            else:
                node_phase = phases[0]
        else:
            node_phase = InterventionPhase.UNANCHORED
            
        macro_obj = MacroNode(
            macro_id=gmn.macro_id,
            label=gmn.label,
            source_normalized_ids=gmn.source_normalized_ids,
            source_atomic_ids=source_atomic_ids,
            functional_role=gmn.functional_role,
            temporal_phase=node_phase,
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
            temporal_phase=node_phase,
            is_intervention=is_intervention or gmn.functional_role == BackboneRole.INTERVENTION,
            is_focal_outcome=is_focal or gmn.functional_role == BackboneRole.FOCAL_OUTCOME,
            is_contingent_outcome=is_contingent or gmn.functional_role == BackboneRole.CONTINGENT_OUTCOME,
            provenance_text_spans=list(set(provenance_spans)),
            confidence=1.0,
            explicitness=Explicitness.EXPLICIT
        )
        nodes_dict[node_id] = backbone_node
        
    # Strictly lift edges deterministically from Stage-C Rich Graph
    backbone_edges = lift_rich_relations_to_backbone_edges(
        graph=graph,
        nodes_dict=nodes_dict,
        ne_to_backbone_id=ne_to_backbone_id
    )
    
    backbone = CausalBackbone(
        backbone_id=f"backbone_{story.story_id}",
        story_id=story.story_id,
        nodes=nodes_dict,
        edges=backbone_edges,
        anchors=anchors,
        pruned_node_ids=pruned_ids,
        pruned_reasons=pruned_reasons,
        metadata={
            "total_backbone_nodes": len(nodes_dict),
            "total_backbone_edges": len(backbone_edges),
            "edge_derivation_method": "deterministic_rich_relation_lifting"
        }
    )
    
    # Invariant validation
    warnings = backbone.validate_invariants()
    backbone.metadata["validation_warnings"] = warnings
    
    return backbone


# Type alias for cleaner code
Tuple_List_BackboneEdge = List[BackboneEdge]
from typing import Tuple
