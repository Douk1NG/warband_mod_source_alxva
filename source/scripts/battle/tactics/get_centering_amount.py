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

get_centering_amount_scripts = [
("get_centering_amount", [
      (store_script_param, ":troop_formation", 1),
      (store_script_param, ":num_troops", 2),
      (store_script_param, ":extra_spacing", 3),
      (store_mul, ":troop_space", ":extra_spacing", 50),
      (val_add, ":troop_space", formation_minimum_spacing),
      (assign, reg0, 0),
      (try_begin),
        (eq, ":troop_formation", formation_square),
        (convert_to_fixed_point, ":num_troops"),
        (store_sqrt, reg0, ":num_troops"),
        (convert_from_fixed_point, reg0),
        (val_mul, reg0, ":troop_space"),
        # (val_sub, reg0, ":troop_space"), MOTO not needed because column added in
        # script_form_infantry
      (else_try),
        (this_or_next | eq, ":troop_formation", formation_ranks),
        (eq, ":troop_formation", formation_shield),
        (call_script, "script_calculate_default_ranks", ":num_troops"),
        (assign, ":num_ranks", reg1),
        (store_div, reg0, ":num_troops", ":num_ranks"),
        (try_begin),
          (store_mod, reg1, ":num_troops", ":num_ranks"),
          (eq, reg1, 0),
          (val_sub, reg0, 1),
        (try_end),
        (val_mul, reg0, ":troop_space"),
      (else_try),
        (eq, ":troop_formation", formation_default),	#assume these are archers in a line
        (store_mul, reg0, ":num_troops", ":troop_space"),
      (try_end),
      (val_div, reg0, 2),])
]
