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


  ###)))

  ##diplomacy end

  ###(((manage_inventory
  

manage_inventory_trigger_simple_triggers = [
(0,
  [
    (map_free),
    (try_begin),
      (eq, "$game_key_manage_inventory", 0),
      (assign, "$game_key_manage_inventory", key_m),
    (try_end),
    (key_clicked, "$game_key_manage_inventory"),
    (assign, "$g_prsnt_param_1", "trp_player"),
    (assign, "$g_selected_troop", "trp_player"),
    (start_presentation, "prsnt_equip_npcs"),
  ]),
]
