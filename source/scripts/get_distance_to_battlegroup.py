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

get_distance_to_battlegroup_scripts = [
("get_distance_to_battlegroup", [
      (store_script_param, ":bgteam", 1),
      (store_script_param, ":bgdivision", 2),
      (store_script_param, ":from_pos", 3),

      (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
      (team_get_slot, ":bgformation", ":bgteam", ":slot"),
      (call_script, "script_battlegroup_get_action_radius", ":bgteam", ":bgdivision"),
      (store_div, ":radius", reg0, 2),	#function returns length of bg
      (assign, ":min_cos_theta", 1),
      (convert_to_fixed_point, ":min_cos_theta"),
      (try_begin),
        (eq, ":bgformation", formation_wedge),
        (val_mul, ":min_cos_theta", 58),	#relation inscribed circle radius to half side: 1 / sqrt 3
        (val_div, ":min_cos_theta", 100),
      (else_try),
        (gt, ":radius", 0),
        (call_script, "script_battlegroup_dist_center_to_front", ":bgteam", ":bgdivision"),
        (val_mul, ":min_cos_theta", reg0),
        (val_div, ":min_cos_theta", ":radius"),
      (else_try),
        (assign, ":min_cos_theta", 0),
      (try_end),

      #acquire rotations
      (call_script, "script_battlegroup_get_position", pos0, ":bgteam", ":bgdivision"),
      (try_begin),
        (gt, ":bgformation", formation_none),
        (neq, ":bgformation", formation_default),
        (call_script, "script_get_formation_destination", pos61, ":bgteam", ":bgdivision"),
        (position_copy_rotation, pos0, pos61),
      (try_end),

      (copy_position, pos61, ":from_pos"),
      (call_script, "script_point_y_toward_position", pos61, pos0),
      (assign, ":distance_to_battlegroup", reg0),

      #calculate difference from center of bg
      (get_angle_between_positions, ":theta", pos61, pos0),
      (val_sub, ":theta", 9000),
      (store_cos, ":cos_theta", ":theta"),
      (val_abs, ":cos_theta"),
      (val_max, ":cos_theta", ":min_cos_theta"),	#doing depth considerations this way allows calling func to use angle; it also
      #avoids Pythagorean calcs

      (store_mul, reg1, ":radius", ":cos_theta"),
      (convert_from_fixed_point, reg1),
      (val_sub, ":distance_to_battlegroup", reg1),
      (assign, reg0, ":distance_to_battlegroup"),
      (assign, reg2, ":cos_theta"),])
]
