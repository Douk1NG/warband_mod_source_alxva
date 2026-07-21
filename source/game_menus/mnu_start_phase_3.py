# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

start_phase_3_menu = [
("start_phase_3",mnf_disable_all_keys,
    "{s16}^^You are exhausted by the time you find the inn in {s1}, and fall asleep quickly. However, you awake before dawn and are eager to explore your surroundings. You venture out onto the streets, which are still deserted. All of a sudden, you hear a sound that stands the hairs of your neck on end -- the rasp of a blade sliding from its scabbard...",
    "none",
    [
      (assign, ":continue", 1),
      (try_begin),
        (eq, "$current_startup_quest_phase", 1),
        (try_begin),
          (eq, "$g_killed_first_bandit", 1),
          (str_store_string, s11, "str_killed_bandit_at_alley_fight"),
        (else_try),
          (str_store_string, s11, "str_wounded_by_bandit_at_alley_fight"),
        (try_end),
        (jump_to_menu, "mnu_start_phase_4"),
        (assign, ":continue", 0),
      (else_try),
        (eq, "$current_startup_quest_phase", 3),
        (try_begin),
          (eq, "$g_killed_first_bandit", 1),
          (str_store_string, s11, "str_killed_bandit_at_alley_fight"),
        (else_try),
          (str_store_string, s11, "str_wounded_by_bandit_at_alley_fight"),
        (try_end),
        (jump_to_menu, "mnu_start_phase_4"),
        (assign, ":continue", 0),
      (try_end),

      (str_store_party_name, s1, "$g_starting_town"),
      (str_clear, s16),
      (eq, ":continue", 1),

    ],
    [

      ("continue",[], "Continue...",
       [
         (assign, "$g_starting_town", "$current_town"),
         # (call_script, "script_player_arrived"),
         # (party_set_morale, "p_main_party", 100), #SB : roll this into previous script
         (set_encountered_party, "$current_town"),
         #SB : play sound
         (play_sound, "snd_draw_sword"),
         (call_script, "script_prepare_alley_to_fight"),
       ]),
    ]
  )
]
