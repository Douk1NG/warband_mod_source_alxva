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

add_routed_party_scripts = [
("add_routed_party",
   [
     (party_get_num_companion_stacks, ":num_stacks", "p_routed_enemies"), #question, I changed (total_enemy_casualties) with (p_routed_enemies) because this is not prisoner in p_routed_enemies party.
     (assign, ":num_regulars", 0),
     (assign, ":deleted_stacks", 0),
     (try_for_range, ":stack_no", 0, ":num_stacks"),
       (store_sub, ":difference", ":num_stacks", ":stack_no"),
       (ge, ":difference", ":deleted_stacks"),
       (store_sub, ":stack_no_minus_deleted", ":stack_no", ":deleted_stacks"),
       (party_stack_get_troop_id, ":stack_troop", "p_routed_enemies", ":stack_no_minus_deleted"),
       (try_begin),
         (troop_is_hero, ":stack_troop"),
         (party_stack_get_size, ":stack_size", "p_routed_enemies", ":stack_no_minus_deleted"),
         (party_remove_members, "p_routed_enemies", ":stack_troop", 1),
         (try_begin),
           (le, ":stack_size", 1),
           (val_add, ":deleted_stacks", 1), #if deleted hero is the only one in his troop, now we have one less stacks
         (try_end),
       (else_try),
         (val_add, ":num_regulars", 1),
       (try_end),
     (try_end),

     #add new party to map if there is at least one routed agent. (new party name : routed_party, template : routed_warriors)
     (try_begin),
       (ge, ":num_regulars", 1),

       (set_spawn_radius, 2),
       (spawn_around_party, "p_main_party", "pt_routed_warriors"),
       (assign, ":routed_party", reg0),
       # SB : white flag
       (party_set_banner_icon, ":routed_party", "icon_white_flag"),
       (party_set_slot, ":routed_party", slot_party_commander_party, -1), #we need this because 0 is player's party!

       (assign, ":max_routed_agents", 0),
       (assign, ":routed_party_faction", "fac_neutral"),
       (try_for_range, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end),
         (faction_get_slot, ":num_routed_agents_in_this_faction", ":cur_faction", slot_faction_num_routed_agents),
         (gt, ":num_routed_agents_in_this_faction", ":max_routed_agents"),
         (assign, ":max_routed_agents", ":num_routed_agents_in_this_faction"),
         (assign, ":routed_party_faction", ":cur_faction"),
       (try_end),

       (party_set_faction, ":routed_party", ":routed_party_faction"),

       (party_set_ai_behavior, ":routed_party", ai_bhvr_travel_to_party),

       (assign, ":minimum_distance", 1000000),
       #SB : get rid of useless range
       (store_random_in_range, ":nearest_ally_city", walled_centers_begin, walled_centers_end),
       (try_for_range, ":party_no", walled_centers_begin, walled_centers_end),
         # (party_is_active, ":party_no"),
         # (party_get_slot, ":cur_party_type", ":party_no", slot_party_type),
         # (this_or_next|eq, ":cur_party_type", spt_town),
         # (eq, ":cur_party_type", spt_castle),
         (store_faction_of_party, ":cur_faction", ":party_no"),
         (this_or_next|eq, ":routed_party_faction", "fac_neutral"),
         (eq, ":cur_faction", ":routed_party_faction"),
         (party_get_position, pos1, ":party_no"),
         (store_distance_to_party_from_party, ":dist", ":party_no", "p_main_party"),
         (try_begin),
           (lt, ":dist", ":minimum_distance"),
           (assign, ":minimum_distance", ":dist"),
           (assign, ":nearest_ally_city", ":party_no"),
         (try_end),
       (try_end),

       (party_get_position, pos1, "p_main_party"), #store position information of main party in pos1
       (party_get_position, pos2, ":nearest_ally_city"), #store position information of target city in pos2

       (assign, ":minimum_distance", 1000000),
       (try_for_range, ":unused", 0, 10),
         (map_get_random_position_around_position, pos3, pos1, 2), #store position of found random position (possible placing position for new routed party) around battle position in pos3
         (get_distance_between_positions, ":dist", pos2, pos3), #store distance between found position and target city in ":dist".
         (try_begin),
           (lt, ":dist", ":minimum_distance"),
           (assign, ":minimum_distance", ":dist"),
           (copy_position, pos63, pos3),
         (try_end),
       (end_try),

       (party_set_position, ":routed_party", pos63),

       (party_set_ai_object, ":routed_party", ":nearest_ally_city"),
       (party_set_flags, ":routed_party", pf_default_behavior, 1),
       #SB : add extra slot to actually merge with garrison
       (party_set_slot, ":routed_party", slot_party_type, spt_reinforcement),

       #adding party members of p_routed_enemies to routed_party
       (party_clear, ":routed_party"),
       (party_get_num_companion_stacks, ":num_stacks", "p_routed_enemies"), #question, I changed (total_enemy_casualties) with (p_routed_enemies) because this is not prisoner in p_routed_enemies party.
       (try_for_range, ":stack_no", 0, ":num_stacks"),
         (party_stack_get_troop_id, ":stack_troop", "p_routed_enemies", ":stack_no"),
         (try_begin),
           (neg|troop_is_hero, ":stack_troop"), #do not add routed heroes to (new created) routed party for now.

           (party_stack_get_size, ":stack_size", "p_routed_enemies", ":stack_no"),
           (party_add_members, ":routed_party", ":stack_troop", ":stack_size"),
         (try_end),
       (try_end),
     (try_end),
    ])
]
