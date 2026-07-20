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

new_order_of_item_types_scripts = [
("new_order_of_item_types",
    [
      (troop_set_slot, "trp_temp_array_sort", 0, itp_type_book),
      (troop_set_slot, "trp_temp_array_sort", 1, itp_type_horse),
      (troop_set_slot, "trp_temp_array_sort", 2, itp_type_one_handed_wpn),
      (troop_set_slot, "trp_temp_array_sort", 3, itp_type_two_handed_wpn),
      (troop_set_slot, "trp_temp_array_sort", 4, itp_type_polearm),
      (troop_set_slot, "trp_temp_array_sort", 5, itp_type_bow),
      (troop_set_slot, "trp_temp_array_sort", 6, itp_type_arrows),
      (troop_set_slot, "trp_temp_array_sort", 7, itp_type_crossbow),
      (troop_set_slot, "trp_temp_array_sort", 8, itp_type_bolts),
      (troop_set_slot, "trp_temp_array_sort", 9, itp_type_thrown),
      (troop_set_slot, "trp_temp_array_sort", 10, itp_type_pistol),
      (troop_set_slot, "trp_temp_array_sort", 11, itp_type_musket),
      (troop_set_slot, "trp_temp_array_sort", 12, itp_type_bullets),
      (troop_set_slot, "trp_temp_array_sort", 13, itp_type_shield),
      (troop_set_slot, "trp_temp_array_sort", 14, itp_type_head_armor),
      (troop_set_slot, "trp_temp_array_sort", 15, itp_type_body_armor),
      (troop_set_slot, "trp_temp_array_sort", 16, itp_type_foot_armor),
      (troop_set_slot, "trp_temp_array_sort", 17, itp_type_hand_armor),
      (troop_set_slot, "trp_temp_array_sort", 18, itp_type_goods),
      (troop_set_slot, "trp_temp_array_sort", 19, itp_type_animal),
    ])
]
