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

multiplayer_calculate_cur_selected_items_cost_scripts = [
#script_multiplayer_calculate_cur_selected_items_cost
# Input: arg1 = player_no
# Output: reg0: total_cost
("multiplayer_calculate_cur_selected_items_cost",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":calculation_type", 2), #0 for normal calculation
     (assign, ":total_cost", 0),
     (player_get_troop_id, ":troop_no", ":player_no"),

     (try_begin),
       (eq, ":calculation_type", 0),
       (assign, ":begin_cond", slot_player_cur_selected_item_indices_begin),
       (assign, ":end_cond", slot_player_cur_selected_item_indices_end),
     (else_try),
       (assign, ":begin_cond", slot_player_selected_item_indices_begin),
       (assign, ":end_cond", slot_player_selected_item_indices_end),
     (try_end),

     (try_for_range, ":i_item", ":begin_cond", ":end_cond"),
       (player_get_slot, ":item_id", ":player_no", ":i_item"),
       (ge, ":item_id", 0), #might be -1 for horses etc.
       (call_script, "script_multiplayer_get_item_value_for_troop", ":item_id", ":troop_no"),
       (val_add, ":total_cost", reg0),
     (try_end),
     (assign, reg0, ":total_cost"),
     ])
]
