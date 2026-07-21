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

cf_select_random_walled_center_with_faction_and_owner_priority_no_siege_scripts = [
#script_cf_select_random_walled_center_with_faction_and_owner_priority_no_siege:
# INPUT:
# arg1 = faction_no
# arg2 = owner_troop_no
#OUTPUT:
# This script may return false if there is no matching town.
# reg0 = center_no (Can fail)
("cf_select_random_walled_center_with_faction_and_owner_priority_no_siege",
    [
      (store_script_param, ":faction_no", 1),
      (store_script_param, ":troop_no", 2),
      (assign, ":result", -1),
      (assign, ":no_centers", 0),

      #SB : faction active conditional
      (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
      (call_script, "script_lord_get_home_center", ":troop_no"),
      (assign, ":home_center", reg0),

      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_add, ":no_centers", 1),

        #(party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
        (eq, ":home_center", ":cur_center"), #I changed it with above line, now if lord is owner of any village its bound walled center is counted as 1000. Better this way. ozan-18.01.09

        (val_add, ":no_centers", 1000),
      (try_end),

      #if no center is available count all centers not besieged do not care its faction.
      (try_begin),
        (le, ":no_centers", 0),
        (ge, "$g_dplmc_lord_recycling", DPLMC_LORD_RECYCLING_ENABLE),
        (assign, "$g_there_is_no_avaliable_centers", 1),

        (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
          #SB : probably original faction
          (party_slot_eq, ":cur_center", slot_center_original_faction, ":faction_no"),
          (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
          (val_add, ":no_centers", 1),
        (try_end),
      (else_try),
        (assign, "$g_there_is_no_avaliable_centers", 0),
      (try_end),

      # (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader), #SB : only one check
      (this_or_next|eq, "$g_there_is_no_avaliable_centers", 0),
      (neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"), #faction leaders cannot spawn if they have no centers.

      (store_random_in_range, ":random_center", 0, ":no_centers"),
      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (this_or_next|eq, "$g_there_is_no_avaliable_centers", 1),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          #(party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
          (eq, ":home_center", ":cur_center"), #I changed it with above line, now if lord is owner of any village its bound walled center is counted as 1000. Better this way. ozan-18.01.09
          (eq, "$g_there_is_no_avaliable_centers", 0),

          (val_sub, ":random_center", 1000),
        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
      (try_end),
      (assign, reg0, ":result"),
  ])
]
