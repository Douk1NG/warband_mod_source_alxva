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

dplmc_move_troops_party_scripts = [
("dplmc_move_troops_party",
  [
    (store_script_param, ":start_party", 1),
    (store_script_param, ":target_party", 2),
    (store_script_param, ":party_no", 3),
    (store_script_param, ":template_faction", 4),

    (set_spawn_radius, 1),
    (spawn_around_party, ":start_party", "pt_patrol_party"),
    (assign,":spawned_party",reg0),
    (party_set_faction, ":spawned_party", ":template_faction"),
    (party_set_slot, ":spawned_party", slot_party_type, spt_patrol),
    (party_set_slot, ":spawned_party", slot_party_home_center, ":start_party"),
    (str_store_party_name, s5, ":target_party"),
    #SB : fixed string
    (party_set_name, ":spawned_party", "str_s5_transfer"),

    (party_set_ai_behavior, ":spawned_party", ai_bhvr_travel_to_party),
    (party_set_ai_object, ":spawned_party", ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_object, ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_state, spai_retreating_to_center),
    (party_set_aggressiveness, ":spawned_party", 0),
    (party_set_courage, ":spawned_party", 3),
    (party_set_ai_initiative, ":spawned_party", 100),

    (call_script, "script_party_add_party", ":spawned_party", ":party_no"),
  ])
]
