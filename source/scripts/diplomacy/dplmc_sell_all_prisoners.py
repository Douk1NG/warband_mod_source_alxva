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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_sell_all_prisoners_scripts = [
# "script_dplmc_sell_all_prisoners"
#
# Taken from rubik's Custom Commander, and altered to have parameters
# and return feedback.
#
#INPUT:
#Arg 1: actually remove (positive for yes, zero or negative for no)
#Arg 2: if positive, use this as a fixed price instead of calculating dynamically
#OUTPUT:
#reg0: amount of gold gained (or would have been gained if the sale occurred)
#reg1: number of prisoners sold (or would have been sold if the sale occurred)
("dplmc_sell_all_prisoners",
   [
    (store_script_param_1, ":actually_remove"),
    (store_script_param_2, ":fixed_price"),
    (call_script, "script_dplmc_sell_all_prisoners_from_party", "p_main_party", ":actually_remove", ":fixed_price"),
  ])
]
