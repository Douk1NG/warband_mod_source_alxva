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

dplmc_send_recruiter_scripts = [
("dplmc_send_recruiter",
    [
    (store_script_param, ":number_of_recruits", 1),
#daedalus begin
   (store_script_param, ":faction_of_recruits", 2),
#daedalus end
   (assign, ":expenses", ":number_of_recruits"),
   (val_mul, ":expenses", 20),
   (val_add, ":expenses", 10),
   (call_script, "script_dplmc_withdraw_from_treasury", ":expenses"),
   (set_spawn_radius, 1),
    (spawn_around_party, "$current_town", "pt_dplmc_recruiter"),
    (assign,":spawned_party",reg0),
    (party_set_ai_behavior, ":spawned_party", ai_bhvr_hold),
    (party_set_slot, ":spawned_party", slot_party_type, dplmc_spt_recruiter),
    (party_set_slot, ":spawned_party", dplmc_slot_party_recruiter_needed_recruits, ":number_of_recruits"),
   #daedalus begin
   (party_set_slot, ":spawned_party", dplmc_slot_party_recruiter_needed_recruits_faction, ":faction_of_recruits"),
   #daedalus end
   (party_set_slot, ":spawned_party", dplmc_slot_party_recruiter_origin, "$current_town"),
   (assign, ":faction", "$players_kingdom"),
   (party_set_faction, ":spawned_party", ":faction"),
    ])
]
