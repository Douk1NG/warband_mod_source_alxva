# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

kingdom_army_quest_messenger_menu = [
(
##diplomacy start+ fix gender of pronouns
    "kingdom_army_quest_messenger",mnf_scale_picture,
    "{s8} sends word that {reg4?she:he} wishes to speak with you about a task {reg4?she:he} needs performed.\
 {reg4?She:He} requests you to come and see {reg4?her:him} as soon as possible.",
##diplomacy end+
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        ##diplomacy start+ put marshall's gender in reg4
        (call_script, "script_dplmc_store_troop_is_female", ":faction_marshall"),
        (assign, reg4, reg0),
        ##diplomacy end+
        (str_store_troop_name, s8, ":faction_marshall"),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  )
]
