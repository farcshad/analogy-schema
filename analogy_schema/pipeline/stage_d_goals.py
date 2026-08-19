from typing import List, Optional
from pydantic import BaseModel, Field
from analogy_schema.models.story import Story
from analogy_schema.models.events import NormalizedEvent
from analogy_schema.models.backbone import NarrativeAnchors, IncentiveContract
from analogy_schema.llm.base import BaseLLMProvider
from analogy_schema.prompts.registry import PromptRegistry


class GoalOutcomeOutput(BaseModel):
    central_problem: Optional[str] = None
    central_goal: Optional[str] = None
    intervention_event_ids: List[str] = Field(default_factory=list)
    focal_outcome_ids: List[str] = Field(default_factory=list)
    contingent_outcome_ids: List[str] = Field(default_factory=list)
    downstream_reaction_ids: List[str] = Field(default_factory=list)
    contracts: List[IncentiveContract] = Field(default_factory=list)
    explanation: Optional[str] = None


def run_stage_d_goal_outcome_identification(
    story: Story,
    normalized_events: List[NormalizedEvent],
    llm: BaseLLMProvider
) -> NarrativeAnchors:
    """Stage D: Narrative anchor and contract identification (Synchronous)."""
    anonymous_story = story.to_llm_input()
    prompt = PromptRegistry.render(
        "goal_outcome",
        story=anonymous_story,
        normalized_events=normalized_events
    )
    system_prompt = "You are a narrative anchor analyzer distinguishing focal outcomes from downstream reactions."
    
    result = llm.generate_structured(
        prompt=prompt,
        response_model=GoalOutcomeOutput,
        system_prompt=system_prompt
    )
    
    return NarrativeAnchors(
        central_problem=result.central_problem,
        central_goal=result.central_goal,
        intervention_event_ids=result.intervention_event_ids,
        focal_outcome_ids=result.focal_outcome_ids,
        contingent_outcome_ids=result.contingent_outcome_ids,
        downstream_reaction_ids=result.downstream_reaction_ids,
        contracts=result.contracts,
        explanation=result.explanation
    )


async def run_stage_d_goal_outcome_identification_async(
    story: Story,
    normalized_events: List[NormalizedEvent],
    llm: BaseLLMProvider
) -> NarrativeAnchors:
    """Stage D: Narrative anchor and contract identification (Asynchronous)."""
    anonymous_story = story.to_llm_input()
    prompt = PromptRegistry.render(
        "goal_outcome",
        story=anonymous_story,
        normalized_events=normalized_events
    )
    system_prompt = "You are a narrative anchor analyzer distinguishing focal outcomes from downstream reactions."
    
    result = await llm.agenerate_structured(
        prompt=prompt,
        response_model=GoalOutcomeOutput,
        system_prompt=system_prompt
    )
    
    return NarrativeAnchors(
        central_problem=result.central_problem,
        central_goal=result.central_goal,
        intervention_event_ids=result.intervention_event_ids,
        focal_outcome_ids=result.focal_outcome_ids,
        contingent_outcome_ids=result.contingent_outcome_ids,
        downstream_reaction_ids=result.downstream_reaction_ids,
        contracts=result.contracts,
        explanation=result.explanation
    )
