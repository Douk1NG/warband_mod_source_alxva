# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *

kingdom_attitude_changes_simple_triggers = [
(24,
   [
      (try_for_range, ":faction1", npc_kingdoms_begin, npc_kingdoms_end),
        (assign, ":attitude_change", 2), #positive means good attitude
        (try_for_range, ":faction2", kingdoms_begin, kingdoms_end),
          (neq, ":faction1", ":faction2"),
		  ##diplomacy start+
		  #FIX: Stop the attitude change from carrying over from the previous kingdom!
		  (assign, ":attitude_change", 2),
		  #Handling for fac_player_supporters_faction & players_kingdom
		  (assign, ":alt_faction", ":faction2"),
		  (try_begin),
		     (eq, ":faction2", "fac_player_supporters_faction"),
			 (neq, ":faction1", "$players_kingdom"),
			 (assign, ":alt_faction", "$players_kingdom"),
		  (else_try),
		     (eq, ":faction2", "$players_kingdom"),
			 (assign, ":alt_faction", "fac_player_supporters_faction"),
		  (try_end),
		  ##Make loop less wasteful.
		  ##OLD:
          #(try_for_parties, ":party"),
          #  (is_between, ":party", centers_begin, centers_end),
		  ##NEW:
		  (try_for_range, ":party", centers_begin, centers_end),
		  ##diplomacy end+
            (store_faction_of_party, ":party_faction", ":party"),
			##diplomacy start+
			##FIX broken slot check!
			##ADD support for player's faction
			##OLD:
            #(eq, ":party_faction", ":faction2"),
            #(party_slot_eq, ":faction1", ":party", slot_center_original_faction),
			##NEW:
			(this_or_next|eq, ":party_faction", ":faction2"),
				(eq, ":party_faction", ":alt_faction"),
			(party_slot_eq, ":party", slot_center_original_faction, ":faction1"),
			#Don't subtract relation when it would be nonsensical
			(this_or_next|neq, ":faction1", "$players_kingdom"),
			(this_or_next|neq, ":faction2", "fac_player_supporters_faction"),
				(party_slot_ge, ":party", dplmc_slot_center_original_lord, 1),
			##diplomacy end+
            (val_sub, ":attitude_change", 1), #less attitude
          (try_end),

          (try_for_range, ":faction3", kingdoms_begin, kingdoms_end),
            (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":faction2", ":faction3"),
            (eq, reg0, -2), #war between 2 and 3
            (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":faction1", ":faction3"),
            (eq, reg0, -2), #war between 1 and 3
            (val_add, ":attitude_change", 1), #higher attitude
          (try_end),
        (try_end),

        (store_add, ":faction1_to_faction2_slot", ":faction2", dplmc_slot_faction_attitude_begin),
        (party_set_slot, ":faction1", ":faction1_to_faction2_slot", ":attitude_change"),
      (try_end),
    ]),
]
