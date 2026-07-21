# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

village_loot_defeat_menu = [
(
    "village_loot_defeat",mnf_scale_picture,
    "Fighting with courage and determination, the villagers manage to hold together and drive off your forces.",
    "none",
    [
        (set_background_mesh, "mesh_pic_villageriot"),
    ],
    [
      ("continue",[],"Continue...",[(change_screen_return),
      #SB : renown loss
      (call_script, "script_change_troop_renown", "trp_player", -3),
      ]),
    ],
  )
]
