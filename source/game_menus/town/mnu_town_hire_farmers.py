# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

town_hire_farmers_menu = [
(
    "town_hire_farmers",0,
    "Their clothing is tattered and their pockets are empty, but their bravery has no boundaries. They have been driven out of their lands for different reasons and their husbands have been killed in the wars, and now the only way for these women make a living is to join a mercenary band. 100 denars each refugee.",
    "none",
    [],
    [
      ("farmer1",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",100),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Farmer.",
       [
           (party_add_members, "p_main_party", "trp_farmer", 1),
           (troop_remove_gold, "$g_player_troop", 100),
        ]),
("farmer5",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",500),
                 (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                 (ge, ":free_capacity",5),
],"5 Farmers.",
       [
           (party_add_members, "p_main_party", "trp_refugee", 5),
           (troop_remove_gold, "$g_player_troop", 500),
        ]),
("farmer10",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",1000),
                 (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                 (ge, ":free_capacity",5),
],"10 Farmers.",
       [
           (party_add_members, "p_main_party", "trp_refugee", 10),
           (troop_remove_gold, "$g_player_troop", 1000),
        ]),
      ("back_to_town_hire_troops",[],"Go back..",
       [
           (jump_to_menu,"mnu_town_hire_troops"),
        ]),
    ]
  )
]
