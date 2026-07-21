# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_trade_auto_buy_food_begin (menu)
# Called by menus in 2 domains: town, village
# ======================================================================

# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_trade_auto_buy_food_begin_menu = [
(
    "dplmc_trade_auto_buy_food_begin",0,
    "You will automatically buy food according to your shopping list. Do you want to continue?^^You can view and configure the shopping list here.",
    "none", [],
  [
    ("continue",[
	  #dplmc+ added to check against weird conditions
 	  (assign, ":merchant_troop", -1),
	  (try_begin),
		  (is_between, "$current_town", towns_begin, towns_end),
        (party_get_slot, ":merchant_troop", "$current_town", slot_town_merchant),
     (else_try),
		  (is_between, "$current_town", villages_begin, villages_end),
        (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
     (try_end),
	  (ge, ":merchant_troop", 1),
	  #dplmc+ end addition
	 ],"Continue...",
    [
 	   (assign, ":merchant_troop", -1),
	   (try_begin),
		  (is_between, "$current_town", towns_begin, towns_end),
        (party_get_slot, ":merchant_troop", "$current_town", slot_town_merchant),
      (else_try),
		  (is_between, "$current_town", villages_begin, villages_end),
        (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
      (try_end),
	   (call_script, "script_dplmc_auto_buy_food", "trp_player", ":merchant_troop"),
      (jump_to_menu, "$g_next_menu"),
      ]),

    ("dplmc_change_shopping_list_of_food",[],"Configure your shopping list.",[(start_presentation, "prsnt_dplmc_shopping_list_of_food"),]),
    ("go_back",[],"Go back",[(jump_to_menu, "$g_next_menu")]),
   ]
  )
]
