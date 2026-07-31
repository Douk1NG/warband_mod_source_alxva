# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *




  # Constable training
  

constable_training_simple_triggers = [
(24, [
    (eq, "$g_player_constable", "trp_dplmc_constable"),
    (is_between, "$g_constable_training_center", walled_centers_begin, walled_centers_end),
    (party_slot_eq, "$g_constable_training_center", slot_town_lord, "trp_player"),

    (store_skill_level, ":trainer_level", skl_trainer, "trp_player"),
    (val_add, ":trainer_level", 4),
    (store_div, ":xp_gain", ":trainer_level", 2),
    #could factor in quantity policy (not quality) here for xp_gain
    (try_begin),
      (ge, "$novice_training_difficulty", 1),
      (assign, ":max_distance", 50),
      (game_get_reduce_campaign_ai, ":cur_number"), #0, 1, 2
      (val_add, ":cur_number", "$novice_training_difficulty"), #1 to 6
      (val_div, ":cur_number", 2),
      (val_max, ":cur_number", 1),
      
      (try_for_range, ":grounds", training_grounds_begin, training_grounds_end),
        (store_distance_to_party_from_party, ":distance", ":grounds", "$g_constable_training_center"),
        (lt, ":distance", ":max_distance"),
        (val_add, ":xp_gain", ":cur_number"),
      (try_end),
    (try_end),
   
   #SB : move calculations up
   (store_mul, ":troop_limit", "$g_constable_training_improved", 2), #from 0 to 4
   (val_add, ":troop_limit", 7), #base recruit level in Natives + 1, values now can be 7/9/11/13/15

   (store_troop_gold, ":gold", "trp_household_possessions"), #player treasury
   (store_mul, ":total_cost", "$g_constable_training_improved", 10), #base cost
   #probably do a message here notifying trainers have left your service
   (gt, ":gold", ":total_cost"),
   #SB : wtf is this
   # (try_for_parties, ":party_no"),
    # (party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
    # (eq, ":party_no", "$g_constable_training_center"),
    (assign, ":party_no", "$g_constable_training_center"),

    (party_get_num_companion_stacks, ":num_stacks", ":party_no"),

    # (assign, ":trained", 0),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      # (eq, ":trained", 0),
      (gt, ":xp_gain", 0),
      (party_stack_get_troop_id, ":troop_id", ":party_no", ":i_stack"),
      (neg|troop_is_hero, ":troop_id"),

      #SB : lots of upgrade troop parsing
      (troop_get_upgrade_troop, ":upgrade_troop_1", ":troop_id" , 0),
      (gt, ":upgrade_troop_1", 0), #if first upgrade doesn't exist, it can't upgrade at all
      (try_begin),
        # (troop_get_class, ":grc", ":upgrade_troop_1"),
        # (eq, ":grc", "$g_constable_training_type"),
        (call_script, "script_cf_troop_is_class", "$g_constable_training_type", ":upgrade_troop_1"),
        (assign, ":upgrade_troop", ":upgrade_troop_1"),
      (else_try),
        (troop_get_upgrade_troop, ":upgrade_troop_2", ":troop_id" , 1),
        (call_script, "script_cf_troop_is_class", "$g_constable_training_type", ":upgrade_troop_2"),
        (assign, ":upgrade_troop", ":upgrade_troop_2"),
      (else_try), #do a look-ahead
        (assign, ":upgrade_troop", ":upgrade_troop_2"),
        (try_begin),
          (troop_get_upgrade_troop, ":upgrade_troop_3", ":upgrade_troop" , 0),
          (call_script, "script_cf_troop_is_class", "$g_constable_training_type", ":upgrade_troop_3"),
          (assign, ":upgrade_troop", ":upgrade_troop_3"),
        (else_try),
          (troop_get_upgrade_troop, ":upgrade_troop_4", ":upgrade_troop" , 1),
          (call_script, "script_cf_troop_is_class", "$g_constable_training_type", ":upgrade_troop_4"),
          (assign, ":upgrade_troop", ":upgrade_troop_4"),
        (try_end),
        (eq, ":upgrade_troop", ":upgrade_troop_2"), #unchanged, check upgrade_troop_2
        (try_begin),
          (troop_get_upgrade_troop, ":upgrade_troop_3", ":upgrade_troop" , 0),
          (call_script, "script_cf_troop_is_class", "$g_constable_training_type", ":upgrade_troop_3"),
          (assign, ":upgrade_troop", ":upgrade_troop_3"),
        (else_try),
          (troop_get_upgrade_troop, ":upgrade_troop_4", ":upgrade_troop" , 1),
          (call_script, "script_cf_troop_is_class", "$g_constable_training_type", ":upgrade_troop_4"),
          (assign, ":upgrade_troop", ":upgrade_troop_4"),
        (try_end),
      (try_end),
      #only proceed if troop is upgradable
      (gt, ":upgrade_troop", 0),

      (store_character_level, ":troop_level", ":troop_id"),
      (le, ":troop_level", ":troop_limit"),
      
      # (party_count_members_of_type,":cur_number",":party_no",":troop_id"),
      (party_stack_get_size, ":cur_number", ":party_no", ":i_stack"),
      (party_stack_get_num_wounded, ":num_wounded",":party_no",":i_stack"),
      (val_sub, ":cur_number", ":num_wounded"),
      (try_begin),
        (ge, "$g_constable_training_improved", 1),
        (le, ":troop_level", 6),
        (val_add, ":cur_number", 2), #more recruits are trained during improved training
      (try_end),
      (val_min, ":cur_number", ":xp_gain"),

      (call_script, "script_game_get_upgrade_cost", ":troop_id"),
      (store_mul, ":upgrade_cost", ":cur_number", reg0),
      
      # (try_for_range, ":troop_count", 0, ":cur_number"),
        # (gt, ":gold", ":total_cost"),
        # (val_add, ":total_cost", ":upgrade_cost"),
      # (else_try), #break and lower cur_number
        # (val_sub, ":total_cost", ":upgrade_cost"), #can't afford
        # (assign, ":cur_number", ":troop_count"),
      # (try_end),

      # (store_troop_gold, ":gold", "trp_household_possessions"),
      (val_add, ":total_cost", ":upgrade_cost"),
      (try_begin), #if we can only afford partial upgrades
        (lt, ":gold", ":total_cost"),
        (val_sub, ":total_cost", ":upgrade_cost"), #undo
        (val_div, ":upgrade_cost", ":cur_number"), #get original cost
        (store_sub, ":cur_number", ":gold", ":total_cost"), #get remainder
        (val_div, ":cur_number", ":upgrade_cost"), #get however many we can afford
        (val_mul, ":cur_number", ":upgrade_cost"), #then redo
        (val_add, ":total_cost", ":upgrade_cost"),
        (str_store_troop_name_plural, s6, ":troop_id"),
        (display_message, "@Not enough money in treasury to upgrade {s6}."),
      (try_end),


      # (val_add, ":total_cost", ":upgrade_cost"),

      # (call_script, "script_dplmc_withdraw_from_treasury", ":upgrade_cost"),
      (party_remove_members,":party_no",":troop_id",":cur_number"),
      (party_add_members, ":party_no", ":upgrade_troop", ":cur_number"),
      (val_sub, ":xp_gain", ":cur_number"),
      (assign, reg5, ":cur_number"),
      (str_store_troop_name_by_count, s6, ":troop_id", ":cur_number"),
      (str_store_troop_name_by_count, s7, ":upgrade_troop", ":cur_number"),
      (str_store_party_name_link, s8, ":party_no"),
      (display_log_message, "@Your constable upgraded {reg5} {s6} to {s7} in {s8}"),
      
    (try_end),
    
    #finalize costs
    (call_script, "script_dplmc_withdraw_from_treasury", ":total_cost"),
   # (try_end),
    ]),
]
