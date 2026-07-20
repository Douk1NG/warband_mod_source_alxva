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

get_troop_of_merchant_scripts = [
("get_troop_of_merchant",
  [
        (store_faction_of_party, ":starting_town_faction", "$g_starting_town"),
        (store_sub, ":troop_of_merchant", ":starting_town_faction", npc_kingdoms_begin),
        (val_add, ":troop_of_merchant", startup_merchants_begin),
        (assign, reg0, ":troop_of_merchant"),
  ])
]
