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

field_start_position_scripts = [
("field_start_position", [
      (store_script_param, ":fteam", 1),

      (assign, ":depth_cavalry", 0),
      (assign, ":largest_mounted_division_size", 0),
      (team_get_leader, ":fleader", ":fteam"),

      (try_begin),
        (ge, ":fleader", 0),
        (agent_get_position, pos2, ":fleader"),
      (else_try),
        (call_script, "script_battlegroup_get_position", pos2, ":fteam", grc_everyone),
      (try_end),

      (try_for_range, ":division", 0, 9),
        (store_add, ":slot", slot_team_d0_type, ":division"),
        (team_slot_eq, ":fteam", ":slot", sdt_cavalry),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_get_slot, reg0, ":fteam", ":slot"),
        (lt, ":largest_mounted_division_size", reg0),
        (assign, ":largest_mounted_division_size", reg0),
      (try_end),

      (try_begin),
        (gt, ":largest_mounted_division_size", 0),
        (val_mul, ":largest_mounted_division_size", 2),
        (convert_to_fixed_point, ":largest_mounted_division_size"),
        (store_sqrt, ":depth_cavalry", ":largest_mounted_division_size"),
        (convert_from_fixed_point, ":depth_cavalry"),
        (val_sub, ":depth_cavalry", 1),

        (store_mul, reg0, formation_start_spread_out, 50),
        (val_add, reg0, formation_minimum_spacing_horse_length),
        (val_mul, ":depth_cavalry", reg0),

        (store_mul, ":depth_infantry", formation_start_spread_out, 50),
        (val_add, ":depth_infantry", formation_minimum_spacing),
        (val_mul, ":depth_infantry", 2),
        (val_sub, ":depth_cavalry", ":depth_infantry"),

        (gt, ":depth_cavalry", 0),
        (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, ":fteam", grc_everyone),
        (call_script, "script_point_y_toward_position", pos2, Enemy_Team_Pos),
        (position_move_y, pos2, ":depth_cavalry"),
      (try_end),])
]
