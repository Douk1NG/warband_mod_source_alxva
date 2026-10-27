# -*- coding: cp1254 -*-
import string
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
#SB: import skills from ID_skills import *
from module_constants import *
##diplomacy start+ Import for use with terrain advantage
from header_terrain_types import *
from module_items import *
#SB : import colors
from module_factions import *
from header_items import *
##diplomacy end
from compiler import *

formation_mod_option = ("formation_mod_option", 0, mesh_load_window, [
    (ti_on_presentation_load, [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
        (call_script, "script_formation_create_ui", 0),
    ]),

    (ti_on_presentation_run, [
        (try_begin),
          (this_or_next|key_clicked, key_escape),
          (key_clicked, key_xbox_start),
          (presentation_set_duration, 0),
        (try_end),
    ]),

    (ti_on_presentation_event_state_change, [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
        (call_script, "script_formation_handle_event", ":object", ":value"),
    ]),
])
