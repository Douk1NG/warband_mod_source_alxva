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



  # Consuming food at every 14 hours
  

consume_food_simple_triggers = [
(14,
   [
    (eq, "$g_player_is_captive", 0),
    (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
    (assign, ":num_men", 0),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
      (val_add, ":num_men", ":stack_size"),
    (try_end),
    (val_div, ":num_men", 3),
    (val_max, ":num_men", 1),
    # (try_begin), #SB : val_max
      # (eq, ":num_men", 0),
      # (val_add, ":num_men", 1),
    # (try_end),

    (try_begin),
      (assign, ":number_of_foods_player_has", 0),
      (try_for_range, ":cur_edible", food_begin, food_end),
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_edible", imod_rotten),
        (val_add, ":number_of_foods_player_has", 1),
      (try_end),
      (try_begin),
        (ge, ":number_of_foods_player_has", 6),
        (unlock_achievement, ACHIEVEMENT_ABUNDANT_FEAST),
      (try_end),
    (try_end),

    # #SB : pre-calculate consumption amount for qst_deliver_wine items, although as with deliver_grain we might not care
    # (try_begin),
      # (check_quest_active,"qst_deliver_wine"),
      # (quest_get_slot, ":quest_target_item", "qst_deliver_wine", slot_quest_target_item),
      # (quest_get_slot, ":quest_target_amount", "qst_deliver_wine", slot_quest_target_amount),
      # (assign, ":quest_amount", 0),
      # (troop_get_inventory_capacity, ":capacity", "trp_player"),
      # (try_for_range, ":cur_slot", 10, ":capacity"),
        # (troop_get_inventory_slot, ":cur_item", "trp_player", ":cur_slot"),
        # (eq, ":cur_item", ":quest_target_item"),
        # (troop_inventory_slot_get_item_amount, ":cur_amount", "trp_player", ":cur_slot"),
        # (val_add, ":quest_amount", ":cur_amount"),
      # (try_end),
    # (try_end),
    (assign, ":consumption_amount", ":num_men"),
    (assign, ":no_food_displayed", 0),
    (try_for_range, ":unused", 0, ":consumption_amount"),
      (assign, ":available_food", 0),
      (try_for_range, ":cur_food", itm_raw_date_fruit, food_end),
        (neq, ":cur_food", "itm_furs"),
        (item_slot_eq, ":cur_food", slot_item_edible, 1),
        (item_set_slot, ":cur_food", slot_item_is_checked, 0),
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_food", imod_rotten),
        (this_or_next|neq, ":cur_food", "itm_wine"),
        (neq, ":cur_food", "itm_ale"),
        (val_add, ":available_food", 1),
      (try_end),
      (try_begin),
        (gt, ":available_food", 0),
        (store_random_in_range, ":selected_food", 0, ":available_food"),
        (call_script, "script_consume_food", ":selected_food"),
      (else_try),
        (eq, ":no_food_displayed", 0),
        (display_message, "@Party has nothing to eat!", message_defeated), #SB : same colour const
        (call_script, "script_change_player_party_morale", -3),
        (assign, ":no_food_displayed", 1),
#NPC companion changes begin
        (try_begin),
          (gt, ":num_men", 1), #SB : easier check
            # (call_script, "script_party_count_fit_regulars", "p_main_party"),
            # (gt, reg0, 0),
          (call_script, "script_objectionable_action", tmt_egalitarian, "str_men_hungry"),
        (try_end),
#NPC companion changes end
      (try_end),
    (try_end),
    ]),
]
