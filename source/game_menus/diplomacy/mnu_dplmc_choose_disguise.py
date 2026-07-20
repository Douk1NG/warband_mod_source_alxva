# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_choose_disguise_menu = [
(
    "dplmc_choose_disguise", 0,
    "You are about to sneak into {s1}. Make sure you don't bring suspicious items or excess denars that might be confiscated. {s2}",
    "none",
    [

         (troop_get_inventory_capacity, ":inv_cap", "trp_random_town_sequence"),
         (assign, ":count", 0),
         (try_for_range, ":i_slot", ek_food + 1, ":inv_cap"),
           (troop_get_inventory_slot, ":cur_item", "trp_random_town_sequence", ":i_slot"),
           (gt, ":cur_item", -1),
           #(assign, reg3, ":cur_item"),
           #(display_message, "@{reg3}"),
           (val_add, ":count", 1),
         (try_end),
         # (assign, reg0, ":count"),
         # (assign, reg1, "$temp"),
         # (display_message, "@{reg0} , {reg1}"),
         (try_begin),
            (gt, ":count", "$temp"),
            #put stuff back
            (set_show_messages, 0), #move all gold
            (call_script, "script_move_inventory_and_gold", "trp_random_town_sequence", "trp_player", -1),
            (set_show_messages, 1),
            (display_message, "@You cannot bring that many items with you. Your items have been returned to your inventory."),
         (try_end),

        (str_store_party_name, s1, "$current_town"),
        #build text
        (try_begin),
          (eq, "$sneaked_into_town", disguise_none),
          (str_store_string, s2, "@Select a suitable disguise for this occasion."),
          (assign, "$temp", 0),
        (else_try),
          (eq, "$sneaked_into_town", disguise_pilgrim),
          (str_store_string, s2, "@As a poor pilgrim with a stout stick and a few tricks up your sleeve, you will be able to blend in with the crowds but not bring much of value with you."),
          (assign, "$temp", 6),
        (else_try),
          (eq, "$sneaked_into_town", disguise_farmer),
          (str_store_string, s2, "@As a farmer, you will be able to a wrangle livestock and smuggle articles of food through."),
          (assign, "$temp", 15),
        (else_try),
          (eq, "$sneaked_into_town", disguise_hunter),
          (str_store_string, s2, "@As a hunter, provisions and raw goods are expected as well as horseflesh."),
          (assign, "$temp", 12),
        (else_try),
          (eq, "$sneaked_into_town", disguise_guard),
          (str_store_string, s2, "@As a caravan guard, you will be able to bear weapons but bring only a few personal belongings."),
          (assign, "$temp", 6),
        (else_try),
          (eq, "$sneaked_into_town", disguise_merchant),
          (str_store_string, s2, "@As a merchant, you will be able to bring any assortment of goods."),
          (assign, "$temp", 32),
        (else_try),
          (eq, "$sneaked_into_town", disguise_bard),
          (str_store_string, s2, "@As a bard, you will be allowed some personal possessions and your instrument."),
          (assign, "$temp", 9),
        (try_end),
        (set_fixed_point_multiplier, 100),
        (init_position, pos0),
        (try_begin),
          (str_is_empty, s2),
          (position_set_x, pos0, 17),
          (position_set_y, pos0, 30),
          (position_set_z, pos0, 100),
        (else_try),
          (position_set_x, pos0, 60),
          (position_set_y, pos0, 20),
          (position_set_z, pos0, 100),
        (try_end),
        (set_game_menu_tableau_mesh, "tableau_game_inventory_window", "trp_player", pos0),
        (troop_get_slot, "$temp_2", "trp_player", slot_troop_player_disguise_sets),
    ],
    [
      ("continue",
      [(gt, "$temp", 0),
       (assign, reg1, "$temp"),],
      "Choose up to {reg1} items to bring.",
      [
        (change_screen_loot, "trp_random_town_sequence"),
      ]),

      ("continue",
      [(neq, "$sneaked_into_town", disguise_none)],
      "Select how much gold to carry.",
      [
        (assign, "$pool_troop", "trp_random_town_sequence"),
        (start_presentation, "prsnt_deposit_withdraw_money"),
      ]),

      ("continue",
      [(neq, "$sneaked_into_town", disguise_none)],
      "Attempt to sneak in...",
      [
        (set_show_messages, 0),

        #do inventory placeholder
        (troop_clear_inventory, "trp_temp_troop"),
        (call_script, "script_dplmc_copy_inventory", "trp_player", "trp_temp_troop"),
        (call_script, "script_dplmc_copy_inventory", "trp_random_town_sequence", "trp_player"),
        (call_script, "script_dplmc_copy_inventory", "trp_temp_troop", "trp_random_town_sequence"),
        #do gold swap
        (store_troop_gold, ":cur_amount", "trp_random_town_sequence"),
        (store_troop_gold, ":cur_gold", "trp_player"),
        (troop_remove_gold, "trp_player", ":cur_gold"),
        (troop_remove_gold, "trp_random_town_sequence", ":cur_amount"),
        (troop_add_gold, "trp_player", ":cur_amount"),
        (troop_add_gold, "trp_random_town_sequence", ":cur_gold"),

        (set_show_messages, 1),


        (faction_get_slot, ":player_alarm", "$g_encountered_party_faction", slot_faction_player_alarm),
        (party_get_num_companions, ":num_men", "p_main_party"),
        (party_get_num_prisoners, ":num_prisoners", "p_main_party"),
        (val_add, ":num_men", ":num_prisoners"),
        (val_mul, ":num_men", 2),
        (val_div, ":num_men", 3),
        (store_add, ":get_caught_chance", ":player_alarm", ":num_men"),
        (store_random_in_range, ":random_chance", 0, 100),
        (try_begin),
            (this_or_next|ge, "$cheat_mode", 1),
            (this_or_next|ge, ":random_chance", ":get_caught_chance"),
            (eq, "$g_last_defeated_bandits_town", "$g_encountered_party"),
            (assign, "$g_last_defeated_bandits_town", 0),
            (assign, "$town_entered", 1), #dckplmc
            (assign, "$g_mt_mode", tcm_disguised),
            (jump_to_menu, "mnu_sneak_into_town_suceeded"),
        (else_try),
            (jump_to_menu,"mnu_sneak_into_town_caught"),
        (try_end),
      ]),

      ("disguise_pilgrim",
      [
        (neq, "$sneaked_into_town", disguise_pilgrim),
      ], "Don the robes of a poor pilgrim.",
      [
        (assign, "$sneaked_into_town", disguise_pilgrim),
      ]),

      #SB : todo, add peasant woman variant
      ("disguise_farmer",
      [(store_and, ":disguise", "$temp_2", disguise_farmer),
       (eq, ":disguise", disguise_farmer),
       (neq, "$sneaked_into_town", disguise_farmer),],
      "Accept your fate as a downtrodden farmer.",
      [
        (assign, "$sneaked_into_town", disguise_farmer),
      ]),
      ("disguise_hunter",
      [(store_and, ":disguise", "$temp_2", disguise_hunter),
       (eq, ":disguise", disguise_hunter),
       (neq, "$sneaked_into_town", disguise_hunter),],
      "Disguise yourself as a skilled {huntsman/huntress}.",
      [
        (assign, "$sneaked_into_town", disguise_hunter),
      ]),
      ("disguise_guard",
      [(store_and, ":disguise", "$temp_2", disguise_guard),
       (eq, ":disguise", disguise_guard),
       (neq, "$sneaked_into_town", disguise_guard),],
      "Pass yourself off as a caravan guard.",
      [
        (assign, "$sneaked_into_town", disguise_guard),
      ]),
      ("disguise_merchant",
      [(store_and, ":disguise", "$temp_2", disguise_merchant),
       (eq, ":disguise", disguise_merchant),
       (neq, "$sneaked_into_town", disguise_merchant),],
      "Adopt the guise of a trader.",
      [
        (assign, "$sneaked_into_town", disguise_merchant),
      ]),
      ("disguise_bard",
      [(store_and, ":disguise", "$temp_2", disguise_bard),
       (eq, ":disguise", disguise_bard),
       (neq, "$sneaked_into_town", disguise_bard),],
      "Try your luck as a bard.",
      [
        (assign, "$sneaked_into_town", disguise_bard),
      ]),

      ("back",
      [],
      "Never mind...",
      [
        #put stuff back
        (set_show_messages, 0), #move all gold
        (call_script, "script_move_inventory_and_gold", "trp_random_town_sequence", "trp_player", -1),
        (set_show_messages, 1),

        (assign, "$sneaked_into_town", disguise_none),
        (jump_to_menu, "mnu_castle_outside"),
      ]),
    ]
  )
]
