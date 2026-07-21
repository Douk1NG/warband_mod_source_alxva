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

dplmc_appoint_constable_scripts = [
("dplmc_appoint_constable",
  [
    (troop_set_auto_equip, "trp_dplmc_constable", 0),
    (troop_set_inventory_slot, "trp_dplmc_constable", ek_body, "itm_dplmc_coat_of_plates_red_constable"),
    (troop_set_inventory_slot, "trp_dplmc_constable", ek_foot, "itm_leather_boots"),
    (assign, "$g_player_constable", "trp_dplmc_constable"),
  ])
]
