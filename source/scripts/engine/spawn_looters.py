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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

spawn_looters_scripts = [
("spawn_looters",
    [
      (store_script_param, ":center_no", 1),
      (store_script_param, ":num_looters", 2),
      # (party_set_slot, ":center_no", slot_center_is_besieged_by, -1), #clear siege
      # (call_script, "script_village_set_state",  ":center_no", 0), #clear siege flag
      (set_spawn_radius, 4),
      (try_for_range, ":unused", 0, ":num_looters"),
        (spawn_around_party, ":center_no", "pt_looters"),
        #(party_set_ai_behavior, reg0, ai_bhvr_avoid_party),
        #(party_set_ai_object, reg0, ":center_no"),
      (try_end),
    ])
]
