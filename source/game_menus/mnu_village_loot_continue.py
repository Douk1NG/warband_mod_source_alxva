# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

village_loot_continue_menu = [
(
    "village_loot_continue",0,
    "Do you wish to continue looting this village?",
    "none",
    [
    (set_background_mesh, "mesh_pic_looted_village"),
    ],
    [
      ("loot_yes",[],"Yes.",[ (rest_for_hours_interactive, 3, 5, 1), #rest while attackable (3 hours will be extended by the trigger)
                              #SB : resume hostilities
                              (call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$current_town"),
                              (change_screen_return),
                              ]),
      ("loot_no",[],"No.",[(call_script, "script_village_set_state", "$current_town", 0),
                            (party_set_slot, "$current_town", slot_village_raided_by, -1),
                            (assign, "$g_player_raiding_village", 0),
                            (assign, "$g_village_raid_evil", 0), #SB : reset global
                            (party_set_slot, "$current_town", slot_town_last_nearby_fire_time, 0),
                            (change_screen_return)]),
    ],
  )
]
