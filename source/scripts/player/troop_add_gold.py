# ======================================================================
# SHARED DEPENDENCY
# Entity: troop_add_gold (script)
# Called by menus in 3 domains: castle, town, village
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

troop_add_gold_scripts = [
("troop_add_gold",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":amount", 2),

      (troop_add_gold, ":troop_no", ":amount"),
      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (play_sound, "snd_money_received"),
      (try_end),
     ])
]
