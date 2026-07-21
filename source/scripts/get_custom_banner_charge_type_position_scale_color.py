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

get_custom_banner_charge_type_position_scale_color_scripts = [
# script_get_custom_banner_charge_type_position_scale_color
# Input: arg1 = troop_no, arg2 = positioning_index
# Output: reg0 = type_1
#         reg1 = scale_1
#         reg2 = color_1
#         reg3 = type_2
#         reg4 = scale_2
#         reg5 = color_2
#         reg6 = type_3
#         reg7 = scale_3
#         reg8 = color_3
#         reg9 = type_4
#         reg10 = scale_4
#         reg11 = color_4
("get_custom_banner_charge_type_position_scale_color",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":positioning", 2),
      (troop_get_slot, ":num_charges", ":troop_no", slot_troop_custom_banner_num_charges),
      (init_position, pos0),
      (init_position, pos1),
      (init_position, pos2),
      (init_position, pos3),

      (troop_get_slot, reg0, ":troop_no", slot_troop_custom_banner_charge_type_1),
      (val_add, reg0, custom_banner_charges_begin),
      (troop_get_slot, reg2, ":troop_no", slot_troop_custom_banner_charge_color_1),
      (troop_get_slot, reg3, ":troop_no", slot_troop_custom_banner_charge_type_2),
      (val_add, reg3, custom_banner_charges_begin),
      (troop_get_slot, reg5, ":troop_no", slot_troop_custom_banner_charge_color_2),
      (troop_get_slot, reg6, ":troop_no", slot_troop_custom_banner_charge_type_3),
      (val_add, reg6, custom_banner_charges_begin),
      (troop_get_slot, reg8, ":troop_no", slot_troop_custom_banner_charge_color_3),
      (troop_get_slot, reg9, ":troop_no", slot_troop_custom_banner_charge_type_4),
      (val_add, reg9, custom_banner_charges_begin),
      (troop_get_slot, reg11, ":troop_no", slot_troop_custom_banner_charge_color_4),

      (try_begin),
        (eq, ":num_charges", 1),
        (try_begin),
          (eq, ":positioning", 0),
          (assign, reg1, 100),
        (else_try),
          (assign, reg1, 50),
        (try_end),
      (else_try),
        (eq, ":num_charges", 2),
        (try_begin),
          (eq, ":positioning", 0),
          (position_set_y, pos0, 25),
          (position_set_y, pos1, -25),
          (assign, reg1, 40),
          (assign, reg4, 40),
        (else_try),
          (eq, ":positioning", 1),
          (position_set_x, pos0, -25),
          (position_set_x, pos1, 25),
          (assign, reg1, 40),
          (assign, reg4, 40),
        (else_try),
          (eq, ":positioning", 2),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, 25),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, -25),
          (assign, reg1, 50),
          (assign, reg4, 50),
        (else_try),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, -25),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, 25),
          (assign, reg1, 50),
          (assign, reg4, 50),
        (try_end),
      (else_try),
        (eq, ":num_charges", 3),
        (try_begin),
          (eq, ":positioning", 0),
          (position_set_y, pos0, 33),
          (position_set_y, pos2, -33),
          (assign, reg1, 30),
          (assign, reg4, 30),
          (assign, reg7, 30),
        (else_try),
          (eq, ":positioning", 1),
          (position_set_x, pos0, -33),
          (position_set_x, pos2, 33),
          (assign, reg1, 30),
          (assign, reg4, 30),
          (assign, reg7, 30),
        (else_try),
          (eq, ":positioning", 2),
          (position_set_x, pos0, -30),
          (position_set_y, pos0, 30),
          (position_set_x, pos2, 30),
          (position_set_y, pos2, -30),
          (assign, reg1, 35),
          (assign, reg4, 35),
          (assign, reg7, 35),
        (else_try),
          (eq, ":positioning", 3),
          (position_set_x, pos0, -30),
          (position_set_y, pos0, -30),
          (position_set_x, pos2, 30),
          (position_set_y, pos2, 30),
          (assign, reg1, 35),
          (assign, reg4, 35),
          (assign, reg7, 35),
        (else_try),
          (eq, ":positioning", 4),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, -25),
          (position_set_y, pos1, 25),
          (position_set_x, pos2, 25),
          (position_set_y, pos2, -25),
          (assign, reg1, 50),
          (assign, reg4, 50),
          (assign, reg7, 50),
        (else_try),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, 25),
          (position_set_y, pos1, -25),
          (position_set_x, pos2, 25),
          (position_set_y, pos2, 25),
          (assign, reg1, 50),
          (assign, reg4, 50),
          (assign, reg7, 50),
        (try_end),
      (else_try),
        (try_begin),
          (eq, ":positioning", 0),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, 25),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, 25),
          (position_set_x, pos2, -25),
          (position_set_y, pos2, -25),
          (position_set_x, pos3, 25),
          (position_set_y, pos3, -25),
          (assign, reg1, 50),
          (assign, reg4, 50),
          (assign, reg7, 50),
          (assign, reg10, 50),
        (else_try),
          (position_set_y, pos0, 30),
          (position_set_x, pos1, -30),
          (position_set_x, pos2, 30),
          (position_set_y, pos3, -30),
          (assign, reg1, 35),
          (assign, reg4, 35),
          (assign, reg7, 35),
          (assign, reg10, 35),
        (try_end),
      (try_end),
     ])
]
