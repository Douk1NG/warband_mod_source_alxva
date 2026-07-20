# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_appoint_chamberlain (script)
# Called by menus in 2 domains: diplomacy, village
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

dplmc_appoint_chamberlain_scripts = [
("dplmc_appoint_chamberlain",
  [
    (troop_set_auto_equip, "trp_dplmc_chamberlain", 0),
    (troop_set_inventory_slot, "trp_dplmc_chamberlain", ek_body, "itm_tabard"),
    (troop_set_inventory_slot, "trp_dplmc_chamberlain", ek_foot, "itm_leather_boots"),
    (assign, "$g_player_chamberlain", "trp_dplmc_chamberlain"),
    #SB : grab all gold from chest troops (seneschals)
    (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
      (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
      (store_sub, ":chest_troop", ":center_no", towns_begin),
      (val_add, ":chest_troop", "trp_town_1_seneschal"),
      (store_troop_gold, ":cur_gold", ":chest_troop"),
      (troop_remove_gold, ":chest_troop", ":cur_gold"),
      (troop_add_gold, "trp_household_possessions", ":cur_gold"), #no script call
    (try_end),
  ])
]
