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

multiplayer_server_before_mission_start_common_scripts = [
#script_multiplayer_server_before_mission_start_common
# INPUT: none
# OUTPUT: none
("multiplayer_server_before_mission_start_common",
   [
     (try_begin),
       (scene_allows_mounted_units),
       (assign, "$g_horses_are_avaliable", 1),
     (else_try),
       (assign, "$g_horses_are_avaliable", 0),
     (try_end),
     (scene_set_day_time, 15),
     (assign, "$g_multiplayer_mission_end_screen", 0),

     (get_max_players, ":num_players"),
     (try_for_range, ":player_no", 0, ":num_players"),
       (player_is_active, ":player_no"),
       (call_script, "script_multiplayer_init_player_slots", ":player_no"),
       (assign, ":initial_gold", multi_initial_gold_value),
       (val_mul, ":initial_gold", "$g_multiplayer_initial_gold_multiplier"),
       (val_div, ":initial_gold", 100),
       (player_set_gold, ":player_no", ":initial_gold"),
       (player_set_slot, ":player_no", slot_player_first_spawn, 1), #not required in siege, bt, fd
     (try_end),
     ])
]
