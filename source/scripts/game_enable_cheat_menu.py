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

game_enable_cheat_menu_scripts = [
#script_get_army_size_from_slider_value
# This script is called from the game engine when user enters "cheatmenu from command console (ctrl+~).
# INPUT:
# none
# OUTPUT:
# none
("game_enable_cheat_menu",
    [
      (store_script_param, ":input", 1),
      (try_begin),
        (eq, ":input", 0),
        (assign, "$cheat_mode", 0),
      (else_try),
        (eq, ":input", 1),
        (assign, "$cheat_mode", 1),
        #SB : flavour text
        (call_script, "script_objectionable_action", tmt_honest, "str_stop_cheating"),
      (try_end),
      (try_begin),
        (neg|is_presentation_active, "prsnt_modify_slots"),
        # (assign, "$g_talk_troop", ":input"),
        (assign, "$g_presentation_state", 0),
        (assign, "$g_presentation_input", rename_companion),
        (start_presentation, "prsnt_modify_slots"),
      (try_end),
      ])
]
