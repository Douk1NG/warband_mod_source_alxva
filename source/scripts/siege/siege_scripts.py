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

####################################################################################################################
# SIEGE SCRIPTS
# 
# This file contains scripts related to the siege mechanics of towns and castles. 
# It handles the daily processing of sieges (starvation, prosperity damage, lifting sieges), 
# as well as the tactical AI positioning during siege battles (e.g., archer placement).
####################################################################################################################

siege_scripts = [
  # Input: none
  # Output: none
  #called from triggers
  ("process_sieges",
    [
       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         #Reducing siege hardness every day by 20
         (party_get_slot, ":siege_hardness", ":center_no", slot_center_siege_hardness),
         (val_sub, ":siege_hardness", 20),
         (val_max, ":siege_hardness", 0),
         (party_set_slot, ":center_no", slot_center_siege_hardness, ":siege_hardness"),

         (party_get_slot, ":town_food_store", ":center_no", slot_party_food_store),
         (call_script, "script_center_get_food_store_limit", ":center_no"),
         (assign, ":food_store_limit", reg0),
         (try_begin),
           (party_get_slot, ":besieger_party", ":center_no", slot_center_is_besieged_by),
           (ge, ":besieger_party", 0), #town is under siege

           #Reduce prosperity of besieged castle/town by -0.33/-4 every day.
           (try_begin),
             (try_begin),
               (is_between, ":center_no", castles_begin, castles_end),
               (store_random_in_range, ":random_value", 0, 3),
               (try_begin),
                 (eq, ":random_value", 0),
                 (assign, ":daily_siege_effect_on_prosperity", -1),
               (else_try),
                 (assign, ":daily_siege_effect_on_prosperity", 0),
               (try_end),
             (else_try),
               (assign, ":daily_siege_effect_on_prosperity", -4),
             (try_end),

             (call_script, "script_change_center_prosperity", ":center_no", ":daily_siege_effect_on_prosperity"),
             (val_add, "$newglob_total_prosperity_from_townloot", ":daily_siege_effect_on_prosperity"),
           (try_end),

           (store_faction_of_party, ":center_faction", ":center_no"),
        # Lift siege unless there is an enemy party nearby
           (assign, ":siege_lifted", 0),
           (try_begin),
             (try_begin),
               (neg|party_is_active, ":besieger_party"),
               (assign, ":siege_lifted", 1),
             (else_try),
               (store_distance_to_party_from_party, ":besieger_distance", ":center_no", ":besieger_party"),
               (gt, ":besieger_distance", 5),
               (assign, ":siege_lifted", 1),
			 (else_try),
  			 ##diplomacy begin
         (neg|party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
         ##diplomacy end
			   (store_faction_of_party, ":besieger_faction", ":besieger_party"),
               (store_relation, ":reln", ":besieger_faction", ":center_faction"),
               (ge, ":reln", 0),
               (assign, ":siege_lifted", 1),
             (try_end),


             (eq, ":siege_lifted", 1),
			 #If another lord can take over the siege, it isn't lifted
             ##diplomacy start+ Support promoted kingdom ladies
             #(try_for_range, ":enemy_hero", active_npcs_begin, active_npcs_end),
             (try_for_range, ":enemy_hero", heroes_begin, heroes_end),
             ##diplomacy end+
               (troop_slot_eq, ":enemy_hero", slot_troop_occupation, slto_kingdom_hero),
               (troop_get_slot, ":enemy_party", ":enemy_hero", slot_troop_leaded_party),
               (ge, ":enemy_party", 0),
               (party_is_active, ":enemy_party"),
               (store_faction_of_party, ":party_faction", ":enemy_party"),
               (store_relation, ":reln", ":party_faction", ":center_faction"),
               (lt, ":reln", 0),
               (store_distance_to_party_from_party, ":distance", ":center_no", ":enemy_party"),
               (lt, ":distance", 4),
               (assign, ":besieger_party", ":enemy_party"),
               (party_set_slot, ":center_no", slot_center_is_besieged_by, ":enemy_party"),
               (assign, ":siege_lifted", 0),
             (try_end),
           (try_end),
           (try_begin),
             (eq, ":siege_lifted", 1),
             (call_script, "script_lift_siege", ":center_no", 1),
           (else_try),
             (call_script, "script_center_get_food_consumption", ":center_no"),
             (assign, ":food_consumption", reg0),
             (val_sub, ":town_food_store", ":food_consumption"), # reduce food only under siege???
             (try_begin),
               (le, ":town_food_store", 0), #town is starving
               (store_random_in_range, ":r", 0, 100),
               (lt, ":r", 10),
               (call_script, "script_party_wound_all_members", ":center_no"), # town falls with 10% chance if starving
             (try_end),
           (try_end),
         (else_try),
           #town is not under siege...
           (val_add, ":town_food_store", 30), #add 30 food (significant for castles only.
         (try_end),

         (val_min, ":town_food_store", ":food_store_limit"),
         (val_max, ":town_food_store", 0),
         (party_set_slot, ":center_no", slot_party_food_store, ":town_food_store"),
       (try_end),
  ]),

  # script_lift_siege
  # Input: arg1 = center_no, arg2 = display_message
  # Output: none
  #called from triggers
  ("lift_siege",
    [
      (store_script_param, ":center_no", 1),
      (store_script_param, ":display_message", 2),
      (party_set_slot, ":center_no", slot_center_is_besieged_by, -1), #clear siege
      (call_script, "script_village_set_state",  ":center_no", 0), #clear siege flag
      (try_begin),
        (eq, ":center_no", "$g_player_besiege_town"),
        (assign, "$g_siege_method", 0), #remove siege progress
      (try_end),
      (try_begin),
        (eq, ":display_message", 1),
        (str_store_party_name_link, s3, ":center_no"),
        (display_message, "@{s3} is no longer under siege."),
      (try_end),

      #SB : ideally we deal with post-conquest here but this is also called for cancelled sieges
      ]),


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
      ]),

  # script_describe_relation_to_s63
  # Input: none
  # Output: none
  ("siege_move_archers_to_archer_positions",
   [
     (try_for_agents, ":agent_no"),
       (agent_is_alive, ":agent_no"),
       (agent_slot_eq, ":agent_no", slot_agent_is_not_reinforcement, 0),
       (agent_is_defender, ":agent_no"),
       (agent_get_class, ":agent_class", ":agent_no"),
       (agent_get_troop_id, ":agent_troop", ":agent_no"),
       (eq, ":agent_class", grc_archers),
       (try_begin),
         (agent_slot_eq, ":agent_no", slot_agent_target_entry_point, 0),
         (store_random_in_range, ":random_entry_point", 40, 44), #40, 48? dckplmc
         (agent_set_slot, ":agent_no", slot_agent_target_entry_point, ":random_entry_point"),
       (try_end),
       (try_begin),
         (agent_get_position, pos0, ":agent_no"),
         (entry_point_get_position, pos1, ":random_entry_point"),
         (get_distance_between_positions, ":dist", pos0, pos1),
         (lt, ":dist", 300),
         (agent_clear_scripted_mode, ":agent_no"),
         (agent_set_slot, ":agent_no", slot_agent_is_in_scripted_mode, 0),
         (agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement, 1),
         (str_store_troop_name, s1, ":agent_troop"),
         (assign, reg0, ":agent_no"),
#         (display_message, "@{s1} ({reg0}) reached pos"),
       (else_try),
         (agent_get_simple_behavior, ":agent_sb", ":agent_no"),
         (agent_get_combat_state, ":agent_cs", ":agent_no"),
         (this_or_next|eq, ":agent_sb", aisb_ranged),
         (eq, ":agent_sb", aisb_go_to_pos),#scripted mode
         (eq, ":agent_cs", 7), # 7 = no visible targets (state for ranged units)
         (try_begin),
           (agent_slot_eq, ":agent_no", slot_agent_is_in_scripted_mode, 0),
           (agent_set_scripted_destination, ":agent_no", pos1, 0),
           (agent_set_slot, ":agent_no", slot_agent_is_in_scripted_mode, 1),
           (str_store_troop_name, s1, ":agent_troop"),
           (assign, reg0, ":agent_no"),
#           (display_message, "@{s1} ({reg0}) moving to pos"),
         (try_end),
       (else_try),
         (try_begin),
           (agent_slot_eq, ":agent_no", slot_agent_is_in_scripted_mode, 1),
           (agent_clear_scripted_mode, ":agent_no"),
           (agent_set_slot, ":agent_no", slot_agent_is_in_scripted_mode, 0),
           (str_store_troop_name, s1, ":agent_troop"),
           (assign, reg0, ":agent_no"),
#           (display_message, "@{s1} ({reg0}) seeing target or changed mode"),
         (try_end),
       (try_end),
     (try_end),
     ]),


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
      ]),

("move_object_to_nearest_entry_point",
   [
     (store_script_param, ":scene_prop_no", 1),

     (scene_prop_get_num_instances, ":num_instances", ":scene_prop_no"),

     (try_for_range, ":instance_no", 0, ":num_instances"),
       (scene_prop_get_instance, ":instance_id", ":scene_prop_no", ":instance_no"),
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
         (ge, ":smallest_dist", 0),
         (lt, ":smallest_dist", 22500), #max 15m distance
         (entry_point_get_position, pos1, ":nearest_entry_point"),
         (position_rotate_x, pos1, -90),
         (prop_instance_animate_to_position, ":instance_id", pos1, 1),
       (try_end),
     (try_end),
   ]),

("move_belfries_to_their_first_entry_point",
   [
    (store_script_param, ":belfry_body_scene_prop", 1),

    (set_fixed_point_multiplier, 100),
    (scene_prop_get_num_instances, ":num_belfries", ":belfry_body_scene_prop"),

    (try_for_range, ":belfry_no", 0, ":num_belfries"),
      #belfry
      (scene_prop_get_instance, ":belfry_scene_prop_id", ":belfry_body_scene_prop", ":belfry_no"),
      (prop_instance_get_position, pos0, ":belfry_scene_prop_id"),

      (try_begin),
        (eq, ":belfry_body_scene_prop", "spr_belfry_a"),
        #belfry platform_a
        (scene_prop_get_instance, ":belfry_platform_a_scene_prop_id", "spr_belfry_platform_a", ":belfry_no"),
        #belfry platform_b
        (scene_prop_get_instance, ":belfry_platform_b_scene_prop_id", "spr_belfry_platform_b", ":belfry_no"),
      (else_try),
        #belfry platform_a
        (scene_prop_get_instance, ":belfry_platform_a_scene_prop_id", "spr_belfry_b_platform_a", ":belfry_no"),
      (try_end),

      #belfry wheel_1
      (store_mul, ":wheel_no", ":belfry_no", 3),
      (try_begin),
        (eq, ":belfry_body_scene_prop", "spr_belfry_b"),
        (scene_prop_get_num_instances, ":number_of_belfry_a", "spr_belfry_a"),
        (store_mul, ":number_of_belfry_a_wheels", ":number_of_belfry_a", 3),
        (val_add, ":wheel_no", ":number_of_belfry_a_wheels"),
      (try_end),
      (scene_prop_get_instance, ":belfry_wheel_1_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
      #belfry wheel_2
      (val_add, ":wheel_no", 1),
      (scene_prop_get_instance, ":belfry_wheel_2_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
      #belfry wheel_3
      (val_add, ":wheel_no", 1),
      (scene_prop_get_instance, ":belfry_wheel_3_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),

      (store_add, ":belfry_first_entry_point_id", 11, ":belfry_no"), #belfry entry points are 110..119 and 120..129 and 130..139
      (try_begin),
        (eq, ":belfry_body_scene_prop", "spr_belfry_b"),
        (scene_prop_get_num_instances, ":number_of_belfry_a", "spr_belfry_a"),
        (val_add, ":belfry_first_entry_point_id", ":number_of_belfry_a"),
      (try_end),
      (val_mul, ":belfry_first_entry_point_id", 10),
      (entry_point_get_position, pos1, ":belfry_first_entry_point_id"),

      #this code block is taken from module_mission_templates.py (multiplayer_server_check_belfry_movement)
      #up down rotation of belfry's next entry point
      (init_position, pos9),
      (position_set_y, pos9, -500), #go 5.0 meters back
      (position_set_x, pos9, -300), #go 3.0 meters left
      (position_transform_position_to_parent, pos10, pos1, pos9),
      (position_get_distance_to_terrain, ":height_to_terrain_1", pos10), #learn distance between 5 meters back of entry point(pos10) and ground level at left part of belfry

      (init_position, pos9),
      (position_set_y, pos9, -500), #go 5.0 meters back
      (position_set_x, pos9, 300), #go 3.0 meters right
      (position_transform_position_to_parent, pos10, pos1, pos9),
      (position_get_distance_to_terrain, ":height_to_terrain_2", pos10), #learn distance between 5 meters back of entry point(pos10) and ground level at right part of belfry

      (store_add, ":height_to_terrain", ":height_to_terrain_1", ":height_to_terrain_2"),
      (val_mul, ":height_to_terrain", 100), #because of fixed point multiplier

      (store_div, ":rotate_angle_of_next_entry_point", ":height_to_terrain", 24), #if there is 1 meters of distance (100cm) then next target position will rotate by 2 degrees. #ac sonra
      (init_position, pos20),
      (position_rotate_x_floating, pos20, ":rotate_angle_of_next_entry_point"),
      (position_transform_position_to_parent, pos23, pos1, pos20),

      #right left rotation of belfry's next entry point
      (init_position, pos9),
      (position_set_x, pos9, -300), #go 3.0 meters left
      (position_transform_position_to_parent, pos10, pos1, pos9), #applying 3.0 meters in -x to position of next entry point target, final result is in pos10
      (position_get_distance_to_terrain, ":height_to_terrain_at_left", pos10), #learn distance between 3.0 meters left of entry point(pos10) and ground level
      (init_position, pos9),
      (position_set_x, pos9, 300), #go 3.0 meters left
      (position_transform_position_to_parent, pos10, pos1, pos9), #applying 3.0 meters in x to position of next entry point target, final result is in pos10
      (position_get_distance_to_terrain, ":height_to_terrain_at_right", pos10), #learn distance between 3.0 meters right of entry point(pos10) and ground level
      (store_sub, ":height_to_terrain_1", ":height_to_terrain_at_left", ":height_to_terrain_at_right"),

      (init_position, pos9),
      (position_set_x, pos9, -300), #go 3.0 meters left
      (position_set_y, pos9, -500), #go 5.0 meters forward
      (position_transform_position_to_parent, pos10, pos1, pos9), #applying 3.0 meters in -x to position of next entry point target, final result is in pos10
      (position_get_distance_to_terrain, ":height_to_terrain_at_left", pos10), #learn distance between 3.0 meters left of entry point(pos10) and ground level
      (init_position, pos9),
      (position_set_x, pos9, 300), #go 3.0 meters left
      (position_set_y, pos9, -500), #go 5.0 meters forward
      (position_transform_position_to_parent, pos10, pos1, pos9), #applying 3.0 meters in x to position of next entry point target, final result is in pos10
      (position_get_distance_to_terrain, ":height_to_terrain_at_right", pos10), #learn distance between 3.0 meters right of entry point(pos10) and ground level
      (store_sub, ":height_to_terrain_2", ":height_to_terrain_at_left", ":height_to_terrain_at_right"),

      (store_add, ":height_to_terrain", ":height_to_terrain_1", ":height_to_terrain_2"),
      (val_mul, ":height_to_terrain", 100), #100 is because of fixed_point_multiplier
      (store_div, ":rotate_angle_of_next_entry_point", ":height_to_terrain", 24), #if there is 1 meters of distance (100cm) then next target position will rotate by 25 degrees.
      (val_mul, ":rotate_angle_of_next_entry_point", -1),

      (init_position, pos20),
      (position_rotate_y_floating, pos20, ":rotate_angle_of_next_entry_point"),
      (position_transform_position_to_parent, pos22, pos23, pos20),

      (copy_position, pos1, pos22),
      #end of code block

      #belfry
      (prop_instance_stop_animating, ":belfry_scene_prop_id"),
      (prop_instance_set_position, ":belfry_scene_prop_id", pos1),

      #belfry platforms
      (try_begin),
        (eq, ":belfry_body_scene_prop", "spr_belfry_a"),

        #belfry platform_a
        (prop_instance_get_position, pos6, ":belfry_platform_a_scene_prop_id"),
        (position_transform_position_to_local, pos7, pos0, pos6),
        (position_transform_position_to_parent, pos8, pos1, pos7),
        (try_begin),
          (neg|scene_prop_slot_eq, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 0),

          (init_position, pos20),
          (position_rotate_x, pos20, 90),
          (position_transform_position_to_parent, pos8, pos8, pos20),
        (try_end),
        (prop_instance_stop_animating, ":belfry_platform_a_scene_prop_id"),
        (prop_instance_set_position, ":belfry_platform_a_scene_prop_id", pos8),
        #belfry platform_b
        (prop_instance_get_position, pos6, ":belfry_platform_b_scene_prop_id"),
        (position_transform_position_to_local, pos7, pos0, pos6),
        (position_transform_position_to_parent, pos8, pos1, pos7),
        (prop_instance_stop_animating, ":belfry_platform_b_scene_prop_id"),
        (prop_instance_set_position, ":belfry_platform_b_scene_prop_id", pos8),
      (else_try),
        #belfry platform_a
        (prop_instance_get_position, pos6, ":belfry_platform_a_scene_prop_id"),
        (position_transform_position_to_local, pos7, pos0, pos6),
        (position_transform_position_to_parent, pos8, pos1, pos7),
        (try_begin),
          (neg|scene_prop_slot_eq, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 0),

          (init_position, pos20),
          (position_rotate_x, pos20, 50),
          (position_transform_position_to_parent, pos8, pos8, pos20),
        (try_end),
        (prop_instance_stop_animating, ":belfry_platform_a_scene_prop_id"),
        (prop_instance_set_position, ":belfry_platform_a_scene_prop_id", pos8),
      (try_end),

      #belfry wheel_1
      (store_mul, ":wheel_no", ":belfry_no", 3),
      (try_begin),
        (eq, ":belfry_body_scene_prop", "spr_belfry_b"),
        (scene_prop_get_num_instances, ":number_of_belfry_a", "spr_belfry_a"),
        (store_mul, ":number_of_belfry_a_wheels", ":number_of_belfry_a", 3),
        (val_add, ":wheel_no", ":number_of_belfry_a_wheels"),
      (try_end),
      (prop_instance_get_position, pos6, ":belfry_wheel_1_scene_prop_id"),
      (position_transform_position_to_local, pos7, pos0, pos6),
      (position_transform_position_to_parent, pos8, pos1, pos7),
      (prop_instance_stop_animating, ":belfry_wheel_1_scene_prop_id"),
      (prop_instance_set_position, ":belfry_wheel_1_scene_prop_id", pos8),
      #belfry wheel_2
      (prop_instance_get_position, pos6, ":belfry_wheel_2_scene_prop_id"),
      (position_transform_position_to_local, pos7, pos0, pos6),
      (position_transform_position_to_parent, pos8, pos1, pos7),
      (prop_instance_stop_animating, ":belfry_wheel_2_scene_prop_id"),
      (prop_instance_set_position, ":belfry_wheel_2_scene_prop_id", pos8),
      #belfry wheel_3
      (prop_instance_get_position, pos6, ":belfry_wheel_3_scene_prop_id"),
      (position_transform_position_to_local, pos7, pos0, pos6),
      (position_transform_position_to_parent, pos8, pos1, pos7),
      (prop_instance_stop_animating, ":belfry_wheel_3_scene_prop_id"),
      (prop_instance_set_position, ":belfry_wheel_3_scene_prop_id", pos8),
    (try_end),
    ]),

("siege_init_ai_and_belfry",
   [(assign, "$cur_belfry_pos", 50),
    (assign, ":cur_belfry_object_pos", slot_scene_belfry_props_begin),
    (store_current_scene, ":cur_scene"),
    #Collecting belfry objects
    (try_for_range, ":i_belfry_instance", 0, 3),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_a", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (try_for_range, ":i_belfry_instance", 0, 3),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_a", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (try_for_range, ":i_belfry_instance", 0, 3),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_b", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (assign, "$belfry_rotating_objects_begin", ":cur_belfry_object_pos"),
    (try_for_range, ":i_belfry_instance", 0, 5),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_wheel", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (assign, "$last_belfry_object_pos", ":cur_belfry_object_pos"),

    #Lifting up the platform  at the beginning
    (try_begin),
      (scene_prop_get_instance, ":belfry_object_to_rotate", "spr_belfry_platform_a", 0),
    (try_end),

    #Moving the belfry objects to their starting position
    (entry_point_get_position,pos1,55),
    (entry_point_get_position,pos3,50),
    (try_for_range, ":i_belfry_object_pos", slot_scene_belfry_props_begin, "$last_belfry_object_pos"),
      (assign, ":pos_no", pos_belfry_begin),
      (val_add, ":pos_no", ":i_belfry_object_pos"),
      (val_sub, ":pos_no", slot_scene_belfry_props_begin),
      (scene_get_slot, ":cur_belfry_object", ":cur_scene", ":i_belfry_object_pos"),
      (prop_instance_get_position, pos2, ":cur_belfry_object"),
      (try_begin),
        (eq, ":cur_belfry_object", ":belfry_object_to_rotate"),
        (position_rotate_x, pos2, 90),
      (try_end),
      (position_transform_position_to_local, ":pos_no", pos1, pos2),
      (position_transform_position_to_parent, pos4, pos3, ":pos_no"),
      (prop_instance_animate_to_position, ":cur_belfry_object", pos4, 1),
    (try_end),
    (assign, "$belfry_positioned", 0),
    (assign, "$belfry_num_slots_positioned", 0),
    (assign, "$belfry_num_men_pushing", 0),

    (set_show_messages, 0),
    (team_give_order, "$attacker_team", grc_everyone, mordr_stand_ground),
    (team_give_order, "$attacker_team_2", grc_everyone, mordr_stand_ground),
    (set_show_messages, 1),
  ]),

("cf_siege_move_belfry",
   [(neq, "$last_belfry_object_pos", slot_scene_belfry_props_begin),
    (entry_point_get_position,pos1,50),
    (entry_point_get_position,pos4,55),
    (get_distance_between_positions, ":total_distance", pos4, pos1),
    (store_current_scene, ":cur_scene"),
    (scene_get_slot, ":first_belfry_object", ":cur_scene", slot_scene_belfry_props_begin),
    (prop_instance_get_position, pos2, ":first_belfry_object"),
    (entry_point_get_position,pos1,"$cur_belfry_pos"),
    (position_transform_position_to_parent, pos3, pos1, pos_belfry_begin),
    (position_transform_position_to_parent, pos5, pos4, pos_belfry_begin),
    (get_distance_between_positions, ":cur_distance", pos2, pos3),
    (get_distance_between_positions, ":distance_left", pos2, pos5),
    (try_begin),
      (le, ":cur_distance", 10),
      (val_add, "$cur_belfry_pos", 1),
      (entry_point_get_position,pos1,"$cur_belfry_pos"),
      (position_transform_position_to_parent, pos3, pos1, pos_belfry_begin),
      (get_distance_between_positions, ":cur_distance", pos2, pos3),
    (try_end),
    (neq, "$cur_belfry_pos", 50),

    (assign, ":base_speed", 20),
    (store_div, ":slow_range", ":total_distance", 60),
    (store_sub, ":distance_moved", ":total_distance", ":distance_left"),

    (try_begin),
      (lt, ":distance_moved", ":slow_range"),
      (store_mul, ":base_speed", ":distance_moved", -60),
      (val_div, ":base_speed", ":slow_range"),
      (val_add, ":base_speed", 80),
    (else_try),
      (lt, ":distance_left", ":slow_range"),
      (store_mul, ":base_speed", ":distance_left", -60),
      (val_div, ":base_speed", ":slow_range"),
      (val_add, ":base_speed", 80),
    (try_end),
    (store_mul, ":belfry_speed", ":cur_distance", ":base_speed"),
    (try_begin),
      (eq, "$belfry_num_men_pushing", 0),
      (assign, ":belfry_speed", 1000000),
    (else_try),
      (val_div, ":belfry_speed", "$belfry_num_men_pushing"),
    (try_end),

    (try_begin),
      (le, "$cur_belfry_pos", 55),
      (init_position, pos3),
      (position_rotate_x, pos3, ":distance_moved"),
      (scene_get_slot, ":base_belfry_object", ":cur_scene", slot_scene_belfry_props_begin),
      (prop_instance_get_position, pos4, ":base_belfry_object"),
      (entry_point_get_position,pos1,"$cur_belfry_pos"),
      (try_for_range, ":i_belfry_object_pos", slot_scene_belfry_props_begin, "$last_belfry_object_pos"),
        (scene_get_slot, ":cur_belfry_object", ":cur_scene", ":i_belfry_object_pos"),
        (try_begin),
          (ge, ":i_belfry_object_pos", "$belfry_rotating_objects_begin"),
          (prop_instance_get_starting_position, pos5, ":base_belfry_object"),
          (prop_instance_get_starting_position, pos6, ":cur_belfry_object"),
          (position_transform_position_to_local, pos7, pos5, pos6),
          (position_transform_position_to_parent, pos5, pos4, pos7),
          (position_transform_position_to_parent, pos6, pos5, pos3),
          (prop_instance_set_position, ":cur_belfry_object", pos6),
        (else_try),
          (assign, ":pos_no", pos_belfry_begin),
          (val_add, ":pos_no", ":i_belfry_object_pos"),
          (val_sub, ":pos_no", slot_scene_belfry_props_begin),
          (position_transform_position_to_parent, pos2, pos1, ":pos_no"),
          (prop_instance_animate_to_position, ":cur_belfry_object", pos2, ":belfry_speed"),
        (try_end),
      (try_end),
    (try_end),
    (gt, "$cur_belfry_pos", 55),
    (assign, "$belfry_positioned", 1),
  ]),

("cf_siege_rotate_belfry_platform",
   [(eq, "$belfry_positioned", 1),
    (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_a", 0),
    (prop_instance_get_position, pos1, ":belfry_object"),
    (position_rotate_x, pos1, -90),
    (prop_instance_animate_to_position, ":belfry_object", pos1, 400),
    (assign, "$belfry_positioned", 2),
  ]),

("cf_siege_assign_men_to_belfry",
   [
##    (store_mission_timer_a, ":cur_seconds"),
    (neq, "$last_belfry_object_pos", slot_scene_belfry_props_begin),
    (assign, ":end_trigger", 0),
    (try_begin),
      (lt, "$belfry_positioned", 3),
      (get_player_agent_no, ":player_agent"),
      (store_current_scene, ":cur_scene"),
      (scene_get_slot, ":first_belfry_object", ":cur_scene", slot_scene_belfry_props_begin),
      (prop_instance_get_position, pos2, ":first_belfry_object"),
      (assign, ":slot_1_positioned", 0),
      (assign, ":slot_2_positioned", 0),
      (assign, ":slot_3_positioned", 0),
      (assign, ":slot_4_positioned", 0),
      (assign, ":slot_5_positioned", 0),
      (assign, ":slot_6_positioned", 0),
      (assign, "$belfry_num_slots_positioned", 0),
      (assign, "$belfry_num_men_pushing", 0),
      (try_for_agents, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (try_begin),
          (agent_get_slot, ":x_pos", ":cur_agent", slot_agent_target_x_pos),
          (neq, ":x_pos", 0),
          (agent_get_slot, ":y_pos", ":cur_agent", slot_agent_target_y_pos),
          (try_begin),
            (eq, ":x_pos", -600),
            (try_begin),
              (eq, ":y_pos", 0),
              (assign, ":slot_1_positioned", 1),
            (else_try),
              (eq, ":y_pos", -200),
              (assign, ":slot_2_positioned", 1),
            (else_try),
              (assign, ":slot_3_positioned", 1),
            (try_end),
          (else_try),
            (try_begin),
              (eq, ":y_pos", 0),
              (assign, ":slot_4_positioned", 1),
            (else_try),
              (eq, ":y_pos", -200),
              (assign, ":slot_5_positioned", 1),
            (else_try),
              (assign, ":slot_6_positioned", 1),
            (try_end),
          (try_end),
          (val_add, "$belfry_num_slots_positioned", 1),
          (init_position, pos1),
          (position_move_x, pos1, ":x_pos"),
          (position_move_y, pos1, ":y_pos"),
          (init_position, pos3),
          (position_move_x, pos3, ":x_pos"),
          (position_move_y, pos3, -1000),
          (position_transform_position_to_parent, pos4, pos2, pos1),
          (position_transform_position_to_parent, pos5, pos2, pos3),
          (agent_get_position, pos6, ":cur_agent"),
          (get_distance_between_positions, ":target_distance", pos6, pos4),
          (get_distance_between_positions, ":waypoint_distance", pos6, pos5),
          (try_begin),
            (this_or_next|lt, ":target_distance", ":waypoint_distance"),
            (lt, ":waypoint_distance", 600),
            (agent_set_scripted_destination, ":cur_agent", pos4, 1),
          (else_try),
            (agent_set_scripted_destination, ":cur_agent", pos5, 1),
          (try_end),
          (try_begin),
            (le, ":target_distance", 300),
            (val_add, "$belfry_num_men_pushing", 1),
          (try_end),
##        (else_try),
##          (agent_get_team, ":cur_agent_team", ":cur_agent"),
##          (this_or_next|eq, "$attacker_team", ":cur_agent_team"),
##          (             eq, "$attacker_team_2", ":cur_agent_team"),
##          (try_begin),
##            (gt, ":cur_seconds", 20),
##            (agent_get_position, pos1, ":cur_agent"),
##            (agent_set_scripted_destination, ":cur_agent", pos1, 0),
##          (else_try),
##            (try_begin),
##              (team_get_movement_order, ":order1", "$attacker_team", grc_infantry),
##              (team_get_movement_order, ":order2", "$attacker_team", grc_cavalry),
##              (team_get_movement_order, ":order3", "$attacker_team", grc_archers),
##              (this_or_next|neq, ":order1", mordr_stand_ground),
##              (this_or_next|neq, ":order2", mordr_stand_ground),
##              (neq, ":order3", mordr_stand_ground),
##              (set_show_messages, 0),
##              (team_give_order, "$attacker_team", grc_everyone, mordr_stand_ground),
##              (set_show_messages, 1),
##            (try_end),
##          (try_end),
        (try_end),
      (try_end),
      (try_begin),
        (lt, "$belfry_num_slots_positioned", 6),
        (try_for_agents, ":cur_agent"),
          (agent_is_alive, ":cur_agent"),
          (agent_get_team, ":cur_agent_team", ":cur_agent"),
          (this_or_next|eq, "$attacker_team", ":cur_agent_team"),
          (eq, "$attacker_team_2", ":cur_agent_team"),
          (neq, ":player_agent", ":cur_agent"),
          (agent_get_class, ":agent_class", ":cur_agent"),
          (this_or_next|eq, ":agent_class", grc_infantry),
          (eq, ":agent_class", grc_cavalry),
          (agent_get_slot, ":x_pos", ":cur_agent", 1),
          (eq, ":x_pos", 0),
          (assign, ":y_pos", 0),
          (try_begin),
            (eq, ":slot_1_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_1_positioned", 1),
          (else_try),
            (eq, ":slot_2_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_2_positioned", 1),
          (else_try),
            (eq, ":slot_3_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_3_positioned", 1),
          (else_try),
            (eq, ":slot_4_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_4_positioned", 1),
          (else_try),
            (eq, ":slot_5_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_5_positioned", 1),
          (else_try),
            (eq, ":slot_6_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_6_positioned", 1),
          (try_end),
          (val_add, "$belfry_num_slots_positioned", 1),
          (agent_set_slot, ":cur_agent", 1, ":x_pos"),
          (agent_set_slot, ":cur_agent", 2, ":y_pos"),
        (try_end),
      (try_end),
      (try_begin),
        (store_mission_timer_a, ":cur_timer"),
        (gt, ":cur_timer", 20),
        (lt, "$belfry_num_slots_positioned", 6),
        (try_for_agents, ":cur_agent"),
          (agent_is_alive, ":cur_agent"),
          (agent_get_team, ":cur_agent_team", ":cur_agent"),
          (this_or_next|eq, "$attacker_team", ":cur_agent_team"),
          (             eq, "$attacker_team_2", ":cur_agent_team"),
          (neq, ":player_agent", ":cur_agent"),
          (agent_get_slot, ":x_pos", ":cur_agent", 1),
          (eq, ":x_pos", 0),
          (assign, ":y_pos", 0),
          (try_begin),
            (eq, ":slot_1_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_1_positioned", 1),
          (else_try),
            (eq, ":slot_2_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_2_positioned", 1),
          (else_try),
            (eq, ":slot_3_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_3_positioned", 1),
          (else_try),
            (eq, ":slot_4_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_4_positioned", 1),
          (else_try),
            (eq, ":slot_5_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_5_positioned", 1),
          (else_try),
            (eq, ":slot_6_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_6_positioned", 1),
          (try_end),
          (val_add, "$belfry_num_slots_positioned", 1),
          (agent_set_slot, ":cur_agent", 1, ":x_pos"),
          (agent_set_slot, ":cur_agent", 2, ":y_pos"),
        (try_end),
      (try_end),
    (else_try),
      (assign, ":end_trigger", 1),
      (try_for_agents, ":cur_agent"),
        (agent_clear_scripted_mode, ":cur_agent"),
      (try_end),
      (set_show_messages, 0),
      (team_give_order, "$attacker_team", grc_everyone, mordr_charge),
      (set_show_messages, 1),
    (try_end),
    (eq, ":end_trigger", 1),
  ]),
]
