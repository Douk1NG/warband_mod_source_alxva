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

dplmc_prepare_hero_center_points_ignoring_center_scripts = [
#script_dplmc_print_centers_in_numbers_to_s0
#
# Input: arg1 = target_center
("dplmc_prepare_hero_center_points_ignoring_center",[
	  (store_script_param, ":target_center", 1),

	  (troop_set_slot, "trp_player", slot_troop_temp_slot, 0),
	  (troop_set_slot, "trp_player", dplmc_slot_troop_temp_slot, 0),

	  (try_for_range, ":troop_no", heroes_begin, heroes_end),
		(troop_set_slot, ":troop_no", slot_troop_temp_slot, 0),
		(troop_set_slot, ":troop_no", dplmc_slot_troop_temp_slot, 0),
	  (try_end),

	  (try_for_range, ":center_no", centers_begin, centers_end),
	    #Skip "target center"
		(neq, ":center_no", ":target_center"),

		#Lord is player or a hero
		(party_get_slot, ":troop_no", ":center_no", slot_town_lord),
		(this_or_next|eq, ":troop_no", "trp_player"),
			(is_between, ":troop_no", heroes_begin, heroes_end),

		#Update lord point total
		(assign, ":center_points", 1),
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_town),
			(assign, ":center_points", 3),
		(else_try),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
			(assign, ":center_points", 2),
		(try_end),

		(troop_get_slot, ":slot_value", ":troop_no", slot_troop_temp_slot),
		(val_add, ":slot_value", ":center_points"),
		(troop_set_slot, ":troop_no", slot_troop_temp_slot, ":slot_value"),

		#Update distance from closest owned center to target
		(is_between, ":target_center", centers_begin, centers_end),
		(troop_get_slot, ":slot_value", ":troop_no", dplmc_slot_troop_temp_slot),
		(store_distance_to_party_from_party, ":cur_distance", ":target_center", ":center_no"),
		(val_max, ":cur_distance", 1),
		(try_begin),
			(eq, ":slot_value", 0),
			(assign, ":slot_value", ":cur_distance"),
		(try_end),
		(val_min, ":slot_value", ":cur_distance"),
		(troop_set_slot, ":troop_no", dplmc_slot_troop_temp_slot, ":slot_value"),
	  (try_end),
	  ##Update cached totals
	  (try_for_range, ":troop_no", heroes_begin, heroes_end),
		(troop_get_slot, reg0, ":troop_no", slot_troop_temp_slot),
		(val_add, reg0, 1),
		(troop_set_slot, ":troop_no", dplmc_slot_troop_center_points_plus_one, reg0),
          (try_end),
          (troop_get_slot, reg0, "trp_player", slot_troop_temp_slot),
          (val_add, reg0, 1),
          (troop_set_slot, "trp_player", dplmc_slot_troop_center_points_plus_one, reg0),
          #Since the target center was omitted from the point totals, handle it here
	  (try_begin),
		(is_between, ":target_center", centers_begin, centers_end),
		(party_get_slot, ":troop_no", ":target_center", slot_town_lord),
		#Only perform this update for a troop whose center point value was updated above
		(this_or_next|is_between, ":troop_no", heroes_begin, heroes_end),
		(eq, ":troop_no", "trp_player"),
		(troop_get_slot, reg0, ":troop_no", dplmc_slot_troop_center_points_plus_one),
		(val_add, reg0, 1),#1 point for villages
		(try_begin),
		   (is_between, ":target_center", walled_centers_begin, walled_centers_end),
		   (val_add, reg0, 1),#2 points for castles
		   (is_between, ":target_center", towns_begin, towns_end),
		   (val_add, reg0, 1),#3 points for towns
		(try_end),
		(troop_set_slot, ":troop_no", dplmc_slot_troop_center_points_plus_one, reg0),
	  (try_end),
   ])
]
