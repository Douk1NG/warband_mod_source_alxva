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

cf_select_most_profitable_town_at_peace_with_faction_in_trade_route_scripts = [
#the following is a very simple adjustment - it measures the difference in prices between two towns
#all goods are weighted equally except for luxuries
#it does not take into account the prices of the goods, nor cargo capacity
#to do that properly, a merchant would have to virtually fill his baggage, slot by slot, for each town
#i also found that one needed to introduce demand inelasticity -- prices should vary a lot for grain,  relatively little for iron
##diplomacy start+
#
#Added a third parameter, the caravan party, for use in distance calculations and perhaps
#other things in the future.  This may be -1, in which case the script attempts to find a
#general answer without referring to any specific attributes.  It may also be a town,
#in which case its position is used for distance calculations.
##diplomacy end+
("cf_select_most_profitable_town_at_peace_with_faction_in_trade_route",
    [
      (store_script_param, ":town_no", 1),
      (store_script_param, ":faction_no", 2),
	  ##diplomacy start+
	  (store_script_param, ":perspective_party", 3),
	  ##diplomacy end+

      (assign, ":result", -1),
	  (assign, ":best_town_score", 0),
      (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),

	  ##diplomacy start+
	  # If economics changes are enabled, the caravan may also take into account the distance
	  # to the destination or bias towards towns of its town faction.
	  (store_random_in_range, ":consider_distance", 0, 2),
	  (store_random_in_range, ":faction_bias", 0, 2),
	  (try_begin),
		(lt, ":perspective_party", 0),
		(assign, ":perspective_party", ":town_no"),
	  (try_end),
      ##diplomacy end+

      (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
        (party_get_slot, ":cur_town", ":town_no", ":cur_slot"),
        (gt, ":cur_town", 0),

        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation, ":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),

		(assign, ":cur_town_score", 0),
		(try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
			(neq, ":cur_goods", "itm_butter"), #Don't count perishables
			(neq, ":cur_goods", "itm_cattle_meat"),
			(neq, ":cur_goods", "itm_chicken"),
			(neq, ":cur_goods", "itm_pork"),

            (store_add, ":cur_goods_price_slot", ":cur_goods", ":item_to_price_slot"),
			(party_get_slot, ":origin_price", ":town_no", ":cur_goods_price_slot"),
			(party_get_slot, ":destination_price", ":cur_town", ":cur_goods_price_slot"),

			(gt, ":destination_price", ":origin_price"),
			(store_sub, ":price_dif", ":destination_price", ":origin_price"),

			(try_begin), #weight luxury goods double
				(this_or_next|eq, ":cur_goods", "itm_spice"),
					(eq, ":cur_goods", "itm_velvet"),
				(val_mul, ":price_dif", 2),
			(try_end),
			(val_add, ":cur_town_score", ":price_dif"),
		(try_end),

##		(try_begin),
##			(eq, "$cheat_mode", 1),
##			(str_store_party_name, s10, ":town_no"),
##			(str_store_party_name, s11, ":cur_town"),
##			(assign, reg3, ":cur_town_score"),
##			(display_message, "str_caravan_in_s10_considers_s11_total_price_dif_=_reg3"),
##		(try_end),

        ##diplomacy start+
		(try_begin),
			#Economic changes must be enabled, or the player must have decided
			#to use mercantilism settings (which expresses a desire to see changes
			#related to that setting applied), or a trade treaty must be in effect.
			(this_or_next|neg|faction_slot_eq, "fac_player_supporters_faction", dplmc_slot_faction_mercantilism, 0),
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
			#Take into account distance, or treat factions preferentially
			(try_begin),
				#Bias towards own faction
				(ge, ":faction_bias", 1),
				(neq, ":faction_no", ":cur_faction"),

				##The penalty is based on the source faction's mercantilism rating, as well as
				##the other faction's mercantilism rating.
				(faction_get_slot, ":source_mercantilism", ":faction_no", dplmc_slot_faction_mercantilism),
				(val_clamp, ":source_mercantilism", -3, 4),
				(faction_get_slot, ":dest_mercantilism", ":cur_faction", dplmc_slot_faction_mercantilism),
				(val_clamp, ":dest_mercantilism", -3, 4),
				##Default (if both factions have mercantilism 0) is a 6% reduction.  Possible range is 0% (least) to 12% (most).
				(store_sub, ":percent", 94, ":source_mercantilism"),
				(val_sub, ":percent", ":dest_mercantilism"),

				(val_mul, ":cur_town_score", ":percent"),
				(val_add, ":cur_town_score", 50),
				(val_div, ":cur_town_score", 100),
			(try_end),
			(try_begin),
				(ge, ":consider_distance", 1),#consider distance
				(store_distance_to_party_from_party, ":dist", ":perspective_party",":cur_town"),
				#Avoid asymptotic effects and undue weighting.
				#Further explanation: What we really care about is time, not distance.
				#It will take time to buy and sell once reaching our destination: halving
				#the distance doesn't double the expected profit per month.
				(val_max, ":dist", 0),
				(val_add, ":dist", 12),
				#Avoid possible problems trying to compare distant towns
				(val_mul, ":cur_town_score", 100),
				(val_div, ":cur_town_score", ":dist"),
			(try_end),
		(try_end),
		##diplomacy end+

		(gt, ":cur_town_score", ":best_town_score"),
		(assign, ":best_town_score", ":cur_town_score"),
		(assign, ":result", ":cur_town"),

	  (try_end),

      (gt, ":result", -1), #Fail if there are no towns

      (assign, reg0, ":result"),

#	  (store_current_hours, ":hour"),
#	  (party_set_slot, ":result", slot_town_caravan_last_visit, ":hour"),

##	  (try_begin),
##		(eq, "$cheat_mode", 1),
##	    (assign, reg3, ":best_town_score"),
##	    (str_store_party_name, s3, ":town_no"),
##	    (str_store_party_name, s4, ":result"),
##	    (display_message, "str_test__caravan_in_s3_selects_for_s4_trade_score_reg3"),
##	  (try_end),

  ])
]
