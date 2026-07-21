# ======================================================================
# SHARED DEPENDENCY
# Entity: cf_dplmc_troop_is_female (script)
# Called by menus in 4 domains: dickplomacy, diplomacy, notifications, reports
# ======================================================================

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

cf_dplmc_troop_is_female_scripts = [
##script_cf_dplmc_troop_is_female
#
#This exists to make it easy to modify this to work with mods that redefine the troop types.
#See script_dplmc_store_troop_is_female
#
#INPUT: arg1: troop_no
#OUTPUT: none
("cf_dplmc_troop_is_female",
  [
	(store_script_param_1, ":troop_no"),
	(assign, ":is_female", 0),
	(ge, ":troop_no", 0),#Undefined behavior when the arguments are invalid.
	(try_begin),
	   (eq, ":troop_no", active_npcs_including_player_begin),
	   (assign, ":troop_no", "trp_player"),
	(try_end),
  	(troop_get_type, ":is_female", ":troop_no"),
	(val_mod, ":is_female", 2), # Makes even number skins "0" odd number "1" - tf_female is eqal to 1
	(eq, ":is_female", tf_female),
  ])
]
