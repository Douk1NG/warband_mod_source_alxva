# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

oath_fulfilled_menu = [
(
    "oath_fulfilled",0,
##diplomacy start+ fix gender of pronoun
    "You had a contract with {s1} to serve {reg4?her:him} for a certain duration.\
 Your contract has now expired. What will you do?",
##diplomacy end+
    "none",
    [
      (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
      ##diplomacy start+ load king's gender into reg4
      (call_script, "script_dplmc_store_troop_is_female", ":faction_leader"),
      (assign, reg4, reg0),
      ##diplomacy end+
      (str_store_troop_name, s1, ":faction_leader"),
     ],
    [
      ("renew_oath",[(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
                     (str_store_troop_name, s1, ":faction_leader")], "Renew your contract with {s1} for another month.",
       [
         (store_current_day, ":cur_day"),
         (store_add, "$mercenary_service_next_renew_day", ":cur_day", 30),
         (change_screen_return),
         ]),
      ("dont_renew_oath",[],"Become free of your bond.",
       [
         (call_script, "script_player_leave_faction", 1), #1 means give back fiefs
         (change_screen_return),
         ]),
    ]
  )
]
