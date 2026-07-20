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

dplmc_send_messenger_to_party_scripts = [
("dplmc_send_messenger_to_party",
  [
    (store_script_param, ":target_party", 1),
    (store_script_param, ":message", 2),
    (store_script_param, ":orders_object", 3),

    (set_spawn_radius, 1),
    (spawn_around_party, "$current_town", "pt_messenger_party"),
    (assign, ":spawned_party", reg0),

    #SB : factionalized messenger
    (store_faction_of_party, ":faction_no", ":target_party"),
    (try_begin),
      (eq, ":faction_no", "fac_player_supporters_faction"),
      (is_between, "$g_player_culture", npc_kingdoms_begin, kingdoms_end),
      (assign, ":faction_no", "$g_player_culture"),
    (try_end),

    (try_begin),
      (is_between, ":faction_no", npc_kingdoms_begin, kingdoms_end),
      (faction_get_slot, ":messenger_troop", ":faction_no", slot_faction_messenger_troop),
    (else_try),
      (assign, ":messenger_troop", "trp_dplmc_messenger"),
    (try_end),
    (party_add_members, ":spawned_party", ":messenger_troop", 1),
    (party_set_faction, ":spawned_party", "fac_player_faction"),
    (party_set_slot, ":spawned_party", slot_party_type, spt_messenger),
    (party_set_slot, ":spawned_party", dplmc_slot_party_mission_diplomacy, ":message"),
    (party_set_slot, ":spawned_party", slot_party_home_center, "$current_town"),

    (party_set_ai_behavior, ":spawned_party", ai_bhvr_travel_to_party),
    (party_set_ai_object, ":spawned_party", ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_object, ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_orders_object, ":orders_object"),

    (try_begin), #debug
      (eq, "$cheat_mode", 1),
      (str_store_party_name, s13, ":target_party"),
      (display_message, "@{!}DEBUG - Send message to {s13}"),
    (try_end),
  ]
  )
]
