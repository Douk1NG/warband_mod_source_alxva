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



  # Reduce renown slightly by 0.5% every week
  

reduce_renown_simple_triggers = [
(7 * 24,
   [
       (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
       (store_div, ":renown_decrease", ":player_renown", 200),
       (val_sub, ":player_renown", ":renown_decrease"),
       (troop_set_slot, "trp_player", slot_troop_renown, ":player_renown"),
       
       #SB : slowly increase renown of minister weekly instead of doing so upon assignment
       (try_begin),
         (gt, "$g_player_minister", 0),
         (neq, "$g_player_minister", "trp_temporary_minister"),
         (call_script, "script_change_troop_renown", "$g_player_minister", 10),
       (try_end)
    ]),
]
