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

multiplayer_get_troop_class_scripts = [
# script_multiplayer_get_troop_class
# Input: arg1 = troop_no
# Output: reg0: troop_class
("multiplayer_get_troop_class",
   [
     (store_script_param_1, ":troop_no"),
     (assign, ":troop_class", multi_troop_class_other),
     (try_begin),
       (this_or_next|eq, ":troop_no", "trp_vaegir_archer_multiplayer"),
       (this_or_next|eq, ":troop_no", "trp_nord_archer_multiplayer"),
       (eq, ":troop_no", "trp_sarranid_archer_multiplayer"),
       (assign, ":troop_class", multi_troop_class_archer),
     (else_try),
       (this_or_next|eq, ":troop_no", "trp_swadian_man_at_arms_multiplayer"),
       (this_or_next|eq, ":troop_no", "trp_nord_scout_multiplayer"),
       (this_or_next|eq, ":troop_no", "trp_rhodok_horseman_multiplayer"),
       (this_or_next|eq, ":troop_no", "trp_sarranid_mamluke_multiplayer"),
       (eq, ":troop_no", "trp_vaegir_horseman_multiplayer"),
       (assign, ":troop_class", multi_troop_class_cavalry),
     (else_try),
       (eq, ":troop_no", "trp_khergit_veteran_horse_archer_multiplayer"),
       (assign, ":troop_class", multi_troop_class_mounted_archer),
#     (else_try),
#       (eq, ":troop_no", "trp_swadian_mounted_crossbowman_multiplayer"),
#       (assign, ":troop_class", multi_troop_class_mounted_crossbowman),
     (else_try),
       (this_or_next|eq, ":troop_no", "trp_swadian_crossbowman_multiplayer"),
       (eq, ":troop_no", "trp_rhodok_veteran_crossbowman_multiplayer"),
       (assign, ":troop_class", multi_troop_class_crossbowman),
     (else_try),
       (this_or_next|eq, ":troop_no", "trp_swadian_infantry_multiplayer"),
       (this_or_next|eq, ":troop_no", "trp_sarranid_footman_multiplayer"),
       (eq, ":troop_no", "trp_nord_veteran_multiplayer"),
       (assign, ":troop_class", multi_troop_class_infantry),
     (else_try),
       (eq, ":troop_no", "trp_vaegir_spearman_multiplayer"),
       (assign, ":troop_class", multi_troop_class_spearman),
     (try_end),
     (assign, reg0, ":troop_class"),
     ])
]
