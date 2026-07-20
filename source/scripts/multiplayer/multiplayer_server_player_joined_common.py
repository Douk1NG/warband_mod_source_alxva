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

multiplayer_server_player_joined_common_scripts = [
#script_multiplayer_server_player_joined_common
# INPUT: arg1 = player_no
# OUTPUT: none
("multiplayer_server_player_joined_common",
   [
     (store_script_param, ":player_no", 1),
     (try_begin),
       (this_or_next|player_is_active, ":player_no"),
       (eq, ":player_no", 0),
       (call_script, "script_multiplayer_init_player_slots", ":player_no"),
       (store_mission_timer_a, ":player_join_time"),
       (player_set_slot, ":player_no", slot_player_join_time, ":player_join_time"),
       (player_set_slot, ":player_no", slot_player_first_spawn, 1),
       #fight and destroy only
       (player_set_slot, ":player_no", slot_player_damage_given_to_target_1, 0),
       (player_set_slot, ":player_no", slot_player_damage_given_to_target_2, 0),
       #fight and destroy only end
       (try_begin),
         (multiplayer_is_server),
         (assign, ":initial_gold", multi_initial_gold_value),
         (val_mul, ":initial_gold", "$g_multiplayer_initial_gold_multiplier"),
         (val_div, ":initial_gold", 100),
         (player_set_gold, ":player_no", ":initial_gold"),
         (call_script, "script_multiplayer_send_initial_information", ":player_no"),
       (try_end),
     (try_end),
     ])
]
