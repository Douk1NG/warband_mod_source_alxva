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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

get_chest_troop_scripts = [
("get_chest_troop",
  [
    (store_script_param, ":party_no", 1),
    (try_begin),
        (gt, "$g_player_chamberlain", 0),
        (assign, ":chest_troop", "trp_household_possessions"),
    (else_try), #assume troops same order as parties
        # (party_get_slot, ":chest_troop", ":party_no", slot_town_seneschal),
        (val_sub, ":party_no", towns_begin),
        (store_add, ":chest_troop", ":party_no", "trp_town_1_seneschal"),
    (try_end),
    (assign, reg0, ":chest_troop"),
  ])
]
