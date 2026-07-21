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

get_improvement_details_scripts = [
("get_improvement_details",
    [(store_script_param, ":improvement_no", 1),
     (try_begin),
       (eq, ":improvement_no", slot_center_has_manor),
       (str_store_string, s0, "@Manor"),
       (str_store_string, s1, "@A manor lets you rest at the village and pay your troops half wages while you rest."),
       (assign, reg0, 8000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_fish_pond),
       (str_store_string, s0, "@Mill"),
       (str_store_string, s1, "@A mill increases village prosperity by 5%."),
       (assign, reg0, 6000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_watch_tower),
       (str_store_string, s0, "@Watch Tower"),
       (str_store_string, s1, "@A watch tower lets the villagers raise alarm earlier. The time it takes for enemies to loot the village increases by 50%."),
       (assign, reg0, 5000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_school),
       (str_store_string, s0, "@School"),
       (str_store_string, s1, "@A shool increases the loyality of the villagers to you by +1 every month."),
       (assign, reg0, 9000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_messenger_post),
       (str_store_string, s0, "@Messenger Post"),
       (str_store_string, s1, "@A messenger post lets the inhabitants send you a message whenever enemies are nearby, even if you are far away from here."),
       (assign, reg0, 4000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_prisoner_tower),
       (str_store_string, s0, "@Prison Tower"),
       (str_store_string, s1, "@A prison tower reduces the chance of captives held here running away successfully."),
       (assign, reg0, 7000),
     (try_end),
     ])
]
