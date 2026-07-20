# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

leave_faction_menu = [
(
    "leave_faction",0,
    "Renouncing your oath is a grave act. Your lord may condemn you and confiscate your lands and holdings.\
 However, if you return them of your own free will, he may let the betrayal go without a fight.",
    "none",
    [
    ],
    [
      ("leave_faction_give_back", [], "Renounce your oath and give up your holdings.",
       [
#Troop commentary changes begin
#        (call_script, "script_add_log_entry", logent_renounced_allegiance,   "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction"),
#Troop commentary changes end
        (call_script, "script_player_leave_faction", 1), #1 means give back fiefs
        (change_screen_return),
        ]),
      ("leave_faction_hold", [
          (str_store_party_name, s2, "$g_center_to_give_to_player"),
          ], "Renounce your oath and rule your lands, including {s2}, in your own name.",
       [
        (call_script, "script_give_center_to_lord", "$g_center_to_give_to_player", "trp_player", 0), #this should activate the player faction (it does not)
        (call_script, "script_player_leave_faction", 0), #"1" would mean give back fiefs
		(call_script, "script_activate_player_faction", "trp_player"), #Activating player faction should now work
        (change_screen_return),
        ]),
      ("leave_faction_cancel", [], "Remain loyal and accept the decision.",
       [
        (change_screen_return),
        ]),
    ],
  )
]
