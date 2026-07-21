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

select_battle_tactic_scripts = [
# script_cf_check_enemies_nearby
# Input: none
# Output: none
("select_battle_tactic",
    [
      (assign, "$ai_team_1_battle_tactic", 0),
      (get_player_agent_no, ":player_agent"),
      (agent_get_team, ":player_team", ":player_agent"),
      (try_begin),
        (num_active_teams_le, 2),
        (try_begin),
          (eq, ":player_team", 0),
          (assign, "$ai_team_1", 1),
        (else_try),
          (assign, "$ai_team_1", 0),
        (try_end),
        (assign, "$ai_team_2", -1),
      (else_try),
        (try_begin),
          (eq, ":player_team", 0),
          (assign, "$ai_team_1", 1),
        (else_try),
          (assign, "$ai_team_1", 0),
        (try_end),
        (store_add, "$ai_team_2", ":player_team", 2),
      (try_end),
      (call_script, "script_select_battle_tactic_aux", "$ai_team_1", 0),
      (assign, "$ai_team_1_battle_tactic", reg0),
      (try_begin),
        (ge, "$ai_team_2", 0),
        (assign, ":defense_not_an_option", 0),
        (try_begin),
          (eq, "$ai_team_1_battle_tactic", btactic_hold),
          (assign, ":defense_not_an_option", 1), #don't let two AI defend at the same time
        (try_end),
        (call_script, "script_select_battle_tactic_aux", "$ai_team_2", ":defense_not_an_option"),
        (assign, "$ai_team_2_battle_tactic", reg0),
      (try_end),
  ])
]
