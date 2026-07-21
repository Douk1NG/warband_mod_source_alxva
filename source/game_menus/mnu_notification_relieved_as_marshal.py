# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

notification_relieved_as_marshal_menu = [
("notification_relieved_as_marshal", mnf_disable_all_keys,
    "{s4} wishes to inform you that your services as marshal are no longer required. In honor of valiant efforts on behalf of the realm over the last {reg4} days, however, {reg8?she:he} offers you a purse of {reg5} denars.",
    "none",
    [
	(assign, reg4, "$g_player_days_as_marshal"),



	(store_div, ":renown_gain", "$g_player_days_as_marshal",4),
	(val_min, ":renown_gain", 20),
	(store_mul, ":denar_gain", "$g_player_days_as_marshal", 50),
	(val_max, ":denar_gain", 200),
	(val_min, ":denar_gain", 4000),
	(troop_add_gold, "trp_player", ":denar_gain"),
	(call_script, "script_change_troop_renown", "trp_player", ":renown_gain"),
	(assign, "$g_player_days_as_marshal", 0),
	(assign, "$g_dont_give_marshalship_to_player_days", 15),
	(assign, reg5, ":denar_gain"),

	(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
	(str_store_troop_name, s4, ":faction_leader"),
	##diplomacy start+ get gender with script
	#(troop_get_type, reg8, ":faction_leader"),#<- OLD
	(assign, ":save_reg0", reg0),
	(call_script, "script_dplmc_store_troop_is_female", ":faction_leader"),
	(assign, reg8, reg0),
	(assign, reg0, ":save_reg0"),
	##diplomacy end+
	],

	 [
      ("continue",[],"Continue",
       [
         (change_screen_return),
       ]),
    ]
  )
]
