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

remove_siege_objects_scripts = [
# script_process_alarms
# Input: none
# Output: none
("remove_siege_objects",
    [
      (replace_scene_props, "spr_battlement_a_destroyed", "spr_battlement_a"),
      (replace_scene_props, "spr_snowy_castle_battlement_a_destroyed", "spr_snowy_castle_battlement_a"),
      (replace_scene_props, "spr_castle_e_battlement_a_destroyed", "spr_castle_e_battlement_a"),
      (replace_scene_props, "spr_castle_battlement_a_destroyed", "spr_castle_battlement_a"),
      (replace_scene_props, "spr_castle_battlement_b_destroyed", "spr_castle_battlement_b"),
      (replace_scene_props, "spr_earth_wall_a2", "spr_earth_wall_a"),
      (replace_scene_props, "spr_earth_wall_b2", "spr_earth_wall_b"),
      (replace_scene_props, "spr_belfry_platform_b", "spr_empty"),
      (replace_scene_props, "spr_belfry_platform_a", "spr_empty"),
      (replace_scene_props, "spr_belfry_a", "spr_empty"),
      (replace_scene_props, "spr_belfry_wheel", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_move_6m", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_move_8m", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_move_10m", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_move_12m", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_move_14m", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_12m", "spr_empty"),
      (replace_scene_props, "spr_siege_ladder_14m", "spr_empty"),
      (replace_scene_props, "spr_mangonel", "spr_empty"),
      (replace_scene_props, "spr_trebuchet_old", "spr_empty"),
      (replace_scene_props, "spr_trebuchet_new", "spr_empty"),
      (replace_scene_props, "spr_stone_ball", "spr_empty"),
      (replace_scene_props, "spr_village_fire_big", "spr_empty"),
      ])
]
