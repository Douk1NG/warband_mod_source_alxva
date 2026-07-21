# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

start_character_2_menu = [
(
    "start_character_2",0,
    "{s10}^^ You started to learn about the world almost as soon as you could walk and talk. You spent your early life as...",
    "none",
    [],
    [
      ("page",[
          ],"A page at a nobleman's court.",[
            (assign,"$background_answer_2", cb2_page),
            (str_store_string,s11,"str_story_childhood_page"),
            (jump_to_menu,"mnu_start_character_3"),
        ]),
      ("apprentice",[
          ],"A craftsman's apprentice.",[
            (assign,"$background_answer_2", cb2_apprentice),
            (str_store_string,s11,"str_story_childhood_apprentice"),
            (jump_to_menu,"mnu_start_character_3"),
        ]),
      ("stockboy",[
          ],"A shop assistant.",[
            (assign,"$background_answer_2",cb2_merchants_helper),
            (str_store_string,s11,"str_story_childhood_stockboy"),
            (jump_to_menu,"mnu_start_character_3"),
        ]),
      ("urchin",[
          ],"A street urchin.",[
            (assign,"$background_answer_2",cb2_urchin),
            (str_store_string,s11,"str_story_childhood_urchin"),
            (jump_to_menu,"mnu_start_character_3"),
        ]),
      ("nomad",[
          ],"A steppe child.",[
            (assign,"$background_answer_2",cb2_steppe_child),
            (str_store_string,s11,"str_story_childhood_nomad"),
            (jump_to_menu,"mnu_start_character_3"),
        ]),

        #SB : standardize strings as prompted
     ("mummer",[],"A mummer.",[
            (assign,"$background_answer_2",dplmc_cb2_mummer),
            (str_store_string,s11,"str_story_childhood_mummer"),
            (jump_to_menu,"mnu_start_character_3"),
        ]),
     ("courtier",[],"A courtier.",[
            (assign,"$background_answer_2",dplmc_cb2_courtier),
            (str_store_string,s11,"str_story_childhood_courtier"),
            (jump_to_menu,"mnu_start_character_3"),
        ]),
        #SB : conditional of parents being noble
     ("noble",[ #"Noble in Training" is vaguely similar to role of courtier/page,
        #we pretend this means you were not fostered but rather educated in-situ
        (eq, "$background_type", cb_noble),
        ],"An unexpected heir.",[
            (assign,"$background_answer_2",dplmc_cb2_noble),
            (str_store_string,s11,"str_story_childhood_noble"),
            (jump_to_menu,"mnu_start_character_3"),
        ]),
     ("acolyte",[],"A cleric acolyte.",[
            (assign,"$background_answer_2",dplmc_cb2_acolyte),
            (str_store_string,s11,"str_story_childhood_acolyte"),
            (jump_to_menu,"mnu_start_character_3"),
        ]),
      ("go_back",[],"Go back.",
     [(jump_to_menu,"mnu_start_character_1"),
    ]),
    ]
  )
]
