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

create_wpn_slot_overlay_scripts = [
("create_wpn_slot_overlay", [
      (store_script_param, ":slot", 1),
      (store_script_param, ":pos", 2),
      (init_position, pos1),
      (position_set_x, pos1, 270),
      (position_set_y, pos1, ":pos"),
      (create_combo_button_overlay, ":obj"),
      (overlay_set_position, ":obj", pos1),
      (assign, ":sub_overlay_id", 0),
      (store_add, ":upgrade_slot", ":slot", dplmc_slot_upgrade_wpn_0),

      # #SB : add meta-types
      # (overlay_add_item, ":obj", "str_dplmc_hero_wpn_slot_pikes"),
      # (overlay_add_item, ":obj", "str_dplmc_hero_wpn_slot_lance"),
      # (overlay_add_item, ":obj", "str_dplmc_hero_wpn_slot_morningstar"),
      # (try_for_range_backwards, ":item_type", dplmc_itp_morningstar, dplmc_itp_pike + 1),
        # (troop_slot_eq, "$temp", ":upgrade_slot", ":item_type"),
        # (overlay_set_val, ":obj", ":sub_overlay_id"),
      # (else_try),
        # (val_add, ":sub_overlay_id", 1),
      # (try_end),
      (call_script, "script_dplmc_get_current_item_for_autoloot", ":slot"), #goes to "keep current", s10
      (try_for_range_backwards, ":item_type", 0, itp_type_animal),
        (this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_goods),
        (this_or_next|is_between, ":item_type", itp_type_pistol, itp_type_animal),
        (eq, ":item_type", 0),
        (store_add, ":out_string", "str_dplmc_hero_wpn_slot_none", ":item_type"),
        (overlay_add_item, ":obj", ":out_string"),
        (try_begin), #find base type
          (troop_get_slot, ":cur_value", "$temp", ":upgrade_slot"),
          (val_mod, ":cur_value", meta_itp_mask),
          (eq, ":cur_value", ":item_type"),
          (overlay_set_val, ":obj", ":sub_overlay_id"),
        (try_end),
        (val_add, ":sub_overlay_id", 1),
      (try_end),

      #store id in slot
      (troop_set_slot, "trp_stack_selection_ids", ":slot", ":obj"),
      # # only works for original button, not drop-down lists
      # (overlay_set_additional_render_height, ":obj", 99),

      (assign, reg1, ":obj"), #return overlay id
  ])
]
