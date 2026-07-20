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

npc_get_troop_wage_scripts = [
#script_game_reset_player_party_name:
# script_npc_get_troop_wage
# This script is called from module system to calculate troop wages for npc parties.
# Input:
# param1: troop_id
# Output: reg0: weekly wage
("npc_get_troop_wage",
    [
      (store_script_param_1, ":troop_id"),
      (assign,":wage", 0),
      (try_begin),
        (troop_is_hero, ":troop_id"),
      (else_try),
        (store_character_level, ":wage", ":troop_id"),
        (val_mul, ":wage", ":wage"),
        (val_add, ":wage", 50),
        (val_div, ":wage", 30),
        (troop_is_mounted, ":troop_id"),
        (val_mul, ":wage", 5),
        (val_div, ":wage", 4),
      (try_end),
      (assign, reg0, ":wage"),
  ])
]
