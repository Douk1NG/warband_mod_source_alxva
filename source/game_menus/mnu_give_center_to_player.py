# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

give_center_to_player_menu = [
(
    "give_center_to_player",mnf_scale_picture,
##diplomacy start+ fix gender of pronoun
    "Your lord offers to extend your fiefs!\
 {s1} sends word that {reg4?she:he} is willing to grant {s2} to you in payment for your loyal service,\
 adding it to your holdings. What is your answer?",
##diplomacy end+
    "none",
    [(set_background_mesh, "mesh_pic_messenger"),
     (store_faction_of_party, ":center_faction", "$g_center_to_give_to_player"),
     (faction_get_slot, ":faction_leader", ":center_faction", slot_faction_leader),
     ##diplomacy start+ put king's gender in reg4
     (call_script, "script_dplmc_store_troop_is_female_reg", ":faction_leader", 4),
     ##diplomacy end+
     (str_store_troop_name, s1, ":faction_leader"),
     (str_store_party_name, s2, "$g_center_to_give_to_player"),
    ],
    [
      ("give_center_to_player_accept",[],"Accept the offer.",
       [(call_script, "script_give_center_to_lord", "$g_center_to_give_to_player", "trp_player", 0),
        (jump_to_menu, "mnu_give_center_to_player_2"),
        ]),
      ("give_center_to_player_reject",[],"Reject. You have no interest in holding {s2}.",
       [(party_set_slot, "$g_center_to_give_to_player", slot_town_lord, stl_rejected_by_player),
        (change_screen_return),
        ]),
    ],
  )
]
