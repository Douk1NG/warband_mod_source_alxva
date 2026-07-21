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

cf_division_data_available_scripts = [
("cf_division_data_available", [
      (assign, ":evidence", 0),
      (try_for_range, ":team", 0, 4),
        (team_slot_ge, ":team", slot_team_size, 1),
        (assign, ":evidence", 1),
      (try_end),
      (neq, ":evidence", 0)])
]
