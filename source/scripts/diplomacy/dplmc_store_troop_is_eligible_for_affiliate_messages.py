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

dplmc_store_troop_is_eligible_for_affiliate_messages_scripts = [
##"script_dplmc_get_troop_standing_in_faction"
("dplmc_store_troop_is_eligible_for_affiliate_messages",
 [
	(store_script_param_1, ":troop_no"),
	(assign, ":is_eligible", 0),
	(assign, ":save_reg1", reg1),
	(try_begin),
		(lt, ":troop_no", 1),
	(else_try),
		(neg|troop_is_hero, ":troop_no"),
	(else_try),
		#Initialize :faction_no and :faction_relation
		(store_faction_of_troop, ":faction_no", ":troop_no"),
		(store_relation, ":faction_relation", ":faction_no", "fac_player_supporters_faction"),
		(try_begin),
			(eq, ":faction_no", "$players_kingdom"),
			(val_max, ":faction_relation", 1),
		(try_end),
		#Companion
		(gt, ":faction_relation", -1),
		(is_between, ":troop_no", companions_begin, companions_end),
		(neg|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
		(troop_slot_ge, ":troop_no", slot_troop_player_relation, 20),
		(assign, ":is_eligible", 1),
	(else_try),
		#Faction marshall (if the player is the faction leader)
		#Faction leader (if the player is the faction marshall)
		(eq, ":faction_no", "$players_kingdom"),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_MARSHALL),
		(call_script, "script_dplmc_get_troop_standing_in_faction", ":troop_no", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_MARSHALL),
		(assign, ":is_eligible", 1),
	(else_try),
		#Spouse / relatives / in-laws
		(gt, ":faction_relation", -1),
		#(is_between, ":troop_no", heroes_begin, heroes_end),## should be safe even for non-heroes
		(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":troop_no", "trp_player"),
		(ge, reg0, 2),
		(troop_get_slot, reg1, ":troop_no", slot_troop_player_relation),
		(val_add, reg0, reg1),
		(ge, reg0, 20),
		(assign, ":is_eligible", 1),
	(else_try),
		#Affiliates
		(call_script, "script_dplmc_is_affiliated_family_member", ":troop_no"),
		(ge, reg0, 1),
		(assign, ":is_eligible", 1),
	(else_try),
		#Cheat mode: add faction leaders to test this out
		(gt, "$cheat_mode", 0),
		(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
		(faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),
		(assign, ":is_eligible", 1),
	(try_end),
	(assign, reg1, ":save_reg1"),
	(assign, reg0, ":is_eligible"),
 ])
]
