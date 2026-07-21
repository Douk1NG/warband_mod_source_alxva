# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

cf_is_thrusting_weapon_scripts = [
("cf_is_thrusting_weapon", [
      (store_script_param, ":item", 1),
      (is_between, ":item", weapons_begin, weapons_end),
      (item_get_thrust_damage, ":thrust_damage", ":item"),
      (item_get_swing_damage, ":swing_damage", ":item"),
      (val_mul, ":thrust_damage", 3),	#it seems thrusts connect faster than swings (as they should) although the
      #animations seem to take the same time
      (val_div, ":thrust_damage", 2),	#factor this in with approximation 2*PI/4 (distance swing must travel vs.
      #thrust) This ignores length, which creates too large a differential.  This is
      #a happy medium.
      (ge, ":thrust_damage", ":swing_damage"),])
]
