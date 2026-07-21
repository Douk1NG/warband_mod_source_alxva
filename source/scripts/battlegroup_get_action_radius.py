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

battlegroup_get_action_radius_scripts = [
("battlegroup_get_action_radius", [
      (store_script_param, ":bgteam", 1),
      (store_script_param, ":bgdivision", 2),

      (store_add, ":slot", slot_team_d0_size, ":bgdivision"),
      (team_get_slot, ":size_battlegroup", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
      (team_get_slot, ":formation", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_type, ":bgdivision"),
      (team_get_slot, ":div_type", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation_space, ":bgdivision"),
      (team_get_slot, ":spacing", ":bgteam", ":slot"),

      (try_begin),
        (this_or_next | eq, ":div_type", sdt_archer),
        (le, ":formation", formation_none),	#Native formation

        (store_mul, ":troop_space", ":spacing", 75),	#Native minimum spacing not consistent but about this
        (val_add, ":troop_space", 100),	#minimum spacing

        #WFaS multi-ranks
        (try_begin),
          (eq, ":formation", formation_2_row),
          (val_div, ":size_battlegroup", 2),
        (else_try),
          (eq, ":formation", formation_3_row),
          (val_div, ":size_battlegroup", 3),
        (else_try),
          (eq, ":formation", formation_4_row),
          (val_div, ":size_battlegroup", 4),
        (else_try),
          (eq, ":formation", formation_5_row),
          (val_div, ":size_battlegroup", 5),

        (else_try),	#WB multi-ranks
          (lt, ":spacing", 0),
          (assign, ":troop_space", 150),
          (val_mul, ":spacing", -1),
          (val_add, ":spacing", 1),
          (val_div, ":size_battlegroup", ":spacing"),
        (try_end),

        (store_mul, ":formation_width", ":size_battlegroup", ":troop_space"),
        (store_div, reg0, ":formation_width", 2),

      (else_try),
        (eq, ":formation", formation_wedge),
        (call_script, "script_get_centering_amount", formation_square, ":size_battlegroup", ":spacing"),	#approximation
        (val_mul, reg0, 7),
        (val_div, reg0, 6),
      (else_try),
        (try_begin),
          (lt, ":spacing", 0),
          (assign, reg0, ":bgteam"),
          (assign, reg1, ":bgdivision"),
          (assign, reg2, ":formation"),
          (display_message, "@{!}battlegroup_get_action_radius: negative radius for team {reg0} division {reg1} formation {reg2}"),
        (try_end),
        (call_script, "script_get_centering_amount", ":formation", ":size_battlegroup", ":spacing"),
      (try_end),

      (val_mul, reg0, 2),])
]
