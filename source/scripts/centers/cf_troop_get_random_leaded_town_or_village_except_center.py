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

cf_troop_get_random_leaded_town_or_village_except_center_scripts = [
# script_cf_troop_get_random_leaded_town_or_village_except_center
# Input: arg1 = troop_no, arg2 = except_center_no
# Output: reg0 = center_no (Can fail)
#SB : only called from checking qst_collect_taxes, apply condition as follows
## not close to arg2 (Native only checks if quest giver is inside town)
## not under siege/raided (arg3)
("cf_troop_get_random_leaded_town_or_village_except_center",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":except_center_no", 2), #unused I guess
      (store_script_param, ":center_state", 3), #pass in svs_normal

	  #SB : re-use except_center_no as a check
	  (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
	  (try_begin),
	    (le, ":party_no", 0),
		(assign, ":party_no", ":except_center_no"),
	  (try_end),
      (assign, ":num_centers", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),

	    # (party_set_slot, ":center_no", slot_party_temp_slot_1, 0),
        (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (neq, ":center_no", ":except_center_no"),
		(assign, ":dist", 9999),
		(try_begin),
		  (gt, ":party_no", 0),
		  (store_distance_to_party_from_party, ":dist", ":center_no", ":party_no"),
		(try_end),
		(gt, ":dist", 15), #can't be within a day's travel
		(party_slot_eq, ":center_no", slot_village_state, ":center_state"),
		# (party_set_slot, ":center_no", slot_party_temp_slot_1, 1),
		(troop_set_slot, "trp_random_town_sequence", ":num_centers", ":center_no"),
        (val_add, ":num_centers", 1),
      (try_end),

      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
	  (troop_get_slot, reg0, "trp_random_town_sequence", ":random_center"),
      # (assign, ":end_cond", centers_end),
      # (try_for_range, ":center_no", centers_begin, ":end_cond"),
        # (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        # (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        # (neq, ":center_no", ":except_center_no"),
        # (val_sub, ":random_center", 1),
        # (lt, ":random_center", 0),
        # (assign, ":target_center", ":center_no"),
        # (assign, ":end_cond", 0),
      # (try_end),
      # (assign, reg0, ":target_center"),
  ])
]
