# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

start_character_3_menu = [
(
    "start_character_3",mnf_disable_all_keys,
    "As a {reg11?girl:boy} growing out of childhood, {s11}^^ Then, as a young adult, life changed as it always does. You became...",
    "none",
    [],
    [
    #SB : maybe restrict these two by gender like squire?
     ("bravo",[],"A travelling bravo.",[
       (assign,"$background_answer_3",dplmc_cb3_bravo),
     (str_store_string,s12,"str_story_job_bravo"),
	(jump_to_menu,"mnu_start_character_4"),
       ]),
     ("merc",[],"A sellsword in foreign lands.",[
       (assign,"$background_answer_3",dplmc_cb3_merc),
     (str_store_string,s12,"str_story_job_merc"),
	(jump_to_menu,"mnu_start_character_4"),
       ]),

      ("squire",[(eq,"$character_gender",tf_male)],"A squire.",[
        (assign,"$background_answer_3",cb3_squire),
      (str_store_string,s12,"str_story_job_squire"),
	(jump_to_menu,"mnu_start_character_4"),
        ]),
      ("lady",[(eq,"$character_gender",tf_female)],"A lady-in-waiting.",[
        (assign,"$background_answer_3",cb3_lady_in_waiting),
      (str_store_string,s12,"str_story_job_lady"),
	(jump_to_menu,"mnu_start_character_4"),
        ]),
      ("troubadour",[],"A troubadour.",[
        (assign,"$background_answer_3",cb3_troubadour),
      (str_store_string,s12,"str_story_job_troubadour"),
	(jump_to_menu,"mnu_start_character_4"),
        ]),
      ("student",[],"A university student.",[
        (assign,"$background_answer_3",cb3_student),
      (str_store_string,s12,"str_story_job_student"),
	(jump_to_menu,"mnu_start_character_4"),
        ]),
      ("peddler",[],"A goods peddler.",[
        (assign,"$background_answer_3",cb3_peddler),
      (str_store_string,s12,"str_story_job_peddler"),
	(jump_to_menu,"mnu_start_character_4"),
        ]),
      ("craftsman",[],"A smith.",[
        (assign,"$background_answer_3", cb3_craftsman),
      (str_store_string,s12,"str_story_job_craftsman"),
	(jump_to_menu,"mnu_start_character_4"),
        ]),
      ("poacher",[],"A game poacher.",[
        (assign,"$background_answer_3", cb3_poacher),
      (str_store_string,s12,"str_story_job_poacher"),
	(jump_to_menu,"mnu_start_character_4"),
        ]),
     ("preacher",[],"An itinerant preacher.",[
       (assign,"$background_answer_3", dplmc_cb3_preacher),
     (str_store_string,s12,"str_story_job_preacher"),
	(jump_to_menu,"mnu_start_character_4"),
       ]),
      ("go_back",[],"Go back.",
       [(jump_to_menu,"mnu_start_character_2"),
        ]
       ),
    ]
  )
]
