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

kill_cattle_from_herd_scripts = [
("kill_cattle_from_herd",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":amount"),

      (troop_clear_inventory, "trp_temp_troop"),
      (store_mul, ":meat_amount", ":amount", 2),
      (troop_add_items, "trp_temp_troop", "itm_cattle_meat", ":meat_amount"),

      (troop_get_inventory_capacity, ":inv_size", "trp_temp_troop"),
      (try_for_range, ":i_slot", 0, ":inv_size"),
        (troop_get_inventory_slot, ":item_id", "trp_temp_troop", ":i_slot"),
        (eq, ":item_id", "itm_cattle_meat"),
        (troop_set_inventory_slot_modifier, "trp_temp_troop", ":i_slot", imod_fresh),
      (try_end),

      (party_get_num_companions, ":num_cattle", ":party_no"),
      (try_begin),
        (ge, ":amount", ":num_cattle"),
        (remove_party, ":party_no"),
      (else_try),
        (party_remove_members, ":party_no", "trp_cattle", ":amount"),
      (try_end),
      ])
]
