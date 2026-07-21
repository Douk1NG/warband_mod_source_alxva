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

find_center_to_attack_alt_scripts = [
("find_center_to_attack_alt",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":attack_by_faction", 2),
      (store_script_param, ":all_vassals_included", 3),

      (assign, ":result", -1),
      (assign, ":score_to_beat", 0),

      (try_for_range, ":center_no", centers_begin, centers_end),
        (call_script, "script_npc_decision_checklist_evaluate_enemy_center_for_attack",	":troop_no", ":center_no", ":attack_by_faction", ":all_vassals_included"),
        (assign, ":score", reg0),

        (gt, ":score", ":score_to_beat"),

        (assign, ":result", ":center_no"),
        (assign, ":score_to_beat", ":score"),
      (try_end),

      (assign, reg0, ":result"),
      (assign, reg1, ":score_to_beat"),
	])
]
