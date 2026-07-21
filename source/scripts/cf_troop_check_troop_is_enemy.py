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

cf_troop_check_troop_is_enemy_scripts = [
("cf_troop_check_troop_is_enemy",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":checked_troop_no"),
	  (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":checked_troop_no"),
	  (lt, reg0, -10),
 ])
]
