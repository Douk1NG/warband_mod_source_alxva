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



    # Count faction armies
    

decide_faction_ai_flag_simple_triggers = [
(24,
    [
       (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
         (call_script, "script_faction_recalculate_strength", ":faction_no"),
         #SB : add stability call every 24
         (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active), #dckplmc - causes script errors if faction is defeated
         (call_script, "script_evaluate_realm_stability", ":faction_no"),
       (try_end),
	   ##diplomacy start+ Add support for promoted kingdom ladies
	   ##OLD:
	   #(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
	   ##NEW:
	   (try_for_range, ":active_npc", heroes_begin, heroes_end),
	    (this_or_next|is_between, ":active_npc", active_npcs_begin, active_npcs_end),
	    (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
	   ##diplomacy end+
		(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
		(neg|faction_slot_eq, ":active_npc_faction", slot_faction_ai_state, sfai_default),
		(neg|faction_slot_eq, ":active_npc_faction", slot_faction_ai_state, sfai_feast),
		(neg|faction_slot_eq, ":active_npc_faction", slot_faction_ai_state, sfai_gathering_army),

		(troop_get_slot, ":active_npc_party", ":active_npc", slot_troop_leaded_party),
		(party_is_active, ":active_npc_party"),

		(val_add, "$total_vassal_days_on_campaign", 1),

	    (party_slot_eq, ":active_npc_party", slot_party_ai_state, spai_accompanying_army),
		(val_add, "$total_vassal_days_responding_to_campaign", 1),


	   (try_end),

    ]),
]
