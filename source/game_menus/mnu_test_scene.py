# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

test_scene_menu = [
(
    "test_scene",0,
    "You enter the test scene.",
    "none",
    [],
    [

      ("enter",[],"Enter 1.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_multi_scene_1"],[change_screen_mission]]),
      ("enter",[],"Enter 2.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_multi_scene_2"],[change_screen_mission]]),
      ("enter",[],"Enter 3.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_multi_scene_3"],[change_screen_mission]]),
      ("enter",[],"Enter 4.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_multi_scene_4"],[change_screen_mission]]),
      ("enter",[],"Enter 5.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_multi_scene_5"],[change_screen_mission]]),
      ("enter",[],"Enter 6.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_multi_scene_6"],[change_screen_mission]]),
      ("enter",[],"Enter 7.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_test2"],[change_screen_mission]]),
      ("enter",[],"Enter 8.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_test3"],[change_screen_mission]]),
      ("enter",[],"Enter 9.",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_multi_scene_13"],[change_screen_mission]]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
  )
]
