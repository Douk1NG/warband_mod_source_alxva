# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

end_game_menu = [
("end_game",0,
   "The decision is made, and you resolve to give up your adventurer's\
 life and settle down. You sell off your weapons and armour, gather up\
 all your money, and ride off into the sunset....",
   "none",
   [],
    [
      ("end_game_bye",[],"Farewell.",
       [
         (change_screen_quit),
        ]
       ),
      ]
  )
]
