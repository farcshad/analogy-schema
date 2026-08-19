from typing import List, Dict
from pydantic import BaseModel, Field
from analogy_schema.models.story import Story
from analogy_schema.models.events import AtomicEvent, NormalizedEvent
from analogy_schema.models.relations import EventRelation
from analogy_schema.models.graph import RichEventGraph
from analogy_schema.llm.base import BaseLLMProvider
from analogy_schema.prompts.registry import PromptRegistry


class RelationExtractionOutput(BaseModel):
    relations: List[EventRelation] = Field(default_factory=list)


def run_stage_c_relation_extraction(
    story: Story,
    atomic_events: List[AtomicEvent],
    normalized_events: List[NormalizedEvent],
    llm: BaseLLMProvider
) -> RichEventGraph:
    """Stage C: Evidence-grounded typed relation extraction (Synchronous)."""
    prompt = PromptRegistry.render(
        "relation_extraction",
        story=story,
        normalized_events=normalized_events
    )
    system_prompt = "You are a causal narrative relation analyst distinguishing temporal order from true causality."
    
    result = llm.generate_structured(
        prompt=prompt,
        response_model=RelationExtractionOutput,
        system_prompt=system_prompt
    )
    
    for i, rel in enumerate(result.relations, start=1):
        if not rel.relation_id:
            rel.relation_id = f"R{i}"
            
    atomic_dict = {e.event_id: e for e in atomic_events}
    norm_dict = {ne.norm_id: ne for ne in normalized_events}
    
    return RichEventGraph(
        graph_id=f"rich_graph_{story.story_id}",
        story_id=story.story_id,
        atomic_events=atomic_dict,
        normalized_events=norm_dict,
        relations=result.relations,
        metadata={"story_length_chars": len(story.text)}
    )


async def run_stage_c_relation_extraction_async(
    story: Story,
    atomic_events: List[AtomicEvent],
    normalized_events: List[NormalizedEvent],
    llm: BaseLLMProvider
) -> RichEventGraph:
    """Stage C: Evidence-grounded typed relation extraction (Asynchronous)."""
    prompt = PromptRegistry.render(
        "relation_extraction",
        story=story,
        normalized_events=normalized_events
    )
    system_prompt = "You are a causal narrative relation analyst distinguishing temporal order from true causality."
    
    result = await llm.agenerate_structured(
        prompt=prompt,
        response_model=RelationExtractionOutput,
        system_prompt=system_prompt
    )
    
    for i, rel in enumerate(result.relations, start=1):
        if not rel.relation_id:
            rel.relation_id = f"R{i}"
            
    atomic_dict = {e.event_id: e for e in atomic_events}
    norm_dict = {ne.norm_id: ne for ne in normalized_events}
    
    return RichEventGraph(
        graph_id=f"rich_graph_{story.story_id}",
        story_id=story.story_id,
        atomic_events=atomic_dict,
        normalized_events=norm_dict,
        relations=result.relations,
        metadata={"story_length_chars": len(story.text)}
    )
