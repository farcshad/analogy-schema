from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from analogy_schema.models.events import Explicitness


class RelationType(str, Enum):
    CAUSES = "CAUSES"                   # Source brings about or causes Target (mechanistic/causal)
    BEFORE = "BEFORE"                   # Source occurs strictly before Target in narrative time (pure temporal)
    ENABLES = "ENABLES"                 # Source creates necessary preconditions making Target possible
    BLOCKS = "BLOCKS"                   # Source prevents, obstructs, or renders impossible Target
    MOTIVATES = "MOTIVATES"             # Source gives agent reason/goal/incentive to attempt Target
    REQUIRES = "REQUIRES"               # Source requires condition Target to be fulfilled/satisfied
    CONDITIONAL_ON = "CONDITIONAL_ON"   # Source outcome depends on Target condition being met
    RESULTS_IN = "RESULTS_IN"           # Source directly produces consequential outcome Target
    PREVENTS = "PREVENTS"               # Source directly counteracts or stops Target


class EventRelation(BaseModel):
    relation_id: str = Field(description="Unique relation ID, e.g., R1, R2")
    source_id: str = Field(description="Source event ID (norm_id or event_id)")
    target_id: str = Field(description="Target event ID")
    relation_type: RelationType = Field(description="Typed ontological relation")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    explicitness: Explicitness = Field(default=Explicitness.EXPLICIT)
    evidence: Optional[str] = Field(default=None, description="Textual explanation or reasoning for relation")
    provenance_span: Optional[str] = Field(default=None, description="Direct text span if explicitly stated")
