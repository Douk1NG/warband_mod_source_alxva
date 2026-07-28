# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_troops import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

mnh_give_manhunter_prisoners_scripts = [
# script_mnh_give_manhunter_prisoners
# Gives a manhunter party some bandit prisoners
# Input: param1 = party_id
("mnh_give_manhunter_prisoners",
  [
    (store_script_param_1, ":party_no"),

    (store_random_in_range, ":num_steppe", 2, 5),
    (party_add_prisoners, ":party_no", "trp_steppe_bandit", ":num_steppe"),

    (store_random_in_range, ":num_forest", 1, 4),
    (party_add_prisoners, ":party_no", "trp_forest_bandit", ":num_forest"),

    (store_random_in_range, ":num_mountain", 1, 4),
    (party_add_prisoners, ":party_no", "trp_mountain_bandit", ":num_mountain"),
  ]),

# script_mnh_get_manhunter_prisoner_price
# Calculates total ransom broker price for all prisoners in a manhunter party
# Input: param1 = party_id
# Output: reg0 = total price
("mnh_get_manhunter_prisoner_price",
  [
    (store_script_param_1, ":party_no"),

    (assign, ":total_price", 0),
    (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_prisoner_stack_get_troop_id, ":troop_no", ":party_no", ":i_stack"),
      (neg|troop_is_hero, ":troop_no"),
      (party_prisoner_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
      (store_character_level, ":troop_level", ":troop_no"),
      (store_add, ":price", ":troop_level", 10),
      (val_mul, ":price", ":price"),
      (val_div, ":price", 6),
      (val_mul, ":price", ":stack_size"),
      (val_add, ":total_price", ":price"),
    (try_end),

    (assign, reg0, ":total_price"),
  ]),

# script_mnh_buy_manhunter_prisoners
# Transfers all non-hero prisoners from a manhunter party to the player, deducts gold
# Input: param1 = party_id, param2 = total_price
("mnh_buy_manhunter_prisoners",
  [
    (store_script_param_1, ":party_no"),
    (store_script_param_2, ":total_price"),

    (store_troop_gold, ":gold", "trp_player"),
    (ge, ":gold", ":total_price"),
    (troop_remove_gold, "trp_player", ":total_price"),

    (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
    (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
      (party_prisoner_stack_get_troop_id, ":troop_no", ":party_no", ":i_stack"),
      (neg|troop_is_hero, ":troop_no"),
      (party_prisoner_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
      (party_remove_prisoners, ":party_no", ":troop_no", ":stack_size"),
      (party_add_prisoners, "p_main_party", ":troop_no", ":stack_size"),
    (try_end),
  ]),
]
