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

move_flag_scripts = [
("move_flag",
   [
     (store_script_param, ":shown_flag_id", 1),
     (store_script_param, ":shown_flag_move_time", 2),

     (try_begin),
       (multiplayer_is_server), #added after auto-animating

       (try_begin),
         (eq, ":shown_flag_move_time", 0), #stop
         (prop_instance_stop_animating, ":shown_flag_id"),
       (else_try),
         (prop_instance_animate_to_position, ":shown_flag_id", pos0, ":shown_flag_move_time"),
       (try_end),
     (try_end),
   ])
]
