# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

village_hunt_down_fugitive_defeated_menu = [
(
    "village_hunt_down_fugitive_defeated",0,
    "A heavy blow from the fugitive sends you to the ground, and your vision spins and goes dark.\
 Time passes. When you open your eyes again you find yourself battered and bloody,\
 but luckily none of the wounds appear to be lethal.",
    "none",
    [
      (call_script, "script_fail_quest", "qst_hunt_down_fugitive"),
    ],
    [
      ("continue",[],"Continue...",[(jump_to_menu, "mnu_village"),
      #SB : renown loss for single target
      (call_script, "script_change_troop_renown", "trp_player", -2),
      # (party_remove_members, "$current_town", "trp_fugitive", 1),
      ]),
    ],
  )
]
