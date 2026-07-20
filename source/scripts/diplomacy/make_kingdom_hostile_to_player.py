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

make_kingdom_hostile_to_player_scripts = [
("make_kingdom_hostile_to_player",
    [
      (store_script_param_1, ":kingdom_no"),
      (store_script_param_2, ":difference"),

      (try_begin),
        (lt, ":difference", 0),
        (store_relation, ":player_relation", ":kingdom_no", "fac_player_supporters_faction"),
        (val_min, ":player_relation", 0),
        (val_add, ":player_relation", ":difference"),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_no", ":player_relation"),
      (try_end),
  ])
]
