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

order_best_besieger_party_to_guard_center_scripts = [
# INPUT:
# param1: defeated_center, param2: winner_faction
# OUTPUT:
# none
("order_best_besieger_party_to_guard_center",
    [
      (store_script_param, ":defeated_center", 1),
      (store_script_param, ":winner_faction", 2),
      (assign, ":best_party", -1),
      (assign, ":best_party_strength", 0),
      ##diplomacy start+ support for promoted kingdom ladies
      (try_for_range, ":kingdom_hero", heroes_begin, heroes_end),#<- changed to heroes
        (this_or_next|troop_slot_eq, ":kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
           (is_between, ":kingdom_hero", active_npcs_begin, active_npcs_end),
      ##diplomacy end+
        (troop_get_slot, ":kingdom_hero_party", ":kingdom_hero", slot_troop_leaded_party),
        (gt, ":kingdom_hero_party", 0),
        (party_is_active, ":kingdom_hero_party"),
        (store_faction_of_party, ":kingdom_hero_party_faction", ":kingdom_hero_party"),
        (eq, ":winner_faction", ":kingdom_hero_party_faction"),
        (store_distance_to_party_from_party, ":dist", ":kingdom_hero_party", ":defeated_center"),
        (lt, ":dist", 5),
        #If marshall has captured the castle, then do not leave him behind.
        (neg|faction_slot_eq, ":winner_faction", slot_faction_marshall, ":kingdom_hero"),
        (assign, ":has_besiege_ai", 0),
        (try_begin),
          (party_slot_eq, ":kingdom_hero_party", slot_party_ai_state, spai_besieging_center),
          (party_slot_eq, ":kingdom_hero_party", slot_party_ai_object, ":defeated_center"),
          (assign, ":has_besiege_ai", 1),
        (else_try),
          (party_slot_eq, ":kingdom_hero_party", slot_party_ai_state, spai_accompanying_army),
          (party_get_slot, ":kingdom_hero_party_commander_party", ":kingdom_hero_party", slot_party_ai_object),
          (party_slot_eq, ":kingdom_hero_party_commander_party", slot_party_ai_state, spai_besieging_center),
          (party_slot_eq, ":kingdom_hero_party_commander_party", slot_party_ai_object, ":defeated_center"),
          (assign, ":has_besiege_ai", 1),
        (try_end),
        (eq, ":has_besiege_ai", 1),
        (party_get_slot, ":kingdom_hero_party_strength", ":kingdom_hero_party", slot_party_cached_strength),#recently calculated
        (gt, ":kingdom_hero_party_strength", ":best_party_strength"),
        (assign, ":best_party_strength", ":kingdom_hero_party_strength"),
        (assign, ":best_party", ":kingdom_hero_party"),
      (try_end),
      (try_begin),
        (gt, ":best_party", 0),
        (call_script, "script_party_set_ai_state", ":best_party", spai_holding_center, ":defeated_center"),
        #(party_set_slot, ":best_party", slot_party_commander_party, -1),
        (party_set_flags, ":best_party", pf_default_behavior, 1),
      (try_end),
      ])
]
