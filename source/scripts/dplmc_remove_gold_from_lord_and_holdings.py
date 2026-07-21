# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_remove_gold_from_lord_and_holdings (script)
# Called by menus in 2 domains: castle, town
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

dplmc_remove_gold_from_lord_and_holdings_scripts = [
#"script_dplmc_remove_gold_from_lord_and_holdings"
#
#
#INPUT:
#   arg1: the amount of money to remove (greater than zero)
#   arg2: the ID of the lord spending the money
#
#OUTPUT:
#   None
("dplmc_remove_gold_from_lord_and_holdings",
   [
    (store_script_param_1, ":gold_cost"),
	(store_script_param_2, ":lord_no"),

	(try_begin),
		(lt, ":lord_no", 0),#Invalid ID
	(else_try),
		(neq, ":lord_no", "trp_player"),
		(neg|troop_is_hero, ":lord_no"),#Not player or hero
	(else_try),
		#If the number is negative, give gold instead of taking it.
		#Handle this using script_dplmc_distribute_gold_to_lord_and_holdings
		(lt, ":gold_cost", 0),
		(val_mul, ":gold_cost", -1),
		(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":gold_cost", ":lord_no"),
		(assign, ":gold_cost", 0),
	(else_try),
		#For the player, first subtract the gold from his treasury (if any).
		(eq, ":lord_no", "trp_player"),
	    (store_troop_gold, ":treasury", "trp_household_possessions"),
		(try_begin),
		(ge, ":treasury", 1),
		(val_min, ":treasury", ":gold_cost"),
		(call_script, "script_dplmc_withdraw_from_treasury", ":treasury"),
		(val_sub, ":gold_cost", ":treasury"),
		(try_end),
		(store_troop_gold, ":treasury", "trp_player"),
		(try_begin),
			(ge, ":treasury", 1),
			(val_min, ":treasury", ":gold_cost"),
			(troop_remove_gold, "trp_player", ":treasury"),
			(val_sub, ":gold_cost", ":treasury"),
		(try_end),
		#Fall through to the next section if the treasury didn't cover it.
		(lt, ":gold_cost", 1),
	(else_try),
		#Remove the gold directly from the lord's wealth slot
		(ge, ":gold_cost", 1),
		(ge, ":lord_no", 1),#not the player
		(troop_get_slot, ":treasure", ":lord_no", slot_troop_wealth),
		(ge, ":treasure", 1),
		(try_begin),
			(ge, ":treasure", ":gold_cost"),
			(val_sub, ":treasure", ":gold_cost"),
			(assign, ":gold_cost", 0),
		(else_try),
			(val_sub, ":gold_cost", ":treasure"),
			(assign, ":treasure", 0),
		(try_end),
		(troop_set_slot, ":lord_no", slot_troop_wealth, ":treasure"),
		#Fall through to the next section if his personal wealth didn't cover it.
		(lt, ":gold_cost", 1),
	(else_try),
		#Remove remaining gold from uncollected taxes.
		#We iterate backwards in order to remove from villages before castles and towns.
		(ge, ":gold_cost", 1),
		(try_for_range_backwards, ":center_no", centers_begin, centers_end),
			(ge, ":gold_cost", 1),
			(party_slot_eq, ":center_no", slot_town_lord, ":lord_no"),
			(party_get_slot, ":treasure", ":center_no", slot_center_accumulated_rents),
			(try_begin),
               	(gt, ":treasure", 0),
				(ge, ":treasure", ":gold_cost"),
				(val_sub, ":treasure", ":gold_cost"),
				(assign, ":gold_cost", 0),
			(else_try),
               	(gt, ":treasure", 0),
				(val_sub, ":gold_cost", ":treasure"),
				(assign, ":treasure", 0),
			(try_end),
				(party_set_slot, ":center_no", slot_center_accumulated_rents, ":treasure"),

			(ge, ":gold_cost", 1),
			(party_get_slot, ":treasure", ":center_no", slot_center_accumulated_tariffs),
			(try_begin),
               	(gt, ":treasure", 0),
				(ge, ":treasure", ":gold_cost"),
				(val_sub, ":treasure", ":gold_cost"),
				(assign, ":gold_cost", 0),
			(else_try),
               	(gt, ":treasure", 0),
				(val_sub, ":gold_cost", ":treasure"),
				(assign, ":treasure", 0),
			(try_end),
			(party_set_slot, ":center_no", slot_center_accumulated_tariffs, ":treasure"),
		(try_end),
		#Fall through to the next section if the uncollected taxes didn't cover it.
		(lt, ":gold_cost", 1),
	(else_try),
		#Remove remaining gold from center wealth.  We iterate backwards to remove from
		#castles before towns.
		(ge, ":gold_cost", 1),
		(try_for_range_backwards, ":center_no", centers_begin, centers_end),
			(ge, ":gold_cost", 1),
			(party_slot_eq, ":center_no", slot_town_lord, ":lord_no"),
			(party_get_slot, ":treasure", ":center_no", slot_town_wealth),
		(ge, ":treasure", 1),
		(try_begin),
			(ge, ":treasure", ":gold_cost"),
			(val_sub, ":treasure", ":gold_cost"),
			(assign, ":gold_cost", 0),
		(else_try),
			(val_sub, ":gold_cost", ":treasure"),
			(assign, ":treasure", 0),
		(try_end),
			(party_set_slot, ":center_no", slot_town_wealth, ":treasure"),
		(try_end),
		(lt, ":gold_cost", 1),
	(else_try),
	    #Try to remove the gold from the hero himself
		(store_troop_gold, ":treasure", ":lord_no"),
		(gt, ":treasure", 0),
		(try_begin),
			(ge, ":treasure", ":gold_cost"),
			(troop_remove_gold, ":lord_no", ":gold_cost"),
			(assign, ":gold_cost", 0),
		(else_try),
			(troop_remove_gold, ":treasure"),
			(val_sub, ":gold_cost", ":treasure"),
		(try_end),
	(try_end),

   ])
]
