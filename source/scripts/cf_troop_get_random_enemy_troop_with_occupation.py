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

cf_troop_get_random_enemy_troop_with_occupation_scripts = [
("cf_troop_get_random_enemy_troop_with_occupation",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":occupation"),

      (assign, ":result", -1),
      (assign, ":count_enemies", 0),
      (try_for_range, ":enemy_troop_no", active_npcs_begin, active_npcs_end),
        (troop_slot_eq, ":enemy_troop_no", slot_troop_occupation, ":occupation"),
        (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":enemy_troop_no"),
        (lt, reg0, -10),
        (val_add, ":count_enemies", 1),
      (try_end),

      (gt, ":count_enemies", 0),
      (store_random_in_range,":random_enemy",0,":count_enemies"),

      (assign, ":count_enemies", 0),
      (try_for_range, ":enemy_troop_no", active_npcs_begin, active_npcs_end),
        (troop_slot_eq, ":enemy_troop_no", slot_troop_occupation, ":occupation"),
        (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":enemy_troop_no"),
        (lt, reg0, -10),
        (val_add, ":count_enemies", 1),
        (eq, ":random_enemy", ":count_enemies"),
        (assign, ":result", ":enemy_troop_no"),
      (try_end),

      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ])
]
