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

game_multiplayer_event_duel_offered_scripts = [
# script_find_number_of_agents_constant
# Input: arg1 = agent_no
# Output: none
("game_multiplayer_event_duel_offered",
   [
     (store_script_param, ":agent_no", 1),
     (get_player_agent_no, ":player_agent_no"),
     (try_begin),
       (agent_is_active, ":player_agent_no"),
       (this_or_next|agent_slot_eq, ":player_agent_no", slot_agent_in_duel_with, -1),
       (agent_check_offer_from_agent, ":player_agent_no", ":agent_no"),
       (neg|agent_slot_eq, ":player_agent_no", slot_agent_in_duel_with, ":agent_no"), #don't allow spamming duel offers during countdown
       (multiplayer_send_int_to_server, multiplayer_event_offer_duel, ":agent_no"),
       (agent_get_player_id, ":player_no", ":agent_no"),
       (try_begin),
         (player_is_active, ":player_no"),
         (str_store_player_username, s0, ":player_no"),
       (else_try),
         (str_store_agent_name, s0, ":agent_no"),
       (try_end),
       (display_message, "str_a_duel_request_is_sent_to_s0"),
     (try_end),
     ])
]
