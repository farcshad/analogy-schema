from typing import List, Dict, Optional, Set
from pydantic import BaseModel, Field
from analogy_schema.models.events import NormalizedEvent, AtomicEvent
from analogy_schema.models.relations import EventRelation


class RichEventGraph(BaseModel):
    graph_id: str
    story_id: str
    atomic_events: Dict[str, AtomicEvent] = Field(default_factory=dict)
    normalized_events: Dict[str, NormalizedEvent] = Field(default_factory=dict)
    relations: List[EventRelation] = Field(default_factory=list)
    metadata: Dict = Field(default_factory=dict)

    def get_outgoing_relations(self, node_id: str) -> List[EventRelation]:
        return [r for r in self.relations if r.source_id == node_id]

    def get_incoming_relations(self, node_id: str) -> List[EventRelation]:
        return [r for r in self.relations if r.target_id == node_id]

    def get_node_ids(self) -> Set[str]:
        if self.normalized_events:
            return set(self.normalized_events.keys())
        return set(self.atomic_events.keys())
