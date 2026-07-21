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

cf_get_random_lord_except_king_with_faction_scripts = [
#script_party_prisoners_add_party_prisoners:
# Input: arg1 = faction_no
# Output: reg0 = troop_no, Can Fail!
("cf_get_random_lord_except_king_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (val_add, ":count_lords", 1),
      (try_end),
      (store_random_in_range, ":random_lord", 0, ":count_lords"),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (eq, ":result", -1),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (val_add, ":count_lords", 1),
        (lt, ":random_lord", ":count_lords"),
        (assign, ":result", ":lord_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ])
]
