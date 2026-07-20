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

get_win_amount_for_tournament_bet_scripts = [
# script_get_win_amount_for_tournament_bet
# Input: none
# Output: reg0 = win_amount_with_100_denars
("get_win_amount_for_tournament_bet",
    [
        (party_get_slot, ":player_odds", "$current_town", slot_town_player_odds),
        (try_begin),
          (eq, "$g_tournament_cur_tier", 0),
          (assign, ":win_amount", 120),
        (else_try),
          (eq, "$g_tournament_cur_tier", 1),
          (assign, ":win_amount", 90),
        (else_try),
          (eq, "$g_tournament_cur_tier", 2),
          (assign, ":win_amount", 60),
        (else_try),
          (eq, "$g_tournament_cur_tier", 3),
          (assign, ":win_amount", 40),
        (else_try),
          (eq, "$g_tournament_cur_tier", 4),
          (assign, ":win_amount", 20),
        (else_try),
          (assign, ":win_amount", 8),
        (try_end),
        (val_mul, ":win_amount", ":player_odds"),
        (val_div, ":win_amount", 100),
        (val_add, ":win_amount", 100), #win amount when 100 denars is placed
        (assign, reg0, ":win_amount"),
     ])
]
