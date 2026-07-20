# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

kingdom_army_follow_failed_menu = [
(
    "kingdom_army_follow_failed",mnf_scale_picture,
    "You have failed to follow {s8}. The marshal assumes that you were otherwise engaged, but would have appreciated your support.",
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (str_store_troop_name, s8, ":faction_marshall"),
        (call_script, "script_abort_quest", "qst_follow_army", 1),
#        (call_script, "script_change_player_relation_with_troop", ":faction_marshall", -3),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  )
]
