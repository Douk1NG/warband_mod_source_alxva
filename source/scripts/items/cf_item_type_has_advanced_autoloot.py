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

cf_item_type_has_advanced_autoloot_scripts = [
("cf_item_type_has_advanced_autoloot", [
    (store_script_param, ":item_type", 1),
    (this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_shield),
    (eq, ":item_type", itp_type_thrown), #throwing axe vs jaridss vs rocks
    #all other ranged weapons are pierce (for now) excluding arena ones
  ])
]
