# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

village_take_food_confirm_menu = [
(
    "village_take_food_confirm",0,
    "It will be difficult to force and threaten the peasants into giving their precious supplies. You think you will need at least one hour.",
    #TODO: mention looting skill?
    "none",
    [],
    [
      ("village_take_food_confirm",[],"Go ahead.",
       [
         (rest_for_hours_interactive, 1, 5, 0), #rest while not attackable
         (assign, "$auto_enter_town", "$current_town"),
         (assign, "$g_town_visit_after_rest", 1),
         (assign, "$auto_enter_menu_in_center", "mnu_village_take_food"),
         (change_screen_return),
         ]),
      ("forget_it",[],"Forget it.",[(jump_to_menu, "mnu_village_hostile_action")]),
    ],
  )
]
