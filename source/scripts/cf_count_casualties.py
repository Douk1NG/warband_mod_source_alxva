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

cf_count_casualties_scripts = [
("cf_count_casualties", [
      (assign, ":num_casualties", 0),
      (try_for_agents,":cur_agent"),
        (try_begin),
          (this_or_next | agent_is_wounded, ":cur_agent"),
          (this_or_next | agent_slot_eq, ":cur_agent", slot_agent_is_running_away, 1),
          (neg | agent_is_alive, ":cur_agent"),
          (val_add, ":num_casualties", 1),
        (try_end),
      (try_end),
      (assign, reg0, ":num_casualties"),
      (gt, ":num_casualties", 0)])
]
