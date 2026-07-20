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

multiplayer_find_spawn_point_2_scripts = [
# script_multiplayer_find_spawn_point_2
# Input: arg1 = team_no, arg2 = examine_all_spawn_points, arg3 = is_horseman
# Output: reg0 = entry_point_no
("multiplayer_find_spawn_point_2",
   [
     (store_script_param, ":team_no", 1),
     (store_script_param, ":examine_all_spawn_points", 2), #0-dm, 1-tdm, 2-cf, 3-hq, 4-sg
     (store_script_param, ":is_horseman", 3), #0:no, 1:yes, -1:do not care

     (assign, ":best_entry_point_score", -10000000),
     (assign, ":best_entry_point", 0),

     (assign, ":num_operations", 0),

     (assign, ":num_human_agents_div_3_plus_one", 0),
     (try_begin), #counting number of agents
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
       (try_for_agents, ":i_agent"),
         (agent_is_alive, ":i_agent"),
         (agent_is_human, ":i_agent"),
         (val_add, ":num_human_agents_div_3_plus_one", 1),
       (try_end),
     (try_end),

     (assign, ":num_human_agents_plus_one", ":num_human_agents_div_3_plus_one"),

     (try_begin),
       (le, ":num_human_agents_plus_one", 4),
       (assign, ":random_number_upper_limit", 2), #this is not typo-mistake this should be 2 too, not 1.
     (else_try),
       (le, ":num_human_agents_plus_one", 8),
       (assign, ":random_number_upper_limit", 2),
     (else_try),
       (le, ":num_human_agents_plus_one", 16),
       (assign, ":random_number_upper_limit", 3),
     (else_try),
       (le, ":num_human_agents_plus_one", 24),
       (assign, ":random_number_upper_limit", 4),
     (else_try),
       (le, ":num_human_agents_plus_one", 32),
       (assign, ":random_number_upper_limit", 5),
     (else_try),
       (le, ":num_human_agents_plus_one", 40),
       (assign, ":random_number_upper_limit", 6),
     (else_try),
       (assign, ":random_number_upper_limit", 7),
     (try_end),

     (val_div, ":num_human_agents_div_3_plus_one", 3),
     (val_add, ":num_human_agents_div_3_plus_one", 1),
     (store_mul, ":negative_num_human_agents_div_3_plus_one", ":num_human_agents_div_3_plus_one", -1),

     (try_begin),
       (eq, ":examine_all_spawn_points", 1),
       (assign, ":random_number_upper_limit", 1),
     (try_end),

     (try_begin), #counting number of our flags and enemy flags
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
       (assign, ":our_flag_count", 0),
       (assign, ":enemy_flag_count", 0),
       (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
         (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
         (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),
         (neq, ":cur_flag_owner", 0),
         (val_sub, ":cur_flag_owner", 1),
         (try_begin),
           (eq, ":cur_flag_owner", ":team_no"),
           (val_add, ":our_flag_count", 1),
         (else_try),
           (val_add, ":enemy_flag_count", 1),
         (try_end),
       (try_end),
     (try_end),

     (assign, ":first_agent", 0),
     (try_begin), #first spawned agents will be spawned at their base points in tdm, cf and hq mods.
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch),
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
       (try_begin),
         (eq, ":team_no", 0),
         (eq, "$g_multiplayer_team_1_first_spawn", 1),
         (assign, ":first_agent", 1),
         (assign, "$g_multiplayer_team_1_first_spawn", 0),
       (else_try),
         (eq, ":team_no", 1),
         (eq, "$g_multiplayer_team_2_first_spawn", 1),
         (assign, ":first_agent", 1),
         (assign, "$g_multiplayer_team_2_first_spawn", 0),
       (try_end),
     (try_end),

     (try_begin),
       (eq, ":first_agent", 1),
       (store_mul, ":best_entry_point", ":team_no", multi_num_valid_entry_points_div_2),
     (else_try),
       (try_for_range, ":i_entry_point", 0, multi_num_valid_entry_points),
         (assign, ":minimum_enemy_distance", 3000),
         (assign, ":second_minimum_enemy_distance", 3000),

         (assign, ":entry_point_score", 0),
         (store_random_in_range, ":random_value", 0, ":random_number_upper_limit"), #in average it is 5
         (eq, ":random_value", 0),
         (entry_point_get_position, pos0, ":i_entry_point"), #pos0 holds current entry point position
         (try_for_agents, ":i_agent"),
           (agent_is_alive, ":i_agent"),
           (agent_is_human, ":i_agent"),
           (agent_get_team, ":agent_team", ":i_agent"),
           (try_begin),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
             (try_begin),
               (teams_are_enemies, ":team_no", ":agent_team"),
               (assign, ":multiplier", -2),
             (else_try),
               (assign, ":multiplier", 1),
             (try_end),
           (else_try),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
             (assign, ":multiplier", -1),
           (try_end),
           (agent_get_position, pos1, ":i_agent"),
           (get_distance_between_positions_in_meters, ":distance", pos0, pos1),
           (val_add, ":num_operations", 1),
           (try_begin),
             (try_begin), #find closest enemy soldiers
               (lt, ":multiplier", 0),
               (try_begin),
                 (lt, ":distance", ":minimum_enemy_distance"),
                 (assign, ":second_minimum_enemy_distance", ":minimum_enemy_distance"),
                 (assign, ":minimum_enemy_distance", ":distance"),
               (else_try),
                 (lt, ":distance", ":second_minimum_enemy_distance"),
                 (assign, ":second_minimum_enemy_distance", ":distance"),
               (try_end),
             (try_end),

             (lt, ":distance", 100),
             (try_begin), #do not spawn over or too near to another agent (limit is 2 meters, squared 4 meters)
               (lt, ":distance", 3),
               (try_begin),
                 (this_or_next|eq, ":examine_all_spawn_points", 0),
                 (this_or_next|lt, ":multiplier", 0), #new added 20.08.08
                 (neq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
                 (try_begin),
                   (lt, ":distance", 1),
                   (assign, ":dist_point", -1000000), #never place
                 (else_try),
                   (lt, ":distance", 2),
                   (try_begin),
                     (lt, ":multiplier", 0),
                     (assign, ":dist_point", -20000),
                   (else_try),
                     (assign, ":dist_point", -2000), #can place, friend and distance is between 1-2 meters
                   (try_end),
                 (else_try),
                   (try_begin),
                     (lt, ":multiplier", 0),
                     (assign, ":dist_point", -10000),
                   (else_try),
                     (assign, ":dist_point", -1000), #can place, friend and distance is between 2-3 meters
                   (try_end),
                 (try_end),
               (else_try),
                 #if examinining all spawn points and mod is siege only. This happens in new round start placings.
                 (try_begin),
                   (lt, ":distance", 1),
                   (assign, ":dist_point", -20000), #very hard to place distance is < 1 meter
                 (else_try),
                   (lt, ":distance", 2),
                   (assign, ":dist_point", -2000),
                 (else_try),
                   (assign, ":dist_point", -1000), #can place, distance is between 2-3 meters
                 (try_end),
               (try_end),

               (val_mul, ":dist_point", ":num_human_agents_div_3_plus_one"),
             (else_try),
               (assign, ":dist_point", 0),
               (this_or_next|neq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
               (this_or_next|lt, ":multiplier", 0),
               (eq, ":team_no", 1), #only attackers are effected by positive enemy & friend distance at siege mod, defenders only get negative score effect a bit

               (try_begin), #in siege give no positive or negative score to > 40m distance. (6400 = 10000 - 3600(60 * 60))
                 (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

                 (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch), #new added after moving below part to above
                 (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel), #new added after moving below part to above
                 (eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch), #new added after moving below part to above

                 (store_sub, ":dist_point", multiplayer_spawn_min_enemy_dist_limit, ":distance"), #up to 40 meters give (positive(if friend) or negative(if enemy)) points
                 (val_max, ":dist_point", 0),
                 (val_mul, ":dist_point", ":dist_point"),
               (else_try),
                 (store_mul, ":one_and_half_limit", multiplayer_spawn_min_enemy_dist_limit, 3),
                 (val_div, ":one_and_half_limit", 2),
                 (store_sub, ":dist_point", ":one_and_half_limit", ":distance"), #up to 60 meters give (positive(if friend) or negative(if enemy)) points
                 (val_mul, ":dist_point", ":dist_point"),
               (try_end),

               (val_mul, ":dist_point", ":multiplier"),
             (try_end),
             (val_add, ":entry_point_score", ":dist_point"),
           (try_end),
         (try_end),

         (try_begin),
           (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
           (store_mul, ":max_enabled_agent_distance_score", 1000, ":num_human_agents_div_3_plus_one"),
           (ge, ":entry_point_score", ":max_enabled_agent_distance_score"),
           (assign, ":entry_point_score", ":max_enabled_agent_distance_score"),
         (try_end),

         (try_begin),
           (neq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

           #(assign, ":minimum_enemy_dist_score", 0), #close also these with displays
           #(assign, ":second_minimum_enemy_dist_score", 0), #close also these with displays
           #(assign, reg2, ":minimum_enemy_distance"), #close also these with displays
           #(assign, reg3, ":second_minimum_enemy_distance"), #close also these with displays

           (try_begin), #if minimum enemy dist score is greater than 40(multiplayer_spawn_above_opt_enemy_dist_point) meters then give negative score
             (lt, ":minimum_enemy_distance", 3000),
             (try_begin),
               (gt, ":minimum_enemy_distance", multiplayer_spawn_above_opt_enemy_dist_point),
               (val_sub, ":minimum_enemy_distance", multiplayer_spawn_above_opt_enemy_dist_point),
               (store_mul, ":minimum_enemy_dist_score", ":minimum_enemy_distance", -50),
               (val_mul, ":minimum_enemy_dist_score", ":num_human_agents_div_3_plus_one"),
               (val_add, ":entry_point_score", ":minimum_enemy_dist_score"),
             (try_end),
           (try_end),

           (try_begin), #if second minimum enemy dist score is greater than 40(multiplayer_spawn_above_opt_enemy_dist_point) meters then give negative score
             (lt, ":second_minimum_enemy_distance", 3000), #3000 x 3000
             (try_begin),
               (gt, ":second_minimum_enemy_distance", multiplayer_spawn_above_opt_enemy_dist_point),
               (val_sub, ":second_minimum_enemy_distance", multiplayer_spawn_above_opt_enemy_dist_point),
               (store_mul, ":second_minimum_enemy_dist_score", ":second_minimum_enemy_distance", -50),
               (val_mul, ":second_minimum_enemy_dist_score", ":num_human_agents_div_3_plus_one"),
               (val_add, ":entry_point_score", ":second_minimum_enemy_dist_score"),
             (try_end),
           (try_end),

           #(assign, reg0, ":minimum_enemy_dist_score"), #close also above assignment lines with these displays
           #(assign, reg1, ":second_minimum_enemy_dist_score"), #close also above assignment lines with these displays
           #(display_message, "@{!}minimum enemy distance : {reg2}, score : {reg0}"), #close also above assignment lines with these displays
           #(display_message, "@{!}second minimum enemy distance : {reg3}, score : {reg1}"), #close also above assignment lines with these displays
         (try_end),

         (try_begin), #giving positive points for "distance of entry point position to ground" while searching for entry point for defender team
           (neq, ":is_horseman", -1), #if being horseman or rider is not (not important)

           #additional score to entry points which has distance to ground value of > 0 meters
           (position_get_distance_to_terrain, ":height_to_terrain", pos0),
           (val_max, ":height_to_terrain", 0),
           (val_min, ":height_to_terrain", 300),
           (ge, ":height_to_terrain", 40),

           (store_mul, ":height_to_terrain_score", ":height_to_terrain", ":num_human_agents_div_3_plus_one"), #it was 8

           (try_begin),
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch),
             (val_mul, ":height_to_terrain_score", 16),
           (else_try),
             (val_mul, ":height_to_terrain_score", 4),
           (try_end),

           (try_begin),
             (eq, ":is_horseman", 0),
             (try_begin),
               (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege), #but only in siege mod, defender infantries will get positive points for spawning in high places.
               (eq, ":team_no", 0),
               (val_add, ":entry_point_score", ":height_to_terrain_score"),
             (try_end),
           (else_try),
             (val_mul, ":height_to_terrain_score", 5),
             (val_sub, ":entry_point_score", ":height_to_terrain_score"),
           (try_end),
         (try_end),

         (try_begin), #additional random entry point score at deathmatch, teamdethmatch, capture the flag and siege
           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
           (eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch),
           (try_begin),
             (neq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
             (store_random_in_range, ":random_value", 0, 400),

             (try_begin),
               (eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
               (val_mul, ":random_value", 5),
             (try_end),
           (else_try),
             (eq, ":team_no", 1),
             (store_random_in_range, ":random_value", 0, 600), #siege-attacker
           (else_try),
             (store_random_in_range, ":random_value", 0, 200), #siege-defender
           (try_end),
           (val_mul, ":random_value", ":num_human_agents_div_3_plus_one"),
           (val_add, ":entry_point_score", ":random_value"),
         (try_end),

         (try_begin),
           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
           (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

           (try_begin),
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
             (try_begin),
               (eq, ":team_no", 0),
               (entry_point_get_position, pos1, multi_base_point_team_1), #our base is at pos1
               (entry_point_get_position, pos2, multi_base_point_team_2), #enemy base is at pos2
             (else_try),
               (entry_point_get_position, pos1, multi_base_point_team_2), #our base is at pos2
               (entry_point_get_position, pos2, multi_base_point_team_1), #enemy base is at pos1
             (try_end),
           (else_try),
             (try_begin), #siege
               (eq, ":team_no", 0),
               (entry_point_get_position, pos1, multi_siege_flag_point), #our base is at pos1 (it was multi_initial_spawn_point_team_1 changed at v622)
               (entry_point_get_position, pos2, multi_initial_spawn_point_team_2), #enemy base is at pos2
             (else_try),
               (entry_point_get_position, pos1, multi_initial_spawn_point_team_2), #our base is at pos2
               (entry_point_get_position, pos2, multi_siege_flag_point), #enemy base is at pos1 (it was multi_initial_spawn_point_team_1 changed at v622)
             (try_end),
           (try_end),

           (try_begin),
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
             (position_get_z, ":pos0_z", pos0),
             (position_set_z, pos1, ":pos0_z"), #make z of our base same with entry point position z
             (position_set_z, pos2, ":pos0_z"), #make z of enemy base same with entry point position z
           (try_end),

           (get_sq_distance_between_positions_in_meters, ":sq_dist_to_our_base", pos0, pos1),
           (get_sq_distance_between_positions_in_meters, ":sq_dist_to_enemy_base", pos0, pos2),
           (get_distance_between_positions_in_meters, ":dist_to_enemy_base", pos0, pos2),

           #give positive points if this entry point is near to our base.
           (assign, ":dist_to_our_base_point", 0),
           (try_begin), #capture the flag (points for being near to base)
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),

             (get_distance_between_positions_in_meters, ":dist_to_our_base", pos0, pos1),
             (lt, ":dist_to_our_base", 100),
             (store_sub, ":dist_to_our_base_point", 100, ":dist_to_our_base"),

             (try_begin), #assign all 75-100's to 75
               (gt, ":dist_to_our_base_point", 75),
               (assign, ":dist_to_our_base_point", 75),
             (try_end),

             (val_mul, ":dist_to_our_base_point", 50), #0..5000 (increase is linear)

             (val_mul, ":dist_to_our_base_point", ":num_human_agents_div_3_plus_one"),
           (else_try), #siege (points for being near to base)
             (lt, ":sq_dist_to_our_base", 10000), #in siege give entry points score until 100m distance is reached
             (try_begin),
               (eq, ":team_no", 0),
               (try_begin),
                 (lt, ":sq_dist_to_our_base", 2500), #if distance is < 50m in siege give all highest point possible
                 (assign, ":sq_dist_to_our_base", 0),
               (else_try),
                 (val_sub, ":sq_dist_to_our_base", 2500),
                 (val_mul, ":sq_dist_to_our_base", 2),
               (try_end),
             (try_end),

             (store_sub, ":dist_to_our_base_point", 10000, ":sq_dist_to_our_base"),

             #can be (10000 - (10000 - 2500) * 2) = -5000 (for only defenders) so we are adding this loss.
             (val_add, ":dist_to_our_base_point", 5000), #so score getting from being near to base changes between 0 to 15000

             (try_begin),
               (eq, ":team_no", 0),
             (else_try), #in siege mod for attackers being near to base entry point has 45 times less importance
               (val_div, ":dist_to_our_base_point", 45),
             (try_end),
             (val_mul, ":dist_to_our_base_point", ":num_human_agents_div_3_plus_one"),
           (try_end),

           (val_add, ":entry_point_score", ":dist_to_our_base_point"),


           #give negative points if this entry point is near to enemy base.
           (assign, ":dist_to_enemy_base_point", 0),
           (try_begin), #capture the flag
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),

             (lt, ":dist_to_enemy_base", 150),
             (store_sub, ":dist_to_enemy_base_point", 150, ":dist_to_enemy_base"),

             (try_begin), #assign 150 to 150 + (150 - 50) * 2 = 350, assign 100 to 100 + (100 - 50) * 2 = 200
               (gt, ":dist_to_enemy_base_point", 50),
               (store_sub, ":dist_to_enemy_base_point_minus_50", ":dist_to_enemy_base_point", 50),
               (val_mul, ":dist_to_enemy_base_point_minus_50", 2),
               (val_add, ":dist_to_enemy_base_point", ":dist_to_enemy_base_point_minus_50"),
             (try_end),

             (val_mul, ":dist_to_enemy_base_point", -50), #-7500(with extras 350 * 50 = -17500)..0 (increase is linear)

             (val_mul, ":dist_to_enemy_base_point", ":num_human_agents_div_3_plus_one"),
           (else_try),
             (this_or_next|neq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
             (eq, ":team_no", 1),

             (assign, ":dist_to_enemy_base_point", 0),

             (try_begin),
               (neq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

               (try_begin),
                 (lt, ":sq_dist_to_enemy_base", 10000),
                 (store_sub, ":dist_to_enemy_base_point", 10000, ":sq_dist_to_enemy_base"),
                 (val_div, ":dist_to_enemy_base_point", 4),
                 (val_mul, ":dist_to_enemy_base_point", ":negative_num_human_agents_div_3_plus_one"),
               (try_end),
             (else_try),
               (val_max, ":dist_to_enemy_base", 60), #<60 meters has all most negative score

               (try_begin),
                 (eq, ":is_horseman", 1),
                 (assign, ":optimal_distance", 120),
               (else_try),
                 (assign, ":optimal_distance", 80),
               (try_end),

               (try_begin),
                 (le, ":dist_to_enemy_base", ":optimal_distance"),
                 (store_sub, ":dist_to_enemy_base_point", ":optimal_distance", ":dist_to_enemy_base"),
                 (val_mul, ":dist_to_enemy_base_point", 180), #-3600 max
               (else_try),
                 (store_sub, ":dist_to_enemy_base_point", ":dist_to_enemy_base", ":optimal_distance"),
                 (val_mul, ":dist_to_enemy_base_point", 30), #-unlimited max but lower slope
               (try_end),

               (val_sub, ":dist_to_enemy_base_point", 600),
               (val_max, ":dist_to_enemy_base_point", 0),

               (val_mul, ":dist_to_enemy_base_point", ":negative_num_human_agents_div_3_plus_one"),
             (try_end),
           (try_end),

           (val_add, ":entry_point_score", ":dist_to_enemy_base_point"),
         (else_try),
           (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),

           (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
             (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
             (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),
             (neq, ":cur_flag_owner", 0),
             (val_sub, ":cur_flag_owner", 1),

             (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"),
             (prop_instance_get_position, pos1, ":pole_id"), #pos1 holds pole position.

             (get_sq_distance_between_positions_in_meters, ":sq_dist_to_cur_pole", pos0, pos1),
             (lt, ":sq_dist_to_cur_pole", 6400),

             (try_begin),
               (eq, ":cur_flag_owner", ":team_no"),
               (store_sub, ":dist_to_flag_point", 6400, ":sq_dist_to_cur_pole"), #up to 80 meters give positive points if entry point is near our base
               (val_mul, ":dist_to_flag_point", 2),
               (val_div, ":dist_to_flag_point", ":our_flag_count"),
               (val_mul, ":dist_to_flag_point", ":num_human_agents_div_3_plus_one"),
             (else_try),
               (store_sub, ":dist_to_flag_point", 6400, ":sq_dist_to_cur_pole"), #up to 80 meters give negative points if entry point is near enemy base
               (val_mul, ":dist_to_flag_point", 2),
               (val_div, ":dist_to_flag_point", ":enemy_flag_count"),
               (val_mul, ":dist_to_flag_point", ":negative_num_human_agents_div_3_plus_one"),
             (try_end),
             (val_add, ":entry_point_score", ":dist_to_flag_point"),
           (try_end),
         (try_end),

         #(assign, reg1, ":i_entry_point"),
         #(assign, reg2, ":entry_point_score"),
         #(display_message, "@{!}entry_no : {reg1} , entry_score : {reg2}"),

         (gt, ":entry_point_score", ":best_entry_point_score"),
         (assign, ":best_entry_point_score", ":entry_point_score"),
         (assign, ":best_entry_point", ":i_entry_point"),
       (try_end),

       #(assign, reg0, ":best_entry_point"),
       #(assign, reg1, ":best_entry_point_score"),
       #(assign, reg2, ":num_operations"),
       #(assign, reg7, ":is_horseman"),
       #(display_message, "@{!},is horse:{reg7}, best entry:{reg0}, best entry score:{reg1}, num_operations:{reg2}"),
     (try_end),
     (assign, reg0, ":best_entry_point"),
     ])
]
