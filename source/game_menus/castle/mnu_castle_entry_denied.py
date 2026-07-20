# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

castle_entry_denied_menu = [
(
    "castle_entry_denied",mnf_scale_picture,
    "The lord of this castle has forbidden you from coming inside these walls,\
 and the guard sergeant informs you that his men will fire if you attempt to come any closer.",
    "none",
    [
        (call_script, "script_set_town_picture"),
    ],
    [
      ("continue",[],
       "Continue...",
       [(jump_to_menu,"mnu_castle_guard")]),
    ]
  )
]
