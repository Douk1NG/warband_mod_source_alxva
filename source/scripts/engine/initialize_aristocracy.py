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

initialize_aristocracy_scripts = [
#script_add_kill_death_counts
("initialize_aristocracy",
	[
	  #LORD OCCUPATIONS, BLOOD RELATIONSHIPS, RENOWN AND REPUTATIONS

	  #King ages
	  (try_for_range, ":cur_troop", kings_begin, kings_end),
		(troop_set_slot, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
		(store_random_in_range, ":age", 50, 60),
		(troop_set_slot, ":cur_troop", slot_troop_age, ":age"),
		##diplomacy start+
		#(eq, ":cur_troop", "trp_kingdom_5_lord"),#<-- There was no reason for this to be in the loop, so moved it out.
		#(troop_set_slot, ":cur_troop", slot_troop_age, 47),
	  (try_end),
	  (troop_set_slot, "trp_kingdom_5_lord", slot_troop_age, 47),#<-- Moved from above
	  ##diplomacy end+

	  #The first thing - family structure
	  #lords 1 to 8 are patriarchs with one live-at-home son and one daughter. They come from one of six possible ancestors, thus making it likely that there will be two sets of siblings
	  #lords 9 to 12 are unmarried landowners with sisters
	  #lords 13 to 20 are sons who still live in their fathers' houses
	  #For the sake of simplicity, we can assume that all male aristocrats in prior generations either married commoners or procured their brides from the Old Country, thus discounting intermarriage

	  (try_for_range, ":cur_troop", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_set_slot, ":cur_troop", slot_troop_occupation, slto_kingdom_lady),
	  (try_end),

	  (assign, ":cur_lady", "trp_kingdom_1_lady_1"),

	  (try_for_range, ":cur_troop", lords_begin, lords_end),
		(troop_set_slot, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),

		(store_random_in_range, ":father_age_at_birth", 23, 26),
#		(store_random_in_range, ":mother_age_at_birth", 19, 22),

		(try_begin),
			(is_between, ":cur_troop", "trp_knight_1_1", "trp_knight_2_1"),
			(store_sub, ":npc_seed", ":cur_troop", "trp_knight_1_1"),
			(assign, ":ancestor_seed", 1),

		(else_try),
			(is_between, ":cur_troop", "trp_knight_2_1", "trp_knight_3_1"),
			(store_sub, ":npc_seed", ":cur_troop", "trp_knight_2_1"),
			(assign, ":ancestor_seed", 7),

		(else_try),
			(is_between, ":cur_troop", "trp_knight_3_1", "trp_knight_4_1"),
			(store_sub, ":npc_seed", ":cur_troop", "trp_knight_3_1"),
			(assign, ":ancestor_seed", 13),

		(else_try),
			(is_between, ":cur_troop", "trp_knight_4_1", "trp_knight_5_1"),
			(store_sub, ":npc_seed", ":cur_troop", "trp_knight_4_1"),
			(assign, ":ancestor_seed", 19),

		(else_try),
			(is_between, ":cur_troop", "trp_knight_5_1", "trp_knight_6_1"),
			(store_sub, ":npc_seed", ":cur_troop", "trp_knight_5_1"),
			(assign, ":ancestor_seed", 25),

		(else_try),
			(is_between, ":cur_troop", "trp_knight_6_1", "trp_kingdom_1_pretender"),
			(store_sub, ":npc_seed", ":cur_troop", "trp_knight_6_1"),
			(assign, ":ancestor_seed", 31),

		(try_end),


		(try_begin),
			(lt, ":npc_seed", 8), #NPC seed is the order in the faction
			##diplomacy start+ do not overwrite reputation if it was already set explicitly
			(troop_get_slot, ":reputation", ":cur_troop", slot_lord_reputation_type),
			(try_begin),
				(lt, ":reputation", 1),
				#Original behavior:
				(assign, ":reputation", ":npc_seed"),
			(try_end),
			##diplomacy end+
			(store_random_in_range, ":age", 45, 64),

			##diplomacy start+ only set father if not already set
			(try_begin),#<- dplmc+ added
				(troop_slot_eq, ":cur_troop", slot_troop_father, -1),#<- dplmc+ added
				(store_random_in_range, ":father", 0, 6), #six possible fathers
				(val_add, ":father", ":ancestor_seed"),
				(troop_set_slot, ":cur_troop", slot_troop_father, ":father"),
			(try_end),#<- dplmc+ added
			##diplomacy end+

			#wife
			##diplomacy start+ do not rebind an already-set wife
			(try_begin),
				(troop_slot_eq, ":cur_troop", slot_troop_spouse, -1),
				#There may be a better solution, but to avoid oddities disable automatic spouses if there is a gender mismatch.
				#Mods that add additional races may want to tweak this (for example if some races shouldn't intermarry).
				(call_script, "script_dplmc_store_is_female_troop_1_troop_2", ":cur_troop", ":cur_lady"),
				#Types are stored to reg0 and reg1.
				(neq, reg0, reg1),#lord and lady aren't both female or both non-female
				(val_mul, reg0, reg1),
				(eq, reg0, 0),#at least one of lord or lady is non-female
			##diplomacy end+
				(troop_set_slot, ":cur_troop", slot_troop_spouse, ":cur_lady"),
				(troop_set_slot, ":cur_lady", slot_troop_spouse, ":cur_troop"),
                (store_faction_of_troop, ":cur_troop_faction", ":cur_troop"),
                (call_script, "script_troop_set_title_according_to_faction", ":cur_lady", ":cur_troop_faction"),
				(store_random_in_range, ":wife_reputation", 20, 26),
				(try_begin),
					(eq, ":wife_reputation", 20),
					(assign, ":wife_reputation", lrep_conventional),
				(try_end),
				(troop_set_slot, ":cur_lady", slot_lord_reputation_type, ":wife_reputation"),


				(call_script, "script_init_troop_age", ":cur_lady", 49),
				(call_script, "script_add_lady_items", ":cur_lady"),

				(val_add, ":cur_lady", 1),
			##diplomacy start+
			(try_end),
			##diplomacy end+

			#daughter
			##diplomacy start+
			(try_begin),
			##diplomacy end+
				(troop_set_slot, ":cur_lady", slot_troop_father, ":cur_troop"),
				(store_sub, ":mother", ":cur_lady", 1),
				(call_script, "script_init_troop_age", ":cur_lady", 19),
			##diplomacy start+
				#fix native bug (daughters are their own mothers)
        # Note: this bug was fixed in native version 1.158
				#(troop_set_slot, ":cur_lady", slot_troop_mother, ":cur_lady"),
				(troop_set_slot, ":cur_lady", slot_troop_mother, ":mother"),
				(try_begin),
					#swap father and mother slots if the lord was female (do nothing if both were female)
					(call_script, "script_dplmc_store_is_female_troop_1_troop_2", ":cur_troop", ":mother"),
					(neq, reg0, 0),#:cur_troop is female
					(eq, reg1, 0),#:mother is not female
					(troop_set_slot, ":cur_lady", slot_troop_mother, ":cur_troop"),
					(troop_set_slot, ":cur_lady", slot_troop_father, ":mother"),
				(try_end),
			##diplomacy end+
				(store_random_in_range, ":lady_reputation", lrep_conventional, 34), #33% chance of father-derived
				(try_begin),
					(le, ":lady_reputation", 25),
					(troop_set_slot, ":cur_lady", slot_lord_reputation_type, ":lady_reputation"),
				(else_try),
					(eq, ":lady_reputation", 26),
					(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_conventional),
				(else_try),
					(eq, ":lady_reputation", 27),
					(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_moralist),
				(else_try),
					(assign, ":guardian_reputation", ":reputation"),
					(try_begin),
						(this_or_next|eq, ":guardian_reputation", lrep_martial),
							(eq, ":guardian_reputation", 0),
						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_conventional),
					(else_try),
						(eq, ":guardian_reputation", lrep_quarrelsome),
						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_otherworldly),
					(else_try),
						(eq, ":guardian_reputation", lrep_selfrighteous),
						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_ambitious),
					(else_try),
						(eq, ":guardian_reputation", lrep_cunning),
						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_adventurous),
					(else_try),
						(eq, ":guardian_reputation", lrep_goodnatured),
						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_adventurous),
					(else_try),
						(eq, ":guardian_reputation", lrep_debauched),
						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_ambitious),
					(else_try),
						(eq, ":guardian_reputation", lrep_upstanding),
						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_moralist),
					(try_end),
				(try_end),

				(call_script, "script_add_lady_items", ":cur_lady"),
				(val_add, ":cur_lady", 1),
			##diplomacy start+
			(try_end),
			##diplomacy end+
			#high renown

		(else_try),	#Older unmarried lords
			(is_between, ":npc_seed", 8, 12),

			(store_random_in_range, ":age", 25, 36),
			##diplomacy start+ do not overwrite reputation if it was already set explicitly
			(troop_get_slot, ":reputation", ":cur_troop", slot_lord_reputation_type),
			(try_begin),
				(lt, ":reputation", 1),
				#Original behavior:
				(store_random_in_range, ":reputation", 0, 8),
			(try_end),
			##diplomacy end+

			(store_random_in_range, ":sister_reputation", 20, 26),
			(try_begin),
				(eq, ":sister_reputation", 20),
				(assign, ":sister_reputation", lrep_conventional),
			(try_end),
			(troop_set_slot, ":cur_lady", slot_lord_reputation_type, ":sister_reputation"),

			(troop_set_slot, ":cur_lady", slot_troop_guardian, ":cur_troop"),
			##diplomacy start+
			#Initialize parents
			(try_begin),
				(troop_slot_eq, ":cur_troop", slot_troop_father, -1),
				(store_mul, ":new_index", ":cur_troop", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),#defined in module_constants.py
				(val_add, ":new_index", DPLMC_VIRTUAL_RELATIVE_FATHER_OFFSET),#defined in module_constants.py
				(troop_set_slot, ":cur_troop", slot_troop_father, ":new_index"),
				(troop_slot_eq, ":cur_lady", slot_troop_father, -1),
				(troop_set_slot, ":cur_lady", slot_troop_father, ":new_index"),
			(try_end),
			(try_begin),
				(troop_slot_eq, ":cur_troop", slot_troop_mother, -1),
				(store_mul, ":new_index", ":cur_troop", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),#defined in module_constants.py
				(val_add, ":new_index", DPLMC_VIRTUAL_RELATIVE_MOTHER_OFFSET),#defined in module_constants.py
				(troop_set_slot, ":cur_troop", slot_troop_mother, ":new_index"),
				(troop_slot_eq, ":cur_lady", slot_troop_mother, -1),
				(troop_set_slot, ":cur_lady", slot_troop_mother, ":new_index"),
			(try_end),
			##diplomacy end+

			(call_script, "script_init_troop_age", ":cur_lady", 21),
			(call_script, "script_add_lady_items", ":cur_lady"),

			(val_add, ":cur_lady", 1),

		(else_try),	#Younger unmarried lords
			#age is father's minus 20 to 25
			(store_sub, ":father", ":cur_troop", 12),
			##diplomacy start+
			#Some submods don't pay attention to this aspect of the troop list, and
			#so initialization produces absurd or impossible results.  Prevent such
			#things from appearing in the game.
			(try_begin),
				#"father" can be father or mother
				#(troop_get_type, ":parent_type", ":father"),
				(try_begin),
					#(eq, ":parent_type", tf_female),
					(call_script, "script_cf_dplmc_troop_is_female", ":father"),
					(assign, ":parent_slot", slot_troop_mother),
					(assign, ":other_parent_slot", slot_troop_father),
				(else_try),
					(assign, ":parent_slot", slot_troop_father),
					(assign, ":other_parent_slot", slot_troop_mother),
				(try_end),

				(troop_slot_eq, ":cur_troop", ":parent_slot", -1),
				(store_add, ":logical_minimum_age", ":father_age_at_birth", 16),
				(troop_slot_ge, ":father", slot_troop_age, ":logical_minimum_age"),
				#Passed test
				(troop_set_slot, ":cur_troop", ":parent_slot", ":father"),
				#Set mother if not already specified
				(try_begin),
					(troop_slot_eq, ":cur_troop", ":other_parent_slot", -1),
					(troop_get_slot, ":mother", ":father", slot_troop_spouse),
					(troop_set_slot, ":cur_troop", ":other_parent_slot", ":mother"),
				(try_end),

				(troop_get_slot, ":father_age", ":father", slot_troop_age),
				(store_sub, ":age", ":father_age", ":father_age_at_birth"),

				(troop_get_slot, ":reputation", ":cur_troop", slot_lord_reputation_type),
				(try_begin),
					#Don't change reputation if it already has been set
					(lt, ":reputation", 1),
					#50% chance of having father's rep
					(store_random_in_range, ":reputation", 0, 16),

					(gt, ":reputation", 7),
					(troop_get_slot, ":reputation", ":father", slot_lord_reputation_type),
				(try_end),
			(else_try),
				#Average age is [45,63] minus [23,25], so [22, 38]
				(store_random_in_range, ":age", 22, 39),
				(troop_get_slot, ":reputation", ":cur_troop", slot_lord_reputation_type),
				#Don't change reputation if it already has been set
				(lt, ":reputation", 1),
				(store_random_in_range, ":reputation", 0, 8),
			(try_end),
			#diplomacy end+
		(try_end),

		(try_begin),
			(eq, ":reputation", 0),
			(assign, ":reputation", 1),
		(try_end),

        (troop_set_slot, ":cur_troop", slot_lord_reputation_type, ":reputation"),

		(call_script, "script_init_troop_age", ":cur_troop", ":age"),
	  (try_end),

	  (try_begin),
	    (eq, "$cheat_mode", 1),
	    (assign, reg3, "$cheat_mode"),
	    (display_message, "@{!}DEBUG -- Assigned lord reputation and relations"),

#	    (display_message, "str_assigned_lord_reputation_and_relations_cheat_mode_reg3"), #This string can be removed
	  (try_end),

	  (try_for_range, ":cur_troop", pretenders_begin, pretenders_end),
		(troop_set_slot, ":cur_troop", slot_troop_occupation, slto_inactive_pretender),
		(store_random_in_range, ":age", 25, 30),
		(troop_set_slot, ":cur_troop", slot_troop_age, ":age"),
		(eq, ":cur_troop", "trp_kingdom_5_pretender"),
		(troop_set_slot, ":cur_troop", slot_troop_age, 45),
	  (try_end),
	])
]
