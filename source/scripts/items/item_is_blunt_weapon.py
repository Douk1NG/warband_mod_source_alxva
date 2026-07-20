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

item_is_blunt_weapon_scripts = [
("item_is_blunt_weapon", 
    [
      (store_script_param, ":item", 1),
      (assign, ":blunt_weapon", 0),
      (try_begin),
        (gt, ":item", -1),
        (item_get_type, ":type", ":item"),
        (try_begin),
          (this_or_next|is_between, ":type", itp_type_one_handed_wpn, itp_type_arrows),
          (this_or_next|is_between, ":type", itp_type_bow, itp_type_goods),
          (is_between, ":type", itp_type_pistol, itp_type_bullets),
          (item_get_swing_damage, ":swing_damage", ":item"),
          (try_begin),
            (gt, ":swing_damage", 0),
            (item_get_swing_damage_type, ":swing_damage_type", ":item"),
            (try_begin),
              (eq, ":swing_damage_type", blunt),
              (val_add, ":blunt_weapon", 1),
            (else_try),
              (val_sub, ":blunt_weapon", 1),
            (try_end),
          (try_end),
          (item_get_thrust_damage, ":thrust_damage", ":item"),
          (try_begin),
            (gt, ":thrust_damage", 0),
            (item_get_thrust_damage_type, ":thrust_damage_type", ":item"),
            (try_begin),
              (eq, ":thrust_damage_type", blunt),
              (val_add, ":blunt_weapon", 1),
            (else_try),
              (val_sub, ":blunt_weapon", 1),
            (try_end),
          (try_end),
          (val_clamp, ":blunt_weapon", 0, 2),
        (try_end),
      (try_end),
      (assign, reg0, ":blunt_weapon"),
    ])
]
