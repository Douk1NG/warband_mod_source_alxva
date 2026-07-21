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

game_multiplayer_get_game_type_mission_template_scripts = [
# script_game_multiplayer_get_game_type_mission_template
# Input: arg1 = game_type
# Output: mission_template
("game_multiplayer_get_game_type_mission_template",
   [
     (assign, ":selected_mt", -1),
     (store_script_param, ":game_type", 1),
     (try_begin),
       (eq, ":game_type", multiplayer_game_type_deathmatch),
       (assign, ":selected_mt", "mt_multiplayer_dm"),
     (else_try),
       (eq, ":game_type", multiplayer_game_type_team_deathmatch),
       (assign, ":selected_mt", "mt_multiplayer_tdm"),
     (else_try),
       (eq, ":game_type", multiplayer_game_type_battle),
       (assign, ":selected_mt", "mt_multiplayer_bt"),
     (else_try),
       (eq, ":game_type", multiplayer_game_type_destroy),
       (assign, ":selected_mt", "mt_multiplayer_fd"),
     (else_try),
       (eq, ":game_type", multiplayer_game_type_capture_the_flag),
       (assign, ":selected_mt", "mt_multiplayer_cf"),
     (else_try),
       (eq, ":game_type", multiplayer_game_type_headquarters),
       (assign, ":selected_mt", "mt_multiplayer_hq"),
     (else_try),
       (eq, ":game_type", multiplayer_game_type_siege),
       (assign, ":selected_mt", "mt_multiplayer_sg"),
     (else_try),
       (eq, ":game_type", multiplayer_game_type_duel),
       (assign, ":selected_mt", "mt_multiplayer_duel"),
     (try_end),
     (assign, reg0, ":selected_mt"),
     ])
]
