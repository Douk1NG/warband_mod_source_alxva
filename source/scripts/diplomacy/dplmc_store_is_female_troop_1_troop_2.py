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

dplmc_store_is_female_troop_1_troop_2_scripts = [
##script_dplmc_store_is_female_troop_1_troop_2
#
#This exists to make it easy to modify this to work with mods that redefine the troop types.
#See script_dplmc_store_troop_is_female
#
#INPUT:
#      arg1: troop_1
#      arg2: troop_2
#OUTPUT:
#       reg0: 0 for not female, 1 for female
#       reg1: 0 for not female, 1 for female
("dplmc_store_is_female_troop_1_troop_2",
  [
	(store_script_param_1, ":troop_1"),
	(store_script_param_2, ":troop_2"),
    (ge, ":troop_1", 0),
    (ge, ":troop_1", 0),
    (troop_get_type, ":is_female_1", ":troop_1"),
    (troop_get_type, ":is_female_2", ":troop_2"),
	(val_mod, ":is_female_1", 2), # Makes even number skins "0" odd number "1" - tf_female is eqal to 1
	(val_mod, ":is_female_2", 2), # Makes even number skins "0" odd number "1" - tf_female is eqal to 1
	(assign, reg0, ":is_female_1"),
	(assign, reg1, ":is_female_2"),
  ])
]
