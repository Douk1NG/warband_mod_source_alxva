# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

cheat_change_weather_menu = [
("cheat_change_weather",0,
   "{!}Current cloud amount: {reg5}^Current Fog Strength: {reg6}",
   "none",
   [
     (get_global_cloud_amount, reg5),
     (get_global_haze_amount, reg6),
     ],
    [
      ("cheat_increase_cloud",[], "{!}Increase Cloud Amount.",
       [
	    (get_global_cloud_amount, ":cur_cloud_amount"),
		(val_add, ":cur_cloud_amount", 5),
		(val_min, ":cur_cloud_amount", 100),
	    (set_global_cloud_amount, ":cur_cloud_amount"),
	   ]
       ),
      ("cheat_decrease_cloud",[], "{!}Decrease Cloud Amount.",
       [
	    (get_global_cloud_amount, ":cur_cloud_amount"),
		(val_sub, ":cur_cloud_amount", 5),
		(val_max, ":cur_cloud_amount", 0),
	    (set_global_cloud_amount, ":cur_cloud_amount"),
	   ]
       ),
      ("cheat_increase_fog",[], "{!}Increase Fog Amount.",
       [
	    (get_global_haze_amount, ":cur_fog_amount"),
		(val_add, ":cur_fog_amount", 5),
		(val_min, ":cur_fog_amount", 100),
	    (set_global_haze_amount, ":cur_fog_amount"),
	   ]
       ),
      ("cheat_decrease_fog",[], "{!}Decrease Fog Amount.",
       [
	    (get_global_haze_amount, ":cur_fog_amount"),
		(val_sub, ":cur_fog_amount", 5),
		(val_max, ":cur_fog_amount", 0),
	    (set_global_haze_amount, ":cur_fog_amount"),
	   ]
       ),

      ("camp_action_4",[],"{!}Back to camp menu.",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  )
]
