# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

requested_castle_granted_to_another_menu = [
(
    "requested_castle_granted_to_another",mnf_scale_picture,
    "You receive a message from your monarch, {s3}.^^\
 'I was most pleased to hear of your valiant efforts in the capture of {s2}. Your victory has gladdened all our hearts.\
 You also requested me to give you ownership of the castle, but that is a favor which I fear I cannot grant,\
 as you already hold significant estates in my realm.\
 Instead I have sent you {reg6} denars to cover the expenses of your campaign, but {s2} I give to {s5}.'\
 ",
    "none",
    [(set_background_mesh, "mesh_pic_messenger"),
     (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
     (str_store_troop_name, s3, ":faction_leader"),
     (str_store_party_name, s2, "$g_center_to_give_to_player"),
     (party_get_slot, ":new_owner", "$g_center_to_give_to_player", slot_town_lord),
     (str_store_troop_name, s5, ":new_owner"),
     (assign, reg6, 900),

	 (assign, "$g_castle_requested_by_player", -1),
	 (assign, "$g_castle_requested_for_troop", -1),

    ],
    [
      ("accept_decision",[],"Accept the decision.",
       [
       (call_script, "script_troop_add_gold", "trp_player", reg6),
        ##diplomacy start+ Remove gold spent by liege
        (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
        (try_begin),
            (gt, ":faction_leader", 0),
            (neq, ":faction_leader", "trp_kingdom_heroes_including_player_begin"),
            (call_script, "script_dplmc_remove_gold_from_lord_and_holdings", reg6, ":faction_leader"),
        (try_end),
        ##diplomacy end+
       (change_screen_return),
       ]),

       ("leave_faction",[],"You have been wronged! Renounce your oath to your liege! ",
       [
         ##diplomacy start+ Remove gold spent by liege
         (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
         (try_begin),
            (gt, ":faction_leader", 0),
            (neq, ":faction_leader", "trp_kingdom_heroes_including_player_begin"),
            (call_script, "script_dplmc_remove_gold_from_lord_and_holdings", reg6, ":faction_leader"),
         (try_end),
         ##diplomacy end+
         (jump_to_menu, "mnu_leave_faction"),
         (call_script, "script_troop_add_gold", "trp_player", reg6),
        ]),
     ],
  )
]
