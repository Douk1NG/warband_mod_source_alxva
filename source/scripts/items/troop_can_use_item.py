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

troop_can_use_item_scripts = [
("troop_can_use_item",
    [
      (store_script_param, ":troop", 1),
      (store_script_param, ":item", 2),
      (store_script_param, ":imod", 3),

      (call_script, "script_get_item_difficulty_with_imod", ":item", ":imod"),
      (assign, ":difficulty", reg0),
      (item_get_type, ":type", ":item"),
      (try_begin),
        (eq, ":type", itp_type_horse),
        (store_skill_level, ":skill", skl_riding, ":troop"),
      (else_try),
        (this_or_next|eq, ":type", itp_type_head_armor),
        (this_or_next|eq, ":type", itp_type_body_armor),
        (this_or_next|eq, ":type", itp_type_foot_armor),
        (this_or_next|eq, ":type", itp_type_hand_armor),
        (this_or_next|eq, ":type", itp_type_one_handed_wpn),
        (this_or_next|eq, ":type", itp_type_two_handed_wpn),
        (this_or_next|eq, ":type", itp_type_polearm),
        (eq, ":type", itp_type_crossbow),
        (store_attribute_level, ":skill", ":troop", ca_strength),
      (else_try),
        (eq, ":type", itp_type_bow),
        (store_skill_level, ":skill", skl_power_draw, ":troop"),
      (else_try),
        (eq, ":type", itp_type_thrown),
        (store_skill_level, ":skill", skl_power_throw, ":troop"),
      (else_try),
        (eq, ":type", itp_type_shield),
        (store_skill_level, ":skill", skl_shield, ":troop"),
      (try_end),

      (try_begin),
        (lt, ":skill", ":difficulty"),
        (assign, reg0, 0),
      (else_try),
        (assign, reg0, 1),
      (try_end),
    ])
]
