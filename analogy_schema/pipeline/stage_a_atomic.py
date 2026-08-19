from typing import List
from pydantic import BaseModel, Field
from analogy_schema.models.story import Story
from analogy_schema.models.events import AtomicEvent
from analogy_schema.llm.base import BaseLLMProvider
from analogy_schema.prompts.registry import PromptRegistry


class AtomicExtractionOutput(BaseModel):
    events: List[AtomicEvent] = Field(default_factory=list)


def run_stage_a_atomic_extraction(story: Story, llm: BaseLLMProvider) -> List[AtomicEvent]:
    """
    Stage A: High-recall atomic event/state extraction with textual span provenance.
    """
    prompt = PromptRegistry.render("atomic_extraction", story=story)
    system_prompt = "You are a scientific NLP extractor specializing in high-recall causal event extraction."
    
    result = llm.generate_structured(
        prompt=prompt,
        response_model=AtomicExtractionOutput,
        system_prompt=system_prompt
    )
    
    # Fill in fallback event IDs if needed
    for i, ev in enumerate(result.events, start=1):
        if not ev.event_id:
            ev.event_id = f"E{i}"
            
    return result.events
