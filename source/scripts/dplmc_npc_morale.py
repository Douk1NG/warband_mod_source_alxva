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

dplmc_npc_morale_scripts = [
##"script_dplmc_estimate_center_weekly_income"
("dplmc_npc_morale",
      [
        (store_script_param_1, ":npc"),
        (store_script_param_2, ":mode"),
        (try_begin), #if we actually care
          (eq, ":mode", 1),
          (call_script, "script_npc_morale", ":npc"),
        (else_try), #we just want the numbers
          (troop_get_slot, ":morality_grievances", ":npc", slot_troop_morality_penalties),
          (troop_get_slot, ":personality_grievances", ":npc", slot_troop_personalityclash_penalties),
          (party_get_morale, ":party_morale", "p_main_party"),

          (store_sub, ":troop_morale", ":party_morale", ":morality_grievances"),
          (val_sub, ":troop_morale", ":personality_grievances"),
          (val_add, ":troop_morale", 50),

          # (assign, reg8, ":troop_morale"),

          (val_mul, ":troop_morale", 3),
          (val_div, ":troop_morale", 4),
          (val_clamp, ":troop_morale", 0, 100),
          (assign, reg0, ":troop_morale"),
        (try_end),
    ])
]
