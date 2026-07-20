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
from module_items import items
from scripts._helpers import make_noswing_weapons

init_noswing_weapons_scripts = [
("init_noswing_weapons", make_noswing_weapons(items))
]
