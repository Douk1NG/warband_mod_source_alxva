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

tactics_scripts = [

("find_high_ground_around_pos1",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":search_radius", 2),
      (val_mul, ":search_radius", 100),
      (get_scene_boundaries, pos10,pos11),
      (team_get_leader, ":ai_leader", ":team_no"),
      (agent_get_position, pos1, ":ai_leader"),
      (set_fixed_point_multiplier, 100),
      (position_get_x, ":o_x", pos1),
      (position_get_y, ":o_y", pos1),
      (store_sub, ":min_x", ":o_x", ":search_radius"),
      (store_sub, ":min_y", ":o_y", ":search_radius"),
      (store_add, ":max_x", ":o_x", ":search_radius"),
      (store_add, ":max_y", ":o_y", ":search_radius"),
      (position_get_x, ":scene_min_x", pos10),
      (position_get_x, ":scene_max_x", pos11),
      (position_get_y, ":scene_min_y", pos10),
      (position_get_y, ":scene_max_y", pos11),
      #do not find positions close to borders (20 m)
      (val_add, ":scene_min_x", 2000),
      (val_sub, ":scene_max_x", 2000),
      (val_add, ":scene_min_y", 2000),
      (val_sub, ":scene_max_y", 2000),
      (val_max, ":min_x", ":scene_min_x"),
      (val_max, ":min_y", ":scene_min_y"),
      (val_min, ":max_x", ":scene_max_x"),
      (val_min, ":max_y", ":scene_max_y"),

      (store_div, ":min_x_meters", ":min_x", 100),
      (store_div, ":min_y_meters", ":min_y", 100),
      (store_div, ":max_x_meters", ":max_x", 100),
      (store_div, ":max_y_meters", ":max_y", 100),

      (assign, ":highest_pos_z", -10000),
      (copy_position, pos52, pos1),
      (init_position, pos15),

      (try_for_range, ":i_x", ":min_x_meters", ":max_x_meters"),
        (store_mul, ":i_x_cm", ":i_x", 100),
        (try_for_range, ":i_y", ":min_y_meters", ":max_y_meters"),
          (store_mul, ":i_y_cm", ":i_y", 100),
          (position_set_x, pos15, ":i_x_cm"),
          (position_set_y, pos15, ":i_y_cm"),
          (position_set_z, pos15, 10000),
          (position_set_z_to_ground_level, pos15),
          (position_get_z, ":cur_pos_z", pos15),
          (try_begin),
            (gt, ":cur_pos_z", ":highest_pos_z"),
            (copy_position, pos52, pos15),
            (assign, ":highest_pos_z", ":cur_pos_z"),
          (try_end),
        (try_end),
      (try_end),
  ]),

("calculate_team_powers",
     [
       (store_script_param, ":agent_no", 1),

       (try_begin),
         (assign, ":agent_side", 0),
         (agent_is_ally, ":agent_no"),
         (assign, ":agent_side", 1),
       (try_end),

       (assign, ":ally_power", 0),
       (assign, ":enemy_power", 0),

       (try_for_agents, ":cur_agent"),
         (agent_is_human, ":cur_agent"),
         (agent_is_alive, ":cur_agent"),

         (try_begin),
           (assign, ":agent_side_cur", 0),
           (agent_is_ally, ":cur_agent"),
           (assign, ":agent_side_cur", 1),
         (try_end),

         (try_begin),
           (agent_get_horse, ":agent_horse_id", ":cur_agent"),
           (neq, ":agent_horse_id", -1),
           (assign, ":agent_power", 2), #if this agent is horseman then his power effect is 2
         (else_try),
           (assign, ":agent_power", 1), #if this agent is walker then his power effect is 1
         (try_end),

         (try_begin),
           (eq, ":agent_side", ":agent_side_cur"),
           (val_add, ":ally_power", ":agent_power"),
         (else_try),
           (val_add, ":enemy_power", ":agent_power"),
         (try_end),
       (try_end),

       (assign, reg0, ":ally_power"),
       (assign, reg1, ":enemy_power"),
  ]),

("team_get_class_percentages",
    [
      (assign, ":num_infantry", 0),
      (assign, ":num_archers", 0),
      (assign, ":num_cavalry", 0),
      (assign, ":num_total", 0),
      (store_script_param, ":team_no", 1),
      (store_script_param, ":negate", 2),
      (try_for_agents,":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_team, ":agent_team", ":cur_agent"),
        (assign, ":continue", 0),
        (try_begin),
          (eq, ":negate", 1),
          (teams_are_enemies, ":agent_team", ":team_no"),
          (assign, ":continue", 1),
        (else_try),
          (eq, ":agent_team", ":team_no"),
          (assign, ":continue", 1),
        (try_end),
        (eq, ":continue", 1),
        (val_add, ":num_total", 1),
        (agent_get_class, ":agent_class", ":cur_agent"),
        (try_begin),
          (eq, ":agent_class", grc_infantry),
          (val_add,  ":num_infantry", 1),
        (else_try),
          (eq, ":agent_class", grc_archers),
          (val_add,  ":num_archers", 1),
        (else_try),
          (eq, ":agent_class", grc_cavalry),
          (val_add,  ":num_cavalry", 1),
        (try_end),
      (try_end),
      (try_begin),
        (eq,  ":num_total", 0),
        (assign,  ":num_total", 1),
      (try_end),
      (store_mul, ":perc_infantry",":num_infantry",100),
      (val_div, ":perc_infantry",":num_total"),
      (store_mul, ":perc_archers",":num_archers",100),
      (val_div, ":perc_archers",":num_total"),
      (store_mul, ":perc_cavalry",":num_cavalry",100),
      (val_div, ":perc_cavalry",":num_total"),
      (assign, reg0, ":perc_infantry"),
      (assign, reg1, ":perc_archers"),
      (assign, reg2, ":perc_cavalry"),
  ]),

("get_closest3_distance_of_enemies_at_pos1",
    [
      (assign, ":min_distance_1", 100000),
      (assign, ":min_distance_2", 100000),
      (assign, ":min_distance_3", 100000),

      (store_script_param, ":team_no", 1),
      (try_for_agents,":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_team, ":agent_team", ":cur_agent"),
        (teams_are_enemies, ":agent_team", ":team_no"),

        (agent_get_position, pos2, ":cur_agent"),
        (get_distance_between_positions,":cur_dist",pos2,pos1),
        (try_begin),
          (lt, ":cur_dist", ":min_distance_1"),
          (assign, ":min_distance_3", ":min_distance_2"),
          (assign, ":min_distance_2", ":min_distance_1"),
          (assign, ":min_distance_1", ":cur_dist"),
        (else_try),
          (lt, ":cur_dist", ":min_distance_2"),
          (assign, ":min_distance_3", ":min_distance_2"),
          (assign, ":min_distance_2", ":cur_dist"),
        (else_try),
          (lt, ":cur_dist", ":min_distance_3"),
          (assign, ":min_distance_3", ":cur_dist"),
        (try_end),
      (try_end),

      (assign, ":total_distance", 0),
      (assign, ":total_count", 0),
      (try_begin),
        (lt, ":min_distance_1", 100000),
        (val_add, ":total_distance", ":min_distance_1"),
        (val_add, ":total_count", 1),
      (try_end),
      (try_begin),
        (lt, ":min_distance_2", 100000),
        (val_add, ":total_distance", ":min_distance_2"),
        (val_add, ":total_count", 1),
      (try_end),
      (try_begin),
        (lt, ":min_distance_3", 100000),
        (val_add, ":total_distance", ":min_distance_3"),
        (val_add, ":total_count", 1),
      (try_end),
      (assign, ":average_distance", 100000),
      (try_begin),
        (gt, ":total_count", 0),
        (store_div, ":average_distance", ":total_distance", ":total_count"),
      (try_end),
      (assign, reg0, ":average_distance"),
      (assign, reg1, ":min_distance_1"),
      (assign, reg2, ":min_distance_2"),
      (assign, reg3, ":min_distance_3"),
  ]),

("team_get_average_position_of_enemies",
    [
      (store_script_param_1, ":team_no"),
      (init_position, pos0),
      (assign, ":num_enemies", 0),
      (assign, ":accum_x", 0),
      (assign, ":accum_y", 0),
      (assign, ":accum_z", 0),
      (try_for_agents,":enemy_agent"),
        (agent_is_alive, ":enemy_agent"),
        (agent_is_human, ":enemy_agent"),
        (agent_get_team, ":enemy_team", ":enemy_agent"),
        (teams_are_enemies, ":team_no", ":enemy_team"),

        (agent_get_position, pos62, ":enemy_agent"),

        (position_get_x, ":x", pos62),
        (position_get_y, ":y", pos62),
        (position_get_z, ":z", pos62),

        (val_add, ":accum_x", ":x"),
        (val_add, ":accum_y", ":y"),
        (val_add, ":accum_z", ":z"),
        (val_add, ":num_enemies", 1),
      (try_end),

      (try_begin), #to avoid division by zeros at below division part.
        (le, ":num_enemies", 0),
        (assign, ":num_enemies", 1),
      (try_end),

      (store_div, ":average_x", ":accum_x", ":num_enemies"),
      (store_div, ":average_y", ":accum_y", ":num_enemies"),
      (store_div, ":average_z", ":accum_z", ":num_enemies"),

      (position_set_x, pos0, ":average_x"),
      (position_set_y, pos0, ":average_y"),
      (position_set_z, pos0, ":average_z"),

      (assign, reg0, ":num_enemies"),
  ]),

("cf_team_get_average_position_of_agents_with_type_to_pos1",
    [
      (store_script_param_1, ":team_no"),
      (store_script_param_2, ":division_no"),
      (assign, ":total_pos_x", 0),
      (assign, ":total_pos_y", 0),
      (assign, ":total_pos_z", 0),
      (assign, ":num_agents", 0),
      (set_fixed_point_multiplier, 100),
      (try_for_agents, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_team, ":cur_team_no", ":cur_agent"),
        (eq, ":cur_team_no", ":team_no"),
        (agent_get_division, ":cur_agent_division", ":cur_agent"),
        (this_or_next|eq, ":division_no", grc_everyone),
        (eq, ":division_no", ":cur_agent_division"),
        (agent_get_position, pos1, ":cur_agent"),
        (position_get_x, ":cur_pos_x", pos1),
        (val_add, ":total_pos_x", ":cur_pos_x"),
        (position_get_y, ":cur_pos_y", pos1),
        (val_add, ":total_pos_y", ":cur_pos_y"),
        (position_get_z, ":cur_pos_z", pos1),
        (val_add, ":total_pos_z", ":cur_pos_z"),
        (val_add, ":num_agents", 1),
      (try_end),
      (gt, ":num_agents", 1),
      (val_div, ":total_pos_x", ":num_agents"),
      (val_div, ":total_pos_y", ":num_agents"),
      (val_div, ":total_pos_z", ":num_agents"),
      (init_position, pos1),
      (position_move_x, pos1, ":total_pos_x"),
      (position_move_y, pos1, ":total_pos_y"),
      (position_move_z, pos1, ":total_pos_z"),
  ]),

("field_start_position", [
      (store_script_param, ":fteam", 1),

      (assign, ":depth_cavalry", 0),
      (assign, ":largest_mounted_division_size", 0),
      (team_get_leader, ":fleader", ":fteam"),

      (try_begin),
        (ge, ":fleader", 0),
        (agent_get_position, pos2, ":fleader"),
      (else_try),
        (call_script, "script_battlegroup_get_position", pos2, ":fteam", grc_everyone),
      (try_end),

      (try_for_range, ":division", 0, 9),
        (store_add, ":slot", slot_team_d0_type, ":division"),
        (team_slot_eq, ":fteam", ":slot", sdt_cavalry),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_get_slot, reg0, ":fteam", ":slot"),
        (lt, ":largest_mounted_division_size", reg0),
        (assign, ":largest_mounted_division_size", reg0),
      (try_end),

      (try_begin),
        (gt, ":largest_mounted_division_size", 0),
        (val_mul, ":largest_mounted_division_size", 2),
        (convert_to_fixed_point, ":largest_mounted_division_size"),
        (store_sqrt, ":depth_cavalry", ":largest_mounted_division_size"),
        (convert_from_fixed_point, ":depth_cavalry"),
        (val_sub, ":depth_cavalry", 1),

        (store_mul, reg0, formation_start_spread_out, 50),
        (val_add, reg0, formation_minimum_spacing_horse_length),
        (val_mul, ":depth_cavalry", reg0),

        (store_mul, ":depth_infantry", formation_start_spread_out, 50),
        (val_add, ":depth_infantry", formation_minimum_spacing),
        (val_mul, ":depth_infantry", 2),
        (val_sub, ":depth_cavalry", ":depth_infantry"),

        (gt, ":depth_cavalry", 0),
        (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, ":fteam", grc_everyone),
        (call_script, "script_point_y_toward_position", pos2, Enemy_Team_Pos),
        (position_move_y, pos2, ":depth_cavalry"),
      (try_end),]),

("battlegroup_place_around_leader", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),

      (try_begin),
        (le, ":fleader", 0),
        (display_message, "@{!}script_battlegroup_place_around_leader: invalid leader agent (bad call)"),

      (else_try),
        (agent_get_group, reg0, ":fleader"),
        (neq, reg0, ":fteam"),
        (display_message, "@{!}script_battlegroup_place_around_leader: leader team mismatch (bad call)"),

      (else_try),
        (agent_get_position, pos1, ":fleader"),
        (call_script, "script_battlegroup_place_around_pos1", ":fteam", ":fdivision", ":fleader"),
      (try_end),]),

("battlegroup_place_around_pos1", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),

      (assign, ":store_fpm", 1),
      (convert_to_fixed_point, ":store_fpm"),
      (set_fixed_point_multiplier, 100),

      (store_sub, ":player_division", "$FormAI_player_in_division", 1),
      (try_begin),
        (eq, ":player_division", ":fdivision"),
        (assign, ":first_member_is_player", 1),
      (else_try),
        (assign, ":first_member_is_player", 0),
      (try_end),

      (try_begin),
        (eq, "$FormAI_autorotate", 1),
        (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, ":fteam", grc_everyone),
        (neq, reg0, 0),	#more than 0 enemies still alive?
        (call_script, "script_point_y_toward_position", pos1, Enemy_Team_Pos),
      (try_end),

      (store_add, ":slot", slot_team_d0_type, ":fdivision"),
      (team_get_slot, ":sd_type", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_size, ":fdivision"),
      (team_get_slot, ":num_troops", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation, ":fdivision"),
      (team_get_slot, ":fformation", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation_space, ":fdivision"),
      (team_get_slot, ":formation_extra_spacing", ":fteam", ":slot"),

      #handle memorized placement
      (try_begin),
        (eq, ":first_member_is_player", 0),
        (store_add, ":slot", slot_faction_d0_mem_relative_x_flag, ":fdivision"),
        (faction_get_slot, ":value", "fac_player_faction", ":slot"),	#only used for player now
        (neq, ":value", 0),

        (position_move_x, pos1, ":value", 0),
        (store_add, ":slot", slot_faction_d0_mem_relative_y, ":fdivision"),
        (faction_get_slot, ":value", "fac_player_faction", ":slot"),	#only used for player now
        (position_move_y, pos1, ":value", 0),
        (copy_position, pos61, pos1),
        (try_begin),
          (gt, ":fformation", formation_none),
          (try_begin),
            (this_or_next | eq, ":sd_type", sdt_cavalry),
            (eq, ":sd_type", sdt_harcher),
            (call_script, "script_form_cavalry", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", 0),
          (else_try),
            (eq, ":sd_type", sdt_archer),
            (call_script, "script_get_centering_amount", formation_default, ":num_troops", ":formation_extra_spacing"),
            (val_mul, reg0, -1),
            (position_move_x, pos1, reg0, 0),
            (call_script, "script_form_archers", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", 0, ":fformation"),
          (else_try),
            (call_script, "script_get_centering_amount", ":fformation", ":num_troops", ":formation_extra_spacing"),
            (position_move_x, pos1, reg0, 0),
            (call_script, "script_form_infantry", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", 0, ":fformation"),
          (try_end),
        (try_end),

      #default placement per division type
      (else_try),
        (this_or_next | eq, ":sd_type", sdt_cavalry),
        (eq, ":sd_type", sdt_harcher),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_x, pos1, "$next_cavalry_place", 0),
        (try_end),

        (try_begin),
          (gt, ":fformation", formation_none),
          (store_mul, ":troop_space", ":formation_extra_spacing", 50),
          (val_add, ":troop_space", formation_minimum_spacing_horse_width),
          (convert_to_fixed_point, ":num_troops"),
          (store_sqrt, ":formation_width", ":num_troops"),
          (val_mul, ":formation_width", ":troop_space"),
          (convert_from_fixed_point, ":formation_width"),
          (val_sub, ":formation_width", ":troop_space"),
          (store_div, reg0, ":formation_width", 2),
          (position_move_x, pos1, reg0, 0),	#cavalry set up RIGHT of leader
          (copy_position, pos61, pos1),
          (call_script, "script_form_cavalry", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player"),

        #handle Native's way of doing things
        (else_try),
          (store_mul, ":troop_space", ":formation_extra_spacing", 133),	#cm added by each Spread Out
          (val_add, ":troop_space", 150),	#minimum spacing

          #WFaS multi-ranks
          (try_begin),
            (eq, ":fformation", formation_2_row),
            (val_div, ":num_troops", 2),
          (else_try),
            (eq, ":fformation", formation_3_row),
            (val_div, ":num_troops", 3),
          (else_try),
            (eq, ":fformation", formation_4_row),
            (val_div, ":num_troops", 4),
          (else_try),
            (eq, ":fformation", formation_5_row),
            (val_div, ":num_troops", 5),

          (else_try),	#WB multi-ranks
            (lt, ":formation_extra_spacing", 0),
            (assign, ":troop_space", 200),
            (val_mul, ":formation_extra_spacing", -1),
            (val_add, ":formation_extra_spacing", 1),
            (val_div, ":num_troops", ":formation_extra_spacing"),
          (try_end),

          (store_mul, ":formation_width", ":num_troops", ":troop_space"),
          (store_div, reg0, ":formation_width", 2),
          (position_move_x, pos1, reg0, 0),	#cavalry set up RIGHT of leader
          (copy_position, pos61, pos1),
        (try_end),

        (try_begin),
          (eq, ":first_member_is_player", 0),
          (val_add, "$next_cavalry_place", ":formation_width"),
          (val_add, "$next_cavalry_place", formation_minimum_spacing_horse_width),
        (try_end),

      (else_try),
        (eq, ":sd_type", sdt_archer),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_y, pos1, "$next_archer_place"),	#archers set up FRONT of leader
          (val_add, "$next_archer_place", 500),	#next archers 5m FRONT of these
        (try_end),
        (copy_position, pos61, pos1),
        (try_begin),
          (gt, ":fformation", formation_none),
          (call_script, "script_get_centering_amount", formation_default, ":num_troops", ":formation_extra_spacing"),
          (val_mul, reg0, -1),
          (position_move_x, pos1, reg0, 0),
          (call_script, "script_form_archers", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player", ":fformation"),
        (try_end),

      (else_try),
        (eq, ":sd_type", sdt_skirmisher),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_y, pos1, "$next_archer_place"),	#skirmishers set up FRONT of leader
          (val_add, "$next_archer_place", 500),	#next archers 5m FRONT of these
        (try_end),
        (copy_position, pos61, pos1),
        (try_begin),
          (gt, ":fformation", formation_none),
          (call_script, "script_get_centering_amount", ":fformation", ":num_troops", ":formation_extra_spacing"),
          (position_move_x, pos1, reg0, 0),
          (call_script, "script_form_infantry", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player", ":fformation"),
        (try_end),

      (else_try),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_x, pos1, "$next_infantry_place", 0),
        (try_end),
        (copy_position, pos61, pos1),

        (try_begin),
          (gt, ":fformation", formation_none),
          (call_script, "script_form_infantry", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player", ":fformation"),
          (call_script, "script_get_centering_amount", ":fformation", ":num_troops", ":formation_extra_spacing"),
          (store_mul, ":formation_width", 2, reg0),
          (store_mul, ":troop_space", ":formation_extra_spacing", 50),
          (val_add, ":troop_space", formation_minimum_spacing),
          (val_add, ":formation_width", ":troop_space"),
          (val_mul, reg0, -1),	#infantry set up LEFT of leader
          (position_move_x, pos61, reg0, 0),

        #handle Native's way of doing things
        (else_try),
          (store_mul, ":troop_space", ":formation_extra_spacing", 75),	#Native minimum spacing not consistent but less than this
          (val_add, ":troop_space", 100),	#minimum spacing

          #WFaS multi-ranks
          (try_begin),
            (eq, ":fformation", formation_2_row),
            (val_div, ":num_troops", 2),
          (else_try),
            (eq, ":fformation", formation_3_row),
            (val_div, ":num_troops", 3),
          (else_try),
            (eq, ":fformation", formation_4_row),
            (val_div, ":num_troops", 4),
          (else_try),
            (eq, ":fformation", formation_5_row),
            (val_div, ":num_troops", 5),

          (else_try),	#WB multi-ranks
            (lt, ":formation_extra_spacing", 0),
            (assign, ":troop_space", 150),
            (val_mul, ":formation_extra_spacing", -1),
            (val_add, ":formation_extra_spacing", 1),
            (val_div, ":num_troops", ":formation_extra_spacing"),
          (try_end),

          (store_mul, ":formation_width", ":num_troops", ":troop_space"),
          (store_div, reg0, ":formation_width", 2),
          (val_mul, reg0, -1),	#infantry set up LEFT of leader
          (position_move_x, pos61, reg0, 0),
        (try_end),

        (try_begin),
          (eq, ":first_member_is_player", 0),
          (val_sub, "$next_infantry_place", ":formation_width"),	#next infantry 1m LEFT of these
          (val_sub, "$next_infantry_place", 100),
        (try_end),
      (try_end),

      (store_add, ":slot", slot_team_d0_move_order, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", mordr_hold),
      (set_show_messages, 0),
      (team_get_movement_order, reg0, ":fteam", ":fdivision"),
      (try_begin),
        (neq, reg0, mordr_hold),
        (team_give_order, ":fteam", ":fdivision", mordr_hold),
      (try_end),
      (call_script, "script_set_formation_destination", ":fteam", ":fdivision", pos61),
      (set_show_messages, 1),
      (set_fixed_point_multiplier, ":store_fpm"),]),

("calculate_default_ranks", [
      (store_script_param, ":bg_size", 1),

      (val_mul, ":bg_size", 20),
      (val_sub, ":bg_size", 25),
      (convert_to_fixed_point, ":bg_size"),
      (store_sqrt, reg1, ":bg_size"),
      (convert_from_fixed_point, reg1),
      (val_sub, reg1, 5),
      (val_div, reg1, 10),
      (val_add, reg1, 1),]),

("get_centering_amount", [
      (store_script_param, ":troop_formation", 1),
      (store_script_param, ":num_troops", 2),
      (store_script_param, ":extra_spacing", 3),
      (store_mul, ":troop_space", ":extra_spacing", 50),
      (val_add, ":troop_space", formation_minimum_spacing),
      (assign, reg0, 0),
      (try_begin),
        (eq, ":troop_formation", formation_square),
        (convert_to_fixed_point, ":num_troops"),
        (store_sqrt, reg0, ":num_troops"),
        (convert_from_fixed_point, reg0),
        (val_mul, reg0, ":troop_space"),
        # (val_sub, reg0, ":troop_space"), MOTO not needed because column added in
        # script_form_infantry
      (else_try),
        (this_or_next | eq, ":troop_formation", formation_ranks),
        (eq, ":troop_formation", formation_shield),
        (call_script, "script_calculate_default_ranks", ":num_troops"),
        (assign, ":num_ranks", reg1),
        (store_div, reg0, ":num_troops", ":num_ranks"),
        (try_begin),
          (store_mod, reg1, ":num_troops", ":num_ranks"),
          (eq, reg1, 0),
          (val_sub, reg0, 1),
        (try_end),
        (val_mul, reg0, ":troop_space"),
      (else_try),
        (eq, ":troop_formation", formation_default),	#assume these are archers in a line
        (store_mul, reg0, ":num_troops", ":troop_space"),
      (try_end),
      (val_div, reg0, 2),]),

("memorize_division_placements", [
      (set_fixed_point_multiplier, 100),
      (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, "$fplayer_team_no", grc_everyone),
      (assign, ":num_enemies", reg0),

      (try_for_range, ":division", 0, 9),
        (class_is_listening_order, "$fplayer_team_no", ":division"),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_ge, "$fplayer_team_no", ":slot", 1),

        (store_add, ":slot", slot_team_d0_formation, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (store_add, ":slot", slot_faction_d0_mem_formation, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),

        (store_add, ":slot", slot_team_d0_formation_space, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (store_add, ":slot", slot_faction_d0_mem_formation_space, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),

        (agent_get_position, pos1, "$fplayer_agent_no"),
        (try_begin),
          (neq, ":num_enemies", 0),	#more than 0 enemies still alive?
          (call_script, "script_point_y_toward_position", pos1, Enemy_Team_Pos),
        (try_end),
        # (call_script, "script_get_formation_destination", Current_Pos,
        # "$fplayer_team_no", ":division"),
        (team_get_order_position, Current_Pos, "$fplayer_team_no", ":division"),	#use this to capture Native Advance and Fall Back positioning
        (position_transform_position_to_local, Temp_Pos, pos1, Current_Pos), #Temp_Pos = vector to division w.r.t.  leader facing enemy

        (position_get_x, ":value", Temp_Pos),
        (store_add, ":slot", slot_faction_d0_mem_relative_x_flag, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),

        (position_get_y, ":value", Temp_Pos),
        (store_add, ":slot", slot_faction_d0_mem_relative_y, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),

        (store_add, ":slot", slot_team_d0_type, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (call_script, "script_str_store_division_type_name", s1, ":value"),
        (store_add, reg0, ":division", 1),
        (display_message, "@The placement of {s1} division {reg0} memorized."),
      (try_end),]),

("default_division_placements", [
      (try_for_range, ":division", 0, 9),
        (class_is_listening_order, "$fplayer_team_no", ":division"),
        (store_add, ":slot", slot_faction_d0_mem_relative_x_flag, ":division"),	#use as flag
        (faction_set_slot, "fac_player_faction", ":slot", 0),

        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_ge, "$fplayer_team_no", ":slot", 1),
        (store_add, ":slot", slot_team_d0_type, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (call_script, "script_str_store_division_type_name", s1, ":value"),
        (store_add, reg0, ":division", 1),
        (display_message, "@The placement of {s1} division {reg0} set to default."),
      (try_end),]),

("process_place_divisions", [
      (assign, ":num_bgroups", 0),
      (try_for_range, ":division", 0, 9),
        (class_is_listening_order, "$fplayer_team_no", ":division"),
        (store_add, ":slot", slot_team_d0_target_team, ":division"),
        (team_set_slot, "$fplayer_team_no", ":slot", -1),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_ge, "$fplayer_team_no", ":slot", 1),
        (store_add, ":slot", slot_team_d0_fclock, ":division"),
        (team_set_slot, "$fplayer_team_no", ":slot", 1),
        (team_get_order_position, pos1, "$fplayer_team_no", ":division"),
        (val_add, ":num_bgroups", 1),
      (try_end),

      (try_begin),
        (gt, ":num_bgroups", 0),
        (copy_position, Target_Pos, pos1),	#kludge around team_get_order_position rotation problems

        (try_begin),
          (eq, "$battle_phase", BP_Deploy),

          (try_begin),
            (eq, "$g_is_quick_battle", 1),
            (assign, reg0, 5),
          (else_try),
            (party_get_skill_level, reg0, "p_main_party", "skl_tactics"),
          (try_end),
          (store_mul, ":range_limit", reg0, 1000),

          (agent_get_position, Temp_Pos, "$fplayer_agent_no"),
          (get_distance_between_positions, reg0, Target_Pos, Temp_Pos),
          (lt, ":range_limit", reg0),
          (display_message, "@Your party's tactical skill limits how far away you can deploy your troops!"),
          (call_script, "script_point_y_toward_position", Temp_Pos, Target_Pos),
          (copy_position, Target_Pos, Temp_Pos),
          (position_move_y, Target_Pos, ":range_limit"),
        (try_end),

        #player designating target battlegroup?
        (assign, ":distance_to_enemy", Far_Away),
        (try_for_range, ":team", 0, 4),
          (teams_are_enemies, ":team", "$fplayer_team_no"),
          (team_slot_ge, ":team", slot_team_size, 1),
          (try_for_range, ":division", 0, 9),
            (store_add, ":slot", slot_team_d0_size, ":division"),
            (team_slot_ge, ":team", ":slot", 1),
            (call_script, "script_battlegroup_get_position", Temp_Pos, ":team", ":division"),
            (get_distance_between_positions, reg0, Target_Pos, Temp_Pos),
            (gt, ":distance_to_enemy", reg0),
            (assign, ":distance_to_enemy", reg0),
            (assign, ":closest_enemy_team", ":team"),
            (assign, ":closest_enemy_division", ":division"),
          (try_end),
        (try_end),

        (call_script, "script_battlegroup_get_action_radius", ":closest_enemy_team", ":closest_enemy_division"),
        (assign, ":radius_enemy_battlegroup", reg0),

        (try_begin),
          (le, ":distance_to_enemy", ":radius_enemy_battlegroup"),	#target position within radius of an enemy battlegroup?
          (le, ":distance_to_enemy", AI_charge_distance),	#limit so player can place divisions near large enemy battlegroups without
          #selecting them
          (call_script, "script_battlegroup_get_position", Target_Pos, ":closest_enemy_team", ":closest_enemy_division"),
          (gt, ":num_bgroups", 1),
          (store_add, ":slot", slot_team_d0_type, ":closest_enemy_division"),
          (team_get_slot, reg0, ":closest_enemy_team", ":slot"),
          (call_script, "script_str_store_division_type_name", s1, reg0),
          (display_message, "@...and attack enemy {s1} division!"),
        (try_end),

        (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, "$fplayer_team_no", grc_everyone),
        (call_script, "script_point_y_toward_position", Target_Pos, Enemy_Team_Pos),

        #place player divisions
        (agent_get_position, pos49, "$fplayer_agent_no"),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
          (gt, ":troop_count", 0),

          (try_begin),
            (le, ":distance_to_enemy", ":radius_enemy_battlegroup"),	#target position within radius of an enemy battlegroup?
            (le, ":distance_to_enemy", AI_charge_distance),	#limit so player can place divisions near large enemy battlegroups without
            #selecting them
            (store_add, ":slot", slot_team_d0_target_team, ":division"),
            (team_set_slot, "$fplayer_team_no", ":slot", ":closest_enemy_team"),
            (store_add, ":slot", slot_team_d0_target_division, ":division"),
            (team_set_slot, "$fplayer_team_no", ":slot", ":closest_enemy_division"),
          (try_end),

          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":fformation", "$fplayer_team_no", ":slot"),

          (try_begin),
            (gt, ":num_bgroups", 1),
            (agent_set_position, "$fplayer_agent_no", Target_Pos),	#fake out script_battlegroup_place_around_leader
            (call_script, "script_player_attempt_formation", ":division", ":fformation", 0),
          (else_try),
            (try_begin),
              (le, ":distance_to_enemy", ":radius_enemy_battlegroup"),	#target position within radius of an enemy battlegroup?
              (le, ":distance_to_enemy", AI_charge_distance),	#limit so player can place divisions near large enemy battlegroups without
              #selecting them
              (call_script, "script_battlegroup_get_attack_destination", Target_Pos, "$fplayer_team_no", ":division", ":closest_enemy_team", ":closest_enemy_division"),
              (store_add, ":slot", slot_team_d0_type, ":closest_enemy_division"),
              (team_get_slot, reg0, ":closest_enemy_team", ":slot"),
              (call_script, "script_str_store_division_type_name", s1, reg0),
              (display_message, "@...and attack enemy {s1} division!"),
            (try_end),

            (call_script, "script_set_formation_destination", "$fplayer_team_no", ":division", Target_Pos),

            (gt, ":fformation", formation_none),
            (store_add, ":slot", slot_team_d0_formation_space, ":division"),
            (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
            (try_begin),
              (store_add, ":slot", slot_team_d0_type, ":division"),
              (team_get_slot, ":sd_type", "$fplayer_team_no", ":slot"),
              (neq, ":sd_type", sdt_cavalry),
              (neq, ":sd_type", sdt_harcher),
              (try_begin),
                (eq, ":sd_type", sdt_archer),
                (call_script, "script_get_centering_amount", formation_default, ":troop_count", ":div_spacing"),
                (val_mul, reg0, -1),
                (assign, ":script", "script_form_archers"),
              (else_try),
                (call_script, "script_get_centering_amount", ":fformation", ":troop_count", ":div_spacing"),
                (assign, ":script", "script_form_infantry"),
              (try_end),
              (position_move_x, Target_Pos, reg0),
            (else_try),
              (assign, ":script", "script_form_cavalry"),
            (try_end),
            (copy_position, pos1, Target_Pos),
            (call_script, ":script", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0, ":fformation"),
          (try_end),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", mordr_hold),
        (try_end), #division loop
        (agent_set_position, "$fplayer_agent_no", pos49),
      (try_end),	#num_bgroups > 0
  ]),

("process_player_division_positioning", [
      (call_script, "script_division_reset_places"),

      #implement HOLD OVER THERE when player lets go of key
      (try_begin),
        (ge, "$gk_order_hold_over_there", HOT_F1_held),
        (neg | game_key_is_down, gk_order_1),
        (assign, "$gk_order_hold_over_there", HOT_no_order),
        (call_script, "script_process_place_divisions"),
      (try_end),	#HOLD OVER THERE

      #periodic functions
      (assign, ":save_autorotate", "$FormAI_autorotate"),
      (assign, "$FormAI_autorotate", 0),
      (try_for_range, ":division", 0, 9),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
        (gt, ":troop_count", 0),

        (store_add, ":slot", slot_team_d0_target_team, ":division"),
        (team_get_slot, ":target_team", "$fplayer_team_no", ":slot"),
        (store_add, ":slot", slot_team_d0_target_division, ":division"),
        (team_get_slot, ":target_division", "$fplayer_team_no", ":slot"),
        (try_begin),
          (ge, ":target_team", 0),	#enemy battlegroup targeted?
          (store_add, ":slot", slot_team_d0_size, ":target_division"),
          (team_get_slot, reg0, ":target_team", ":slot"),

          (le, reg0, 0),	#target destroyed?
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),

          (store_add, ":slot", slot_team_d0_type, ":target_division"),
          (team_get_slot, reg0, ":target_team", ":slot"),
          (call_script, "script_str_store_division_type_name", s1, reg0),

          (str_store_class_name, s2, ":division"),
          (display_message, "@{s2}: returning after destroying enemy {s1} division."),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", mordr_follow),
        (try_end),

        (store_add, ":slot", slot_team_d0_fclock, ":division"),
        (team_get_slot, ":fclock", "$fplayer_team_no", ":slot"),
        (store_mod, ":time_slice", ":fclock", Reform_Trigger_Modulus),
        (val_add, ":fclock", 1),
        (team_set_slot, "$fplayer_team_no", ":slot", ":fclock"),

        (try_begin),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_slot_eq, "$fplayer_team_no", ":slot", mordr_follow),
          (call_script, "script_battlegroup_place_around_leader", "$fplayer_team_no", ":division", "$fplayer_agent_no"),
          (team_set_slot, "$fplayer_team_no", ":slot", mordr_follow),	#override script_battlegroup_place_around_leader

        #periodically reform
        (else_try),
          (eq, ":time_slice", 0),
          (team_get_movement_order, reg0, "$fplayer_team_no", ":division"),
          (neq, reg0, mordr_stand_ground),

          (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, "$fplayer_team_no", grc_everyone),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":fformation", "$fplayer_team_no", ":slot"),
          (try_begin),
            (gt, ":fformation", formation_none),
            (store_add, ":slot", slot_team_d0_formation_space, ":division"),
            (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
            (store_add, ":slot", slot_team_d0_type, ":division"),
            (team_get_slot, ":sd_type", "$fplayer_team_no", ":slot"),

            (try_begin),
              (store_add, ":slot", slot_team_d0_first_member, ":division"),
              (team_slot_eq, "$fplayer_team_no", ":slot", "$fplayer_agent_no"),
              (assign, ":first_member_is_player", 1),
            (else_try),
              (assign, ":first_member_is_player", 0),
            (try_end),

            (try_begin),
              (ge, ":target_team", 0),	#enemy battlegroup targeted?
              (try_begin),
                (this_or_next | eq, ":sd_type", sdt_archer),
                (this_or_next | eq, ":sd_type", sdt_harcher),
                (eq, ":sd_type", sdt_skirmisher),
                (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
                (team_slot_ge, "$fplayer_team_no", ":slot", 1),	#ranged are firing?
                (call_script, "script_formation_current_position", pos1, "$fplayer_team_no", ":division"),	#stop advancing
              (else_try),
                (call_script, "script_battlegroup_get_attack_destination", pos1, "$fplayer_team_no", ":division", ":target_team", ":target_division"),
              (try_end),

            (else_try),
              (call_script, "script_get_formation_destination", pos1, "$fplayer_team_no", ":division"),
              (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
              (team_get_slot, ":is_fighting", "$fplayer_team_no", ":slot"),
              (try_begin),
                (neq, ":sd_type", sdt_cavalry),
                (neq, ":sd_type", sdt_harcher),
                (neq, ":is_fighting", 0),
                (eq, ":first_member_is_player", 0),
                (position_move_y, pos1, -2000),
              (try_end),
              (call_script, "script_point_y_toward_position", pos1, Enemy_Team_Pos),
              (try_begin),
                (neq, ":sd_type", sdt_cavalry),
                (neq, ":sd_type", sdt_harcher),
                (neq, ":is_fighting", 0),
                (eq, ":first_member_is_player", 0),
                (position_move_y, pos1, 2000),
              (try_end),
            (try_end),

            (call_script, "script_set_formation_destination", "$fplayer_team_no", ":division", pos1),

            (try_begin),
              (eq, ":sd_type", sdt_archer),
              (call_script, "script_get_centering_amount", formation_default, ":troop_count", ":div_spacing"),
              (val_mul, reg0, -1),
              (position_move_x, pos1, reg0),
            (else_try),
              (neq, ":sd_type", sdt_cavalry),
              (neq, ":sd_type", sdt_harcher),
              (call_script, "script_get_centering_amount", ":fformation", ":troop_count", ":div_spacing"),
              (position_move_x, pos1, reg0),
            (try_end),

            (try_begin),
              (eq, ":sd_type", sdt_archer),
              (call_script, "script_form_archers", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":fformation"),
            (else_try),
              (this_or_next | eq, ":sd_type", sdt_cavalry),
              (eq, ":sd_type", sdt_harcher),
              (try_begin),
                (ge, ":target_team", 0),	#enemy battlegroup targeted?
                (call_script, "script_formation_current_position", pos29, "$fplayer_team_no", ":division"),
                (call_script, "script_battlegroup_get_position", Enemy_Team_Pos, ":target_team", ":target_division"),
                (get_distance_between_positions, ":distance_to_enemy", pos29, Enemy_Team_Pos),

                (call_script, "script_battlegroup_get_action_radius", "$fplayer_team_no", ":division"),
                (assign, ":combined_radius", reg0),
                (call_script, "script_battlegroup_get_action_radius", ":target_team", ":target_division"),
                (val_add, ":combined_radius", reg0),

                (le, ":distance_to_enemy", ":combined_radius"),
                (call_script, "script_formation_end", "$fplayer_team_no", ":division"),
                (str_store_class_name, s1, ":division"),
                (display_message, "@{s1}: cavalry formation disassembled."),
                (set_show_messages, 0),
                (team_give_order, "$fplayer_team_no", ":division", mordr_charge),
                (set_show_messages, 1),
              (else_try),
                (call_script, "script_form_cavalry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player"),
              (try_end),
            (else_try),
              (call_script, "script_form_infantry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":fformation"),
            (try_end),

          (else_try),	#divisions not in formation
            (ge, ":target_team", 0),	#enemy battlegroup targeted?
            (store_add, ":slot", slot_team_d0_target_division, ":division"),
            (team_get_slot, ":target_division", "$fplayer_team_no", ":slot"),
            (try_begin),
              (this_or_next | eq, ":sd_type", sdt_archer),
              (this_or_next | eq, ":sd_type", sdt_harcher),
              (eq, ":sd_type", sdt_skirmisher),
              (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
              (team_slot_ge, "$fplayer_team_no", ":slot", 1),	#ranged are firing?
              (call_script, "script_battlegroup_get_position", pos1, "$fplayer_team_no", ":division"),	#stop advancing
            (else_try),
              (call_script, "script_battlegroup_get_attack_destination", pos1, "$fplayer_team_no", ":division", ":target_team", ":target_division"),
            (try_end),
            (call_script, "script_set_formation_destination", "$fplayer_team_no", ":division", pos1),
            (team_get_movement_order, ":existing_order", "$fplayer_team_no", ":division"),
            (try_begin),
              (ge, ":target_team", 0),	#enemy battlegroup targeted?
              (call_script, "script_battlegroup_get_position", pos29, "$fplayer_team_no", ":division"),
              (call_script, "script_battlegroup_get_position", Enemy_Team_Pos, ":target_team", ":target_division"),
              (get_distance_between_positions, ":distance_to_enemy", pos29, Enemy_Team_Pos),

              (call_script, "script_battlegroup_get_action_radius", "$fplayer_team_no", ":division"),
              (assign, ":combined_radius", reg0),
              (call_script, "script_battlegroup_get_action_radius", ":target_team", ":target_division"),
              (val_add, ":combined_radius", reg0),

              (le, ":distance_to_enemy", ":combined_radius"),
              (try_begin),
                (neq, ":existing_order", mordr_charge),
                (set_show_messages, 0),
                (team_give_order, "$fplayer_team_no", ":division", mordr_charge),
                (set_show_messages, 1),
              (try_end),
            (else_try),
              (neq, ":existing_order", mordr_hold),
              (set_show_messages, 0),
              (team_give_order, "$fplayer_team_no", ":division", mordr_hold),
              (set_show_messages, 1),
            (try_end),
          (try_end),
        (try_end),	#Periodic Reform
      (try_end),	#Division Loop

      (assign, "$FormAI_autorotate", ":save_autorotate"),]),

("point_y_toward_position", [
      (store_script_param, ":from_position", 1),
      (store_script_param, ":to_position", 2),
      (assign, ":save_fpm", 1),
      (convert_to_fixed_point, ":save_fpm"),
      (set_fixed_point_multiplier, 100),  #to match cm returned by get_distance_between_positions

      #remove current rotation
      (position_get_x, ":from_x", ":from_position"),
      (position_get_y, ":from_y", ":from_position"),
      (position_get_z, ":from_z", ":from_position"),
      (init_position, ":from_position"),
      (position_set_x, ":from_position", ":from_x"),
      (position_set_y, ":from_position", ":from_y"),
      (position_set_z, ":from_position", ":from_z"),

      #horizontal rotation
      (position_get_x, ":change_in_x", ":to_position"),
      (val_sub, ":change_in_x", ":from_x"),
      (position_get_y, ":change_in_y", ":to_position"),
      (val_sub, ":change_in_y", ":from_y"),

      (try_begin),
        (this_or_next | neq, ":change_in_y", 0),
        (neq, ":change_in_x", 0),
        (store_atan2, ":theta", ":change_in_y", ":change_in_x"),
        (assign, ":ninety", 90),
        (convert_to_fixed_point, ":ninety"),
        (val_sub, ":theta", ":ninety"),	#point Y axis at to position
        (position_rotate_z_floating, ":from_position", ":theta"),
      (try_end),

      #vertical rotation
      (get_distance_between_positions, ":distance_between", ":from_position", ":to_position"),
      (try_begin),
        (gt, ":distance_between", 0),
        (position_get_z, ":dist_z_to_sine", ":to_position"),
        (val_sub, ":dist_z_to_sine", ":from_z"),
        (val_div, ":dist_z_to_sine", ":distance_between"),
        (store_asin, ":theta", ":dist_z_to_sine"),
        (position_rotate_x_floating, ":from_position", ":theta"),
      (try_end),

      (assign, reg0, ":distance_between"),
      (set_fixed_point_multiplier, ":save_fpm"),]),

("store_battlegroup_type", [
      (store_script_param_1, ":fteam"),
      (store_script_param_2, ":fdivision"),

      (assign, ":count_infantry", 0),
      (assign, ":count_archer", 0),
      (assign, ":count_cavalry", 0),
      (assign, ":count_harcher", 0),
      (assign, ":count_polearms", 0),
      (assign, ":count_skirmish", 0),
      (assign, ":count_support", 0),
      (assign, ":count_bodyguard", 0),

      (team_get_leader, ":leader", ":fteam"),

      (try_for_agents, ":cur_agent"),
        (call_script, "script_cf_valid_formation_member", ":fteam", ":fdivision", ":leader", ":cur_agent"),
        (agent_get_troop_id, ":cur_troop", ":cur_agent"),
        (agent_get_ammo, ":cur_ammo", ":cur_agent", 0),

        (try_begin),
          (neg | troop_is_hero, ":cur_troop"),
          (try_begin), #Cavalry
            (agent_get_horse, reg0, ":cur_agent"),
            (ge, reg0, 0),
            (try_begin),
              (ge, ":cur_ammo", minimum_ranged_ammo),
              (val_add, ":count_harcher", 1),
            (else_try),
              (val_add, ":count_cavalry", 1),
            (try_end),
          (else_try), #Archers
            (ge, ":cur_ammo", minimum_ranged_ammo),
            # #use when troops are equipped with ranged at start of battle
            # (agent_get_class, ":bgclass", ":cur_agent"),
            # (eq, ":bgclass", grc_archers),
            # #end use when troops equipped with ranged at start of battle
            (assign, ":end", ek_head),
            (try_for_range, ":i", ek_item_0, ":end"),
              (agent_get_item_slot, ":item", ":cur_agent", ":i"),
              (gt, ":item", 0),
              (item_get_type, ":weapontype", ":item"),
              (is_between, ":weapontype", itp_type_bow, itp_type_thrown),  # bow or crossbow
              (assign, ":end", ek_item_0), #loop Break
            (try_end),
            (try_begin),
              (eq, ":end", ek_head), #failed to find bow or crossbow
              (val_add, ":count_skirmish", 1),
            (else_try),
              (val_add, ":count_archer", 1),
            (try_end),
          (else_try), #Infantry
            (assign, ":end", ek_head),
            (try_for_range, ":i", ek_item_0, ":end"),
              (agent_get_item_slot, ":item", ":cur_agent", ":i"),
              (call_script, "script_cf_is_thrusting_weapon", ":item"),
              (item_get_type, ":weapontype", ":item"),
              (eq, ":weapontype", itp_type_polearm),
              (assign, ":end", ek_item_0), #loop Break
            (try_end),
            (try_begin),
              (eq, ":end", ek_head), #failed to find a polearm
              (val_add, ":count_infantry", 1),
            (else_try),
              (val_add, ":count_polearms", 1),
            (try_end),
          (try_end),
        (else_try), #Heroes
          (assign, ":support_skills", 0), #OPEN TO SUGGESTIONS HERE ?skl_trade, skl_spotting, skl_pathfinding,
          #skl_tracking?
          (store_skill_level, reg0, skl_engineer, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (store_skill_level, reg0, skl_first_aid, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (store_skill_level, reg0, skl_surgery, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (store_skill_level, reg0, skl_wound_treatment, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (try_begin),
            (gt, ":support_skills", 5),
            (val_add, ":count_support", 1),
          (else_try),
            (val_add, ":count_bodyguard", 1),
          (try_end),
        (try_end), #Regular v Hero
      (try_end), #Agent Loop

      #Do Comparisons With Counts, set ":div_type"
      (assign, ":slot", slot_team_d0_type),
      (team_set_slot, scratch_team, ":slot", ":count_infantry"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_archer"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_cavalry"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_polearms"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_skirmish"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_harcher"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_support"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_bodyguard"),

      (assign, ":count_to_beat", 0),
      (assign, ":count_total", 0),
      (try_for_range, ":type", sdt_infantry, sdt_infantry + 8), #only 8 sdt_types at the moment
        (store_add, ":slot", slot_team_d0_type, ":type"),
        (team_get_slot, ":count", scratch_team, ":slot"),
        (val_add, ":count_total", ":count"),
        (lt, ":count_to_beat", ":count"),
        (assign, ":count_to_beat", ":count"),
        (assign, ":div_type", ":type"),
      (try_end),

      (val_mul, ":count_to_beat", 2),
      (try_begin),
        (lt, ":count_to_beat", ":count_total"), #Less than half of this division
        (assign, ":count_to_beat", 0),
        (assign, ":div_type", -1),
        (try_for_range, ":type", sdt_infantry, sdt_infantry + 3), #check main types for a majority
          (store_add, ":slot", slot_team_d0_type, ":type"),
          (team_get_slot, ":count", scratch_team, ":slot"),
          (val_add, ":slot", 3),	#subtype is three more than main type
          (team_get_slot, reg0, scratch_team, ":slot"),
          (val_add, ":count", reg0),
          (lt, ":count_to_beat", ":count"),
          (assign, ":count_to_beat", ":count"),
          (assign, ":div_type", ":type"),
        (try_end),

        (val_mul, ":count_to_beat", 2),
        (lt, ":count_to_beat", ":count_total"), #Less than half of this division
        (assign, ":div_type", sdt_unknown), #Or 0
      (try_end),

      #hard-code traditional infantry division (avoid player confusion for mods
      #which arm troops with ranged at start of battle)
      (try_begin),
        (eq, ":fdivision", grc_infantry),
        (neq, ":div_type", sdt_polearm),
        (assign, ":div_type", sdt_infantry),
      (try_end),

      (store_add, ":slot", slot_team_d0_type, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", ":div_type"),
      (assign, reg0, ":div_type"),]),

("store_battlegroup_data", [
      (assign, ":team0_leader", 0),
      (assign, ":team0_x_leader", 0),
      (assign, ":team0_y_leader", 0),
      (assign, ":team0_zrot_leader", 0),
      (assign, ":team0_level_leader", 0),
      (assign, ":team1_leader", 0),
      (assign, ":team1_x_leader", 0),
      (assign, ":team1_y_leader", 0),
      (assign, ":team1_zrot_leader", 0),
      (assign, ":team1_level_leader", 0),
      (assign, ":team2_leader", 0),
      (assign, ":team2_x_leader", 0),
      (assign, ":team2_y_leader", 0),
      (assign, ":team2_zrot_leader", 0),
      (assign, ":team2_level_leader", 0),
      (assign, ":team3_leader", 0),
      (assign, ":team3_x_leader", 0),
      (assign, ":team3_y_leader", 0),
      (assign, ":team3_zrot_leader", 0),
      (assign, ":team3_level_leader", 0),

      #save some info
      (try_for_range, ":division", 0, 9),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (try_begin),
          (team_slot_ge, "$fplayer_team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_exists, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),

        (else_try),
          (store_add, ":slot", slot_team_d0_exists, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 0),
        (try_end),
      (try_end),

      #Team Slots reset every mission, like agent slots, but just to be sure for
      #when it gets called during the mission
      (try_for_range, ":slot", reset_team_stats_begin, reset_team_stats_end), #Those within the "RESET GROUP" in formations_constants
        (try_for_range, ":team", 0, 4),
          (team_set_slot, ":team", ":slot", 0),
        (try_end),
      (try_end),

      (try_for_agents, ":cur_agent"),
        (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, -1),

        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_slot_eq, ":cur_agent", slot_agent_is_running_away, 0),

        (agent_get_group, ":bgteam", ":cur_agent"),
        (agent_get_division, ":bgdivision", ":cur_agent"),
        (agent_get_class, ":agent_class", ":cur_agent"),
        (agent_get_position, pos1, ":cur_agent"),

        (try_begin),
          (agent_is_non_player, ":cur_agent"),

          (store_add, ":slot", slot_team_d0_type, ":bgdivision"),
          (team_get_slot, ":bgtype", ":bgteam", ":slot"),
          (this_or_next | eq, ":bgtype", sdt_cavalry),	#assigned to horsed division
          (eq, ":bgtype", sdt_harcher),

          (team_get_riding_order, reg0, ":bgteam", ":bgdivision"),
          (neq, reg0, rordr_dismount),

          (team_get_order_position, pos0, ":bgteam", ":bgdivision"),
          (get_distance_between_positions, ":old_distance", pos0, pos1),
          (gt, ":old_distance", AI_charge_distance),	#agent is out of formation?

          (assign, ":target_type", ":bgtype"),

          (try_begin),
            (eq, ":agent_class", grc_infantry),	#Native has transferred this agent to infantry
            (assign, ":target_type", sdt_infantry),

            (try_for_range, ":item_slot", ek_item_0, ek_head),
              (eq, ":bgteam", "$fplayer_team_no"),	#AI doesn't use extended right now
              (agent_get_item_slot, ":item", ":cur_agent", ":item_slot"),
              (call_script, "script_cf_is_thrusting_weapon", ":item"),
              (item_get_type, reg0, ":item"),
              (eq, reg0, itp_type_polearm),
              (assign, ":target_type", sdt_polearm),
            (try_end),

          (else_try),
            (eq, ":agent_class", grc_archers),	#Native has transferred this agent to archers
            (assign, ":target_type", sdt_archer),

            (try_for_range, ":item_slot", ek_item_0, ek_head),
              (eq, ":bgteam", "$fplayer_team_no"),	#AI doesn't use extended right now
              (agent_get_item_slot, ":item", ":cur_agent", ":item_slot"),
              (call_script, "script_cf_is_weapon_ranged", ":item", 1),
              (agent_get_ammo, reg1, ":cur_agent", 0),
              (ge, reg1, minimum_ranged_ammo),  #more than two to throw on a charge?
              (item_get_type, reg0, ":item"),
              (eq, reg0, itp_type_thrown),
              (assign, ":target_type", sdt_skirmisher),
            (try_end),
          (try_end),

          (neq, ":target_type", ":bgtype"),
          (assign, ":bgdivision", ":target_type"),

          (try_for_range_backwards, ":new_division", 0, 9),
            (store_add, ":slot", slot_team_d0_size, ":new_division"),
            (team_get_slot, reg0, ":bgteam", ":slot"),
            (gt, reg0, 0),

            (store_add, ":slot", slot_team_d0_type, ":new_division"),
            (team_get_slot, reg0, ":bgteam", ":slot"),
            (eq, reg0, ":target_type"),

            (assign, ":bgdivision", ":new_division"),
          (try_end),

          (try_begin),
            (store_add, ":slot", slot_team_d0_exists, ":bgdivision"),
            (team_slot_eq, "$fplayer_team_no", ":slot", 0),	#division does not yet exist?
            (agent_is_alive, "$fplayer_agent_no"),
            (store_add, ":slot", slot_team_d0_move_order, ":bgdivision"),
            (neg | team_slot_eq, "$fplayer_team_no", ":slot", mordr_follow),
            (team_set_slot, "$fplayer_team_no", ":slot", mordr_follow),
            (set_show_messages, 0),
            (team_give_order, "$fplayer_team_no", ":bgdivision", mordr_follow),
            (set_show_messages, 1),
          (try_end),

          (agent_set_slot, ":cur_agent", slot_agent_new_division, ":bgdivision"),	#reassign
          (agent_set_division, ":cur_agent", ":bgdivision"),

        (else_try),	#Maintain any changed divisions (apparently agents get switched back)
          (agent_is_non_player, ":cur_agent"),
          (agent_slot_ge, ":cur_agent", slot_agent_new_division, 0),
          (neg | agent_slot_eq, ":cur_agent", slot_agent_new_division, ":bgdivision"),
          (agent_get_slot, ":bgdivision", ":cur_agent", slot_agent_new_division),
          (agent_set_division, ":cur_agent", ":bgdivision"),
        (try_end),
        (agent_get_troop_id, ":cur_troop", ":cur_agent"),
        (try_begin),
          (game_in_multiplayer_mode),
          (try_begin),
            (is_between, ":cur_troop", multiplayer_troops_begin, multiplayer_troops_end),	#it's a player
            (assign, ":bgdivision", -1),
          (try_end),
        (else_try),
          (team_get_leader, ":leader", ":bgteam"),
          (eq, ":leader", ":cur_agent"),
          (assign, ":bgdivision", -1),
        (try_end),
        (store_character_level, ":cur_level", ":cur_troop"),
        (agent_get_ammo, ":cur_ammo", ":cur_agent", 0),

        #get weapon characteristics
        (assign, ":cur_weapon_type", 0),
        (assign, ":cur_weapon_length", 0),
        (assign, ":cur_swung_weapon_length", 0),
        (agent_get_wielded_item, ":cur_weapon", ":cur_agent", 0),
        (try_begin),
          (is_between, ":cur_weapon", weapons_begin, weapons_end),
          # (neg | is_between, ":cur_weapon", estandartes_begin, estandartes_end),	#put exceptions here, such as standards, that will otherwise force a lot of
          #extra spacing for nothing
          (item_get_weapon_length, ":cur_weapon_length", ":cur_weapon"),

          (try_begin),
            (call_script, "script_cf_is_thrusting_weapon", ":cur_weapon"),
          (else_try),
            (assign, ":cur_swung_weapon_length", ":cur_weapon_length"),
          (try_end),
        (try_end),

        #add up armor
        (assign, ":cur_avg_armor", 0),
        (try_for_range, ":item_slot", ek_head, ek_horse),
          (agent_get_item_slot, ":armor", ":cur_agent", ":item_slot"),
          (gt, ":armor", itm_no_item),
          (item_get_head_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
          (item_get_body_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
          (item_get_leg_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
        (try_end),
        (agent_get_wielded_item, ":armor", ":cur_agent", 1),	#include shield
        (try_begin),
          (gt, ":armor", itm_no_item),
          (item_get_type, ":item_type", ":armor"),
          (eq, ":item_type", itp_type_shield),
          (item_get_body_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
        (try_end),
        (val_div, ":cur_avg_armor", 3),	#average the zones (head, body, leg)

        #average with horse armor for mounted agents
        (agent_get_horse, ":cur_horse", ":cur_agent"),
        (try_begin),
          (gt, ":cur_horse", -1),
          (agent_get_item_id, ":itm_horse", ":cur_horse"),
          (gt, ":itm_horse", itm_no_item),
          (item_get_body_armor, reg0, ":itm_horse"),
          (val_add, ":cur_avg_armor", reg0),
          (val_div, ":cur_avg_armor", 2),
        (try_end),

        (position_get_x, ":x_value", pos1),
        (position_get_y, ":y_value", pos1),
        (position_get_rotation_around_z, ":zrot_value", pos1),
        (try_begin),
          (eq, ":bgdivision", -1), #Leaders
          (try_begin),
            (eq, ":bgteam", 0),
            (assign, ":team0_leader", 1),
            (assign, ":team0_x_leader", ":x_value"),
            (assign, ":team0_y_leader", ":y_value"),
            (assign, ":team0_zrot_leader", ":zrot_value"),
            (assign, ":team0_level_leader", ":cur_level"),
          (else_try),
            (eq, ":bgteam", 1),
            (assign, ":team1_leader", 1),
            (assign, ":team1_x_leader", ":x_value"),
            (assign, ":team1_y_leader", ":y_value"),
            (assign, ":team1_zrot_leader", ":zrot_value"),
            (assign, ":team1_level_leader", ":cur_level"),
          (else_try),
            (eq, ":bgteam", 2),
            (assign, ":team2_leader", 1),
            (assign, ":team2_x_leader", ":x_value"),
            (assign, ":team2_y_leader", ":y_value"),
            (assign, ":team2_zrot_leader", ":zrot_value"),
            (assign, ":team2_level_leader", ":cur_level"),
          (else_try),
            (eq, ":bgteam", 3),
            (assign, ":team3_leader", 1),
            (assign, ":team3_x_leader", ":x_value"),
            (assign, ":team3_y_leader", ":y_value"),
            (assign, ":team3_zrot_leader", ":zrot_value"),
            (assign, ":team3_level_leader", ":cur_level"),
          (try_end),
        (else_try),
          # (agent_get_ammo, reg0, ":cur_agent", 1), #Division in Melee
          (try_begin),
            # (le, reg0, 0), #not wielding ranged weapon?
            (agent_get_attack_action, reg0, ":cur_agent"),
            (gt, reg0, 0),
            (store_add, ":slot", slot_team_d0_is_fighting, ":bgdivision"),
            (team_get_slot, reg0, ":bgteam", ":slot"),
            (val_add, reg0, 1),
            (team_set_slot, ":bgteam", ":slot", reg0),
          (try_end),

          (store_add, ":slot", slot_team_d0_size, ":bgdivision"), #Division Count
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (try_begin),
            (ge, ":cur_ammo", minimum_ranged_ammo),
            (store_add, ":slot", slot_team_d0_percent_ranged, ":bgdivision"), #Division Percentage are Archers
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (val_add, ":value", 1),
            (team_set_slot, ":bgteam", ":slot", ":value"),
          (else_try),
            (store_add, ":slot", slot_team_d0_low_ammo, ":bgdivision"), #Division Running out of Ammo Flag
            (team_set_slot, ":bgteam", ":slot", 1),
          (try_end),

          (try_begin),
            (eq, ":cur_weapon_type", itp_type_thrown),
            (store_add, ":slot", slot_team_d0_percent_throwers, ":bgdivision"), #Division Percentage are Throwers
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (val_add, ":value", 1),
            (team_set_slot, ":bgteam", ":slot", ":value"),
          (try_end),

          (store_add, ":slot", slot_team_d0_level, ":bgdivision"), #Division Level
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":cur_level"),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_weapon_length, ":bgdivision"), #Division Weapon Length
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":cur_weapon_length"),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_swung_weapon_length, ":bgdivision"), #Division Swung Weapon Length
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (try_begin),
            (lt, ":value", ":cur_swung_weapon_length"),
            (team_set_slot, ":bgteam", ":slot", ":cur_swung_weapon_length"),
          (try_end),

          (store_add, ":slot", slot_team_d0_armor, ":bgdivision"), #Division Armor
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":cur_avg_armor"),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (try_begin),	#Division First Rank Shortest Weapon Length
            (agent_slot_eq, ":cur_agent", slot_agent_formation_rank, 1),
            (store_add, ":slot", slot_team_d0_front_weapon_length, ":bgdivision"),
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (this_or_next | eq, ":value", 0),
            (gt, ":value", ":cur_weapon_length"),
            (team_set_slot, ":bgteam", ":slot", ":cur_weapon_length"),
          (try_end),

          (store_add, ":slot", slot_team_d0_avg_x, ":bgdivision"), #Position X
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":x_value"),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_avg_y, ":bgdivision"), #Position Y
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":y_value"),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_avg_zrot, ":bgdivision"), #Rotation
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":zrot_value"),
          (team_set_slot, ":bgteam", ":slot", ":value"),
        (try_end), #Leader vs Regular

        (try_begin),
          (eq, ":agent_class", grc_archers),
          (team_get_slot, ":value", ":bgteam", slot_team_num_archers),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", slot_team_num_archers, ":value"),

        (else_try),
          (eq, ":agent_class", grc_cavalry),
          (team_get_slot, ":value", ":bgteam", slot_team_num_cavalry),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", slot_team_num_cavalry, ":value"),

        (else_try),
          (eq, ":agent_class", grc_infantry),
          (team_get_slot, ":value", ":bgteam", slot_team_num_infantry),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", slot_team_num_infantry, ":value"),
        (try_end),

        #find nearest enemy agent
        (assign, ":nearest_runner", -1),
        (agent_ai_get_num_cached_enemies, ":num_nearby_agents", ":cur_agent"),
        (try_for_range, reg0, 0, ":num_nearby_agents"),
          (agent_ai_get_cached_enemy, ":enemy_agent", ":cur_agent", reg0),
          (agent_is_alive, ":enemy_agent"),

          (try_begin),
            (eq, ":nearest_runner", -1),
            (assign, ":nearest_runner", ":enemy_agent"),

          (else_try),
            (agent_get_position, pos0, ":enemy_agent"),
            (get_distance_between_positions, ":new_distance", pos0, pos1),
            (agent_get_position, pos0, ":nearest_runner"),
            (get_distance_between_positions, ":old_distance", pos0, pos1),
            (lt, ":new_distance", ":old_distance"),
            (assign, ":nearest_runner", ":enemy_agent"),
          (try_end),

          (agent_slot_eq, ":enemy_agent", slot_agent_is_running_away, 0),

          (try_begin),
            (agent_get_slot, ":closest_enemy", ":cur_agent", slot_agent_nearest_enemy_agent),
            (eq, ":closest_enemy", -1),
            (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, ":enemy_agent"),

          (else_try),
            (agent_get_position, pos0, ":enemy_agent"),
            (get_distance_between_positions, ":new_distance", pos0, pos1),
            (agent_get_position, pos0, ":closest_enemy"),
            (get_distance_between_positions, ":old_distance", pos0, pos1),
            (lt, ":new_distance", ":old_distance"),
            (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, ":enemy_agent"),
          (try_end),
        (try_end),
        (try_begin),
          (agent_slot_eq, ":cur_agent", slot_agent_nearest_enemy_agent, -1),
          (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, ":nearest_runner"),
        (try_end),

        #exploit closest agent data
        (try_begin),
          (agent_get_slot, ":closest_enemy", ":cur_agent", slot_agent_nearest_enemy_agent),
          (neq, ":closest_enemy", -1),
          (agent_get_position, pos0, ":closest_enemy"),
          (get_distance_between_positions, ":closest_distance", pos0, pos1),

          #check target of AI agent behavior
          (try_begin),
            (agent_is_non_player, ":cur_agent"),

            (agent_ai_get_behavior_target, ":cur_targeted_agent", ":cur_agent"),
            (neq, ":closest_enemy", ":cur_targeted_agent"),

            (this_or_next | neg | agent_is_non_player, ":closest_enemy"),	#AI can always sense player behind them (balancing factor, dedicated to
            #Idibil)
            (neg | position_is_behind_position, pos0, pos1),

            (lt, ":closest_distance", 2000),	#Assuming rethink is expensive, don't bother beyond 20m

            (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (this_or_next | eq, formation_rethink_for_formations_only, 0),
            (gt, ":value", formation_none),

            (agent_force_rethink, ":cur_agent"),
          (try_end),

          #update division information
          (try_begin),
            (ge, ":bgdivision", 0),	#not leaders

            (try_begin),
              (lt, ":closest_distance", 350),
              (agent_get_division, reg0, ":closest_enemy"),
              (store_add, ":slot", slot_team_d0_enemy_supporting_melee, reg0),
              (agent_get_group, reg0, ":closest_enemy"),
              (team_get_slot, ":value", reg0, ":slot"),
              (val_add, ":value", 1),
              (team_set_slot, reg0, ":slot", ":value"),
            (try_end),

            (store_add, ":slot", slot_team_d0_closest_enemy_dist, ":bgdivision"),
            (team_get_slot, ":old_distance", ":bgteam", ":slot"),
            (try_begin),
              (this_or_next | eq, ":old_distance", 0),
              (lt, ":closest_distance", ":old_distance"),
              (team_set_slot, ":bgteam", ":slot", ":closest_distance"),
              (store_add, ":slot", slot_team_d0_closest_enemy, ":bgdivision"),
              (team_set_slot, ":bgteam", ":slot", ":closest_enemy"),
            (try_end),

            (assign, ":doit", 0),
            (agent_get_class, ":enemy_agent_class", ":closest_enemy"),
            (store_add, ":slot", slot_team_d0_type, ":bgdivision"),
            (team_get_slot, ":value", ":bgteam", ":slot"),

            #AI infantry division tracks non-infantry to preferably chase
            (try_begin),
              (this_or_next | eq, ":value", sdt_polearm),
              (eq, ":value", sdt_infantry),
              (neq, ":enemy_agent_class", grc_cavalry),
              (assign, ":doit", 1),

              #AI archer division tracks infantry to avoid
            (else_try),
              (this_or_next | eq, ":value", sdt_archer),
              (eq, ":value", sdt_skirmisher),
              (eq, ":enemy_agent_class", grc_infantry),
              (assign, ":doit", 1),
            (try_end),

            (eq, ":doit", 1),
            (store_add, ":slot", slot_team_d0_closest_enemy_special_dist, ":bgdivision"),
            (team_get_slot, ":old_distance", ":bgteam", ":slot"),
            (try_begin),
              (this_or_next | eq, ":old_distance", 0),
              (lt, ":closest_distance", ":old_distance"),
              (team_set_slot, ":bgteam", ":slot", ":closest_distance"),
              (store_add, ":slot", slot_team_d0_closest_enemy_special, ":bgdivision"),
              (team_set_slot, ":bgteam", ":slot", ":closest_enemy"),
            (try_end),
          (try_end),	#update division info
        (try_end),	#exploit closest agent data
      (try_end), #Agent Loop

      #calculate team sizes, sum positions; within calculate battle group averages
      (try_for_range, ":team", 0, 4),
        (assign, ":team_size", 0),
        (assign, ":team_level", 0),
        (assign, ":team_x", 0),
        (assign, ":team_y", 0),
        (assign, ":team_zrot", 0),

        (try_for_range, ":division", 0, 9),
          #sum for team averages
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_get_slot, ":division_size", ":team", ":slot"),
          (gt, ":division_size", 0),
          (val_add, ":team_size", ":division_size"),

          (store_add, ":slot", slot_team_d0_level, ":division"),
          (team_get_slot, ":division_level", ":team", ":slot"),
          (val_add, ":team_level", ":division_level"),

          (store_add, ":slot", slot_team_d0_avg_x, ":division"),
          (team_get_slot, ":division_x", ":team", ":slot"),
          (val_add, ":team_x", ":division_x"),

          (store_add, ":slot", slot_team_d0_avg_y, ":division"),
          (team_get_slot, ":division_y", ":team", ":slot"),
          (val_add, ":team_y", ":division_y"),

          (store_add, ":slot", slot_team_d0_avg_zrot, ":division"),
          (team_get_slot, ":division_zrot", ":team", ":slot"),
          (val_add, ":team_zrot", ":division_zrot"),

          #calculate battle group averages
          (store_add, ":slot", slot_team_d0_level, ":division"),
          (val_div, ":division_level", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_level"),

          (store_add, ":slot", slot_team_d0_percent_ranged, ":division"),
          (team_get_slot, ":value", ":team", ":slot"),
          (val_mul, ":value", 100),
          (val_div, ":value", ":division_size"),
          (team_set_slot, ":team", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_percent_throwers, ":division"),
          (team_get_slot, ":value", ":team", ":slot"),
          (val_mul, ":value", 100),
          (val_div, ":value", ":division_size"),
          (team_set_slot, ":team", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_weapon_length, ":division"),
          (team_get_slot, ":value", ":team", ":slot"),
          (val_div, ":value", ":division_size"),
          (team_set_slot, ":team", ":slot", ":value"),

          # (store_add, ":slot", slot_team_d0_swung_weapon_length, ":division"), MOTO
          # systematic testing shows best to use max swung weapon length as basis for
          # formation spacing
          # (team_get_slot, ":value", ":team", ":slot"),
          # (val_div, ":value", ":division_size"),
          # (team_set_slot, ":team", ":slot", ":value"),

          # (store_add, ":slot", slot_team_d0_front_agents, ":division"), MOTO front
          # rank should be within shortest weapon distance, not average
          # (team_get_slot, reg0, ":team", ":slot"),
          # (try_begin),
          # (gt, reg0, 0),
          # (store_add, ":slot", slot_team_d0_front_weapon_length, ":division"),
          # (team_get_slot, ":value", ":team", ":slot"),
          # (val_div, ":value", reg0),
          # (team_set_slot, ":team", ":slot", ":value"),
          # (try_end),

          (store_add, ":slot", slot_team_d0_avg_x, ":division"),
          (val_div, ":division_x", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_x"),

          (store_add, ":slot", slot_team_d0_avg_y, ":division"),
          (val_div, ":division_y", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_y"),

          (store_add, ":slot", slot_team_d0_avg_zrot, ":division"),
          (val_div, ":division_zrot", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_zrot"),

          (store_add, ":slot", slot_team_d0_type, ":division"),
          (team_get_slot, reg0, ":team", ":slot"),
          (try_begin),
            (neg | is_between, reg0, 0, 8),	#TODO reset on reinforcements
            (call_script, "script_store_battlegroup_type", ":team", ":division"),
          (try_end),
        (try_end), #Division Loop

        #Team Leader Additions
        (try_begin),
          (eq, ":team", 0),
          (val_add, ":team_size", ":team0_leader"),
          (val_add, ":team_level", ":team0_level_leader"),
          (val_add, ":team_x", ":team0_x_leader"),
          (val_add, ":team_y", ":team0_y_leader"),
          (val_add, ":team_zrot", ":team0_zrot_leader"),
        (else_try),
          (eq, ":team", 1),
          (val_add, ":team_size", ":team1_leader"),
          (val_add, ":team_level", ":team1_level_leader"),
          (val_add, ":team_x", ":team1_x_leader"),
          (val_add, ":team_y", ":team1_y_leader"),
          (val_add, ":team_zrot", ":team1_zrot_leader"),
        (else_try),
          (eq, ":team", 2),
          (val_add, ":team_size", ":team2_leader"),
          (val_add, ":team_level", ":team2_level_leader"),
          (val_add, ":team_x", ":team2_x_leader"),
          (val_add, ":team_y", ":team2_y_leader"),
          (val_add, ":team_zrot", ":team2_zrot_leader"),
        (else_try),
          (eq, ":team", 3),
          (val_add, ":team_size", ":team3_leader"),
          (val_add, ":team_level", ":team3_level_leader"),
          (val_add, ":team_x", ":team3_x_leader"),
          (val_add, ":team_y", ":team3_y_leader"),
          (val_add, ":team_zrot", ":team3_zrot_leader"),
        (try_end),

        #calculate team averages
        (gt, ":team_size", 0),
        (team_set_slot, ":team", slot_team_size, ":team_size"),
        (val_div, ":team_level", ":team_size"),
        (team_set_slot, ":team", slot_team_level, ":team_level"),

        (val_div, ":team_x", ":team_size"),
        (team_set_slot, ":team", slot_team_avg_x, ":team_x"),
        (val_div, ":team_y", ":team_size"),
        (team_set_slot, ":team", slot_team_avg_y, ":team_y"),
        (val_div, ":team_zrot", ":team_size"),
        (team_set_slot, ":team", slot_team_avg_zrot, ":team_zrot"),
      (try_end), #Team Loop
  ]),

("cf_division_data_available", [
      (assign, ":evidence", 0),
      (try_for_range, ":team", 0, 4),
        (team_slot_ge, ":team", slot_team_size, 1),
        (assign, ":evidence", 1),
      (try_end),
      (neq, ":evidence", 0)]),

("battlegroup_get_position", [
      (store_script_param, ":bgposition", 1),
      (store_script_param, ":bgteam", 2),
      (store_script_param, ":bgdivision", 3),

      (assign, ":x", 0),
      (assign, ":y", 0),
      (init_position, ":bgposition"),
      (try_begin),
        (neg | is_between, ":bgdivision", 0, 9),
        (team_slot_ge, ":bgteam", slot_team_size, 1),
        (team_get_slot, ":x", ":bgteam", slot_team_avg_x),
        (team_get_slot, ":y", ":bgteam", slot_team_avg_y),
        (team_get_slot, ":zrot", ":bgteam", slot_team_avg_zrot),
      (else_try),
        (is_between, ":bgdivision", 0, 9),
        (store_add, ":slot", slot_team_d0_size, ":bgdivision"),
        (team_slot_ge, ":bgteam", ":slot", 1),

        (store_add, ":slot", slot_team_d0_avg_x, ":bgdivision"),
        (team_get_slot, ":x", ":bgteam", ":slot"),

        (store_add, ":slot", slot_team_d0_avg_y, ":bgdivision"),
        (team_get_slot, ":y", ":bgteam", ":slot"),

        (store_add, ":slot", slot_team_d0_avg_zrot, ":bgdivision"),
        (team_get_slot, ":zrot", ":bgteam", ":slot"),
      (try_end),
      (position_set_x, ":bgposition", ":x"),
      (position_set_y, ":bgposition", ":y"),
      (position_rotate_z, ":bgposition", ":zrot", 0),
      (position_set_z_to_ground_level, ":bgposition"),]),

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
      (position_move_y, ":bgposition", ":distance_to_move"),]),

("battlegroup_dist_center_to_front", [
      (store_script_param, ":bgteam", 1),
      (store_script_param, ":bgdivision", 2),

      (store_add, ":slot", slot_team_d0_formation_space, ":bgdivision"),
      (team_get_slot, ":spacing", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
      (team_get_slot, ":bgformation", ":bgteam", ":slot"),

      (try_begin),
        (eq, ":bgformation", formation_none),	#single row
        (assign, ":depth", 0),

        #WFaS multi-ranks
      (else_try),
        (eq, ":bgformation", formation_2_row),
        (assign, ":depth", 100),
      (else_try),
        (eq, ":bgformation", formation_3_row),
        (assign, ":depth", 200),
      (else_try),
        (eq, ":bgformation", formation_4_row),
        (assign, ":depth", 300),
      (else_try),
        (eq, ":bgformation", formation_5_row),
        (assign, ":depth", 400),

      (else_try),	#WB multi-ranks
        (lt, ":spacing", 0),
        (store_mul, ":depth", ":spacing", -1),
        (val_mul, ":depth", 100),

      #Non Native
      (else_try),
        (store_add, ":slot", slot_team_d0_size, ":bgdivision"),
        (team_get_slot, ":size_enemy_battlegroup", ":bgteam", ":slot"),
        (store_mul, ":row_depth", ":spacing", 50),
        (val_add, ":row_depth", formation_minimum_spacing),

        (this_or_next | eq, ":bgformation", formation_ranks),
        (eq, ":bgformation", formation_shield),
        (call_script, "script_calculate_default_ranks", ":size_enemy_battlegroup"),
        (val_sub, reg1, 1),
        (store_mul, ":depth", ":row_depth", reg1),

      (else_try),
        (convert_to_fixed_point, ":size_enemy_battlegroup"),
        (store_sqrt, ":columns", ":size_enemy_battlegroup"),

        (eq, ":bgformation", formation_square),
        (convert_from_fixed_point, ":columns"),
        (val_add, ":columns", 1),	#see script_form_infantry
        (store_div, ":rows", ":size_enemy_battlegroup", ":columns"),
        (store_mul, ":depth", ":row_depth", ":rows"),
        (convert_from_fixed_point, ":depth"),
        (val_sub, ":depth", ":row_depth"),

      (else_try),
        (eq, ":bgformation", formation_wedge),
        (store_mul, ":depth", ":row_depth", ":columns"),	#approximation
        (convert_from_fixed_point, ":depth"),
      (try_end),

      (try_begin),
        (neq, ":bgformation", formation_wedge),
        (store_div, reg0, ":depth", 2),
      (else_try),
        (store_mul, reg0, ":depth", 2),	#another approximation (height - inner radius)
        (val_div, reg0, 3),
      (try_end),]),

("battlegroup_get_action_radius", [
      (store_script_param, ":bgteam", 1),
      (store_script_param, ":bgdivision", 2),

      (store_add, ":slot", slot_team_d0_size, ":bgdivision"),
      (team_get_slot, ":size_battlegroup", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
      (team_get_slot, ":formation", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_type, ":bgdivision"),
      (team_get_slot, ":div_type", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation_space, ":bgdivision"),
      (team_get_slot, ":spacing", ":bgteam", ":slot"),

      (try_begin),
        (this_or_next | eq, ":div_type", sdt_archer),
        (le, ":formation", formation_none),	#Native formation

        (store_mul, ":troop_space", ":spacing", 75),	#Native minimum spacing not consistent but about this
        (val_add, ":troop_space", 100),	#minimum spacing

        #WFaS multi-ranks
        (try_begin),
          (eq, ":formation", formation_2_row),
          (val_div, ":size_battlegroup", 2),
        (else_try),
          (eq, ":formation", formation_3_row),
          (val_div, ":size_battlegroup", 3),
        (else_try),
          (eq, ":formation", formation_4_row),
          (val_div, ":size_battlegroup", 4),
        (else_try),
          (eq, ":formation", formation_5_row),
          (val_div, ":size_battlegroup", 5),

        (else_try),	#WB multi-ranks
          (lt, ":spacing", 0),
          (assign, ":troop_space", 150),
          (val_mul, ":spacing", -1),
          (val_add, ":spacing", 1),
          (val_div, ":size_battlegroup", ":spacing"),
        (try_end),

        (store_mul, ":formation_width", ":size_battlegroup", ":troop_space"),
        (store_div, reg0, ":formation_width", 2),

      (else_try),
        (eq, ":formation", formation_wedge),
        (call_script, "script_get_centering_amount", formation_square, ":size_battlegroup", ":spacing"),	#approximation
        (val_mul, reg0, 7),
        (val_div, reg0, 6),
      (else_try),
        (try_begin),
          (lt, ":spacing", 0),
          (assign, reg0, ":bgteam"),
          (assign, reg1, ":bgdivision"),
          (assign, reg2, ":formation"),
          (display_message, "@{!}battlegroup_get_action_radius: negative radius for team {reg0} division {reg1} formation {reg2}"),
        (try_end),
        (call_script, "script_get_centering_amount", ":formation", ":size_battlegroup", ":spacing"),
      (try_end),

      (val_mul, reg0, 2),]),

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

      (assign, reg0, ":total_size"),]),

("get_distance_to_battlegroup", [
      (store_script_param, ":bgteam", 1),
      (store_script_param, ":bgdivision", 2),
      (store_script_param, ":from_pos", 3),

      (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
      (team_get_slot, ":bgformation", ":bgteam", ":slot"),
      (call_script, "script_battlegroup_get_action_radius", ":bgteam", ":bgdivision"),
      (store_div, ":radius", reg0, 2),	#function returns length of bg
      (assign, ":min_cos_theta", 1),
      (convert_to_fixed_point, ":min_cos_theta"),
      (try_begin),
        (eq, ":bgformation", formation_wedge),
        (val_mul, ":min_cos_theta", 58),	#relation inscribed circle radius to half side: 1 / sqrt 3
        (val_div, ":min_cos_theta", 100),
      (else_try),
        (gt, ":radius", 0),
        (call_script, "script_battlegroup_dist_center_to_front", ":bgteam", ":bgdivision"),
        (val_mul, ":min_cos_theta", reg0),
        (val_div, ":min_cos_theta", ":radius"),
      (else_try),
        (assign, ":min_cos_theta", 0),
      (try_end),

      #acquire rotations
      (call_script, "script_battlegroup_get_position", pos0, ":bgteam", ":bgdivision"),
      (try_begin),
        (gt, ":bgformation", formation_none),
        (neq, ":bgformation", formation_default),
        (call_script, "script_get_formation_destination", pos61, ":bgteam", ":bgdivision"),
        (position_copy_rotation, pos0, pos61),
      (try_end),

      (copy_position, pos61, ":from_pos"),
      (call_script, "script_point_y_toward_position", pos61, pos0),
      (assign, ":distance_to_battlegroup", reg0),

      #calculate difference from center of bg
      (get_angle_between_positions, ":theta", pos61, pos0),
      (val_sub, ":theta", 9000),
      (store_cos, ":cos_theta", ":theta"),
      (val_abs, ":cos_theta"),
      (val_max, ":cos_theta", ":min_cos_theta"),	#doing depth considerations this way allows calling func to use angle; it also
      #avoids Pythagorean calcs

      (store_mul, reg1, ":radius", ":cos_theta"),
      (convert_from_fixed_point, reg1),
      (val_sub, ":distance_to_battlegroup", reg1),
      (assign, reg0, ":distance_to_battlegroup"),
      (assign, reg2, ":cos_theta"),]),

("calculate_decision_numbers", [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_presence", 2),
      (try_begin),
        (team_get_slot, reg0, ":team_no", slot_team_level),
        (store_div, reg1, reg0, 3),
        (store_add, reg0, ":battle_presence", reg1),	#decision w.r.t.  all enemy teams
      (try_end)]),

("team_field_ranged_tactics", [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":rel_army_size", 2),
      (store_script_param, ":battle_presence", 3),
      (assign, ":division", grc_archers), #Pre-Many Divisions
      (assign, ":bg_pos", Archers_Pos), #Pre-Many Divisions

      (try_begin),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_eq, ":team_no", ":slot", 0),
        (try_begin),	#undo reversion to BP_Jockey (see below)
          (lt, "$battle_phase", BP_Fight),
          (call_script, "script_cf_any_fighting"),
          (call_script, "script_cf_count_casualties"),
          (assign, "$battle_phase", BP_Fight),
        (try_end),

      (else_try),
        (call_script, "script_battlegroup_get_position", ":bg_pos", ":team_no", ":division"),
        (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, ":team_no", grc_everyone),
        (call_script, "script_point_y_toward_position", ":bg_pos", Enemy_Team_Pos),

        (store_add, ":slot", slot_team_d0_closest_enemy_special_dist, ":division"),	#distance to nearest enemy infantry agent
        (team_get_slot, ":distance_to_enemy", ":team_no", ":slot"),
        (try_begin),
          (eq, ":distance_to_enemy", 0),
          (call_script, "script_get_nearest_enemy_battlegroup_location", Nearest_Enemy_Battlegroup_Pos, ":team_no", ":bg_pos"),
          (assign, ":distance_to_enemy", reg0),
        (try_end),

        (try_begin),	#avoid being provoked from defensive position
          (ge, "$battle_phase", BP_Fight),
          (try_begin),
            (call_script, "script_cf_any_fighting"),
          (else_try),
            (assign, "$battle_phase", BP_Jockey),
            (assign, "$clock_reset", 0),
          (try_end),
        (try_end),

        (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
        (team_get_slot, ":is_firing", ":team_no", ":slot"),
        (store_add, ":slot", slot_team_d0_size, grc_infantry),
        (team_get_slot, ":num_infantry", ":team_no", ":slot"),

        (call_script, "script_calculate_decision_numbers", ":team_no", ":battle_presence"),
        (assign, ":decision_index", reg0),
        (assign, ":level_bump", reg1),

        (try_begin),
          (gt, ":decision_index", 86),	#outpower enemies more than 6:1?
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_charge),
            (team_give_order, ":team_no", ":division", mordr_charge),
          (try_end),

        (else_try),
          (lt, ":decision_index", 14),	#outpowered more than 6:1?
          (eq, ":num_infantry", 0),	#no infantry to delay enemy?
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_retreat),
            (team_give_order, ":team_no", ":division", mordr_retreat),
          (try_end),

        (else_try),
          (ge, "$battle_phase", BP_Jockey),
          (store_add, ":slot", slot_team_d0_low_ammo, ":division"),
          (team_slot_ge, ":team_no", ":slot", 1),	#running out of ammo?
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_charge),
            (team_give_order, ":team_no", ":division", mordr_charge),
          (try_end),

        (else_try),
          (ge, "$battle_phase", BP_Fight),
          (eq, ":is_firing", 0),
          (gt, ":decision_index", Advance_More_Point),
          (le, ":distance_to_enemy", AI_long_range),	#closer than reposition?
          (team_give_order, ":team_no", ":division", mordr_advance),

        #hold somewhere
        (else_try),
          (store_add, ":decision_index", ":rel_army_size", ":level_bump"),	#decision w.r.t. largest enemy team
          (assign, ":move_archers", 0),

          (init_position, Team_Starting_Point),
          (team_get_slot, reg0, ":team_no", slot_team_starting_x),
          (position_set_x, Team_Starting_Point, reg0),
          (team_get_slot, reg0, ":team_no", slot_team_starting_y),
          (position_set_y, Team_Starting_Point, reg0),
          (position_set_z_to_ground_level, Team_Starting_Point),

          (try_begin),
            (eq, "$battle_phase", BP_Setup),
            (assign, ":move_archers", 1),
          (else_try),
            (ge, "$battle_phase", BP_Fight),
            (try_begin),
              (neg | is_between, ":distance_to_enemy", AI_charge_distance, AI_long_range),
              (assign, ":move_archers", 1),
            (else_try),
              (lt, ":decision_index", Hold_Point),	#probably coming from a defensive position (see below)
              (eq, "$FormAI_AI_no_defense", 0),	#player hasn't set disallow defense option?
              (eq, ":is_firing", 0),	#probably because player team has retreated
              (assign, ":move_archers", 1),
            (try_end),
          (else_try),	#jockey phase
            (this_or_next | gt, "$FormAI_AI_no_defense", 0),	#player has set disallow defense option OR
            (ge, ":decision_index", Hold_Point),	#not starting in a defensive position (see below)
            (try_begin),
              (gt, ":distance_to_enemy", AI_long_range),	#enemy very far off
              (assign, ":move_archers", 1),
            (else_try),
              (call_script, "script_point_y_toward_position", Team_Starting_Point, ":bg_pos"),
              (position_get_rotation_around_z, reg0, Team_Starting_Point),
              (position_get_rotation_around_z, reg1, ":bg_pos"),
              (val_sub, reg0, reg1),
              (this_or_next | is_between, reg0, -45, 45),	#only move if within "cone of advancement" to prevent constant adjusting at
              #border OR
              (eq, ":is_firing", 0),	#if not firing for some reason (hill in way?)

              (try_begin),
                (eq, ":num_infantry", 0),	#no infantry to wait for
                (assign, ":move_archers", 1),
              (else_try),
                (call_script, "script_battlegroup_get_position", Infantry_Pos, ":team_no", grc_infantry),
                (get_distance_between_positions, ":infantry_to_enemy", Infantry_Pos, Enemy_Team_Pos),
                (get_distance_between_positions, ":archers_to_enemy", ":bg_pos", Enemy_Team_Pos),
                (val_sub, ":infantry_to_enemy", ":archers_to_enemy"),
                (le, ":infantry_to_enemy", 1500),	#don't outstrip infantry when closing
                (assign, ":move_archers", 1),
              (try_end),
            (try_end),
          (try_end),

          (try_begin),
            (gt, ":move_archers", 0),
            (try_begin),
              (lt, ":decision_index", Hold_Point),	#outnumbered?
              (eq, "$FormAI_AI_no_defense", 0),	#player hasn't set disallow defense option?
              (lt, "$battle_phase", BP_Fight),
              (neq, ":team_no", 1),	#not attacker?
              (neq, ":team_no", 3),	#not ally of attacker?
              (store_div, ":distance_to_move", ":distance_to_enemy", 6),	#middle of rear third of battlefield
              (assign, ":hill_search_radius", ":distance_to_move"),

            (else_try),
              (try_begin),
                (ge, "$battle_phase", BP_Fight),
                (copy_position, ":bg_pos", Team_Starting_Point),
                (call_script, "script_point_y_toward_position", ":bg_pos", Enemy_Team_Pos),
                (try_begin),
                  (gt, ":num_infantry", 0),
                  (store_add, ":slot", slot_team_d0_closest_enemy, grc_infantry),
                  (team_get_slot, ":enemy_agent_nearest_infantry", ":team_no", ":slot"),
                  (le, ":enemy_agent_nearest_infantry", 0),
                  (agent_get_team, ":target_team", ":enemy_agent_nearest_infantry"),
                  (agent_get_division, ":target_division", ":enemy_agent_nearest_infantry"),
                  (call_script, "script_battlegroup_get_position", Nearest_Enemy_Battlegroup_Pos, ":target_team", ":target_division"),
                  (get_distance_between_positions, ":distance_to_enemy", ":bg_pos", Nearest_Enemy_Battlegroup_Pos),
                (else_try),
                  (call_script, "script_get_nearest_enemy_battlegroup_location", Nearest_Enemy_Battlegroup_Pos, ":team_no", ":bg_pos"),
                  (assign, ":distance_to_enemy", reg0),
                (try_end),
              (try_end),

              (try_begin),
                (eq, "$battle_phase", BP_Setup),
                (assign, ":shot_distance", AI_long_range),
              (else_try),
                (assign, ":shot_distance", AI_firing_distance),
                (store_sub, reg1, AI_firing_distance, AI_charge_distance),
                (val_sub, reg1, 200),	#subtract two meters to prevent automatically provoking melee from forward
                #enemy infantry
                (store_add, ":slot", slot_team_d0_percent_throwers, ":division"),
                (team_get_slot, reg0, ":team_no", ":slot"),
                (val_mul, reg1, reg0),
                (val_div, reg1, 100),
                (val_sub, ":shot_distance", reg1),
              (try_end),

              (store_sub, ":distance_to_move", ":distance_to_enemy", ":shot_distance"),
              (store_div, ":hill_search_radius", ":shot_distance", 3),	#limit so as not to run into enemy
              (try_begin),
                (lt, "$battle_phase", BP_Fight),
                (try_begin),
                  (this_or_next | eq, "$battle_phase", BP_Setup),
                  (lt, ":battle_presence", Advance_More_Point),	#expect to meet halfway?
                  (val_div, ":distance_to_move", 2),
                (try_end),
              (try_end),
            (try_end),

            (position_move_y, ":bg_pos", ":distance_to_move", 0),
            (try_begin),
              (lt, "$battle_phase", BP_Fight),
              (copy_position, pos1, ":bg_pos"),
              (store_div, reg0, ":hill_search_radius", 100),
              (call_script, "script_find_high_ground_around_pos1_corrected", ":bg_pos", reg0),
            (try_end),
          (try_end),

          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_hold),
            (team_give_order, ":team_no", ":division", mordr_hold),
          (try_end),
          (call_script, "script_set_formation_destination", ":team_no", ":division", ":bg_pos"),
        (try_end),
      (try_end)]),

("team_field_melee_tactics", [
      (store_script_param, ":team_no", 1),
      #	(store_script_param, ":rel_army_size", 2),
      (store_script_param, ":battle_presence", 3),
      (call_script, "script_calculate_decision_numbers", ":team_no", ":battle_presence"),

      #mop up if outnumber enemies more than 6:1
      (try_begin),
        (gt, reg0, 86),
        (try_for_range, ":division", 0, 9),
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_slot_ge, ":team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_type, ":division"),
          (neg | team_slot_eq, ":team_no", ":slot", sdt_archer),
          (neg | team_slot_eq, ":team_no", ":slot", sdt_skirmisher),
          (call_script, "script_formation_end", ":team_no", ":division"),
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_charge),
            (team_give_order, ":team_no", ":division", mordr_charge),
          (try_end),
        (try_end),

      (else_try),
        (assign, ":num_enemies", 0),
        (try_for_range, ":enemy_team_no", 0, 4),
          (teams_are_enemies, ":enemy_team_no", ":team_no"),
          (team_get_slot, ":value", ":enemy_team_no", slot_team_size),
          (val_add, ":num_enemies", ":value"),
        (try_end),

        (gt, ":num_enemies", 0),
        (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, ":team_no", grc_everyone),

        (store_add, ":slot", slot_team_d0_size, grc_archers),
        (team_get_slot, ":num_archers", ":team_no", ":slot"),
        (try_begin),
          (eq, ":num_archers", 0),
          (assign, ":enemy_bg_nearest_archers_dist", Far_Away),
          (assign, ":archer_order", mordr_charge),
        (else_try),
          (call_script, "script_battlegroup_get_position", Archers_Pos, ":team_no", grc_archers),
          (call_script, "script_point_y_toward_position", Archers_Pos, Enemy_Team_Pos),
          (call_script, "script_get_nearest_enemy_battlegroup_location", pos0, ":team_no", Archers_Pos),
          (assign, ":enemy_bg_nearest_archers_dist", reg0),
          (team_get_movement_order, ":archer_order", ":team_no", grc_archers),
        (try_end),

        (store_add, ":slot", slot_team_d0_size, grc_infantry),
        (team_get_slot, ":num_infantry", ":team_no", ":slot"),
        (try_begin),
          (eq, ":num_infantry", 0),
          (assign, ":enemy_bg_nearest_infantry_dist", Far_Away),
          (assign, ":enemy_agent_nearest_infantry_dist", Far_Away),
        (else_try),
          (call_script, "script_battlegroup_get_position", Infantry_Pos, ":team_no", grc_infantry),
          (call_script, "script_get_nearest_enemy_battlegroup_location", pos0, ":team_no", Infantry_Pos),
          (assign, ":enemy_bg_nearest_infantry_dist", reg0),
          (store_add, ":slot", slot_team_d0_closest_enemy_dist, grc_infantry),
          (team_get_slot, ":enemy_agent_nearest_infantry_dist", ":team_no", ":slot"),
          (eq, ":enemy_agent_nearest_infantry_dist", 0),	#happens when player turns off closest agent mechanism (see mod options)
          (assign, ":enemy_agent_nearest_infantry_dist", ":enemy_bg_nearest_infantry_dist"),
        (try_end),

        (store_add, ":slot", slot_team_d0_size, grc_cavalry),
        (team_get_slot, ":num_cavalry", ":team_no", ":slot"),
        (try_begin),
          (eq, ":num_cavalry", 0),
          (assign, ":enemy_bg_nearest_cavalry_dist", Far_Away),
          (assign, ":enemy_agent_nearest_cavalry_dist", Far_Away),
        (else_try),
          (call_script, "script_battlegroup_get_position", Cavalry_Pos, ":team_no", grc_cavalry),
          (call_script, "script_get_nearest_enemy_battlegroup_location", pos0, ":team_no", Cavalry_Pos),
          (assign, ":enemy_bg_nearest_cavalry_dist", reg0),
          (store_add, ":slot", slot_team_d0_closest_enemy_dist, grc_cavalry),
          (team_get_slot, ":enemy_agent_nearest_cavalry_dist", ":team_no", ":slot"),
          (eq, ":enemy_agent_nearest_cavalry_dist", 0),	#happens when player turns off closest agent mechanism (see mod options)
          (assign, ":enemy_agent_nearest_cavalry_dist", ":enemy_bg_nearest_infantry_dist"),
        (try_end),

        (try_begin),
          (lt, "$battle_phase", BP_Fight),
          (this_or_next | le, ":enemy_bg_nearest_infantry_dist", AI_charge_distance),
          (this_or_next | le, ":enemy_bg_nearest_cavalry_dist", AI_charge_distance),
          (le, ":enemy_bg_nearest_archers_dist", AI_charge_distance),
          (assign, "$battle_phase", BP_Fight),
        (else_try),
          (lt, "$battle_phase", BP_Jockey),
          (this_or_next | le, ":enemy_agent_nearest_infantry_dist", AI_long_range),
          (le, ":enemy_agent_nearest_cavalry_dist", AI_long_range),
          (assign, "$battle_phase", BP_Jockey),
        (try_end),

        (team_get_leader, ":team_leader", ":team_no"),
        (assign, ":place_leader_by_infantry", 0),

        #infantry AI
        (store_add, ":slot", slot_team_d0_closest_enemy, grc_infantry),
        (team_get_slot, ":enemy_agent_nearest_infantry", ":team_no", ":slot"),
        (try_begin),
          (this_or_next | le, ":num_infantry", 0),
          (le, ":enemy_agent_nearest_infantry", 0),
          (assign, ":infantry_order", ":archer_order"),

          #deal with mounted heroes that team_give_order() treats as infantry
          ##CABA...could change their division?
          (team_get_movement_order, reg0, ":team_no", grc_infantry),
          (try_begin),
            (neq, reg0, ":infantry_order"),
            (team_give_order, ":team_no", grc_infantry, ":infantry_order"),
          (try_end),
          (try_begin),
            (gt, ":num_archers", 0),
            (copy_position, pos1, Archers_Pos),
            (position_move_y, pos1, 1000, 0),
            (call_script, "script_set_formation_destination", ":team_no", grc_infantry, pos1),
          (else_try),
            (call_script, "script_set_formation_destination", ":team_no", grc_infantry, Cavalry_Pos),
          (try_end),

        (else_try),
          (agent_get_position, Nearest_Enemy_Troop_Pos, ":enemy_agent_nearest_infantry"),
          (agent_get_team, ":enemy_agent_nearest_infantry_team", ":enemy_agent_nearest_infantry"),
          (agent_get_division, ":enemy_agent_nearest_infantry_div", ":enemy_agent_nearest_infantry"),

          (assign, ":sum_level_enemy_infantry", 0),
          (try_for_range, ":enemy_team_no", 0, 4),
            (teams_are_enemies, ":enemy_team_no", ":team_no"),
            (try_for_range, ":enemy_division", 0, 9),
              (store_add, ":slot", slot_team_d0_type, ":enemy_division"),
              (team_get_slot, ":value", ":enemy_team_no", ":slot"),
              (this_or_next | eq, ":value", sdt_polearm),
              (eq, ":value", sdt_infantry),
              (store_add, ":slot", slot_team_d0_size, ":enemy_division"),
              (team_get_slot, ":value", ":enemy_team_no", ":slot"),
              (store_add, ":slot", slot_team_d0_level, ":enemy_division"),
              (team_get_slot, reg0, ":enemy_team_no", ":slot"),
              (val_mul, ":value", reg0),
              (val_add, ":sum_level_enemy_infantry", ":value"),
            (try_end),
          (try_end),

          (store_mul, ":percent_level_enemy_infantry", ":sum_level_enemy_infantry", 100),
          (val_div, ":percent_level_enemy_infantry", ":num_enemies"),
          (try_begin),
            (teams_are_enemies, ":team_no", "$fplayer_team_no"),
            (assign, ":combined_level", 0),
            (assign, ":combined_team_size", 0),
            (assign, ":combined_num_infantry", ":num_infantry"),
          (else_try),
            (store_add, ":slot", slot_team_d0_level, grc_infantry),
            (team_get_slot, ":combined_level", "$fplayer_team_no", ":slot"),
            (team_get_slot, ":combined_team_size", "$fplayer_team_no", slot_team_size),
            (store_add, ":slot", slot_team_d0_size, grc_infantry),
            (team_get_slot, ":combined_num_infantry", "$fplayer_team_no", ":slot"),
            (val_add, ":combined_num_infantry", ":num_infantry"),
          (try_end),
          (store_mul, ":percent_level_infantry", ":combined_num_infantry", 100),
          (store_add, ":slot", slot_team_d0_level, grc_infantry),
          (team_get_slot, ":level_infantry", ":team_no", ":slot"),
          (val_add, ":combined_level", ":level_infantry"),
          (val_mul, ":percent_level_infantry", ":combined_level"),
          (team_get_slot, reg0, ":team_no", slot_team_size),
          (val_add, ":combined_team_size", reg0),
          (val_div, ":percent_level_infantry", ":combined_team_size"),

          (assign, ":infantry_order", mordr_charge),
          (try_begin),	#enemy far away AND ranged not charging
            (gt, ":enemy_bg_nearest_archers_dist", AI_charge_distance),
            (gt, ":enemy_agent_nearest_infantry_dist", AI_charge_distance),
            (neq, ":archer_order", mordr_charge),
            (try_begin),	#fighting not started OR not enough infantry
              (this_or_next | le, "$battle_phase", BP_Jockey),
              (lt, ":percent_level_infantry", ":percent_level_enemy_infantry"),
              (assign, ":infantry_order", mordr_hold),
            (try_end),
          (try_end),

          # bum rush enemy archers?
          (try_begin),
            # (le, ":level_infantry", AI_Poor_Troop_Level), unfortunately leaves them
            # susceptible to rings of archers
            (store_add, ":slot", slot_team_d0_type, ":enemy_agent_nearest_infantry_div"),
            (this_or_next | team_slot_eq, ":enemy_agent_nearest_infantry_team", ":enemy_agent_nearest_infantry_div", sdt_archer),
            (team_slot_eq, ":enemy_agent_nearest_infantry_team", ":enemy_agent_nearest_infantry_div", sdt_skirmisher),
            (get_distance_between_positions, reg0, Infantry_Pos, Nearest_Enemy_Troop_Pos),
            (le, reg0, AI_charge_distance),
            (call_script, "script_formation_end", ":team_no", grc_infantry),
            (team_get_movement_order, reg0, ":team_no", grc_infantry),
            (try_begin),
              (neq, reg0, mordr_charge),
              (team_give_order, ":team_no", grc_infantry, mordr_charge),
            (try_end),

          #else attempt to make formation somewhere
          (else_try),
            (store_add, ":slot", slot_team_d0_formation, grc_infantry),
            (team_get_slot, ":infantry_formation", ":team_no", ":slot"),
            (team_get_leader, ":enemy_leader", ":enemy_agent_nearest_infantry_team"),

            #consider new formation
            (try_begin),
              (store_add, ":slot", slot_team_d0_is_fighting, grc_infantry),
              (this_or_next | le, ":infantry_formation", formation_none),
              (this_or_next | eq, ":infantry_formation", formation_default),
              (team_slot_eq, ":team_no", ":slot", 0),

              (call_script, "script_get_default_formation", ":team_no"),
              (assign, ":infantry_formation", reg0),
              (agent_get_class, ":enemy_nearest_troop_class", ":enemy_agent_nearest_infantry"),

              (assign, ":num_enemy_cavalry", 0),
              (try_for_range, ":enemy_team_no", 0, 4),
                (teams_are_enemies, ":enemy_team_no", ":team_no"),
                (team_get_slot, ":value", ":enemy_team_no", slot_team_num_cavalry),
                (val_add, ":num_enemy_cavalry", ":value"),
              (try_end),

              (store_mul, ":percent_enemy_cavalry", ":num_enemy_cavalry", 100),
              (val_div, ":percent_enemy_cavalry", ":num_enemies"),
              (try_begin),
                (gt, ":infantry_formation", formation_none),
                (try_begin),
                  (gt, ":percent_enemy_cavalry", 66),
                  (assign, ":infantry_formation", formation_square),
                (else_try),
                  (neq, ":enemy_nearest_troop_class", grc_cavalry),
                  (neq, ":enemy_nearest_troop_class", grc_archers),
                  (neq, ":enemy_agent_nearest_infantry", ":enemy_leader"),
                  (ge, ":num_infantry", 21),
                  (store_add, ":slot", slot_team_d0_size, ":enemy_agent_nearest_infantry_div"),
                  (team_get_slot, reg0, ":enemy_agent_nearest_infantry_team", ":slot"),
                  (gt, reg0, ":num_infantry"),	#got fewer troops?
                  (store_add, ":slot", slot_team_d0_armor, grc_infantry),
                  (team_get_slot, ":average_armor", ":team_no", ":slot"),
                  (store_add, ":slot", slot_team_d0_armor, ":enemy_agent_nearest_infantry_div"),
                  (team_get_slot, reg0, ":enemy_agent_nearest_infantry_team", ":slot"),
                  (gt, ":average_armor", reg0),	#got better armor?
                  (assign, ":infantry_formation", formation_wedge),
                (try_end),
              (try_end),
            (try_end),	#consider new formation

            (try_begin),
              (call_script, "script_cf_battlegroup_valid_formation", ":team_no", grc_infantry, ":infantry_formation"),
              (store_add, ":slot", slot_team_d0_formation, grc_infantry),
              (team_set_slot, ":team_no", ":slot", ":infantry_formation"),

              #adjust spacing for long swung weapons
              (store_add, ":slot", slot_team_d0_swung_weapon_length, grc_infantry),
              (team_get_slot, ":spacing", ":team_no", ":slot"),
              (val_add, ":spacing", 25),	#rounding for 50cm
              (val_div, ":spacing", 50),
              (store_add, ":slot", slot_team_d0_formation_space, grc_infantry),
              (team_set_slot, ":team_no", ":slot", ":spacing"),

              (assign, ":place_leader_by_infantry", 1),

            (else_try),
              (call_script, "script_formation_end", ":team_no", grc_infantry),
              (team_get_movement_order, reg0, ":team_no", grc_infantry),
              (try_begin),
                (neq, reg0, ":infantry_order"),
                (team_give_order, ":team_no", grc_infantry, ":infantry_order"),
              (try_end),
              (eq, ":infantry_order", mordr_hold),
              (assign, ":place_leader_by_infantry", 1),
            (try_end),

            #hold near archers?
            (try_begin),
              (eq, ":infantry_order", mordr_hold),
              (gt, ":num_archers", 0),
              # (copy_position, pos1, Archers_Pos),
              (team_get_order_position, pos1, ":team_no", grc_archers),	#anticipate archers
              (position_move_x, pos1, -100, 0),
              (try_begin),
                (this_or_next | eq, ":enemy_agent_nearest_infantry_div", grc_cavalry),
                (gt, ":percent_level_infantry", ":percent_level_enemy_infantry"),
                (call_script, "script_battlegroup_dist_center_to_front", ":team_no", grc_infantry),	#make sure to clear archers
                (store_mul, ":distance_to_move", reg0, 2),
                (val_add, ":distance_to_move", 1000),
                (position_move_y, pos1, ":distance_to_move", 0),	#move ahead of archers in anticipation of charges
              (else_try),
                (position_move_y, pos1, -1000, 0),
              (try_end),

            #obtain destination
            (else_try),
              (assign, ":target_division", -1),
              (try_begin),
                (store_add, ":slot", slot_team_d0_is_fighting, grc_infantry),
                (team_slot_eq, ":team_no", ":slot", 0),	#not engaged?
                (gt, ":enemy_bg_nearest_archers_dist", AI_charge_distance),	#don't have to protect archers?
                # (lt, ":percent_enemy_cavalry", 100), #non-cavalry exist?  MOTO next
                # command tests

                #prefer non-cavalry target (that infantry can catch)
                (store_add, ":slot", slot_team_d0_closest_enemy_special_dist, grc_infantry),
                (team_get_slot, ":distance_to_enemy_troop", ":team_no", ":slot"),
                (gt, ":distance_to_enemy_troop", 0),
                (store_add, ":slot", slot_team_d0_closest_enemy_special, grc_infantry),
                (team_get_slot, ":enemy_nearest_non_cav_agent", ":team_no", ":slot"),
                (gt, ":enemy_nearest_non_cav_agent", 0),
                (agent_get_position, pos60, ":enemy_nearest_non_cav_agent"),
                (agent_get_team, ":enemy_non_cav_team", ":enemy_nearest_non_cav_agent"),
                (team_get_leader, reg0, ":enemy_non_cav_team"),
                (try_begin),
                  (eq, ":enemy_nearest_non_cav_agent", reg0),	#team leader?
                  (assign, ":distance_to_enemy_group", Far_Away),
                (else_try),
                  (agent_get_division, ":target_division", ":enemy_nearest_non_cav_agent"),
                  (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
                  (team_set_slot, ":team_no", ":slot", ":enemy_non_cav_team"),
                  (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
                  (team_set_slot, ":team_no", ":slot", ":target_division"),
                  (call_script, "script_battlegroup_get_attack_destination", pos1, ":team_no", grc_infantry, ":enemy_non_cav_team", ":target_division"),
                  (call_script, "script_get_distance_to_battlegroup", ":enemy_non_cav_team", ":target_division", Infantry_Pos),
                  (assign, ":distance_to_enemy_group", reg0),
                (try_end),

              #chase nearest target
              (else_try),
                (assign, ":distance_to_enemy_troop", ":enemy_agent_nearest_infantry_dist"),
                (copy_position, pos60, Nearest_Enemy_Troop_Pos),
                (try_begin),
                  (eq, ":enemy_agent_nearest_infantry", ":enemy_leader"),
                  (assign, ":distance_to_enemy_group", Far_Away),
                (else_try),
                  (assign, ":target_division", ":enemy_agent_nearest_infantry_div"),
                  (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
                  (team_set_slot, ":team_no", ":slot", ":enemy_agent_nearest_infantry_team"),
                  (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
                  (team_set_slot, ":team_no", ":slot", ":target_division"),
                  (call_script, "script_battlegroup_get_attack_destination", pos1, ":team_no", grc_infantry, ":enemy_agent_nearest_infantry_team", ":target_division"),
                  (call_script, "script_get_distance_to_battlegroup", ":enemy_agent_nearest_infantry_team", ":target_division", Infantry_Pos),
                  (assign, ":distance_to_enemy_group", reg0),
                (try_end),
              (try_end),

              #reassemble if too scattered
              (try_begin),
                (call_script, "script_get_distance_to_battlegroup", ":team_no", grc_infantry, pos60),	#we're using enemy troop as a reference
                (val_sub, reg0, ":distance_to_enemy_troop"),
                (gt, reg0, 1500),	#division center too far from where it should be (probably because of
                #reinforcing troops)
                (position_copy_origin, pos1, Infantry_Pos),	#gather at average position
                (call_script, "script_battlegroup_dist_center_to_front", ":team_no", grc_infantry),
                (assign, ":distance_to_move", reg0),
                (store_mul, reg0, 350, formation_reform_interval),
                (val_add, ":distance_to_move", reg0),	#one interval movement
                (position_move_y, pos1, ":distance_to_move"),	#keep rear moving forward

              #attack leader if is closest troop
              (else_try),
                (eq, ":target_division", -1),
                (position_copy_origin, pos1, pos60),
                (call_script, "script_point_y_toward_position", Infantry_Pos, pos1),
                (position_copy_rotation, pos1, Infantry_Pos),

              #move no farther than nearest troop if its unit is far off
              (else_try),
                (call_script, "script_battlegroup_dist_center_to_front", ":team_no", grc_infantry),
                (val_add, ":distance_to_enemy_troop", reg0),	#distance to center of bg from nearest edge
                (store_sub, reg0, ":distance_to_enemy_group", ":distance_to_enemy_troop"),
                (gt, reg0, AI_charge_distance),
                (position_copy_origin, pos1, Infantry_Pos),
                (position_move_y, pos1, ":distance_to_enemy_troop"),

              #shift dead player troops right to clear allies when both attacking the
              #same enemy battlegroup
              (else_try),
                (eq, ":team_no", "$fplayer_team_no"),
                (store_add, ":ally_team", "$fplayer_team_no", 2),
                (neg | teams_are_enemies, ":ally_team", "$fplayer_team_no"),
                (store_add, ":slot", slot_team_d0_size, grc_infantry),
                (team_slot_ge, ":ally_team", ":slot", 1),
                (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
                (team_get_slot, ":target_team", "$fplayer_team_no", ":slot"),
                (team_slot_eq, ":ally_team", ":slot", ":target_team"),
                (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
                (team_slot_eq, ":ally_team", ":slot", ":target_division"),
                (call_script, "script_battlegroup_get_position", pos0, ":ally_team", grc_infantry),
                (get_distance_between_positions, ":distance_to_ally", Infantry_Pos, pos0),
                (lt, ":distance_to_ally", ":distance_to_enemy_group"),	#shift only when not in melee to avoid rotation
                (call_script, "script_battlegroup_get_action_radius", ":ally_team", grc_infantry),	#move larger group less to maintain center
                (val_div, reg0, 2),	#function returns length of bg
                (position_move_x, pos1, reg0),

              #shift allies left to clear dead player troops when both attacking the
              #same enemy battlegroup
              (else_try),
                (main_hero_fallen),
                (eq, AI_Replace_Dead_Player, 1),
                (neq, ":team_no", "$fplayer_team_no"),
                (neg | teams_are_enemies, ":team_no", "$fplayer_team_no"),
                (store_add, ":slot", slot_team_d0_size, grc_infantry),
                (team_slot_ge, "$fplayer_team_no", ":slot", 1),
                (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
                (team_get_slot, ":target_team", "$fplayer_team_no", ":slot"),
                (team_slot_eq, ":team_no", ":slot", ":target_team"),
                (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
                (team_slot_eq, "$fplayer_team_no", ":slot", ":target_division"),
                (call_script, "script_battlegroup_get_position", pos0, "$fplayer_team_no", grc_infantry),
                (get_distance_between_positions, ":distance_to_ally", Infantry_Pos, pos0),
                (lt, ":distance_to_ally", ":distance_to_enemy_group"),	#shift only when not in melee to avoid rotation
                (call_script, "script_battlegroup_get_action_radius", "$fplayer_team_no", grc_infantry),	#move larger group less to maintain center
                (val_div, reg0, -2),	#function returns length of bg
                (position_move_x, pos1, reg0),
              (try_end),
            (try_end),	#obtain destination

            (call_script, "script_set_formation_destination", ":team_no", grc_infantry, pos1),

            (try_begin),
              (store_add, ":slot", slot_team_d0_formation, grc_infantry),
              (neg | team_slot_eq, ":team_no", ":slot", formation_none),
              (team_slot_ge, ":team_no", ":slot", formation_none),
              (call_script, "script_get_centering_amount", ":infantry_formation", ":num_infantry", ":spacing"),
              (position_move_x, pos1, reg0),
              (call_script, "script_form_infantry", ":team_no", grc_infantry, ":team_leader", ":spacing", 0, ":infantry_formation"),
            (try_end),
          (try_end),	#attempt to make formation somewhere
        (try_end),

        #cavalry AI
        (try_begin),
          (gt, ":num_cavalry", 0),

          #get distance to nearest enemy battlegroup(s)
          (store_add, ":slot", slot_team_d0_armor, grc_cavalry),
          (team_get_slot, ":average_armor", ":team_no", ":slot"),
          (assign, ":nearest_threat_distance", Far_Away),
          (assign, ":nearest_target_distance", Far_Away),
          (assign, ":num_targets", 0),
          (try_for_range, ":enemy_team_no", 0, 4),
            (team_slot_ge, ":enemy_team_no", slot_team_size, 1),
            (teams_are_enemies, ":enemy_team_no", ":team_no"),
            (try_for_range, ":enemy_division", 0, 9),
              (store_add, ":slot", slot_team_d0_size, ":enemy_division"),
              (team_get_slot, ":size_enemy_battle_group", ":enemy_team_no", ":slot"),
              (gt, ":size_enemy_battle_group", 0),
              (call_script, "script_battlegroup_get_position", pos0, ":enemy_team_no", ":enemy_division"),
              (get_distance_between_positions, ":distance_of_enemy", Cavalry_Pos, pos0),
              (try_begin),	#threat or target?
                (store_add, ":slot", slot_team_d0_weapon_length, ":enemy_division"),
                (team_get_slot, reg0, ":enemy_team_no", ":slot"),
                (assign, ":decision_index", reg0),
                (store_add, ":slot", slot_team_d0_armor, ":enemy_division"),
                (team_get_slot, reg0, ":enemy_team_no", ":slot"),
                (val_mul, ":decision_index", reg0),
                (val_mul, ":decision_index", ":size_enemy_battle_group"),
                (val_div, ":decision_index", ":average_armor"),
                (val_div, ":decision_index", ":num_cavalry"),
                (try_begin),
                  (neq, ":enemy_division", grc_cavalry),
                  (val_div, ":decision_index", 2),	#double count cavalry vs.  foot soldiers
                (try_end),
                (gt, ":decision_index", 100),
                (try_begin),
                  (gt, ":nearest_threat_distance", ":distance_of_enemy"),
                  (copy_position, Nearest_Threat_Pos, pos0),
                  (assign, ":nearest_threat_distance", ":distance_of_enemy"),
                (try_end),
              (else_try),
                (val_add, ":num_targets", 1),
                (gt, ":nearest_target_distance", ":distance_of_enemy"),
                (copy_position, Nearest_Target_Pos, pos0),
                (assign, ":nearest_target_distance", ":distance_of_enemy"),
                (store_add, ":slot", slot_team_d0_target_team, grc_cavalry),
                (team_set_slot, ":team_no", ":slot", ":enemy_team_no"),
                (store_add, ":slot", slot_team_d0_target_division, grc_cavalry),
                (team_set_slot, ":team_no", ":slot", ":enemy_division"),
              (try_end),
            (try_end),
          (try_end),
          (try_begin),
            (eq, ":nearest_threat_distance", Far_Away),
            (assign, ":nearest_target_guarded", 0),
          (else_try),
            (eq, ":nearest_target_distance", Far_Away),
            (assign, ":nearest_target_guarded", 1),
          (else_try),
            (get_distance_between_positions, reg0, Nearest_Target_Pos, Nearest_Threat_Pos),
            (store_div, reg1, AI_charge_distance, 2),
            (try_begin),	#ignore target too close to threat
              (le, reg0, reg1),
              (assign, ":nearest_target_guarded", 1),
            (else_try),
              (assign, ":nearest_target_guarded", 0),
            (try_end),
          (try_end),

          (assign, ":cavalry_order", mordr_charge), ##CABA HERE
          (try_begin),
            (teams_are_enemies, ":team_no", 0),
            (neg | team_slot_ge, 1, slot_team_reinforcement_stage, AI_Max_Reinforcements),
            (neg | team_slot_eq, 1, slot_team_reinforcement_stage, "$attacker_reinforcement_stage"),
            (assign, ":cavalry_order", mordr_hold),
          (else_try),
            (teams_are_enemies, ":team_no", 1),
            (neg | team_slot_ge, 0, slot_team_reinforcement_stage, AI_Max_Reinforcements),
            (neg | team_slot_eq, 0, slot_team_reinforcement_stage, "$defender_reinforcement_stage"),
            (assign, ":cavalry_order", mordr_hold),
          (else_try),
            (neq, ":infantry_order", mordr_charge),
            (try_begin),
              (le, "$battle_phase", BP_Jockey),
              (assign, ":cavalry_order", mordr_hold),
            (else_try),
              (eq, ":nearest_target_distance", Far_Away),
              (try_begin),
                (eq, ":num_archers", 0),
                (assign, ":distance_to_archers", 0),
              (else_try),
                (get_distance_between_positions, ":distance_to_archers", Cavalry_Pos, Archers_Pos),
              (try_end),
              (try_begin),
                (this_or_next | gt, ":enemy_agent_nearest_cavalry_dist", AI_charge_distance),
                (gt, ":distance_to_archers", AI_charge_distance),
                (assign, ":cavalry_order", mordr_hold),
              (try_end),
            (try_end),
          (try_end),

          (try_begin),
            (eq, ":team_no", 0),
            (assign, ":cav_destination", Team0_Cavalry_Destination),
          (else_try),
            (eq, ":team_no", 1),
            (assign, ":cav_destination", Team1_Cavalry_Destination),
          (else_try),
            (eq, ":team_no", 2),
            (assign, ":cav_destination", Team2_Cavalry_Destination),
          (else_try),
            (eq, ":team_no", 3),
            (assign, ":cav_destination", Team3_Cavalry_Destination),
          (try_end),
          (store_add, ":slot", slot_team_d0_percent_ranged, grc_cavalry),
          (team_get_slot, reg0, ":team_no", ":slot"),

          #horse archers don't use wedge
          (try_begin),
            (ge, reg0, 50),
            (call_script, "script_formation_end", ":team_no", grc_cavalry),
            (try_begin),
              (eq, ":num_archers", 0),
              (team_get_movement_order, reg0, ":team_no", grc_cavalry),
              (try_begin),
                (neq, reg0, mordr_charge),
                (team_give_order, ":team_no", grc_cavalry, mordr_charge),
              (try_end),
            (else_try),
              (team_get_movement_order, reg0, ":team_no", grc_cavalry),
              (try_begin),
                (neq, reg0, ":cavalry_order"),
                (team_give_order, ":team_no", grc_cavalry, ":cavalry_order"),
              (try_end),
              (copy_position, ":cav_destination", Archers_Pos),
              (position_move_y, ":cav_destination", -500, 0),
              (call_script, "script_set_formation_destination", ":team_no", grc_cavalry, ":cav_destination"),
            (try_end),

          #close in with no unguarded target farther off, free fight
          (else_try),
            (eq, ":cavalry_order", mordr_charge),
            (this_or_next | eq, ":num_archers", 0),
            (le, ":enemy_agent_nearest_cavalry_dist", AI_charge_distance),
            (try_begin),
              (eq, ":num_targets", 1),
              (eq, ":nearest_target_guarded", 0),
              (gt, ":nearest_target_distance", ":nearest_threat_distance"),
              (assign, reg0, 0),
            (else_try),
              (ge, ":num_targets", 2),
              (eq, ":nearest_target_guarded", 1),
              (assign, reg0, 0),
            (else_try),
              (assign, reg0, 1),
            (try_end),
            (eq, reg0, 1),
            (call_script, "script_formation_end", ":team_no", grc_cavalry),
            (team_get_movement_order, reg0, ":team_no", grc_cavalry),
            (try_begin),
              (neq, reg0, mordr_charge),
              (team_give_order, ":team_no", grc_cavalry, mordr_charge),
            (try_end),

          #grand charge if target closer than threat AND not guarded
          (else_try),
            (lt, ":nearest_target_distance", ":nearest_threat_distance"),
            (eq, ":nearest_target_guarded", 0),
            (call_script, "script_formation_end", ":team_no", grc_cavalry),
            (team_get_movement_order, reg0, ":team_no", grc_cavalry),
            (try_begin),
              (neq, reg0, mordr_hold),
              (team_give_order, ":team_no", grc_cavalry, mordr_hold),
            (try_end),

            #lead archers up to firing point
            (try_begin),
              (gt, ":nearest_target_distance", AI_firing_distance),
              (eq, ":cavalry_order", mordr_hold),
              (try_begin),
                (eq, ":num_archers", 0),
                (copy_position, ":cav_destination", Cavalry_Pos),	#must be reinforcements, so gather at average position
              (else_try),
                (copy_position, ":cav_destination", Archers_Pos),
                (position_move_y, ":cav_destination", AI_charge_distance, 0),
              (try_end),

            #then CHARRRRGE!
            (else_try),
              (copy_position, ":cav_destination", Cavalry_Pos),
              (call_script, "script_point_y_toward_position", ":cav_destination", Nearest_Target_Pos),
              (position_move_y, ":cav_destination", ":nearest_target_distance", 0),
            (try_end),
            (call_script, "script_set_formation_destination", ":team_no", grc_cavalry, ":cav_destination"),

          #make a wedge somewhere
          (else_try),
            (try_begin),
              (eq, ":cavalry_order", mordr_charge),
              (neq, ":nearest_target_distance", Far_Away),
              (copy_position, ":cav_destination", Cavalry_Pos),
              (call_script, "script_point_y_toward_position", ":cav_destination", Nearest_Target_Pos),
              (position_move_y, ":cav_destination", ":nearest_target_distance", 0),
              (position_move_y, ":cav_destination", AI_charge_distance, 0),	#charge on through to the other side
            (else_try),
              (neq, ":cavalry_order", mordr_charge),
              (eq, ":num_archers", 0),
              (copy_position, ":cav_destination", Cavalry_Pos),	#must be reinforcements, so gather at average position
            (else_try),
              (copy_position, ":cav_destination", Archers_Pos),	#hold near archers
              (position_move_x, ":cav_destination", 500, 0),
              (position_move_y, ":cav_destination", -1000, 0),
            (try_end),

            #move around threat in the way to destination
            (try_begin),
              (neq, ":nearest_threat_distance", Far_Away),
              (call_script, "script_point_y_toward_position", Cavalry_Pos, Nearest_Threat_Pos),
              (call_script, "script_point_y_toward_position", Nearest_Threat_Pos, ":cav_destination"),
              (position_get_rotation_around_z, reg0, Cavalry_Pos),
              (position_get_rotation_around_z, reg1, Nearest_Threat_Pos),
              (store_sub, ":rotation_diff", reg0, reg1),
              (try_begin),
                (lt, ":rotation_diff", -180),
                (val_add, ":rotation_diff", 360),
              (else_try),
                (gt, ":rotation_diff", 180),
                (val_sub, ":rotation_diff", 360),
              (try_end),

              (try_begin),
                (is_between, ":rotation_diff", -135, 136),
                (copy_position, ":cav_destination", Cavalry_Pos),
                (assign, ":distance_to_move", AI_firing_distance),
                (try_begin),	#target is left of threat
                  (is_between, ":rotation_diff", -135, 0),
                  (val_mul, ":distance_to_move", -1),
                (try_end),
                (position_move_x, ":cav_destination", ":distance_to_move", 0),
                (store_sub, ":distance_to_move", ":nearest_threat_distance", AI_firing_distance),
                (position_move_y, ":cav_destination", ":distance_to_move", 0),
                (call_script, "script_point_y_toward_position", ":cav_destination", Cavalry_Pos),
                (position_rotate_z, ":cav_destination", 180),
              (try_end),
            (try_end),
            (get_scene_boundaries, pos0, pos1),
            (position_get_x, reg0, ":cav_destination"),
            (position_get_x, reg1, pos0),
            (val_max, reg0, reg1),
            (position_get_x, reg1, pos1),
            (val_min, reg0, reg1),
            (position_set_x, ":cav_destination", reg0),
            (position_get_y, reg0, ":cav_destination"),
            (position_get_y, reg1, pos0),
            (val_max, reg0, reg1),
            (position_get_y, reg1, pos1),
            (val_min, reg0, reg1),
            (position_set_y, ":cav_destination", reg0),
            (position_set_z_to_ground_level, ":cav_destination"),

            (try_begin),
              (call_script, "script_cf_battlegroup_valid_formation", ":team_no", grc_cavalry, formation_wedge),
              (copy_position, pos1, ":cav_destination"),
              (call_script, "script_form_cavalry", ":team_no", grc_cavalry, ":team_leader", 0, 0),
              (store_add, ":slot", slot_team_d0_formation, grc_cavalry),
              (team_set_slot, ":team_no", ":slot", formation_wedge),
              # (team_give_order, ":team_no", grc_cavalry, mordr_hold),
            (else_try),
              (call_script, "script_formation_end", ":team_no", grc_cavalry),
              (team_get_movement_order, reg0, ":team_no", grc_cavalry),
              (try_begin),
                (neq, reg0, ":cavalry_order"),
                (team_give_order, ":team_no", grc_cavalry, ":cavalry_order"),
              (try_end),
            (try_end),
            (call_script, "script_set_formation_destination", ":team_no", grc_cavalry, ":cav_destination"),
          (try_end),
        (try_end),

        #place leader
        (try_begin),
          (ge, ":team_leader", 0),
          (agent_is_alive, ":team_leader"),
          (agent_slot_eq, ":team_leader", slot_agent_is_running_away, 0),
          (try_begin),
            (le, ":num_infantry", 0),
            (try_begin),
              (this_or_next | le, ":num_archers", 0),
              (eq, ":archer_order", mordr_retreat),

              (assign, ":more_reinforcements", 1),
              (try_begin),
                (teams_are_enemies, ":team_no", 0),
                (team_slot_ge, 1, slot_team_reinforcement_stage, AI_Max_Reinforcements),
                (assign, ":more_reinforcements", 0),
              (else_try),
                (teams_are_enemies, ":team_no", 1),
                (team_slot_ge, 0, slot_team_reinforcement_stage, AI_Max_Reinforcements),
                (assign, ":more_reinforcements", 0),
              (try_end),
              (eq, ":more_reinforcements", 0),

              (agent_get_troop_id, ":troop_id", ":team_leader"), #for now do not let heroes to run away from battle
              (neg|troop_is_hero, ":troop_id"),
              (agent_clear_scripted_mode, ":team_leader"),
              (agent_start_running_away, ":team_leader"),
              (agent_set_slot, ":team_leader",  slot_agent_is_running_away, 1),
            (else_try),
              (eq, ":archer_order", mordr_charge),
              (agent_clear_scripted_mode, ":team_leader"),
            (else_try),
              (copy_position, pos1, Archers_Pos),
              (position_move_y, pos1, -1000, 0),
              (agent_set_scripted_destination, ":team_leader", pos1, 1),
            (try_end),
          (else_try),
            (neq, ":place_leader_by_infantry", 0),
            (call_script, "script_battlegroup_get_position", pos1, ":team_no", grc_infantry),
            (team_get_order_position, pos0, ":team_no", grc_infantry),
            (call_script, "script_point_y_toward_position", pos1, pos0),
            (call_script, "script_battlegroup_get_action_radius", ":team_no", grc_infantry),
            (val_div, reg0, 2),	#bring to edge of battlegroup
            (position_move_x, pos1, reg0, 0),
            (position_move_x, pos1, 100, 0),
            (agent_set_scripted_destination, ":team_leader", pos1, 1),
          (else_try),
            (agent_clear_scripted_mode, ":team_leader"),
          (try_end),
        (try_end),
      (try_end),

  ]),

("field_tactics", [
      (store_script_param, ":include_ranged", 1),

      (assign, ":largest_team_size", 0),
      (assign, ":battle_size", 0),
      (try_for_range, ":ai_team", 0, 4),
        (team_get_slot, ":team_size", ":ai_team", slot_team_size),
        (gt, ":team_size", 0),
        (team_get_slot, ":team_cav_size", ":ai_team", slot_team_num_cavalry),
        (store_add, ":team_adj_size", ":team_size", ":team_cav_size"),	#double count cavalry to capture effect on battlefield
        (val_add, ":battle_size", ":team_adj_size"),

        (try_begin),
          (neq, ":ai_team", "$fplayer_team_no"),
          (neg | teams_are_enemies, ":ai_team", "$fplayer_team_no"),
          (team_get_slot, ":player_team_adj_size", "$fplayer_team_no", slot_team_adj_size),
          (val_add, ":team_adj_size", ":player_team_adj_size"),	#ally team takes player team into account
          (team_set_slot, "$fplayer_team_no", slot_team_adj_size, ":team_adj_size"),	#and vice versa
        (try_end),
        (team_set_slot, ":ai_team", slot_team_adj_size, ":team_adj_size"),

        (lt, ":largest_team_size", ":team_adj_size"),
        (assign, ":largest_team_size", ":team_adj_size"),
      (try_end),

      #apply tactics to every AI team
      (set_show_messages, 0),
      (try_for_range, ":ai_team", 0, 4),
        (team_get_slot, ":ai_team_size", ":ai_team", slot_team_adj_size),
        (gt, ":ai_team_size", 0),

        (assign, ":do_it", 0),
        (try_begin),
          (neq, ":ai_team", "$fplayer_team_no"),
          (assign, ":do_it", 1),
        (else_try),
          (main_hero_fallen),    #have AI take over for mods with post-player battle action
          (eq, AI_Replace_Dead_Player, 1),
          (assign, ":do_it", 1),
        (try_end),
        (eq, ":do_it", 1),

        (team_get_slot, ":ai_faction", ":ai_team", slot_team_faction),
        (try_begin),
          (neq, AI_for_kingdoms_only, 0),
          (neq, ":ai_faction", fac_deserters),	#deserters have military training
          (neq, ":ai_faction", fac_black_khergits),
          (neq, ":ai_faction", fac_dark_knights),
          #(neq, ":ai_faction", fac_mountain_bandits),	#scoti, frank and dena pirates have military training Chief anade
          (neg | is_between, ":ai_faction", kingdoms_begin, kingdoms_end),

          (call_script, "script_formation_end", ":ai_team", grc_everyone),
          (team_get_movement_order, reg0, ":ai_team", grc_everyone),
          (try_begin),
            (neq, reg0, mordr_charge),
            (team_give_order, ":ai_team", grc_everyone, mordr_charge),
          (try_end),

        #uses tactics
        (else_try),
          (val_mul, ":ai_team_size", 100),
          (store_div, ":team_percentage", ":ai_team_size", ":largest_team_size"),
          (store_div, ":team_battle_presence", ":ai_team_size", ":battle_size"),
          (try_begin),
            (eq, ":include_ranged", 1),
            (try_begin),
              (store_mod, ":team_phase", ":ai_team", 2),
              (eq, ":team_phase", 0),
              (assign, ":time_slice", 0),
            (else_try),
              (store_div, ":time_slice", Reform_Trigger_Modulus, 2),
            (try_end),

            (store_mod, reg0, "$ranged_clock", Reform_Trigger_Modulus),
            (this_or_next | eq, reg0, ":time_slice"),
            (eq, "$battle_phase", BP_Setup),
            (call_script, "script_team_field_ranged_tactics", ":ai_team", ":team_percentage", ":team_battle_presence"),
          (try_end),

          (try_begin),
            (gt, "$fplayer_team_no", 0),	#not a spectator
            (neg | main_hero_fallen),
            (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
            (team_slot_eq, ":ai_team", ":slot", "$fplayer_team_no"),
            (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
            (team_get_slot, ":enemy_division", ":ai_team", ":slot"),
            (store_add, ":slot", slot_team_d0_size, ":enemy_division"),
            (team_slot_ge, "$fplayer_team_no", ":slot", 1),
            (store_add, ":slot", slot_team_d0_fclock, ":enemy_division"),
            (team_get_slot, ":fclock", "$fplayer_team_no", ":slot"),
            (store_mod, reg0, ":fclock", Reform_Trigger_Modulus),
            (store_div, ":time_slice", Reform_Trigger_Modulus, 2),
          (else_try),
            (store_mod, reg0, "$ranged_clock", Reform_Trigger_Modulus),
            (store_mod, ":team_phase", ":ai_team", 2),
            (eq, ":team_phase", 0),
            (assign, ":time_slice", 0),
          (else_try),
            (store_div, ":time_slice", Reform_Trigger_Modulus, 2),
          (try_end),

          (eq, reg0, ":time_slice"),
          (call_script, "script_team_field_melee_tactics", ":ai_team", ":team_percentage", ":team_battle_presence"),
        (try_end),
      (try_end),
      (set_show_messages, 1),]),

("find_high_ground_around_pos1_corrected", [
      (store_script_param, ":destination_pos", 1),
      (store_script_param, ":search_radius", 2),
      (assign, ":fixed_point_multiplier", 1),
      (convert_to_fixed_point, ":fixed_point_multiplier"),
      (set_fixed_point_multiplier, 1),

      (position_get_x, ":o_x", pos1),
      (position_get_y, ":o_y", pos1),
      (store_sub, ":min_x", ":o_x", ":search_radius"),
      (store_sub, ":min_y", ":o_y", ":search_radius"),
      (store_add, ":max_x", ":o_x", ":search_radius"),
      (store_add, ":max_y", ":o_y", ":search_radius"),

      (get_scene_boundaries, ":destination_pos", pos0),
      (position_get_x, ":scene_min_x", ":destination_pos"),
      (position_get_x, ":scene_max_x", pos0),
      (position_get_y, ":scene_min_y", ":destination_pos"),
      (position_get_y, ":scene_max_y", pos0),
      (val_max, ":min_x", ":scene_min_x"),
      (val_max, ":min_y", ":scene_min_y"),
      (val_min, ":max_x", ":scene_max_x"),
      (val_min, ":max_y", ":scene_max_y"),

      (assign, ":highest_pos_z", -100),
      (copy_position, ":destination_pos", pos1),
      (init_position, pos0),

      (try_for_range, ":i_x", ":min_x", ":max_x"),
        (try_for_range, ":i_y", ":min_y", ":max_y"),
          (position_set_x, pos0, ":i_x"),
          (position_set_y, pos0, ":i_y"),
          (position_set_z_to_ground_level, pos0),
          (position_get_z, ":cur_pos_z", pos0),
          (try_begin),
            (gt, ":cur_pos_z", ":highest_pos_z"),
            (copy_position, ":destination_pos", pos0),
            (assign, ":highest_pos_z", ":cur_pos_z"),
          (try_end),
        (try_end),
      (try_end),

      (set_fixed_point_multiplier, ":fixed_point_multiplier"),]),

("get_nearest_enemy_battlegroup_location", [
      (store_script_param, ":bgposition", 1),
      (store_script_param, ":team_no", 2),
      (store_script_param, ":from_pos", 3),
      (assign, ":distance_to_nearest_enemy_battlegoup", Far_Away),
      (try_for_range, ":enemy_team_no", 0, 4),
        (team_slot_ge, ":enemy_team_no", slot_team_size, 1),
        (teams_are_enemies, ":enemy_team_no", ":team_no"),
        (try_for_range, ":enemy_division", 0, 9),
          (store_add, ":slot", slot_team_d0_size, ":enemy_division"),
          (team_slot_ge, ":enemy_team_no", ":slot", 1),
          (call_script, "script_battlegroup_get_position", pos0, ":enemy_team_no", ":enemy_division"),
          (get_distance_between_positions, reg0, pos0, ":from_pos"),
          (try_begin),
            (gt, ":distance_to_nearest_enemy_battlegoup", reg0),
            (assign, ":distance_to_nearest_enemy_battlegoup", reg0),
            (copy_position, ":bgposition", pos0),
          (try_end),
        (try_end),
      (try_end),
      (assign, reg0, ":distance_to_nearest_enemy_battlegoup")]),

("find_nearest_enemy_position",
		[
			(store_script_param, ":agent", 1),
			(store_script_param, ":agent_team", 2),
			(store_script_param, ":threshold", 3), #if under threshold then stop searching
			(assign, ":nearest_dist", 100000),
			(assign, ":nearest_agent", -1),
			(agent_get_position, pos1, ":agent"),
			(try_for_agents, ":agent2"),
				(gt, ":nearest_dist", ":threshold"),
				(agent_is_alive, ":agent2"),
				(agent_is_active, ":agent2"),
				(agent_is_human, ":agent2"),
				(agent_get_team, ":agent2_team", ":agent2"),
				(teams_are_enemies, ":agent2_team", ":agent_team"),
				(agent_get_position, pos2, ":agent2"),
				(get_distance_between_positions, ":enemy_dist", pos2, pos1),
				(lt, ":enemy_dist", ":nearest_dist"),
				(assign, ":nearest_agent", ":agent2"),
				(assign, ":nearest_dist", ":enemy_dist"),
			(try_end),
			(assign, reg1, ":nearest_dist"),
			(assign, reg4, ":nearest_agent")
		]),

("horse_archer_skirmish",
		[
			(store_script_param, ":agent", 1), #agent
			(store_script_param, ":enemy_agent", 2), #enemy agent
			(store_script_param, ":enemy_dist", 3), #distance from enemy
			(store_script_param, ":min_dist", 4), #min distance (inner radius)
			(store_script_param, ":max_dist", 5), #max distance (outer radius)
			(store_script_param, ":script_param_6", 6), #new position adder
			(try_begin),
				(assign, ":min_dist_from_enemy", ":min_dist"),
				(gt, ":enemy_agent", 0),
				(agent_get_position, pos0, ":agent"),
				(agent_get_position, pos1, ":enemy_agent"),
				# (agent_get_slot, ":skirmish_direction", ":agent", 106), #1/2 agents go clockwise
				(agent_get_slot, ":dist_to_add", ":agent", slot_agent_make_dist_with_enemy),
				# (try_begin),
					# (eq, ":skirmish_direction", 0),
					# (store_random_in_range, ":skirmish_direction", 1, 3),
					# (agent_set_slot, ":agent", 106, ":skirmish_direction"),
				# (try_end),
				(try_begin),
					(le, ":enemy_dist", ":max_dist"),
					(val_add, ":dist_to_add", ":script_param_6"),
					(try_begin),
						(ge, ":dist_to_add", 360),
						(assign, ":dist_to_add", 0),
					(try_end),
					(agent_set_slot, ":agent", slot_agent_make_dist_with_enemy, ":dist_to_add"),
					# (try_begin),
						# (eq, ":skirmish_direction", 1),
						# (val_mul, ":dist_to_add", -1),
						# (val_sub, ":min_dist_from_enemy", 1500), #clockwise agents stay closer to enemy
					# (try_end),
					(position_get_rotation_around_z, reg1, 1),
					(store_sub, reg0, 360, reg1),
					(val_add, ":dist_to_add", reg0),
					(position_rotate_z, pos1, ":dist_to_add"),
					(position_move_x, pos1, ":min_dist_from_enemy", 0),
					(agent_set_scripted_destination, ":agent", pos1, 1), #no rethink?
					(agent_set_slot, ":agent", slot_agent_is_skirmishing, 1),
				(else_try),
					(agent_clear_scripted_mode, ":agent"),
					(agent_set_slot, ":agent", slot_agent_is_skirmishing, 0),
				(try_end),
			(try_end)
		]),
]