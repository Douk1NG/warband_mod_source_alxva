# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

invite_player_to_faction_accepted_menu = [
(
    "invite_player_to_faction_accepted",0,
##diplomacy start+ fix gender of pronouns (king's gender should already be in reg4)
    "In order to become a vassal, you must swear an oath of homage to {s3}.\
 You shall have to find {reg4?her:him} and give {reg4?her:him} your oath in person. {s5}",
##diplomacy end+
    "none",
    [
        (call_script, "script_get_information_about_troops_position", "$g_invite_faction_lord", 0),
        (str_store_troop_name, s3, "$g_invite_faction_lord"),
        (str_store_string, s5, "@{!}{s1}"),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  )
]
