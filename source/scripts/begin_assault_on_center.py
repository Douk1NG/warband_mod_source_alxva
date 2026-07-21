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

begin_assault_on_center_scripts = [
# script_process_kingdom_parties_ai
# Input: arg1: faction_no
# Output: none
#called from triggers
("begin_assault_on_center",
   [
     (store_script_param, ":center_no", 1),
	 ##diplomacy start+ add support for promoted kingdom ladies
     (try_for_range, ":troop_no", heroes_begin, heroes_end),#<- change active_npcs to heroes
	 ##diplomacy end+
       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
       (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
       (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
       (gt, ":party_no", 0),
       (party_is_active, ":party_no"),

       (assign, ":continue", 0),
       (try_begin),
         (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
         (party_slot_eq, ":party_no", slot_party_ai_object, ":center_no"),
         (party_slot_eq, ":party_no", slot_party_ai_substate, 0),
         (assign, ":continue", 1),
       (else_try),
         (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
         (party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
         (gt, ":commander_party", 0),
         (party_is_active, ":commander_party"),
         (party_slot_eq, ":commander_party", slot_party_ai_state, spai_besieging_center),
         (party_slot_eq, ":commander_party", slot_party_ai_object, ":center_no"),
         (call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, ":center_no"),
         (assign, ":continue", 1),
       (try_end),

       (eq, ":continue", 1),

       (party_set_ai_behavior, ":party_no", ai_bhvr_attack_party),
       (party_set_ai_object, ":party_no", ":center_no"),
       (party_set_flags, ":party_no", pf_default_behavior, 1),
       (party_set_slot, ":party_no", slot_party_ai_substate, 1),
     (try_end),
   ])
]
