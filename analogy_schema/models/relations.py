from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from analogy_schema.models.events import Explicitness


class RelationFamily(str, Enum):
    CAUSAL = "CAUSAL"                       # Direct mechanistic/behavioral cause-and-effect
    CONSEQUENCE = "CONSEQUENCE"             # Consequential outcome produced by requirement success/failure
    MOTIVATION = "MOTIVATION"               # Intentional stimulus / goal requirement
    CONSTRAINT = "CONSTRAINT"               # Obstruction, enablement, prevention
    TEMPORAL = "TEMPORAL"                   # Chronological sequencing


class RelationType(str, Enum):
    # Causal Mechanism
    CAUSES = "CAUSES"                   # Source brings about or causes Target (mechanistic/behavioral)
    
    # Consequential Outcome
    RESULTS_IN = "RESULTS_IN"           # Source directly produces consequential outcome Target (e.g. failure -> reward withheld)
    
    # Constraint & Precondition
    ENABLES = "ENABLES"                 # Source creates necessary preconditions making Target possible
    BLOCKS = "BLOCKS"                   # Source prevents, obstructs, or renders impossible Target
    PREVENTS = "PREVENTS"               # Source directly counteracts or stops Target
    
    # Motivation & Requirement
    MOTIVATES = "MOTIVATES"             # Source provides explicit reason/goal for agent to attempt Target (requires textual evidence of intentionality)
    REQUIRES = "REQUIRES"               # Source requires condition Target to be fulfilled/satisfied
    
    # Pure Temporal (Non-Causal)
    BEFORE = "BEFORE"                   # Source occurs strictly before Target in narrative time (non-causal temporal succession)

    @property
    def is_causal_or_explanatory(self) -> bool:
        """True if the relation provides causal or explanatory mechanism."""
        return self in (
            RelationType.CAUSES,
            RelationType.RESULTS_IN,
            RelationType.ENABLES,
            RelationType.BLOCKS,
            RelationType.PREVENTS,
            RelationType.MOTIVATES,
            RelationType.REQUIRES,
        )

    @property
    def is_temporal_only(self) -> bool:
        """True if the relation indicates only chronological order."""
        return self == RelationType.BEFORE


class EventRelation(BaseModel):
    relation_id: str = Field(description="Unique relation ID, e.g., R1, R2")
    source_id: str = Field(description="Source event ID")
    target_id: str = Field(description="Target event ID")
    relation_type: RelationType = Field(description="Typed ontological relation")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    explicitness: Explicitness = Field(default=Explicitness.EXPLICIT)
    evidence: Optional[str] = Field(default=None, description="Textual narrative evidence (not generic world knowledge)")
    provenance_span: Optional[str] = Field(default=None, description="Direct text span if explicitly stated")
