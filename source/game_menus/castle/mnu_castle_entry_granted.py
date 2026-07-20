# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

castle_entry_granted_menu = [
(
    "castle_entry_granted",mnf_scale_picture,
    "After a brief wait, the guards open the gates for you and allow your party inside.",
    "none",
    [
        (call_script, "script_set_town_picture"),
    ],
    [
      ("continue",[],
       "Continue...",
       [(jump_to_menu,"mnu_town")]),
    ]
  )
]
