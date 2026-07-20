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

multiplayer_change_leader_of_bot_scripts = [
# script_multiplayer_change_leader_of_bot
# Input: arg1 = agent_no
# Output: none
("multiplayer_change_leader_of_bot",
    [
      (store_script_param, ":agent_no", 1),
      (agent_get_team, ":team_no", ":agent_no"),
      (call_script, "script_multiplayer_find_player_leader_for_bot", ":team_no", 1),
      (assign, ":leader_player", reg0),
      (agent_set_group, ":agent_no", ":leader_player"),
      ])
]
