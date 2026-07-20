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

multiplayer_get_mission_template_game_type_scripts = [
# script_multiplayer_get_mission_template_game_type
# Input: arg1 = mission_template_no
# Output: game_type
("multiplayer_get_mission_template_game_type",
   [
     (store_script_param, ":mission_template_no", 1),
     (assign, ":game_type", -1),
     (try_begin),
       (eq, ":mission_template_no", "mt_multiplayer_dm"),
       (assign, ":game_type", multiplayer_game_type_deathmatch),
     (else_try),
       (eq, ":mission_template_no", "mt_multiplayer_tdm"),
       (assign, ":game_type", multiplayer_game_type_team_deathmatch),
     (else_try),
       (eq, ":mission_template_no", "mt_multiplayer_bt"),
       (assign, ":game_type", multiplayer_game_type_battle),
     (else_try),
       (eq, ":mission_template_no", "mt_multiplayer_fd"),
       (assign, ":game_type", multiplayer_game_type_destroy),
     (else_try),
       (eq, ":mission_template_no", "mt_multiplayer_cf"),
       (assign, ":game_type", multiplayer_game_type_capture_the_flag),
     (else_try),
       (eq, ":mission_template_no", "mt_multiplayer_hq"),
       (assign, ":game_type", multiplayer_game_type_headquarters),
     (else_try),
       (eq, ":mission_template_no", "mt_multiplayer_sg"),
       (assign, ":game_type", multiplayer_game_type_siege),
     (else_try),
       (eq, ":mission_template_no", "mt_multiplayer_duel"),
       (assign, ":game_type", multiplayer_game_type_duel),
     (try_end),
     (assign, reg0, ":game_type"),
     ])
]
