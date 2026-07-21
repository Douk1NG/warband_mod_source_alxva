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

faction_conclude_feast_scripts = [
#it might be easier to monitor whether prices are following an intuitive pattern if we separate production from consumption
("faction_conclude_feast",
	[
	(store_script_param, ":faction_no", 1),
	(store_script_param, ":venue", 2),

	(str_store_faction_name, s3, ":faction_no"),
	(str_store_party_name, s4, ":venue"),

    (try_begin),
        (eq, "$cheat_mode", 1),
	    (display_message, "str_s3_feast_concludes_at_s4"),
    (try_end),

	(try_begin),
		(eq, ":faction_no", "fac_player_faction"),
		(assign, ":faction_no", "$players_kingdom"),
	(try_end),

	(party_set_slot, ":venue", slot_town_has_tournament, 0),

	#markspot

	(assign, ":nobility_in_faction", 0),
	(assign, ":nobility_in_attendance", 0),

	(try_for_range, ":troop_no", active_npcs_begin, kingdom_ladies_end),
		(store_faction_of_troop, ":troop_faction", ":troop_no"),
		(eq, ":faction_no", ":troop_faction"),

		(val_add, ":nobility_in_faction", 1),

		#CHECK -- is the troop there?
		(troop_slot_eq, ":troop_no", slot_troop_cur_center, ":venue"),
		(val_add, ":nobility_in_attendance", 1),

		#check for marriages
		##diplomacy start+ enable marriages for non-kingdom ladies (for example, between two companions)
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_robber_knight),
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_seneschal),
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_player_companion),
		##diplomacy end+
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
		(troop_get_slot, ":groom", ":troop_no", slot_troop_betrothed),
		(gt, ":groom", 0),

		(troop_get_slot, ":groom_party", ":groom", slot_troop_leaded_party),
		(party_is_active, ":groom_party"),
		(party_get_attached_to, ":groom_party_attached", ":groom_party"),
		(eq, ":groom_party_attached", ":venue"),

		(store_faction_of_troop, ":lady_faction", ":troop_no"),
		(store_faction_of_troop, ":groom_faction", ":groom"),

		(eq, ":groom_faction", ":lady_faction"),
		(eq, ":lady_faction", ":faction_no"),
		(store_current_hours, ":hours_since_betrothal"),
		(troop_get_slot, ":betrothal_time", ":troop_no", slot_troop_betrothal_time),
		(val_sub, ":hours_since_betrothal", ":betrothal_time"),
		(ge, ":hours_since_betrothal", 144), #6 days, should perhaps eventually be 29 days, or 696 yours

		(call_script, "script_get_kingdom_lady_social_determinants", ":troop_no"),
		(assign, ":wedding_venue", reg1),
        ##diplomacy start+ be less picky about where to hold the feast as time goes on
		#(eq, ":venue", ":wedding_venue"),
		(neq, ":troop_no", "trp_player"),
		(neq, ":groom", "trp_player"),
		(party_get_slot, ":town_lord", ":venue", slot_town_lord),
		(assign, ":hold_the_wedding", 0),
		(try_begin),
			#after 6 days, will be held if the venue is the ideal one
			(eq, ":venue", ":wedding_venue"),
			(assign, ":hold_the_wedding", 1),
		(else_try),
			#after 6 days, will be held if the bride's father/guardian holds a feast
			(ge, ":town_lord", 0),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_father, ":town_lord"),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_mother, ":town_lord"),
			   (troop_slot_eq, ":troop_no", slot_troop_guardian, ":town_lord"),
			(assign, ":hold_the_wedding", 1),
		(else_try),
			#after 20 days, will be held if the bride, the groom, or either of their
			#parents hold a feast
			(ge, ":hours_since_betrothal", 24 * 20),
			(ge, ":town_lord", 0),
			(this_or_next|eq, ":troop_no", ":town_lord"),
			(this_or_next|eq, ":groom", ":town_lord"),
			(this_or_next|troop_slot_eq, ":groom", slot_troop_father, ":town_lord"),
			   (troop_slot_eq, ":groom", slot_troop_mother, ":town_lord"),
			(assign, ":hold_the_wedding", 1),
		(else_try),
			#after 60 days, if against all odds the engagement hasn't been called off,
			#the faction leader qualifies, as does any relative
			(ge, ":hours_since_betrothal", 24 * 60),
			(ge, ":town_lord", 0),
			#(call_script, "script_troop_get_family_relation_to_troop", ":town_lord", ":troop_no"),
			(call_script, "script_dplmc_troop_get_family_relation_to_troop",  ":town_lord", ":troop_no"),
			(assign, ":bride_relation", reg0),
			#(call_script, "script_troop_get_family_relation_to_troop", ":town_lord", ":groom"),
			(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":town_lord", ":groom"),
			(this_or_next|faction_slot_eq, ":troop_faction", slot_faction_leader, ":town_lord"),
			(this_or_next|ge, reg0, 1),
				(ge, ":bride_relation", 1),
			(assign, ":hold_the_wedding", 1),
		(try_end),
		(eq, ":hold_the_wedding", 1),
		##diplomacy end+
		(call_script, "script_courtship_event_bride_marry_groom", ":troop_no", ":groom", 0), #parameters from dialog
	(try_end),


#ssss	(assign, ":placeholder_reminder_to_calculate_effect_for_player_feast", 1),



	(party_get_slot, ":feast_host", ":venue", slot_town_lord),
	(assign, ":quality_of_feast", 0),

	(try_begin),
		(check_quest_active, "qst_organize_feast"),
		(quest_slot_eq, "qst_organize_feast", slot_quest_target_center, ":venue"),
		(assign, ":feast_host", "trp_player"),

		(assign, ":total_guests", 400),

		(call_script, "script_succeed_quest", "qst_organize_feast"),
		(call_script, "script_end_quest", "qst_organize_feast"),

		(call_script, "script_internal_politics_rate_feast_to_s9", "trp_household_possessions", ":total_guests", "$players_kingdom", 1),
		(assign, ":quality_of_feast", reg0),
	(else_try),
		(assign, ":quality_of_feast", 60),
	(try_end),


	(try_begin),
		(ge, "$cheat_mode", 1),
		(str_store_troop_name, s4, ":feast_host"),
		(assign, reg4, ":quality_of_feast"),
		(display_message, "@{!}DEBUG - {s4}'s feast has rating of {reg4}"),
	(try_end),


	(try_begin),
	  (ge, ":feast_host", 0),
	  (store_div, ":renown_boost", ":quality_of_feast", 3),
	  (call_script, "script_change_troop_renown", ":feast_host", ":renown_boost"),

	  (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(troop_get_slot, ":leaded_party", ":troop_no", slot_troop_leaded_party),
		(party_is_active, ":leaded_party"),
		(party_get_attached_to, ":leaded_party_attached", ":leaded_party"),
		(eq, ":leaded_party_attached", ":venue"),

		(assign, ":relation_booster", ":quality_of_feast"),
		(val_div, ":relation_booster", 20),

		(try_begin),
			(eq, ":feast_host", "trp_player"),
			(val_sub, ":relation_booster", 1),
			(val_max, ":relation_booster", 0),
		(try_end),
		(call_script, "script_troop_change_relation_with_troop", ":feast_host", ":troop_no", ":relation_booster"),
		(val_add, "$total_feast_changes", ":relation_booster"),
	  (try_end),
	(try_end),


	(assign, reg3, ":nobility_in_attendance"),
	(assign, reg4, ":nobility_in_faction"),

	(try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "str_attendance_reg3_nobles_out_of_reg4"),
	(try_end),
	])
]
