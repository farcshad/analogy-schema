from analogy_schema.models.events import (
    AtomicEvent,
    NormalizedEvent,
    EventType,
    Polarity,
    Explicitness,
    InterventionPhase,
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
                arguments={"actor": "William", "task": "clean_room", "reason": "daydreaming"},
                atomic_event_ids=["E4", "E6"],
                summary_label="William neglects cleaning his room due to daydreaming",
                temporal_phase=InterventionPhase.PRE_INTERVENTION,
                is_persistent_state=False,
            ),
            NormalizedEvent(
                norm_id="NE2",
                predicate_name="DEFICIT_STATE",
                arguments={"actor": "William", "state": "room_is_mess"},
                atomic_event_ids=["E5"],
                summary_label="Room remains in an accumulated deficit backlog state",
                temporal_phase=InterventionPhase.SPANS_INTERVENTION,
                is_persistent_state=True,
            ),
            NormalizedEvent(
                norm_id="NE3",
                predicate_name="INTRODUCE_INCENTIVE",
                arguments={"provider": "nurse", "recipient": "William", "reward": "gingerbread", "condition": "clean_room"},
                atomic_event_ids=["E7"],
                summary_label="Nurse introduces conditional incentive to motivate cleaning",
                temporal_phase=InterventionPhase.AT_INTERVENTION,
                is_persistent_state=False,
            ),
            NormalizedEvent(
                norm_id="NE4",
                predicate_name="INSUFFICIENT_TIME_BUFFER",
                arguments={"actor": "William", "target": "complete_cleaning"},
                atomic_event_ids=["E9"],
                summary_label="Insufficient time remaining to overcome backlog",
                temporal_phase=InterventionPhase.SPANS_INTERVENTION,
                is_persistent_state=True,
            ),
            NormalizedEvent(
                norm_id="NE5",
                predicate_name="FAIL_REQUIREMENT",
                arguments={"actor": "William", "requirement": "room_inspection"},
                atomic_event_ids=["E2", "E10"],
                summary_label="William fails the room inspection standard",
                temporal_phase=InterventionPhase.POST_INTERVENTION,
                is_persistent_state=False,
            ),
            NormalizedEvent(
                norm_id="NE6",
                predicate_name="WITHHOLD_REWARD",
                arguments={"recipient": "William", "reward": "gingerbread"},
                atomic_event_ids=["E11"],
                summary_label="Gingerbread reward is withheld due to unmet requirement",
                temporal_phase=InterventionPhase.POST_INTERVENTION,
                is_persistent_state=False,
            ),
            NormalizedEvent(
                norm_id="NE7",
                predicate_name="EMOTIONAL_OUTBURST",
                arguments={"actor": "William", "actions": ["sulk", "slam_door", "crack_plaster"]},
                atomic_event_ids=["E3", "E8", "E12"],
                summary_label="William reacts with frustration and door slamming",
                temporal_phase=InterventionPhase.POST_INTERVENTION,
                is_persistent_state=False,
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
                evidence="Habitual daydreaming and inaction directly brought about the accumulated backlog.",
                explicitness=Explicitness.EXPLICIT,
            ),
            EventRelation(
                relation_id="R2",
                source_id="NE2",
                target_id="NE4",
                relation_type=RelationType.CAUSES,
                evidence="The accumulated backlog created an insuperable shortage of remaining time.",
                explicitness=Explicitness.STRONGLY_INFERRED,
            ),
            EventRelation(
                relation_id="R3",
                source_id="NE2",
                target_id="NE3",
                relation_type=RelationType.BEFORE,
                evidence="The room backlog already existed before the incentive was introduced.",
                explicitness=Explicitness.EXPLICIT,
            ),
            EventRelation(
                relation_id="R4",
                source_id="NE3",
                target_id="NE5",
                relation_type=RelationType.REQUIRES,
                evidence="Receiving the offered reward requires meeting the inspection standard.",
                explicitness=Explicitness.EXPLICIT,
            ),
            EventRelation(
                relation_id="R5",
                source_id="NE4",
                target_id="NE5",
                relation_type=RelationType.RESULTS_IN,
                evidence="Having insufficient time to finish resulted directly in inspection failure.",
                explicitness=Explicitness.EXPLICIT,
            ),
            EventRelation(
                relation_id="R6",
                source_id="NE5",
                target_id="NE6",
                relation_type=RelationType.RESULTS_IN,
                evidence="Failing the inspection directly triggered the withholding of the reward.",
                explicitness=Explicitness.EXPLICIT,
            ),
            EventRelation(
                relation_id="R7",
                source_id="NE6",
                target_id="NE7",
                relation_type=RelationType.RESULTS_IN,
                evidence="Reward withholding triggered downstream emotional frustration.",
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
                label="Task neglect and inaction",
                source_normalized_ids=["NE1"],
                functional_role=BackboneRole.CAUSAL_ANTECEDENT,
                temporal_phase=InterventionPhase.PRE_INTERVENTION,
                temporal_order=1,
                abstraction_level_0="William spends his time daydreaming about food instead of cleaning",
                abstraction_level_1="William neglects cleaning his room",
                abstraction_level_2="task neglect / inaction",
                abstraction_level_3="failure to pursue primary task",
            ),
            GeneratedMacroNode(
                macro_id="M2",
                label="Accumulated deficit backlog",
                source_normalized_ids=["NE2"],
                functional_role=BackboneRole.PROBLEM_STATE,
                temporal_phase=InterventionPhase.SPANS_INTERVENTION,
                temporal_order=2,
                abstraction_level_0="The room remains messy a few days before inspection",
                abstraction_level_1="Room is in an uncleaned backlog state",
                abstraction_level_2="accumulated deficit / backlog",
                abstraction_level_3="deficit condition",
            ),
            GeneratedMacroNode(
                macro_id="M3",
                label="Conditional incentive introduced",
                source_normalized_ids=["NE3"],
                functional_role=BackboneRole.INTERVENTION,
                temporal_phase=InterventionPhase.AT_INTERVENTION,
                temporal_order=3,
                abstraction_level_0="Nurse promises gingerbread if William scrubs the room",
                abstraction_level_1="Authority offers food reward for completing room cleaning",
                abstraction_level_2="conditional reward offered as incentive",
                abstraction_level_3="external motivation intervention",
            ),
            GeneratedMacroNode(
                macro_id="M4",
                label="Inability to recover in remaining time",
                source_normalized_ids=["NE4"],
                functional_role=BackboneRole.CONSTRAINT,
                temporal_phase=InterventionPhase.SPANS_INTERVENTION,
                temporal_order=4,
                abstraction_level_0="There was no longer enough time for him to put it in order",
                abstraction_level_1="Insufficient remaining time to clean room",
                abstraction_level_2="insufficient remaining time / inability to recover",
                abstraction_level_3="irreversible task obstruction",
            ),
            GeneratedMacroNode(
                macro_id="M5",
                label="Requirement failure",
                source_normalized_ids=["NE5"],
                functional_role=BackboneRole.FOCAL_OUTCOME,
                temporal_phase=InterventionPhase.POST_INTERVENTION,
                temporal_order=5,
                abstraction_level_0="William does not pass the monthly room inspection",
                abstraction_level_1="Fails room inspection standard",
                abstraction_level_2="requirement failure",
                abstraction_level_3="task objective failure",
            ),
            GeneratedMacroNode(
                macro_id="M6",
                label="Reward withheld",
                source_normalized_ids=["NE6"],
                functional_role=BackboneRole.CONTINGENT_OUTCOME,
                temporal_phase=InterventionPhase.POST_INTERVENTION,
                temporal_order=6,
                abstraction_level_0="William does not get any gingerbread",
                abstraction_level_1="Gingerbread treat is withheld",
                abstraction_level_2="reward withheld",
                abstraction_level_3="incentive withholding",
            ),
        ]
    )
