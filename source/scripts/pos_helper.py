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

pos_helper_scripts = [
("pos_helper",
 [  (store_script_param, ":ti_on", 1),
    (try_begin),
        (eq, ":ti_on", 1),# ti_on_presentation_load
		(create_text_overlay, "$g_little_pos_helper", "@00,00"),
		(overlay_set_color, "$g_little_pos_helper", 0xFFFFFFFF),
		(position_set_x, pos1, 10),
		(position_set_y, pos1, 700),
		(overlay_set_position, "$g_little_pos_helper", pos1),
    (try_end),
    (try_begin),
        (eq, ":ti_on", 2),# ti_on_presentation_run
		(mouse_get_position, pos1),
		(position_get_x, reg1, pos1),
		(position_get_y, reg2, pos1),
		(overlay_set_text, "$g_little_pos_helper", "@{reg1},{reg2}"),
    (try_end),
 ])
]
