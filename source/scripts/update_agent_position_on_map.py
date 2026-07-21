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

update_agent_position_on_map_scripts = [
("update_agent_position_on_map",
   [(store_script_param_1, ":agent_no"),
    (agent_get_slot, ":agent_overlay", ":agent_no", slot_agent_map_overlay_id),

    (get_player_agent_no, ":player_agent"),
    (try_begin),
      (le, ":agent_overlay", 0),
      (set_fixed_point_multiplier, 1000),
      (try_begin),
        (eq, ":agent_no", ":player_agent"),
        (create_mesh_overlay, reg1, "mesh_player_dot"),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 500),
        (overlay_set_size, reg1, pos1),
      (else_try),
        (create_mesh_overlay, reg1, "mesh_white_dot"),
        (position_set_x, pos1, 200),
        (position_set_y, pos1, 200),
        (overlay_set_size, reg1, pos1),
      (try_end),
      (overlay_set_alpha, reg1, 0x88),
      (agent_set_slot, ":agent_no", slot_agent_map_overlay_id, reg1),
      (assign, ":agent_overlay", reg1),
    (try_end),

    (try_begin),
      (neq, ":agent_no", ":player_agent"),
      (agent_get_party_id, ":agent_party", ":agent_no"),
      (try_begin),
        (eq, ":agent_party", "p_main_party"),
        (agent_get_division, ":agent_division", ":agent_no"),
        (try_begin),
          (eq, ":agent_division", 0),
          (overlay_set_color, ":agent_overlay", 0x8d5220),
        (else_try),
          (eq, ":agent_division", 1),
          (overlay_set_color, ":agent_overlay", 0x34c6e4),
        (else_try),
          (eq, ":agent_division", 2),
          (overlay_set_color, ":agent_overlay", 0x569619),
        (else_try),
          (eq, ":agent_division", 3),
          (overlay_set_color, ":agent_overlay", 0xFFE500),
        (else_try),
          (eq, ":agent_division", 4),
          (overlay_set_color, ":agent_overlay", 0x990099),
        (else_try),
          (eq, ":agent_division", 5),
          (overlay_set_color, ":agent_overlay", 0x99FE80),
        (else_try),
          (eq, ":agent_division", 6),
          (overlay_set_color, ":agent_overlay", 0x9DEFFE),
        (else_try),
          (eq, ":agent_division", 7),
          (overlay_set_color, ":agent_overlay", 0xFECB9D),
        (else_try),
          (eq, ":agent_division", 8),
          (overlay_set_color, ":agent_overlay", 0xB19C9C),
        (try_end),
      (else_try),
        (agent_is_ally, ":agent_no"),
        (overlay_set_color, ":agent_overlay", 0x5555FF),
      (else_try),
        (overlay_set_color, ":agent_overlay", 0xFF0000),
      (try_end),
    (try_end),

    (try_begin),
      (eq, ":agent_no", ":player_agent"),
      (agent_get_look_position, pos1, ":agent_no"),
      (position_get_rotation_around_z, ":rot", pos1),
      (init_position, pos10),
      (position_rotate_z, pos10, ":rot"),
      (overlay_set_mesh_rotation, ":agent_overlay", pos10),
      (call_script, "script_convert_3d_pos_to_map_pos"),
    (else_try),
      (agent_get_position, pos1, ":agent_no"),
      (call_script, "script_convert_3d_pos_to_map_pos"),
    (try_end),
    (overlay_set_position, ":agent_overlay", pos0),
  ])
]
