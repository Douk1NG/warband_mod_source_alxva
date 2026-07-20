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

create_cattle_herd_scripts = [
("create_cattle_herd",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":amount"),

      (assign, ":herd_party", -1),
      (set_spawn_radius,1),

      (spawn_around_party,":center_no", "pt_cattle_herd"),
      (assign, ":herd_party", reg0),
      (party_get_position, pos1, ":center_no"),
      (call_script, "script_map_get_random_position_around_position_within_range", 1, 2),
      (party_set_position, ":herd_party", pos2),

      (party_set_slot, ":herd_party", slot_party_type, spt_cattle_herd),
      (party_set_slot, ":herd_party", slot_party_ai_state, spai_undefined),
      (party_set_ai_behavior, ":herd_party", ai_bhvr_hold),

      (party_set_slot, ":herd_party", slot_party_commander_party, -1), #we need this because 0 is player's party!

      (try_begin),
        (gt, ":amount", 0),
        (party_clear, ":herd_party"),
        (party_add_members, ":herd_party", "trp_cattle", ":amount"),
      (try_end),

      (assign, reg0, ":herd_party"),
  ])
]
