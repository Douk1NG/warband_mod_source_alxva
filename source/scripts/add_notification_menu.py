# ======================================================================
# SHARED DEPENDENCY
# Entity: add_notification_menu (script)
# Called by menus in 2 domains: kingdom_management, notifications
# ======================================================================

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

add_notification_menu_scripts = [
("add_notification_menu",
    [
      (try_begin),
        (eq, "$g_infinite_camping", 0),
        (store_script_param, ":menu_no", 1),
        (store_script_param, ":menu_var_1", 2),
        (store_script_param, ":menu_var_2", 3),
        (assign, ":end_cond", 1),
        (try_for_range, ":cur_slot", 0, ":end_cond"),
          (try_begin),
            (troop_slot_ge, "trp_notification_menu_types", ":cur_slot", 1),
            (val_add, ":end_cond", 1),
          (else_try),
            (troop_set_slot, "trp_notification_menu_types", ":cur_slot", ":menu_no"),
            (troop_set_slot, "trp_notification_menu_var1", ":cur_slot", ":menu_var_1"),
            (troop_set_slot, "trp_notification_menu_var2", ":cur_slot", ":menu_var_2"),
          (try_end),
        (try_end),
      (try_end),
      ])
]
