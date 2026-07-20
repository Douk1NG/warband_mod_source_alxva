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

cf_no_known_taverngoers_scripts = [
#Adapted "auto-sell" from rubik's Custom Commander
#does not account for alternative towns
("cf_no_known_taverngoers",
  [
      (store_script_param_1, ":begin"),
      (store_script_param_2, ":end"),
      # (assign, ":num_towns", tavern_booksellers_end),
      (try_for_range, ":troop_no", ":begin", ":end"),
        # (neg|party_slot_eq, ":town_no", slot_center_tavern_bookseller, 0),
        # (party_get_slot, ":seller", ":town_no", slot_center_tavern_bookseller),#addition - fixed 2011-03-29
        (troop_slot_ge, ":troop_no", slot_troop_met, 1),
        (troop_get_slot, ":town_no", ":troop_no", slot_troop_cur_center),
        (is_between, ":town_no", walled_centers_begin, walled_centers_end),
        (assign, ":end", ":begin"), #loop break
      (try_end),
      (neq, ":begin", ":end"),
  ])
]
