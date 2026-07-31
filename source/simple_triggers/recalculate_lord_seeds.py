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



    #recalculate lord random decision seeds once in every week
	

recalculate_lord_seeds_simple_triggers = [
(24 * 7,
	[
	  ##diplomacy start+ Kingdom ladies should also have their decision seeds updated.
	  ##                 Also, use 10000 instead of 9999, since the upper bound for store_random_in_range is exclusive.
	  ##OLD:
      #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
      #  (store_random_in_range, ":random", 0, 9999),
	  ##NEW:
	  (try_for_range, ":troop_no", heroes_begin, heroes_end),
	     (store_random_in_range, ":random", 0, 10000),
	  ##diplomacy end+
        (troop_set_slot, ":troop_no", slot_troop_temp_decision_seed, ":random"),
      (try_end),

	  ##diplomacy start+ Also update the temporary seed for the player
	  (store_random_in_range, ":random", 0, 10000),
	  (troop_set_slot, "trp_player", slot_troop_temp_decision_seed, ":random"),
	  ##diplomacy end+

	#npcs will only change their minds on issues at least 24 hours after speaking to the player
    #(store_current_hours, ":hours"),
    #(try_begin),
    #  (eq, 1, 0), #disabled
    #  (try_for_range, ":npc", active_npcs_begin, active_npcs_end),
    #    (troop_get_slot, ":last_talk", ":npc", slot_troop_last_talk_time),
    #    (val_sub, ":hours", ":last_talk"),
    #    (ge, ":hours", 24),
    #    (store_random_in_range, ":random", 0, 9999),
    #    (troop_set_slot, ":npc", slot_troop_temp_decision_seed, ":random"),
    #  (try_end),
    #(try_end),
	]),
]
