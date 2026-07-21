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

get_random_custom_banner_scripts = [
# script_get_random_custom_banner
# Input: arg1 = troop_no
# Output: none
("get_random_custom_banner",
    [
      (store_script_param, ":troop_no", 1),
      (store_random_in_range, ":num_charges", 1, 5),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_num_charges, ":num_charges"),
      (store_random_in_range, ":random_color_index", 0, 42),
      (call_script, "script_get_custom_banner_color_from_index", ":random_color_index"),
      (assign, ":color_1", reg0),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_bg_color_1, ":color_1"),
      (assign, ":end_cond", 1),
      (try_for_range, ":unused", 0, ":end_cond"),
        (store_random_in_range, ":random_color_index", 0, 42),
        (call_script, "script_get_custom_banner_color_from_index", ":random_color_index"),
        (assign, ":color_2", reg0),
        (try_begin),
          (call_script, "script_cf_check_color_visibility", ":color_1", ":color_2"),
          (troop_set_slot, ":troop_no", slot_troop_custom_banner_bg_color_2, ":color_2"),
        (else_try),
          (val_add, ":end_cond", 1),
        (try_end),
      (try_end),
      (assign, ":end_cond", 4),
      (assign, ":cur_charge", 0),
      (try_for_range, ":unused", 0, ":end_cond"),
        (store_random_in_range, ":random_color_index", 0, 42),
        (call_script, "script_get_custom_banner_color_from_index", ":random_color_index"),
        (assign, ":charge_color", reg0),
        (try_begin),
          (call_script, "script_cf_check_color_visibility", ":charge_color", ":color_1"),
          (call_script, "script_cf_check_color_visibility", ":charge_color", ":color_2"),
          (store_add, ":cur_slot", ":cur_charge", slot_troop_custom_banner_charge_color_1),
          (troop_set_slot, ":troop_no", ":cur_slot", ":charge_color"),
          (store_random_in_range, ":random_charge", custom_banner_charges_begin, custom_banner_charges_end),
          (val_sub, ":random_charge", custom_banner_charges_begin),
          (store_add, ":cur_slot", ":cur_charge", slot_troop_custom_banner_charge_type_1),
          (troop_set_slot, ":troop_no", ":cur_slot", ":random_charge"),
          (val_add, ":cur_charge", 1),
        (else_try),
          (val_add, ":end_cond", 1),
        (try_end),
      (try_end),
      (store_random_in_range, ":random_bg", custom_banner_backgrounds_begin, custom_banner_backgrounds_end),
      (val_sub, ":random_bg", custom_banner_backgrounds_begin),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_bg_type, ":random_bg"),
      (store_random_in_range, ":random_flag", custom_banner_flag_types_begin, custom_banner_flag_types_end),
      (val_sub, ":random_flag", custom_banner_flag_types_begin),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_flag_type, ":random_flag"),
      (store_random_in_range, ":random_positioning", 0, 4),
      (troop_set_slot, ":troop_no", slot_troop_custom_banner_positioning, ":random_positioning"),
     ])
]
