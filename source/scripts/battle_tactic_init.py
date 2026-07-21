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

battle_tactic_init_scripts = [
# script_battle_calculate_initial_powers
# Input: none
# Output: none
#("battle_calculate_initial_powers",
#  [
#    (try_for_agents, ":agent_no"),
#      (agent_is_human, ":agent_no"),
#
#      (call_script, "script_calculate_team_powers", ":agent_no"),
#      (assign, ":ally_power", reg0),
#      (assign, ":enemy_power", reg1),
#
#      (agent_set_slot, ":agent_no", slot_agent_initial_ally_power, ":ally_power"),
#      (agent_set_slot, ":agent_no", slot_agent_initial_enemy_power, ":enemy_power"),
#    (try_end),
#]),
# script_battle_tactic_init
# Input: none
# Output: none
("battle_tactic_init",
    [
      (call_script, "script_battle_tactic_init_aux", "$ai_team_1", "$ai_team_1_battle_tactic"),
      (try_begin),
        (ge, "$ai_team_2", 0),
        (call_script, "script_battle_tactic_init_aux", "$ai_team_2", "$ai_team_2_battle_tactic"),
      (try_end),

      (try_for_agents, ":cur_agent"),
        (agent_set_slot, ":cur_agent",  slot_agent_is_running_away, 0), #initially nobody is running away.
      (try_end),
  ])
]
