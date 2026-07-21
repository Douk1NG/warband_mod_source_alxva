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

battlegroup_dist_center_to_front_scripts = [
("battlegroup_dist_center_to_front", [
      (store_script_param, ":bgteam", 1),
      (store_script_param, ":bgdivision", 2),

      (store_add, ":slot", slot_team_d0_formation_space, ":bgdivision"),
      (team_get_slot, ":spacing", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
      (team_get_slot, ":bgformation", ":bgteam", ":slot"),

      (try_begin),
        (eq, ":bgformation", formation_none),	#single row
        (assign, ":depth", 0),

        #WFaS multi-ranks
      (else_try),
        (eq, ":bgformation", formation_2_row),
        (assign, ":depth", 100),
      (else_try),
        (eq, ":bgformation", formation_3_row),
        (assign, ":depth", 200),
      (else_try),
        (eq, ":bgformation", formation_4_row),
        (assign, ":depth", 300),
      (else_try),
        (eq, ":bgformation", formation_5_row),
        (assign, ":depth", 400),

      (else_try),	#WB multi-ranks
        (lt, ":spacing", 0),
        (store_mul, ":depth", ":spacing", -1),
        (val_mul, ":depth", 100),

      #Non Native
      (else_try),
        (store_add, ":slot", slot_team_d0_size, ":bgdivision"),
        (team_get_slot, ":size_enemy_battlegroup", ":bgteam", ":slot"),
        (store_mul, ":row_depth", ":spacing", 50),
        (val_add, ":row_depth", formation_minimum_spacing),

        (this_or_next | eq, ":bgformation", formation_ranks),
        (eq, ":bgformation", formation_shield),
        (call_script, "script_calculate_default_ranks", ":size_enemy_battlegroup"),
        (val_sub, reg1, 1),
        (store_mul, ":depth", ":row_depth", reg1),

      (else_try),
        (convert_to_fixed_point, ":size_enemy_battlegroup"),
        (store_sqrt, ":columns", ":size_enemy_battlegroup"),

        (eq, ":bgformation", formation_square),
        (convert_from_fixed_point, ":columns"),
        (val_add, ":columns", 1),	#see script_form_infantry
        (store_div, ":rows", ":size_enemy_battlegroup", ":columns"),
        (store_mul, ":depth", ":row_depth", ":rows"),
        (convert_from_fixed_point, ":depth"),
        (val_sub, ":depth", ":row_depth"),

      (else_try),
        (eq, ":bgformation", formation_wedge),
        (store_mul, ":depth", ":row_depth", ":columns"),	#approximation
        (convert_from_fixed_point, ":depth"),
      (try_end),

      (try_begin),
        (neq, ":bgformation", formation_wedge),
        (store_div, reg0, ":depth", 2),
      (else_try),
        (store_mul, reg0, ":depth", 2),	#another approximation (height - inner radius)
        (val_div, reg0, 3),
      (try_end),])
]
