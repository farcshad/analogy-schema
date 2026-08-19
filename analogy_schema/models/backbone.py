import re
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from analogy_schema.models.relations import RelationType, EventRelation
from analogy_schema.models.events import Explicitness, BackboneRole, InterventionPhase, TemporalGrounding, Polarity


class IncentiveContract(BaseModel):
    intervention_event_id: Optional[str] = None
    promised_reward: str = Field(description="The incentive reward offered")
    contingent_requirement: str = Field(description="The condition/standard required to earn the reward")
    condition_polarity: Polarity = Field(default=Polarity.POSITIVE)


class AbstractionLadder(BaseModel):
    level_0_raw: str = Field(description="Story-grounded literal description")
    level_1_domain: str = Field(description="Domain-specific semantic predicate")
    level_2_functional: str = Field(description="Atomic functional causal role / state description (no relational clauses)")
    level_3_schema: str = Field(description="High-level abstract schema label")


class MacroNode(BaseModel):
    macro_id: str = Field(description="Unique macro node ID, e.g., M1, M2")
    label: str = Field(description="Atomic state or event label (without relational clauses)")
    source_normalized_ids: List[str] = Field(default_factory=list)
    source_atomic_ids: List[str] = Field(default_factory=list)
    functional_role: BackboneRole = Field(default=BackboneRole.PROBLEM_STATE)
    temporal_grounding: TemporalGrounding = Field(default_factory=TemporalGrounding)
    temporal_order: int = Field(default=0)


class BackboneNode(BaseModel):
    node_id: str = Field(description="Unique backbone node ID, e.g., N1, N2")
    macro_node: MacroNode
    abstraction: AbstractionLadder
    functional_role: BackboneRole = Field(default=BackboneRole.PROBLEM_STATE)
    temporal_grounding: TemporalGrounding = Field(default_factory=TemporalGrounding)
    is_intervention: bool = Field(default=False)
    is_focal_outcome: bool = Field(default=False)
    is_contingent_outcome: bool = Field(default=False)
    provenance_text_spans: List[str] = Field(default_factory=list)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    explicitness: Explicitness = Field(default=Explicitness.EXPLICIT)

    @property
    def onset_phase(self) -> InterventionPhase:
        return self.temporal_grounding.onset_phase

    @property
    def holds_at_intervention(self) -> bool:
        return self.temporal_grounding.holds_at_intervention

    @property
    def mention_phase(self) -> InterventionPhase:
        return self.temporal_grounding.mention_phase


class BackboneEdge(BaseModel):
    edge_id: str = Field(description="Unique backbone edge ID, e.g., BE1, BE2")
    source_id: str
    target_id: str
    relation_type: RelationType
    justification: Optional[str] = Field(default=None, description="Counterfactual or explanatory rationale")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    explicitness: Explicitness = Field(default=Explicitness.EXPLICIT)
    underlying_relation_ids: List[str] = Field(
        default_factory=list,
        description="Mandatory provenance: Stage-C Rich Graph relation IDs from which this edge is lifted"
    )


class NarrativeAnchors(BaseModel):
    central_problem: Optional[str] = None
    central_goal: Optional[str] = None
    intervention_event_ids: List[str] = Field(default_factory=list, description="IDs of intervention events")
    focal_outcome_ids: List[str] = Field(default_factory=list, description="IDs of primary focal outcome events")
    contingent_outcome_ids: List[str] = Field(default_factory=list, description="IDs of contingent consequences")
    downstream_reaction_ids: List[str] = Field(default_factory=list, description="IDs of emotional reactions (excluded from causal anchors)")
    contracts: List[IncentiveContract] = Field(default_factory=list, description="Structured incentive contract metadata")
    explanation: Optional[str] = None

    @property
    def anchor_event_ids(self) -> List[str]:
        return list(set(self.focal_outcome_ids + self.contingent_outcome_ids))


class CausalBackbone(BaseModel):
    backbone_id: str
    story_id: str
    nodes: Dict[str, BackboneNode] = Field(default_factory=dict)
    edges: List[BackboneEdge] = Field(default_factory=list)
    anchors: NarrativeAnchors = Field(default_factory=NarrativeAnchors)
    pruned_node_ids: List[str] = Field(default_factory=list)
    pruned_reasons: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def validate_invariants(self) -> List[str]:
        """
        Validates methodological and topological invariants:
        1. Edge provenance invariant.
        2. Temporal-causal consistency (e.g. POST_INTERVENTION node cannot precede or cause an intervention).
        3. Relational neutrality in node labels.
        4. Node existence & self-loop prevention.
        """
        warnings = []
        forbidden_label_phrases = [
            "caused by", "due to", "leading to", "results in", "resulting in",
            "because of", "despite intervention", "prevents "
        ]
        
        # Check node labels
        for nid, node in self.nodes.items():
            l2 = node.abstraction.level_2_functional.lower()
            for phrase in forbidden_label_phrases:
                if phrase in l2:
                    warnings.append(
                        f"Node {nid} Level-2 label '{node.abstraction.level_2_functional}' embeds relational phrase '{phrase}'. Prefer atomic event/state description."
                    )
                    
        # Check edges and temporal consistency
        for edge in self.edges:
            if edge.source_id not in self.nodes:
                warnings.append(f"Edge {edge.edge_id}: source_id '{edge.source_id}' does not exist in nodes.")
                continue
            if edge.target_id not in self.nodes:
                warnings.append(f"Edge {edge.edge_id}: target_id '{edge.target_id}' does not exist in nodes.")
                continue
            if edge.source_id == edge.target_id:
                warnings.append(f"Edge {edge.edge_id}: self-loop detected on '{edge.source_id}'.")
            if not edge.underlying_relation_ids:
                warnings.append(
                    f"Invariant Violation: Backbone edge {edge.edge_id} ({edge.source_id} -> {edge.target_id}) has no underlying rich relation provenance."
                )
                
            # Temporal-causal consistency check
            src_node = self.nodes[edge.source_id]
            dst_node = self.nodes[edge.target_id]
            
            src_onset = src_node.temporal_grounding.onset_phase
            dst_onset = dst_node.temporal_grounding.onset_phase
            
            if src_onset == InterventionPhase.POST_INTERVENTION and dst_onset in (InterventionPhase.PRE_INTERVENTION, InterventionPhase.AT_INTERVENTION):
                if edge.relation_type in (RelationType.CAUSES, RelationType.BEFORE, RelationType.ENABLES, RelationType.RESULTS_IN):
                    warnings.append(
                        f"Temporal Anomaly: Node {edge.source_id} (onset=POST_INTERVENTION) is linked via {edge.relation_type.value} to {edge.target_id} (onset={dst_onset.value})."
                    )
                    
        return warnings
