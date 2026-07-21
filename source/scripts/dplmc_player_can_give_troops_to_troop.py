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

dplmc_player_can_give_troops_to_troop_scripts = [
#script_dplmc_player_can_give_troops_to_troop  (Warning, clobbers {s11}!)
#
# INPUT: arg1 = troop_id
# OUTPUT: reg0 = 1 or more is yes, 0 or less is no
#
# This script does not take into account things like whether the troop
# is a prisoner of a party, so it can be used for checking whether troops
# can be added to a garrison.
#
# The general logic is that you can give troops to a member of your
# own faction if any of the following are true:
#   - You are the faction leader or marshall
#   - You are the spouse of the faction leader, and the faction
#     leader is not on bad terms with you
#   - The troop is an affiliated family member
#   - The troop is your spouse, and is either pliable or not on bad terms
#   - The troop is a former companion with whom you are on good terms
#   - The troop is related to you by marriage and you are on good terms
#
# For allied factions, the conditions are similar to the above.
# However, being the marshall or leader of your own faction does not
# guarantee cooperation from lords who dislike you.
#
# For non-allied other factions, the check for faction leader or
# marshall are not relevant, and the faction must not be at war
# with the player's faction.
("dplmc_player_can_give_troops_to_troop",
  [
	(store_script_param, ":troop_id", 1), #Party_id
	(assign, ":can_give_troops", 0),
	(assign, ":save_reg1", reg1),

	(try_begin),
		(this_or_next|eq, ":troop_id", "trp_kingdom_heroes_including_player_begin"),
		(eq, ":troop_id", "trp_player"),
		(assign, ":can_give_troops", 1),
	(else_try),
		(lt, ":troop_id", 1),
		(assign, ":can_give_troops", 0),
	(else_try),
		(store_faction_of_troop, ":troop_faction", ":troop_id"),

		(call_script, "script_troop_get_player_relation", ":troop_id"),
		(assign, ":troop_relation", reg0),
		(troop_get_slot, ":troop_reputation", ":troop_id", slot_lord_reputation_type),

		(try_begin),
			#Troop is member of player supporters faction
			(eq, ":troop_faction", "fac_player_supporters_faction"),
			##Always yes in Native, but if centralization is negative allow non-compliance
			(faction_get_slot, reg0, ":troop_faction", dplmc_slot_faction_centralization),
			(try_begin),
				(ge, reg0, 0),
				(assign, reg0, -200),
			(else_try),
				(val_mul, reg0, -10),
				(val_add, reg0, -35),#Centralization -1 has -25, -2 has -15, and -3 has -5
			(try_end),
			(gt, ":troop_relation", reg0),
			(assign, ":can_give_troops", 1),
		(else_try),
			#Troop is a member of the same faction as the player
			(eq, ":troop_faction", "$players_kingdom"),
			(faction_get_slot, ":troop_faction_leader", ":troop_faction", slot_faction_leader),
			(try_begin),
				#Leader or marshall
				(this_or_next|eq, ":troop_faction_leader", "trp_player"),
					(faction_slot_eq, ":troop_faction", slot_faction_marshall, "trp_player"),
				#If centralization is negative allow non-compliance
				(faction_get_slot, reg0, ":troop_faction", dplmc_slot_faction_centralization),
				(try_begin),
					(ge, reg0, 0),
					(assign, reg0, -200),
				(else_try),
					(val_mul, reg0, -10),
					(val_add, reg0, -35),#Centralization -1 has -25, -2 has -15, and -3 has -5
				(try_end),
				(gt, ":troop_relation", reg0),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Spouse of leader
				(gt, ":troop_faction_leader", 1),
				(neg|troop_slot_eq, "trp_player", slot_troop_spouse, -1),
				(this_or_next|troop_slot_eq, ":troop_faction_leader", slot_troop_spouse, "trp_player"),
					(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_faction_leader"),
				(call_script, "script_troop_get_player_relation", ":troop_faction_leader"),
				(ge, reg0, 0),
				#If centralization is negative allow non-compliance
				(faction_get_slot, reg0, ":troop_faction", dplmc_slot_faction_centralization),
				(try_begin),
					(ge, reg0, 0),
					(assign, reg0, -200),
				(else_try),
					(val_mul, reg0, -10),
					(val_add, reg0, -35),#Centralization -1 has -25, -2 has -15, and -3 has -5
				(try_end),
				(gt, ":troop_relation", reg0),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Spouse of troop
				(neg|troop_slot_eq, "trp_player", slot_troop_spouse, -1),
				(this_or_next|troop_slot_eq, ":troop_id", slot_troop_spouse, "trp_player"),
					(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_id"),
				(this_or_next|ge, ":troop_relation", 0),
				(this_or_next|eq, ":troop_reputation", lrep_conventional),
				(this_or_next|eq, ":troop_reputation", lrep_moralist),
					(eq, ":troop_reputation", lrep_otherworldly),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Affiliated family member
				(call_script, "script_dplmc_is_affiliated_family_member", ":troop_id"),
				(ge, reg0, 1),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Close companion previously under arms
				(this_or_next|is_between, ":troop_id", companions_begin, companions_end),
					(is_between, ":troop_id", pretenders_begin, pretenders_end),
				(neg|troop_slot_eq, ":troop_id", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
				(ge, ":troop_relation", 20),
				(assign, ":can_give_troops", 1),
			(else_try),
				#In-law (or hypothetically a blood relative) who is close with the player
				(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":troop_id", "trp_player"),
				(ge, reg0, 2),#<-- deliberately set the cutoff to 2, not 1
				(ge, ":troop_relation", 14),
				(this_or_next|ge, reg0, 10),
					(ge, ":troop_relation", 20),
				(assign, ":can_give_troops", 1),
			(try_end),
		(else_try),
			#Troop is member of a faction allied with the player's
			(call_script, "script_dplmc_get_faction_truce_length_with_faction", "$players_kingdom", ":troop_faction"),
			(gt, reg0, dplmc_treaty_defense_days_expire),
			(faction_get_slot, ":player_faction_leader", "$players_kingdom", slot_faction_leader),
			(try_begin),
				#Leader or marshall
				(this_or_next|eq, ":player_faction_leader", "trp_player"),
					(faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
				(ge, ":troop_relation", 0),#only for allied factions, not for the player's own faction
				(assign, ":can_give_troops", 1),
			(else_try),
				#Spouse of leader
				(gt, ":player_faction_leader", 1),
				(neg|troop_slot_eq, "trp_player", slot_troop_spouse, -1),
				(this_or_next|troop_slot_eq, ":player_faction_leader", slot_troop_spouse, "trp_player"),
					(troop_slot_eq, "trp_player", slot_troop_spouse, ":player_faction_leader"),
				(ge, ":troop_relation", 0),#only for allied factions, not for the player's own faction
				(call_script, "script_troop_get_player_relation", ":player_faction_leader"),
				(ge, reg0, 0),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Spouse of troop
				(neg|troop_slot_eq, "trp_player", slot_troop_spouse, -1),
				(this_or_next|troop_slot_eq, ":troop_id", slot_troop_spouse, "trp_player"),
					(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_id"),
				(this_or_next|ge, ":troop_relation", 0),
				(this_or_next|eq, ":troop_reputation", lrep_conventional),
				(this_or_next|eq, ":troop_reputation", lrep_moralist),
					(eq, ":troop_reputation", lrep_otherworldly),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Affiliated family member
				(call_script, "script_dplmc_is_affiliated_family_member", ":troop_id"),
				(ge, reg0, 1),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Close companion previously under arms
				(this_or_next|is_between, ":troop_id", companions_begin, companions_end),
					(is_between, ":troop_id", pretenders_begin, pretenders_end),
				(neg|troop_slot_eq, ":troop_id", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
				(ge, ":troop_relation", 20),
				(assign, ":can_give_troops", 1),
			(else_try),
				#In-law (or hypothetically a blood relative) who is close with the player
				(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":troop_id", "trp_player"),
				(ge, reg0, 2),#<-- deliberately set the cutoff to 2, not 1
				(ge, ":troop_relation", 14),
				(this_or_next|ge, reg0, 10),
					(ge, ":troop_relation", 20),
				(assign, ":can_give_troops", 1),
			(try_end),
		(else_try),
			#Troop is a member of a faction that isn't hostile to the player's
			(store_relation, reg0, ":troop_faction", "fac_player_faction"),
			(ge, reg0, 0),
			(store_relation, reg0, ":troop_faction", "$players_kingdom"),
			(ge, reg0, 0),
			(try_begin),
				#Spouse of troop
				(neg|troop_slot_eq, "trp_player", slot_troop_spouse, -1),
				(this_or_next|troop_slot_eq, ":troop_id", slot_troop_spouse, "trp_player"),
					(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_id"),
				(this_or_next|ge, ":troop_relation", 0),
				(this_or_next|eq, ":troop_reputation", lrep_conventional),
				(this_or_next|eq, ":troop_reputation", lrep_moralist),
					(eq, ":troop_reputation", lrep_otherworldly),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Affiliated family member
				(call_script, "script_dplmc_is_affiliated_family_member", ":troop_id"),
				(ge, reg0, 1),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Close companion previously under arms
				(this_or_next|is_between, ":troop_id", companions_begin, companions_end),
					(is_between, ":troop_id", pretenders_begin, pretenders_end),
				(neg|troop_slot_eq, ":troop_id", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
				(ge, ":troop_relation", 20),
				(assign, ":can_give_troops", 1),
			(else_try),
				#In-law (or hypothetically a blood relative) who is close with the player
				(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":troop_id", "trp_player"),
				(ge, reg0, 2),#<-- deliberately set the cutoff to 2, not 1
				(ge, ":troop_relation", 14),
				(this_or_next|ge, reg0, 10),
					(ge, ":troop_relation", 20),
				(assign, ":can_give_troops", 1),
			(try_end),
		(try_end),
	(try_end),

	(assign, reg1, ":save_reg1"),
	(assign, reg0, ":can_give_troops"),
  ])
]
