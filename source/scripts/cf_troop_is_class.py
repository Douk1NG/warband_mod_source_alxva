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

cf_troop_is_class_scripts = [
("cf_troop_is_class",
    [
        (store_script_param, ":grc", 1),
        (store_script_param, ":troop_no", 2),
        (is_between, ":grc", grc_infantry, grc_everyone), #usually $g_constable_training_type
        (gt, ":troop_no", 0), #this is usually obtained through troop_get_upgrade_troop, sanitize it here

        (troop_get_class, ":class_no", ":troop_no"),
        (eq, ":grc", ":class_no"),
    ])
]
