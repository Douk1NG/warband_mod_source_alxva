# ======================================================================
# SHARED DEPENDENCY
# Entity: party_calculate_loot (script)
# Called by menus in 2 domains: battle, siege
# ======================================================================

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

party_calculate_loot_scripts = [
("party_calculate_loot",
    [
      (store_script_param_1, ":enemy_party"), #Enemy Party_id

      (call_script, "script_calculate_main_party_shares"),
      (assign, ":num_player_party_shares", reg0),

      (try_for_range, ":i_loot", 0, num_party_loot_slots),
        (store_add, ":cur_loot_slot", ":i_loot", slot_party_looted_item_1),
        (party_get_slot, ":item_no", "$g_enemy_party", ":cur_loot_slot"),
        (gt, ":item_no", 0),
        (party_set_slot, "$g_enemy_party", ":cur_loot_slot", 0),
        (val_sub, ":cur_loot_slot", slot_party_looted_item_1),
        (val_add, ":cur_loot_slot", slot_party_looted_item_1_modifier),
        (party_get_slot, ":item_modifier", "$g_enemy_party", ":cur_loot_slot"),
        (troop_add_item, "trp_temp_troop", ":item_no", ":item_modifier"),
      (try_end),
      (party_set_slot, "$g_enemy_party", slot_party_next_looted_item_slot, 0),

      (assign, ":num_looted_items",0),
      (try_begin),
        (this_or_next|party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_caravan),
        (this_or_next|party_slot_eq, "$g_enemy_party", slot_party_type, spt_bandit_lair),
        (party_slot_eq, "$g_enemy_party", slot_party_type, spt_village_farmer),
        (store_mul, ":plunder_amount", player_loot_share, 30),
        (val_mul, ":plunder_amount", "$g_strength_contribution_of_player"),
        (val_div, ":plunder_amount", 100),
        (val_div, ":plunder_amount", ":num_player_party_shares"),
        (try_begin),
          (party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_caravan),
          (reset_item_probabilities, 100),
          (assign, ":range_min", trade_goods_begin),
          (assign, ":range_max", trade_goods_end),
        (else_try),
          (party_slot_eq, "$g_enemy_party", slot_party_type, spt_bandit_lair),
          (val_div, ":plunder_amount", 2),
          (reset_item_probabilities, 1),
          (assign, ":range_min", food_begin),
          (assign, ":range_max", food_end),
        (else_try),
          (val_div, ":plunder_amount", 5),
          (reset_item_probabilities, 1),
          (assign, ":range_min", food_begin),
          (assign, ":range_max", food_end),
        (try_end),
        (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
        (try_for_range, ":cur_goods", ":range_min", ":range_max"),
          (try_begin),
            (neg|party_slot_eq, "$g_enemy_party", slot_party_type, spt_bandit_lair),
            (store_add, ":cur_price_slot", ":cur_goods", ":item_to_price_slot"),
            (party_get_slot, ":cur_price", "$g_enemy_party", ":cur_price_slot"),
          (else_try),
            (assign, ":cur_price", maximum_price_factor),
            (val_add, ":cur_price", average_price_factor),
            (val_div, ":cur_price", 3),
          (try_end),

          (assign, ":cur_probability", 100),
          (val_mul, ":cur_probability", average_price_factor),
          (val_div, ":cur_probability", ":cur_price"),
          (assign, reg0, ":cur_probability"),
          (set_item_probability_in_merchandise, ":cur_goods", ":cur_probability"),
        (try_end),
        (troop_add_merchandise, "trp_temp_troop", itp_type_goods, ":plunder_amount"),
        (val_add, ":num_looted_items", ":plunder_amount"),
      (try_end),

      #Now loot the defeated party
      (store_mul, ":loot_probability", player_loot_share, 3),
      (val_mul, ":loot_probability", "$g_strength_contribution_of_player"),
      (party_get_skill_level, ":player_party_looting", "p_main_party", "skl_looting"),
      (val_add, ":player_party_looting", 10),
      (val_mul, ":loot_probability", ":player_party_looting"),
      (val_div, ":loot_probability", 10),
      (val_div, ":loot_probability", ":num_player_party_shares"),

      (party_get_num_companion_stacks, ":num_stacks",":enemy_party"),
      ###(((sort troops of enemy_party by level
      (assign, ":last_stack", ":num_stacks"),
      (try_for_range, ":unused", 0, ":num_stacks"),
        (assign, ":best_stack", -1),
        (assign, ":best_level", -999999),
        (try_for_range, ":cur_stack", 0, ":last_stack"),
          (party_stack_get_troop_id, ":cur_troop", ":enemy_party", ":cur_stack"),
          (neg|troop_is_hero, ":cur_troop"),
          (store_character_level, ":cur_level", ":cur_troop"),
          (gt, ":cur_level", ":best_level"),
          (assign, ":best_level", ":cur_level"),
          (assign, ":best_stack", ":cur_stack"),
        (try_end),
        (gt, ":best_stack", -1),
        (party_stack_get_troop_id, ":stack_troop", ":enemy_party", ":best_stack"),
        (party_stack_get_size, ":stack_size", ":enemy_party", ":best_stack"),
        (party_remove_members, ":enemy_party", ":stack_troop", ":stack_size"),
        (party_add_members, ":enemy_party", ":stack_troop", ":stack_size"),
        (val_sub, ":last_stack", 1),
      (try_end),
      ###)))
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":enemy_party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size, ":stack_size",":enemy_party",":i_stack"),
        (try_for_range, ":unused", 0, ":stack_size"),
          (troop_loot_troop, "trp_temp_troop", ":stack_troop", ":loot_probability"),
        (try_end),
      (try_end),

      #(troop_get_inventory_capacity, ":inv_cap", "trp_temp_troop"),
      #(try_for_range, ":i_slot", 0, ":inv_cap"),
      #  (troop_get_inventory_slot, ":item_id", "trp_temp_troop", ":i_slot"),
      #  (is_between, ":item_id", horses_begin, horses_end),
      #  (troop_set_inventory_slot, "trp_temp_troop", ":i_slot", -1),
      #(try_end),

      (troop_get_inventory_capacity, ":inv_cap", "trp_temp_troop"),
      (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":item_id", "trp_temp_troop", ":i_slot"),
        (ge, ":item_id", 0),
        (val_add, ":num_looted_items", 1),
      (try_end),

      (assign, reg0, ":num_looted_items"),
  ])
]
