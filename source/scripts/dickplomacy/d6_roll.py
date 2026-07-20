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

d6_roll_scripts = [
# script_d6_roll # "script_d6_roll"
# Input: arg1 = none
# Output: reg0 = mesh
# Output: reg1 = pip
("d6_roll",
   [(store_script_param, ":d6", 1),
    (try_begin),
        (try_begin),
		    (eq,":d6", 0),
		    (store_random_in_range,":d6",1,7),
		(try_end),
		(try_begin),
		    (eq,":d6",1),
		    (assign,reg0,"mesh_mmc_dice_1"),
        (else_try),
		    (eq,":d6",2),
		    (assign,reg0,"mesh_mmc_dice_2"),
        (else_try),
		    (eq,":d6",3),
		    (assign,reg0,"mesh_mmc_dice_3"),
		(else_try),
		    (eq,":d6",4),
		    (assign,reg0,"mesh_mmc_dice_4"),
    	(else_try),
		    (eq,":d6",5),
		    (assign,reg0,"mesh_mmc_dice_5"),
    	(else_try),
		    (eq,":d6",6),
		    (assign,reg0,"mesh_mmc_dice_6"),
    	(try_end),
	  (assign,reg1,":d6"),
	(try_end),
   ])
]
