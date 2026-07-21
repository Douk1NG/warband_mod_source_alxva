# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

cf_melee_weapon_is_civilian_scripts = [
("cf_melee_weapon_is_civilian", [
    (store_script_param, ":item", 1),
    (this_or_next|is_between, ":item", "itm_sickle", "itm_dagger"),
    (this_or_next|is_between, ":item", "itm_scythe", "itm_military_fork"),
    (this_or_next|eq, ":item", "itm_wooden_stick"),
    (eq, ":item", "itm_torch"),
    # (eq, ":item", "itm_stones"),
     #include arena weapons here as well
  ])
]
