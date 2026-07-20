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

change_color_scripts = [
("change_color",
    [
      (call_script, "script_get_dest_color_from_rgb", reg2, reg3, reg4),
      (assign, ":cur_color", reg0),
      (overlay_set_color, "$g_presentation_obj_2", ":cur_color"),
      (try_begin),
        (eq, "$g_presentation_state", recolor_kingdom),
        (troop_get_slot, ":cur_faction", "trp_temp_array_a", "$temp"),
        (faction_set_color, ":cur_faction", ":cur_color"),
      (else_try),
        (eq, "$g_presentation_state", recolor_heraldic),
        (troop_get_slot, ":banner", "trp_player", slot_troop_banner_scene_prop),
        (val_sub, ":banner", banner_scene_props_begin),
        (troop_set_slot, "trp_banner_background_color_array", ":banner", ":cur_color"),
      (else_try),
        (eq, "$g_presentation_state", recolor_groups),
        (troop_set_slot, "trp_multiplayer_data", "$temp", ":cur_color"),
      (try_end),
      (call_script, "script_convert_rgb_code_to_html_code", reg2, reg3, reg4),
      (overlay_set_text, "$g_presentation_obj_9", "str_html"),
    ])
]
