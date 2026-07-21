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

get_relevant_comment_to_s42_scripts = [
("get_relevant_comment_to_s42",
    [

     (troop_get_slot, ":reputation", "$g_talk_troop", slot_lord_reputation_type),
     (try_begin),
       (eq, "$cheat_mode", 1),
       (store_add, ":rep_string", ":reputation", "str_personality_archetypes"),
       (str_store_string, s15, ":rep_string"),
       (display_message, "@{!}Reputation type: {s15}"),
     (try_end),


     (assign, ":highest_score_so_far", 50),
     (assign, ":best_comment_so_far", -1),
     (assign, ":rejoinder_to_best_comment_so_far", -1),
     (assign, ":comment_found", 0),
     (assign, ":best_log_entry", -1),
     (assign, ":comment_relation_change", 0),
     (store_current_hours, ":current_time"),
	 ##diplomacy start+
	 (assign, ":best_comment_reg4", 0),
	 ##diplomacy end+

#prevents multiple comments in conversations in same hour

#     (troop_get_slot, ":talk_troop_last_comment_time", "$g_talk_troop", slot_troop_last_comment_time),
#"$num_log_entries should also be set to one, not zero. This is included in the initialize npcs script, although could be moved to game_start
     (troop_get_slot, ":talk_troop_last_comment_slot", "$g_talk_troop", slot_troop_last_comment_slot),
     (troop_set_slot, "$g_talk_troop", slot_troop_last_comment_slot, "$num_log_entries"),

     (store_add, ":log_entries_plus_one", "$num_log_entries", 1),
     (try_for_range, ":log_entry_no", 1, ":log_entries_plus_one"),
#      It should be log entries plus one, so that the try_ sequence does not stop short of the last log entry
#      $Num_log_entries is now the number of the last log entry, which begins at "1" rather than "0"
#      This is so that (le, ":log_entry_no", ":talk_troop_last_comment_slot") works properly

       (troop_get_slot, ":entry_time",           "trp_log_array_entry_time",           ":log_entry_no"),
#      (val_max, ":entry_time", 1), #This is needed for pre-game events to be commented upon, if hours are used rather than the order of events
       (store_sub, ":entry_hours_elapsed", ":current_time", ":entry_time"),
       (try_begin),
         (le, ":log_entry_no", ":talk_troop_last_comment_slot"),
#         (le, ":entry_time", ":talk_troop_last_comment_time"),
         (try_begin),
           (eq, ":log_entry_no", ":talk_troop_last_comment_slot"),
           (eq, "$cheat_mode", 1),
           (assign, reg5, ":log_entry_no"),
           (display_message, "@{!}Entries up to #{reg5} skipped"),
         (try_end),
#       I suggest using the log entry number as opposed to time so that events in the same hour can be commented upon
#       This feels more natural, for example, if there are other lords in the court when the player pledges allegiance
       (else_try),
#         (le, ":entry_hours_elapsed", 3), #don't comment on really fresh events
#       (else_try),
         (call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
         (gt, reg1, 10),
         (assign, ":score", reg1),
         (assign, ":comment", reg0),
		 #reg2 is what
		 (assign, ":rejoinder", reg3),

         (store_random_in_range, ":rand", 70, 140),
         (val_mul, ":score", ":rand"),
         (store_add, ":entry_time_score", ":entry_hours_elapsed", 500), #approx. one month
         (val_mul, ":score", 1000),
         (val_div, ":score", ":entry_time_score"), ###Relevance decreases over time - halved after one month, one-third after two, etc
         (try_begin),
           (gt, ":score", ":highest_score_so_far"),
           (assign, ":highest_score_so_far", ":score"),
           (assign, ":best_comment_so_far",  ":comment"),
           (assign, ":rejoinder_to_best_comment_so_far",  ":rejoinder"),
           (assign, ":best_log_entry", ":log_entry_no"),
           (assign, ":comment_relation_change", reg2),
		   ##diplomacy start+
		   (assign, ":best_comment_reg4", reg4),
		   ##diplomacy end+
         (try_end),
       (try_end),
     (try_end),

     (try_begin),
       (gt, ":best_comment_so_far", 0),
       (assign, ":comment_found", 1), #comment found print it to s61 now.
       (troop_get_slot, ":actor",                 "trp_log_array_actor",                 ":best_log_entry"),
       (troop_get_slot, ":center_object",         "trp_log_array_center_object",         ":best_log_entry"),
       (troop_get_slot, ":center_object_lord",    "trp_log_array_center_object_lord",    ":best_log_entry"),
       (troop_get_slot, ":center_object_faction", "trp_log_array_center_object_faction", ":best_log_entry"),
       (troop_get_slot, ":troop_object",          "trp_log_array_troop_object",          ":best_log_entry"),
       (troop_get_slot, ":troop_object_faction",  "trp_log_array_troop_object_faction",  ":best_log_entry"),
       (troop_get_slot, ":faction_object",        "trp_log_array_faction_object",        ":best_log_entry"),
	   ##diplomacy start+
	   (assign, reg4, ":best_comment_reg4"),
	   ##diplomacy end+
       (try_begin),
         (ge, ":actor", 0),
         (str_store_troop_name,   s50, ":actor"),
		 ##diplomacy start+
		 (eq, ":best_comment_so_far", "str_comment_i_quarreled_with_troop_over_woman"),
		 (neq, ":actor", "$g_talk_troop"),
		 (neq, ":actor", "trp_player"),
         #SB : other script
         (call_script, "script_dplmc_store_troop_is_female_reg", ":actor", 3),
		 ##diplomacy end+
       (try_end),
       (try_begin),
         (ge, ":center_object", 0),
		 ##diplomacy start+
		 ##OLD:
		 #(str_store_party_name,   s51, ":center_object"),
		 ##NEW:
		 #Alternate meaning (not usually called from this script, but just in case)
		 #In this case, s51 is actually a troop.  Use reg3 for the gender.
		 (try_begin),
			(eq, ":best_comment_so_far", "str_comment_i_quarreled_with_troop_over_woman"),
			(str_store_troop_name, s51, ":center_object"),
			(neq, ":center_object", "$g_talk_troop"),
			(neq, ":center_object", "trp_player"),
			(call_script, "script_dplmc_store_troop_is_female_reg", ":center_object", 3),
		 (else_try),
		   (neq, ":best_comment_so_far", "str_comment_i_quarreled_with_troop_over_woman"),
 		   (str_store_party_name,   s51, ":center_object"),#<- old behavior
  	    (try_end),
		##diplomacy end+
       (try_end),
       (try_begin),
         (ge, ":center_object_lord", 0),
         (str_store_troop_name,   s52, ":center_object_lord"),
       (try_end),
       (try_begin),
         (ge, ":center_object_faction", 0),
         (str_store_faction_name, s53, ":center_object_faction"),
       (try_end),
       (try_begin),
         (ge, ":troop_object", 0),
         (str_store_troop_name,   s54, ":troop_object"),
       (try_end),
       (try_begin),
         (is_between, ":troop_object_faction", kingdoms_begin, kingdoms_end),
         (str_store_faction_name, s55, ":troop_object_faction"),
         (str_store_string, s55, "str_the_s55"),
	   (else_try),
		 (is_between, ":troop_object", bandits_begin, bandits_end),
         (str_store_string, s55, "str_bandits"),
	   (else_try),
	     (eq, ":troop_object_faction", "fac_deserters"),
         (str_store_string, s55, "str_deserters"),
       (else_try),
         (str_store_string, s55, "str_travellers_on_the_road"),
	   (else_try),

       (try_end),

       (try_begin),
         (ge, ":faction_object", 0),
         (str_store_faction_name, s56, ":faction_object"),
       (try_end),
	   (assign, "$g_last_comment_copied_to_s42", ":best_comment_so_far"), #maybe deprecate
	   (assign, "$g_rejoinder_to_last_comment", ":rejoinder_to_best_comment_so_far"),

       (str_store_string, s42, ":best_comment_so_far"),
     (try_end),

     (assign, reg0, ":comment_found"),

     (assign, "$log_comment_relation_change", ":comment_relation_change"),
     ])
]
