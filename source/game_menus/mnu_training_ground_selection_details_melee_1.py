# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

training_ground_selection_details_melee_1_menu = [
("training_ground_selection_details_melee_1",0,
   "How many opponents will you go against?",
   "none",
   [
     (call_script, "script_write_fit_party_members_to_stack_selection", "p_main_party", 1),
     (troop_get_slot, "$temp", "trp_stack_selection_amounts", 1), #number of men fit
     (assign, "$temp_2", 1),
     ],
    [
      ("camp_train_melee_num_men_1",[(ge, "$temp", 1)], "One.",
       [
         (assign, "$temp", 1),
         (jump_to_menu, "mnu_training_ground_selection_details_melee_2"),
         ]),
      ("camp_train_melee_num_men_2",[(ge, "$temp", 2)], "Two.",
       [
         (assign, "$temp", 2),
         (jump_to_menu, "mnu_training_ground_selection_details_melee_2"),
         ]),
      ("camp_train_melee_num_men_3",[(ge, "$temp", 3)], "Three.",
       [
         (assign, "$temp", 3),
         (jump_to_menu, "mnu_training_ground_selection_details_melee_2"),
         ]),
      ("camp_train_melee_num_men_4",[(ge, "$temp", 4)], "Four.",
       [
         (assign, "$temp", 4),
         (jump_to_menu, "mnu_training_ground_selection_details_melee_2"),
         ]),
      ("go_back_dot",[],"Cancel.",
       [
         (jump_to_menu, "mnu_training_ground"),
        ]),
      ]
  )
]
