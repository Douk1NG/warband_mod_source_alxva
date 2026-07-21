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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_sell_all_prisoners_from_party_scripts = [
# "script_dplmc_sell_all_prisoners_from_party"
#
#INPUT:
#Arg 1: party to sell regular prisoners from
#Arg 2: actually remove (positive for yes, zero or negative for no)
#Arg 3: if positive, use this as a fixed price instead of calculating dynamically
#OUTPUT:
#reg0: amount of gold gained (or would have been gained if the sale occurred)
#reg1: number of prisoners sold (or would have been sold if the sale occurred)
("dplmc_sell_all_prisoners_from_party",
   [
    (store_script_param_1, ":source_party"),
    (store_script_param_2, ":actually_remove"),
    (store_script_param, ":fixed_price", 3),

    (assign, ":total_removed", 0),
    (assign, ":total_income", 0),
    (party_get_num_prisoner_stacks, ":num_stacks", ":source_party"),
    (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
      (party_prisoner_stack_get_troop_id, ":troop_no", ":source_party", ":i_stack"),
      #SB : correction to use game script
      (call_script, "script_game_check_prisoner_can_be_sold", ":troop_no"),
      (eq, reg0, 1),
      # (neg|troop_is_hero, ":troop_no"),
      (party_prisoner_stack_get_size, ":stack_size", ":source_party", ":i_stack"),
      (try_begin),
         (gt, ":fixed_price", 0),
         (assign, ":sell_price", ":fixed_price"),
      (else_try),
         (call_script, "script_game_get_prisoner_price", ":troop_no"),
         (assign, ":sell_price", reg0),
      (try_end),
      (store_mul, ":stack_total_price", ":sell_price", ":stack_size"),
      (val_add, ":total_income", ":stack_total_price"),
      (val_add, ":total_removed", ":stack_size"),
      (gt, ":actually_remove", 0),#Stop short if this is a dry run
      (party_remove_prisoners, ":source_party", ":troop_no", ":stack_size"),
    (try_end),
    (try_begin),
      (gt, ":actually_remove", 0),#Stop short if this is a dry run
      (troop_add_gold, "trp_player", ":total_income"),
    (try_end),
    (assign, reg0, ":total_income"),
    (assign, reg1, ":total_removed"),
  ])
]
