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

get_enterprise_prosperity_numerator_scripts = [
("get_enterprise_prosperity_numerator", [
	#reg0: prosperity quantity numerator (denominator is 100) for the given center.
	#      very poor (<30): 50 | poor (30-49): 75 | normal (50-69): 100 | rich (70-89): 150 | very rich (90-100): 200
	#Used so rich towns produce more goods (and earn more) while poor towns produce less.
	# INPUTS:
	#   arg1: center
      (store_script_param, ":center", 1),
      (party_get_slot, ":prosperity", ":center", slot_town_prosperity),
      (try_begin),
        (lt, ":prosperity", 30),
        (assign, reg0, 50),
      (else_try),
        (lt, ":prosperity", 50),
        (assign, reg0, 75),
      (else_try),
        (lt, ":prosperity", 70),
        (assign, reg0, 100),
      (else_try),
        (lt, ":prosperity", 90),
        (assign, reg0, 150),
      (else_try),
        (assign, reg0, 200),
      (try_end),
    ])
]
