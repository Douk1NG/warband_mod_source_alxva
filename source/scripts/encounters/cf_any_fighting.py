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

cf_any_fighting_scripts = [
("cf_any_fighting", [
      (assign, ":any_fighting", 0),
      (try_for_range, ":team", 0, 4),
        (team_slot_ge, ":team", slot_team_size, 1),
        (eq, ":any_fighting", 0),
        (assign, ":num_divs", 9),
        (try_for_range, ":division", 0, ":num_divs"),
          (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
          (team_slot_ge, ":team", ":slot", 1),
          (assign, ":any_fighting", 1),
          (assign, ":num_divs", 0),
        (try_end),
      (try_end),

      #lag this check to be sure
      (store_mission_timer_c, ":time_stamp"),
      (try_begin),	#time lag
        (gt, ":any_fighting", 0),
        (assign, "$teams_last_fighting", ":time_stamp"),
      (try_end),
      (assign, ":fighting_finished", formation_reform_interval),
      (val_max, ":fighting_finished", 5),
      (val_add, ":fighting_finished", "$teams_last_fighting"),
      (gt, ":fighting_finished", ":time_stamp"),])
]
