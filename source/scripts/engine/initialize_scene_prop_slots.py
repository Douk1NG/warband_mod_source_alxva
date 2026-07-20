# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

initialize_scene_prop_slots_scripts = [
#script_initialize_scene_prop_slots
# INPUT: arg1 = scene_prop_no
# OUTPUT: none
("initialize_scene_prop_slots",
   [
     (store_script_param, ":scene_prop_no", 1),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", ":scene_prop_no"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", ":scene_prop_no", ":cur_instance"),
       (try_for_range, ":cur_slot", 0, scene_prop_slots_end),
         (scene_prop_set_slot, ":cur_instance_id", ":cur_slot", 0),
       (try_end),
     (try_end),
     ])
]
