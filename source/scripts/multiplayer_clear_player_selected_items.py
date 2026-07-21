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

multiplayer_clear_player_selected_items_scripts = [
#script_multiplayer_clear_player_selected_items
# Input: arg1 = player_no
# Output: none
("multiplayer_clear_player_selected_items",
   [
     (store_script_param, ":player_no", 1),
     (try_for_range, ":slot_no", slot_player_selected_item_indices_begin, slot_player_selected_item_indices_end),
       (player_set_slot, ":player_no", ":slot_no", -1),
     (try_end),
     ])
]
