# ======================================================================
# SHARED DEPENDENCY
# Entity: get_kingdom_lady_social_determinants (script)
# Called by menus in 3 domains: court, notifications, town
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

get_kingdom_lady_social_determinants_scripts = [
("get_kingdom_lady_social_determinants", #Calradian society is rather patriarchal, at least among the upper classes
    [
	(store_script_param, ":kingdom_lady", 1),

	(store_faction_of_troop, ":faction_of_lady", ":kingdom_lady"),
	(assign, ":center", -1),
	(assign, ":closest_male_relative", -1),
	(assign, ":best_center_score", 0),

	##diplomacy start+
	##TODO: Re-implement, disabled for now.  "Don't get stuck attached to a MIA relative"
	(try_begin),
		(troop_slot_ge, ":kingdom_lady", slot_troop_spouse, 0),
		(troop_get_slot, ":closest_male_relative", ":kingdom_lady", slot_troop_spouse),
		#(neg|troop_slot_ge, ":closest_male_relative", slot_troop_occupation, slto_retirement),#added: has not been removed from play
	(else_try),
		(troop_slot_ge, ":kingdom_lady", slot_troop_father, 0),
		(troop_get_slot, ":closest_male_relative", ":kingdom_lady", slot_troop_father),
		#(neg|troop_slot_ge, ":closest_male_relative", slot_troop_occupation, slto_retirement),#added: has not been removed from play
	(else_try),
		#added
		(troop_slot_ge, ":kingdom_lady", slot_troop_mother, 0),
		(troop_get_slot, ":closest_male_relative", ":kingdom_lady", slot_troop_mother),
		(troop_slot_eq, ":closest_male_relative", slot_troop_occupation, slto_kingdom_hero),
	(else_try),
		(troop_slot_ge, ":kingdom_lady", slot_troop_guardian, 0),
		(troop_get_slot, ":closest_male_relative", ":kingdom_lady", slot_troop_guardian),
		#(neg|troop_slot_ge, ":closest_male_relative", slot_troop_occupation, slto_retirement),#added: has not been removed from play
	(try_end),
	##diplomacy end+

	##diplomacy start+
    #Avoid strange problems if the argument is not a kingdom lady.
	(try_begin),
		(this_or_next|is_between, ":kingdom_lady", kingdom_ladies_begin, kingdom_ladies_end),
			(troop_slot_eq, ":kingdom_lady", slot_troop_occupation, slto_kingdom_lady),
		(neg|troop_slot_eq, ":kingdom_lady", slot_troop_occupation, slto_kingdom_hero),
		(assign, ":is_lady", 1),
	(else_try),
		(assign, ":is_lady", 0),
		(assign, ":closest_male_relative", ":kingdom_lady"),# is doing this useful for the way this script is used, or should we just set it to -1?
	(try_end),

	##OLD:
	#(try_begin), #if ongoing social event (maybe add if not besieged)
	##NEW:
	(try_begin),
		(eq, ":is_lady", 0),
		(call_script, "script_lord_get_home_center", ":kingdom_lady"),
		(assign, ":center", reg0),
		(is_between, ":center", walled_centers_begin, walled_centers_end),
	(else_try), #if ongoing social event (maybe add if not besieged)
	##diplomacy end+
		(faction_slot_eq, ":faction_of_lady", slot_faction_ai_state, sfai_feast),
		(faction_get_slot, ":feast_center", ":faction_of_lady", slot_faction_ai_object),

		(gt, ":closest_male_relative", -1),
		(troop_get_slot, ":closest_male_party", ":closest_male_relative", slot_troop_leaded_party),
		(party_is_active, ":closest_male_party"),
		(party_get_attached_to, ":closest_male_cur_location", ":closest_male_party"),

		(eq, ":closest_male_cur_location", ":feast_center"),
		(is_between, ":feast_center", walled_centers_begin, walled_centers_end),

		(assign, ":center", ":feast_center"),

	(else_try),
		(troop_slot_eq, "trp_player", slot_troop_spouse, ":kingdom_lady"),
		###diplomacy begin
    (try_begin),
    ##diplomacy end
		(is_between, "$g_player_court", walled_centers_begin, walled_centers_end),
		(assign, ":center", "$g_player_court"),
		##diplomacy begin
    (else_try),
      (troop_get_slot, ":cur_residence", ":kingdom_lady", slot_troop_cur_center),
      (is_between, ":cur_residence", walled_centers_begin, walled_centers_end),
      (party_slot_eq, ":cur_residence", slot_town_lord, "trp_player"),
      (assign, ":center", ":cur_residence"),
    (try_end),
    (is_between, ":center",  walled_centers_begin, walled_centers_end),
    ##diplomacy end
	(else_try),
		(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
			(store_faction_of_party, ":walled_center_faction", ":walled_center"),
			(this_or_next|eq, ":faction_of_lady", ":walled_center_faction"),
				(neg|is_between, ":faction_of_lady", kingdoms_begin, kingdoms_end), #lady married to a player without a faction

			(party_get_slot, ":castle_lord", ":walled_center", slot_town_lord),

			(gt, ":castle_lord", -1),

			(call_script, "script_troop_get_family_relation_to_troop", ":kingdom_lady", ":castle_lord"),
			##diplomacy start+
			(try_begin),
				(eq, ":is_lady", 0),
				(eq, ":castle_lord", ":kingdom_lady"),
				(val_max, reg0, 16),
			(try_end),
			##diplomacy end+

			(try_begin),
				(this_or_next|is_between, ":faction_of_lady", kingdoms_begin, kingdoms_end),
					(troop_slot_eq, "trp_player", slot_troop_spouse, ":kingdom_lady"),

				(faction_slot_eq, ":faction_of_lady", slot_faction_leader, ":castle_lord"),
				(val_max, reg0, 1),
			(try_end),

			(try_begin),
				(eq, "$cheat_mode", 2),
				(str_store_troop_name, s3, ":kingdom_lady"),
				(str_store_troop_name, s4, ":castle_lord"),
				(str_store_party_name, s5, ":walled_center"),
				(display_message, "str_checking_s3_at_s5_with_s11_relationship_with_s4_score_reg0"),
				(str_clear, s11),
			(try_end),

			(gt, reg0, ":best_center_score"),

			(assign, ":best_center_score", reg0),
			(assign, ":center", ":walled_center"),


	    (try_end),
	(try_end),

	(assign, reg0, ":closest_male_relative"),
	(assign, reg1, ":center"),


	])
]
