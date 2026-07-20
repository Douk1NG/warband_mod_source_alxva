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

calculate_new_death_waiting_time_at_death_mod_scripts = [
("calculate_new_death_waiting_time_at_death_mod",
   [
     (assign, ":num_living_players", 0), #count number of living players to find out death wait time
     (try_begin),
       (try_for_agents, ":agent_no"),
         (agent_is_human, ":agent_no"),
         (agent_is_alive, ":agent_no"),
         (val_add, ":num_living_players", 1),
       (try_end),
     (try_end),

     (val_add, ":num_living_players", multiplayer_battle_formula_value_a),
     (set_fixed_point_multiplier, 100),
     (store_mul, ":num_living_players", ":num_living_players", 100),
     (store_sqrt, ":sqrt_num_living_players", ":num_living_players"),
     (store_div, "$g_battle_waiting_seconds", multiplayer_battle_formula_value_b, ":sqrt_num_living_players"),
     (store_mission_timer_a, "$g_death_mode_part_1_start_time"),
   ])
]
