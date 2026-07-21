# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

start_game_0_menu = [
("start_game_0",menu_text_color(0xFF000000)|mnf_disable_all_keys,
  ##diplomacy begin
    "Welcome, adventurer, to Diplomacy for Mount & Blade: Warband. Before beginning the game you must create your character. Remember that in the traditional medieval society depicted in the game, war and politics are usually dominated by male members of the nobility. That does not however mean that you should not choose to play a female character, or one who is not of noble birth. Male nobles may have a somewhat easier start, but women and commoners can attain all of the same goals -- and in fact may have a much more interesting if more challenging early game.",
  ##diplomacy end
  "none",
    [],
    [
     ("continue",[],"Continue...",
       [
       #SB : randomized quick start
        (try_begin),
          (this_or_next|key_is_down, key_left_shift),
          (key_is_down, key_right_shift),
          (assign, "$g_disable_condescending_comments", 0),
          (store_random_in_range, "$character_gender", tf_male, tf_female + 1),
          (troop_set_type, "trp_player", "$character_gender"),
          (store_random_in_range, "$background_type", cb_noble, cb_priest + 1),
          (store_random_in_range, "$background_answer_2", cb2_page, dplmc_cb2_acolyte + 1),
          (store_random_in_range, "$background_answer_3", dplmc_cb3_bravo, cb3_student + 1),
          (store_random_in_range, "$background_answer_4", cb4_revenge, cb4_greed + 1),
          (str_store_string, s13, "@Perhaps you have forgotten the face of your father."),
          (jump_to_menu, "mnu_choose_skill"),
        (else_try),
          (jump_to_menu, "mnu_start_game_1"),
        (try_end),
        ]
       ),
      ("go_back",[],"Go back",
       [
         (change_screen_quit),
       ]),
    ]
  )
]
