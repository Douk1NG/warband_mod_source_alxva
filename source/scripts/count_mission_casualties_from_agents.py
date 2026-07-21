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

count_mission_casualties_from_agents_scripts = [
("count_mission_casualties_from_agents",
    [(party_clear, "p_player_casualties"),
     (party_clear, "p_enemy_casualties"),
     (party_clear, "p_ally_casualties"),
     (assign, "$any_allies_at_the_last_battle", 0),
     #(assign, "$num_routed_us", 0), #these should not assign to 0 here to protect routed agents to spawn again in next turns.
     #(assign, "$num_routed_allies", 0),
     #(assign, "$num_routed_enemies", 0),

     #initialize all routed counts of troops
     (try_for_agents, ":cur_agent"),
       (agent_is_human, ":cur_agent"),
       (agent_get_party_id, ":agent_party", ":cur_agent"),
       (agent_get_troop_id, ":agent_troop_id", ":cur_agent"),
       (troop_set_slot, ":agent_troop_id", slot_troop_player_routed_agents, 0),
       (troop_set_slot, ":agent_troop_id", slot_troop_ally_routed_agents, 0),
       (troop_set_slot, ":agent_troop_id", slot_troop_enemy_routed_agents, 0),
     (try_end),

     (try_for_agents, ":cur_agent"),
       (agent_is_human, ":cur_agent"),
       (agent_get_party_id, ":agent_party", ":cur_agent"),
       (try_begin),
         (neq, ":agent_party", "p_main_party"),
         (agent_is_ally, ":cur_agent"),
         (assign, "$any_allies_at_the_last_battle", 1),
       (try_end),
       #count routed agents in player party, ally parties and enemy parties
       (try_begin),
         #(agent_is_routed, ":cur_agent"), #dckplmc
         (assign, ":continue", 0),
         (agent_get_slot, ":agent_was_running_away", ":cur_agent", slot_agent_is_running_away),
         (try_begin),
             (agent_is_routed, ":cur_agent"),
             (eq, ":agent_was_running_away", 1),
             (assign, ":continue", 1),
         (else_try),
            (agent_is_alive, ":cur_agent"),
            (eq, ":agent_was_running_away", 1),
            (assign, ":continue", 1),
         (try_end),
         (eq, ":continue", 1),
         (try_begin),
           (agent_get_troop_id, ":routed_ag_troop_id", ":cur_agent"),
           (agent_get_party_id, ":routed_ag_party_id", ":cur_agent"),
           #only enemies
           #only regulars

           (try_begin),
             (eq, ":agent_party", "p_main_party"),
             (val_add, "$num_routed_us", 1),
           (else_try),
             (agent_is_ally, ":cur_agent"),
             (val_add, "$num_routed_allies", 1),
           (else_try),
             #for now only count and include routed enemy agents in new routed party.
             (val_add, "$num_routed_enemies", 1),

             (gt, ":routed_ag_party_id", -1),
             (store_faction_of_party, ":faction_of_routed_agent_party", ":routed_ag_party_id"),

             (faction_get_slot, ":num_routed_agents_in_this_faction", ":faction_of_routed_agent_party", slot_faction_num_routed_agents),
             (val_add, ":num_routed_agents_in_this_faction", 1),
             (faction_set_slot, ":faction_of_routed_agent_party", slot_faction_num_routed_agents, ":num_routed_agents_in_this_faction"),
             (party_add_members, "p_routed_enemies", ":routed_ag_troop_id", 1),
           (try_end),
         (try_end),
         (agent_get_troop_id, ":agent_troop_id", ":cur_agent"),
         (try_begin),
           (eq, ":agent_party", "p_main_party"),
           (troop_get_slot, ":player_routed_agents", ":agent_troop_id", slot_troop_player_routed_agents),
           (val_add, ":player_routed_agents", 1),
           (troop_set_slot, ":agent_troop_id", slot_troop_player_routed_agents, ":player_routed_agents"),

         (else_try),
           (agent_is_ally, ":cur_agent"),
           (troop_get_slot, ":ally_routed_agents", ":agent_troop_id", slot_troop_ally_routed_agents),
           (val_add, ":ally_routed_agents", 1),
           (troop_set_slot, ":agent_troop_id", slot_troop_ally_routed_agents, ":ally_routed_agents"),

         (else_try),
           (troop_get_slot, ":enemy_routed_agents", ":agent_troop_id", slot_troop_enemy_routed_agents),
           (val_add, ":enemy_routed_agents", 1),
           (troop_set_slot, ":agent_troop_id", slot_troop_enemy_routed_agents, ":enemy_routed_agents"),

         (try_end),
       (try_end),
       #count and save killed agents in player party, ally parties and enemy parties
       (assign, ":continue", 0),
       (agent_get_slot, ":agent_was_running_away", ":cur_agent", slot_agent_is_running_away),
       (try_begin),
         (neg|agent_is_alive, ":cur_agent"),
         (assign, ":continue", 1),
       (else_try),
        (eq, ":agent_was_running_away", 1),
        (assign, ":continue", 1),
       (try_end),
       (eq, ":continue", 1),
       #(neg|agent_is_alive, ":cur_agent"),
       (agent_get_troop_id, ":agent_troop_id", ":cur_agent"),
       (try_begin),
         (eq, ":agent_party", "p_main_party"),
         (party_add_members, "p_player_casualties", ":agent_troop_id", 1),
         (try_begin),
           (agent_is_wounded, ":cur_agent"),
           (party_wound_members, "p_player_casualties", ":agent_troop_id", 1),
         (try_end),
       (else_try),
         (agent_is_ally, ":cur_agent"),
         (party_add_members, "p_ally_casualties", ":agent_troop_id", 1),
         (try_begin),
           (agent_is_wounded, ":cur_agent"),
           (party_wound_members, "p_ally_casualties", ":agent_troop_id", 1),
         (try_end),
       (else_try),
         (party_add_members, "p_enemy_casualties", ":agent_troop_id", 1),
         (try_begin),
           (agent_is_wounded, ":cur_agent"),
           (party_wound_members, "p_enemy_casualties", ":agent_troop_id", 1),
         (try_end),
       (try_end),
     (try_end),
     ])
]
