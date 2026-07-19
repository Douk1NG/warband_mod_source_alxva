# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

custom_battle_scene_menu = [
(
    "custom_battle_scene",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "(NO_TRANS)",

    "none",
    [],
    [

      ("quick_battle_scene_1",[],"{!}quick_battle_scene_1",
       [
           (set_jump_mission,"mt_ai_training"),
           (jump_to_scene,"scn_quick_battle_scene_1"),(change_screen_mission)
		]
       ),
      ("quick_battle_scene_2",[],"{!}quick_battle_scene_2",
       [
           (set_jump_mission,"mt_ai_training"),
           (jump_to_scene,"scn_quick_battle_scene_2"),(change_screen_mission)
		]
       ),
      ("quick_battle_scene_3",[],"{!}quick_battle_scene_3",
       [
           (set_jump_mission,"mt_ai_training"),
           (jump_to_scene,"scn_quick_battle_scene_3"),(change_screen_mission)
		]
       ),
      ("quick_battle_scene_4",[],"{!}quick_battle_scene_4",
       [
           (set_jump_mission,"mt_ai_training"),
           (jump_to_scene,"scn_quick_battle_scene_4"),(change_screen_mission)
		]
       ),
      ("quick_battle_scene_5",[],"{!}quick_battle_scene_5",
       [
           (set_jump_mission,"mt_ai_training"),
           (jump_to_scene,"scn_quick_battle_scene_5"),(change_screen_mission)
		]
       ),

      ("go_back",[],"{!}Go back",
       [(change_screen_quit),
        ]
       ),
      ]
  )
]
