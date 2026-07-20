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

formation_move_position_scripts = [
("formation_move_position", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fcurrentpos", 3),
      (store_script_param, ":direction", 4),
      (copy_position, pos1, ":fcurrentpos"),
      (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, ":fteam", grc_everyone),
      (try_begin),
        (neq, reg0, 0),	#more than 0 enemies still alive?
        (copy_position, pos1, ":fcurrentpos"),	#restore current formation "position"
        (call_script, "script_point_y_toward_position", pos1, Enemy_Team_Pos),	#record angle from center to enemy
        (assign, ":distance_to_enemy", reg0),
        (call_script, "script_get_formation_destination", pos61, ":fteam", ":fdivision"),
        (get_distance_between_positions, ":move_amount", pos1, pos61),	#distance already moving from previous orders
        (val_add, ":move_amount", 1000),
        (try_begin),
          (gt, ":direction", 0),	#moving forward?
          (gt, ":move_amount", ":distance_to_enemy"),
          (assign, ":move_amount", ":distance_to_enemy"),
        (try_end),
        (val_mul, ":move_amount", ":direction"),
        (position_move_y, pos1, ":move_amount", 0),
        (position_get_x, ":from_x", pos1),
        (position_get_y, ":from_y", pos1),
        (try_begin),
          (is_between, ":from_x", "$g_bound_left", "$g_bound_right"),
          (is_between, ":from_y", "$g_bound_bottom", "$g_bound_top"),
          (try_begin),
            (lt, ":distance_to_enemy", 1000),	#less than a move away?
            (position_copy_rotation, pos1, pos61),	#avoid rotating formation
          (try_end),
          (call_script, "script_set_formation_destination", ":fteam", ":fdivision", pos1),
          (store_add, ":slot", slot_team_d0_size, ":fdivision"),
          (team_get_slot, ":num_troops", ":fteam", ":slot"),
          (store_add, ":slot", slot_team_d0_formation_space, ":fdivision"),
          (team_get_slot, ":formation_extra_spacing", ":fteam", ":slot"),
          (try_begin),
            (store_add, ":slot", slot_team_d0_type, ":fdivision"),
            (neg | team_slot_eq, ":fteam", ":slot", sdt_archer),
            (store_add, ":slot", slot_team_d0_formation, ":fdivision"),
            (team_get_slot, ":fformation", ":fteam", ":slot"),
            (call_script, "script_get_centering_amount", ":fformation", ":num_troops", ":formation_extra_spacing"),
          (else_try),
            (call_script, "script_get_centering_amount", formation_default, ":num_troops", ":formation_extra_spacing"),
            (val_mul, reg0, -1),
          (try_end),
          (position_move_x, pos1, reg0, 0),

          #out of bounds
        (else_try),
          (copy_position, pos1, ":fcurrentpos"),	#restore current formation "position"
        (try_end),
      (try_end),])
]
