# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_initialize_autoloot (script)
# Called by menus in 4 domains: camp, diplomacy, town, village
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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_initialize_autoloot_scripts = [
#script_dplmc_print_player_spouse_says_my_husband_wife_to_s0
##
##Only needs to be called once, but it's safe to call multiple times
##(it uses "$g_autoloot" to store the version)
##
##Inputs: arg1: 1 to force this to run
##Outputs: None
("dplmc_initialize_autoloot",
  [
	(store_script_param_1, ":force_to_run"),

	(try_begin),
		#Check if there is anything to do
		(this_or_next|eq, ":force_to_run", 1),
			(neq, "$g_autoloot", 2),
      (try_begin),
		   #Print a message to make it obvious when this is happening more than it should.
		   (ge, "$cheat_mode", 1),
		   (store_current_hours, ":hours"),
		   (gt, ":hours", 0),
		   (display_message, "@{!}Initializing auto-loot.  This message should not appear more than once."),
      (try_end),
		#Initialize
		(try_for_range, ":cur_food", "itm_raw_date_fruit", food_end),
			(neq, ":cur_food", "itm_furs"),
			(item_set_slot, ":cur_food", dplmc_slot_item_food_portion, 1),
		(try_end),

		# #deprecated due to 1.165 operations
		# (call_script, "script_dplmc_init_item_difficulties"),
		# (call_script, "script_dplmc_init_item_base_score"),

		(assign, "$g_dplmc_auto_sell_price_limit", 50),
		(assign, "$g_dplmc_sell_items_when_leaving", 0),
		(assign, "$g_dplmc_buy_food_when_leaving", 0),

		(item_set_slot, itp_type_book, dplmc_slot_item_type_not_for_sell, 1),
		(item_set_slot, itp_type_goods, dplmc_slot_item_type_not_for_sell, 1),
		(item_set_slot, itp_type_animal, dplmc_slot_item_type_not_for_sell, 1),

		(assign, "$g_autoloot", 2),
	(try_end),
  ])
]
