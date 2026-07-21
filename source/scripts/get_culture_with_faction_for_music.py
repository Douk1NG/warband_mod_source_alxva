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

get_culture_with_faction_for_music_scripts = [
# script_get_culture_with_faction_for_music
# Input: arg1 = party_no
# Output: reg0 = culture
("get_culture_with_faction_for_music",
    [
      (store_script_param, ":faction_no", 1),
      (try_begin),
        (eq, ":faction_no", "fac_kingdom_1"),
        (assign, ":result", mtf_culture_1),
      (else_try),
        (eq, ":faction_no", "fac_kingdom_2"),
        (assign, ":result", mtf_culture_2),
      (else_try),
        (eq, ":faction_no", "fac_kingdom_3"),
        (assign, ":result", mtf_culture_3),
      (else_try),
        (eq, ":faction_no", "fac_kingdom_4"),
        (assign, ":result", mtf_culture_4),
      (else_try),
        (eq, ":faction_no", "fac_kingdom_5"),
        (assign, ":result", mtf_culture_5),
      (else_try),
        (eq, ":faction_no", "fac_kingdom_6"),
        (assign, ":result", mtf_culture_6),
      (else_try),
        (this_or_next|eq, ":faction_no", "fac_outlaws"),
        (this_or_next|eq, ":faction_no", "fac_peasant_rebels"),
        (this_or_next|eq, ":faction_no", "fac_deserters"),
        (this_or_next|eq, ":faction_no", "fac_mountain_bandits"),
        (eq, ":faction_no", "fac_forest_bandits"),
        (assign, ":result", mtf_culture_6),
      (else_try),
        (assign, ":result", 0), #no culture, including player with no bindings to another kingdom
      (try_end),
      (assign, reg0, ":result"),
     ])
]
