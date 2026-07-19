# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

start_phase_4_menu = [
("start_phase_4",mnf_disable_all_keys,
    "{s11}",
    "none",
    [
      (assign, ":continue", 1),
      (try_begin),
        (eq, "$current_startup_quest_phase", 2),
        (change_screen_return),
        (assign, ":continue", 0),
      (else_try),
        (eq, "$current_startup_quest_phase", 3),
        (str_store_string, s11, "str_merchant_and_you_call_some_townsmen_and_guards_to_get_ready_and_you_get_out_from_tavern"),
      (else_try),
        (eq, "$current_startup_quest_phase", 4),
        (try_begin),
          (eq, "$g_killed_first_bandit", 1),
          (str_store_string, s11, "str_town_fight_ended_you_and_citizens_cleaned_town_from_bandits"),
        (else_try),
          (str_store_string, s11, "str_town_fight_ended_you_and_citizens_cleaned_town_from_bandits_you_wounded"),
        (try_end),
      (try_end),

      (eq, ":continue", 1),
    ],
    [
      ("continue",
      [
        (this_or_next|eq, "$current_startup_quest_phase", 1),
        (eq, "$current_startup_quest_phase", 4),
      ],
      "Continue...",
      [
        (assign, "$town_entered", 1),

        (try_begin),
          (eq, "$current_town", "p_town_1"),
          (assign, ":town_merchant", "trp_nord_merchant"),
          (assign, ":town_room_scene", "scn_town_1_room"),
        (else_try),
          (eq, "$current_town", "p_town_5"),
          (assign, ":town_merchant", "trp_rhodok_merchant"),
          (assign, ":town_room_scene", "scn_town_5_room"),
        (else_try),
          (eq, "$current_town", "p_town_6"),
          (assign, ":town_merchant", "trp_swadian_merchant"),
          (assign, ":town_room_scene", "scn_town_6_room"),
        (else_try),
          (eq, "$current_town", "p_town_8"),
          (assign, ":town_merchant", "trp_vaegir_merchant"),
          (assign, ":town_room_scene", "scn_town_8_room"),
        (else_try),
          (eq, "$current_town", "p_town_10"),
          (assign, ":town_merchant", "trp_khergit_merchant"),
          (assign, ":town_room_scene", "scn_town_10_room"),
        (else_try),
          (eq, "$current_town", "p_town_19"),
          (assign, ":town_merchant", "trp_sarranid_merchant"),
          (assign, ":town_room_scene", "scn_town_19_room"),
        (try_end),

        (modify_visitors_at_site, ":town_room_scene"),
        (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (set_visitor, 9, ":town_merchant"),

        (assign, "$talk_context", tc_merchants_house),

        (assign, "$dialog_with_merchant_ended", 0),

        (set_jump_mission, "mt_meeting_merchant"),

        (jump_to_scene, ":town_room_scene"),
        (change_screen_mission),
      ]),

      ("continue",
      [
        (eq, "$current_startup_quest_phase", 3),
      ],
      "Continue...",
      [
        (call_script, "script_prepare_town_to_fight"),
      ]),
    ]
  )
]
