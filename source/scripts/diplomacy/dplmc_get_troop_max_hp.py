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

dplmc_get_troop_max_hp_scripts = [
("dplmc_get_troop_max_hp",
   [
    (store_script_param_1, ":troop"),

    (store_skill_level, ":skill", skl_ironflesh, ":troop"),
    (store_attribute_level, ":attrib", ":troop", ca_strength),
    (val_mul, ":skill", 2),
    (val_add, ":skill", ":attrib"),
    (val_add, ":skill", 35),
    (assign, reg0, ":skill"),
  ])
]
