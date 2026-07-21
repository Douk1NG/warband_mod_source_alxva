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

refresh_center_weaponsmiths_scripts = [
# script_refresh_center_weaponsmiths
("refresh_center_weaponsmiths",
  [
	  (reset_item_probabilities,100),
	  (set_merchandise_modifier_quality,150),
    (try_for_range, ":cur_merchant", weapon_merchants_begin, weapon_merchants_end),
	  (store_sub, ":cur_town", ":cur_merchant", weapon_merchants_begin),
	    (val_add, ":cur_town", towns_begin),
	  (troop_clear_inventory, ":cur_merchant"),
	    (party_get_slot, ":cur_faction", ":cur_town", slot_center_original_faction),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_one_handed_wpn, 5),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_two_handed_wpn, 5),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_polearm, 5),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_shield, 6),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_bow, 4),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_crossbow, 3),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_thrown, 5),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_arrows, 2),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_bolts, 2),
      #Guns and gun related items
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_pistol, 1),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_musket, 1),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_bullets, 1),
      (troop_ensure_inventory_space, ":cur_merchant", merchant_inventory_space),
      (troop_sort_inventory, ":cur_merchant"),
      (store_troop_gold, reg6, ":cur_merchant"),

	    ##diplomacy start+
		#Option: scaling gold additions by the prosperity of the town.
		(try_begin),
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#this must be explicitly enabled
		    (party_get_slot, ":prosperity_75", ":cur_town", slot_town_prosperity),
			(val_add, ":prosperity_75", 75),
			(store_mul, ":target_gold", ":prosperity_75", 900),
			(val_add, ":target_gold", 62),
			(val_div, ":target_gold", 125),#average 900
			(lt, reg6, ":target_gold"),
			(store_random_in_range,":new_gold",200,400),
			(val_mul, ":new_gold", ":prosperity_75"),
			(val_add, ":new_gold", 62),
			(val_div, ":new_gold", 125),
			(call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
		(else_try),
			(lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		    #fall through to default behavior
		    ##diplomacy end+
	    (lt,reg6,1000),
	    (store_random_in_range,":new_gold",250,500),
	  (call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
	  ##diplomacy start+
	  (try_end),
	  ##diplomacy end+
	  (try_end),
  ])
]
