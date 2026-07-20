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

replace_scene_items_with_spawn_items_after_ms_scripts = [
("replace_scene_items_with_spawn_items_after_ms",
    [
      (try_for_range, ":item_no", all_items_begin, all_items_end),
        (item_get_slot,  ":num_positions", ":item_no", slot_item_num_positions),
        (item_get_type, ":item_type",":item_no"),
        (try_for_range, ":cur_position", 0, ":num_positions"),
          (store_add, ":cur_slot", slot_item_positions_begin, ":cur_position"),
          (item_get_slot, ":pos_no", ":item_no", ":cur_slot"),
          (set_spawn_position, ":pos_no"),
          (try_begin),
            (eq, ":item_type", itp_type_horse),
            (spawn_horse, ":item_no"),
          (else_try),
            (spawn_item, ":item_no", 0),
          (try_end),
        (try_end),
      (try_end),
     ])
]
