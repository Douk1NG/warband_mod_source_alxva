# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

training_ground_selection_details_ranged_1_menu = [
("training_ground_selection_details_ranged_1",0,
   "What kind of ranged weapon do you want to train with?",
   "none",
   [
   (set_background_mesh, "mesh_pic_mb_warrior_4"), #SB : background mesh
   ],
    [
      ("camp_train_ranged_weapon_bow",[], "Bow and arrows.",
       [
         (assign, "$g_mt_mode", ctm_ranged),
         (assign, "$temp", itp_type_bow),
         (jump_to_menu, "mnu_training_ground_selection_details_ranged_2"),
         ]),
      ("camp_train_ranged_weapon_crossbow",[], "Crossbow.",
       [
         (assign, "$g_mt_mode", ctm_ranged),
         (assign, "$temp", itp_type_crossbow),
         (jump_to_menu, "mnu_training_ground_selection_details_ranged_2"),
         ]),
      ("camp_train_ranged_weapon_thrown",[], "Throwing Knives.",
       [
         (assign, "$g_mt_mode", ctm_ranged),
         (assign, "$temp", itp_type_thrown),
         (jump_to_menu, "mnu_training_ground_selection_details_ranged_2"),
         ]),
      ("go_back_dot",[],"Go back.",
       [(jump_to_menu, "mnu_training_ground"),
        ]
       ),
      ]
  )
]
