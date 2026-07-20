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

dplmc_good_produced_at_center_or_its_villages_scripts = [
#script_dplmc_good_produced_at_center_or_its_villages
# For towns, also includes the villages that attach to it
#
# INPUT: arg1 = good_no
#        arg2 = center_no
# OUTPUT:
#        reg0 = 0 if no, 1 if yes
("dplmc_good_produced_at_center_or_its_villages",
  [
	(store_script_param, ":good_no", 1),
	(store_script_param, ":center_no", 2),

	(assign, ":has_good", 0),
	(assign, ":save_reg1", reg1),
	(assign, ":save_reg2", reg2),
	(store_current_hours, ":cur_hours"),
	(store_sub, ":recent_time", ":cur_hours", 3 * 24),


	(try_begin),
		(is_between, ":good_no", trade_goods_begin, trade_goods_end),
		(ge, ":center_no", 1),
		(this_or_next|is_between, ":center_no", centers_begin, centers_end),
			(party_is_active, ":center_no"),
		(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
		(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_castle),
		(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_village),
			(is_between, ":center_no", centers_begin, centers_end),
		(call_script, "script_center_get_production", ":center_no", ":good_no"),
		(try_begin),
			#Positive production
			(ge, reg0, 1),
			(assign, ":has_good", 1),
		(else_try),
			#Is a town or a castle, and one of its villages has positive prodution
			(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
				(party_slot_eq, ":center_no", slot_party_type, spt_castle),
			(try_for_range, ":cur_village", villages_begin, villages_end),
				(eq, ":has_good", 0),
				#is bound to center
				(this_or_next|party_slot_eq, ":cur_village", slot_village_market_town, ":center_no"),
					(party_slot_eq, ":cur_village", slot_village_bound_center, ":center_no"),#for castles
               (assign, reg0, 0),
               (try_begin),
                  #If a trading party from the village reached the town recently, its goods are
				  #available.
                  (party_slot_ge, ":cur_village", dplmc_slot_village_trade_last_arrived_to_market, ":recent_time"),
                  (assign, reg0, 1),
               (else_try),
                  #If the village is not looted and this center is not under siege, the
				  #goods from the village could be acquired if they were needed.
					   (neg|party_slot_eq, ":cur_village", slot_village_state, svs_looted),
					   (neg|party_slot_eq, ":cur_village", slot_village_state, svs_deserted),
                  (neg|party_slot_eq, ":center_no", slot_village_state, svs_under_siege),
                  (assign, reg0, 1),
               (try_end),
               (eq, reg0, 1),
				#If an eligible village has positive production, set "has_good" to true.
				(call_script, "script_center_get_production", ":cur_village", ":good_no"),
				(ge, reg0, 1),
				(assign, ":has_good", 1),
			(try_end),
		(try_end),
	(try_end),

	(assign, reg0, ":has_good"),
	(assign, reg1, ":save_reg1"),
	(assign, reg2, ":save_reg2"),
  ])
]
