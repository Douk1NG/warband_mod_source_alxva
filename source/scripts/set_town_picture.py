# ======================================================================
# SHARED DEPENDENCY
# Entity: set_town_picture (script)
# Called by menus in 5 domains: castle, center_management, cheats, town, village
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

set_town_picture_scripts = [
# script_siege_init_ai_and_belfry
# Input: none
# Output: none
("set_town_picture",
   [
        (try_begin),
          (party_get_current_terrain, ":cur_terrain", "$current_town"),
          (party_slot_eq,"$current_town",slot_party_type, spt_town),
          (try_begin),
            (this_or_next|eq, ":cur_terrain", rt_steppe),
            (this_or_next|eq, ":cur_terrain", rt_steppe_forest),
            (this_or_next|eq, ":cur_terrain", rt_desert),
            (             eq, ":cur_terrain", rt_desert_forest),
            (set_background_mesh, "mesh_pic_towndes"),
          (else_try),
            (this_or_next|eq, ":cur_terrain", rt_snow),
            (             eq, ":cur_terrain", rt_snow_forest),
            (set_background_mesh, "mesh_pic_townsnow"),
          (else_try),
            (set_background_mesh, "mesh_pic_town1"),
          (try_end),
        (else_try),
          (party_slot_eq,"$current_town",slot_party_type, spt_castle),
          (try_begin),
            (this_or_next|eq, ":cur_terrain", rt_steppe),
            (this_or_next|eq, ":cur_terrain", rt_steppe_forest),
            (this_or_next|eq, ":cur_terrain", rt_desert),
            (             eq, ":cur_terrain", rt_desert_forest),
            (set_background_mesh, "mesh_pic_castledes"),
          (else_try),
            (this_or_next|eq, ":cur_terrain", rt_snow),
            (             eq, ":cur_terrain", rt_snow_forest),
            (set_background_mesh, "mesh_pic_castlesnow"),
          (else_try),
            (set_background_mesh, "mesh_pic_castle1"),
          (try_end),
        (else_try), #SB : enable for villages
          (party_slot_eq,"$current_town",slot_party_type, spt_village),
          (try_begin),
            (this_or_next|eq, ":cur_terrain", rt_steppe),
            (this_or_next|eq, ":cur_terrain", rt_steppe_forest),
            (this_or_next|eq, ":cur_terrain", rt_desert),
            (             eq, ":cur_terrain", rt_desert_forest),
            (set_background_mesh, "mesh_pic_village_s"),
          (else_try),
            (this_or_next|eq, ":cur_terrain", rt_snow),
            (             eq, ":cur_terrain", rt_snow_forest),
            (set_background_mesh, "mesh_pic_village_w"),
          (else_try),
            (set_background_mesh, "mesh_pic_village_p"),
          (try_end),
        (try_end),
    ])
]
