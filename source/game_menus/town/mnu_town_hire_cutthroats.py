# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

town_hire_cutthroats_menu = [
(
    "town_hire_cutthroats",0,
    "Vile and vicious people with rotten theeth glares at you whilst you question their value and usefulness in your party. 150 for each Looter, 700 for each Nord archer, 300 for each bandit and 500 for each Brigand.",
    "none",
    [],
    [
      ("looter1",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",150),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Looter.",
       [
           (party_add_members, "p_main_party", "trp_looter", 1),
           (troop_remove_gold, "trp_player", 150),
        ]),
      ("looter5",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",750),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "5 Looters.",
       [
           (party_add_members, "p_main_party", "trp_looter", 5),
           (troop_remove_gold, "trp_player", 750),
        ]),
      ("looter10",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",1500),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "10 Looters.",
       [
           (party_add_members, "p_main_party", "trp_looter", 10),
           (troop_remove_gold, "trp_player", 1500),
        ]),
            ("bandit1",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",300),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Bandit.",
       [
           (party_add_members, "p_main_party", "trp_bandit", 1),
           (troop_remove_gold, "trp_player", 300),
        ]),
            ("bandit5",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",1500),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Bandits.",
       [
           (party_add_members, "p_main_party", "trp_bandit", 5),
           (troop_remove_gold, "trp_player", 1500),
        ]),
        ("bandit10",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",3000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Bandits.",
       [
           (party_add_members, "p_main_party", "trp_bandit", 10),
           (troop_remove_gold, "trp_player", 3000),
        ]),
              ("brigand1",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",500),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Brigand.",
       [
           (party_add_members, "p_main_party", "trp_brigand", 1),
           (troop_remove_gold, "trp_player", 500),
        ]),
                    ("brigand5",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",2500),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Brigands.",
       [
           (party_add_members, "p_main_party", "trp_brigand", 5),
           (troop_remove_gold, "trp_player", 2500),
        ]),
                    ("brigand10",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",5000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "10 Brigands.",
       [
           (party_add_members, "p_main_party", "trp_brigand", 10),
           (troop_remove_gold, "trp_player", 5000),
        ]),
                      ("nord_archer",[(store_troop_gold,":total_money","trp_player"),(ge, ":total_money",7000),
                       (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
                       (ge, ":free_capacity",1),
],
       "1 Nord Archers.",
       [
           (party_add_members, "p_main_party", "trp_nord_archer", 10),
           (troop_remove_gold, "trp_player", 7000),
        ]),
      ("back_to_town_hire_troops",[],"Go back..",
       [
           (jump_to_menu,"mnu_town_hire_troops"),
        ]),
        ]
  )
]
