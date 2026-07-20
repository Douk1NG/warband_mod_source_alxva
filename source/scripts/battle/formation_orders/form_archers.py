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

form_archers_scripts = [
("form_archers", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),
      (store_script_param, ":formation_extra_spacing", 4),
      (store_script_param, ":include_leader", 5),
      (store_script_param, ":archers_formation", 6),
      (store_mul, ":extra_space", ":formation_extra_spacing", 50),
      (store_add, ":distance", formation_minimum_spacing, ":extra_space"),		#minimum distance between troops
      (assign, ":total_move_y", 0),	#staggering variable
      (try_begin),
        (eq, ":include_leader", 0),
        (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
        (team_set_slot, ":fteam", ":slot", -1),
      (else_try),	#after leader, move to next position (copied from below)
        (team_set_slot, ":fteam", ":slot", ":fleader"),
        (position_move_x, pos1, ":distance", 0),
        (try_begin),
          (eq, ":archers_formation", formation_ranks),
          (val_add, ":total_move_y", 75),
          (try_begin),
            (le, ":total_move_y", 150),
            (position_move_y, pos1, 75, 0),
          (else_try),
            (position_move_y, pos1, -150, 0),
            (assign, ":total_move_y", 0),
          (try_end),
        (try_end),
      (try_end),

      (try_for_agents, ":agent"),
        (call_script, "script_cf_valid_formation_member", ":fteam", ":fdivision", ":fleader", ":agent"),
        (agent_set_scripted_destination, ":agent", pos1, 1),
        (try_begin),	#First Agent
          (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
          (neg | team_slot_ge, ":fteam", ":slot", 0),
          (team_set_slot, ":fteam", ":slot", ":agent"),
        (try_end),
        (position_move_x, pos1, ":distance", 0),
        (try_begin),
          (eq, ":archers_formation", formation_ranks),
          (val_add, ":total_move_y", 75),
          (try_begin),
            (le, ":total_move_y", 150),
            (position_move_y, pos1, 75, 0),
          (else_try),
            (position_move_y, pos1, -150, 0),
            (assign, ":total_move_y", 0),
          (try_end),
        (try_end),
      (try_end),])
]
