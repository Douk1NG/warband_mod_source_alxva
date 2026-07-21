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

calculate_troop_ai_scripts = [
# script_calculate_troop_ai
# Input: troop_no
# Output: none
#Now called directly from scripts
("calculate_troop_ai",
    [
      (store_script_param, ":troop_no", 1),

      (try_begin),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (gt, ":party_no", 0),
		(party_is_active, ":party_no"),
		##diplomacy start+
		#Testing notifications
		(party_get_slot, ":old_ai_state", ":party_no", slot_party_ai_state),
		#(party_get_slot, ":old_ai_object", ":party_no", slot_party_ai_object),
		##diplomacy end+
		(call_script, "script_npc_decision_checklist_party_ai", ":troop_no"), #This handles AI for both marshal and other parties
		(call_script, "script_party_set_ai_state", ":party_no", reg0, reg1),
		##diplomacy start+
		#Notify the player of changes to spouse and affiliates
		(party_get_slot, ":new_ai_state", ":party_no", slot_party_ai_state),
		(party_get_slot, ":new_ai_object", ":party_no", slot_party_ai_object),

		##(this_or_next|neq, ":old_ai_object", ":new_ai_object",
		(neq, ":old_ai_state", ":new_ai_state"),
		(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		#(assign, reg0, 0),
		#(try_begin),
		#	(this_or_next|troop_slot_eq, ":troop_no", slot_troop_spouse, "trp_player"),
		#	(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_no"),
		#	(assign, reg0, 1),
		##(else_try),
		##	(store_faction_of_troop, ":troop_faction", ":troop_no"),
		##	(is_between,
		##(else_try),
		#	(call_script, "script_dplmc_is_affiliated_family_member", ":troop_no"),
		#(try_end),
		(call_script, "script_dplmc_store_troop_is_eligible_for_affiliate_messages", ":troop_no"),
		(gt, reg0, 0),


		#Some of these have non-obvious secondary uses.
		#xxx TODO: Later, I should go and verify all of them.
		(str_store_troop_name, s0, ":troop_no"),

		(try_begin),
			(eq, ":new_ai_state", spai_besieging_center),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is laying siege to {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_patrolling_around_center),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is patrolling around {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_raiding_around_center),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is raiding around {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_engaging_army),
			(gt, ":new_ai_object", -1),
			(party_is_active, ":new_ai_object"),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is engaging {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_accompanying_army),
			(gt, ":new_ai_object", -1),
			(party_is_active, ":new_ai_object"),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is accompanying {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_screening_army),
			(gt, ":new_ai_object", -1),
			(party_is_active, ":new_ai_object"),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is screening the advance of {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_trading_with_town),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is trading with {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_retreating_to_center),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is retreating to {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_visiting_village),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is visiting {s1}."),
		(try_end),
		#Make it obvious that something went wrong if something tries to use the registers
		(str_store_string, s0, "str_ERROR_string"),
		(str_store_string, s1, "str_ERROR_string"),
		##diplomacy end+
      (try_end),
    ])
]
