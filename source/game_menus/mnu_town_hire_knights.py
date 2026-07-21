# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

town_hire_knights_menu = [
(
    "town_hire_knights",0,
    "Wearing shiny armour and swords ready to cut through flesh, they stand in front of you with their honour held high(as long as you pay them.).. 1000 denars each knight.",
    "none",
    [],
    [

              ("swadian_knight1",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",1000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],

       "1 Swadian Knight.",
       [
           (party_add_members, "p_main_party", "trp_swadian_knight", 1),
           (troop_remove_gold, "trp_player", 1000),
        ]),
                       ("swadian_knight5",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",5000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "5 Swadian Knights.",
       [
           (party_add_members, "p_main_party", "trp_swadian_knight", 5),
           (troop_remove_gold, "trp_player", 5000),
        ]),
                       ("swadian_knight10",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",10000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "10 Swadian Knights.",
       [
           (party_add_members, "p_main_party", "trp_swadian_knight", 10),
           (troop_remove_gold, "trp_player", 10000),
        ]),
                      ("vaegir_knight1",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",1000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Vaegir Knights.",
       [
           (party_add_members, "p_main_party", "trp_Vaegir_knight", 1),
           (troop_remove_gold, "trp_player", 1000),
        ]),
                      ("vaegir_knight5",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",5000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "5 Vaegir Knights.",
       [
           (party_add_members, "p_main_party", "trp_vaegir_knight", 5),
           (troop_remove_gold, "trp_player", 5000),
        ]),
                      ("vaegir_knight10",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",10000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "10 Vaegir Knights.",
       [
           (party_add_members, "p_main_party", "trp_vaegir_knight", 10),
           (troop_remove_gold, "trp_player", 10000),
        ]),
      ("back_to_town_hire_troops",[],"Go back..",
       [
           (jump_to_menu,"mnu_town_hire_troops"),
        ]),
        ]
  )
]
