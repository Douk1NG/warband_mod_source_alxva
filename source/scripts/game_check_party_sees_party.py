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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

game_check_party_sees_party_scripts = [
# Note to modders: Uncomment these if you'd like to use the following.
##  #script_game_check_party_sees_party
##  # This script is called from the game engine when a party is inside the range of another party
##  # INPUT: arg1 = party_no_seer, arg2 = party_no_seen
##  # OUTPUT: trigger_result = true or false (1 = true, 0 = false)
##  ("game_check_party_sees_party",
##   [
##     (store_script_param, ":party_no_seer", 1),
##     (store_script_param, ":party_no_seen", 2),
##     (set_trigger_result, 1),
##    ]),
##
##diplomacy start+
#Enable script_game_check_party_sees_party to prevent compassionate lords from
#attacking villagers and merchant caravans.
#script_game_check_party_sees_party
# This script is called from the game engine when a party is inside the range of another party
# INPUT: arg1 = party_no_seer, arg2 = party_no_seen
# OUTPUT: trigger_result = true or false (1 = true, 0 = false)
("game_check_party_sees_party",
	[
	(store_script_param_1, ":party_no_seer"),
	(store_script_param_2, ":party_no_seen"),

	(assign, ":trigger_result", 1),
	(assign, ":save_reg0", reg0),

	#Lords who dislike raiding caravans should not attack village_farmer or kingdom_caravan
	#parties.  Achieve this by stopping them from seeing them.
	(try_begin),
		(gt, ":party_no_seer", spawn_points_end),
		(gt, ":party_no_seen", spawn_points_end),

		#Only apply this when the "seer" is a kingdom hero party
		(party_slot_eq, ":party_no_seer", slot_party_type, spt_kingdom_hero_party),

		#Only needed if the seen party is of a hostile faction
		(call_script, "script_get_relation_between_parties", ":party_no_seer", ":party_no_seen"),
		(lt, reg0, 0),

		#Only apply this when the seen party is a merchant caravan or villagers
		(party_get_template_id, ":template", ":party_no_seen"),
		(this_or_next|party_slot_eq, ":party_no_seen", slot_party_type, spt_kingdom_caravan),
		(this_or_next|party_slot_eq,":party_no_seen", slot_party_type, dplmc_spt_gift_caravan),#custom diplomacy caravan
		(this_or_next|eq,":template", "pt_refugees"),
			(party_slot_eq, ":party_no_seen", slot_party_type, spt_village_farmer),

		#Never apply this when the seen party is engaging in hostile actions
		(party_get_battle_opponent, reg0, ":party_no_seen"),
		(lt, reg0, 0),
		(neg|party_slot_eq, ":party_no_seen", slot_party_ai_state, spai_besieging_center),
		(neg|party_slot_eq, ":party_no_seen", slot_party_ai_state, spai_raiding_around_center),
		(neg|party_slot_eq, ":party_no_seen", slot_party_ai_state, spai_engaging_army),
		(neg|party_slot_eq, ":party_no_seen", slot_party_ai_state, spai_accompanying_army),
		(neg|party_slot_eq, ":party_no_seen", slot_party_ai_state, spai_screening_army),


		#Only apply this when the leader is tmt_humanitarian, lrep_benefactor, or lrep_moralist
		(party_get_num_companion_stacks, ":num_stacks", ":party_no_seer"),
		(ge, ":num_stacks", 1),
		(party_stack_get_troop_id, ":leader", ":party_no_seer", 0),
		(ge, ":leader", 1),
		(troop_is_hero, ":leader"),
		(call_script, "script_dplmc_get_troop_morality_value", ":leader", tmt_humanitarian),
		(ge, reg0, 0),# (never apply for leaders who like raiding caravans and attacking villagers)
		(this_or_next|ge, reg0, 1),
		(this_or_next|troop_slot_eq, ":leader", slot_lord_reputation_type, lrep_benefactor),
			(troop_slot_eq, ":leader", slot_lord_reputation_type, lrep_moralist),
		(assign, ":trigger_result", 0),
	(try_end),

	(assign, reg0, ":save_reg0"),
	(set_trigger_result, ":trigger_result"),
	])
]
