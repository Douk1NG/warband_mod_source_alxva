# ======================================================================
# SHARED DEPENDENCY
# Entity: set_player_relation_with_faction (script)
# Called by menus in 2 domains: castle, notifications
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

set_player_relation_with_faction_scripts = [
# script_set_player_relation_with_faction
# Input: arg1 = faction_no, arg2 = relation
# Output: none
("set_player_relation_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":relation"),

      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (store_sub, ":reln_dif", ":relation", ":player_relation"),
      (call_script, "script_change_player_relation_with_faction", ":faction_no", ":reln_dif"),
      ])
]
