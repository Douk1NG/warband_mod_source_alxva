# ======================================================================
# SHARED DEPENDENCY
# Entity: objectionable_action (script)
# Called by menus in 5 domains: battle, camp, dickplomacy, taxes, village
# ======================================================================

# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

objectionable_action_scripts = [
("objectionable_action",
    [
        (store_script_param_1, ":action_type"),
        (store_script_param_2, ":action_string"),

        (assign, ":grievance_minimum", -2),
        (try_for_range, ":npc", companions_begin, companions_end),
            (main_party_has_troop, ":npc"),

###Primary morality check
            (try_begin),
                (troop_slot_eq, ":npc", slot_troop_morality_type, ":action_type"),
                (troop_get_slot, ":value", ":npc", slot_troop_morality_value),
                (try_begin),
                    (troop_slot_eq, ":npc", slot_troop_morality_state, tms_acknowledged),
# npc is betrayed, major penalty to player honor and morale
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_mul, ":value", 2),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
                    (this_or_next|troop_slot_eq, ":npc", slot_troop_morality_state, tms_dismissed),
                        (eq, "$disable_npc_complaints", 1),
# npc is quietly disappointed
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
# npc raises the issue for the first time
                    (troop_slot_eq, ":npc", slot_troop_morality_state, tms_no_problem),
                    (gt, ":value", ":grievance_minimum"),
                    (assign, "$npc_with_grievance", ":npc"),
                    (assign, "$npc_grievance_string", ":action_string"),
                    (assign, "$npc_grievance_slot", slot_troop_morality_state),
                    (assign, ":grievance_minimum", ":value"),
                    (assign, "$npc_praise_not_complaint", 0),
                    (try_begin),
                        (lt, ":value", 0),
                        (assign, "$npc_praise_not_complaint", 1),
                    (try_end),
                (try_end),

###Secondary morality check
            (else_try),
                (troop_slot_eq, ":npc", slot_troop_2ary_morality_type, ":action_type"),
                (troop_get_slot, ":value", ":npc", slot_troop_2ary_morality_value),
                (try_begin),
                    (troop_slot_eq, ":npc", slot_troop_2ary_morality_state, tms_acknowledged),
# npc is betrayed, major penalty to player honor and morale
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_mul, ":value", 2),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
                    (this_or_next|troop_slot_eq, ":npc", slot_troop_2ary_morality_state, tms_dismissed),
                        (eq, "$disable_npc_complaints", 1),
# npc is quietly disappointed
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
# npc raises the issue for the first time
                    (troop_slot_eq, ":npc", slot_troop_2ary_morality_state, tms_no_problem),
                    (gt, ":value", ":grievance_minimum"),
                    (assign, "$npc_with_grievance", ":npc"),
                    (assign, "$npc_grievance_string", ":action_string"),
                    (assign, "$npc_grievance_slot", slot_troop_2ary_morality_state),
                    (assign, ":grievance_minimum", ":value"),
                    (assign, "$npc_praise_not_complaint", 0),
                    (try_begin),
                        (lt, ":value", 0),
                        (assign, "$npc_praise_not_complaint", 1),
                    (try_end),
                (try_end),
            (try_end),

            (try_begin),
                (gt, "$npc_with_grievance", 0),
                (eq, "$npc_praise_not_complaint", 0),
                (str_store_troop_name, 4, "$npc_with_grievance"),
                (display_message, "@{s4} looks upset.", message_alert),
            (try_end),
        (try_end),
     ])
]
