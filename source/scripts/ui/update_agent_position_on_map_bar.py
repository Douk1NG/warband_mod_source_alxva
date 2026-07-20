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

update_agent_position_on_map_bar_scripts = [
("update_agent_position_on_map_bar",
   [(store_script_param_1, ":agent_no"),
    (agent_get_slot, ":agent_overlay", ":agent_no", slot_agent_map_overlay_id),

    (get_player_agent_no, ":player_agent"),
    (try_begin),
      (le, ":agent_overlay", 0),
      (set_fixed_point_multiplier, 1000),
      (try_begin),
        (eq, ":agent_no", ":player_agent"),
        (create_mesh_overlay, reg1, "mesh_player_dot"),
        (position_set_x, pos1, 800),
        (position_set_y, pos1, 800),
        (overlay_set_size, reg1, pos1),
      (else_try),
        (create_mesh_overlay, reg1, "mesh_white_dot"),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, 300),
        (overlay_set_size, reg1, pos1),
      (try_end),
      (agent_set_slot, ":agent_no", slot_agent_map_overlay_id, reg1),
      (assign, ":agent_overlay", reg1),
    (try_end),

    (agent_get_team, ":player_team", ":player_agent"),
    (try_begin),
      (neq, ":agent_no", ":player_agent"),
      (agent_get_team, ":agent_team", ":agent_no"),
      (try_begin),
        (neg|agent_is_ally, ":agent_no"),
        (overlay_set_color, ":agent_overlay", 0xFF4040),
        (assign, ":y_offset", 10),
      (else_try),
        (eq, ":agent_team", ":player_team"),
        (overlay_set_color, ":agent_overlay", 0x80FF80),
        (assign, ":y_offset", -10),
      (else_try),
        (overlay_set_color, ":agent_overlay", 0x8080FF),
        (assign, ":y_offset", 0),
      (try_end),
    (try_end),

    (try_begin),
      (eq, ":agent_no", ":player_agent"),
      (agent_get_look_position, pos1, ":agent_no"),
      (position_get_rotation_around_z, ":rot", pos1),
      (init_position, pos10),
      (position_rotate_z, pos10, ":rot"),
      (overlay_set_mesh_rotation, ":agent_overlay", pos10),
      (position_set_x, pos0, 620),
      (position_set_y, pos0, 721),
    (else_try),
      (agent_get_position, pos1, ":agent_no"),
      (call_script, "script_convert_3d_pos_to_map_bar_pos", ":y_offset"),
    (try_end),
    (overlay_set_position, ":agent_overlay", pos0),
  ])
]
