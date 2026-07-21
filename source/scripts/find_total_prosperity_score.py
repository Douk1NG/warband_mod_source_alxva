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

find_total_prosperity_score_scripts = [
#script_cf_has_companion_emissary for diplomatic options
(
	"find_total_prosperity_score",
	[
	  (store_script_param, ":center_no", 1),

      (try_begin), #":total_prosperity_score" changes between 10..100
        (is_between, ":center_no", walled_centers_begin, walled_centers_end),

        (party_get_slot, ":center_prosperity", ":center_no", slot_town_prosperity),
        (store_add, ":center_prosperity_add_200_div_10", ":center_prosperity", 200),
        (val_div, ":center_prosperity_add_200_div_10", 10),
        (try_begin),
          (is_between, ":center_no", towns_begin, towns_end),
          (store_mul, ":this_center_score", ":center_prosperity_add_200_div_10", 15),
        (else_try),
          (store_mul, ":this_center_score", ":center_prosperity_add_200_div_10", 5),
        (try_end),
        (assign, ":total_prosperity_score", ":this_center_score"),

        (try_for_range_backwards, ":village_no", villages_begin, villages_end),
          (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),

          (party_get_slot, ":village_prosperity", ":village_no", slot_town_prosperity),
          (store_add, ":village_prosperity_add_200_div_10", ":village_prosperity", 200),
          (val_div, ":village_prosperity_add_200_div_10", 10),
          (store_mul, ":this_village_score", ":village_prosperity_add_200_div_10", 5),

          (val_add, ":total_prosperity_score", ":this_village_score"),
        (try_end),
      (else_try),
        (party_get_slot, ":center_prosperity", ":center_no", slot_town_prosperity),
        (store_add, ":center_prosperity_add_200_div_10", ":center_prosperity", 200),
        (val_div, ":center_prosperity_add_200_div_10", 10),
        (store_mul, ":this_center_score", ":center_prosperity_add_200_div_10", 5),
        (assign, ":total_prosperity_score", ":this_center_score"),
      (try_end),
      (val_div, ":total_prosperity_score", 10),

      (assign, reg0, ":total_prosperity_score"),
	])
]
