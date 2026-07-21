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

cf_get_random_active_faction_except_player_faction_and_faction_scripts = [
# script_cf_get_random_active_faction_except_player_faction_and_faction
# Input: arg1 = except_faction_no
# Output: reg0 = random_faction
("cf_get_random_active_faction_except_player_faction_and_faction",
    [
      (store_script_param_1, ":except_faction_no"),
      (assign, ":num_factions", 0),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (neq, ":faction_no", ":except_faction_no"),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (val_add, ":num_factions", 1),
      (try_end),
      (gt, ":num_factions", 0),
      (assign, ":selected_faction", -1),
      (store_random_in_range, ":random_faction", 0, ":num_factions"),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (ge, ":random_faction", 0),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (neq, ":faction_no", ":except_faction_no"),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (val_sub, ":random_faction", 1),
        (lt, ":random_faction", 0),
        (assign, ":selected_faction", ":faction_no"),
      (try_end),
      (assign, reg0, ":selected_faction"),
  ])
]
