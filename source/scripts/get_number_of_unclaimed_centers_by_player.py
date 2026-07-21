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

get_number_of_unclaimed_centers_by_player_scripts = [
# script_enter_court
# Input: none
# Output: reg0 = number of unclaimed centers, reg1 = last unclaimed center_no
("get_number_of_unclaimed_centers_by_player",
    [
      (assign, ":unclaimed_centers", 0),
      (assign, reg1, -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":faction_no", ":center_no"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (party_slot_eq, ":center_no", slot_town_claimed_by_player, 0),
        (party_get_num_companion_stacks, ":num_stacks", ":center_no"),
        (ge, ":num_stacks", 1), #castle is garrisoned
        (assign, reg1, ":center_no"),
        (val_add, ":unclaimed_centers", 1),
      (try_end),
      (assign, reg0, ":unclaimed_centers"),
  ])
]
