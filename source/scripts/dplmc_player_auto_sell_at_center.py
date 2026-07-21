# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_player_auto_sell_at_center (script)
# Called by menus in 2 domains: diplomacy, town
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

dplmc_player_auto_sell_at_center_scripts = [
#auto sell credit rubik (CC) end
##For use with autosell
#Input: center_no
#Output: none
("dplmc_player_auto_sell_at_center", [
     (store_script_param, ":center_no", 1),
	 (assign, ":save_reg0", reg0),
	 (assign, ":save_reg1", reg1),
	 (try_begin),
	    ##For Towns:
		(is_between, ":center_no", towns_begin, towns_end),
		(try_begin),
			#1. Selling weapons, shields, and ranged weapons to the weaponsmith
		    (party_get_slot, ":merchant_troop", ":center_no", slot_town_weaponsmith),
			(ge, ":merchant_troop", 1),
			(call_script, "script_dplmc_auto_sell", "trp_player", ":merchant_troop", "$g_dplmc_auto_sell_price_limit", weapons_begin, ranged_weapons_end, 4),
		(try_end),
		(try_begin),
			#2. Selling armor to the armorer
			(party_get_slot, ":merchant_troop", ":center_no", slot_town_armorer),
			(ge, ":merchant_troop", 1),
			(call_script, "script_dplmc_auto_sell", "trp_player", ":merchant_troop", "$g_dplmc_auto_sell_price_limit", armors_begin, armors_end, 4),
 		(try_end),
		(try_begin),
			#3. Selling horses to the horse merchant
			(party_get_slot, ":merchant_troop", ":center_no", slot_town_horse_merchant),
			(ge, ":merchant_troop", 1),
			(call_script, "script_dplmc_auto_sell", "trp_player", ":merchant_troop", "$g_dplmc_auto_sell_price_limit", horses_begin, horses_end, 4),
		(try_end),
		(try_begin),
			#4. Selling whatever may remain to the general merchant
			(party_get_slot, ":merchant_troop", ":center_no", slot_town_merchant),
			(ge, ":merchant_troop", 1),
			(call_script, "script_dplmc_auto_sell", "trp_player", ":merchant_troop", "$g_dplmc_auto_sell_price_limit", all_items_begin, all_items_end, 4),
		(try_end),
	 (else_try),
		##For Villages:
		(is_between, ":center_no", villages_begin, villages_end),
		(party_get_slot, ":merchant_troop", ":center_no", slot_town_elder),
		(ge, ":merchant_troop", 1),
		(call_script, "script_dplmc_auto_sell", "trp_player", ":merchant_troop", "$g_dplmc_auto_sell_price_limit", all_items_begin, all_items_end, 4),
	 (else_try),
        #Don't show an error for castles, since we wouldn't expect this to work there
        (neg|is_between, ":center_no", castles_begin, castles_end),
	    ##Error
		(assign, reg0, ":center_no"),
		(display_message, "@{!} ERROR FOR AUTOSELL for town ID {reg0}: Bad town or merchant was missing"),
	 (try_end),
	 (assign, reg0, ":save_reg0"),
	 (assign, reg1, ":save_reg1"),
  ])
]
