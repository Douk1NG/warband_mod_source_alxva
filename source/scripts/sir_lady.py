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

sir_lady_scripts = [
#/custom armor
("sir_lady", [ #male 1, female 0, (player, talk_troop) -> (reg33, reg6)
		(troop_get_type, ":is_female", "trp_player"),
		(try_begin),
			(ge, ":is_female", 1),
			(assign, reg33, 0),
		(else_try),
			(assign, reg33, 1),
		(try_end),
		#(troop_get_type, ":is_female", "$g_talk_troop"),
		#(try_begin),
		#	(ge, ":is_female", 1),
		#	(assign, reg6, 0),
		#(else_try),
		#	(assign, reg6, 1),
		#(try_end),
	]
  )
]
