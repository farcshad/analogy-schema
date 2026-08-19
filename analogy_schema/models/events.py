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


class InterventionPhase(str, Enum):
    PRE_INTERVENTION = "PRE_INTERVENTION"        # Began and/or occurred strictly before intervention
    AT_INTERVENTION = "AT_INTERVENTION"          # Coincident with / introduced by the intervention
    POST_INTERVENTION = "POST_INTERVENTION"      # Initiated after intervention introduction
    SPANS_INTERVENTION = "SPANS_INTERVENTION"    # Began before intervention and persisted through/after it
    UNANCHORED = "UNANCHORED"                    # Contextual background or narrative without intervention


class TemporalExtent(str, Enum):
    POINT = "POINT"                              # Instantaneous event or discrete action
    PERSISTENT_STATE = "PERSISTENT_STATE"        # State that persists across time until changed
    INTERVAL = "INTERVAL"                        # Extended activity over a duration


class TemporalGrounding(BaseModel):
    mention_phase: InterventionPhase = Field(
        default=InterventionPhase.UNANCHORED,
        description="Textual position in narrative relative to the intervention mention sentence"
    )
    onset_phase: InterventionPhase = Field(
        default=InterventionPhase.UNANCHORED,
        description="True story-world time when this event or state began"
    )
    holds_at_intervention: bool = Field(
        default=False,
        description="True if this state exists / holds active when the intervention is introduced"
    )
    temporal_extent: TemporalExtent = Field(
        default=TemporalExtent.POINT,
        description="Point event vs persistent state vs extended interval"
    )


class BackboneRole(str, Enum):
    BACKGROUND = "BACKGROUND"                    # Contextual setting, static traits, chronic past history
    CAUSAL_ANTECEDENT = "CAUSAL_ANTECEDENT"      # Action or event triggering the problem/deficit
    PROBLEM_STATE = "PROBLEM_STATE"              # Ongoing deficit, backlog, or challenge
    GOAL = "GOAL"                                # Target objective or requirement
    INTERVENTION = "INTERVENTION"                # External nudge, incentive, aid, or plan introduced
    ACTION_RESPONSE = "ACTION_RESPONSE"          # Agent's subsequent effort or non-effort
    CONSTRAINT = "CONSTRAINT"                    # Insuperable barrier, deadline, resource limit
    FOCAL_OUTCOME = "FOCAL_OUTCOME"              # Primary success or failure of requirement/goal
    CONTINGENT_OUTCOME = "CONTINGENT_OUTCOME"    # Consequence conditional on focal outcome (e.g. reward given/withheld)
    DOWNSTREAM_REACTION = "DOWNSTREAM_REACTION"  # Emotional outburst, secondary reaction, incidental damage


class AtomicEvent(BaseModel):
    event_id: str = Field(description="Unique atomic event ID, e.g., E1, E2")
    text_span: str = Field(description="Exact or near-exact story text span supporting the event")
    sentence_id: Optional[int] = Field(default=None, description="Sentence index from the story")
    predicate: str = Field(description="Core predicate or state")
    participants: List[str] = Field(default_factory=list, description="Entities involved")
    event_type: EventType = Field(default=EventType.EVENT, description="Syntactic/semantic category")
    polarity: Polarity = Field(default=Polarity.POSITIVE, description="Positive or negated event")
    explicitness: Explicitness = Field(default=Explicitness.EXPLICIT, description="Degree of textual grounding")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score [0.0, 1.0]")
    temporal_rank: Optional[int] = Field(default=None, description="Order of occurrence in narrative time")


class NormalizedEvent(BaseModel):
    norm_id: str = Field(description="Unique normalized event ID, e.g., NE1, NE2")
    predicate_name: str = Field(description="Normalized predicate, e.g., NEGLECT_TASK, DEFICIT_STATE")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Semantic arguments")
    atomic_event_ids: List[str] = Field(default_factory=list, description="Provenance: source AtomicEvent IDs")
    summary_label: str = Field(description="Human readable summary label (atomic event/state description without embedded relations)")
    polarity: Polarity = Field(default=Polarity.POSITIVE)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    temporal_grounding: TemporalGrounding = Field(
        default_factory=TemporalGrounding,
        description="Disambiguated mention time, onset time, and state persistence"
    )

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
