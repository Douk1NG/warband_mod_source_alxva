# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

battlefields_menu = [
(
    "battlefields",0,
    "{!}Select a field...",
    "none",
    [],
    [

      ("enter_f1",[],"{!}Field 1",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_1"],[change_screen_mission]]),
      ("enter_f2",[],"{!}Field 2",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_2"],[change_screen_mission]]),
      ("enter_f3",[],"{!}Field 3",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_3"],[change_screen_mission]]),
      ("enter_f4",[],"{!}Field 4",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_4"],[change_screen_mission]]),
      ("enter_f5",[],"{!}Field 5",[[set_jump_mission,"mt_ai_training"],[jump_to_scene,"scn_field_5"],[change_screen_mission]]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
  )
]
