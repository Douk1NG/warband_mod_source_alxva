# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_print_cultural_word_to_sreg (script)
# Called by menus in 2 domains: diplomacy, siege
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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_print_cultural_word_to_sreg_scripts = [
##Auto-Buy-Food from rubik's Custom Commander end
##INPUTS:
#  arg1  - speaker troop
#  arg2  - which word/phrase to retrieve (arbitrary code)
#  arg3  - string register
#OUTPUTS:
#  writes result to string register
("dplmc_print_cultural_word_to_sreg", [
     (store_script_param, ":speaker", 1),
     (store_script_param, ":context", 2),
     (store_script_param, ":string_register", 3),

     #Right now this is entirely faction-based, but you could give different
     #results for individual lords.
	 #(Note: Now certain parts of it do vary for heroes, to mimic the behavior in Native
	 #feast dialogs for the word for wine.)

     (assign, ":speaker_faction", -1),
     (try_begin),
		#Player faction
		(this_or_next|eq, ":speaker", "trp_player"),
			(eq, ":speaker", "trp_kingdom_heroes_including_player_begin"),
		(assign, ":speaker_faction", "fac_player_supporters_faction"),#<- This will potentially get translated later
	 (else_try),
		#Hero original faction
        (is_between, ":speaker", heroes_begin, heroes_end),
        (troop_get_slot, ":speaker_faction", ":speaker", slot_troop_original_faction),
	 (else_try),
		#Hero original faction
		(gt, ":speaker", -1),
		(troop_is_hero, ":speaker"),
		(troop_slot_ge, ":speaker", slot_troop_original_faction, npc_kingdoms_begin),
		(neg|troop_slot_ge, ":speaker", slot_troop_original_faction, npc_kingdoms_end),
		(troop_get_slot, ":speaker_faction", ":speaker", slot_troop_original_faction),
     (else_try),
		#Troop current faction
        (gt, ":speaker", -1),
        (store_troop_faction, ":speaker_faction", ":speaker"),
     (try_end),

	 (try_begin),
      (lt, ":speaker", 1),
     (else_try),
	   ##Only continue if the current faction isn't associated with a distinctive culture
	   (lt, ":speaker_faction", dplmc_non_generic_factions_begin),
	   ##This will work unless the order of the first factions gets changed
	 (else_try),
	   #Translate raiders into the equivalent kingdoms
	   (is_between, ":speaker", bandits_begin, bandits_end),
         (try_begin),
			(eq, ":speaker", "trp_mountain_bandit"),#Mountain bandits
			(assign, ":speaker_faction", "fac_kingdom_5"),#Rhodoks
		 (else_try),
			(eq, ":speaker", "trp_forest_bandit"),#Forest bandits
			(assign, ":speaker_faction", "fac_kingdom_1"),#Swadian
		 (else_try),
			(eq, ":speaker", "trp_sea_raider"),#Sea raiders
			(assign, ":speaker_faction", "fac_kingdom_4"),#Nords
		 (else_try),
			(eq, ":speaker", "trp_steppe_bandit"),#Steppe bandits
			(assign, ":speaker_faction", "fac_kingdom_3"),#Khergits
		 (else_try),
			(eq, ":speaker", "trp_taiga_bandit"),#Taiga bandits
			(assign, ":speaker_faction", "fac_kingdom_2"),#Vaegir
		 (else_try),
			(eq, ":speaker", "trp_desert_bandit"),#Desert bandits
			(assign, ":speaker_faction", "fac_kingdom_6"),#Sarranid
		 (try_end),
		 (ge, ":speaker_faction", dplmc_non_generic_factions_begin),
    (else_try),
		#For companions without default initial cultures, infer one from their home.
		#(Actually, don't limit this to companions, since there's a chance that others
		#could have a valid home slot.)
		#(is_between, ":speaker", companions_begin, companions_end),
		#(is_between, ":speaker", heroes_begin, heroes_end),
		(troop_is_hero, ":speaker"),
		(troop_get_slot, ":home_center", ":speaker", slot_troop_home),
		(is_between, ":home_center", centers_begin, centers_end),
		(party_get_slot, ":speaker_faction", ":home_center", slot_center_original_faction),
	 (else_try),
		#For villagers, merchants, etc.
		(eq, ":speaker", "$g_talk_troop"),
		(neg|is_between, ":speaker", heroes_begin, heroes_end),#Not a character that might have an explicitly-set faction
		(neg|is_between, ":speaker", training_ground_trainers_begin, tavern_minstrels_end),#Not a trainer, ransom broker, traveler, bookseller, or minstrel
		(ge, "$g_encountered_party", 0),
		(try_begin),
			#For towns / castles / villages, use the original faction
			(is_between, "$g_encountered_party", centers_begin, centers_end),
			(party_get_slot, ":speaker_faction", "$g_encountered_party", slot_center_original_faction),
		(else_try),
			#Use faction of encountered party
			(party_is_active, "$g_encountered_party"),
			(store_faction_of_party, ":speaker_faction", "$g_encountered_party"),
			#For generic factions, use the closest center
			(lt, ":speaker_faction", dplmc_non_generic_factions_begin),
			(assign, ":speaker_faction", reg0),#save register
			(call_script, "script_get_closest_center", "$g_encountered_party"),
			(assign, ":home_center", reg0),
			(assign, reg0, ":speaker_faction"),#revert register
			(party_get_slot, ":speaker_faction", ":home_center", slot_center_original_faction),
		(try_end),
	 (try_end),

    #Translate for player's kingdom
	 (try_begin),
		(ge, "$players_kingdom", dplmc_non_generic_factions_begin),
		(this_or_next|eq, ":speaker_faction", "fac_player_faction"),
		(this_or_next|eq, ":speaker_faction", "fac_player_supporters_faction"),
		(eq, ":speaker_faction", "$players_kingdom"),
		(assign, ":speaker_faction", "$players_kingdom"),
		(neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(this_or_next|is_between, "$g_player_culture", cultures_begin, cultures_end),
		(is_between,"$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
		(assign, ":speaker_faction", "$g_player_culture"),
	 (try_end),

     #Store variant
     (try_begin),
        #Iconic cultural weapon that can be used metonymously for force of arms.
		#Native equivalent is "sword".
		#Non-Warband example: "He who lives by the {sword}, dies by the {sword}."
		#Example usage: "My {sword} is at the disposal of my liege."
		(eq, ":context", DPLMC_CULTURAL_TERM_WEAPON),
        (try_begin),
           (this_or_next|eq, ":speaker_faction", "fac_kingdom_4"),#Nords
           (eq, ":speaker_faction", "fac_kingdom_2"),#Vaegirs
           (str_store_string, ":string_register", "@axe"),
        (else_try),
           (eq, ":speaker_faction", "fac_kingdom_5"),#Rhodoks
           (str_store_string, ":string_register", "@spear"),
        (else_try),
           (eq, ":speaker_faction", "fac_kingdom_3"),#Khergits
           (str_store_string, ":string_register", "@bow"),
        (else_try),
			#Default: Swadia, Sarranid, others
           (str_store_string, ":string_register", "@sword"),
        (try_end),
    (else_try),
        #Plural version of iconic cultural weapon that can be used metonymously for force of arms.
		#Native equivalent is "swords".
		(eq, ":context", DPLMC_CULTURAL_TERM_WEAPON_PLURAL),
        (try_begin),
           (this_or_next|eq, ":speaker_faction", "fac_kingdom_4"),#Nords
           (eq, ":speaker_faction", "fac_kingdom_2"),#Vaegirs
           (str_store_string, ":string_register", "@axes"),
        (else_try),
           (eq, ":speaker_faction", "fac_kingdom_5"),#Rhodoks
           (str_store_string, ":string_register", "@spears"),
        (else_try),
           (eq, ":speaker_faction", "fac_kingdom_3"),#Khergits
           (str_store_string, ":string_register", "@bows"),
        (else_try),
			#Default: Swadia, Sarranid, others
           (str_store_string, ":string_register", "@swords"),
        (try_end),
	 (else_try),
		#Cultural phrase that means "fight" (first person singular)
		#Native equivalent is "swing my sword."
		#Example usage: "I want to be able to {swing my sword} with a good conscience."
        (eq, ":context", DPLMC_CULTURAL_TERM_USE_MY_WEAPON),
        (try_begin),
           (eq, ":speaker_faction", "fac_kingdom_4"),#Nords
           (eq, ":speaker_faction", "fac_kingdom_2"),#Vaegirs
           (str_store_string, ":string_register", "@swing my axe"),
        (else_try),
           (eq, ":speaker_faction", "fac_kingdom_5"),#Rhodoks
           (str_store_string, ":string_register", "@lift my spear"),
        (else_try),
           (eq, ":speaker_faction", "fac_kingdom_3"),#Khergits
           (str_store_string, ":string_register", "@loose my arrows"),
        (else_try),
			#Default: Swadia, Sarranid, others
           (str_store_string, ":string_register", "@swing my sword"),
        (try_end),
	(else_try),
		#equivalent to lowercase "king" or "queen"
		(this_or_next|eq, ":context", DPLMC_CULTURAL_TERM_KING_FEMALE),
		(eq, ":context", DPLMC_CULTURAL_TERM_KING),
		(try_begin),
		   (eq, ":speaker_faction", "fac_kingdom_3"),#Khergit
		   (str_store_string, ":string_register", "str_khan"),
		(else_try),
		   (eq, ":speaker_faction", "fac_kingdom_6"),#Sarranid
		   (str_store_string, ":string_register", "@sultan"),
		(else_try),
		   #Default: Swadia, Rhodok, Nord, Vaegir, others
		   (str_store_string, ":string_register", "str_king"),
		   (eq, ":context", DPLMC_CULTURAL_TERM_KING_FEMALE),
		   (str_store_string, ":string_register", "str_queen"),
		(try_end),
	(else_try),
		#equivalent to lowercase "kings"
		(eq, ":context", DPLMC_CULTURAL_TERM_KING_PLURAL),
		(try_begin),
		   (eq, ":speaker_faction", "fac_kingdom_3"),#Khergit
		   (str_store_string, ":string_register", "@khans"),
		(else_try),
		   (eq, ":speaker_faction", "fac_kingdom_6"),#Sarranid
		   (str_store_string, ":string_register", "@sultans"),
		(else_try),
 		   #Default: Swadia, Rhodok, Nord, Vaegir, others
		   (str_store_string, ":string_register", "@kings"),
		(try_end),
	(else_try),
		#equivalent to lowercase "lord"
		(eq, ":context", DPLMC_CULTURAL_TERM_LORD),
		(str_store_string, ":string_register", "@lord"),
	(else_try),
		#equivalent to lowercase "lords"
		(eq, ":context", DPLMC_CULTURAL_TERM_LORD_PLURAL),
		(str_store_string, ":string_register", "@lords"),
	(else_try),
		#As in, "I shall tell my {swineherd} about your sweet promises" or "Any {swineherd} can claim to be king".
		(eq, ":context", DPLMC_CULTURAL_TERM_SWINEHERD),
		(assign, ":mode", ":speaker"),
		(try_begin),
		   (gt, ":speaker", 0),
		   (neg|troop_is_hero, ":speaker"),
		   (store_current_hours, ":mode"),
		   (val_add, ":mode", "$g_encountered_party"),
		(try_end),
		(val_max, ":mode", 0),#Default to mode 0 for negative speakers
		(val_mod, ":mode", 2),
		(try_begin),
           (eq, ":speaker_faction", "fac_kingdom_2"),#Vaegirs
		   (try_begin),
		      (eq, ":mode", 0),
              (str_store_string, ":string_register", "@goatherd"),
		   (else_try),
		       (str_store_string, ":string_register", "@swineherd"),
		   (try_end),
        (else_try),
		   (eq, ":speaker_faction", "fac_kingdom_3"),#Khergits
		   (try_begin),
		      (eq, ":mode", 0),
              (str_store_string, ":string_register", "@stable {boy/girl}"),
        (else_try),
		      (str_store_string, ":string_register", "@shepherd {boy/girl}"),
		   (try_end),
		(else_try),
		   (eq, ":speaker_faction", "fac_kingdom_6"),#Sarranids
		   (try_begin),
		      (eq, ":mode", 0),
		      (str_store_string, ":string_register", "@goatherd"),
		   (else_try),
		      (str_store_string, ":string_register", "@shepherd {boy/girl}"),
		   (try_end),
        (else_try),
           #Swadia, Rhodok, Nord, others
           (str_store_string, ":string_register", "@swineherd"),
        (try_end),
	(else_try),
		#As in, "I'd like to buy every man who comes in here tonight a jar of your best wine."
		(this_or_next|eq, ":context", DPLMC_CULTURAL_TERM_TAVERNWINE),
		#Follow the pattern used in Native for lords in feasts
		#(c.f. "str_flagon_of_mead", "str_skin_of_kumis", "str_mug_of_kvass", "str_cup_of_wine")

		(try_begin),
			#For lords, use "mode" so it works the same as in feast dialogs
			(is_between, ":speaker", heroes_begin, heroes_end),
			(this_or_next|neg|is_between, ":speaker", companions_begin, companions_end),
				(neg|troop_slot_eq, ":speaker", slot_troop_original_faction, ":speaker_faction"),
			(store_mod, ":mode", ":speaker", 2),
		(else_try),
			#Otherwise set mode to 0, to always use the cultural alternative
			(assign, ":mode", 0),
		(try_end),

		(try_begin),
			(eq, ":speaker_faction", "fac_kingdom_2"),
			(eq, ":mode", 0),#From feast: 50% chance of falling through to "wine"
			(str_store_string, ":string_register", "@kvass"),#Vaegirs: kvass
		(else_try),
			(eq, ":speaker_faction", "fac_kingdom_3"),
			(eq, ":mode", 0),#From feast: 50% chance of falling through to "wine"
			(str_store_string, ":string_register", "@kumis"),#Khergits: kumis
		(else_try),
			(eq, ":speaker_faction", "fac_kingdom_4"),
			(str_store_string, ":string_register", "@mead"),#Nords: mead
		(else_try),
			(str_store_string, ":string_register", "@wine"),#Default: wine
		(try_end),
    (else_try),
	#Error string
        (assign, ":save_reg0", reg0),
		(assign, reg0, ":context"),
		(display_message, "@{!}ERROR - dplmc_print_cultural_word_to_sreg called for bad context {reg0}"),
		(str_store_string, ":string_register", "str_ERROR_string"),
		(assign, reg0, ":save_reg0"),
    (try_end),

   ])
]
