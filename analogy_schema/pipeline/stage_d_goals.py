from typing import List, Optional
from pydantic import BaseModel, Field
from analogy_schema.models.story import Story
from analogy_schema.models.events import NormalizedEvent
from analogy_schema.models.backbone import NarrativeAnchors
from analogy_schema.llm.base import BaseLLMProvider
from analogy_schema.prompts.registry import PromptRegistry


class GoalOutcomeOutput(BaseModel):
    central_problem: Optional[str] = None
    central_goal: Optional[str] = None
    intervention: Optional[str] = None
    terminal_outcomes: List[str] = Field(default_factory=list)
    anchor_event_ids: List[str] = Field(default_factory=list)


def run_stage_d_goal_outcome_identification(
    story: Story,
    normalized_events: List[NormalizedEvent],
    llm: BaseLLMProvider
) -> NarrativeAnchors:
    """
    Stage D: Identify narrative problem, goal, intervention, and terminal outcomes.
    """
    prompt = PromptRegistry.render(
        "goal_outcome",
        story=story,
        normalized_events=normalized_events
    )
    system_prompt = "You are a narrative goal and outcome analyzer."
    
    result = llm.generate_structured(
        prompt=prompt,
        response_model=GoalOutcomeOutput,
        system_prompt=system_prompt
    )
    
    return NarrativeAnchors(
        central_problem=result.central_problem,
        central_goal=result.central_goal,
        intervention=result.intervention,
        terminal_outcomes=result.terminal_outcomes,
        anchor_event_ids=result.anchor_event_ids
    )
