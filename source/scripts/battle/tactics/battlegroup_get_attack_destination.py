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

battlegroup_get_attack_destination_scripts = [
("battlegroup_get_attack_destination", [
      (store_script_param, ":bgposition", 1),
      (store_script_param, ":bgteam", 2),
      (store_script_param, ":bgdivision", 3),
      (store_script_param, ":enemy_team", 4),
      (store_script_param, ":enemy_division", 5),

      (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
      (team_get_slot, ":bgformation", ":bgteam", ":slot"),
      (try_begin),
        (le, ":bgformation", formation_none),
        (call_script, "script_battlegroup_get_position", ":bgposition", ":bgteam", ":bgdivision"),
      (else_try),
        (call_script, "script_formation_current_position", ":bgposition", ":bgteam", ":bgdivision"),
      (try_end),

      #distance to enemy center
      (store_add, ":slot", slot_team_d0_formation, ":enemy_division"),
      (team_get_slot, ":enemy_formation", ":enemy_team", ":slot"),
      (call_script, "script_battlegroup_get_position", Enemy_Team_Pos, ":enemy_team", ":enemy_division"),
      (get_distance_between_positions, ":distance_to_move", ":bgposition", Enemy_Team_Pos),

      (call_script, "script_battlegroup_get_action_radius", ":bgteam", ":bgdivision"),
      (assign, ":bgwidth", reg0),
      (call_script, "script_battlegroup_get_action_radius", ":enemy_team", ":enemy_division"),
      (store_add, ":combined_width", ":bgwidth", reg0),

      (assign, ":min_radius", reg0),
      (val_min, ":min_radius", ":bgwidth"),
      (val_div, ":min_radius", 2),	#function returns length of bg

      (try_begin),
        (gt, ":bgformation", formation_none),	#in formation AND
        (le, ":distance_to_move", ":combined_width"),	#close to enemy
        (store_mul, reg0, -350, formation_reform_interval),	#back up one move (to avoid wild swings / reversals on overruns)
        (position_move_y, ":bgposition", reg0),
        (get_distance_between_positions, ":distance_to_move", ":bgposition", Enemy_Team_Pos),
      (try_end),

      #subtract enemy center to edge-of-contact (determined by minimum half-width
      #between the two battlegroups)
      (call_script, "script_get_distance_to_battlegroup", ":enemy_team", ":enemy_division", ":bgposition"),
      (store_mul, ":angle_adjusted_half_depth", ":min_radius", reg2),	#reg2 is cosine glancing angle, FP
      (convert_from_fixed_point, ":angle_adjusted_half_depth"),
      (try_begin),
        (neq, ":enemy_formation", formation_wedge),
        (call_script, "script_battlegroup_dist_center_to_front", ":enemy_team", ":enemy_division"),
        (val_max, ":angle_adjusted_half_depth", reg0),
      (try_end),
      (val_sub, ":distance_to_move", ":angle_adjusted_half_depth"),

      #modify by bg center to edge-of-contact, if needed
      (call_script, "script_battlegroup_dist_center_to_front", ":bgteam", ":bgdivision"),
      (assign, ":bg_half_depth", reg0),
      (try_begin),
        (le, ":bgformation", formation_none),
        (val_sub, ":distance_to_move", ":bg_half_depth"),	#position from script_battlegroup_get_position is in middle of bg
      (else_try),
        (eq, ":bgformation", formation_wedge),
        (call_script, "script_battlegroup_dist_center_to_front", ":enemy_team", ":enemy_division"),
        (val_add, ":distance_to_move", reg0),	#move in from nearest edge found by script_get_distance_to_battlegroup
        (val_add, ":distance_to_move", ":bg_half_depth"),	#drive wedge through target formation!
      (try_end),

      #modify by speed differential
      (try_begin),
        (gt, ":enemy_formation", formation_none),
        (neq, ":enemy_formation", formation_default),

        (store_add, ":slot", slot_team_d0_first_member, ":enemy_division"),
        (team_get_slot, reg0, ":enemy_team", ":slot"),
        (agent_is_active, reg0),

        (agent_get_speed, Speed_Pos, reg0),
        (init_position, Temp_Pos),
        (get_distance_between_positions, ":enemy_formation_speed", Speed_Pos, Temp_Pos),
        (val_mul, ":enemy_formation_speed", formation_reform_interval),	#calculate distance to next call

        (try_begin),
          (position_is_behind_position, ":bgposition", Enemy_Team_Pos),	#attacking from rear?
          (val_add, ":distance_to_move", ":enemy_formation_speed"),	#catch up to anticipated position
        (else_try),	#attacking enemy formation from front
          (store_add, ":slot", slot_team_d0_is_fighting, ":bgdivision"),
          (team_slot_eq, ":bgteam", ":slot", 0),
          (val_sub, ":distance_to_move", ":enemy_formation_speed"),	#avoid overrunning enemy
        (try_end),
      (try_end),

      (store_add, ":slot", slot_team_d0_front_weapon_length, ":bgdivision"),
      (team_get_slot, ":striking_distance", ":bgteam", ":slot"),
      (val_sub, ":distance_to_move", ":striking_distance"),

      (call_script, "script_point_y_toward_position", ":bgposition", Enemy_Team_Pos),
      (position_move_y, ":bgposition", ":distance_to_move"),])
]
