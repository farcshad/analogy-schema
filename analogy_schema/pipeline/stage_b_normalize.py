from typing import List
from pydantic import BaseModel, Field
from analogy_schema.models.story import Story
from analogy_schema.models.events import AtomicEvent, NormalizedEvent
from analogy_schema.llm.base import BaseLLMProvider
from analogy_schema.prompts.registry import PromptRegistry


class NormalizationOutput(BaseModel):
    normalized_events: List[NormalizedEvent] = Field(default_factory=list)


def run_stage_b_semantic_normalization(
    story: Story,
    atomic_events: List[AtomicEvent],
    llm: BaseLLMProvider
) -> List[NormalizedEvent]:
    """Stage B: Semantic normalization of atomic events (Synchronous)."""
    prompt = PromptRegistry.render(
        "semantic_normalization",
        story=story,
        atomic_events=atomic_events
    )
    system_prompt = "You are a semantic predicate normalizer maintaining strict provenance to atomic event IDs."
    
    result = llm.generate_structured(
        prompt=prompt,
        response_model=NormalizationOutput,
        system_prompt=system_prompt
    )
    
    for i, ne in enumerate(result.normalized_events, start=1):
        if not ne.norm_id:
            ne.norm_id = f"NE{i}"
            
    return result.normalized_events


async def run_stage_b_semantic_normalization_async(
    story: Story,
    atomic_events: List[AtomicEvent],
    llm: BaseLLMProvider
) -> List[NormalizedEvent]:
    """Stage B: Semantic normalization of atomic events (Asynchronous)."""
    prompt = PromptRegistry.render(
        "semantic_normalization",
        story=story,
        atomic_events=atomic_events
    )
    system_prompt = "You are a semantic predicate normalizer maintaining strict provenance to atomic event IDs."
    
    result = await llm.agenerate_structured(
        prompt=prompt,
        response_model=NormalizationOutput,
        system_prompt=system_prompt
    )
    
    for i, ne in enumerate(result.normalized_events, start=1):
        if not ne.norm_id:
            ne.norm_id = f"NE{i}"
            
    return result.normalized_events
