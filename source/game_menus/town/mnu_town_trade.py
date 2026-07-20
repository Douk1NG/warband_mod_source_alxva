# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

town_trade_menu = [
(
    "town_trade",0,
    "The marketplace is home to shops, inns, warehouses, and merchant hubs. Coming upon the main plaza, you decide where you will go...",
    "none",
    [
                (try_begin),
                (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
                (ge, ":center_lord", 0),
                (set_fixed_point_multiplier, 100),
                (position_set_x, pos1, 70),
                (position_set_y, pos1, 5),
                (position_set_z, pos1, 75),
                (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":center_lord", pos1),
                (try_end),],
    [
      #SB : re-order dialog options for consistency, add talk instead of trade option
		##diplomacy start+
		#Begin auto-sell, credit rubik (Custom Commander)
      ## CC
      ("auto_sell",[],
       "Sell items automatically.",
       [
          (assign, "$g_next_menu", "mnu_town"),
          (jump_to_menu,"mnu_dplmc_trade_auto_sell_begin"),
        ]),

      ("auto_buy_food",[
	  (eq,1,0), #Disabled because, again, running out of space. Also this is pretty pointless who uses it.
	  ],
       "Buy food automatically.",
       [
          (assign, "$g_next_menu", "mnu_town"),
          (jump_to_menu,"mnu_dplmc_trade_auto_buy_food_begin"),
        ]),

      ## CC
		#End auto-sell, credit rubik (Custom Commander)
		##diplomacy start+
      ("assess_prices",
       [
         (store_faction_of_party, ":current_town_faction", "$current_town"),
         (store_relation, ":reln", ":current_town_faction", "fac_player_supporters_faction"),
         (ge, ":reln", 0),
         ],
       "Assess the local prices.",
       [
           (jump_to_menu,"mnu_town_trade_assessment_begin"),
        ]),

      ("trade_with_arms_merchant",[(party_slot_ge, "$current_town", slot_town_weaponsmith, 1)],
       "Trade with the arms merchant.",
       [
            (party_get_slot, ":merchant_troop", "$current_town", slot_town_weaponsmith),
            (assign, "$g_talk_troop", ":merchant_troop"),
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_start_town_conversation", slot_town_weaponsmith, 10),
            (else_try),
              (troop_set_slot, ":merchant_troop", slot_troop_met, 1),
              (change_screen_trade, ":merchant_troop"),
            (try_end),
        ]),
      ("trade_with_armor_merchant",[(party_slot_ge, "$current_town", slot_town_armorer, 1)],
       "Trade with the armor merchant.",
       [
            (party_get_slot, ":merchant_troop", "$current_town", slot_town_armorer),
            (assign, "$g_talk_troop", ":merchant_troop"),
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_start_town_conversation", slot_town_armorer, 9),
            (else_try),
              (troop_set_slot, ":merchant_troop", slot_troop_met, 1),
              (change_screen_trade, ":merchant_troop"),
            (try_end),
        ]),
      ("trade_with_horse_merchant",[(party_slot_ge, "$current_town", slot_town_horse_merchant, 1)],
       "Trade with the horse merchant.",
       [
            (party_get_slot, ":merchant_troop", "$current_town", slot_town_horse_merchant),
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_start_town_conversation", slot_town_horse_merchant, 12),
            (else_try),
              (troop_set_slot, ":merchant_troop", slot_troop_met, 1),
              (change_screen_trade, ":merchant_troop"),
            (try_end),
        ]),
      ("trade_with_goods_merchant",[(party_slot_ge, "$current_town", slot_town_merchant, 1)],
       "Trade with the goods merchant.",
       [
            (party_get_slot, ":merchant_troop", "$current_town", slot_town_merchant),
            (assign, "$g_talk_troop", ":merchant_troop"),
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_start_town_conversation", slot_town_merchant, 9),
            (else_try),
              (troop_set_slot, ":merchant_troop", slot_troop_met, 1),
              (change_screen_trade, ":merchant_troop"),
            (try_end),
        ]),
      #Autotrade begin
      ("auto_Trade",[],
       "Buy and sell trade goods automatically.",
       [
          (assign, "$g_next_menu", "mnu_town"),
          (jump_to_menu,"mnu_auto_trade"),
        ]),
      #Autotrade end
      ("back_to_town_menu",[],"Head back.",
       [
           (jump_to_menu,"mnu_town"),
        ]),
    ]
  )
]
