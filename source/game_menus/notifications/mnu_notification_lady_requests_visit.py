# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

notification_lady_requests_visit_menu = [
(
    "notification_lady_requests_visit",0, #add this once around seven days after the last visit, or three weeks, or three months
    "An elderly woman approaches your party and passes one of your men a letter, sealed in plain wax. It is addressed to you. When you break the seal, you see it is from {s15}. It reads, 'I so enjoyed your last visit. {s14} I am currently in {s10}.{s12}'",
    "none",
    [

      (assign, ":lady_no", "$g_notification_menu_var1"),
      (assign, ":center_no", "$g_notification_menu_var2"),

      (str_store_troop_name, s15, ":lady_no"),
      (str_store_party_name, s10, ":center_no"),

      (store_current_hours, ":hours_since_last_visit"),
      (troop_get_slot, ":last_visit_hours", ":lady_no", slot_troop_last_talk_time),
      (val_sub, ":hours_since_last_visit", ":last_visit_hours"),

      (call_script, "script_get_kingdom_lady_social_determinants", ":lady_no"),
      (assign, ":lady_guardian", reg0),

      (str_store_troop_name, s16, ":lady_guardian"),
      (call_script, "script_troop_get_family_relation_to_troop", ":lady_guardian", ":lady_no"),

      (str_clear, s14),
      (try_begin),
        (lt, ":hours_since_last_visit", 336),
        (try_begin),
            (troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_otherworldly),
            (str_store_string, s14, "str_as_brief_as_our_separation_has_been_the_longing_in_my_heart_to_see_you_has_made_it_seem_as_many_years"),
        (else_try),
            (str_store_string, s14, "str_although_it_has_only_been_a_short_time_since_your_departure_but_i_would_be_most_pleased_to_see_you_again"),
        (try_end),
      (else_try),
        (ge, ":hours_since_last_visit", 336),
        (try_begin),
            (troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_ambitious),
            (str_store_string, s14, "str_although_i_have_received_no_word_from_you_for_quite_some_time_i_am_sure_that_you_must_have_been_very_busy_and_that_your_failure_to_come_see_me_in_no_way_indicates_that_your_attentions_to_me_were_insincere_"),
        (else_try),
            (troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_moralist),
            (str_store_string, s14, "str_i_trust_that_you_have_comported_yourself_in_a_manner_becoming_a_gentleman_during_our_long_separation_"),
        (else_try),
            (str_store_string, s14, "str_it_has_been_many_days_since_you_came_and_i_would_very_much_like_to_see_you_again"),
        (try_end),
      (try_end),


      (str_clear, s12),
      (str_clear, s18),
      ##diplomacy start+ Store gender in register for use below
      (assign, ":save_reg4", reg4),
      (call_script, "script_dplmc_store_troop_is_female_reg", ":lady_guardian", 4),
      ##diplomacy end+
      (try_begin),
        (troop_slot_eq, ":lady_guardian", slot_lord_granted_courtship_permission, 0),
        (str_store_string, s12, "str__you_should_ask_my_s11_s16s_permission_but_i_have_no_reason_to_believe_that_he_will_prevent_you_from_coming_to_see_me"),
        (str_store_string, s18, "str__you_should_first_ask_her_s11_s16s_permission"),
      (else_try),
        (troop_slot_eq, ":lady_guardian", slot_lord_granted_courtship_permission, -1),
        (str_store_string, s12, "str__alas_as_we_know_my_s11_s16_will_not_permit_me_to_see_you_however_i_believe_that_i_can_arrange_away_for_you_to_enter_undetected"),
      (else_try),
        (troop_slot_eq, ":lady_guardian", slot_lord_granted_courtship_permission, 1),
        (str_store_string, s12, "str__as_my_s11_s16_has_already_granted_permission_for_you_to_see_me_i_shall_expect_your_imminent_arrival"),
      (try_end),
      ##diplomacy start+ Revert register
      (assign, reg4, ":save_reg4"),
      ##diplomacy end+

      #SB : add tableau for lady
      (set_fixed_point_multiplier, 100),
      (init_position, pos0),
      (position_set_x, pos0, 60),
      (position_set_y, pos0, 20),
      (position_set_z, pos0, 100),
      (set_game_menu_tableau_mesh, "tableau_dplmc_lord_profile", ":lady_no", pos0),
      ],
    [

      ("continue",[],"Tell the woman to inform her mistress that you will come shortly",
       [

        (assign, ":lady_to_visit", "$g_notification_menu_var1"),
        (str_store_troop_name_link, s3, ":lady_to_visit"),
        (str_store_party_name_link, s4, "$g_notification_menu_var2"),

        (str_store_string, s2, "str_visit_s3_who_was_last_at_s4s18"),
        (call_script, "script_start_quest", "qst_visit_lady", ":lady_to_visit"),
        (quest_set_slot, "qst_visit_lady", slot_quest_giver_troop, ":lady_to_visit"), #don't know why this is necessary

        (try_begin),
            (eq, "$cheat_mode", 1),
            (quest_get_slot, ":giver_troop", "qst_visit_lady", slot_quest_giver_troop),
            (str_store_troop_name, s2, ":giver_troop"),
            (display_message, "str_giver_troop_=_s2"),
        (try_end),

        (quest_set_slot, "qst_visit_lady", slot_quest_expiration_days, 30),
        (change_screen_return),
        ]),

      ("continue",[],"Tell the woman to inform her mistress that you are indisposed",
       [
        (troop_set_slot, "$g_notification_menu_var1", slot_lady_no_messages, 1),
        (change_screen_return),
        ]),
     ]
  )
]
