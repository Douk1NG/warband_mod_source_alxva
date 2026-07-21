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

dplmc_center_point_calc_scripts = [
# script_script_dplmc_faction_leader_splits_gold
# INPUT: arg1 = faction_id
#        arg2 = troop_1
#        arg2 = troop_2
#        arg3 = town_point_value (see explanation below)
#
# OUTPUT:
#        reg0 = total renown / total faction points (or 0 if no centers held)
#        reg1 = troop_1 total (not divided)
#        reg2 = troop_2 total (not divided)
#        reg3 = faction average lord renown (or 0 if no lords)
#
#In various places the game tallies center points differently.  The values of
#villages/castles/fiefs, respectively, in some places are 1/2/2, in other
#places are 1/2/3, and in others are 1/3/4.
#Specifying the town point value determines which scheme will be used to
#determine ceter points:
#        arg3 = 2 gives 1/2/2
#        arg3 = 3 gives 1/2/3
#        arg3 = 4 gives 1/2/4
#
#If the specified town_point_value is not 2,3, or 4, the script is allowed to
#clamp the value or substitute a default.
("dplmc_center_point_calc",
    [
		(store_script_param, ":faction_id", 1),
		(store_script_param, ":troop_1", 2),
		(store_script_param, ":troop_2", 3),
		(store_script_param, ":town_point_value", 4),

		(val_clamp, ":town_point_value", 2, 5),

		#The outputs
		(assign, ":faction_score", 0),
		(assign, ":troop_1_score", 0),
		(assign, ":troop_2_score", 0),
		#(assign, ":average_renown", 0),

		#Intermediate values we use for computing outputs
		(assign, ":total_renown", 0),
		(assign, ":num_lords", 0),

		#Handle the player first
		#(assign, ":player_in_faction", 0),
		(assign, ":faction_alias", ":faction_id"),
		(try_begin),
			(this_or_next|eq, ":faction_id", "$players_kingdom"),
				(eq, ":faction_id", "fac_player_supporters_faction"),
			(val_add, ":num_lords", 1),
			(troop_get_slot, ":total_renown", "trp_player", slot_troop_renown),
			#(assign, ":player_in_faction", 1),
			(assign, ":faction_alias", "fac_player_supporters_faction"),
			(eq, ":faction_id", "fac_player_supporters_faction"),
			(assign, ":faction_alias", "$players_kingdom"),
		(try_end),

		#Get lords in faction
		(try_for_range, ":troop_no", heroes_begin, heroes_end),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(neq, ":troop_no", "trp_kingdom_heroes_including_player_begin"),
			(store_troop_faction, ":faction_no", ":troop_no"),
			(this_or_next|eq, ":faction_no", ":faction_id"),
				(eq, ":faction_no", ":faction_alias"),

			(val_add, ":num_lords", 1),
			(troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
			(val_max, ":renown", 0),
			(val_add, ":total_renown", ":renown"),
		(try_end),

		#Get stats for centers
		(try_for_parties, ":center_no"),
			(assign, ":points", 0),
			(try_begin),
				#Towns are 2, 3, or 4 points
				(this_or_next|is_between, ":center_no", towns_begin, towns_end),
				(party_slot_eq, ":center_no", slot_party_type, spt_town),
				(assign, ":points", ":town_point_value"),
			(else_try),
				#Castles are always 2 points
				(this_or_next|is_between, ":center_no", castles_begin, castles_end),
				(party_slot_eq, ":center_no", slot_party_type, spt_castle),
				(assign, ":points", 2),#castles are always 2
			(else_try),
				#Villages are always 1 point
				(this_or_next|is_between, ":center_no", villages_begin, villages_end),
				(party_slot_eq, ":center_no", slot_party_type, spt_village),
			(try_end),

			#Don't process parties that aren't centers.
			(ge, ":points", 1),

			#NB: We don't know for sure that troop_1 and troop_2 aren't the
			#same value, and we don't even necessarily know that they're part
			#of the specified faction.
			(try_begin),
				(party_slot_eq, ":center_no", slot_town_lord, ":troop_1"),
				(val_add, ":troop_1_score", ":points"),
			(try_end),

			(try_begin),
				(party_slot_eq, ":center_no", slot_town_lord, ":troop_2"),
				(val_add, ":troop_2_score", ":points"),
			(try_end),

			(store_faction_of_party, ":faction_no", ":center_no"),
			(this_or_next|eq, ":faction_no", ":faction_id"),
				(eq, ":faction_no", ":faction_alias"),
			(val_add, ":faction_score", ":points"),
		(try_end),

		# OUTPUT:
		#        reg0 = faction renown / faction points (or 0 if faction has no centers)
		#        reg1 = troop_1 total (not divided)
		#        reg2 = troop_2 total (not divided)
		#        reg3 = faction average lord renown (or 0 if no lords)
		(assign, reg0, 0),
		(try_begin),
			(neq, ":faction_score", 0),
			(store_div, reg0, ":total_renown", ":faction_score"),
		(try_end),
		(assign, reg1, ":troop_1_score"),
		(assign, reg2, ":troop_2_score"),
		(assign, reg3, 0),
		(try_begin),
			(neq, ":num_lords", 0),
			(store_div, reg0, ":total_renown", ":num_lords"),
		(try_end),
	])
]
