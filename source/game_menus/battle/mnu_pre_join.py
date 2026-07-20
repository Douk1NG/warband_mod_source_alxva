# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

pre_join_menu = [
(
    "pre_join",0,
    "You come across a battle between {s2} and {s1}. You decide to...",
    "none",
    [
        (str_store_party_name, 1,"$g_encountered_party"),
        (str_store_party_name, 2,"$g_encountered_party_2"),
      ],
    [
      ("pre_join_help_attackers",[
         # (store_faction_of_party, ":attacker_faction", "$g_encountered_party_2"),
         # (store_relation, ":attacker_relation", ":attacker_faction", "fac_player_supporters_faction"),
          #(store_faction_of_party, ":defender_faction", "$g_encountered_party"),
          #(store_relation, ":defender_relation", ":defender_faction", "fac_player_supporters_faction"),
         # (ge, ":attacker_relation", 0),
         # (lt, ":defender_relation", 0),
          ],
          "Move in to help the {s2}.",[
              (select_enemy,0),
              (assign,"$g_enemy_party","$g_encountered_party"),
              (assign,"$g_ally_party","$g_encountered_party_2"),
              (jump_to_menu,"mnu_join_battle")]),
      ("pre_join_help_defenders",[
          #(store_faction_of_party, ":attacker_faction", "$g_encountered_party_2"),
          #(store_relation, ":attacker_relation", ":attacker_faction", "fac_player_supporters_faction"),
          #(store_faction_of_party, ":defender_faction", "$g_encountered_party"),
          #(store_relation, ":defender_relation", ":defender_faction", "fac_player_supporters_faction"),
          #(ge, ":defender_relation", 0),
          #(lt, ":attacker_relation", 0),
          ],
          "Rush to the aid of the {s1}.",[
              (select_enemy,1),
              (assign,"$g_enemy_party","$g_encountered_party_2"),
              (assign,"$g_ally_party","$g_encountered_party"),
              (jump_to_menu,"mnu_join_battle")]),
      ("pre_join_leave",[],"Don't get involved.",[(leave_encounter),(change_screen_return)]),
    ]
  )
]
