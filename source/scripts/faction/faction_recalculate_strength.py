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

faction_recalculate_strength_scripts = [
# script_faction_recalculate_strength
# Input: arg1 = faction_no
# Output: reg0 = strength
("faction_recalculate_strength",
   [
      (store_script_param_1, ":faction_no"),

      (call_script, "script_faction_get_number_of_armies", ":faction_no"),
      (assign, ":num_armies", reg0),
      (assign, ":num_castles", 0),
      (assign, ":num_towns", 0),

      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (eq, ":center_faction", ":faction_no"),
        (try_begin),
          (party_slot_eq, ":center_no", slot_party_type, spt_castle),
          (val_add, ":num_castles", 1),
        (else_try),
          (party_slot_eq, ":center_no", slot_party_type, spt_town),
          (val_add, ":num_towns", 1),
        (try_end),
      (try_end),

      (faction_set_slot, ":faction_no", slot_faction_num_armies, ":num_armies"),
      (faction_set_slot, ":faction_no", slot_faction_num_castles, ":num_castles"),
      (faction_set_slot, ":faction_no", slot_faction_num_towns, ":num_towns"),

    ])
]
