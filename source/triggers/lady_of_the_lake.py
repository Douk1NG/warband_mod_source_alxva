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




#NPC system changes end
#SB : change interval
# Lady of the lake achievement
   

lady_of_the_lake_triggers = [
(12, 0, 0,
   [
     # (troop_get_type, ":is_female", "trp_player"),
     (eq, "$character_gender", tf_female),

    ],
   [
     (assign, ":inv_cap", companions_end),
     (try_for_range, ":companion", companions_begin, ":inv_cap"),
       (troop_slot_eq, ":companion", slot_troop_occupation, slto_player_companion),

       # (troop_get_inventory_capacity, ":inv_cap", ":companion"),
       (try_for_range, ":i_slot", 0, ek_head),
         (troop_get_inventory_slot, ":item_id", ":companion", ":i_slot"),

		 (ge, ":item_id", 0),

	 	 (this_or_next|eq, ":item_id", "itm_great_sword"),
	 	 (this_or_next|eq, ":item_id", "itm_sword_two_handed_a"),
		 (eq, ":item_id", "itm_strange_great_sword"),

		 (unlock_achievement, ACHIEVEMENT_LADY_OF_THE_LAKE),
		 (assign, ":inv_cap", 0),
	   (try_end),
	 (try_end),
   ]
   ),
]
