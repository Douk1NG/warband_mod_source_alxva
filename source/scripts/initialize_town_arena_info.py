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

initialize_town_arena_info_scripts = [
("initialize_town_arena_info",
    [
      (try_for_range, ":town_no", towns_begin, towns_end),
        (party_set_slot, ":town_no", slot_town_tournament_max_teams, 4),
        (party_set_slot, ":town_no", slot_town_tournament_max_team_size, 8),
      (try_end),
      (party_set_slot, "p_town_6", slot_town_tournament_max_team_size, 2),

      (party_set_slot,"p_town_1", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_1", slot_town_arena_melee_1_team_size,   1),
      (party_set_slot,"p_town_1", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_1", slot_town_arena_melee_2_team_size,   1),
      (party_set_slot,"p_town_1", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_1", slot_town_arena_melee_3_team_size,   1),

      (party_set_slot,"p_town_2", slot_town_arena_melee_1_num_teams,   4),
      (party_set_slot,"p_town_2", slot_town_arena_melee_1_team_size,   4),
      (party_set_slot,"p_town_2", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_2", slot_town_arena_melee_2_team_size,   6),
      (party_set_slot,"p_town_2", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_2", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_3", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_3", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_3", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_3", slot_town_arena_melee_2_team_size,   8),
      (party_set_slot,"p_town_3", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_3", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_4", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_4", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_4", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_4", slot_town_arena_melee_2_team_size,   8),
      (party_set_slot,"p_town_4", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_4", slot_town_arena_melee_3_team_size,   5),

      (party_set_slot,"p_town_5", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_5", slot_town_arena_melee_1_team_size,   3),
      (party_set_slot,"p_town_5", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_5", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_5", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_5", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_6", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_6", slot_town_arena_melee_1_team_size,   4),
      (party_set_slot,"p_town_6", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_6", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_6", slot_town_arena_melee_3_num_teams,   3),
      (party_set_slot,"p_town_6", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_7", slot_town_arena_melee_1_num_teams,   4),
      (party_set_slot,"p_town_7", slot_town_arena_melee_1_team_size,   4),
      (party_set_slot,"p_town_7", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_7", slot_town_arena_melee_2_team_size,   6),
      (party_set_slot,"p_town_7", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_7", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_8", slot_town_arena_melee_1_num_teams,   3),
      (party_set_slot,"p_town_8", slot_town_arena_melee_1_team_size,   1),
      (party_set_slot,"p_town_8", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_8", slot_town_arena_melee_2_team_size,   3),
      (party_set_slot,"p_town_8", slot_town_arena_melee_3_num_teams,   3),
      (party_set_slot,"p_town_8", slot_town_arena_melee_3_team_size,   7),

      (party_set_slot,"p_town_9", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_9", slot_town_arena_melee_1_team_size,   2),
      (party_set_slot,"p_town_9", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_9", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_9", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_9", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_10", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_10", slot_town_arena_melee_1_team_size,   3),
      (party_set_slot,"p_town_10", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_10", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_10", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_10", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_11", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_11", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_11", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_11", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_11", slot_town_arena_melee_3_num_teams,   3),
      (party_set_slot,"p_town_11", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_12", slot_town_arena_melee_1_num_teams,   3),
      (party_set_slot,"p_town_12", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_12", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_12", slot_town_arena_melee_2_team_size,   6),
      (party_set_slot,"p_town_12", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_12", slot_town_arena_melee_3_team_size,   5),

      (party_set_slot,"p_town_13", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_13", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_13", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_13", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_13", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_13", slot_town_arena_melee_3_team_size,   7),

      (party_set_slot,"p_town_14", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_14", slot_town_arena_melee_1_team_size,   4),
      (party_set_slot,"p_town_14", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_14", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_14", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_14", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_15", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_15", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_15", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_15", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_15", slot_town_arena_melee_3_num_teams,   3),
      (party_set_slot,"p_town_15", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_16", slot_town_arena_melee_1_num_teams,   3),
      (party_set_slot,"p_town_16", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_16", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_16", slot_town_arena_melee_2_team_size,   6),
      (party_set_slot,"p_town_16", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_16", slot_town_arena_melee_3_team_size,   5),

      (party_set_slot,"p_town_17", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_17", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_17", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_17", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_17", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_17", slot_town_arena_melee_3_team_size,   7),

      (party_set_slot,"p_town_18", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_18", slot_town_arena_melee_1_team_size,   4),
      (party_set_slot,"p_town_18", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_18", slot_town_arena_melee_2_team_size,   5),
      (party_set_slot,"p_town_18", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_18", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_19", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_19", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_19", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_19", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_19", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_19", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_20", slot_town_arena_melee_1_num_teams,   4),
      (party_set_slot,"p_town_20", slot_town_arena_melee_1_team_size,   2),
      (party_set_slot,"p_town_20", slot_town_arena_melee_2_num_teams,   4),
      (party_set_slot,"p_town_20", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_20", slot_town_arena_melee_3_num_teams,   4),
      (party_set_slot,"p_town_20", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_21", slot_town_arena_melee_1_num_teams,   3),
      (party_set_slot,"p_town_21", slot_town_arena_melee_1_team_size,   3),
      (party_set_slot,"p_town_21", slot_town_arena_melee_2_num_teams,   2),
      (party_set_slot,"p_town_21", slot_town_arena_melee_2_team_size,   6),
      (party_set_slot,"p_town_21", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_21", slot_town_arena_melee_3_team_size,   8),

      (party_set_slot,"p_town_22", slot_town_arena_melee_1_num_teams,   4),
      (party_set_slot,"p_town_22", slot_town_arena_melee_1_team_size,   3),
      (party_set_slot,"p_town_22", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_22", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_22", slot_town_arena_melee_3_num_teams,   2),
      (party_set_slot,"p_town_22", slot_town_arena_melee_3_team_size,   6),

      (party_set_slot,"p_town_23", slot_town_arena_melee_1_num_teams,   2),
      (party_set_slot,"p_town_23", slot_town_arena_melee_1_team_size,   8),
      (party_set_slot,"p_town_23", slot_town_arena_melee_2_num_teams,   3),
      (party_set_slot,"p_town_23", slot_town_arena_melee_2_team_size,   4),
      (party_set_slot,"p_town_23", slot_town_arena_melee_3_num_teams,   3),
      (party_set_slot,"p_town_23", slot_town_arena_melee_3_team_size,   6),
	])
]
