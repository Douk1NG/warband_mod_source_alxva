# ======================================================================
# SHARED DEPENDENCY
# Entity: change_player_right_to_rule (script)
# Called by menus in 2 domains: cheats, notifications
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

change_player_right_to_rule_scripts = [
(
   "change_player_right_to_rule",
   [
     (store_script_param_1, ":right_to_rule_dif"),
     (val_add, "$player_right_to_rule", ":right_to_rule_dif"),
     (val_clamp, "$player_right_to_rule", 0, 100),
     (try_begin),
       (gt, ":right_to_rule_dif", 0),
       (display_message, "@You gain right to rule.", message_positive),
     (else_try),
       (lt, ":right_to_rule_dif", 0),
       (display_message, "@You lose right to rule.", message_negative),
     (try_end),
   ])
]
