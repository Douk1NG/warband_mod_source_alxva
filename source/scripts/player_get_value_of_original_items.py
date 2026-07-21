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

player_get_value_of_original_items_scripts = [
("player_get_value_of_original_items",
    [
      (store_script_param, ":player_no", 1),
      (store_script_param, ":agent_no", 2),
      (store_script_param, ":troop_id", 3),
      (assign, ":total_equipment_cost", 0),
      (try_for_range, ":i_item_slot", 0, 8),
          (neg|player_item_slot_is_picked_up, ":player_no", ":i_item_slot"),
          (agent_get_item_slot, ":item_id", ":agent_no", ":i_item_slot"), #value between 0-7, order is weapon1, weapon2, weapon3, weapon4, head_armor, body_armor, leg_armor, hand_armor
          #(player_get_item_id, ":item_id", ":player_no", ":i_item_slot"), #only for server
          (neq, ":item_id", -1),
          (call_script, "script_multiplayer_get_item_value_for_troop", ":item_id", ":troop_id"),
          (val_add, ":total_equipment_cost", reg0),

          #Debugging
          #(assign, reg1, ":total_equipment_cost"),
          #(str_store_item_name, s0, ":item_id"),
          #(multiplayer_send_string_to_player, ":player_no", multiplayer_event_show_server_message, "@{s0} for {reg0}g added to total equipment cost, which is now: {reg1}g"),
          ##
      (try_end),
      (try_for_agents, ":cur_horse"),
         #Check all horses in the scene and see if one of them is agent_no's bought horse. Won't be enough to just do (agent_get_horse, ":horse", ":agent_no"),
         #since you get money back for a bought horse, even if you have dismounted it, if the horse is still alive and has no other rider.
         (agent_is_alive, ":cur_horse"),
         (neg|agent_is_human, ":cur_horse"),  #Spawned agent is horse
         (agent_get_slot, ":agent_no_bought_horse", ":agent_no", slot_agent_bought_horse),
         (eq, ":agent_no_bought_horse", ":cur_horse"),
         (assign, ":add_horse_cost_to_equipment_value", 0),
         (try_begin),
             (agent_get_rider, ":rider_agent_id", ":cur_horse"),
             (try_begin),
                 (neq, ":rider_agent_id", -1),
                 (neg|agent_is_non_player, ":rider_agent_id"),
                 (agent_get_slot, ":agent_no_bought_horse", ":rider_agent_id", slot_agent_bought_horse),
                 (eq, ":agent_no_bought_horse", ":cur_horse"), #agent_no is mounted on the same horse he bought
                 (assign, ":add_horse_cost_to_equipment_value", 1),

                 #Debugging
                 #(agent_get_item_id, ":mount_type", ":cur_horse"), #(works only for horses, returns -1 otherwise)
                 #(str_store_item_name, s0, ":mount_type"),
                 #(multiplayer_send_string_to_player, ":player_no", multiplayer_event_show_server_message, "@You are mounted on your bought {s0} and will get money for it"),
                 ##
             (else_try),
                 (eq, ":rider_agent_id", -1), #If cur_horse doesn't have a rider
                 (agent_get_horse, ":agent_no_mount", ":agent_no"),
                 (eq, ":agent_no_mount", -1), #If agent_no is not mounted on another horse
                 (agent_get_slot, ":agent_no_bought_horse", ":agent_no", slot_agent_bought_horse),
                 (eq, ":agent_no_bought_horse", ":cur_horse"),
                 (assign, ":add_horse_cost_to_equipment_value", 1),

                 #Debugging
                 #(agent_get_item_id, ":mount_type", ":cur_horse"), #(works only for horses, returns -1 otherwise)
                 #(str_store_item_name, s0, ":mount_type"),
                 #(multiplayer_send_string_to_player, ":player_no", multiplayer_event_show_server_message, "@Your bought {s0} is alive so you get money for it"),
                 ##
            (try_end),
            (eq, ":add_horse_cost_to_equipment_value", 1),
            (agent_get_item_id, ":cur_mount_type", ":cur_horse"), #Checks which type the horse is
            (call_script, "script_multiplayer_get_item_value_for_troop", ":cur_mount_type", ":troop_id"),
            (val_add, ":total_equipment_cost", reg0),
            (multiplayer_send_string_to_player, ":player_no", multiplayer_event_show_server_message, "@Added money for your old horse"),
         (try_end),
      (try_end),
      (agent_set_slot, ":agent_no", slot_agent_bought_horse, -1),
      (assign, reg0, ":total_equipment_cost"),
     ])
]
