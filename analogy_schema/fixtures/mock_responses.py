from analogy_schema.models.events import (
    AtomicEvent,
    NormalizedEvent,
    EventType,
    Polarity,
    Explicitness,
    InterventionPhase,
    TemporalExtent,
    TemporalGrounding,
    BackboneRole,
)
from analogy_schema.models.relations import EventRelation, RelationType
from analogy_schema.pipeline.stage_a_atomic import AtomicExtractionOutput
from analogy_schema.pipeline.stage_b_normalize import NormalizationOutput
from analogy_schema.pipeline.stage_c_relations import RelationExtractionOutput
from analogy_schema.pipeline.stage_d_goals import GoalOutcomeOutput
from analogy_schema.pipeline.stage_f_backbone import BackboneSelectionOutput, PrunedEventAudit
from analogy_schema.pipeline.stage_g_macro import (
    MacroGroupingOutput,
    GeneratedMacroNode,
)
from analogy_schema.models.backbone import IncentiveContract


def get_william_mock_stage_a() -> AtomicExtractionOutput:
    return AtomicExtractionOutput(
        events=[
            AtomicEvent(
                event_id="E1",
                text_span="William was a patient in a psychiatric hospital who was confined indoors almost all the time.",
                sentence_id=1,
                predicate="is confined indoors",
                participants=["William"],
                event_type=EventType.STATE,
                explicitness=Explicitness.EXPLICIT,
                temporal_rank=1,
            ),
            AtomicEvent(
                event_id="E2",
                text_span="He could never pass the monthly room inspections",
                sentence_id=2,
                predicate="habitually fails inspections",
                participants=["William", "room inspection"],
                event_type=EventType.STATE,
                explicitness=Explicitness.EXPLICIT,
                temporal_rank=2,
            ),
            AtomicEvent(
                event_id="E3",
                text_span="so he hated them",
                sentence_id=2,
                predicate="hates room inspections",
                participants=["William", "room inspection"],
                event_type=EventType.EMOTION_REACTION,
                explicitness=Explicitness.EXPLICIT,
                temporal_rank=2,
            ),
            AtomicEvent(
                event_id="E4",
                text_span="He spent most of his time daydreaming about food.",
                sentence_id=3,
                predicate="daydreams about food",
                participants=["William", "food"],
                event_type=EventType.ACTION,
                explicitness=Explicitness.EXPLICIT,
                temporal_rank=3,
            ),
            AtomicEvent(
                event_id="E5",
                text_span="William's room was still a mess",
                sentence_id=4,
                predicate="room is in messy state",
                participants=["William", "room"],
                event_type=EventType.STATE,
                explicitness=Explicitness.EXPLICIT,
                temporal_rank=4,
            ),
            AtomicEvent(
                event_id="E6",
                text_span="since he had done nothing but daydream.",
                sentence_id=4,
                predicate="neglects cleaning due to daydreaming",
                participants=["William"],
                event_type=EventType.ACTION,
                explicitness=Explicitness.EXPLICIT,
                temporal_rank=4,
            ),
            AtomicEvent(
                event_id="E7",
                text_span="the nurse promised him some gingerbread from the cookie shop if he scrubbed his room",
                sentence_id=5,
                predicate="nurse offers gingerbread incentive for cleaning",
                participants=["nurse", "William", "gingerbread"],
                event_type=EventType.EVENT,
                explicitness=Explicitness.EXPLICIT,
                temporal_rank=5,
            ),
            AtomicEvent(
                event_id="E8",
                text_span="William was overjoyed.",
                sentence_id=6,
                predicate="becomes happy about incentive",
                participants=["William"],
                event_type=EventType.EMOTION_REACTION,
                explicitness=Explicitness.EXPLICIT,
                temporal_rank=6,
            ),
            AtomicEvent(
                event_id="E9",
                text_span="there was no longer enough time for him to put it in order.",
                sentence_id=7,
                predicate="insufficient time remaining to finish",
                participants=["William", "room"],
                event_type=EventType.CONSTRAINT,
                explicitness=Explicitness.EXPLICIT,
                temporal_rank=7,
            ),
            AtomicEvent(
                event_id="E10",
                text_span="he did not pass the inspection",
                sentence_id=8,
                predicate="fails room inspection",
                participants=["William", "inspection"],
                event_type=EventType.OUTCOME,
                polarity=Polarity.NEGATIVE,
                explicitness=Explicitness.EXPLICIT,
                temporal_rank=8,
            ),
            AtomicEvent(
                event_id="E11",
                text_span="did not get any gingerbread.",
                sentence_id=8,
                predicate="does not receive gingerbread",
                participants=["William", "gingerbread"],
                event_type=EventType.OUTCOME,
                polarity=Polarity.NEGATIVE,
                explicitness=Explicitness.EXPLICIT,
                temporal_rank=8,
            ),
            AtomicEvent(
                event_id="E12",
                text_span="William sulked all day and slammed his door so hard the plaster cracked",
                sentence_id=9,
                predicate="sulks and slams door",
                participants=["William", "door"],
                event_type=EventType.EMOTION_REACTION,
                explicitness=Explicitness.EXPLICIT,
                temporal_rank=9,
            ),
        ]
    )


def get_william_mock_stage_b() -> NormalizationOutput:
    return NormalizationOutput(
        normalized_events=[
            NormalizedEvent(
                norm_id="NE1",
                predicate_name="NEGLECT_TASK",
                arguments={"actor": "William", "task": "clean_room", "activity": "daydreaming"},
                atomic_event_ids=["E4", "E6"],
                summary_label="task neglect",
                temporal_grounding=TemporalGrounding(
                    mention_phase=InterventionPhase.PRE_INTERVENTION,
                    onset_phase=InterventionPhase.PRE_INTERVENTION,
                    holds_at_intervention=True,
                    temporal_extent=TemporalExtent.INTERVAL
                ),
            ),
            NormalizedEvent(
                norm_id="NE2",
                predicate_name="DEFICIT_STATE",
                arguments={"actor": "William", "state": "room_is_mess"},
                atomic_event_ids=["E5"],
                summary_label="accumulated deficit",
                temporal_grounding=TemporalGrounding(
                    mention_phase=InterventionPhase.PRE_INTERVENTION,
                    onset_phase=InterventionPhase.PRE_INTERVENTION,
                    holds_at_intervention=True,
                    temporal_extent=TemporalExtent.PERSISTENT_STATE
                ),
            ),
            NormalizedEvent(
                norm_id="NE3",
                predicate_name="INTRODUCE_INCENTIVE",
                arguments={"provider": "nurse", "recipient": "William", "reward": "gingerbread", "condition": "clean_room"},
                atomic_event_ids=["E7"],
                summary_label="conditional incentive",
                temporal_grounding=TemporalGrounding(
                    mention_phase=InterventionPhase.AT_INTERVENTION,
                    onset_phase=InterventionPhase.AT_INTERVENTION,
                    holds_at_intervention=True,
                    temporal_extent=TemporalExtent.POINT
                ),
            ),
            NormalizedEvent(
                norm_id="NE4",
                predicate_name="INSUFFICIENT_TIME_BUFFER",
                arguments={"actor": "William", "target": "complete_cleaning"},
                atomic_event_ids=["E9"],
                summary_label="insufficient remaining time",
                temporal_grounding=TemporalGrounding(
                    mention_phase=InterventionPhase.POST_INTERVENTION,
                    onset_phase=InterventionPhase.PRE_INTERVENTION,
                    holds_at_intervention=True,
                    temporal_extent=TemporalExtent.PERSISTENT_STATE
                ),
            ),
            NormalizedEvent(
                norm_id="NE5",
                predicate_name="FAIL_REQUIREMENT",
                arguments={"actor": "William", "requirement": "room_inspection"},
                atomic_event_ids=["E2", "E10"],
                summary_label="requirement failure",
                temporal_grounding=TemporalGrounding(
                    mention_phase=InterventionPhase.POST_INTERVENTION,
                    onset_phase=InterventionPhase.POST_INTERVENTION,
                    holds_at_intervention=False,
                    temporal_extent=TemporalExtent.POINT
                ),
            ),
            NormalizedEvent(
                norm_id="NE6",
                predicate_name="WITHHOLD_REWARD",
                arguments={"recipient": "William", "reward": "gingerbread"},
                atomic_event_ids=["E11"],
                summary_label="reward withheld",
                temporal_grounding=TemporalGrounding(
                    mention_phase=InterventionPhase.POST_INTERVENTION,
                    onset_phase=InterventionPhase.POST_INTERVENTION,
                    holds_at_intervention=False,
                    temporal_extent=TemporalExtent.POINT
                ),
            ),
            NormalizedEvent(
                norm_id="NE7",
                predicate_name="EMOTIONAL_OUTBURST",
                arguments={"actor": "William", "actions": ["sulk", "slam_door", "crack_plaster"]},
                atomic_event_ids=["E3", "E8", "E12"],
                summary_label="emotional outburst",
                temporal_grounding=TemporalGrounding(
                    mention_phase=InterventionPhase.POST_INTERVENTION,
                    onset_phase=InterventionPhase.POST_INTERVENTION,
                    holds_at_intervention=False,
                    temporal_extent=TemporalExtent.POINT
                ),
            ),
        ]
    )


def get_william_mock_stage_c() -> RelationExtractionOutput:
    return RelationExtractionOutput(
        relations=[
            EventRelation(
                relation_id="R1",
                source_id="NE1",
                target_id="NE2",
                relation_type=RelationType.CAUSES,
                evidence="Task neglect directly caused the messy room deficit state.",
                explicitness=Explicitness.EXPLICIT,
            ),
            EventRelation(
                relation_id="R2",
                source_id="NE2",
                target_id="NE4",
                relation_type=RelationType.CAUSES,
                evidence="The accumulated deficit backlog created the insurmountable shortage of remaining time.",
                explicitness=Explicitness.STRONGLY_INFERRED,
            ),
            EventRelation(
                relation_id="R3",
                source_id="NE2",
                target_id="NE3",
                relation_type=RelationType.BEFORE,
                evidence="The messy deficit state already existed before the incentive was introduced.",
                explicitness=Explicitness.EXPLICIT,
            ),
            EventRelation(
                relation_id="R4",
                source_id="NE4",
                target_id="NE5",
                relation_type=RelationType.RESULTS_IN,
                evidence="Insufficient time to finish resulted directly in failing the inspection standard.",
                explicitness=Explicitness.EXPLICIT,
            ),
            EventRelation(
                relation_id="R5",
                source_id="NE5",
                target_id="NE6",
                relation_type=RelationType.RESULTS_IN,
                evidence="Failing the inspection requirement directly resulted in the promised reward being withheld.",
                explicitness=Explicitness.EXPLICIT,
            ),
            EventRelation(
                relation_id="R6",
                source_id="NE6",
                target_id="NE7",
                relation_type=RelationType.RESULTS_IN,
                evidence="Withholding the reward triggered the downstream emotional outburst.",
                explicitness=Explicitness.EXPLICIT,
            ),
        ]
    )


def get_william_mock_stage_d() -> GoalOutcomeOutput:
    return GoalOutcomeOutput(
        central_problem="Accumulated task backlog caused by inaction makes recovery impossible",
        central_goal="Pass inspection standard and earn incentive reward",
        intervention_event_ids=["NE3"],
        focal_outcome_ids=["NE5"],
        contingent_outcome_ids=["NE6"],
        downstream_reaction_ids=["NE7"],
        contracts=[
            IncentiveContract(
                intervention_event_id="NE3",
                promised_reward="gingerbread",
                contingent_requirement="pass room inspection",
                condition_polarity=Polarity.POSITIVE
            )
        ],
        explanation="NE5 is the primary focal failure; NE6 is the direct contingent consequence; NE7 is a downstream reaction."
    )


def get_william_mock_stage_f() -> BackboneSelectionOutput:
    return BackboneSelectionOutput(
        retained_event_ids=["NE1", "NE2", "NE3", "NE4", "NE5", "NE6"],
        pruned_events=[
            PrunedEventAudit(
                norm_id="NE7",
                reason="Downstream emotional reaction and door slamming do not causally explain why the inspection failed."
            )
        ]
    )


def get_william_mock_stage_gh() -> MacroGroupingOutput:
    return MacroGroupingOutput(
        macro_nodes=[
            GeneratedMacroNode(
                macro_id="M1",
                label="task neglect",
                source_normalized_ids=["NE1"],
                functional_role=BackboneRole.CAUSAL_ANTECEDENT,
                temporal_order=1,
                abstraction_level_0="William daydreams about food instead of cleaning",
                abstraction_level_1="William neglects cleaning task",
                abstraction_level_2="task neglect",
                abstraction_level_3="inaction",
            ),
            GeneratedMacroNode(
                macro_id="M2",
                label="accumulated deficit",
                source_normalized_ids=["NE2"],
                functional_role=BackboneRole.PROBLEM_STATE,
                temporal_order=2,
                abstraction_level_0="The room remains messy a few days before inspection",
                abstraction_level_1="Room is in uncleaned backlog state",
                abstraction_level_2="accumulated deficit",
                abstraction_level_3="deficit condition",
            ),
            GeneratedMacroNode(
                macro_id="M3",
                label="conditional incentive",
                source_normalized_ids=["NE3"],
                functional_role=BackboneRole.INTERVENTION,
                temporal_order=3,
                abstraction_level_0="Nurse promises gingerbread if William cleans the room",
                abstraction_level_1="Authority offers food reward for completing cleaning",
                abstraction_level_2="conditional incentive",
                abstraction_level_3="external motivation intervention",
            ),
            GeneratedMacroNode(
                macro_id="M4",
                label="insufficient remaining time",
                source_normalized_ids=["NE4"],
                functional_role=BackboneRole.CONSTRAINT,
                temporal_order=4,
                abstraction_level_0="There was no longer enough time for him to put it in order",
                abstraction_level_1="Insufficient remaining time to clean room",
                abstraction_level_2="insufficient remaining resources",
                abstraction_level_3="irreversible constraint",
            ),
            GeneratedMacroNode(
                macro_id="M5",
                label="requirement failure",
                source_normalized_ids=["NE5"],
                functional_role=BackboneRole.FOCAL_OUTCOME,
                temporal_order=5,
                abstraction_level_0="William does not pass the monthly room inspection",
                abstraction_level_1="Fails room inspection standard",
                abstraction_level_2="requirement failure",
                abstraction_level_3="task failure",
            ),
            GeneratedMacroNode(
                macro_id="M6",
                label="reward withheld",
                source_normalized_ids=["NE6"],
                functional_role=BackboneRole.CONTINGENT_OUTCOME,
                temporal_order=6,
                abstraction_level_0="William does not get any gingerbread",
                abstraction_level_1="Gingerbread treat is withheld",
                abstraction_level_2="reward withheld",
                abstraction_level_3="forfeited incentive",
            ),
        ]
    )
