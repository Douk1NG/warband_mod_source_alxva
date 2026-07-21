# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

start_character_4_menu = [
(
    "start_character_4",mnf_disable_all_keys,
    "Though the distinction felt sudden to you, somewhere along the way you had become a {reg11?woman:man}, and the whole world seemed to change around you.\
 {s12}^^But soon everything changed and you decided to strike out on your own as an adventurer. What made you take this decision was...",
    #Finally, what made you decide to strike out on your own as an adventurer?",
    "none",
    [],
    [
      ("revenge",[],"Personal revenge.",[
        (assign,"$background_answer_4", cb4_revenge),
        (str_store_string,s13,"str_story_reason_revenge"),
        (jump_to_menu,"mnu_choose_skill"),
        ]),
      ("death",[],"The loss of a loved one.",[
        (assign,"$background_answer_4",cb4_loss),
        (str_store_string,s13,"str_story_reason_death"),
        (jump_to_menu,"mnu_choose_skill"),
        ]),
      ("wanderlust",[],"Wanderlust.",[
        (assign,"$background_answer_4",cb4_wanderlust),
        (str_store_string,s13,"str_story_reason_wanderlust"),
        (jump_to_menu,"mnu_choose_skill"),
        ]),
        #SB : condition of at least one priestly background
     ("fervor",[
        (this_or_next|eq, "$background_type", cb_priest),
        (eq, "$background_answer_2", dplmc_cb2_acolyte),
     ],"Religious fervor.",[
        (assign,"$background_answer_4",dplmc_cb4_fervor),
        (str_store_string,s13,"str_story_reason_fervor"),
        (jump_to_menu,"mnu_choose_skill"),
       ]),
      ("disown",[],"Being forced out of your home.",[
        (assign,"$background_answer_4",cb4_disown),
        (str_store_string,s13,"str_story_reason_disown"),
        (jump_to_menu,"mnu_choose_skill"),
        ]),
     ("greed",[],"Lust for money and power.",[
        (assign,"$background_answer_4",cb4_greed),
        (str_store_string,s13,"str_story_reason_greed"),
        (jump_to_menu,"mnu_choose_skill"),
        ]),
      ("go_back",[],"Go back.",
       [(jump_to_menu,"mnu_start_character_3"),
        ]
       ),
    ]
  )
]
