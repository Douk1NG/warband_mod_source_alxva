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

multiplayer_move_moveable_objects_initial_positions_scripts = [
#script_multiplayer_move_moveable_objects_initial_positions
# INPUT: none
# OUTPUT: none
("multiplayer_move_moveable_objects_initial_positions",
   [
     (call_script, "script_move_object_to_nearest_entry_point", "spr_siege_ladder_move_6m"),
     (call_script, "script_move_object_to_nearest_entry_point", "spr_siege_ladder_move_8m"),
     (call_script, "script_move_object_to_nearest_entry_point", "spr_siege_ladder_move_10m"),
     (call_script, "script_move_object_to_nearest_entry_point", "spr_siege_ladder_move_12m"),
     (call_script, "script_move_object_to_nearest_entry_point", "spr_siege_ladder_move_14m"),
   ])
]
