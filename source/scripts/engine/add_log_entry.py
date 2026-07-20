# ======================================================================
# SHARED DEPENDENCY
# Entity: add_log_entry (script)
# Called by menus in 6 domains: battle, castle, kingdom_management, notifications, town, village
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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

add_log_entry_scripts = [
("add_log_entry",
    [(store_script_param, ":entry_type", 1),
     (store_script_param, ":actor", 2),
     (store_script_param, ":center_object", 3),
     (store_script_param, ":troop_object", 4),
     (store_script_param, ":faction_object", 5),
     (assign, ":center_object_lord", -1),
     (assign, ":center_object_faction", -1),
     (assign, ":troop_object_faction", -1),

     (try_begin),
       (party_is_active, ":center_object", 0),
       (party_get_slot, ":center_object_lord", ":center_object", slot_town_lord),
       (store_faction_of_party, ":center_object_faction", ":center_object"),
	 (else_try),
	   (assign, ":center_object_lord", 0),
       (assign, ":center_object_faction", 0),
     (try_end),

     (try_begin),
       (is_between, ":troop_object", 0, "trp_local_merchant"),
       (store_troop_faction, ":troop_object_faction", ":troop_object"),
	 (else_try),
	   (assign, ":troop_object_faction", 0),
     (try_end),

     (val_add, "$num_log_entries", 1),

     (store_current_hours, ":entry_time"),
     (troop_set_slot, "trp_log_array_entry_type",            "$num_log_entries", ":entry_type"),
     (troop_set_slot, "trp_log_array_entry_time",            "$num_log_entries", ":entry_time"),
     (troop_set_slot, "trp_log_array_actor",                 "$num_log_entries", ":actor"),
     (troop_set_slot, "trp_log_array_center_object",         "$num_log_entries", ":center_object"),
     (troop_set_slot, "trp_log_array_center_object_lord",    "$num_log_entries", ":center_object_lord"),
     (troop_set_slot, "trp_log_array_center_object_faction", "$num_log_entries", ":center_object_faction"),
     (troop_set_slot, "trp_log_array_troop_object",          "$num_log_entries", ":troop_object"),
     (troop_set_slot, "trp_log_array_troop_object_faction",  "$num_log_entries", ":troop_object_faction"),
     (troop_set_slot, "trp_log_array_faction_object",        "$num_log_entries", ":faction_object"),

     (try_begin),
       (eq, "$cheat_mode", 1),
       (assign, reg3, "$num_log_entries"),
       (assign, reg4, ":entry_type"),
       (display_message, "@{!}Log entry {reg3}: type {reg4}"),
       (try_begin),
          (gt, ":center_object", 0),
		  (neq, ":entry_type", logent_traveller_attacked),
		  (neq, ":entry_type", logent_party_traded),
		  (party_is_active, ":center_object"), #sometimes is a troop

          (str_store_party_name, s4, ":center_object"),
          (display_message, "@{!}Center: {s4}"),
       (try_end),
       (try_begin),
          (gt, ":troop_object", 0),
		  (neq, ":entry_type", logent_traveller_attacked),
		  (neq, ":entry_type", logent_party_traded),

		  (str_store_troop_name, s4, ":troop_object"),
		  (display_message, "@{!}Troop: {s4}"),
       (try_end),
       (try_begin),
          (gt, ":center_object_lord", 0),
		  (neq, ":entry_type", logent_traveller_attacked),
		  (neq, ":entry_type", logent_party_traded),

		  (str_store_troop_name, s4, ":center_object_lord"),
          (display_message, "@{!}Lord: {s4}"),
       (try_end),
     (try_end),


     (try_begin),
	   (this_or_next|eq, ":entry_type", logent_lord_defeated_by_player),
       (this_or_next|eq, ":entry_type", logent_player_participated_in_major_battle),
		(eq, ":entry_type", logent_player_participated_in_siege),

       (try_begin),
         (eq, "$cheat_mode", 1),
         (display_message, "@{!}Ally party is present"),
       (try_end),
	   ##diplomacy start+ support kingdom ladies as well
       #(try_for_range, ":hero", active_npcs_begin, active_npcs_end),
	   (try_for_range, ":hero", heroes_begin, heroes_end),
	     (this_or_next|is_between, ":hero", active_npcs_begin, active_npcs_end),
	     (this_or_next|troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_hero),
		 (this_or_next|troop_slot_eq, ":hero", slot_troop_occupation, slto_player_companion),
		    (troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_seneschal),
	   ##diplomacy end+
         (party_count_companions_of_type, ":hero_present", "p_collective_friends", ":hero"),
         (gt, ":hero_present", 0),
         (troop_set_slot, ":hero", slot_troop_present_at_event, "$num_log_entries"),
#         (store_sub, ":skip_up_to_here", "$num_log_entries", 1),
#         (troop_set_slot, ":hero", slot_troop_last_comment_slot, ":skip_up_to_here"),
         (try_begin),
           (eq, "$cheat_mode", 1),
           (str_store_troop_name, s4, ":hero"),
           (display_message, "@{!}{s4} is present at event"),
         (try_end),
       (try_end),
     (else_try), #SB : log kingdom policy changes as well
        (eq, ":entry_type", logent_player_renamed_capital),
        (party_clear, "p_temp_party"),
        (call_script, "script_get_heroes_attached_to_center", ":center_object", "p_temp_party"),
        (party_get_num_companion_stacks, ":num_stacks","p_temp_party"),
        (try_for_range, ":stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":hero", "p_temp_party", ":stack"),
          (troop_set_slot, ":hero", slot_troop_present_at_event, "$num_log_entries"), #need to check if this gets called before or after, add +1
        (try_end),
        #they can give their opinion in the feast, although comment strings aren't set up.
     (try_end),
     ])
]
