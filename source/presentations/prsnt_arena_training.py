# -*- coding: cp1254 -*-
import string
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
#SB: import skills from ID_skills import *
from module_constants import *
##diplomacy start+ Import for use with terrain advantage
from header_terrain_types import *
from module_items import *
#SB : import colors
from module_factions import *
from header_items import *
##diplomacy end
from compiler import *

arena_training = ("arena_training", prsntf_read_only|prsntf_manual_end_only, 0, [
      (ti_on_presentation_load,
       [(presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
        (get_player_agent_no, ":player_agent"),
        (agent_get_kill_count, reg1, ":player_agent", 1),
        (str_store_string, s1, "@Number of men knocked down: {reg1}"),
        (create_text_overlay, "$g_presentation_obj_arena_training_1", s1),
        (overlay_set_color, "$g_presentation_obj_arena_training_1", 0xFFFFFF),
        (position_set_x, pos1, 10),
        (position_set_y, pos1, 700),
        (overlay_set_position, "$g_presentation_obj_arena_training_1", pos1),
        (assign, reg1, 0),
        (str_store_string, s1, "@Number of men left: {reg1}"),
        (create_text_overlay, "$g_presentation_obj_arena_training_2", s1),
        (overlay_set_color, "$g_presentation_obj_arena_training_2", 0xFFFFFF),
        (position_set_x, pos1, 10),
        (position_set_y, pos1, 670),
        (overlay_set_position, "$g_presentation_obj_arena_training_2", pos1),
        ]),
      (ti_on_presentation_run,
       [(get_player_agent_no, ":player_agent"),
        (agent_get_kill_count, reg1, ":player_agent", 1),
        (str_store_string, s1, "@Opponents Beaten: {reg1}"),
        (overlay_set_text, "$g_presentation_obj_arena_training_1", s1),
        (assign, ":num_left", "$g_arena_training_max_opponents"),
        (try_for_agents, ":agent_no"),
          (agent_is_human, ":agent_no"),
          (neg|agent_is_alive, ":agent_no"),
          (neq, ":agent_no", ":player_agent"),
          (val_sub, ":num_left", 1),
        (try_end),
        (assign, reg1, ":num_left"),
        (str_store_string, s1, "@Opponents Remaining: {reg1}"),
        (overlay_set_text, "$g_presentation_obj_arena_training_2", s1),
        ]),
      ])
