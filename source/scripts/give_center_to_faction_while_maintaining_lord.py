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

give_center_to_faction_while_maintaining_lord_scripts = [
# Input: arg1 = center_no, arg2 = faction
("give_center_to_faction_while_maintaining_lord",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":faction_no"),

      (store_faction_of_party, ":old_faction", ":center_no"),
	  ##diplomacy start+
	  #If the player, previously the head of his own faction, is now joining
	  #an NPC faction, don't reset the "last taken" time or the "ex faction"
	  #slots.
	  (try_begin),
		#Friendly transfer: don't update transfer time or ex-faction
		(eq, ":old_faction", "fac_player_supporters_faction"),
		(eq, ":faction_no", "$players_kingdom"),
	  (else_try),
		#Defection: update transfer time and ex-faction
		(party_set_slot, ":center_no", slot_center_ex_faction, ":old_faction"),
		(store_current_hours, ":cur_hours"),
		(party_set_slot, ":center_no", dplmc_slot_center_last_transfer_time, ":cur_hours"),
	  (try_end),
	  ##diplomacy end+
      (party_set_faction, ":center_no", ":faction_no"),

      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        #SB : reinforcement
        (try_begin),
          (party_get_slot, ":farmer_party", ":center_no", slot_village_farmer_party),
          (gt, ":farmer_party", 0),
          (party_is_active, ":farmer_party"),
          (party_set_faction, ":farmer_party", ":faction_no"),
        (try_end),
        (try_begin),
          (party_get_slot, ":reinf_party", ":center_no", slot_village_reinforcement_party),
          (gt, ":reinf_party", 0),
          (party_is_active, ":reinf_party"),
          (party_set_faction, ":reinf_party", ":faction_no"),
        (try_end),
      (try_end),

      (call_script, "script_update_faction_notes", ":faction_no"),
      (call_script, "script_update_center_notes", ":center_no"),

      (try_for_range, ":other_center", centers_begin, centers_end),
        (party_slot_eq, ":other_center", slot_village_bound_center, ":center_no"),
        (call_script, "script_give_center_to_faction_while_maintaining_lord", ":other_center", ":faction_no"),
      (try_end),
  ])
]
