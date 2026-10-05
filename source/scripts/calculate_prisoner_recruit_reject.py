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

calculate_prisoner_recruit_reject_scripts = [
    ("calculate_prisoner_recruit_reject",
        [
            (store_script_param_1, ":troop_id"),
            # Tier base by level: T1 30 / T2 40 / T3 50 / T4 70 / T5 80 / T6 90 (elite harder)
            (store_character_level, ":level", ":troop_id"),
            (try_begin),
                (le, ":level", 6),
                (assign, ":base", 30),
            (else_try),
                (le, ":level", 11),
                (assign, ":base", 40),
            (else_try),
                (le, ":level", 16),
                (assign, ":base", 50),
            (else_try),
                (le, ":level", 22),
                (assign, ":base", 70),
            (else_try),
                (le, ":level", 27),
                (assign, ":base", 80),
            (else_try),
                (assign, ":base", 90),
            (try_end),
            (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
            (val_mul, ":persuasion", 4),
            (val_sub, ":base", ":persuasion"),
            # Renown: every 100 -> 2.5%  => renown*25//1000
            (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
            (store_mul, ":renown_bonus", ":renown", 25),
            (val_div, ":renown_bonus", 1000),
            (val_sub, ":base", ":renown_bonus"),
            # Honor: every 10 -> 2%  => floor(max(honor,0)/10)*2
            (assign, ":honor_bonus", 0),
            (try_begin),
                (gt, "$player_honor", 0),
                (store_div, ":honor_bonus", "$player_honor", 10),
                (val_mul, ":honor_bonus", 2),
                (val_sub, ":base", ":honor_bonus"),
            (try_end),
            # clamp 5..75
            (try_begin),
                (lt, ":base", 5),
                (assign, ":base", 5),
            (else_try),
                (gt, ":base", 75),
                (assign, ":base", 75),
            (try_end),
            (assign, reg0, ":base"),
        ]),
]
