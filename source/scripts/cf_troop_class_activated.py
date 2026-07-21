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

cf_troop_class_activated_scripts = [
("cf_troop_class_activated",
    [
        (store_script_param, ":grc", 1),
        (store_script_param, ":party_no", 2),
        (is_between, ":grc", grc_infantry, grc_everyone),
        (try_begin), #first 3 always available
          (le, ":grc", grc_cavalry),
          (assign, ":end", -1),
        (else_try),
          (party_get_num_companion_stacks, ":end", ":party_no"),

          (try_for_range, ":stack_no", 0, ":end"),
            (party_stack_get_troop_id, ":troop_no", ":party_no", ":stack_no"),
            (neg|troop_is_hero, ":troop_no"),
            (try_begin),
              (troop_get_upgrade_troop, ":upgrade_troop", ":troop_no", 0),
              (gt, ":upgrade_troop", 0),
              (troop_get_class, ":class_no", ":upgrade_troop"),
              (eq, ":class_no", ":grc"),
              (assign, ":end", -1),
            (try_end),
            (try_begin), #not found, check other upgrade
              (neq, ":end", -1),
              (troop_get_upgrade_troop, ":upgrade_troop", ":troop_no", 1),
              (gt, ":upgrade_troop", 0),
              (troop_get_class, ":class_no", ":upgrade_troop"),
              (eq, ":class_no", ":grc"),
              (assign, ":end", -1),
            (try_end),
          (try_end),
        # (try_for_range, ":troop_no", soldiers_begin, soldiers_end),
          # (neg|troop_is_hero, ":troop_no"),
          # (troop_get_class, ":class", ":troop_no"),
        # (try_end),
        (try_end),
        (eq, ":end", -1),

    ])
]
