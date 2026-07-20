# ======================================================================
# SHARED DEPENDENCY
# Entity: get_information_about_troops_position (script)
# Called by menus in 2 domains: diplomacy, kingdom_management
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

get_information_about_troops_position_scripts = [
("get_information_about_troops_position",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, reg3),
	  ##diplomacy start+
	  #(troop_get_type, reg4, ":troop_no"),
     (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 4),
	  ##diplomacy end+
      (str_store_troop_name, s2, ":troop_no"),

      (assign, ":found", 0),
      (troop_get_slot, ":center_no", ":troop_no", slot_troop_cur_center),
      (try_begin),
        (gt, ":center_no", 0),
        (is_between, ":center_no", centers_begin, centers_end),
        (str_store_party_name_link, s3, ":center_no"),
        (str_store_string, s1, "@{s2} {reg3?was:is currently} at {s3}."),
        (assign, ":found", 1),
      (else_try),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (gt, ":party_no", 0),
        (call_script, "script_get_troop_attached_party", ":troop_no"),
        (assign, ":center_no", reg0),
        (try_begin),
          (is_between, ":center_no", centers_begin, centers_end),
          (str_store_party_name_link, s3, ":center_no"),
          (str_store_string, s1, "@{s2} {reg3?was:is currently} at {s3}."),
          (assign, ":found", 1),
        (else_try),
          (get_party_ai_behavior, ":ai_behavior", ":party_no"),
          (eq, ":ai_behavior", ai_bhvr_travel_to_party),
          (get_party_ai_object, ":ai_object", ":party_no"),
          (is_between, ":ai_object", centers_begin, centers_end),
		  ##diplomacy start+
		  #(call_script, "script_get_closest_center", ":party_no"),
		  (call_script, "script_dplmc_get_closest_center_or_two", ":party_no"),
		  ##diplomacy end+
          (str_store_party_name_link, s4, reg0),
          (str_store_party_name_link, s3, ":ai_object"),
          (str_store_string, s1, "@{s2} {reg3?was:is} travelling to {s3} and {reg4?she:he} {reg3?was:should be} close to {s4}{reg3?: at the moment}."),
          (assign, ":found", 1),
		  ##diplomacy start+
		  (try_begin),
		     (gt, reg1, -1),
			 (str_store_party_name_link, s1, reg1),
			 (str_store_string, s1, "@{s2} {reg3?was:is} travelling to {s3} and {reg4?she:he} {reg3?was:should be} between {s4} and {s1}{reg3?: at the moment}."),
		  (try_end),
		  ##diplomacy end+
        (else_try),
		  ##diplomacy start+
		  #(call_script, "script_get_closest_center", ":party_no"),
		  (call_script, "script_dplmc_get_closest_center_or_two", ":party_no"),
		  ##diplomacy end+
          (str_store_party_name_link, s3, reg0),
          (str_store_string, s1, "@{s2} {reg3?was:is} in the field and {reg4?she:he} {reg3?was:should be} close to {s3}{reg3?: at the moment}."),
          (assign, ":found", 1),
		  ##diplomacy start+
		  (try_begin),
		     (gt, reg1, -1),
			 (str_store_party_name_link, s1, reg1),
			 (str_store_string, s1, "@{s2} {reg3?was:is} in the field and {reg4?she:he} {reg3?was:should be} between {s3} and {s1}{reg3?: at the moment}."),
		  (try_end),
		  ##diplomacy end+
        (try_end),
      (else_try),
        #(troop_slot_ge, ":troop_no", slot_troop_is_prisoner, 1),
        (troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
          (party_count_prisoners_of_type, ":num_prisoners", ":center_no", ":troop_no"),
          (gt, ":num_prisoners", 0),
          (assign, ":found", 1),
          (str_store_party_name_link, s3, ":center_no"),
          (str_store_string, s1, "@{s2} {reg3?was:is} being held captive at {s3}."),
        (try_end),
        (try_begin),
          (eq, ":found", 0),
          (str_store_string, s1, "@{s2} {reg3?was:has been} taken captive by {reg4?her:his} enemies."),
          (assign, ":found", 1),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":found", 0),
        (str_store_string, s1, "@{reg3?{s2}'s location was unknown:I don't know where {s2} is}."),
      (try_end),
      (assign, reg0, ":found"),
  ])
]
