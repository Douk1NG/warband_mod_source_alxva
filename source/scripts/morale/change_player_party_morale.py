# ======================================================================
# SHARED DEPENDENCY
# Entity: change_player_party_morale (script)
# Called by menus in 3 domains: battle, camp, village
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

change_player_party_morale_scripts = [
("change_player_party_morale",
    [
      (store_script_param_1, ":morale_dif"),
      (party_get_morale, ":cur_morale", "p_main_party"),
      (val_clamp, ":cur_morale", 0, 100),

      (store_add, ":new_morale", ":cur_morale", ":morale_dif"),
      (val_clamp, ":new_morale", 0, 100),

      (party_set_morale, "p_main_party", ":new_morale"),
      #SB : colorize message
      (try_begin),
        (lt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":cur_morale", ":new_morale"),
        (display_message, "str_party_lost_morale", message_negative),
      (else_try),
        (gt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":new_morale", ":cur_morale"),
        (display_message, "str_party_gained_morale", message_positive),
      (try_end),
  ])
]
