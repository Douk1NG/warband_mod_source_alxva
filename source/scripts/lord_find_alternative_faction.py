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

lord_find_alternative_faction_scripts = [
("lord_find_alternative_faction", #Also, make it so that lords will try to keep at least one center unassigned
	[
	  (store_script_param, ":troop_no", 1),
	  (store_faction_of_troop, ":orig_faction", ":troop_no"),

	  (assign, ":new_faction", -1),
	  (assign, ":score_to_beat", -5),
	  ##diplomacy start+
	  (troop_get_slot, ":true_original_faction", ":troop_no", slot_troop_original_faction),#not necessarily ":orig_faction"
	  (try_begin),
	     (neg|is_between, ":true_original_faction", kingdoms_begin, kingdoms_end),
	     (troop_get_slot, reg0, ":troop_no", slot_troop_home),
	     (is_between, reg0, centers_begin, centers_end),
	     (party_get_slot, reg0, reg0, slot_center_original_faction),
	     (gt, reg0, 0),
	     (assign, ":true_original_faction", reg0),
	  (try_end),
	  (assign, ":original_culture", -2),
	  (try_begin),
	     (gt, ":true_original_faction", 0),
		 (faction_get_slot, ":original_culture", ":true_original_faction", slot_faction_culture),
		 (lt, ":original_culture", 1),
		 (assign, ":original_culture", ":true_original_faction"),
	  (try_end),
	  ##diplomacy end+

	  #Factions with an available center
	  (try_for_range, ":center_no", centers_begin, centers_end),
	    (this_or_next|party_slot_eq, ":center_no", slot_town_lord, stl_unassigned),
	    (party_slot_eq, ":center_no", slot_town_lord, stl_rejected_by_player),
	    (store_faction_of_party, ":center_faction", ":center_no"),
	    ##diplomacy start+ In Warband 1.142 / 1.143, this variable was added.
	    #To make certain kinds of mistakes or saved-game issues less likely,
	    #instead of checking for value 1 I'll check if the value matches the troop.
	    (this_or_next|eq, "$g_give_advantage_to_original_faction", ":troop_no"),
	    ##diplomacy end+
	    (neq, ":center_faction", ":orig_faction"),
	    (faction_get_slot, ":liege", ":center_faction", slot_faction_leader),
	    (this_or_next|neq, ":liege", "trp_player"),
	    (ge, "$player_right_to_rule", 25),
	    (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":liege"),
	    (assign, ":liege_relation", reg0),

		##diplomacy start+
		(try_begin),
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
			#If behavioral changes are enabled, bias heavily towards joining the
			#faction that contains your home (if you have one), or that has the
			#greatest cultural similarity.
			(ge, reg0, 0),
			(try_begin),
				(this_or_next|troop_slot_eq, ":troop_no", slot_troop_original_faction, ":center_faction"),
				(this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":troop_no"),
					(troop_slot_eq, ":troop_no", slot_troop_home, ":center_no"),
				(val_add, ":liege_relation", 20),
			(else_try),
				(gt, ":true_original_faction", 0),
				(party_slot_eq, ":center_no", slot_center_original_faction, ":true_original_faction"),
				(val_add, ":liege_relation", 5),
			(else_try),
				(gt, ":original_culture", 0),
				(faction_slot_eq, ":center_faction", slot_faction_culture, ":original_culture"),
				(val_add, ":liege_relation", 5),
			(try_end),
		(try_end),
		##diplomacy end+

	    (gt, ":liege_relation", ":score_to_beat"),
	    (assign, ":new_faction", ":center_faction"),
	    (assign, ":score_to_beat", ":liege_relation"),
	  (try_end),

	  #Factions without an available center
	  (try_begin),
	    (eq, ":new_faction", -1),
	    (assign, ":score_to_beat", 0),
	     #diplomacy start+
	     #If AI changes are explicitly enabled, slightly ease the requirements for entry.
	     (try_begin),
		    (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
	        (assign, ":score_to_beat", -5),
	     (try_end),
		 (store_add, ":min_acceptable_score", ":score_to_beat", 1),#used below
	     ##diplomacy end+

	    (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
	      (faction_slot_eq, ":kingdom", slot_faction_state, sfs_active),
	      (faction_get_slot, ":liege", ":kingdom", slot_faction_leader),
	      (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":liege"),
	      (assign, ":liege_relation", reg0),

		  ##diplomacy start+
		  (try_begin),
				#In Warband 1.142 / 1.143, this variable was added.
				#To make certain kinds of mistakes or saved-game issues less likely,
				#instead of checking for value 1 I'll check if the value matches the troop.
				(this_or_next|eq, "$g_give_advantage_to_original_faction", ":troop_no"),
				(neq, ":kingdom", ":orig_faction"),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
				#If behavioral changes are enabled, base your decision in part
				#on how many friends you have in the faction.
				(ge, reg0, ":min_acceptable_score"),
				(try_for_range, ":lord", heroes_begin, heroes_end),
					(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
					(neq, ":lord", ":troop_no"),
					(neq, ":lord", ":liege"),
					(store_faction_of_troop, ":lord_faction", ":lord"),
					(eq, ":lord_faction", ":kingdom"),
					(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":lord"),
					(try_begin),
						(ge, reg0, 20),
						(val_add, ":liege_relation", 1),
					(else_try),
						(lt, reg0, -19),
						(val_sub, ":liege_relation", 1),
					(try_end),
				(try_end),
				#Also give a bonus towards rejoining the lord's original faction.
				#if it isn't the one the lord has just left.
				(try_begin),
					(eq, ":true_original_faction", ":kingdom"),
					(val_add, ":liege_relation", 5),
				(else_try),
					#Not the same but similar
					(gt, ":original_culture", 0),
					(faction_slot_eq, ":kingdom", slot_faction_culture, ":original_culture"),
					(val_add, ":liege_relation", 2),
				(try_end),
				#The next bit is to prevent this change from increasing the number of
				#lords who find all kingdoms unacceptable.
				(val_max, ":liege_relation", ":min_acceptable_score"),
		  (try_end),
		  ##diplomacy end+

	      (gt, ":liege_relation", ":score_to_beat"),

	      (assign, ":new_faction", ":kingdom"),
	      (assign, ":score_to_beat", ":liege_relation"),
	    (try_end),
	  (try_end),

	  (assign, reg0, ":new_faction"),
	])
]
