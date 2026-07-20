# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

village_loot_complete_menu = [
(
    "village_loot_complete",mnf_disable_all_keys,
    "On your orders your troops sack the village, pillaging everything of any value,\
 and then put the buildings to the torch. From the coins and valuables that are found, you get your share of {reg1} denars.",
    "none",
    [
        (get_achievement_stat, ":number_of_village_raids", ACHIEVEMENT_THE_BANDIT, 0),
        (get_achievement_stat, ":number_of_caravan_raids", ACHIEVEMENT_THE_BANDIT, 1),
        (val_add, ":number_of_village_raids", 1),
        (set_achievement_stat, ACHIEVEMENT_THE_BANDIT, 0, ":number_of_village_raids"),

        (try_begin),
          (ge, ":number_of_village_raids", 3),
          (ge, ":number_of_caravan_raids", 3),
          (unlock_achievement, ACHIEVEMENT_THE_BANDIT),
        (try_end),

        (party_get_slot, ":village_lord", "$current_town", slot_town_lord),
        (try_begin),
          (gt,  ":village_lord", 0),
          (call_script, "script_change_player_relation_with_troop", ":village_lord", -5),
        (try_end),
        (store_random_in_range, ":enmity", -35, -25),
        (call_script, "script_change_player_relation_with_center", "$current_town", ":enmity"),

        (store_faction_of_party, ":village_faction", "$current_town"),
        (store_relation, ":relation", ":village_faction", "fac_player_supporters_faction"),
        (try_begin),
          (lt, ":relation", 0),
          (call_script, "script_change_player_relation_with_faction", ":village_faction", -3),
        (try_end),

        (assign, ":money_gained", 50), #SB : change this to be somewhat based on actual wealth
        (party_get_slot, ":village_elder", "$current_town",slot_town_elder),
        (try_begin),
          (gt, ":village_elder", 0),
          (store_troop_gold, ":money_gained", ":village_elder"),
          (troop_remove_gold, ":village_elder", ":money_gained"),
          (val_div, ":money_gained", 2),
        (try_end),
        (val_max, ":money_gained", 50),
        (party_get_slot, ":prosperity", "$current_town", slot_town_prosperity),
        (store_mul, ":prosperity_of_village_mul_5", ":prosperity", 5),
        (val_add, ":money_gained", ":prosperity_of_village_mul_5"),
        (call_script, "script_troop_add_gold", "trp_player", ":money_gained"),

        (assign, ":morale_increase", 3),
        (store_div, ":money_gained_div_100", ":money_gained", 100),
        (val_add, ":morale_increase", ":money_gained_div_100"),
        (call_script, "script_change_player_party_morale", ":morale_increase"),


        # (faction_get_slot, ":faction_morale", ":village_faction",  slot_faction_morale_of_player_troops),
        (store_mul, ":morale_decrease", ":morale_increase", -200),
        (call_script, "script_change_faction_troop_morale", ":village_faction", ":morale_decrease", 1), #SB : script call
        # (val_sub, ":faction_morale", ":morale_increase_mul_2"),
        # (faction_set_slot, ":village_faction",  slot_faction_morale_of_player_troops, ":faction_morale"),



#NPC companion changes begin
        (call_script, "script_objectionable_action", tmt_humanitarian, "str_loot_village"),
#NPC companion changes end
        (assign, reg1, ":money_gained"),
      ],
    [
      ("continue",[], "Continue...",
       [
       (jump_to_menu, "mnu_close"),
          (call_script, "script_calculate_amount_of_cattle_can_be_stolen", "$current_town"),
          (assign, ":max_cattle", reg0),
          (val_mul, ":max_cattle", 3),
          (val_div, ":max_cattle", 2),
          (party_get_slot, ":num_cattle", "$current_town", slot_village_number_of_cattle),
          (val_min, ":max_cattle", ":num_cattle"),
          (val_add, ":max_cattle", 1),
          (store_random_in_range, ":random_value", 0, ":max_cattle"),
          (try_begin),
            (gt, ":random_value", 0),
            (call_script, "script_create_cattle_herd", "$current_town", ":random_value"),
            (val_sub, ":num_cattle", ":random_value"),
            (party_set_slot, "$current_town", slot_village_number_of_cattle, ":num_cattle"),
          (try_end),

          #below line changed with below lines to make plunder result more realistic. Now only items produced in bound town can be stolen after raid.
          #(reset_item_probabilities,100),

          #begin of changes
          (party_get_slot, ":bound_town", "$current_town", slot_village_market_town),
          #the above line is the culprit for divide by zero
          # (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
          (assign, ":item_to_price_slot", slot_town_trade_good_prices_begin),
          (reset_item_probabilities,100),
          (assign, ":total_probability", 0),
          (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
            (party_get_slot, ":cur_price", ":bound_town", ":item_to_price_slot"),
            (val_add, ":item_to_price_slot", 1),
            (call_script, "script_center_get_production", ":bound_town", ":cur_goods"),
            (assign, ":cur_probability", reg0),
            (call_script, "script_center_get_consumption", ":bound_town", ":cur_goods"),
            (val_div, reg0, 3),
            (val_add, ":cur_probability", reg0),
            (val_mul, ":cur_probability", 4),
            (try_begin),
              (neq, ":cur_price", 0),
              (val_mul, ":cur_probability", average_price_factor),
              (val_div, ":cur_probability", ":cur_price"), #divide by zero error here
            (try_end),
            #first only simulation
            #(set_item_probability_in_merchandise,":cur_goods",":cur_probability"),
            (val_add, ":total_probability", ":cur_probability"),
            # (assign, reg1, ":total_probability"),
            # (assign, reg2, ":cur_price"),
            # (assign, reg3, ":cur_probability"),
            # (assign, reg4, ":item_to_price_slot"),
            # (str_store_item_name, s1, ":cur_goods"),
            # (display_message, "@{s1} price : {reg2} in slot {reg4}, probability: {reg3};{reg1} total"),
          (try_end),
          (val_max, ":total_probability", 1),
          (assign, ":item_to_price_slot", slot_town_trade_good_prices_begin),
          (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
            (party_get_slot, ":cur_price", ":bound_town", ":item_to_price_slot"),
            (val_add, ":item_to_price_slot", 1),
            (call_script, "script_center_get_production", ":bound_town", ":cur_goods"),
            (assign, ":cur_probability", reg0),
            (call_script, "script_center_get_consumption", ":bound_town", ":cur_goods"),
            (val_div, reg0, 3),
            (val_add, ":cur_probability", reg0),
            (val_mul, ":cur_probability", 4),
            (try_begin),
              (neq, ":cur_price", 0),
              (val_mul, ":cur_probability", average_price_factor),
              (val_div, ":cur_probability", ":cur_price"), #divide by zero error here
            (try_end),

            (val_mul, ":cur_probability", num_merchandise_goods),
            (val_mul, ":cur_probability", 100),
            (val_div, ":cur_probability", ":total_probability"),

            (set_item_probability_in_merchandise,":cur_goods",":cur_probability"),
          (try_end),
          #end of changes

          (troop_add_merchandise,"trp_temp_troop",itp_type_goods,30),
          (troop_sort_inventory, "trp_temp_troop"),
          (change_screen_loot, "trp_temp_troop"),
        ]),
    ],
  )
]
