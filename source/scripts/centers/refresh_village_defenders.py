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

refresh_village_defenders_scripts = [
# script_refresh_village_defenders
# Input: arg1 = village_no
# Output: none
("refresh_village_defenders",
    [
      (store_script_param_1, ":village_no"),

      (assign, ":ideal_size", 50),
      (try_begin),
        (party_get_num_companions, ":party_size", ":village_no"),
        (lt, ":party_size", ":ideal_size"),
        #SB : add restriction of not reinforcing while looted or infested
        (call_script, "script_cf_village_normal_cond", ":village_no"),
        (party_add_template, ":village_no", "pt_village_defenders"),

        (try_begin), #SB : upgrade into watchmen, each template had at least 10 farmers
          (party_slot_ge, ":village_no", slot_center_has_watch_tower, 1),
          (party_count_companions_of_type, ":count", ":village_no", "trp_watchman"),
          (lt, ":count", 10),
          (store_random_in_range, ":random_no", 2, 5),
          (party_add_members, ":village_no", "trp_watchman", ":random_no"),
          (party_remove_members, ":village_no", "trp_farmer"),
        (try_end),
        (try_begin), #SB : add messenger
          (party_slot_ge, ":village_no", slot_center_has_messenger_post, 1),
          (store_faction_of_party, ":faction_no", ":village_no"),
          (assign, ":troop", "trp_dplmc_messenger"),
          (try_begin),
            (is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
            (faction_get_slot, ":troop", ":faction_no", slot_faction_messenger_troop),
          (try_end),
          (party_count_companions_of_type, ":count", ":village_no", ":troop"),
          (lt, ":count", 1),
          (party_add_members, ":village_no", ":troop", 1),
        (try_end),
      (try_end),
  ])
]
