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
]
