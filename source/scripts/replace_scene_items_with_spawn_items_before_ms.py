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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

replace_scene_items_with_spawn_items_before_ms_scripts = [
("replace_scene_items_with_spawn_items_before_ms",
    [
      (try_for_range, ":item_no", all_items_begin, all_items_end),
        (item_get_type, ":item_type", ":item_no"),
        (neq, ":item_type", itp_type_goods),
        (neq, ":item_type", itp_type_book),
        (scene_item_get_num_instances, ":num_instances", ":item_no"),
        (item_set_slot, ":item_no", slot_item_num_positions, 0),
        (assign, ":num_positions", 0),
        (try_for_range, ":cur_instance", 0, ":num_instances"),
          (scene_item_get_instance, ":scene_item", ":item_no", ":cur_instance"),
          (prop_instance_get_position, "$g_position_to_use_for_replacing_scene_items", ":scene_item"),
          (store_add, ":cur_slot", slot_item_positions_begin, ":num_positions"),
          (item_set_slot, ":item_no", ":cur_slot", "$g_position_to_use_for_replacing_scene_items"),
          (val_add, ":num_positions", 1),
          (val_add, "$g_position_to_use_for_replacing_scene_items", 1),
          (item_set_slot, ":item_no", slot_item_num_positions, ":num_positions"),
        (try_end),
        (replace_scene_items_with_scene_props, ":item_no", "spr_empty"),
      (try_end),
     ])
]
