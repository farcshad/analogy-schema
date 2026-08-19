from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from analogy_schema.models.relations import RelationType, EventRelation
from analogy_schema.models.events import Explicitness


class AbstractionLadder(BaseModel):
    level_0_raw: str = Field(description="Story-grounded literal description (e.g. 'William spends time daydreaming about food')")
    level_1_domain: str = Field(description="Domain-specific semantic predicate (e.g. 'William neglects cleaning his room')")
    level_2_functional: str = Field(description="Functional causal role / relational label (e.g. 'task neglect / inaction')")
    level_3_schema: str = Field(description="High-level abstract schema label (e.g. 'failure to pursue requirement')")


class MacroNode(BaseModel):
    macro_id: str = Field(description="Unique macro node ID, e.g., M1, M2")
    label: str = Field(description="Descriptive summary label")
    source_normalized_ids: List[str] = Field(default_factory=list)
    source_atomic_ids: List[str] = Field(default_factory=list)
    functional_role: str = Field(description="Explanatory role, e.g., 'primary_cause', 'intervention', 'terminal_outcome'")
    temporal_order: int = Field(default=0, description="Coarse temporal placement in narrative progression")


class BackboneNode(BaseModel):
    node_id: str = Field(description="Unique backbone node ID, e.g., N1, N2")
    macro_node: MacroNode
    abstraction: AbstractionLadder
    functional_role: str = Field(description="Functional role in causal backbone")
    is_intervention: bool = Field(default=False)
    is_terminal_outcome: bool = Field(default=False)
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
    underlying_relation_ids: List[str] = Field(default_factory=list)


class NarrativeAnchors(BaseModel):
    central_problem: Optional[str] = None
    central_goal: Optional[str] = None
    intervention: Optional[str] = None
    terminal_outcomes: List[str] = Field(default_factory=list)
    anchor_event_ids: List[str] = Field(default_factory=list)


class CausalBackbone(BaseModel):
    backbone_id: str
    story_id: str
    nodes: Dict[str, BackboneNode] = Field(default_factory=dict)
    edges: List[BackboneEdge] = Field(default_factory=list)
    anchors: NarrativeAnchors = Field(default_factory=NarrativeAnchors)
    pruned_node_ids: List[str] = Field(default_factory=list, description="IDs of events removed during backbone selection")
    pruned_reasons: Dict[str, str] = Field(default_factory=dict, description="Audit trail explaining why nodes were pruned")
    metadata: Dict[str, Any] = Field(default_factory=dict)
