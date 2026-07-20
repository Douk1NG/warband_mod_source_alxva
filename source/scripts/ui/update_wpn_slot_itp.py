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

update_wpn_slot_itp_scripts = [
("update_wpn_slot_itp", [
      (store_script_param, ":slot", 1),
      (store_script_param, ":value", 2),
      (troop_get_slot, ":item_type", "trp_temp_array_c", ":value"),
      (troop_get_slot, ":slot_value", "$temp", ":slot"),
      (try_begin), #if new value supports metamods, inherit
        (call_script, "script_cf_item_type_has_advanced_autoloot", ":item_type"),
        (store_mod, ":original_value", ":slot_value", meta_itp_mask),
        (val_sub, ":slot_value", ":original_value"), #remove original itp
        (val_add, ":slot_value", ":item_type"), #add new
      (else_try), #otherwise replace value
        (assign, ":slot_value", ":item_type"),
      (try_end),
      (troop_set_slot, "$temp", ":slot", ":slot_value"),
      (assign, "$temp_2", ":slot"),
      #restart presentation instead of updating overlay value (because we can't)
      (start_presentation, "prsnt_dplmc_autoloot_upgrade_management"),
  ])
]
