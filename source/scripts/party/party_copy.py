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

party_copy_scripts = [
("party_copy",
    [
      (assign, "$g_move_heroes", 1),
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_clear, ":target_party"),
      (call_script, "script_party_add_party", ":target_party", ":source_party"),
  ])
]
