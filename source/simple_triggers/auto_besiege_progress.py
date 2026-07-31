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

auto_besiege_progress_simple_triggers = [
(0.25,
   [
      (gt,"$auto_besiege_town",0),
      (gt,"$g_player_besiege_town", 0),
      (ge, "$g_siege_method", 1),
   
      (store_distance_to_party_from_party, ":distance", "$g_player_besiege_town", "p_main_party"),
      (try_begin),
        (gt, ":distance", raid_distance / 2),
        (str_store_party_name_link, s1, "$g_player_besiege_town"),
        (display_message, "@You have broken off your siege of {s1}."),
        (call_script, "script_lift_siege", "$g_player_besiege_town", 0),
        (assign, "$g_player_besiege_town", -1),
        (rest_for_hours, 0, 0, 0), #stop resting - abort
      (else_try),
        (ge, ":distance", raid_distance / 3),
        (map_free),
        (str_store_party_name_link, s1, "$g_player_besiege_town"),
        (display_message, "@You cannot maintain your siege of {s1} from this distance. You risk your lines breaking."),
      (else_try),
        (store_current_hours, ":cur_hours"),
        (ge, ":cur_hours", "$g_siege_method_finish_hours"),
        (neg|is_currently_night),
        (rest_for_hours, 0, 0, 0), #stop resting, if resting
        (start_encounter, "$auto_besiege_town"),
      (try_end),
    ]),
]
