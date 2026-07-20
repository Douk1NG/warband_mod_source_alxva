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

multiplayer_init_player_slots_scripts = [
#script_multiplayer_init_player_slots
# Input: arg1 = player_no
# Output: none
("multiplayer_init_player_slots",
   [
     (store_script_param, ":player_no", 1),
     (call_script, "script_multiplayer_clear_player_selected_items", ":player_no"),
     (player_set_slot, ":player_no", slot_player_spawned_this_round, 0),
     (player_set_slot, ":player_no", slot_player_last_rounds_used_item_earnings, 0),
     (player_set_slot, ":player_no", slot_player_poll_disabled_until_time, 0),

     (player_set_slot, ":player_no", slot_player_bot_type_1_wanted, 0),
     (player_set_slot, ":player_no", slot_player_bot_type_2_wanted, 0),
     (player_set_slot, ":player_no", slot_player_bot_type_3_wanted, 0),
     (player_set_slot, ":player_no", slot_player_bot_type_4_wanted, 0),
     ])
]
