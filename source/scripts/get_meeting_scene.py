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

get_meeting_scene_scripts = [
("get_meeting_scene",
    [
      (party_get_current_terrain, ":terrain_type", "p_main_party"),
      (assign, ":scene_to_use", "scn_random_scene"),
      (try_begin),
        (eq, ":terrain_type", rt_steppe),
        (assign, ":scene_to_use", "scn_meeting_scene_steppe"),
      (else_try),
        (eq, ":terrain_type", rt_plain),
        (assign, ":scene_to_use", "scn_meeting_scene_plain"),
      (else_try),
        (eq, ":terrain_type", rt_snow),
        (assign, ":scene_to_use", "scn_meeting_scene_snow"),
      (else_try),
        (eq, ":terrain_type", rt_desert),
        (assign, ":scene_to_use", "scn_meeting_scene_desert"),
      (else_try),
        (eq, ":terrain_type", rt_steppe_forest),
        (assign, ":scene_to_use", "scn_meeting_scene_steppe"),
      (else_try),
        (eq, ":terrain_type", rt_forest),
        (assign, ":scene_to_use", "scn_meeting_scene_plain"),
      (else_try),
        (eq, ":terrain_type", rt_snow_forest),
        (assign, ":scene_to_use", "scn_meeting_scene_snow"),
      (else_try),
        (eq, ":terrain_type", rt_desert_forest),
        (assign, ":scene_to_use", "scn_meeting_scene_desert"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_river),
        (eq, ":terrain_type", rt_water),
        (assign, ":scene_to_use", "scn_sea_boarding_a_a"),

        (party_get_slot, ":ship_type", "$g_encountered_party", slot_party_ship_type),
        (try_begin),
          (eq, ":ship_type", 1),
          (assign, ":scene_to_use", "scn_sea_boarding_a_a"),
        (else_try),
          (eq, ":ship_type", 2),
          (assign, ":scene_to_use", "scn_sea_boarding_b_b"),
        (else_try),
          (eq, ":ship_type", 3),
          (assign, ":scene_to_use", "scn_sea_boarding_c_c"),
        (else_try),
          (eq, ":ship_type", 4),
          (assign, ":scene_to_use", "scn_sea_boarding_d_d"),
        (try_end),

      (else_try),
        (assign, ":scene_to_use", "scn_meeting_scene_plain"),
      (try_end),
      (assign, reg0, ":scene_to_use"),
  ])
]
