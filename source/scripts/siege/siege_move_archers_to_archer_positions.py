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

siege_move_archers_to_archer_positions_scripts = [
# script_describe_relation_to_s63
# Input: none
# Output: none
("siege_move_archers_to_archer_positions",
   [
     (try_for_agents, ":agent_no"),
       (agent_is_alive, ":agent_no"),
       (agent_slot_eq, ":agent_no", slot_agent_is_not_reinforcement, 0),
       (agent_is_defender, ":agent_no"),
       (agent_get_class, ":agent_class", ":agent_no"),
       (agent_get_troop_id, ":agent_troop", ":agent_no"),
       (eq, ":agent_class", grc_archers),
       (try_begin),
         (agent_slot_eq, ":agent_no", slot_agent_target_entry_point, 0),
         (store_random_in_range, ":random_entry_point", 40, 44), #40, 48? dckplmc
         (agent_set_slot, ":agent_no", slot_agent_target_entry_point, ":random_entry_point"),
       (try_end),
       (try_begin),
         (agent_get_position, pos0, ":agent_no"),
         (entry_point_get_position, pos1, ":random_entry_point"),
         (get_distance_between_positions, ":dist", pos0, pos1),
         (lt, ":dist", 300),
         (agent_clear_scripted_mode, ":agent_no"),
         (agent_set_slot, ":agent_no", slot_agent_is_in_scripted_mode, 0),
         (agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement, 1),
         (str_store_troop_name, s1, ":agent_troop"),
         (assign, reg0, ":agent_no"),
#         (display_message, "@{s1} ({reg0}) reached pos"),
       (else_try),
         (agent_get_simple_behavior, ":agent_sb", ":agent_no"),
         (agent_get_combat_state, ":agent_cs", ":agent_no"),
         (this_or_next|eq, ":agent_sb", aisb_ranged),
         (eq, ":agent_sb", aisb_go_to_pos),#scripted mode
         (eq, ":agent_cs", 7), # 7 = no visible targets (state for ranged units)
         (try_begin),
           (agent_slot_eq, ":agent_no", slot_agent_is_in_scripted_mode, 0),
           (agent_set_scripted_destination, ":agent_no", pos1, 0),
           (agent_set_slot, ":agent_no", slot_agent_is_in_scripted_mode, 1),
           (str_store_troop_name, s1, ":agent_troop"),
           (assign, reg0, ":agent_no"),
#           (display_message, "@{s1} ({reg0}) moving to pos"),
         (try_end),
       (else_try),
         (try_begin),
           (agent_slot_eq, ":agent_no", slot_agent_is_in_scripted_mode, 1),
           (agent_clear_scripted_mode, ":agent_no"),
           (agent_set_slot, ":agent_no", slot_agent_is_in_scripted_mode, 0),
           (str_store_troop_name, s1, ":agent_troop"),
           (assign, reg0, ":agent_no"),
#           (display_message, "@{s1} ({reg0}) seeing target or changed mode"),
         (try_end),
       (try_end),
     (try_end),
     ])
]
