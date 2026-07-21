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

get_headquarters_scores_scripts = [
("get_headquarters_scores",
   [
     (assign, ":team_1_num_flags", 0),
     (assign, ":team_2_num_flags", 0),
     (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
       (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
       (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),
       (neq, ":cur_flag_owner", 0),
       (try_begin),
         (eq, ":cur_flag_owner", 1),
         (val_add, ":team_1_num_flags", 1),
       (else_try),
         (val_add, ":team_2_num_flags", 1),
       (try_end),
     (try_end),
     (assign, reg0, ":team_1_num_flags"),
     (assign, reg1, ":team_2_num_flags"),
     ])
]
