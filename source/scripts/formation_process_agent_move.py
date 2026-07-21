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

formation_process_agent_move_scripts = [
("formation_process_agent_move", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":agent", 3),
      (store_script_param, ":rank", 4),

      (agent_set_scripted_destination, ":agent", pos1, 1),

      (agent_get_position, Current_Pos, ":agent"),
      (get_distance_between_positions, ":distance_to_go", Current_Pos, pos1),

      (store_add, ":slot", slot_team_d0_speed_limit, ":fdivision"),
      (team_get_slot, ":speed_limit", ":fteam", ":slot"),

      (agent_get_speed, Speed_Pos, ":agent"),
      (position_transform_position_to_parent, Temp_Pos, Current_Pos, Speed_Pos),
      (call_script, "script_point_y_toward_position", Current_Pos, Temp_Pos),	#get direction of travel
      (store_mul, ":expected_travel", reg0, formation_reform_interval),
      (store_div, ":speed", ":expected_travel", Km_Per_Hour_To_Cm),

      #First Agent
      (try_begin),
        (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
        (neg | team_slot_ge, ":fteam", ":slot", 0),
        (team_set_slot, ":fteam", ":slot", ":agent"),

        (try_begin),	#reset speed when first member stopped
          (le, ":speed", 5),	#minimum observed speed
          (store_add, ":slot", slot_team_d0_speed_limit, ":fdivision"),
          (team_set_slot, ":fteam", ":slot", Top_Speed),
          (agent_set_speed_limit, ":agent", Top_Speed),

        (else_try),	#first member in motion
          (val_mul, ":speed", 2),	#after terrain & encumbrance, agents tend to move about half their speed limit
          (try_begin),	#speed up if everyone caught up
            (store_add, ":slot", slot_team_d0_percent_in_place, ":fdivision"),
            (team_slot_ge, ":fteam", ":slot", 100),
            (try_begin),
              (ge, ":speed", ":speed_limit"),
              (val_add, ":speed_limit", 1),
            (try_end),
          (else_try),	#else slow down
            (val_min, ":speed_limit", ":speed"),
            (val_sub, ":speed_limit", 1),
            (val_max, ":speed_limit", 5),	#minimum observed speed
          (try_end),

          #build formation from first agent
          (store_add, ":slot", slot_team_d0_prev_first_member, ":fdivision"),
          (team_slot_eq, ":fteam", ":slot", ":agent"),	#looking at same first member as last call?

          (call_script, "script_battlegroup_get_position", Temp_Pos, ":fteam", ":fdivision"),
          (get_distance_between_positions, ":distance_from_group", Current_Pos, Temp_Pos),
          (call_script, "script_battlegroup_get_action_radius", ":fteam", ":fdivision"),
          (val_div, reg0, 2),	#function returns length of bg
          (val_sub, ":distance_from_group", reg0),
          (lt, ":distance_from_group", 2000),	#within 20m of rest of division?

          (store_mul, ":expected_travel", ":speed_limit", Km_Per_Hour_To_Cm),
          (lt, ":expected_travel", ":distance_to_go"),	#more than one call from destination?

          (store_add, ":slot", slot_team_d0_speed_limit, ":fdivision"),
          (team_set_slot, ":fteam", ":slot", ":speed_limit"),
          (agent_set_speed_limit, ":agent", ":speed_limit"),

          (copy_position, Temp_Pos, Current_Pos),
          (call_script, "script_point_y_toward_position", Temp_Pos, pos1),
          (position_move_y, Temp_Pos, ":expected_travel", 0),	#anticipate where first member will be next
          (position_copy_rotation, Temp_Pos, pos1),	#conserve destination facing of formation
          (copy_position, pos1, Temp_Pos),	#reference the rest of the formation to first member's anticipated position
        (try_end),

        (store_add, ":slot", slot_team_d0_percent_in_place, ":fdivision"),
        (team_set_slot, ":fteam", ":slot", 1),	#reinit: always count first member as having arrived
        (store_add, ":slot", slot_team_d0_prev_first_member, ":fdivision"),
        (team_set_slot, ":fteam", ":slot", ":agent"),

      #Not First Agent
      (else_try),
        (try_begin),
          (le, ":speed", 0),
          (assign, ":speed_limit", Top_Speed),
        (else_try),
          (neg | position_is_behind_position, pos1, Current_Pos),
          (store_div, ":speed_limit", ":distance_to_go", Km_Per_Hour_To_Cm),
          (val_max, ":speed_limit", 1),
        (else_try),
          (store_add, ":slot", slot_team_d0_is_fighting, ":fdivision"),
          (team_slot_eq, ":fteam", ":slot", 0),
          (assign, ":speed_limit", 1),
        (else_try),
          (assign, ":speed_limit", Top_Speed),
        (try_end),
        (agent_set_speed_limit, ":agent", ":speed_limit"),
        (try_begin),
          (this_or_next | le, ":speed", 0),	#reached previous destination or blocked OR
          (this_or_next | lt, ":speed_limit", Top_Speed),	#destination within reach OR
          (position_is_behind_position, pos1, Current_Pos),	#agent ahead of formation
          (store_add, ":slot", slot_team_d0_percent_in_place, ":fdivision"),
          (team_get_slot, reg0, ":fteam", ":slot"),
          (val_add, reg0, 1),
          (team_set_slot, ":fteam", ":slot", reg0),
        (try_end),
      (try_end),

      #Housekeeping
      (agent_set_slot, ":agent", slot_agent_formation_rank, ":rank"),])
]
