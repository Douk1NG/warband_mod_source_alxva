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

tournament_place_bet_scripts = [
# script_tournament_place_bet
# Input: arg1 = bet_amount
# Output: none
("tournament_place_bet",
    [
        (store_script_param, ":bet_amount", 1),
        (call_script, "script_get_win_amount_for_tournament_bet"),
        (assign, ":win_amount", reg0),
        (val_mul, ":win_amount", ":bet_amount"),
        (val_div, ":win_amount", 100),
        (val_sub, ":win_amount", ":bet_amount"),
        (val_add, "$g_tournament_bet_placed", ":bet_amount"),
        (val_add, "$g_tournament_bet_win_amount", ":win_amount"),
        (troop_remove_gold, "trp_player", ":bet_amount"),
        (assign, "$g_tournament_last_bet_tier", "$g_tournament_cur_tier"),
     ])
]
