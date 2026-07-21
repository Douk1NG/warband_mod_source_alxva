# ======================================================================
# SHARED DEPENDENCY
# Entity: party_wound_all_members (script)
# Called by menus in 3 domains: battle, cheats, siege
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

party_wound_all_members_scripts = [
("party_wound_all_members",
    [
      (store_script_param_1, ":party_no"),

      (call_script, "script_party_wound_all_members_aux", ":party_no"),
  ])
]
