# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

rename_court_menu = [
(
    "rename_court",0,
    "{!}This menu jumps to the rename presentation",
    "none",
    [
    # (call_script, "script_change_player_right_to_rule", 1), #handled in dialogues
    (assign, reg0, "$temp"),
    (display_message, "@{reg0}"),
    (try_begin),
        #(eq, "$temp", 1), #avoid menus getting stuck
        (jump_to_menu, "mnu_auto_return_to_map"),
    (try_end),
    (assign, "$g_presentation_state", rename_center),
    (call_script, "script_add_log_entry", logent_player_renamed_capital, "trp_player", "$g_player_court", -1, -1),
    (assign, "$temp", 1),
    (start_presentation, "prsnt_name_kingdom"),

    ],
    [])
]
