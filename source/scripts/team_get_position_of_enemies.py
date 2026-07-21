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

team_get_position_of_enemies_scripts = [
("team_get_position_of_enemies", [
      (store_script_param, ":enemy_position", 1),
      (store_script_param, ":team_no", 2),
      (store_script_param, ":troop_type", 3),
      (assign, ":pos_x", 0),
      (assign, ":pos_y", 0),
      (assign, ":total_size", 0),
      (try_begin),
        (neq, ":troop_type", grc_everyone),
        (assign, ":closest_distance", Far_Away),
        (call_script, "script_battlegroup_get_position", Temp_Pos, ":team_no", grc_everyone),
      (try_end),

      (try_for_range, ":other_team", 0, 4),
        (teams_are_enemies, ":other_team", ":team_no"),
        (try_begin),
          (eq, ":troop_type", grc_everyone),
          (team_get_slot, ":team_size", ":other_team", slot_team_size),
          (try_begin),
            (gt, ":team_size", 0),
            (call_script, "script_battlegroup_get_position", ":enemy_position", ":other_team", grc_everyone),
            (position_get_x, reg0, ":enemy_position"),
            (val_mul, reg0, ":team_size"),
            (val_add, ":pos_x", reg0),
            (position_get_y, reg0, ":enemy_position"),
            (val_mul, reg0, ":team_size"),
            (val_add, ":pos_y", reg0),
          (try_end),
        (else_try),	#for multiple divisions, should find the CLOSEST of a given type
          (assign, ":team_size", 0),
          (try_for_range, ":enemy_battle_group", 0, 9),
            (store_add, ":slot", slot_team_d0_size, ":enemy_battle_group"),
            (team_get_slot, ":troop_count", ":other_team", ":slot"),
            (gt, ":troop_count", 0),
            (store_add, ":slot", slot_team_d0_type, ":enemy_battle_group"),
            (team_get_slot, ":bg_type", ":other_team", ":slot"),
            (store_sub, ":bg_root_type", ":bg_type", 3), #subtype is three more than main type
            (this_or_next | eq, ":bg_type", ":troop_type"),
            (eq, ":bg_root_type", ":troop_type"),
            (val_add, ":team_size", ":troop_count"),
            (call_script, "script_battlegroup_get_position", ":enemy_position", ":other_team", ":enemy_battle_group"),
            (get_distance_between_positions, reg0, Temp_Pos, ":enemy_position"),
            (lt, reg0, ":closest_distance"),
            (assign, ":closest_distance", reg0),
            (position_get_x, ":pos_x", ":enemy_position"),
            (position_get_y, ":pos_y", ":enemy_position"),
          (try_end),
        (try_end),
        (val_add, ":total_size", ":team_size"),
      (try_end),

      (try_begin),
        (eq, ":total_size", 0),
        (init_position, ":enemy_position"),
      (else_try),
        (eq, ":troop_type", grc_everyone),
        (val_div, ":pos_x", ":total_size"),
        (position_set_x, ":enemy_position", ":pos_x"),
        (val_div, ":pos_y", ":total_size"),
        (position_set_y, ":enemy_position", ":pos_y"),
        (position_set_z_to_ground_level, ":enemy_position"),
      (else_try),
        (position_set_x, ":enemy_position", ":pos_x"),
        (position_set_y, ":enemy_position", ":pos_y"),
        (position_set_z_to_ground_level, ":enemy_position"),
      (try_end),

      (assign, reg0, ":total_size"),])
]
