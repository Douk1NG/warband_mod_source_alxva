# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

pick_native_formation_scripts = [
("pick_native_formation", [
      (store_script_param, ":team", 1),
      (store_script_param, ":division", 2),

      (store_add, ":slot", slot_team_d0_size, ":division"),
      (team_get_slot, ":bg_size", ":team", ":slot"),

      (try_begin),
        (eq, ":bg_size", 0),	#script_store_battlegroup_data is not being called
        (team_get_leader, ":leader", ":team"),
        (try_for_agents, ":agent"),
          (call_script, "script_cf_valid_formation_member", ":team", ":division", ":leader", ":agent"),
          (val_add, ":bg_size", 1),
        (try_end),
      (try_end),

      (call_script, "script_calculate_default_ranks", ":bg_size"),
      (try_begin),
        (eq, reg1, 1),
        (assign, reg0, formation_1_row),
      (else_try),
        (eq, reg1, 2),
        (assign, reg0, formation_2_row),
      (else_try),
        (eq, reg1, 3),
        (assign, reg0, formation_3_row),
      (else_try),
        (this_or_next | eq, reg1, 4),
        (eq, Native_Formations_Implementation, WB_Implementation),
        (assign, reg0, formation_4_row),
        (assign, reg1, 4),
      (else_try),
        (assign, reg0, formation_5_row),
        (assign, reg1, 5),
      (try_end)])
]
