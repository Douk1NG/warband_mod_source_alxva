# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

multiplayer_accept_duel_scripts = [
# script_multiplayer_accept_duel
# Input: arg1 = agent_no, arg2 = agent_no_offerer
# Output: none
("multiplayer_accept_duel",
   [
     (store_script_param, ":agent_no", 1),
     (store_script_param, ":agent_no_offerer", 2),
     (try_begin),
       (agent_slot_ge, ":agent_no", slot_agent_in_duel_with, 0),
       (agent_get_slot, ":ex_duelist", ":agent_no", slot_agent_in_duel_with),
       (agent_is_active, ":ex_duelist"),
       (agent_clear_relations_with_agents, ":ex_duelist"),
       (agent_set_slot, ":ex_duelist", slot_agent_in_duel_with, -1),
       (agent_get_player_id, ":player_no", ":ex_duelist"),
       (try_begin),
         (player_is_active, ":player_no"), #might be AI
         (multiplayer_send_int_to_player, ":player_no", multiplayer_event_cancel_duel, ":agent_no"),
       (else_try),
         (agent_force_rethink, ":ex_duelist"),
       (try_end),
     (try_end),
     (try_begin),
       (agent_slot_ge, ":agent_no_offerer", slot_agent_in_duel_with, 0),
       (agent_get_slot, ":ex_duelist", ":agent_no_offerer", slot_agent_in_duel_with),
       (agent_is_active, ":ex_duelist"),
       (agent_clear_relations_with_agents, ":ex_duelist"),
       (agent_set_slot, ":ex_duelist", slot_agent_in_duel_with, -1),
       (try_begin),
         (player_is_active, ":player_no"), #might be AI
         (multiplayer_send_int_to_player, ":player_no", multiplayer_event_cancel_duel, ":agent_no_offerer"),
       (else_try),
         (agent_force_rethink, ":ex_duelist"),
       (try_end),
     (try_end),
     (agent_set_slot, ":agent_no", slot_agent_in_duel_with, ":agent_no_offerer"),
     (agent_set_slot, ":agent_no_offerer", slot_agent_in_duel_with, ":agent_no"),
     (agent_clear_relations_with_agents, ":agent_no"),
     (agent_clear_relations_with_agents, ":agent_no_offerer"),
##     (agent_add_relation_with_agent, ":agent_no", ":agent_no_offerer", -1),
##     (agent_add_relation_with_agent, ":agent_no_offerer", ":agent_no", -1),
     (agent_get_player_id, ":player_no", ":agent_no"),
     (store_mission_timer_a, ":mission_timer"),
     (try_begin),
       (player_is_active, ":player_no"), #might be AI
       (multiplayer_send_int_to_player, ":player_no", multiplayer_event_start_duel, ":agent_no_offerer"),
     (else_try),
       (agent_force_rethink, ":agent_no"),
     (try_end),
     (agent_set_slot, ":agent_no", slot_agent_duel_start_time, ":mission_timer"),
     (agent_get_player_id, ":agent_no_offerer_player", ":agent_no_offerer"),
     (try_begin),
       (player_is_active, ":agent_no_offerer_player"), #might be AI
       (multiplayer_send_int_to_player, ":agent_no_offerer_player", multiplayer_event_start_duel, ":agent_no"),
     (else_try),
       (agent_force_rethink, ":agent_no_offerer"),
     (try_end),
     (agent_set_slot, ":agent_no_offerer", slot_agent_duel_start_time, ":mission_timer"),
     ])
]
