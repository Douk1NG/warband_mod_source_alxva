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

multiplayer_send_item_selections_scripts = [
#script_multiplayer_send_item_selections
# Input: none
# Output: none
("multiplayer_send_item_selections",
   [
     (multiplayer_get_my_player, ":my_player_no"),
     (try_for_range, ":i_item", slot_player_selected_item_indices_begin, slot_player_selected_item_indices_end),
       (player_get_slot, ":item_id", ":my_player_no", ":i_item"),
       (multiplayer_send_2_int_to_server, multiplayer_event_set_item_selection, ":i_item", ":item_id"),
     (try_end),
     ])
]
