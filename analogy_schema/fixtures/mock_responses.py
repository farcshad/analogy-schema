from analogy_schema.models.events import AtomicEvent, NormalizedEvent, EventType, Polarity, Explicitness
from analogy_schema.models.relations import EventRelation, RelationType
from analogy_schema.pipeline.stage_a_atomic import AtomicExtractionOutput
from analogy_schema.pipeline.stage_b_normalize import NormalizationOutput
from analogy_schema.pipeline.stage_c_relations import RelationExtractionOutput
from analogy_schema.pipeline.stage_d_goals import GoalOutcomeOutput
from analogy_schema.pipeline.stage_f_backbone import BackboneSelectionOutput, PrunedEventAudit
from analogy_schema.pipeline.stage_g_macro import (
    MacroAbstractionOutput,
    GeneratedMacroNode,
    GeneratedBackboneEdge,
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
            ),
            NormalizedEvent(
                norm_id="NE2",
                predicate_name="INSUFFICIENT_PROGRESS",
                arguments={"actor": "William", "state": "room_is_mess"},
                atomic_event_ids=["E5"],
                summary_label="Room remains messy and uncleaned before inspection",
            ),
            NormalizedEvent(
                norm_id="NE3",
                predicate_name="OFFER_CONDITIONAL_INCENTIVE",
                arguments={"provider": "nurse", "recipient": "William", "reward": "gingerbread", "condition": "clean_room"},
                atomic_event_ids=["E7"],
                summary_label="Nurse offers gingerbread incentive conditional on cleaning room",
            ),
            NormalizedEvent(
                norm_id="NE4",
                predicate_name="INSUFFICIENT_REMAINING_TIME",
                arguments={"actor": "William", "target": "complete_cleaning"},
                atomic_event_ids=["E9"],
                summary_label="There is insufficient remaining time to complete the task",
            ),
            NormalizedEvent(
                norm_id="NE5",
                predicate_name="FAIL_REQUIREMENT",
                arguments={"actor": "William", "requirement": "room_inspection"},
                atomic_event_ids=["E2", "E10"],
                summary_label="William fails the room inspection requirement",
            ),
            NormalizedEvent(
                norm_id="NE6",
                predicate_name="WITHHOLD_REWARD",
                arguments={"recipient": "William", "reward": "gingerbread"},
                atomic_event_ids=["E11"],
                summary_label="Gingerbread reward is withheld",
            ),
            NormalizedEvent(
                norm_id="NE7",
                predicate_name="EMOTIONAL_FRUSTRATION",
                arguments={"actor": "William", "actions": ["sulk", "slam_door"]},
                atomic_event_ids=["E3", "E8", "E12"],
                summary_label="William reacts with frustration and slams door",
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
                evidence="William doing nothing but daydreaming directly caused the room to remain a mess.",
                explicitness=Explicitness.EXPLICIT,
            ),
            EventRelation(
                relation_id="R2",
                source_id="NE2",
                target_id="NE4",
                relation_type=RelationType.CAUSES,
                evidence="Accumulated backlog and messiness led to insufficient remaining time to finish.",
                explicitness=Explicitness.STRONGLY_INFERRED,
            ),
            EventRelation(
                relation_id="R3",
                source_id="NE2",
                target_id="NE3",
                relation_type=RelationType.BEFORE,
                evidence="The backlog and messy room existed before the nurse intervened with an incentive.",
                explicitness=Explicitness.EXPLICIT,
            ),
            EventRelation(
                relation_id="R4",
                source_id="NE3",
                target_id="NE5",
                relation_type=RelationType.CONDITIONAL_ON,
                evidence="Receiving the reward offered in NE3 was conditional on passing the requirement NE5.",
                explicitness=Explicitness.EXPLICIT,
            ),
            EventRelation(
                relation_id="R5",
                source_id="NE4",
                target_id="NE5",
                relation_type=RelationType.RESULTS_IN,
                evidence="Having insufficient time to finish resulted in William failing the inspection.",
                explicitness=Explicitness.EXPLICIT,
            ),
            EventRelation(
                relation_id="R6",
                source_id="NE5",
                target_id="NE6",
                relation_type=RelationType.RESULTS_IN,
                evidence="Failing the room inspection resulted in the gingerbread reward being withheld.",
                explicitness=Explicitness.EXPLICIT,
            ),
            EventRelation(
                relation_id="R7",
                source_id="NE6",
                target_id="NE7",
                relation_type=RelationType.RESULTS_IN,
                evidence="Reward withholding triggered William's emotional frustration.",
                explicitness=Explicitness.EXPLICIT,
            ),
        ]
    )


def get_william_mock_stage_d() -> GoalOutcomeOutput:
    return GoalOutcomeOutput(
        central_problem="William neglects cleaning and falls too far behind to recover",
        central_goal="Clean room and pass room inspection",
        intervention="Nurse offers gingerbread incentive to motivate room cleaning",
        terminal_outcomes=["Fails room inspection", "Gingerbread reward withheld"],
        anchor_event_ids=["NE1", "NE2", "NE3", "NE4", "NE5", "NE6"]
    )


def get_william_mock_stage_f() -> BackboneSelectionOutput:
    return BackboneSelectionOutput(
        retained_event_ids=["NE1", "NE2", "NE3", "NE4", "NE5", "NE6"],
        pruned_events=[
            PrunedEventAudit(
                norm_id="NE7",
                reason="Emotional reaction / door slamming does not explain why the inspection failed or how the incentive functioned."
            )
        ]
    )


def get_william_mock_stage_gh() -> MacroAbstractionOutput:
    return MacroAbstractionOutput(
        macro_nodes=[
            GeneratedMacroNode(
                macro_id="M1",
                label="Task neglect and daydreaming",
                source_normalized_ids=["NE1"],
                functional_role="primary_neglect",
                temporal_order=1,
                abstraction_level_0="William spends his time daydreaming about food instead of cleaning",
                abstraction_level_1="William neglects cleaning his hospital room",
                abstraction_level_2="task neglect / inaction",
                abstraction_level_3="failure to pursue primary task",
                is_intervention=False,
                is_terminal_outcome=False,
            ),
            GeneratedMacroNode(
                macro_id="M2",
                label="Accumulated backlog / insufficient progress",
                source_normalized_ids=["NE2"],
                functional_role="accumulated_deficit",
                temporal_order=2,
                abstraction_level_0="The room remains messy a few days before inspection",
                abstraction_level_1="Room is in an uncleaned backlog state",
                abstraction_level_2="insufficient task progress / accumulated deficit",
                abstraction_level_3="deficit condition",
                is_intervention=False,
                is_terminal_outcome=False,
            ),
            GeneratedMacroNode(
                macro_id="M3",
                label="Conditional incentive offered",
                source_normalized_ids=["NE3"],
                functional_role="intervention",
                temporal_order=3,
                abstraction_level_0="Nurse promises gingerbread if William scrubs the room",
                abstraction_level_1="Authority offers food reward for completing room cleaning",
                abstraction_level_2="conditional reward offered as incentive",
                abstraction_level_3="external motivation intervention",
                is_intervention=True,
                is_terminal_outcome=False,
            ),
            GeneratedMacroNode(
                macro_id="M4",
                label="Inability to recover due to deficit",
                source_normalized_ids=["NE4"],
                functional_role="irrecoverable_state",
                temporal_order=4,
                abstraction_level_0="There was no longer enough time for him to put it in order",
                abstraction_level_1="Insufficient remaining time to clean room",
                abstraction_level_2="insufficient remaining time / inability to recover",
                abstraction_level_3="irreversible task obstruction",
                is_intervention=False,
                is_terminal_outcome=False,
            ),
            GeneratedMacroNode(
                macro_id="M5",
                label="Requirement failure",
                source_normalized_ids=["NE5"],
                functional_role="requirement_failure",
                temporal_order=5,
                abstraction_level_0="William does not pass the monthly room inspection",
                abstraction_level_1="Fails room inspection standard",
                abstraction_level_2="requirement failure",
                abstraction_level_3="task objective failure",
                is_intervention=False,
                is_terminal_outcome=True,
            ),
            GeneratedMacroNode(
                macro_id="M6",
                label="Reward withheld",
                source_normalized_ids=["NE6"],
                functional_role="consequential_penalty",
                temporal_order=6,
                abstraction_level_0="William does not get any gingerbread",
                abstraction_level_1="Gingerbread treat is withheld",
                abstraction_level_2="reward withheld",
                abstraction_level_3="incentive withholding",
                is_intervention=False,
                is_terminal_outcome=True,
            ),
        ],
        backbone_edges=[
            GeneratedBackboneEdge(
                edge_id="BE1",
                source_macro_id="M1",
                target_macro_id="M2",
                relation_type=RelationType.CAUSES,
                justification="Neglect and daydreaming directly caused the deficit backlog.",
            ),
            GeneratedBackboneEdge(
                edge_id="BE2",
                source_macro_id="M2",
                target_macro_id="M4",
                relation_type=RelationType.CAUSES,
                justification="The accumulated deficit caused an irrecoverable shortage of remaining time.",
            ),
            GeneratedBackboneEdge(
                edge_id="BE3",
                source_macro_id="M2",
                target_macro_id="M3",
                relation_type=RelationType.BEFORE,
                justification="The deficit existed before the incentive was introduced; incentive did not cause the backlog.",
            ),
            GeneratedBackboneEdge(
                edge_id="BE4",
                source_macro_id="M4",
                target_macro_id="M5",
                relation_type=RelationType.RESULTS_IN,
                justification="Inability to recover in time resulted directly in inspection failure.",
            ),
            GeneratedBackboneEdge(
                edge_id="BE5",
                source_macro_id="M5",
                target_macro_id="M6",
                relation_type=RelationType.RESULTS_IN,
                justification="Failing the requirement caused the promised reward to be withheld.",
            ),
        ]
    )
