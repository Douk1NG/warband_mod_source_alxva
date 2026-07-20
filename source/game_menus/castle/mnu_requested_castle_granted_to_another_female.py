# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

requested_castle_granted_to_another_female_menu = [
(
    "requested_castle_granted_to_another_female",mnf_scale_picture,
##diplomacy start+ make gender correct
    "You receive a message from your monarch, {s3}.^^\
 'I was most pleased to hear of your valiant efforts in the capture of {s2}. Your victory has gladdened all our hearts.\
 You also requested me to give ownership of the castle to your {wife/husband}, but that is a favor which I fear I cannot grant,\
 as {she/he} already holds significant estates in my realm.\
 Instead I have sent you {reg6} denars to cover the expenses of your campaign, but {s2} I give to {s5}.'\
 ",
##diplomacy end+
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
        (change_screen_return),
        ]),
    ],
)
]
