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

form_cavalry_scripts = [
("form_cavalry", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),
      (store_script_param, ":formation_extra_spacing", 4),
      (store_script_param, ":include_leader", 5),
      (store_mul, ":extra_space", ":formation_extra_spacing", 50),
      (store_add, ":x_distance", formation_minimum_spacing_horse_width, ":extra_space"),
      (store_add, ":y_distance", formation_minimum_spacing_horse_length, ":extra_space"),
      (assign, ":max_level", 0),
      (try_for_agents, ":agent"),
        (call_script, "script_cf_valid_formation_member", ":fteam", ":fdivision", ":fleader", ":agent"),
        (agent_get_troop_id, ":troop_id", ":agent"),
        (store_character_level, ":troop_level", ":troop_id"),
        (gt, ":troop_level", ":max_level"),
        (assign, ":max_level", ":troop_level"),
      (end_try),
      (assign, ":column", 1),
      (assign, ":rank_dimension", 1),
      (store_mul, ":neg_y_distance", ":y_distance", -1),
      (store_mul, ":neg_x_distance", ":x_distance", -1),
      (store_div, ":wedge_adj", ":x_distance", 2),
      (store_div, ":neg_wedge_adj", ":neg_x_distance", 2),
      (assign, ":form_left", 1),
      (try_begin),
        (eq, ":include_leader", 0),
        (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
        (team_set_slot, ":fteam", ":slot", -1),
      (else_try),	#after leader, move to next position (copied from below)
        (team_set_slot, ":fteam", ":slot", ":fleader"),
        (try_begin),
          (eq, ":form_left", 1),
          (position_move_x, pos1, ":neg_x_distance", 0),
        (else_try),
          (position_move_x, pos1, ":x_distance", 0),
        (try_end),
        (val_add, ":column", 1),
        (gt, ":column", ":rank_dimension"),
        (position_move_y, pos1, ":neg_y_distance", 0),
        (try_begin),
          (neq, ":form_left", 1),
          (assign, ":form_left", 1),
          (position_move_x, pos1, ":neg_wedge_adj", 0),
        (else_try),
          (assign, ":form_left", 0),
          (position_move_x, pos1, ":wedge_adj", 0),
        (try_end),
        (assign, ":column", 1),
        (val_add, ":rank_dimension", 1),
      (try_end),

      (val_add, ":max_level", 1),
      (try_for_range_backwards, ":rank_level", 0, ":max_level"),	#put troops with highest exp in front
        (try_for_agents, ":agent"),
          (agent_get_troop_id, ":troop_id", ":agent"),
          (store_character_level, ":troop_level", ":troop_id"),
          (eq, ":troop_level", ":rank_level"),
          (call_script, "script_cf_valid_formation_member", ":fteam", ":fdivision", ":fleader", ":agent"),
          (agent_set_scripted_destination, ":agent", pos1, 1),
          (try_begin),	#First Agent
            (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
            (neg | team_slot_ge, ":fteam", ":slot", 0),
            (team_set_slot, ":fteam", ":slot", ":agent"),
          (try_end),
          (try_begin),
            (eq, ":form_left", 1),
            (position_move_x, pos1, ":neg_x_distance", 0),
          (else_try),
            (position_move_x, pos1, ":x_distance", 0),
          (try_end),
          (val_add, ":column", 1),
          (gt, ":column", ":rank_dimension"),
          (position_move_y, pos1, ":neg_y_distance", 0),
          (try_begin),
            (neq, ":form_left", 1),
            (assign, ":form_left", 1),
            (position_move_x, pos1, ":neg_wedge_adj", 0),
          (else_try),
            (assign, ":form_left", 0),
            (position_move_x, pos1, ":wedge_adj", 0),
          (try_end),
          (assign, ":column", 1),
          (val_add, ":rank_dimension", 1),
        (end_try),
      (end_try),])
]
