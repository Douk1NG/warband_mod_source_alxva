# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

training_ground_description_menu = [
("training_ground_description",0,
   "{s0}",
   "none",
   [
   #Sb : format string here instead of script_start_training_at_training_ground
   (store_sub, reg0, "$g_training_ground_training_num_enemies", 1),
   (store_sub, ":string", "$g_mt_mode", 1),
   (val_add, ":string", "str_ctm_melee"),
   (str_store_string, s0, ":string"),

   ],
    [
      ("continue", [], "Continue...",
       [
         (jump_to_scene, "$g_training_ground_training_scene"),
         (change_screen_mission),
        ]
       ),
      ]
  )
]
