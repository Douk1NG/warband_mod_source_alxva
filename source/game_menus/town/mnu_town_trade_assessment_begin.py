# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

town_trade_assessment_begin_menu = [
(
   "town_trade_assessment_begin",0,
   #"You overhear the following details about the roads out of town :^(experimental feature -- this may go into dialogs)^{s42}^You also overhear several discussions about the price of trade goods across the local area.^You listen closely, trying to work out the best deals around.",
   "You overhear several discussions about the price of trade goods across the local area.^You listen closely, trying to work out the best deals around.",
    "none",
    [
	(str_clear, s42),
##	(call_script, "script_merchant_road_info_to_s42", "$g_encountered_party"),

    ],

    [
      ("continue",[],"Continue...",
       [
           (assign,"$auto_enter_town", "$current_town"),
           (assign, "$g_town_assess_trade_goods_after_rest", "$current_town"), #SB : save this
           (call_script, "script_get_max_skill_of_player_party", "skl_trade"),
           (val_div, reg0, 2),
           (store_sub, ":num_hours", 6, reg0),
           (assign, "$g_last_rest_center", "$current_town"),
           (assign, "$g_last_rest_payment_until", -1),
           (rest_for_hours, ":num_hours", 5, 0), #rest while not attackable
           (change_screen_return),
        ]),
      ("go_back_dot",[],"Go back.",
       [
           (jump_to_menu,"mnu_town_trade"),
        ]),
    ]
  )
]
