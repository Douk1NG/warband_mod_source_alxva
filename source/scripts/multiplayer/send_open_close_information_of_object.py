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

send_open_close_information_of_object_scripts = [
("send_open_close_information_of_object",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":scene_prop_no", 2),

     (scene_prop_get_num_instances, ":num_instances", ":scene_prop_no"),

     (try_for_range, ":instance_no", 0, ":num_instances"),
       (scene_prop_get_instance, ":instance_id", ":scene_prop_no", ":instance_no"),
       (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),
       (try_begin),
         (eq, ":opened_or_closed", 1),
         (multiplayer_send_int_to_player, ":player_no", multiplayer_event_set_scene_prop_open_or_close, ":instance_id"),
       (try_end),
     (try_end),
     ])
]
