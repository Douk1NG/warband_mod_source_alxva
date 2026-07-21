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

dplmc_send_patrol_scripts = [
("dplmc_send_patrol",
  [
    (store_script_param, ":start_party", 1),
    (store_script_param, ":target_party", 2),
    (store_script_param, ":size", 3), #0 small, 1 medium, 2, big, 3 elite
    (store_script_param, ":template_faction", 4),
    (store_script_param, ":order_troop", 5),

    (set_spawn_radius, 1),
    (spawn_around_party, ":start_party", "pt_patrol_party"),
    (assign,":spawned_party",reg0),
    (party_set_faction, ":spawned_party", ":template_faction"),
    (party_set_slot, ":spawned_party", slot_party_type, spt_patrol),
    (party_set_slot, ":spawned_party", slot_party_home_center, ":start_party"),
    (party_set_slot, ":spawned_party", dplmc_slot_party_mission_diplomacy, ":order_troop"),
    (str_store_party_name, s5, ":target_party"),
    (party_set_name, ":spawned_party", "str_s5_patrol"),

    (party_set_ai_behavior, ":spawned_party", ai_bhvr_travel_to_party),
    (party_set_ai_object, ":spawned_party", ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_object, ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_state, spai_patrolling_around_center),

    (try_begin),
      (neg|is_between, ":template_faction", npc_kingdoms_begin, npc_kingdoms_end),

      (party_get_slot, ":template_faction", ":start_party", slot_center_original_faction),
      (try_begin),
        (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
        (assign, ":template_faction", "$g_player_culture"),
      (else_try),
        (party_get_slot, ":town_lord", ":start_party", slot_town_lord),
        (gt, ":town_lord", 0),
        (troop_get_slot, ":template_faction", ":town_lord", slot_troop_original_faction),
      (try_end),

      (try_begin),
        (eq, ":size", 0),
        (call_script, "script_dplmc_withdraw_from_treasury", 1000),
      (else_try),
        (this_or_next|eq, ":size", 1),
        (eq, ":size", 3),
        (call_script, "script_dplmc_withdraw_from_treasury", 2000),
      (else_try),
        (eq, ":size", 2),
        (call_script, "script_dplmc_withdraw_from_treasury", 3000),
      (try_end),
    (try_end),

    (faction_get_slot, ":party_template_a", ":template_faction", slot_faction_reinforcements_a),
    (faction_get_slot, ":party_template_b", ":template_faction", slot_faction_reinforcements_b),
    (faction_get_slot, ":party_template_c", ":template_faction", slot_faction_reinforcements_c),

    (try_begin),
      (eq, ":size", 3),
      (party_add_template, ":spawned_party", ":party_template_c"),
      (party_add_template, ":spawned_party", ":party_template_c"),
    (else_try),
      (val_add, ":size", 1),
      (val_mul, ":size", 2),
      (try_for_range, ":cur_i", 0, ":size"),
        (store_random_in_range, ":random", 0, 3),
        (try_begin),
          (eq, ":random", 0),
          (party_add_template, ":spawned_party", ":party_template_a"),
        (else_try),
          (eq, ":random", 1),
          (party_add_template, ":spawned_party", ":party_template_b"),
        (else_try),
          (party_add_template, ":spawned_party", ":party_template_c"),
        (try_end),

        (try_begin), #debug
          (eq, "$cheat_mode", 1),
          (assign, reg0, ":cur_i"),
          (str_store_faction_name, s7, ":template_faction"),
          (display_message, "@{!}DEBUG - Added {reg0}.template of faction {s7} to patrol."),
        (try_end),
      (try_end),
    (try_end),


    (try_begin), #debug
      (eq, "$cheat_mode", 1),
      (str_store_party_name, s13, ":target_party"),
      (str_store_faction_name, s14, ":template_faction"),
      (str_store_party_name, s15, ":start_party"),
      (display_message, "@{!}DEBUG - Send {s14} patrol from {s15} to {s13}"),
    (try_end),
  ])
]
