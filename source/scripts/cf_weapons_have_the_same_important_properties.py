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

cf_weapons_have_the_same_important_properties_scripts = [
("cf_weapons_have_the_same_important_properties", 
    [
      (store_script_param, ":item_1", 1),
      (store_script_param, ":item_2", 2),
      (assign, ":item_1_has_property_1", 0),
      (assign, ":item_1_has_property_2", 0),
      (assign, ":item_1_has_property_3", 0),
      (assign, ":item_1_has_property_4", 0),
      (try_begin),
        (item_has_property, ":item_1", itp_cant_reload_on_horseback),
        (assign, ":item_1_has_property_1", 1),
      (try_end),
      (try_begin),
        (item_has_property, ":item_1", itp_two_handed),
        (assign, ":item_1_has_property_2", 1),
      (try_end),
      (try_begin),
        (item_has_property, ":item_1", itp_cant_use_on_horseback),
        (assign, ":item_1_has_property_3", 1),
      (try_end),
      (try_begin),
        (item_has_property, ":item_1", itp_couchable),
        (assign, ":item_1_has_property_4", 1),
      (try_end),
      (assign, ":item_2_has_property_1", 0),
      (assign, ":item_2_has_property_2", 0),
      (assign, ":item_2_has_property_3", 0),
      (assign, ":item_2_has_property_4", 0),
      (try_begin),
        (item_has_property, ":item_2", itp_cant_reload_on_horseback),
        (assign, ":item_2_has_property_1", 1),
      (try_end),
      (try_begin),
        (item_has_property, ":item_2", itp_two_handed),
        (assign, ":item_2_has_property_2", 1),
      (try_end),
      (try_begin),
        (item_has_property, ":item_2", itp_cant_use_on_horseback),
        (assign, ":item_2_has_property_3", 1),
      (try_end),
      (try_begin),
        (item_has_property, ":item_2", itp_couchable),
        (assign, ":item_2_has_property_4", 1),
      (try_end),
      (eq, ":item_1_has_property_1", ":item_2_has_property_1"),
      (eq, ":item_1_has_property_2", ":item_2_has_property_2"),
      (eq, ":item_1_has_property_3", ":item_2_has_property_3"),
      (eq, ":item_1_has_property_4", ":item_2_has_property_4"),
    ])
]
