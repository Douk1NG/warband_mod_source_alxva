# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *

dplmc_daily_updates_simple_triggers = [
(24,
   [
   (val_sub, "$g_dont_give_fief_to_player_days", 1),
   (val_max, "$g_dont_give_fief_to_player_days", -1),
   (val_sub, "$g_dont_give_marshalship_to_player_days", 1),
   (val_max, "$g_dont_give_marshalship_to_player_days", -1),

   ##diplomacy start+
   ##Add version checking, so the corrections are only applied once.
   ##This allows for more complicated things to be added here in the future
   (troop_get_slot, ":diplomacy_version_code", "trp_dplmc_chamberlain", dplmc_slot_troop_affiliated),#I've arbitrarily picked "when I started tracking this" as 0
   (store_mod, ":verification", ":diplomacy_version_code", 128),
   (assign, ":save_reg0", reg0),
   (assign, ":save_reg1", reg1),
   (try_begin),
		#Detect bad values
		(neq, ":diplomacy_version_code", 0),
		(neq, ":verification", 68),
		(assign, reg0, ":diplomacy_version_code"),
		(display_message, "@{!} A slot had an unexpected value: {reg0}.  This might be because you are using an incompatible troop list, or are using a non-native strange game.  This message will repeat daily."),
		(assign, ":diplomacy_version_code", -1),
	(else_try),
		(val_div, ":diplomacy_version_code", 128),
		#Update if necessary.
		(lt, ":diplomacy_version_code", DPLMC_CURRENT_VERSION_CODE),
		(ge, "$cheat_mode", 1),
		(assign, reg0, ":diplomacy_version_code"),

		(assign, reg1, DPLMC_CURRENT_VERSION_CODE),
		(display_message, "@{!} DEBUG - Detected a new version of diplomacy: previous version was {reg0}, and current version is {reg1}.  Performing updates."),
		(val_mul, reg1, 128),
		(val_add, reg1, DPLMC_VERSION_LOW_7_BITS),
		(troop_set_slot, "trp_dplmc_chamberlain", dplmc_slot_troop_affiliated, reg1),
	(try_end),

	(try_begin),
	(is_between, ":diplomacy_version_code", -1, 1),#-1 or 0
	#Native behavior follows
	##diplomacy end+

   #this to correct string errors in games started in 1.104 or before
   (party_set_name, "p_steppe_bandit_spawn_point", "str_the_steppes"),
   (party_set_name, "p_taiga_bandit_spawn_point", "str_the_tundra"),
   (party_set_name, "p_forest_bandit_spawn_point", "str_the_forests"),
   (party_set_name, "p_mountain_bandit_spawn_point", "str_the_highlands"),
   (party_set_name, "p_sea_raider_spawn_point_1", "str_the_coast"),
   (party_set_name, "p_sea_raider_spawn_point_2", "str_the_coast"),
   (party_set_name, "p_desert_bandit_spawn_point", "str_the_deserts"),


   #this to correct inappropriate home strings - Katrin to Uxkhal, Matheld to Fearichen
   # (troop_set_slot, "trp_npc11", slot_troop_home, "p_town_7"),
   (troop_set_slot, "trp_npc8", slot_troop_home, "p_village_35"),

   (troop_set_slot, "trp_npc15", slot_troop_town_with_contacts, "p_town_20"), #durquba

   #this to correct linen production at villages of durquba
   (party_set_slot, "p_village_93", slot_center_linen_looms, 0), #mazigh
   (party_set_slot, "p_village_94", slot_center_linen_looms, 0), #sekhtem
   (party_set_slot, "p_village_95", slot_center_linen_looms, 0), #qalyut
   (party_set_slot, "p_village_96", slot_center_linen_looms, 0), #tilimsal
   (party_set_slot, "p_village_97", slot_center_linen_looms, 0), #shibal zumr
   (party_set_slot, "p_village_102", slot_center_linen_looms, 0), #tamnuh
   (party_set_slot, "p_village_109", slot_center_linen_looms, 0), #habba

   (party_set_slot, "p_village_67", slot_center_fishing_fleet, 0), #Tebandra
   (party_set_slot, "p_village_5", slot_center_fishing_fleet, 15), #Kulum

   ##diplomacy start+
   #End the changes in Native
	(try_end),

   #Behavior specific to a fresh Diplomacy version
	(try_begin),
   (ge, ":diplomacy_version_code", 0),#do not run this if the code is bad
   (lt, ":diplomacy_version_code", 1),
   
   #Add home centers for claimants (mods not using standard NPCs or map may wish to remove this)
   (troop_set_slot, "trp_kingdom_1_pretender", slot_troop_home, "p_town_4"),#Lady Isolle - Suno
   (troop_set_slot, "trp_kingdom_2_pretender", slot_troop_home, "p_town_11"),#Prince Valdym - Curaw
   (troop_set_slot, "trp_kingdom_3_pretender", slot_troop_home, "p_town_18"),#Dustum Khan - Narra
   (troop_set_slot, "trp_kingdom_4_pretender", slot_troop_home, "p_town_12"),#Lethwin Far-Seeker - Wercheg
   (troop_set_slot, "trp_kingdom_5_pretender", slot_troop_home, "p_town_3"),#Lord Kastor - Veluca
   (troop_set_slot, "trp_kingdom_6_pretender", slot_troop_home, "p_town_20"),#Arwa the Pearled One - Durquba
   #add ancestral fiefs to home slots (mods not using standard NPCs or map should remove this)
   (troop_set_slot, "trp_knight_2_10", slot_troop_home, "p_castle_29"), #Nelag_Castle
   (troop_set_slot, "trp_knight_3_4", slot_troop_home, "p_castle_30"), #Asugan_Castle
   (troop_set_slot, "trp_knight_1_3", slot_troop_home, "p_castle_35"), #Haringoth_Castle
   (troop_set_slot, "trp_knight_5_11", slot_troop_home, "p_castle_33"), #Etrosq_Castle
   #Also the primary six towns (mods not using standard NPCs or map may wish to remove this)
   (troop_set_slot, "trp_kingdom_1_lord", slot_troop_home, "p_town_6"),#King Harlaus to Praven
   (troop_set_slot, "trp_kingdom_2_lord", slot_troop_home, "p_town_8"),#King Yaroglek to Reyvadin
   (troop_set_slot, "trp_kingdom_3_lord", slot_troop_home, "p_town_10"),#Sanjar Khan to Tulga
   (troop_set_slot, "trp_kingdom_4_lord", slot_troop_home, "p_town_1"),#King Ragnar to Sargoth
   (troop_set_slot, "trp_kingdom_5_lord", slot_troop_home, "p_town_5"),#King Graveth to Jelkala
   (troop_set_slot, "trp_kingdom_6_lord", slot_troop_home, "p_town_19"),#Sultan Hakim to Shariz
   
   (call_script, "script_dplmc_init_domestic_policy"),
   #Set the "original lord" values corresponding to the above.
   (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
		(this_or_next|eq, ":troop_no", "trp_knight_2_10"),#Nelag
		(this_or_next|eq, ":troop_no", "trp_knight_3_4"),#Asugan
		(this_or_next|eq, ":troop_no", "trp_knight_1_3"),#Haringoth
		(this_or_next|eq, ":troop_no", "trp_knight_5_11"),#Etrosq
		(this_or_next|is_between, ":troop_no", kings_begin, kings_end),
			(is_between, ":troop_no", pretenders_begin, pretenders_end),

		(troop_get_slot, ":center_no", ":troop_no", slot_troop_home),
		(is_between, ":center_no", centers_begin, centers_end),
		(neg|party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
		(party_set_slot, ":center_no",  dplmc_slot_center_original_lord, ":troop_no"),

		#Also set "ex-lord"
		(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(neg|party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
		(neg|party_slot_ge, ":center_no", dplmc_slot_center_ex_lord, 1),
		(party_set_slot, ":center_no", dplmc_slot_center_ex_lord, ":troop_no"),
   (try_end),

   #Make sure the affiliation slot is set correctly.
   (try_begin),
	 (is_between, "$g_player_affiliated_troop", lords_begin, kingdom_ladies_end),
	 (troop_get_slot, ":slot_val", "$g_player_affiliated_troop", dplmc_slot_troop_affiliated),
	 (is_between, ":slot_val", 0, 3),#0 is default, 1 is asked, in previous versions there was no use of 2
	 (troop_set_slot, "$g_player_affiliated_troop", dplmc_slot_troop_affiliated, 3),#3 is affiliated
   (try_end),

   #Set father/mother slots for the unmarried medium-age lords, so checking for
   #being related will work as expected.
   (try_for_range, ":troop_no", lords_begin, lords_end),
		(troop_slot_eq, ":troop_no", slot_troop_father, -1),
		(troop_slot_eq, ":troop_no", slot_troop_mother, -1),
		(store_mul, ":father", ":troop_no", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),#defined in module_constants.py
		(val_add, ":father", DPLMC_VIRTUAL_RELATIVE_FATHER_OFFSET),
		(troop_set_slot, ":troop_no", slot_troop_father, ":father"),
		(store_add, ":mother", ":father", DPLMC_VIRTUAL_RELATIVE_MOTHER_OFFSET - DPLMC_VIRTUAL_RELATIVE_FATHER_OFFSET),
		(troop_set_slot, ":troop_no", slot_troop_mother, ":mother"),
   (try_end),

   #Fix kingdom lady daughters having "slot_troop_mother" set to themselves.
   #The old fix was in troop_get_family_relation_to_troop, but now we can
   #just do it once here.
   (try_for_range, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
		(try_begin),
			(troop_slot_eq, ":troop_no", slot_troop_mother, ":troop_no"),
			(troop_get_slot, ":father", ":troop_no", slot_troop_father),
			(try_begin),
				(is_between, ":father", active_npcs_begin, active_npcs_end),
				(troop_get_slot, ":mother", ":father", slot_troop_spouse),
				(troop_set_slot, ":troop_no", slot_troop_mother, ":mother"),
				(try_begin),
					#Print a message if desired
					(ge, "$cheat_mode", 1),
					(str_store_troop_name, s0, ":troop_no"),
					(display_message, "@{!}DEBUG - Fixed slot_troop_mother for {s0}."),
				(try_end),
			(else_try),
				(troop_set_slot, ":troop_no", slot_troop_mother, -1),#better than being set to herself
				#Print a message if desired
				(ge, "$cheat_mode", 1),
				(str_store_troop_name, s0, ":troop_no"),
				(display_message, "@{!}DEBUG - When fixing slot_troop_mother for {s0}, could not find a valid mother."),
			(try_end),
	#While we're at it, also give parents to the sisters of the middle-aged lords.
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_father, -1),
			(troop_slot_eq, ":troop_no", slot_troop_mother, -1),
			#"Guardian" here means brother
			(troop_get_slot, ":guardian", ":troop_no", slot_troop_guardian),
			(ge, ":guardian", 1),
			#Has brother's father
			(troop_get_slot, ":father", ":guardian", slot_troop_father),
			(troop_set_slot, ":troop_no", slot_troop_father, ":father"),
			#Has brother's mother
			(troop_get_slot, ":mother", ":guardian", slot_troop_mother),
			(troop_set_slot, ":troop_no", slot_troop_mother, ":mother"),
		(try_end),
   #Also set original factions for ladies.
	   (neg|troop_slot_ge, ":troop_no", slot_troop_original_faction, 1),
		(assign, ":guardian", -1),
		(try_begin),
		   (troop_slot_ge, ":troop_no", slot_troop_father, 1),
			(troop_get_slot, ":guardian", ":troop_no", slot_troop_father),
 	   (else_try),
		   (troop_slot_ge, ":troop_no", slot_troop_guardian, 1),
			(troop_get_slot, ":guardian", ":troop_no", slot_troop_guardian),
		(else_try),
		   (troop_slot_ge, ":troop_no", slot_troop_spouse, 1),
			(troop_get_slot, ":guardian", ":troop_no", slot_troop_spouse),
	   (try_end),
		(ge, ":guardian", 1),
		(troop_get_slot, ":original_faction", ":guardian", slot_troop_original_faction),
		(troop_set_slot, ":troop_no", slot_troop_original_faction, ":original_faction"),
   (try_end),

	  ##Set relations between kingdom ladies and their relatives.
	  ##Do *not* initialize their relations with anyone they aren't related to:
	  ##that is used for courtship.
	  ##  The purpose of this initialization is so if a kingdom lady gets promoted,
	  ##her relations aren't a featureless slate.  Also, it would be interesting to
	  ##further develop the idea of ladies as pursuing agendas even if they aren't
	  ##leading warbands, which would benefit from giving them relations with other
	  ##people.
	  #
	  #Because relations may already exist, only call this in instances where
	  #they are 0 or 1 (the latter just means "met" between NPCs).
     (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_lady),
		(troop_get_slot, ":lady_faction", ":lady", slot_troop_original_faction),
		(ge, ":lady_faction", 1),

		(try_for_range, ":other_hero", heroes_begin, heroes_end),
		   (this_or_next|troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_lady),
			(this_or_next|troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_hero),
				(troop_slot_eq, ":other_hero", slot_troop_occupation, slto_inactive_pretender),
			(troop_slot_eq, ":other_hero", slot_troop_original_faction, ":lady_faction"),

			#Because this is not a new game: first check if relations have developed
			(call_script, "script_troop_get_relation_with_troop", ":lady", ":other_hero"),
			(is_between, reg0, 0, 2),#0 or 1

			(try_begin),
				(this_or_next|troop_slot_eq, ":lady", slot_troop_spouse, ":other_hero"),
				(troop_slot_eq, ":other_hero", slot_troop_spouse, ":lady"),
				(store_random_in_range, reg0, 0, 11),
			(else_try),
				#(call_script, "script_troop_get_family_relation_to_troop", ":lady", ":other_hero"),
				(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":lady", ":other_hero"),
			(try_end),

			(call_script, "script_troop_change_relation_with_troop", ":lady", ":other_hero", reg0),

			#This relation change only applies between kingdom ladies.
			(troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_lady),
			(is_between, ":other_hero", kingdom_ladies_begin, kingdom_ladies_end),

			(store_random_in_range, ":random", 0, 11),
			(call_script, "script_troop_change_relation_with_troop", ":lady", ":other_hero", ":random"),
		(try_end),
	  (try_end),

   #Change the occupation of exiled lords (not including pretenders or kings)
   (try_for_range, ":troop_no", lords_begin, lords_end),
		(store_troop_faction, ":faction_no", ":troop_no"),
		#A lord in the outlaw faction
		(eq, ":faction_no", "fac_outlaws"),
		#Possible values for his occupation if he's an exile (but there's some overlap between these and "bandit hero")
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),#<- The default
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),#<- This can happen joining the player faction
			(troop_slot_eq, ":troop_no", slot_troop_occupation, 0),#<- This gets set for prisoners
		#(Quick Check) Not leading a party or the prisoner of a party or at a center
		(neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 0),
		(neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
		(neg|troop_slot_ge, ":troop_no", slot_troop_cur_center, 1),#deliberately 1 instead of 0
		#(Slow check) Does not own any fiefs
		(assign, ":end", centers_end),
		(try_for_range, ":center_no", centers_begin, ":end"),
			(party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
			(assign, ":end", ":center_no"),#stop loop, and also signal failure
		(try_end),
		#(Slow check) Explicitly verify he is not a prisoner anywhere.
		(call_script, "script_search_troop_prisoner_of_party", ":troop_no"),
		(eq, reg0, -1),
		#(Slow check) Explicitly verify he's not a member of any party
		(assign, ":member_of_party", -1),
		(try_for_parties, ":party_no"),
			(eq, ":member_of_party", -1),
			(this_or_next|eq, ":party_no", "p_main_party"),
				(ge, ":party_no", centers_begin),
			(party_count_members_of_type, ":count", ":party_no", ":troop_no"),
			(gt, ":count", 0),
			(assign, ":member_of_party", ":party_no"),
		(try_end),
		(eq, ":member_of_party", -1),
		#Finally verified that he is in exile.  Set the slot value to make
		#this easier in the future.
		(troop_set_slot, ":troop_no", slot_troop_occupation, dplmc_slto_exile),
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s0, ":troop_no"),
			(display_message, "@{!}DEBUG - Changed occupation of {s0} to dplmc_slto_exile"),
		(try_end),
   (try_end),

   #Initialize histories for supported pretenders.
   (try_for_range, ":troop_no", pretenders_begin, pretenders_end),
      (neg|troop_slot_eq, ":troop_no", slot_troop_met, 0),
      (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	  (troop_slot_eq, ":troop_no", slot_troop_playerparty_history, 0),
	  (troop_set_slot, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
   (try_end),

   #Initialize histories for promoted companions
   (try_for_range, ":troop_no", companions_begin, companions_end),
	  (neg|troop_slot_eq, ":troop_no", slot_troop_met, 0),
      (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	  (neg|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
	  (troop_set_slot, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
   (try_end),

   #For all centers, update new slots
   (try_for_range, ":center_no", centers_begin, centers_end),
	  #Last attacker
	  (try_begin),
	     (party_slot_eq, ":center_no", dplmc_slot_center_last_attacker, 0),
		 (party_slot_eq, ":center_no", dplmc_slot_center_last_attacked_time, 0),
		 (party_set_slot, ":center_no", dplmc_slot_center_last_attacker, -1),
	  (try_end),

      (party_slot_eq, ":center_no", dplmc_slot_center_last_transfer_time, 0),
	  #Ex-lord
	  (try_begin),
  	     (party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, 0),
	     (party_set_slot, ":center_no", dplmc_slot_center_ex_lord, -1),
	  (try_end),
	  #Original lord
	  (try_begin),
		(party_slot_eq, ":center_no", dplmc_slot_center_original_lord, 0),
		(neg|troop_slot_eq, "trp_player", slot_troop_home, ":center_no"),
		(party_set_slot, ":center_no", dplmc_slot_center_original_lord, -1),
	  (try_end),
   (try_end),

   #Don't bother filling in "last caravan arrival" slots with fake values.
   #Right now the scripts check and do that automatically if they aren't
   #set.

   #Perform initialization for autoloot / autosell.
   (call_script, "script_dplmc_initialize_autoloot", 1),#argument "1" forces this to make changes

   #Fix a mistake I had introduced before, where you could get the wrong
   #"marry betrothed" quest when courting a lady.
   (try_begin),
      (check_quest_active, "qst_wed_betrothed_female"),
	  (quest_get_slot, ":betrothed_troop", "qst_wed_betrothed_female", slot_quest_giver_troop),
	  (is_between, ":betrothed_troop", kingdom_ladies_begin, kingdom_ladies_end),
	  (display_message, "@{!}FIXED PROBLEM - Cancelled erroneous version of qst_wed_betrothed_female.  You should be able to marry normally if you try again."),
	  (call_script, "script_abort_quest", "qst_wed_betrothed_female", 0),#abort with type 0 "event" should give no penalties to the player
   (try_end),
   #End version-checked block.
   (try_end),

   (try_begin),
    (ge, ":diplomacy_version_code", 1),
    (lt, ":diplomacy_version_code", 110615),
    #Fix a bug that was introduced in some version before 2011-06-15 that made
	#all "young unmarried lords" only have half-siblings, with either their own
	#father or mother slot uninitialized.
	(try_begin),
		(lt, 31, heroes_begin),
		(neg|troop_slot_eq, 31, 31, 0),#"slot_troop_father" was 31 in those saved games
		(troop_set_slot, 31, 31, -1),#(it still is 31 as far as I know, but this code should remain the same even if the slot value changes)
	(try_end),
	(try_begin),
		(lt, 32, heroes_begin),
		(neg|troop_slot_eq, 32,32,0),#"slot_troop_mother" was 32 in those saved games
		(troop_set_slot, 32, 32, -1),
	(try_end),
	(try_for_range, ":troop_no", lords_begin, lords_end),
		(troop_get_slot, reg0, ":troop_no", slot_troop_father),
		(troop_get_slot, reg1, ":troop_no", slot_troop_mother),
		(try_begin),
			(is_between, reg0, lords_begin, lords_end),
			(neg|is_between, reg1, kingdom_ladies_begin, kingdom_ladies_end),
			(troop_get_slot, reg1, reg0, slot_troop_spouse),
			(is_between, reg1, kingdom_ladies_begin, kingdom_ladies_end),
			(troop_set_slot, ":troop_no", slot_troop_mother, reg1),
			(call_script, "script_update_troop_notes", ":troop_no"),#Doesn't actually do anything
		(else_try),
			(is_between, reg1, kingdom_ladies_begin, kingdom_ladies_end),
			(neg|is_between, reg0, lords_begin, lords_end),
			(troop_get_slot, reg0, reg1, slot_troop_spouse),
			(is_between, reg0, lords_begin, lords_end),
			(troop_set_slot, ":troop_no", slot_troop_father, reg0),
			(call_script, "script_update_troop_notes", ":troop_no"),#Doesn't actually do anything
		(try_end),
	(try_end),

	#For old saved games, a reputation bug that was introduced in the release 2011-06-06 and was fixed on 2011-06-07.
	(eq, ":diplomacy_version_code", 1),
	(assign, reg0, 0),
	(try_for_range, ":troop_no", lords_begin, lords_end),
		(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_none),
		(store_random_in_range, reg1, lrep_none, lrep_roguish),
		(val_max, reg1, lrep_none + 1),#So there's an extra chance of getting reputation 1, which is lrep_martial
		(troop_set_slot, ":troop_no", slot_lord_reputation_type, reg1),
		(val_add, reg0, 1),
	(try_end),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(store_sub, reg1, reg0, 1),
		(display_message, "@{!} Bug fix: set personality types for {reg0} {reg1?lords:lord}"),
	(try_end),

	(assign, reg0, 0),
	(try_for_range, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
		(neq, ":troop_no", "trp_knight_1_1_wife"),#That lady should not appear in the game
		(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_none),
		(store_random_in_range, reg1, lrep_conventional - 1, lrep_moralist + 1),
		(val_max, reg1, lrep_conventional),#So there's an extra chance of getting lrep_conventional
		(troop_set_slot, ":troop_no", slot_lord_reputation_type, reg1),
		(val_add, reg0, 1),
	(try_end),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(store_sub, reg1, reg0, 1),
		(display_message, "@{!} Bug fix: set personality types for {reg0} {reg1?ladies:lady}"),
	(try_end),
   (try_end),

   #Behavior for an upgrade from Native or pre-Diplomacy 4.0 to Diplomacy 4.0
   (try_begin),
      (is_between, ":diplomacy_version_code", 0, 111001),
      #Fix: slot_faction_leader and slot_faction_marshall should not equal trp_player
      #if the player is not a member of the faction.  (This is initially true because
      #trp_player is 0, and uninitialized slots default to 0.)
      (try_for_range, ":faction_no", 0, dplmc_factions_end),
         (neq, ":faction_no", "fac_player_faction"),
         (neq, ":faction_no", "fac_player_supporters_faction"),
         (this_or_next|neq, ":faction_no", "$players_kingdom"),
         (eq, ":faction_no", 0),
         #The player is not a member of the faction:
         (try_begin),
            (faction_slot_eq, ":faction_no", slot_faction_leader, 0),
            (faction_set_slot, ":faction_no", slot_faction_leader, -1),
         (try_end),
         (try_begin),
            (faction_slot_eq, ":faction_no", slot_faction_marshall, 0),
            (faction_set_slot, ":faction_no", slot_faction_marshall, -1),
         (try_end),
      (try_end),
      #Initialize home slots for town merchants, elders, etc.
      (try_for_range, ":center_no", centers_begin, centers_end),
         (try_for_range, ":troop_no", dplmc_slot_town_merchants_begin, dplmc_slot_town_merchants_end),
            (party_get_slot, ":troop_no", ":center_no", ":troop_no"),
            (gt, ":troop_no", walkers_end),
            (troop_is_hero, ":troop_no"),
            (troop_slot_eq, ":troop_no", slot_troop_home, 0),
            (troop_set_slot, ":troop_no", slot_troop_home, ":center_no"),
         (try_end),
      (try_end),
      #Initialize home slots for startup merchants.  (Merchant of Praven, etc.)
      #This should be done after kings have their home slots initialized.
      (try_for_range, ":troop_no", kings_begin, kings_end),
         (troop_get_slot, ":center_no", ":troop_no", slot_troop_home),
         (val_sub, ":troop_no", kings_begin),
         (val_add, ":troop_no", startup_merchants_begin),
         (is_between, ":troop_no", startup_merchants_begin, startup_merchants_end),#Right now there's a startup merchant for each faction.  Verify this hasn't unexpectedly changed.
         (neg|troop_slot_ge, ":troop_no", slot_troop_home, 1),#Verify that the home slot is not already set
         (troop_set_slot, ":troop_no", slot_troop_home, ":center_no"),
      (try_end),
      #Reset potentially bad value in "slot_troop_stance_on_faction_issue" (i.e. 153) from auto-loot
      (eq, 153, slot_troop_stance_on_faction_issue),
      (try_for_range, ":troop_no", companions_begin, companions_end),
         (try_begin),
            (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
            (troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
         (else_try),
            (troop_get_slot, ":slot_val", ":troop_no", slot_troop_stance_on_faction_issue),
            (neg|is_between, ":slot_val", -1, 1),#0 or -1
            (neg|is_between, ":slot_val", heroes_begin, heroes_end),
            (troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
         (try_end),
      (try_end),
   (try_end),
   
   #SB : new features
   (try_begin),
      (is_between, ":diplomacy_version_code", 0, DPLMC_CURRENT_VERSION_CODE),
      #set up camera keys
      (call_script, "script_setup_camera_keys"),
      
      #set up disguise system, disabled by default
      (assign, "$g_dplmc_player_disguise", 0),
      (try_begin),
        (assign, ":disguise", disguise_pilgrim), #always available
        #farmer, acquired from village elders
        (assign, ":villages_end", villages_end),
        (try_for_range, ":center_no", villages_begin, ":villages_end"),
          (party_slot_ge, ":center_no", slot_center_player_relation, 25),
          (val_add, ":disguise", disguise_farmer),
          (assign, ":villages_end", -1), #loop break
        (try_end),
        
        #hunter, acquired from background or archery skill
        (try_begin),
          (store_proficiency_level, ":cur_amount", "trp_player", wpt_archery),
          (this_or_next|ge, ":cur_amount", 250),
          (this_or_next|eq, "$background_answer", cb_forester),
          (this_or_next|eq, "$background_answer_2", cb2_steppe_child),
          (eq, "$background_answer_3", cb3_poacher),
          (val_add, ":disguise", disguise_hunter),
        (try_end),
        
        #merchant, from background or gold count or enterprise
        (try_begin),
          (assign, ":continue", 0),
          (assign, ":villages_end", towns_end),
          (try_for_range, ":center_no", towns_begin, ":villages_end"),
            (party_slot_ge, ":center_no", slot_center_player_enterprise, 1),
            (assign, ":continue", 1),
            (assign, ":villages_end", towns_begin), #loop break
          (try_end),
          (try_begin),
            (eq, ":continue", 0),
            (store_troop_gold, ":cur_amount", "trp_player"),
            (store_skill_level, ":cur_skill", "trp_player", "skl_trade"),
            (ge, ":cur_skill", 5),
            (ge, ":cur_amount", 10000),
            (assign, ":continue", 1),
          (try_end),
          (this_or_next|gt, ":continue", 0),
          (this_or_next|eq, "$background_answer", cb_merchant),
          (this_or_next|eq, "$background_answer_2", cb2_merchants_helper),
          (eq, "$background_answer_3", cb3_peddler),
          (val_add, ":disguise", disguise_merchant),
        (try_end),

        #guard, from background or weapon mastery
        (try_begin),
          (store_skill_level, ":cur_skill", "trp_player", "skl_weapon_master"),
          (this_or_next|ge, ":cur_skill", 5),
          (this_or_next|eq, "$background_answer", cb_guard),
          (this_or_next|eq, "$background_answer_3", dplmc_cb3_bravo),
          (this_or_next|eq, "$background_answer_3", dplmc_cb3_merc),
          (eq, "$background_answer_3", cb3_squire),
          (val_add, ":disguise", disguise_guard),
        (try_end),
        
        #bard, from background or known songs
        (try_begin),
          (store_add, ":cur_amount", "$allegoric_poem_recitations", "$mystic_poem_recitations"),
          (val_add, ":cur_amount", "$tragic_poem_recitations"),
          (val_add, ":cur_amount", "$heroic_poem_recitations"),
          (val_add, ":cur_amount", "$comic_poem_recitations"),
          (this_or_next|ge, ":cur_amount", 2), #2 poems known
          (eq, "$background_answer_3", cb3_troubadour),
          (val_add, ":disguise", disguise_bard),
        (try_end),
      (try_end),
      (troop_set_slot, "trp_player", slot_troop_player_disguise_sets, ":disguise"),
      
      
      #equip voulges
      (troop_add_item, "trp_fighter_woman", "itm_shortened_voulge"),
      (troop_add_item, "trp_swadian_sergeant", "itm_awlpike_long"),
      (troop_add_item, "trp_swadian_deserter", "itm_shortened_voulge"),
      (troop_add_item, "trp_swadian_deserter", "itm_long_voulge"),
      (troop_add_item, "trp_swadian_crossbowman", "itm_shortened_voulge"),
      (troop_add_item, "trp_swadian_sharpshooter", "itm_long_voulge"),
      (troop_add_item, "trp_vaegir_guard", "itm_two_handed_battle_axe_2"),
      (troop_add_item, "trp_vaegir_guard", "itm_long_bardiche"),
      (troop_add_item, "trp_vaegir_infantry", "itm_two_handed_battle_axe_2"),
      (troop_remove_item, "trp_vaegir_infantry", "itm_battle_axe"),
      
      #add coloured tunics to messengers, remove leather_jerkin
      (troop_remove_item, "trp_swadian_messenger", "itm_leather_jerkin"),
      (troop_remove_item, "trp_vaegir_messenger", "itm_leather_jerkin"),
      (troop_remove_item, "trp_vaegir_messenger", "itm_sword_medieval_b"),
      (troop_remove_item, "trp_khergit_messenger", "itm_leather_jerkin"),
      (troop_remove_item, "trp_khergit_messenger", "itm_short_bow"),
      (troop_remove_item, "trp_khergit_messenger", "itm_arrows"),
      (troop_remove_item, "trp_nord_messenger", "itm_leather_jerkin"),
      (troop_remove_item, "trp_nord_messenger", "itm_short_bow"),
      (troop_remove_item, "trp_rhodok_messenger", "itm_leather_jerkin"),
      (troop_remove_item, "trp_rhodok_messenger", "itm_short_bow"),
      (troop_remove_item, "trp_rhodok_messenger", "itm_arrows"),
      #sarranid messenger already copied from horseman
      (troop_add_item, "trp_swadian_messenger", "itm_arena_tunic_red"),
      (troop_add_item, "trp_vaegir_messenger", "itm_fighting_axe"),
      (troop_add_item, "trp_vaegir_messenger", "itm_studded_leather_coat"),
      (troop_add_item, "trp_khergit_messenger", "itm_khergit_bow"),
      (troop_add_item, "trp_khergit_messenger", "itm_khergit_arrows"),
      (troop_add_item, "trp_khergit_messenger", "itm_nomad_robe"),
      (troop_add_item, "trp_nord_messenger", "itm_long_bow"),
      (troop_add_item, "trp_nord_messenger", "itm_arena_tunic_blue"),
      (troop_add_item, "trp_rhodok_messenger", "itm_light_crossbow"),
      (troop_add_item, "trp_rhodok_messenger", "itm_steel_bolts"),
      (troop_add_item, "trp_rhodok_messenger", "itm_arena_tunic_green"),
      
      #equip tavern drunks/assassin (could be done as easily in trigger)
      (troop_add_item, "trp_belligerent_drunk","itm_sword_medieval_a"),
      (troop_add_item, "trp_belligerent_drunk","itm_sword_khergit_1"), 
      (troop_add_item, "trp_belligerent_drunk","itm_arabian_sword_a"),
      (troop_remove_item, "trp_hired_assassin","itm_sword_medieval_a"),
      (troop_add_item, "trp_hired_assassin","itm_sword_viking_3"),
      (troop_add_item, "trp_hired_assassin","itm_sword_medieval_d_long"),
      (troop_add_item, "trp_hired_assassin","itm_sword_khergit_4"),
      (troop_add_item, "trp_hired_assassin","itm_arabian_sword_d"),
      (troop_add_item, "trp_hired_assassin","itm_strange_sword"),
      
      #rivacheg strange bonus chest
      (store_random_in_range, ":imod", imod_rusty, imod_strong),
      (troop_add_item, "trp_bonus_chest_1","itm_strange_sword", ":imod"),
      (store_random_in_range, ":imod", imod_rusty, imod_strong),
      (troop_add_item, "trp_bonus_chest_1","itm_strange_great_sword", ":imod"),
      (store_random_in_range, ":imod", imod_tattered, imod_lame),
      (troop_add_item, "trp_bonus_chest_1","itm_strange_boots", ":imod"),
      (store_random_in_range, ":imod", imod_tattered, imod_lame),
      (troop_add_item, "trp_bonus_chest_1","itm_strange_helmet", ":imod"),
      
      (troop_add_item, "trp_bonus_chest_2","itm_bride_dress", imod_stubborn),
      (troop_add_item, "trp_bonus_chest_2","itm_bride_crown", imod_deadly),
      (troop_add_item, "trp_bonus_chest_2","itm_bride_shoes", imod_smelling),
      (troop_add_item, "trp_bonus_chest_2","itm_torch", imod_old),

      (troop_add_item, "trp_bonus_chest_3","itm_black_armor", imod_lordly),
      (troop_add_item, "trp_bonus_chest_3","itm_black_greaves", imod_lordly),
      (troop_add_item, "trp_bonus_chest_3","itm_black_helmet", imod_lordly),
      (troop_add_item, "trp_bonus_chest_3","itm_steel_shield", imod_lordly),
      (troop_add_item, "trp_bonus_chest_3","itm_charger", imod_lordly), #charger_plate_1

      #training ground variables based on global
      (try_for_range, ":npc", training_ground_trainers_begin, training_ground_trainers_end),
        #init trainer vars, global applied to all trainers instead of individual progress
        # (troop_set_slot, ":npc", slot_troop_trainer_met, 0),
        (troop_set_slot, ":npc", slot_troop_trainer_waiting_for_result, "$waiting_for_training_fight_result"),
        (troop_set_slot, ":npc", slot_troop_trainer_training_fight_won, "$training_fight_won"),
        (troop_set_slot, ":npc", slot_troop_trainer_num_opponents_to_beat, "$num_opponents_to_beat_in_a_row"),
        (troop_set_slot, ":npc", slot_troop_trainer_training_system_explained, "$training_system_explained"),
        (troop_set_slot, ":npc", slot_troop_trainer_opponent_troop, "$novicemaster_opponent_troop"),
        (troop_set_slot, ":npc", slot_troop_trainer_training_difficulty, "$novice_training_difficulty"),
        #add random equipment
        (store_random_in_range, ":item_no", "itm_practice_sword", "itm_practice_shield"),
        (troop_add_item, ":npc", ":item_no", imod_champion),
        (store_sub, ":offset", ":npc", training_ground_trainers_begin),
        #init grounds vars
        (store_add, ":grounds", ":offset", training_grounds_begin),
        (store_add, ":scene", ":offset", "scn_training_ground_ranged_melee_1"),
        (party_set_slot, ":grounds", slot_grounds_melee, ":scene"),
        (store_add, ":scene", ":offset", "scn_training_ground_horse_track_1"),
        (party_set_slot, ":grounds", slot_grounds_track, ":scene"),
        (party_set_slot, ":grounds", slot_grounds_trainer, ":npc"),
        (party_set_slot, ":grounds", slot_grounds_count, "$g_training_ground_training_count"),
        (troop_set_slot, ":npc", slot_troop_cur_center, ":grounds"),
      (try_end),
    
    #other tavern npc based on location
      (try_for_range, ":town_no", towns_begin, towns_end),
        (try_for_range, ":slot_no", slot_center_ransom_broker, slot_center_tavern_minstrel + 1),
          (neq, ":slot_no", slot_center_traveler_info_faction),
          (party_get_slot, ":npc", ":town_no", ":slot_no"),
          (is_between, ":npc", ransom_brokers_begin, tavern_minstrels_end),
          (troop_set_slot, ":npc", slot_troop_cur_center, ":town_no"),
        (try_end),
      (try_end),
    (try_end),
    #Ensure $character_gender is set correctly
    (try_begin),
      (call_script, "script_cf_dplmc_troop_is_female", "trp_player"),
      (assign, "$character_gender", 1),
    (else_try),
      (assign, "$character_gender", 0),
    (try_end),
   ##diplomacy end+
   
   (assign, reg1, ":save_reg1"),#Revert register
   (assign, reg0, ":save_reg0"),#Revert register

   #The following scripts are to end quests which should have cancelled, but did not because of a bug
   (try_begin),
	(check_quest_active, "qst_formal_marriage_proposal"),
	(check_quest_failed, "qst_formal_marriage_proposal"),
    (call_script, "script_end_quest", "qst_formal_marriage_proposal"),
   (try_end),

   (try_begin),
	(check_quest_active, "qst_lend_companion"),
	(quest_get_slot, ":giver_troop", "qst_lend_companion", slot_quest_giver_troop),
	(store_faction_of_troop, ":giver_troop_faction", ":giver_troop"),
    (store_relation, ":faction_relation", ":giver_troop_faction", "$players_kingdom"),
    (this_or_next|lt, ":faction_relation", 0),
    (neg|is_between, ":giver_troop_faction", kingdoms_begin, kingdoms_end),
    (call_script, "script_abort_quest", "qst_lend_companion", 0),
   (try_end),



   (try_begin),
	(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
	(neq, "$players_kingdom", "fac_player_supporters_faction"),
    (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
    (val_add, "$g_player_days_as_marshal", 1),
   (else_try),
    (assign, "$g_player_days_as_marshal", 0),
   (try_end),

   (try_for_range, ":town", towns_begin, towns_end),
	(party_get_slot, ":days_to_completion", ":town", slot_center_player_enterprise_days_until_complete),
    (ge, ":days_to_completion", 1),
	(val_sub, ":days_to_completion", 1),
	(party_set_slot, ":town", slot_center_player_enterprise_days_until_complete, ":days_to_completion"),
   (try_end),
    ]),
]
