# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_distribute_gold_to_lord_and_holdings (script)
# Called by menus in 2 domains: castle, diplomacy
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

dplmc_distribute_gold_to_lord_and_holdings_scripts = [
#script_dplmc_get_troop_morality_value
#
#Related to script_dplmc_remove_gold_from_lord_and_holdings, divides the gold
#between the lord and his fortresses in a semi-intelligent way.
#
#INPUT:
#   arg1: the amount of gold
#   arg2: the lord's ID
("dplmc_distribute_gold_to_lord_and_holdings",
   [
	(store_script_param_1, ":gold_left"),
	(store_script_param_2, ":lord_no"),

	(try_begin),
		(lt, ":lord_no", 0),#Invalid ID
	(else_try),
		#If the number is negative, handle this using script_dplmc_remove_gold_from_lord_and_holdings
		(lt, ":gold_left", 0),
		(val_mul, ":gold_left", -1),
		(call_script, "script_dplmc_remove_gold_from_lord_and_holdings", ":gold_left", ":lord_no"),
		(assign, ":gold_left", 0),
	(else_try),
		(neq, ":lord_no", "trp_player"),
		(neg|troop_is_hero, ":lord_no"),#Not hero or player
        (troop_add_gold, ":lord_no", ":gold_left"),
        (assign, ":gold_left", 0),
	(else_try),
		#The player doesn't use center wealth to pay garrison wages, so just
		#give it directly.
		(eq, ":lord_no", "trp_player"),
		(troop_add_gold, "trp_player", ":gold_left"),
		(assign, ":gold_left", 0),
	(else_try),
		(neg|troop_is_hero, ":lord_no"),#If the lord isn't the player, and isn't a hero, do nothing
	(else_try),
		(troop_get_slot, ":target_gold", ":lord_no", slot_troop_wealth),
		(val_max, ":target_gold", 0),
		#If the lord is low on gold, first he takes enough gold so he isn't low on funds,
		#or all of the gold, whichever is less.
		(store_sub, ":gold_to_give", 6000, ":target_gold"),#6000 is the standard starting gold for lords (kings start with more, but don't increase this for them, since I'm using this number as a "low on gold" threshold)
		(val_max, ":gold_to_give", 0),
		(val_min, ":gold_to_give", ":gold_left"),

		(val_add, ":target_gold", ":gold_to_give"),
		(troop_set_slot, ":lord_no", slot_troop_wealth, ":target_gold"),
		(val_sub, ":gold_left", ":gold_to_give"),
		#If gold remains, the lord gives some to any castles or towns he owns that have
		#low wealth.  Note that iterating in this order means that towns get checked
		#before castles do.
		(gt, ":gold_left", 0),
		(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			(party_slot_eq, ":center_no", slot_town_lord, ":lord_no"),
			(party_get_slot, ":target_gold", ":center_no", slot_town_wealth),
			#Don't give gold to centers with garrisons more than 50% above the ideal size
			(store_party_size_wo_prisoners, ":garrison_size", ":center_no"),
			(call_script, "script_party_get_ideal_size", ":center_no"),#This script has been modified to support this use
			(val_mul, reg0, 3),
			(val_div, reg0, 2),
			(ge, reg0, ":garrison_size"),

			(try_begin),
				(party_slot_eq, ":center_no", slot_party_type, spt_town),
				(store_sub, ":gold_to_give", 4000, ":target_gold"),#4000 is the standard starting gold for towns
			(else_try),
				(store_sub, ":gold_to_give", 2000, ":target_gold"),#2000 is the standard starting gold for castles
			(try_end),

			(val_max, ":gold_to_give", 0),
			(val_min, ":gold_to_give", ":gold_left"),
			(gt, ":gold_to_give", 0),
			(val_add, ":target_gold", ":gold_to_give"),
			(party_set_slot, ":center_no", slot_town_wealth, ":target_gold"),
			(val_sub, ":gold_left", ":gold_to_give"),
		(try_end),
		#If gold is left -- the lord isn't low on gold, and none of his walled centers are --
		#he pockets the remainder.
		(gt, ":gold_left", 0),
		(troop_get_slot, ":target_gold", ":lord_no", slot_troop_wealth),
		(val_add, ":target_gold", ":gold_left"),
		(val_max, ":target_gold", 0),
		(troop_set_slot, ":lord_no", slot_troop_wealth, ":target_gold"),
		(assign, ":gold_left", 0),
	(try_end),
	])
]
