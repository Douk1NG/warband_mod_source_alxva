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

check_creating_ladder_dust_effect_scripts = [
# script_store_movement_order_name_to_s1
("check_creating_ladder_dust_effect",
   [
      (store_trigger_param_1, ":instance_id"),
      (store_trigger_param_2, ":remaining_time"),

      (try_begin),
        (lt, ":remaining_time", 15), #less then 0.15 seconds
        (gt, ":remaining_time", 3), #more than 0.03 seconds

        (scene_prop_get_slot, ":smoke_effect_done", ":instance_id", scene_prop_smoke_effect_done),
        (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),

        (try_begin),
          (eq, ":smoke_effect_done", 0),
          (eq, ":opened_or_closed", 0),

          (prop_instance_get_position, pos0, ":instance_id"),

          (assign, ":smallest_dist", -1),
          (try_for_range, ":entry_point_no", multi_entry_points_for_usable_items_start, multi_entry_points_for_usable_items_end),
            (entry_point_get_position, pos1, ":entry_point_no"),
            (get_sq_distance_between_positions, ":dist", pos0, pos1),
            (this_or_next|eq, ":smallest_dist", -1),
            (lt, ":dist", ":smallest_dist"),
            (assign, ":smallest_dist", ":dist"),
            (assign, ":nearest_entry_point", ":entry_point_no"),
          (try_end),

          (try_begin),
            (set_fixed_point_multiplier, 100),

            (ge, ":smallest_dist", 0),
            (lt, ":smallest_dist", 22500), #max 15m distance

            (entry_point_get_position, pos1, ":nearest_entry_point"),
            (position_rotate_x, pos1, -90),

            (prop_instance_get_scene_prop_kind, ":scene_prop_kind", ":instance_id"),
            (try_begin),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_6m"),
              (init_position, pos2),
              (position_set_z, pos2, 300),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_6m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_6m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_8m"),
              (init_position, pos2),
              (position_set_z, pos2, 400),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_8m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_8m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_10m"),
              (init_position, pos2),
              (position_set_z, pos2, 500),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_10m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_10m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_12m"),
              (init_position, pos2),
              (position_set_z, pos2, 600),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_12m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_12m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_14m"),
              (init_position, pos2),
              (position_set_z, pos2, 700),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_14m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_14m", pos3, 100),
            (try_end),

            (scene_prop_set_slot, ":instance_id", scene_prop_smoke_effect_done, 1),
          (try_end),
        (try_end),
      (try_end),
      ])
]
