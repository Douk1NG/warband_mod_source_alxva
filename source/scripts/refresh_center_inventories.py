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

refresh_center_inventories_scripts = [
# script_check_concilio_calradi_achievement
("refresh_center_inventories",
  [
  (set_merchandise_modifier_quality,150),
  (reset_item_probabilities,100),

  # Add trade goods to merchant inventories
  (try_for_range,":cur_center",towns_begin,towns_end),
    (party_get_slot,":cur_merchant",":cur_center",slot_town_merchant),
    (reset_item_probabilities,100),
      (assign, ":total_production", 0),
    (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
        (call_script, "script_center_get_production", ":cur_center", ":cur_goods"),
		(assign, ":cur_production", reg0),

        (try_for_range, ":cur_village", villages_begin, villages_end),
		  (party_slot_eq, ":cur_village", slot_village_bound_center, ":cur_center"),
          (call_script, "script_center_get_production", ":cur_village", ":cur_goods"),
		  (val_div, reg0, 3),
		  (val_add, ":cur_production", reg0),
		(try_end),

		(val_max, ":cur_production", 1),
		(val_mul, ":cur_production", 4),

		(val_add, ":total_production", ":cur_production"),
      (try_end),

	  (party_get_slot, ":town_prosperity", ":cur_center", slot_town_prosperity),
	  (assign, ":number_of_items_in_town", 25),

	  (try_begin), #1.0x - 2.0x (50 - 100 prosperity)
	    (ge, ":town_prosperity", 50),
		(store_sub, ":ratio", ":town_prosperity", 50),
		(val_mul, ":ratio", 2),
		(val_add, ":ratio", 100),
		(val_mul, ":number_of_items_in_town", ":ratio"),
		(val_div, ":number_of_items_in_town", 100),
	  (else_try), #0.5x - 1.0x (0 - 50 prosperity)
		(store_sub, ":ratio", ":town_prosperity", 50),
		(val_add, ":ratio", 100),
		(val_mul, ":number_of_items_in_town", ":ratio"),
		(val_div, ":number_of_items_in_town", 100),
	  (try_end),

	  (val_clamp, ":number_of_items_in_town", 10, 40),

	  (try_begin),
	    (is_between, ":cur_center", castles_begin, castles_end),
	    (val_div, ":number_of_items_in_town", 2),
      (try_end),

      (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
	  (call_script, "script_center_get_production", ":cur_center", ":cur_goods"),
		(assign, ":cur_production", reg0),

        (try_for_range, ":cur_village", villages_begin, villages_end),
		  (party_slot_eq, ":cur_village", slot_village_bound_center, ":cur_center"),
          (call_script, "script_center_get_production", ":cur_village", ":cur_goods"),
		  (val_div, reg0, 3),
		  (val_add, ":cur_production", reg0),
		(try_end),

		(val_max, ":cur_production", 1),
		(val_mul, ":cur_production", 4),

        (val_mul, ":cur_production", ":number_of_items_in_town"),
		(val_mul, ":cur_production", 100),
		(val_div, ":cur_production", ":total_production"),
        (set_item_probability_in_merchandise, ":cur_goods", ":cur_production"),
    (try_end),

	  (troop_clear_inventory, ":cur_merchant"),
      (troop_add_merchandise, ":cur_merchant", itp_type_goods, ":number_of_items_in_town"),

      (troop_ensure_inventory_space, ":cur_merchant", 20),
    (troop_sort_inventory, ":cur_merchant"),
    (store_troop_gold, ":cur_gold",":cur_merchant"),
    ##diplomacy start+
	#Option: scaling gold additions by the prosperity of the town.
	(try_begin),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#this must be explicitly enabled
	    (party_get_slot, ":prosperity_75", ":cur_center", slot_town_prosperity),
		(val_add, ":prosperity_75", 75),
		(store_mul, ":target_gold", ":prosperity_75", 1500),
		(val_add, ":target_gold", 62),
		(val_div, ":target_gold", 125),#average 1500
		(lt, ":cur_gold", ":target_gold"),
		(store_random_in_range,":new_gold",500,1000),
		(val_mul, ":new_gold", ":prosperity_75"),
		(val_add, ":new_gold", 62),
		(val_div, ":new_gold", 125),
		(call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
	(else_try),
		(lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
	    #fall through to default behavior
	    ##diplomacy end+
    (lt,":cur_gold",1500),
    (store_random_in_range,":new_gold",500,1000),
    (call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
    ##diplomacy start+
    (try_end),
	##diplomacy end+
  (try_end),
  ])
]
