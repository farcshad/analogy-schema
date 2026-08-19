from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Explicitness(str, Enum):
    EXPLICIT = "explicit"
    STRONGLY_INFERRED = "strongly_inferred"
    SPECULATIVE = "speculative"


class Polarity(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


class EventType(str, Enum):
    ACTION = "action"
    STATE = "state"
    EVENT = "event"
    GOAL = "goal"
    CONSTRAINT = "constraint"
    OUTCOME = "outcome"
    EMOTION_REACTION = "emotion_reaction"


class AtomicEvent(BaseModel):
    event_id: str = Field(description="Unique atomic event ID, e.g., E1, E2")
    text_span: str = Field(description="Exact or near-exact story text span supporting the event")
    sentence_id: Optional[int] = Field(default=None, description="Sentence index from the story")
    predicate: str = Field(description="Core predicate or state, e.g., 'is confined', 'daydreams'")
    participants: List[str] = Field(default_factory=list, description="Entities involved, e.g., ['William', 'nurse']")
    event_type: EventType = Field(default=EventType.EVENT, description="Syntactic/semantic category")
    polarity: Polarity = Field(default=Polarity.POSITIVE, description="Positive or negated event")
    explicitness: Explicitness = Field(default=Explicitness.EXPLICIT, description="Degree of textual grounding")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score [0.0, 1.0]")
    temporal_rank: Optional[int] = Field(default=None, description="Order of occurrence in narrative time")


class NormalizedEvent(BaseModel):
    norm_id: str = Field(description="Unique normalized event ID, e.g., NE1, NE2")
    predicate_name: str = Field(description="Normalized predicate, e.g., NEGLECT_TASK, INSUFFICIENT_TIME")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Semantic arguments, e.g., {'actor': 'William', 'task': 'clean_room'}")
    atomic_event_ids: List[str] = Field(default_factory=list, description="Provenance: source AtomicEvent IDs")
    summary_label: str = Field(description="Human readable summary label, e.g., 'William neglects cleaning room'")
    polarity: Polarity = Field(default=Polarity.POSITIVE)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
