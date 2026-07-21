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

shuffle_troop_slots_scripts = [
("shuffle_troop_slots",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":slots_begin", 2),
      (store_script_param, ":slots_end", 3),
      (try_for_range, ":cur_slot_no", ":slots_begin", ":slots_end"),
        (store_random_in_range, ":random_slot_no", ":slots_begin", ":slots_end"), #reg(58) = random slot. Now exchange slots reg(57) and reg(58)
        (troop_get_slot, ":cur_slot_value", ":troop_no", ":cur_slot_no"), #temporarily store the value in slot reg(57) in reg(59)
        (troop_get_slot, ":random_slot_value", ":troop_no", ":random_slot_no"), #temporarily store the value in slot reg(58) in reg(60)
        (troop_set_slot, ":troop_no", ":cur_slot_no", ":random_slot_value"), # Now exchange the two...
        (troop_set_slot, ":troop_no", ":random_slot_no", ":cur_slot_value"),
      (try_end),
  ])
]
