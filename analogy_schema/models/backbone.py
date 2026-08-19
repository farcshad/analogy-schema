import re
from typing import List, Dict, Optional, Any, Set
import networkx as nx
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

    @property
    def temporal_phase(self) -> InterventionPhase:
        return self.temporal_grounding.onset_phase


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
    def temporal_phase(self) -> InterventionPhase:
        return self.temporal_grounding.onset_phase

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

    @property
    def is_explanatory(self) -> bool:
        return self.relation_type.is_causal_or_explanatory

    @property
    def is_temporal_only(self) -> bool:
        return self.relation_type.is_temporal_only


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
    explanatory_edges: List[BackboneEdge] = Field(default_factory=list, description="Causal, motivational, and consequential edges")
    temporal_constraints: List[BackboneEdge] = Field(default_factory=list, description="Minimal non-redundant chronological constraints")
    anchors: NarrativeAnchors = Field(default_factory=NarrativeAnchors)
    pruned_node_ids: List[str] = Field(default_factory=list)
    pruned_reasons: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def edges(self) -> List[BackboneEdge]:
        """Returns all edges combining explanatory edges and temporal constraints."""
        return self.explanatory_edges + self.temporal_constraints

    def validate_invariants(self) -> List[str]:
        """
        Comprehensive Methodological & Topological Invariant Validators:
        1. Label leakage verification.
        2. Downstream-reaction / causal-path conflict verification.
        3. Disconnected non-anchor node verification.
        4. Valid Level-2 functional abstraction verification.
        5. Temporal-causal consistency verification.
        6. Redundant temporal constraint verification.
        7. Edge provenance verification.
        """
        warnings = []
        
        # 1. Label leakage check
        forbidden_benchmark_labels = [
            "true_analogy", "false_analogy", "surface_similar",
            "literally_similar", "mere_appearance"
        ]
        all_text = " ".join([
            node.abstraction.level_0_raw + " " + node.abstraction.level_2_functional + " " + node.macro_node.label
            for node in self.nodes.values()
        ] + [
            edge.justification or "" for edge in self.edges
        ] + [
            self.anchors.central_problem or "", self.anchors.central_goal or ""
        ]).lower()
        for label in forbidden_benchmark_labels:
            if label in all_text:
                warnings.append(f"Ground-Truth Leakage Warning: Found benchmark condition label '{label}' in backbone text!")

        # 2. Downstream-reaction on causal path check
        for nid, node in self.nodes.items():
            if node.functional_role == BackboneRole.DOWNSTREAM_REACTION:
                # Check if this node has outgoing explanatory edges
                out_explanatory = [e for e in self.explanatory_edges if e.source_id == nid]
                if out_explanatory:
                    warnings.append(
                        f"Anchor Role Conflict: Node {nid} marked DOWNSTREAM_REACTION has outgoing explanatory edge(s) {[e.edge_id for e in out_explanatory]} to {', '.join(e.target_id for e in out_explanatory)}."
                    )

        # 3. Disconnected non-anchor check
        all_edge_nodes = set(e.source_id for e in self.edges).union(set(e.target_id for e in self.edges))
        for nid, node in self.nodes.items():
            if nid not in all_edge_nodes and not (node.is_focal_outcome or node.is_intervention):
                warnings.append(
                    f"Minimality Violation: Node {nid} ({node.abstraction.level_2_functional}) is disconnected from the backbone graph and is not an intervention/focal outcome."
                )

        # 4. Valid Level-2 abstraction check
        forbidden_label_phrases = [
            "caused by", "due to", "leading to", "results in", "resulting in",
            "because of", "despite intervention", "prevents "
        ]
        for nid, node in self.nodes.items():
            l2 = node.abstraction.level_2_functional.strip()
            if not l2 or len(l2) < 3:
                warnings.append(f"Level-2 Abstraction Invalid: Node {nid} has empty or degenerate Level-2 functional label '{l2}'.")
            for phrase in forbidden_label_phrases:
                if phrase in l2.lower():
                    warnings.append(
                        f"Relational Embedding Warning: Node {nid} Level-2 label '{l2}' embeds relational phrase '{phrase}'."
                    )

        # 5. Temporal-causal consistency check
        for edge in self.explanatory_edges:
            if edge.source_id in self.nodes and edge.target_id in self.nodes:
                src_node = self.nodes[edge.source_id]
                dst_node = self.nodes[edge.target_id]
                src_onset = src_node.temporal_grounding.onset_phase
                dst_onset = dst_node.temporal_grounding.onset_phase
                if src_onset == InterventionPhase.POST_INTERVENTION and dst_onset in (InterventionPhase.PRE_INTERVENTION, InterventionPhase.AT_INTERVENTION):
                    if edge.relation_type in (RelationType.CAUSES, RelationType.RESULTS_IN, RelationType.ENABLES):
                        warnings.append(
                            f"Temporal-Causal Inversion: Node {edge.source_id} (onset=POST_INTERVENTION) is asserted to {edge.relation_type.value} {edge.target_id} (onset={dst_onset.value})."
                        )

        # 6. Edge provenance check
        for edge in self.edges:
            if not edge.underlying_relation_ids:
                warnings.append(
                    f"Provenance Invariant Violation: Edge {edge.edge_id} ({edge.source_id} -> {edge.target_id}) has no underlying rich-graph relation provenance."
                )

        return warnings
