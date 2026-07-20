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

refresh_village_merchant_inventory_scripts = [
# script_refresh_village_merchant_inventory
# Input: arg1 = village_no
# Output: none
("refresh_village_merchant_inventory",
    [
      (store_script_param_1, ":village_no"),
      (party_get_slot, ":merchant_troop", ":village_no", slot_town_elder),
      (reset_item_probabilities,0),

	  (party_get_slot, ":bound_center", ":village_no", slot_village_bound_center),

	  (assign, ":total_probability", 0),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
	    (call_script, "script_center_get_production", ":village_no", ":cur_good"),
		(assign, ":cur_probability", reg0),

        (call_script, "script_center_get_production", ":bound_center", ":cur_good"),
		(val_div, reg0, 5), #also add 1/5 of bound center production to village's inventory.
		(val_add, ":cur_probability", reg0),

		(val_max, ":cur_probability", 5),
		(val_add, ":total_probability", ":cur_probability"),
      (try_end),

	  (try_begin),
		(party_get_slot, ":prosperity", ":village_no", slot_town_prosperity),
		(val_div, ":prosperity", 15), #up to 6
		(store_add, ":number_of_items_in_village", ":prosperity", 1),
	  (try_end),

      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
	    (call_script, "script_center_get_production", ":village_no", ":cur_good"),
		(assign, ":cur_probability", reg0),

        (call_script, "script_center_get_production", ":bound_center", ":cur_good"),
		(val_div, reg0, 5), #also add 1/5 of bound center production to village's inventory.
		(val_add, ":cur_probability", reg0),

		(val_max, ":cur_probability", 5),
        (val_mul, ":cur_probability", ":number_of_items_in_village"),
		(val_mul, ":cur_probability", 100),
		(val_div, ":cur_probability", ":total_probability"),

        (set_item_probability_in_merchandise, ":cur_good", ":cur_probability"),
      (try_end),

      #SB : probably do something like trash item at base values
      (troop_clear_inventory, ":merchant_troop"),
      (troop_add_merchandise, ":merchant_troop", itp_type_goods, ":number_of_items_in_village"),
      (troop_ensure_inventory_space, ":merchant_troop", 80),

      #Adding 1 prosperity to the village while reducing each 3000 gold from the elder
      (store_troop_gold, ":gold",":merchant_troop"),
      (try_begin),
        (gt, ":gold", 3500),
        (store_div, ":prosperity_added", ":gold", 3000),
        (store_mul, ":gold_removed", ":prosperity_added", 3000),
        (troop_remove_gold, ":merchant_troop", ":gold_removed"),
        (call_script, "script_change_center_prosperity", ":village_no", ":prosperity_added"),
      (try_end),
  ])
]
