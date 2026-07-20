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

multiplayer_close_gate_if_it_is_open_scripts = [
#script_multiplayer_close_gate_if_it_is_open
# INPUT: none
# OUTPUT: none
("multiplayer_close_gate_if_it_is_open",
   [
     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_winch_b"),
     (try_for_range, ":cur_prop_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":prop_instance_id", "spr_winch_b", ":cur_prop_instance"),
       (scene_prop_slot_eq, ":prop_instance_id", scene_prop_open_or_close_slot, 1),
       (scene_prop_get_instance, ":effected_object_instance_id", "spr_portcullis", ":cur_prop_instance"),
       (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),
       (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 1),
     (try_end),
   ])
]
