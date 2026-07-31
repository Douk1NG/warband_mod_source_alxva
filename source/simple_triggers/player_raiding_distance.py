# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *

player_raiding_distance_simple_triggers = [
(0.25,
   [
      (ge,"$g_player_raiding_village",1),
      (store_distance_to_party_from_party, ":distance", "$g_player_raiding_village", "p_main_party"),
      (try_begin),
        (gt, ":distance", raid_distance),
        (str_store_party_name_link, s1, "$g_player_raiding_village"),
        (display_message, "@You have broken off your raid of {s1}."),
        (call_script, "script_village_set_state", "$current_town", 0),
        (party_set_slot, "$current_town", slot_village_raided_by, -1),
        (assign, "$g_player_raiding_village", 0),
        (rest_for_hours, 0, 0, 0), #stop resting - abort
      (else_try),
        (ge, ":distance", raid_distance / 2),
        (map_free),
        (jump_to_menu, "mnu_village_loot_continue"),
      (try_end),
    ]),
]
