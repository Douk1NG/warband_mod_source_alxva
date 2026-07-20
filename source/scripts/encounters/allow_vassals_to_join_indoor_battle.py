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

allow_vassals_to_join_indoor_battle_scripts = [
("allow_vassals_to_join_indoor_battle",
    [
     #if our commander attacks an enemy army
     ##diplomacy start+ Support promoted kingdom ladies
     #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
     (try_for_range, ":troop_no", heroes_begin, heroes_end),
     ##diplomacy end+
       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
       (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
       (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
       (gt, ":party_no", 0),
       (party_is_active, ":party_no"),

       (party_get_attached_to, ":party_is_attached_to", ":party_no"),
       (lt, ":party_is_attached_to", 0),

       (store_troop_faction, ":faction_no", ":troop_no"),

       (try_begin),
         #(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
         (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
         (party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
         (gt, ":commander_party", 0),
         (party_is_active, ":commander_party"),

         (assign, ":besieged_center", -1),
         (try_begin),
           (party_slot_eq, ":commander_party", slot_party_ai_state, spai_holding_center), #if commander is holding a center
           (party_get_slot, ":commander_object", ":commander_party", slot_party_ai_object), #get commander's ai object (center they are holding)
           (party_get_battle_opponent, ":besieger_enemy", ":commander_object"), #get this object's battle opponent
           (party_is_active, ":besieger_enemy"),
           (assign, ":besieged_center", ":commander_object"),
           (assign, ":commander_object", ":besieger_enemy"),
         (else_try),
           (party_slot_eq, ":commander_party", slot_party_ai_state, spai_engaging_army), #if commander is engaging an army
           (party_get_slot, ":commander_object", ":commander_party", slot_party_ai_object), #get commander's ai object (army which they engaded)
           (ge, ":commander_object", 0), #if commander has an object
           (neg|is_between, ":commander_object", centers_begin, centers_end), #if this object is not a center, so it is a party
           (party_is_active, ":commander_object"),
           (party_get_battle_opponent, ":besieged_center", ":commander_object"), #get this object's battle opponent
         (else_try),
           (assign, ":besieged_center", -1),
         (try_end),

         (is_between, ":besieged_center", walled_centers_begin, walled_centers_end), #if battle opponent of our commander's ai object is a walled center

         (party_get_attached_to, ":attached_to_party", ":commander_party"), #if commander is attached to besieged center already.
         (eq, ":attached_to_party", ":besieged_center"),

         (store_faction_of_party, ":besieged_center_faction", ":besieged_center"),#get (battle opponent of our commander's ai object)'s faction
         (eq, ":besieged_center_faction", ":faction_no"), #if battle opponent of our commander's ai object is from same faction with current party
         (party_is_active, ":commander_object"),
         #make also follow_or_not check if needed

         (call_script, "script_party_set_ai_state", ":party_no", spai_engaging_army, ":commander_object"), #go and help commander

         (try_begin),
           (eq, "$cheat_mode", 1),
           (str_store_party_name, s7, ":party_no"),
           (str_store_party_name, s6, ":commander_object"),
           (display_message, "@{!}DEBUG : {s7} is helping his commander by fighting with {s6}."),
         (try_end),
       (else_try),
         #(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),

         (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
         (party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
         (gt, ":commander_party", 0),
         (party_is_active, ":commander_party"),

         (party_get_battle_opponent, ":besieged_center", ":commander_party"), #get this object's battle opponent

         #make also follow_or_not check if needed

         (is_between, ":besieged_center", walled_centers_begin, walled_centers_end), #if this object is a center
         (party_get_attached_to, ":attached_to_party", ":party_no"),
         (neq, ":attached_to_party", ":besieged_center"),
         (party_is_active, ":besieged_center"),

         (call_script, "script_party_set_ai_state", ":party_no", spai_engaging_army, ":besieged_center"), #go and help commander

         #(try_begin),
         #  (eq, "$cheat_mode", 1),
         #  (str_store_party_name, s7, ":party_no"),
         #  (str_store_party_name, s6, ":besieged_center"),
         #  (display_message, "@{!}DEBUG : {s7} is helping his commander by attacking {s6}."),
         #(try_end),

         #(party_set_ai_behavior, ":party_no", ai_bhvr_attack_party),
         #(party_set_ai_object, ":party_no", ":besieged_center"),
         #(party_set_flags, ":party_no", pf_default_behavior, 1), #is these needed?
         #(party_set_slot, ":party_no", slot_party_ai_substate, 1), #is these needed?
       (try_end),
     (try_end),
     ])
]
