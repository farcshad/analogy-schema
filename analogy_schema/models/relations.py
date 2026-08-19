from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from analogy_schema.models.events import Explicitness


class RelationType(str, Enum):
    CAUSES = "CAUSES"               # A brings about B (mechanistic or direct causal)
    BEFORE = "BEFORE"               # A occurs strictly before B (pure temporal, not necessarily causal)
    ENABLES = "ENABLES"             # A creates conditions making B possible
    BLOCKS = "BLOCKS"               # A prevents or obstructs B from happening
    MOTIVATES = "MOTIVATES"         # A gives agent reason/goal to attempt B
    CONDITIONAL_ON = "CONDITIONAL_ON" # B depends on condition A being met
    RESULTS_IN = "RESULTS_IN"       # Consequential outcome / terminal state of A
    PREVENTS = "PREVENTS"           # Direct counteraction


class EventRelation(BaseModel):
    relation_id: str = Field(description="Unique relation ID, e.g., R1, R2")
    source_id: str = Field(description="Source event ID (atomic, normalized, or macro)")
    target_id: str = Field(description="Target event ID")
    relation_type: RelationType = Field(description="Typed ontological relation")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    explicitness: Explicitness = Field(default=Explicitness.EXPLICIT)
    evidence: Optional[str] = Field(default=None, description="Textual explanation or reasoning for relation")
    provenance_span: Optional[str] = Field(default=None, description="Direct text span if explicitly stated")
