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

get_formation_destination_scripts = [
("get_formation_destination", [
      (store_script_param, ":fposition", 1),
      (store_script_param, ":fteam", 2),
      (store_script_param, ":fdivision", 3),
      (init_position, ":fposition"),
      # (try_begin),
      #(is_between, ":fteam", 0, 4), #Caba - this will always pass MOTO except in
      #mods with more than four teams (eg SWC arena) but now obsolete by other
      #limits
      (store_add, ":slot", slot_team_d0_destination_x, ":fdivision"),
      (team_get_slot, ":x", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_destination_y, ":fdivision"),
      (team_get_slot, ":y", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_destination_zrot, ":fdivision"),
      (team_get_slot, ":zrot", ":fteam", ":slot"),

      (position_set_x, ":fposition", ":x"),
      (position_set_y, ":fposition", ":y"),
      (position_rotate_z, ":fposition", ":zrot"),
      # (else_try),
      # (store_add, ":slot", slot_team_d0_first_member, ":fdivision"), #only
      # defined for divisions in formation
      # (team_get_slot, reg0, ":fteam", ":slot"),
      # (try_begin), # "launder" team_get_order_position shutting down
      # position_move_x
      # (gt, reg0, -1),
      # (team_get_order_position, ":fposition", ":fteam", ":fdivision"),
      # (agent_get_position, pos0, reg0),
      # (agent_set_position, reg0, ":fposition"),
      # (agent_get_position, ":fposition", reg0),
      # (agent_set_position, reg0, pos0),
      # (try_end),
      # (try_end),
      (position_set_z_to_ground_level, ":fposition"),])
]
