from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class NodeAlignment(BaseModel):
    alignment_id: str
    base_node_id: str
    target_node_id: str
    base_functional_role: str
    target_functional_role: str
    similarity_score: float = Field(ge=0.0, le=1.0)
    paired_abstraction_label: Optional[str] = Field(default=None, description="Generalized role if both match")
    rationale: str = Field(description="Scientific justification for aligning these two nodes")


class EdgeAlignment(BaseModel):
    base_edge_id: str
    target_edge_id: str
    base_relation: str
    target_relation: str
    relation_preserved: bool
    rationale: str


class AnalogyClassification(BaseModel):
    category: str = Field(description="Literally Similar | True Analogy | False Analogy | Surface Similar | Mere Appearance")
    structural_similarity_score: float = Field(ge=0.0, le=1.0)
    surface_similarity_score: float = Field(ge=0.0, le=1.0)
    order_consistency_score: float = Field(ge=0.0, le=1.0)
    explanation: str


class GraphAlignment(BaseModel):
    alignment_id: str
    base_story_id: str
    target_story_id: str
    node_alignments: List[NodeAlignment] = Field(default_factory=list)
    edge_alignments: List[EdgeAlignment] = Field(default_factory=list)
    unaligned_base_nodes: List[str] = Field(default_factory=list)
    unaligned_target_nodes: List[str] = Field(default_factory=list)
    structural_score: float = Field(default=0.0, ge=0.0, le=1.0)
    temporal_order_preserved: bool = True
    systematicity_score: float = Field(default=0.0, ge=0.0, le=1.0)
    analogy_analysis: Optional[AnalogyClassification] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
