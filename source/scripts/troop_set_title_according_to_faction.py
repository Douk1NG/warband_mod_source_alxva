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

troop_set_title_according_to_faction_scripts = [
# script_troop_set_title_according_to_faction
# Input: arg1 = troop_no, arg2 = faction_no
# EDITED FROM NATIVE TO ALLOW CUSTOM PLAYER KINGDOM TITLES
("troop_set_title_according_to_faction",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":faction_no", 2),
      ##diplomacy start+
      # OLD CODE:
      #(try_begin),
      #  (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
      #  (str_store_troop_name_plural, s0, ":troop_no"),
      #  (troop_get_type, ":gender", ":troop_no"),
      #  (store_sub, ":title_index", ":faction_no", kingdoms_begin),
      #  (try_begin),
      #    (eq, ":gender", 0), #male
      #    (val_add, ":title_index", kingdom_titles_male_begin),
      #  (else_try),
      #    (val_add, ":title_index", kingdom_titles_female_begin),
      #  (try_end),
      #  (str_store_string, s1, ":title_index"),
      #  (troop_set_name, ":troop_no", s1),
      #  (troop_get_slot, ":troop_party", ":troop_no", slot_troop_leaded_party),
      #  (gt, ":troop_party", 0),
      #  (str_store_troop_name, s5, ":troop_no"),
      #  (party_set_name, ":troop_party", "str_s5_s_party"),
      #(try_end),
      #
      # NEW CODE:
      (assign, ":save_reg0", 0),
      (assign, ":custom_name", 0),
      (try_begin),
	    #Don't do anything when given a bad value.
		 #
		 #We could restrict this further, checking whether the troop is a hero,
		 #or whether it's between heroes_begin and heroes_end, but there are
		 #legitimate reasons a coder may want to run this to get a temporary value,
		 #or use this with temporary heroes, or so forth.
		 #
		 #However, some things are unambiguously errors:
		 (this_or_next|lt, ":troop_no", 0),# At best, the rename operation would fail.
		 (this_or_next|eq, ":troop_no", "trp_heroes_end"),# This is used to store custom titles, so applying a title to this will mess them up.
		 (this_or_next|eq, ":troop_no", "trp_kingdom_heroes_including_player_begin"),#This could easily end up changed due to carelessness
		 #There is also no legitimate reason to try to give the titles to generic soldiers.
		 (is_between, ":troop_no", soldiers_begin, soldiers_end),
	  ##Custom player kingdom vassal titles, credit Caba`drin start
	  #(Updated 2011-04-24, to use Caba`drin's 2011-04-20 bug-fix and update)
	  # See http://forums.taleworlds.com/index.php/topic,148259.0.html
      (else_try),
		(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),#<- dplmc+ altered
		(assign, ":troop_is_female", reg0),
		##Additional alteration start
		#All Rhodok benefactor / custodian NPCs insist on the name "Tribune"
		#Currently this is just Bunduk, but others could be added.
		(try_begin),
			(str_store_troop_name, s1, ":troop_no"),#s1 is overwritten below
			#For dialogue reasons, this should be enabled even when the player
			#is co-ruler of an NPC kingdom.
			(this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
				(eq, ":faction_no", "$players_kingdom"),
			(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor),
				(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_custodian),
			(troop_slot_eq, ":troop_no", slot_troop_original_faction, "fac_kingdom_5"),
			(assign, ":is_coruler", 0),
			(try_begin),
				(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
				(faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
				(gt, ":faction_leader", -1),
				(this_or_next|eq, ":faction_leader", "trp_player"),
				(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":faction_leader"),
					(troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
				(assign, ":is_coruler", 1),
			(try_end),
			(this_or_next|eq, ":is_coruler", 1),
				(eq, ":faction_no", "fac_player_supporters_faction"),
			(str_store_string, s0, "@Tribune"),
			(str_store_troop_name_plural, s1, ":troop_no"),
			(str_store_string, s1, "str_s0_s1"),
		##Additional alteration end
		(else_try),
            (eq, ":faction_no", "fac_player_supporters_faction"),
            #(troop_get_type, ":gender", ":troop_no"),#<- dplmc+ altered (use script for gender instead)
            (try_begin),
              (eq, ":troop_is_female", 0), #male #<- dplmc+ altered
              (troop_slot_eq, "trp_heroes_end", 0, 1),
              (str_store_troop_name, s0, "trp_heroes_end"),
              (str_store_troop_name_plural, s1, ":troop_no"),
              (str_store_string, s1, "str_s0_s1"),
              (assign, ":custom_name", 1),
            (else_try),
              (eq, ":troop_is_female", 1), #slot 0 is potentially unassigned, 'Countess Alayen'
              (troop_slot_eq, "trp_heroes_end", 1, 1),

              #unmarried ladies should retain title
              (assign, ":continue", 0),
              (try_begin),
                  (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
                  (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                  (troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
                  (assign, ":continue", 1),
              (else_try),
                  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                  (assign, ":continue", 1),
              (try_end),
              (eq, ":continue", 1),

              (str_store_troop_name_plural, s0, "trp_heroes_end"),
              (str_store_troop_name_plural, s1, ":troop_no"),
              (str_store_string, s1, "str_s0_s1"),
              (assign, ":custom_name", 1),
            (try_end),
            (eq, ":custom_name", 1), #So if it fails, will rename normally
        (else_try),
            (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
            (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
            ##Additional section begin: add support for player kingdom culture
            (try_begin),
                (eq, ":faction_no", "fac_player_supporters_faction"),
                (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
                (assign, ":faction_no", "$g_player_culture"),#<- Use title from culture if one is set, and not using custom titles
            (try_end),
            ##Additional section end
            (str_store_troop_name_plural, s0, ":troop_no"),
            #(troop_get_type, ":gender", ":troop_no"),#<- dplmc+ altered
            (store_sub, ":title_index", ":faction_no", kingdoms_begin),
            (try_begin),
                (this_or_next|eq, ":troop_no", ":faction_leader"),
                (troop_slot_eq, ":troop_no", slot_troop_spouse, ":faction_leader"), #wife is now queen/khatun/sultana
                (try_begin),
                    (eq, ":troop_is_female", 0),
                    (val_add, ":title_index", "str_faction_leader_title_male_player"),
                (else_try),
                    (val_add, ":title_index", "str_faction_leader_title_female_player"),
                (try_end),
            (else_try),
                (try_begin),
                  (eq, ":troop_is_female", 0), #<- dplmc+ altered
                  (val_add, ":title_index", kingdom_titles_male_begin),
                (else_try),
                  (try_begin),
                      (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
                      (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                      (troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
                      (val_add, ":title_index", kingdom_titles_female_begin),
                  (else_try),
                      (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                      (val_add, ":title_index", kingdom_titles_female_begin),
                  (else_try),
                      (assign, ":title_index", kingdom_titles_female_begin), #unmarried or unlanded ladies should just be Lady
                  (try_end),
                (try_end),
            (try_end),
            (str_store_string, s1, ":title_index"),
        (try_end),
        (troop_set_name, ":troop_no", s1),
        (troop_get_slot, ":troop_party", ":troop_no", slot_troop_leaded_party),
        (gt, ":troop_party", 0),
        (str_store_troop_name, s5, ":troop_no"),
        (party_set_name, ":troop_party", "str_s5_s_party"),
      (try_end),
      ##Custom player kingdom vassal titles, credit Caba'drin end
      (assign, reg0, ":save_reg0"),
      ##diplomacy end+
      ])
]
