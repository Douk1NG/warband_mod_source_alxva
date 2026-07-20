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

team_give_order_from_order_panel_scripts = [
# script_store_weapon_usage_order_name_to_s1
# Input: arg1 = leader_agent_no, arg2 = class_no
# Output: none
("team_give_order_from_order_panel",
   [(store_script_param_1, ":leader_agent_no"),
    (store_script_param_2, ":order"),
    (agent_get_team, ":team_no", ":leader_agent_no"),
    #(set_show_messages, 0),
    (try_begin),
      (eq, "$g_formation_group0_selected", 1),
      (team_give_order, ":team_no", 0, ":order"),
    (try_end),
    (try_begin),
      (eq, "$g_formation_group1_selected", 1),
      (team_give_order, ":team_no", 1, ":order"),
    (try_end),
    (try_begin),
      (eq, "$g_formation_group2_selected", 1),
      (team_give_order, ":team_no", 2, ":order"),
    (try_end),
    (try_begin),
      (eq, "$g_formation_group3_selected", 1),
      (team_give_order, ":team_no", 3, ":order"),
    (try_end),
    (try_begin),
      (eq, "$g_formation_group4_selected", 1),
      (team_give_order, ":team_no", 4, ":order"),
    (try_end),
    (try_begin),
      (eq, "$g_formation_group5_selected", 1),
      (team_give_order, ":team_no", 5, ":order"),
    (try_end),
    (try_begin),
      (eq, "$g_formation_group6_selected", 1),
      (team_give_order, ":team_no", 6, ":order"),
    (try_end),
    (try_begin),
      (eq, "$g_formation_group7_selected", 1),
      (team_give_order, ":team_no", 7, ":order"),
    (try_end),
    (try_begin),
      (eq, "$g_formation_group8_selected", 1),
      (team_give_order, ":team_no", 8, ":order"),
    (try_end),

    (try_begin),
      (eq, ":order", mordr_hold),
      (agent_get_position, pos1, ":leader_agent_no"),
      (try_begin),
        (eq, "$g_formation_group0_selected", 1),
        (team_set_order_position, ":team_no", 0, pos1),
      (try_end),
      (try_begin),
        (eq, "$g_formation_group1_selected", 1),
        (team_set_order_position, ":team_no", 1, pos1),
      (try_end),
      (try_begin),
        (eq, "$g_formation_group2_selected", 1),
        (team_set_order_position, ":team_no", 2, pos1),
      (try_end),
      (try_begin),
        (eq, "$g_formation_group3_selected", 1),
        (team_set_order_position, ":team_no", 3, pos1),
      (try_end),
      (try_begin),
        (eq, "$g_formation_group4_selected", 1),
        (team_set_order_position, ":team_no", 4, pos1),
      (try_end),
      (try_begin),
        (eq, "$g_formation_group5_selected", 1),
        (team_set_order_position, ":team_no", 5, pos1),
      (try_end),
      (try_begin),
        (eq, "$g_formation_group6_selected", 1),
        (team_set_order_position, ":team_no", 6, pos1),
      (try_end),
      (try_begin),
        (eq, "$g_formation_group7_selected", 1),
        (team_set_order_position, ":team_no", 7, pos1),
      (try_end),
      (try_begin),
        (eq, "$g_formation_group8_selected", 1),
        (team_set_order_position, ":team_no", 8, pos1),
      (try_end),
    (try_end),
    (call_script, "script_player_order_formations", ":order"),
    #(set_show_messages, 1),
  ])
]
