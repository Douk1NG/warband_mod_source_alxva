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

dplmc_cap_troop_describes_troop_to_troop_s1_scripts = [
##"script_dplmc_cap_troop_describes_troop_to_troop_s1"
#
# e.g.
#
#(call_script, "script_dplmc_cap_troop_describes_troop_to_troop_s1", 1, "trp_player", ":third_lord", "$g_talk_troop"),
#
#INPUT:
#        arg1  :capitalization (0 if middle of sentence, 1 if sentence start)
#        arg2  :speaker (the one doing the talking)
#        arg3  :described (the one being named)
#        arg4  :listener (the one being spoken to)
#
#OUTPUT:
#        Writes result to s1, clobbers s0
#
#Similar to "script_troop_describes_troop_to_s15", except
#it takes into account the perspective of the one being
#spoken to, and writes to s1
("dplmc_cap_troop_describes_troop_to_troop_s1",
  [
	(store_script_param, ":capitalization", 1),
	(store_script_param, ":speaker", 2),
	(store_script_param, ":described", 3),
	(store_script_param, ":listener", 4),

	(assign, ":save_reg0", reg0),
	(assign, ":save_reg1", reg1),

	(str_store_troop_name, s0, ":described"),

	(assign, reg0, ":capitalization"),
	(try_begin),
		(eq, ":described", ":listener"),
		(neq, ":speaker", ":listener"),
		(str_store_string, s0, "@{reg0?Y:y}ou"),
		(assign, reg0, 1),
	(else_try),
		(eq, ":described", ":speaker"),
		(str_store_string, s0, "@{reg0?M:m}yself"),
		(assign, reg0, 1),
	(else_try),
		(this_or_next|eq, ":described", "trp_player"),#only calculate family relationships for the player and heroes
			(is_between, ":described", heroes_begin, heroes_end),
		(assign, ":speaker_relation", 0),
		(assign, ":speaker_relation_string", 0),
		(try_begin),
			(this_or_next|eq, ":speaker", "trp_player"),#only calculate family relationships for the player and heroes
				(is_between, ":speaker", heroes_begin, heroes_end),
			(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":described", ":speaker"),
			(assign, ":speaker_relation", reg0),
			(assign, ":speaker_relation_string", reg1),
		(try_end),
		(assign, reg0, 0),
		(try_begin),
			(this_or_next|eq, ":described", "trp_player"),#only calculate family relationships for the player and heroes
				(is_between, ":described", heroes_begin, heroes_end),
			(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":described", ":listener"),
		(try_end),
		(this_or_next|ge, ":speaker_relation", 1),
			(ge, reg0, 1),
		(try_begin),
			(eq, ":speaker_relation", reg0),
			(eq, reg1, ":speaker_relation_string"),
			(neq, ":speaker", ":listener"),
			(assign, reg0, ":capitalization"),
			(str_store_string, s1, ":speaker_relation_string"),
			(str_store_string, s1, "@{reg0?O:o}ur {s1} {s0}"),
		(else_try),
			(ge, ":speaker_relation", reg0),
			(assign, reg0, ":capitalization"),
			(str_store_string, s1, ":speaker_relation_string"),
			(str_store_string, s1, "@{reg0?M:m}y {s1} {s0}"),
		(else_try),
			(assign, reg0, ":capitalization"),
			(str_store_string, s1, reg1),
			(str_store_string, s1, "@{reg0?Y:y}our {s1} {s0}"),
		(try_end),
	###Disable "marshall/liege", because that's done elsewhere anyway
	#(else_try),
	#	(store_faction_of_troop, ":speaker_faction", ":speaker"),
	#	(try_begin),
	#		(eq, ":speaker", "trp_player"),
	#		(assign, ":speaker_faction", "$players_kingdom"),
	#	(try_end),
	#
	#	(store_faction_of_troop, ":listener_faction", ":listener"),
	#	(try_begin),
	#		(eq, ":listener", "trp_player"),
	#		(assign, ":listener_faction", "$players_kingdom"),
	#	(try_end),
	#
	#	(faction_slot_eq, ":speaker_faction", slot_faction_leader, ":described"),
	#	(this_or_next|is_between, ":speaker_faction", npc_kingdoms_begin, npc_kingdoms_end),
	#		(faction_slot_eq, ":speaker_faction", slot_faction_state, sfs_active),
	#	(this_or_next|neq, ":described", "trp_player"),
	#		(eq, ":speaker_faction", "$players_kingdom"),
	#	(assign, reg0, ":capitalization"),
	#	(try_begin),
	#		(eq, ":speaker_faction", ":listener_faction"),
	#		(neq, ":speaker", ":listener"),
	#		(str_store_string, s1, "@{reg0?O:o}ur liege {s0}"),
	#	(else_try),
	#		(str_store_string, s1, "@{reg0?M:m}y liege {s0}"),
	#	(try_end),
	#(else_try),
	#	(faction_slot_eq, ":speaker_faction", slot_faction_marshall, ":described"),
	#	(this_or_next|is_between, ":speaker_faction", npc_kingdoms_begin, npc_kingdoms_end),
	#		(faction_slot_eq, ":speaker_faction", slot_faction_state, sfs_active),
	#	(this_or_next|neq, ":described", "trp_player"),
	#		(eq, ":speaker_faction", "$players_kingdom"),
	#	(try_begin),
	#		(eq, ":speaker_faction", ":listener_faction"),
	#		(neq, ":speaker", ":listener"),
	#		(str_store_string, s1, "@{reg0?O:o}ur marshall {s0}"),
	#	(else_try),
	#		(str_store_string, s1, "@{reg0?M:m}y marshall {s0}"),
	#	(try_end),
	#(else_try),
	#	(this_or_next|is_between, ":listener_faction", npc_kingdoms_begin, npc_kingdoms_end),
	#		(faction_slot_eq, ":listener_faction", slot_faction_state, sfs_active),
	#	(faction_slot_eq, ":listener_faction", slot_faction_leader, ":described"),
	#	(this_or_next|neq, ":described", "trp_player"),
	#		(eq, ":listener_faction", "$players_kingdom"),
	#	(assign, reg0, ":capitalization"),
	#	(str_store_string, s1, "@{reg0?Y:y}our liege {s0}"),

	###Disable "friend", because it gets really spammy.  (It looks really stupid to have
	###a list of fifty names, all of them starting with "Your Friend So-and-So".)
	#(else_try),
	#	(call_script, "script_troop_get_relation_with_troop", ":described", ":listener"),
	#	(ge, reg0, 20),
	#	(this_or_next|neq, ":listener", "trp_player"),
	#		(ge, reg0, 50),
	#	(call_script, "script_troop_get_relation_with_troop", ":described", ":speaker"),
	#	(this_or_next|neq, ":listener", "trp_player"),
	#		(neq, ":speaker_trp_player"),
	#	(try_begin),
	#		(ge, reg0, 20),
	#		(this_or_next|neq, ":speaker", "trp_player"),
	#			(ge, reg0, 50),
	#		(assign, reg0, ":capitalization"),
	#		(str_store_string, s1, "@{reg0?O:o}ur friend {s0}"),
	#	(else_try),
	#		(assign, reg0, ":capitalization"),
	#		(str_store_string, s1, "@{reg0?Y:y}our friend {s0}"),
	#	(try_end),
	#(else_try),
	#	(call_script, "script_troop_get_relation_with_troop", ":described", ":speaker"),
	#	(ge, reg0, 20),
	#	(this_or_next|neq, ":speaker", "trp_player"),
	#		(ge, reg0, 50),
	#	(assign, reg0, ":capitalization"),
	#	(str_store_string, s1, "@{reg0?M:m}y friend {s0}"),

	###The "<Jarl Aedin> of <Tihr>" condition works fine, but I'm not particularly impressed.
	###I'm not sure it's an improvement over just using their name, so I'm disabling it for now.
	#(else_try),
	#	#Did not use relation string: name by owned town.
	#	#Do not use names of castles, due to potential absurdities like "Count Harringoth of Harringoth Castle".
	#	#Skip kings and pretenders because of "Lady Isolla of Suno of Suno" and similar things.
	#	(neg|is_between, ":described", kings_begin, kings_end),
	#	(neg|is_between, ":described", pretenders_begin, pretenders_end),
	#	(this_or_next|eq, ":described", "trp_player"),
	#		(is_between, ":described", heroes_begin, heroes_end),
	#
	#	(assign, ":owned_town", -1),
	#	(assign, ":owned_town_score", -1),
	#	(troop_get_slot, ":original_faction", ":described", slot_troop_original_faction),
	#	(try_for_range, ":town_no", towns_begin, towns_end),
	#		(party_get_slot, ":town_lord", ":town_no", slot_town_lord),
	#		(ge, ":town_lord", 0),
	#		(assign, reg0, 0),
	#		(try_begin),
	#			(eq, ":town_lord", ":described"),
	#			(assign, reg0, 10),
	#		(else_try),
	#			(this_or_next|troop_slot_eq, ":town_lord", slot_troop_spouse, ":described"),
	#				(troop_slot_eq, ":described", slot_troop_spouse, ":town_lord"),
	#			(this_or_next|is_between, ":described", kingdom_ladies_begin, kingdom_ladies_end),
	#				(troop_slot_eq, ":described", slot_troop_occupation, slto_kingdom_lady),
	#			(assign, reg0, 1),
	#		(else_try),
	#			(assign, reg0, 0),
	#		(try_end),
	#		(gt, reg0, 0),
	#		(try_begin),
	#			(party_slot_eq, ":town_no", slot_center_original_faction, ":original_faction"),
	#			(val_add, reg0, 1),
	#		(try_end),
	#		(try_begin),
	#			(this_or_next|party_slot_eq, ":town_no", dplmc_slot_center_original_lord, ":described"),
	#				(party_slot_eq, ":town_no", dplmc_slot_center_original_lord, ":town_lord"),
	#			(val_add, reg0, 2),
	#		(try_end),
	#		(try_begin),
	#			(this_or_next|troop_slot_eq, ":town_lord", slot_troop_home, ":town_no"),
	#				(troop_slot_eq, ":town_lord", slot_troop_home, ":town_no"),
	#			(val_add, reg0, 2),
	#		(try_end),
	#		(gt, reg0, ":owned_town_score"),
	#		(assign, ":owned_town_score", reg0),
	#		(assign, ":owned_town", ":town_no"),
	#	(try_end),
	#	(is_between, ":owned_town", towns_begin, towns_end),
	#	(str_store_party_name, s1, ":owned_town"),
	#	(str_store_string, s1, "@{s0} of {s1}"),
	(else_try),
		(str_store_string, s1, "str_s0"),
	(try_end),

	(assign, reg0, ":save_reg0"),
	(assign, reg1, ":save_reg1"),
	(str_store_string_reg, s0, s1),
	])
]
