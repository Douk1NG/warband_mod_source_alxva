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

set_num_agents_around_flag_scripts = [
("set_num_agents_around_flag",
   [
     (store_script_param, ":flag_no", 1),
     (store_script_param, ":current_owner_code", 2),

     (store_div, ":number_of_agents_around_flag_team_1", ":current_owner_code", 100),
     (store_mod, ":number_of_agents_around_flag_team_2", ":current_owner_code", 100),

     (store_add, ":cur_flag_owner_counts_slot", multi_data_flag_players_around_begin, ":flag_no"),
     (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owner_counts_slot", ":current_owner_code"),

     (call_script, "script_move_headquarters_flags", ":flag_no", ":number_of_agents_around_flag_team_1", ":number_of_agents_around_flag_team_2"),
  ])
]
