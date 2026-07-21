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

get_proficient_melee_training_weapon_scripts = [
("get_proficient_melee_training_weapon",
    [
        (store_script_param, ":troop_no", 1),
        (store_proficiency_level, ":onehands", ":troop_no", wpt_one_handed_weapon),
        (store_proficiency_level, ":twohands", ":troop_no", wpt_two_handed_weapon),
        (store_proficiency_level, ":polearms", ":troop_no", wpt_polearm),

        (assign, ":item_no", -1),
        (try_begin), #practice shield will be added automatically
          (ge, ":onehands", ":twohands"),
          (ge, ":onehands", ":polearms"),
          # (agent_equip_item, ":agent_no", "itm_practice_shield"),
          (assign, ":item_no", "itm_practice_sword"),
        (else_try),
          (ge, ":twohands", ":onehands"),
          (ge, ":twohands", ":polearms"),
          (assign, ":item_no", "itm_heavy_practice_sword"),
        (else_try),
          (ge, ":polearms", ":onehands"),
          (ge, ":polearms", ":twohands"),
          (assign, ":item_no", "itm_practice_staff"),
        (try_end),
        (assign, reg0, ":item_no"),
    ])
]
