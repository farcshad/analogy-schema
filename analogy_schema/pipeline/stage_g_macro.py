import re
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import defaultdict
from pydantic import BaseModel, Field
from analogy_schema.models.story import Story
from analogy_schema.models.graph import RichEventGraph
from analogy_schema.models.events import (
    NormalizedEvent,
    Explicitness,
    BackboneRole,
    InterventionPhase,
    TemporalExtent,
    TemporalGrounding,
)
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
    label: str = Field(description="Neutral state or event label (without relational clauses)")
    source_normalized_ids: List[str] = Field(description="Retained normalized event IDs mapped to this macro node")
    functional_role: BackboneRole = Field(description="Controlled generic role")
    temporal_order: int = Field(default=0)
    abstraction_level_0: str
    abstraction_level_1: str
    abstraction_level_2: str = Field(description="Atomic functional role/state description (no relational clauses)")
    abstraction_level_3: str


class MacroGroupingOutput(BaseModel):
    macro_nodes: List[GeneratedMacroNode] = Field(default_factory=list)


def enforce_anti_merging_constraints(
    proposed_nodes: List[GeneratedMacroNode],
    graph: RichEventGraph
) -> List[GeneratedMacroNode]:
    """
    Hard Invariant: If two normalized events are connected by a meaningful relation
    (CAUSES, RESULTS_IN, BLOCKS, PREVENTS, ENABLES, MOTIVATES, REQUIRES, BEFORE),
    they MUST NOT be merged into a single macro-node.
    """
    # Build set of related pairs in rich graph
    related_pairs: Set[Tuple[str, str]] = set()
    for rel in graph.relations:
        related_pairs.add((rel.source_id, rel.target_id))
        related_pairs.add((rel.target_id, rel.source_id))
        
    sanitized_nodes: List[GeneratedMacroNode] = []
    split_counter = 1
    
    for gmn in proposed_nodes:
        if len(gmn.source_normalized_ids) <= 1:
            sanitized_nodes.append(gmn)
            continue
            
        # Check if any two events in this macro-node have a relation between them
        has_internal_relation = False
        events = gmn.source_normalized_ids
        for i in range(len(events)):
            for j in range(i + 1, len(events)):
                if (events[i], events[j]) in related_pairs:
                    has_internal_relation = True
                    break
            if has_internal_relation:
                break
                
        if not has_internal_relation:
            sanitized_nodes.append(gmn)
        else:
            # Split into individual single-event macro nodes to preserve structural edges
            for ne_id in events:
                ne = graph.normalized_events.get(ne_id)
                summary = ne.summary_label if ne else ne_id
                sanitized_nodes.append(GeneratedMacroNode(
                    macro_id=f"{gmn.macro_id}_split_{split_counter}",
                    label=summary,
                    source_normalized_ids=[ne_id],
                    functional_role=gmn.functional_role,
                    temporal_order=gmn.temporal_order,
                    abstraction_level_0=summary,
                    abstraction_level_1=summary,
                    abstraction_level_2=summary,
                    abstraction_level_3=gmn.abstraction_level_3
                ))
                split_counter += 1
                
    return sanitized_nodes


def sanitize_level_2_label(label: str) -> str:
    """Removes relational connective clauses from Level-2 functional descriptions."""
    sanitized = label
    patterns = [
        r"(?i)\s+caused by.*$",
        r"(?i)\s+due to.*$",
        r"(?i)\s+leading to.*$",
        r"(?i)\s+results in.*$",
        r"(?i)\s+resulting in.*$",
        r"(?i)\s+because of.*$",
        r"(?i)\s+despite.*$",
    ]
    for pat in patterns:
        sanitized = re.sub(pat, "", sanitized).strip()
    return sanitized if sanitized else label


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
    projected: Dict[Tuple[str, str], List[EventRelation]] = defaultdict(list)
    
    for rel in graph.relations:
        src_bb = ne_to_backbone_id.get(rel.source_id)
        dst_bb = ne_to_backbone_id.get(rel.target_id)
        
        if src_bb and dst_bb and src_bb != dst_bb:
            projected[(src_bb, dst_bb)].append(rel)
            
    relation_priority = {
        RelationType.RESULTS_IN: 10,
        RelationType.CAUSES: 9,
        RelationType.BLOCKS: 8,
        RelationType.PREVENTS: 8,
        RelationType.ENABLES: 7,
        RelationType.REQUIRES: 6,
        RelationType.MOTIVATES: 5,
        RelationType.BEFORE: 1,
    }
    
    backbone_edges: List[BackboneEdge] = []
    edge_idx = 1
    
    for (src_id, dst_id), rel_list in projected.items():
        rel_list_sorted = sorted(
            rel_list,
            key=lambda r: relation_priority.get(r.relation_type, 0),
            reverse=True
        )
        primary_rel = rel_list_sorted[0]
        
        underlying_ids = [r.relation_id for r in rel_list]
        evidence_snippets = [r.evidence for r in rel_list if r.evidence]
        justification = "; ".join(evidence_snippets) if evidence_snippets else primary_rel.evidence
        
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
    2. Anti-merging programmatic constraint prevents destruction of relational edges.
    3. Relational clauses are stripped from Level-2 node labels.
    4. Backbone edges are strictly and deterministically lifted from Stage-C Rich Graph relations.
    5. Invariants are validated and attached to metadata.
    """
    retained_ids = set(e.norm_id for e in retained_events)
    retained_relations = [
        r for r in graph.relations
        if r.source_id in retained_ids and r.target_id in retained_ids
    ]
    
    prompt = PromptRegistry.render(
        "macro_grouping",
        story=story,
        retained_events=retained_events,
        rich_relations=retained_relations
    )
    system_prompt = "You are a scientific abstract schema induction parser grouping events into atomic functional macro-nodes."
    
    result = llm.generate_structured(
        prompt=prompt,
        response_model=MacroGroupingOutput,
        system_prompt=system_prompt
    )
    
    # Enforce programmatic anti-merging constraint
    sanitized_nodes = enforce_anti_merging_constraints(result.macro_nodes, graph)
    
    nodes_dict: Dict[str, BackboneNode] = {}
    macro_to_backbone_id: Dict[str, str] = {}
    ne_to_backbone_id: Dict[str, str] = {}
    
    intervention_set = set(anchors.intervention_event_ids)
    focal_outcome_set = set(anchors.focal_outcome_ids)
    contingent_outcome_set = set(anchors.contingent_outcome_ids)
    
    for i, gmn in enumerate(sanitized_nodes, start=1):
        node_id = f"N{i}"
        macro_to_backbone_id[gmn.macro_id] = node_id
        
        source_atomic_ids = []
        provenance_spans = []
        is_intervention = False
        is_focal = False
        is_contingent = False
        
        groundings: List[TemporalGrounding] = []
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
                groundings.append(ne.temporal_grounding)
                for aid in ne.atomic_event_ids:
                    source_atomic_ids.append(aid)
                    if aid in graph.atomic_events:
                        provenance_spans.append(graph.atomic_events[aid].text_span)
            elif item_id in graph.atomic_events:
                source_atomic_ids.append(item_id)
                provenance_spans.append(graph.atomic_events[item_id].text_span)
                
        # Resolve temporal grounding from source events
        if groundings:
            first_tg = groundings[0]
            onset = (
                InterventionPhase.SPANS_INTERVENTION
                if any(g.onset_phase == InterventionPhase.SPANS_INTERVENTION for g in groundings)
                else (
                    InterventionPhase.PRE_INTERVENTION
                    if any(g.onset_phase == InterventionPhase.PRE_INTERVENTION for g in groundings)
                    else first_tg.onset_phase
                )
            )
            holds_at_int = any(g.holds_at_intervention for g in groundings)
            node_tg = TemporalGrounding(
                mention_phase=first_tg.mention_phase,
                onset_phase=onset,
                holds_at_intervention=holds_at_int,
                temporal_extent=first_tg.temporal_extent
            )
        else:
            node_tg = TemporalGrounding()
            
        # Clean label and level-2 abstraction of relational clauses
        cleaned_label = sanitize_level_2_label(gmn.label)
        cleaned_level_2 = sanitize_level_2_label(gmn.abstraction_level_2)
        
        macro_obj = MacroNode(
            macro_id=gmn.macro_id,
            label=cleaned_label,
            source_normalized_ids=gmn.source_normalized_ids,
            source_atomic_ids=source_atomic_ids,
            functional_role=gmn.functional_role,
            temporal_grounding=node_tg,
            temporal_order=gmn.temporal_order
        )
        
        ladder = AbstractionLadder(
            level_0_raw=gmn.abstraction_level_0,
            level_1_domain=gmn.abstraction_level_1,
            level_2_functional=cleaned_level_2,
            level_3_schema=gmn.abstraction_level_3
        )
        
        backbone_node = BackboneNode(
            node_id=node_id,
            macro_node=macro_obj,
            abstraction=ladder,
            functional_role=gmn.functional_role,
            temporal_grounding=node_tg,
            is_intervention=is_intervention or gmn.functional_role == BackboneRole.INTERVENTION,
            is_focal_outcome=is_focal or gmn.functional_role == BackboneRole.FOCAL_OUTCOME,
            is_contingent_outcome=is_contingent or gmn.functional_role == BackboneRole.CONTINGENT_OUTCOME,
            provenance_text_spans=list(set(provenance_spans)),
            confidence=1.0,
            explicitness=Explicitness.EXPLICIT
        )
        nodes_dict[node_id] = backbone_node
        
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
    
    warnings = backbone.validate_invariants()
    backbone.metadata["validation_warnings"] = warnings
    
    return backbone
