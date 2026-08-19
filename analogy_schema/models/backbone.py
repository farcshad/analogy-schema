from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from analogy_schema.models.relations import RelationType, EventRelation
from analogy_schema.models.events import Explicitness, BackboneRole, InterventionPhase


class AbstractionLadder(BaseModel):
    level_0_raw: str = Field(description="Story-grounded literal description")
    level_1_domain: str = Field(description="Domain-specific semantic predicate")
    level_2_functional: str = Field(description="Functional causal role / relational state (target operating level)")
    level_3_schema: str = Field(description="High-level abstract schema label")


class MacroNode(BaseModel):
    macro_id: str = Field(description="Unique macro node ID, e.g., M1, M2")
    label: str = Field(description="Descriptive state/event label (do not embed relations in name)")
    source_normalized_ids: List[str] = Field(default_factory=list)
    source_atomic_ids: List[str] = Field(default_factory=list)
    functional_role: BackboneRole = Field(default=BackboneRole.PROBLEM_STATE)
    temporal_phase: InterventionPhase = Field(default=InterventionPhase.UNANCHORED)
    temporal_order: int = Field(default=0, description="Coarse temporal placement in narrative progression")


class BackboneNode(BaseModel):
    node_id: str = Field(description="Unique backbone node ID, e.g., N1, N2")
    macro_node: MacroNode
    abstraction: AbstractionLadder
    functional_role: BackboneRole = Field(default=BackboneRole.PROBLEM_STATE)
    temporal_phase: InterventionPhase = Field(default=InterventionPhase.UNANCHORED)
    is_intervention: bool = Field(default=False)
    is_focal_outcome: bool = Field(default=False)
    is_contingent_outcome: bool = Field(default=False)
    provenance_text_spans: List[str] = Field(default_factory=list)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    explicitness: Explicitness = Field(default=Explicitness.EXPLICIT)


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
    focal_outcome_ids: List[str] = Field(default_factory=list, description="IDs of primary focal outcome events (success/failure of goal)")
    contingent_outcome_ids: List[str] = Field(default_factory=list, description="IDs of contingent consequences (e.g. reward withheld/granted)")
    downstream_reaction_ids: List[str] = Field(default_factory=list, description="IDs of emotional reactions / incidental damage (NOT causal anchors)")
    explanation: Optional[str] = None

    @property
    def anchor_event_ids(self) -> List[str]:
        """Returns valid anchor event IDs for backward tracing (excludes downstream reactions)."""
        return list(set(self.focal_outcome_ids + self.contingent_outcome_ids))


class CausalBackbone(BaseModel):
    backbone_id: str
    story_id: str
    nodes: Dict[str, BackboneNode] = Field(default_factory=dict)
    edges: List[BackboneEdge] = Field(default_factory=list)
    anchors: NarrativeAnchors = Field(default_factory=NarrativeAnchors)
    pruned_node_ids: List[str] = Field(default_factory=list, description="IDs of events removed during backbone selection")
    pruned_reasons: Dict[str, str] = Field(default_factory=dict, description="Audit trail explaining why nodes were pruned")
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def validate_invariants(self) -> List[str]:
        """
        Validates methodological invariants:
        1. Every backbone edge must have underlying rich relation provenance.
        2. Source and Target nodes must exist in backbone.
        3. No self-loops.
        4. Downstream reactions must not be focal outcomes.
        """
        warnings = []
        for edge in self.edges:
            if edge.source_id not in self.nodes:
                warnings.append(f"Edge {edge.edge_id}: source_id '{edge.source_id}' does not exist in backbone nodes.")
            if edge.target_id not in self.nodes:
                warnings.append(f"Edge {edge.edge_id}: target_id '{edge.target_id}' does not exist in backbone nodes.")
            if edge.source_id == edge.target_id:
                warnings.append(f"Edge {edge.edge_id}: self-loop detected on '{edge.source_id}'.")
            if not edge.underlying_relation_ids:
                warnings.append(f"Invariant Violation: Backbone edge {edge.edge_id} ({edge.source_id} -> {edge.target_id}) has no underlying rich-graph relation provenance.")
        return warnings
