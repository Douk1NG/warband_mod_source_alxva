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

get_number_of_hero_centers_scripts = [
##  # script_give_town_to_besiegers
##  # Input: arg1 = center_no, arg2 = besieger_party
##  ("give_town_to_besiegers",
##    [
##      (store_script_param_1, ":center_no"),
##      (store_script_param_2, ":besieger_party"),
##      (store_faction_of_party, ":besieger_faction", ":besieger_party"),
##
##      (try_begin),
##        (call_script, "script_cf_get_party_leader", ":besieger_party"),
##        (assign, ":new_leader", reg0),
##      (else_try),
##        (call_script, "script_select_kingdom_hero_for_new_center", ":besieger_faction"),
##        (assign, ":new_leader", reg0),
##      (try_end),
##
##      (call_script, "script_give_center_to_lord", ":center_no", ":new_leader"),
##
##      (try_for_parties, ":party_no"),
##        (get_party_ai_object, ":object", ":party_no"),
##        (get_party_ai_behavior, ":behavior", ":party_no"),
##        (eq, ":object", ":center_no"),
##        (this_or_next|eq, ":behavior", ai_bhvr_travel_to_party),
##        (eq, ":behavior", ai_bhvr_attack_party),
##        (party_set_ai_behavior, ":party_no", ai_bhvr_hold),
##        (party_set_slot, ":party_no", slot_party_ai_state, spai_undefined),
##        (party_set_flags, ":party_no", pf_default_behavior, 0),
##      (try_end),
##
##      #Staying at the center for a while
##      (party_set_ai_behavior, ":besieger_party", ai_bhvr_hold),
##      (party_set_slot, ":besieger_party", slot_party_ai_state, spai_undefined),
##      (party_set_flags, ":besieger_party", pf_default_behavior, 0),
##
##      (faction_get_slot, ":reinforcement_a", ":besieger_faction", slot_faction_reinforcements_a),
##      (faction_get_slot, ":reinforcement_b", ":besieger_faction", slot_faction_reinforcements_b),
##      (party_add_template, ":center_no", ":reinforcement_a"),
##      (party_add_template, ":center_no", ":reinforcement_b"),
##  ]),
##
# script_get_number_of_hero_centers
# Input: arg1 = troop_no
# Output: reg0 = number of centers that are ruled by the hero
("get_number_of_hero_centers",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":result", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (val_add, ":result", 1),
      (try_end),
      (assign, reg0, ":result"),
  ])
]
