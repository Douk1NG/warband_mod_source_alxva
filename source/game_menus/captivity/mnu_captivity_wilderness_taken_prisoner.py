# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

captivity_wilderness_taken_prisoner_menu = [
(
    "captivity_wilderness_taken_prisoner",mnf_scale_picture,
    "Your enemies take you prisoner.",
    "none",
    [
        (set_background_mesh, "mesh_pic_prisoner_wilderness"),
     ],
    [
      ("continue",[],"Continue...",
       [
	     # Explanation of removing below code : heros are already being removed with 50% (was 75%, I decreased it) probability in mnu_total_defeat, why here there is additionally 30% removing of heros?
		 # See codes linked to "mnu_captivity_start_wilderness_surrender" and "mnu_captivity_start_wilderness_defeat" which is connected with here they all also enter
		 # "mnu_total_defeat" and inside the "mnu_total_defeat" there is script_party_remove_all_companions which removes 50% (was 75%, I decreased it) of compainons from player party.

         #(try_for_range, ":npc", companions_begin, companions_end),
         #  (main_party_has_troop, ":npc"),
         #  (store_random_in_range, ":rand", 0, 100),
         #  (lt, ":rand", 30),
         #  (remove_member_from_party, ":npc", "p_main_party"),
         #  (troop_set_slot, ":npc", slot_troop_occupation, 0),
         #  (troop_set_slot, ":npc", slot_troop_playerparty_history, pp_history_scattered),
         #  (assign, "$last_lost_companion", ":npc"),
         #  (store_faction_of_party, ":victorious_faction", "$g_encountered_party"),
         #  (troop_set_slot, ":npc", slot_troop_playerparty_history_string, ":victorious_faction"),
         #  (troop_set_health, ":npc", 100),
         #  (store_random_in_range, ":rand_town", towns_begin, towns_end),
         #  (troop_set_slot, ":npc", slot_troop_cur_center, ":rand_town"),
         #  (assign, ":nearest_town_dist", 1000),
         #  (try_for_range, ":town_no", towns_begin, towns_end),
         #    (store_faction_of_party, ":town_fac", ":town_no"),
         #    (store_relation, ":reln", ":town_fac", "fac_player_faction"),
         #    (ge, ":reln", 0),
         #    (store_distance_to_party_from_party, ":dist", ":town_no", "p_main_party"),
         #    (lt, ":dist", ":nearest_town_dist"),
         #    (assign, ":nearest_town_dist", ":dist"),
         #    (troop_set_slot, ":npc", slot_troop_cur_center, ":town_no"),
         #  (try_end),
         #(try_end),

         # (set_camera_follow_party, "$capturer_party"),
         # (assign, "$g_player_is_captive", 1),
         # (store_random_in_range, ":random_hours", 18, 30),
         # (call_script, "script_event_player_captured_as_prisoner"),
         # (call_script, "script_stay_captive_for_hours", ":random_hours"),
         # (assign,"$auto_menu","mnu_captivity_wilderness_check"),
         # (change_screen_return),


         (assign, "$talk_context", tc_player_defeated),

         (party_stack_get_troop_id, ":capturer_troop", "$capturer_party", 0),
         (party_stack_get_troop_dna, ":capturer_dna", "$capturer_party", 0),
         (party_get_template_id, ":template", "$capturer_party"),
         (store_faction_of_troop, ":troop_faction", ":capturer_troop"),

         (try_begin),
             (eq, "$g_sexual_content", 2),
             (this_or_next|eq, ":template", "pt_deserters"),
             (this_or_next|eq, ":troop_faction", fac_outlaws),
             (this_or_next|eq, ":troop_faction", fac_forest_bandits),
             (this_or_next|eq, ":troop_faction", fac_mountain_bandits),
             (this_or_next|eq, ":troop_faction", fac_black_khergits),
             (this_or_next|eq, ":troop_faction", fac_dark_knights),
             (this_or_next|eq, "$g_encountered_party_faction", fac_outlaws),
             (this_or_next|eq, "$g_encountered_party_faction", fac_forest_bandits),
             (this_or_next|eq, "$g_encountered_party_faction", fac_mountain_bandits),
             (this_or_next|eq, "$g_encountered_party_faction", fac_black_khergits),
             (eq, "$g_encountered_party_faction", fac_dark_knights),
             (call_script, "script_setup_troop_meeting", ":capturer_troop", ":capturer_dna"),
         (else_try),
            (eq, "$g_sexual_content", 2),
            (is_between, ":capturer_troop", heroes_begin, heroes_end),
            (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
            (call_script, "script_setup_troop_meeting", ":capturer_troop", -1),
         (else_try),
             (set_camera_follow_party, "$capturer_party"),
             (assign, "$g_player_is_captive", 1),
             (store_random_in_range, ":random_hours", 18, 30),
             (call_script, "script_event_player_captured_as_prisoner"),
             (call_script, "script_stay_captive_for_hours", ":random_hours"),
             (assign,"$auto_menu","mnu_captivity_wilderness_check"),
             (change_screen_return),
         (try_end),
         ]),
      ]
  )
]
