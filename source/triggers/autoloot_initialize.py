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



  #initialize autoloot feature if you have a chamberlain
  ##diplomacy start+
  #Disable this: autoloot gets initialized elsewhere.
  

autoloot_initialize_triggers = [
(24, 0, ti_once,
  [
	  ##NEW:
	  (eq, 0, 1),
	  ##OLD:
      #(store_skill_level, ":inv_skill", "skl_inventory_management", "trp_player"),
      #(gt, "$g_player_chamberlain", 0),
      #(ge, ":inv_skill", 3),
  ],
  [
	##NEW:
	#This doesn't ever get called, but if it did here's what should happen"
	(call_script, "script_dplmc_initialize_autoloot", 1),#argument "1" forces this to make changes
	##OLD:
    #(call_script, "script_dplmc_init_item_difficulties"),
    #(call_script, "script_dplmc_init_item_base_score"),
    #(assign, "$g_autoloot", 1),
  ]),
]
