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

get_random_tournament_team_amount_and_size_scripts = [
# script_get_random_tournament_team_amount_and_size
# Input: none
# Output: reg0 = number_of_teams, reg1 = team_size
("get_random_tournament_team_amount_and_size",
    [
        (call_script, "script_get_num_tournament_participants"),
        (assign, ":num_participants", reg0),
        (party_get_slot, ":town_max_teams", "$current_town", slot_town_tournament_max_teams),
        (val_add, ":town_max_teams", 1),
        (party_get_slot, ":town_max_team_size", "$current_town", slot_town_tournament_max_team_size),
        (val_add, ":town_max_team_size", 1),
        (assign, ":max_teams", ":num_participants"),
        (val_min, ":max_teams", ":town_max_teams"),
        (assign, ":max_size", ":num_participants"),
        (val_min, ":max_size", ":town_max_team_size"),
        (assign, ":min_size", 1),
        (try_begin),
          (ge, ":num_participants", 32),
          (assign, ":min_size", 2),
          (val_min, ":min_size", ":town_max_team_size"),
        (try_end),
        (assign, ":end_cond", 500),
        (try_for_range, ":unused", 0, ":end_cond"),
          (store_random_in_range, ":random_teams", 2, ":max_teams"),
          (store_random_in_range, ":random_size", ":min_size", ":max_size"),
          (store_mul, ":total_men", ":random_teams", ":random_size"),
          (le, ":total_men", ":num_participants"),
          (store_sub, ":left_men", ":num_participants", ":total_men"),
          (neq, ":left_men", 1),
          (assign, ":end_cond", 0),
        (try_end),
        (try_begin),
          (gt, ":end_cond", 0),
          (assign, ":random_teams", 2),
          (assign, ":random_size", 1),
        (try_end),
        (assign, reg0, ":random_teams"),
        (assign, reg1, ":random_size"),
     ])
]
