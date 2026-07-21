# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

game_receive_url_response_scripts = [
#script_show_multiplayer_message
#response format should be like this:
#  [a number or a string]|[another number or a string]|[yet another number or a string] ...
# here is an example response:
# 12|Player|100|another string|142|323542|34454|yet another string
# INPUT: arg1 = num_integers, arg2 = num_strings
# reg0, reg1, reg2, ... up to 128 registers contain the integer values
# s0, s1, s2, ... up to 128 strings contain the string values
("game_receive_url_response",
    [
      #here is an example usage
##      (store_script_param, ":num_integers", 1),
##      (store_script_param, ":num_strings", 2),
##      (try_begin),
##        (gt, ":num_integers", 4),
##        (display_message, "@{reg0}, {reg1}, {reg2}, {reg3}, {reg4}"),
##      (try_end),
##      (try_begin),
##        (gt, ":num_strings", 4),
##        (display_message, "@{s0}, {s1}, {s2}, {s3}, {s4}"),
##      (try_end),
      ])
]
