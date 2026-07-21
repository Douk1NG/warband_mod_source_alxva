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

item_get_type_aux_scripts = [
("item_get_type_aux", [
    (store_script_param, ":item", 1),

    (item_get_type, ":itp", ":item"),
    (try_begin),
      # (item_slot_eq, ":item", dplmc_slot_two_handed_one_handed, 1),
      # (item_has_property, ":item", itp_type_two_handed_wpn),
      (eq, ":itp", itp_type_two_handed_wpn),
      (neg|item_has_property, ":item", itp_two_handed),
      (assign, ":itp", dplmc_itp_morningstar), # type 11 = two-handed/one-handed
    (else_try),
      (eq, ":itp", itp_type_polearm),
      (item_get_swing_damage, ":swing", ":item"),
      (item_get_thrust_damage, ":thrust", ":item"),
      (try_begin),
        (ge, ":swing", ":thrust"),
        (item_get_swing_damage_type, ":damage_type", ":item"),
        (eq, ":damage_type", cut),
        (assign, ":itp", dplmc_itp_halberd),
      (else_try),
        (lt, ":swing", ":thrust"),
        (try_begin), #lances
          (item_has_property, ":item", itp_couchable),
          (assign, ":itp", dplmc_itp_lance),
        (else_try), #can't be both lance and pike
          # (item_has_property, ":item", itp_cant_use_on_horseback), #too restrictive
          (item_get_weapon_length, ":length", ":item"),
          (ge, ":length", dplmc_pike_length_cutoff), #arbitrary value to allow awlpikes to fall in range
          (item_has_capability, ":item", itcf_thrust_polearm), #has two-handed thrust
          (this_or_next|item_has_property, ":item", itp_two_handed),
          (item_has_property, ":item", itp_penalty_with_shield),
          (assign, ":itp", dplmc_itp_pike),
        (try_end),
      (try_end),
    (try_end),
    (assign, reg0, ":itp"),
  ])
]
