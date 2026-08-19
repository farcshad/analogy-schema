from typing import List, Dict, Set, Any
from pydantic import BaseModel, Field
from analogy_schema.models.story import Story
from analogy_schema.models.graph import RichEventGraph
from analogy_schema.models.events import NormalizedEvent
from analogy_schema.models.backbone import NarrativeAnchors
from analogy_schema.llm.base import BaseLLMProvider
from analogy_schema.prompts.registry import PromptRegistry


class PrunedEventAudit(BaseModel):
    norm_id: str
    reason: str


class BackboneSelectionOutput(BaseModel):
    retained_event_ids: List[str] = Field(description="Normalized event IDs kept in causal backbone")
    pruned_events: List[PrunedEventAudit] = Field(default_factory=list, description="Audit of pruned events with reasons")


def run_stage_f_backbone_selection(
    story: Story,
    graph: RichEventGraph,
    anchors: NarrativeAnchors,
    llm: BaseLLMProvider,
    candidate_ancestors: List[str] = None
) -> Dict[str, Any]:
    """Stage F: Counterfactual backbone selection (Synchronous)."""
    anonymous_story = story.to_llm_input()
    normalized_list = list(graph.normalized_events.values())
    prompt = PromptRegistry.render(
        "backbone_selection",
        story=anonymous_story,
        normalized_events=normalized_list,
        anchors=anchors
    )
    system_prompt = "You are a causal reasoning engine selecting the minimal explanatory causal backbone."
    
    result = llm.generate_structured(
        prompt=prompt,
        response_model=BackboneSelectionOutput,
        system_prompt=system_prompt
    )
    
    retained_ids = set(result.retained_event_ids)
    protected_anchors = set(anchors.focal_outcome_ids + anchors.intervention_event_ids + anchors.contingent_outcome_ids)
    for pa in protected_anchors:
        if pa in graph.normalized_events:
            retained_ids.add(pa)
            
    retained_events = [graph.normalized_events[nid] for nid in retained_ids if nid in graph.normalized_events]
    pruned_reasons = {p.norm_id: p.reason for p in result.pruned_events}
    all_norm_ids = set(graph.normalized_events.keys())
    pruned_ids = list(all_norm_ids - set(retained_ids))
    for pid in pruned_ids:
        if pid not in pruned_reasons:
            pruned_reasons[pid] = "Excluded during counterfactual necessity pruning (not required to explain focal outcome)."
            
    return {
        "retained_events": retained_events,
        "pruned_ids": pruned_ids,
        "pruned_reasons": pruned_reasons
    }


async def run_stage_f_backbone_selection_async(
    story: Story,
    graph: RichEventGraph,
    anchors: NarrativeAnchors,
    llm: BaseLLMProvider,
    candidate_ancestors: List[str] = None
) -> Dict[str, Any]:
    """Stage F: Counterfactual backbone selection (Asynchronous)."""
    anonymous_story = story.to_llm_input()
    normalized_list = list(graph.normalized_events.values())
    prompt = PromptRegistry.render(
        "backbone_selection",
        story=anonymous_story,
        normalized_events=normalized_list,
        anchors=anchors
    )
    system_prompt = "You are a causal reasoning engine selecting the minimal explanatory causal backbone."
    
    result = await llm.agenerate_structured(
        prompt=prompt,
        response_model=BackboneSelectionOutput,
        system_prompt=system_prompt
    )
    
    retained_ids = set(result.retained_event_ids)
    protected_anchors = set(anchors.focal_outcome_ids + anchors.intervention_event_ids + anchors.contingent_outcome_ids)
    for pa in protected_anchors:
        if pa in graph.normalized_events:
            retained_ids.add(pa)
            
    retained_events = [graph.normalized_events[nid] for nid in retained_ids if nid in graph.normalized_events]
    pruned_reasons = {p.norm_id: p.reason for p in result.pruned_events}
    all_norm_ids = set(graph.normalized_events.keys())
    pruned_ids = list(all_norm_ids - set(retained_ids))
    for pid in pruned_ids:
        if pid not in pruned_reasons:
            pruned_reasons[pid] = "Excluded during counterfactual necessity pruning (not required to explain focal outcome)."
            
    return {
        "retained_events": retained_events,
        "pruned_ids": pruned_ids,
        "pruned_reasons": pruned_reasons
    }
