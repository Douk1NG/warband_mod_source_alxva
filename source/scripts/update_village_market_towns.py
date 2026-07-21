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

update_village_market_towns_scripts = [
#script_player_join_faction
##  # INPUT: arg1 = center_no
##  # OUTPUT: reg0 = mercenary_troop_type, reg1 = amount
##  ("get_available_mercenary_troop_and_amount_of_center",
##    [(store_script_param, ":center_no", 1),
##     (party_get_slot, ":mercenary_troop", ":center_no", slot_center_mercenary_troop_type),
##     (party_get_slot, ":mercenary_amount", ":center_no", slot_center_mercenary_troop_amount),
##     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
##     (val_min, ":mercenary_amount", ":free_capacity"),
##     (store_troop_gold, ":cur_gold", "trp_player"),
##     (call_script, "script_game_get_join_cost", ":mercenary_troop"),
##     (assign, ":join_cost", reg0),
##     (try_begin),
##       (gt, ":join_cost", 0),
##       (val_div, ":cur_gold", ":join_cost"),
##       (val_min, ":mercenary_amount", ":cur_gold"),
##     (try_end),
##     (assign, reg0, ":mercenary_troop"),
##     (assign, reg1, ":mercenary_amount"),
##     ]),
##
#script_update_village_market_towns
# INPUT: none
# OUTPUT: none
("update_village_market_towns",
    [(try_for_range, ":cur_village", villages_begin, villages_end),
       (store_faction_of_party, ":village_faction", ":cur_village"),
       (assign, ":min_dist", 999999),
       (assign, ":min_dist_town", -1),
       (try_for_range, ":cur_town", towns_begin, towns_end),
         (store_faction_of_party, ":town_faction", ":cur_town"),
         (eq, ":town_faction", ":village_faction"),
         (store_distance_to_party_from_party, ":cur_dist", ":cur_village", ":cur_town"),
         (lt, ":cur_dist", ":min_dist"),
         (assign, ":min_dist", ":cur_dist"),
         (assign, ":min_dist_town", ":cur_town"),
       (try_end),

	   (try_begin),
		(gt, ":min_dist_town", -1),
		(party_set_slot, ":cur_village", slot_village_market_town, ":min_dist_town"),
	   (else_try),
		(assign, ":min_dist", 999999),
		(assign, ":min_dist_town", -1),
		(try_for_range, ":cur_town", towns_begin, towns_end),
			(store_faction_of_party, ":town_faction", ":cur_town"),
			(store_relation, ":relation", ":town_faction", ":village_faction"),
			(ge, ":relation", 0),
			(store_distance_to_party_from_party, ":cur_dist", ":cur_village", ":cur_town"),
			(lt, ":cur_dist", ":min_dist"),
			(assign, ":min_dist", ":cur_dist"),
			(assign, ":min_dist_town", ":cur_town"),
		(try_end),
		(gt, ":min_dist_town", -1),
		(party_set_slot, ":cur_village", slot_village_market_town, ":min_dist_town"),
	   (try_end),
     (try_end),
     ])
]
