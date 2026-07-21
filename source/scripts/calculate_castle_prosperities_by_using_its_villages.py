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

calculate_castle_prosperities_by_using_its_villages_scripts = [
#script_calculate_castle_prosperities_by_using_its_villages
(
  "calculate_castle_prosperities_by_using_its_villages",
  [
    (try_for_range, ":cur_castle", castles_begin, castles_end),
      (assign, ":total_prosperity", 0),
      (assign, ":total_villages", 0),

      (try_for_range, ":cur_village", villages_begin, villages_end),
        (party_get_slot, ":bound_center", ":cur_village", slot_village_bound_center),
        (eq, ":cur_castle", ":bound_center"),

        (party_get_slot, ":village_prosperity", ":cur_village", slot_town_prosperity),

        (val_add, ":total_prosperity", ":village_prosperity"),
        (val_add, ":total_villages", 1),
      (try_end),

      (try_begin),
        (store_div, ":castle_prosperity", ":total_prosperity", ":total_villages"),
      (else_try),
        (assign, ":castle_prosperity", 50),
      (try_end),

      (party_set_slot, ":cur_castle", slot_town_prosperity, ":castle_prosperity"),
    (try_end),
  ])
]
