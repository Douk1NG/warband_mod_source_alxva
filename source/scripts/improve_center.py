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

improve_center_scripts = [
("improve_center", [
        (store_script_param, ":center_no", 1),
        (store_script_param, ":builder", 2),
        (store_script_param, ":improvement_time", 3),
        (party_set_slot, ":center_no", slot_center_current_improvement, "$g_improvement_type"),
        (store_current_hours, ":cur_hours"),
        (store_mul, ":hours_takes", ":improvement_time", 24),
        (val_add, ":hours_takes", ":cur_hours"),
        (party_set_slot, ":center_no", slot_center_improvement_end_hour, ":hours_takes"),
        (assign, reg6, ":improvement_time"),
        (call_script, "script_get_improvement_details", "$g_improvement_type"),
        (add_party_note_from_sreg, ":center_no", 2, "@A {s0} is being built. It will finish in {reg6} days", 1),
        (try_begin), #should probably raise this depending on project instead of constant reward
          (troop_is_hero, ":builder"),
          (neq, ":builder", "trp_player"),
          (call_script, "script_change_troop_renown", ":builder", dplmc_companion_skill_renown),
        (try_end),
    ])
]
