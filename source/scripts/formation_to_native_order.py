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

formation_to_native_order_scripts = [
("formation_to_native_order", [
      (store_script_param, ":team", 1),
      (store_script_param, ":division", 2),
      (store_script_param, ":formation", 3),

      (try_begin),
        (gt, ":formation", formation_none),	#custom formation (bad call)

      (else_try),
        (eq, Native_Formations_Implementation, WB_Implementation),
        (store_add, ":slot", slot_team_d0_formation_space, ":division"),
        (team_get_slot, ":spacing", ":team", ":slot"),
        (val_sub, ":spacing", ":formation"),	#formation constants indicate number of "Stand Closer"
        (set_show_messages, 0),
        (try_for_range, reg0, 0, ":spacing"),
          (team_give_order, ":team", ":division", mordr_stand_closer),
        (try_end),
        (set_show_messages, 1),
        (team_set_slot, ":team", ":slot", ":spacing"),

      #WFAS implementation
      (else_try),
        (eq, ":formation", formation_1_row),
        (team_give_order, ":team", ":division", mordr_form_1_row),
      (else_try),
        (eq, ":formation", formation_2_row),
        (team_give_order, ":team", ":division", mordr_form_2_row),
      (else_try),
        (eq, ":formation", formation_3_row),
        (team_give_order, ":team", ":division", mordr_form_3_row),
      (else_try),
        (eq, ":formation", formation_4_row),
        (team_give_order, ":team", ":division", mordr_form_4_row),
      (else_try),
        (eq, ":formation", formation_5_row),
        (team_give_order, ":team", ":division", mordr_form_5_row),
      (try_end)])
]
