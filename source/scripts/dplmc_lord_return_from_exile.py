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

dplmc_lord_return_from_exile_scripts = [
# INPUT: arg1 = troop_id, arg2 = new faction_no
# OUTPUT: none
("dplmc_lord_return_from_exile",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":faction_no"),
      #Check validity
	  (try_begin),
		  (is_between, ":troop_no", heroes_begin, heroes_end),
		  (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
		  (neq, ":troop_no", "trp_player"),
		  (faction_get_slot, ":faction_liege", ":faction_no", slot_faction_leader),
		  #The lord definitely should not already belong to a kingdom
		  (store_troop_faction, ":old_faction", ":troop_no"),
		  (neg|is_between, ":old_faction", kingdoms_begin, kingdoms_end),
		  (try_begin),
			#Handle separately for adding to the player's faction
			#The player may decide to accept or reject the return
			(this_or_next|eq, ":faction_liege", "trp_player"),
			(eq, ":faction_no", "fac_player_supporters_faction"),
			#(eq, 1, 0),#<-- temporarily disable
			#Lord comes to petition the player instead of automatically returning
			(call_script, "script_change_troop_faction", ":troop_no", ":faction_no"),
			(troop_set_slot, ":troop_no", slot_troop_occupation, slto_inactive),
			#Show event (no log without actual faction change)
			(str_store_troop_name_link, s4, ":troop_no"),
			(str_store_faction_name_link, s5, ":faction_no"),
			(faction_get_color, ":color", ":faction_no"), #SB : store colour for logs
			(str_store_troop_name_link, s6, ":faction_liege"),
			(display_message, "@{s4} has returned from exile, seeking refuge with {s6} of {s5}.", ":color"),
		    #Remove party
			(troop_get_slot, ":led_party", ":troop_no", slot_troop_leaded_party),
			(try_begin),
				(party_is_active, ":led_party"),
				(neq, ":led_party", "p_main_party"),
				(remove_party, ":led_party"),
				(troop_set_slot, ":troop_no", slot_troop_leaded_party, -1),
			(try_end),
			#
		  (else_try),
			 #NPC king auto-accepts
			 #Normalize relation between NPC and king
			 (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_liege"),
			 (store_sub, ":relation_change", 0, reg0),#enough to increase to 0 if negative
			 (val_max, ":relation_change", 5),
			 (call_script, "script_troop_change_relation_with_troop", ":troop_no", ":faction_liege", ":relation_change"),
			 #Perform reverse of relation change for exile
			 (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end), #all lords in own faction, and relatives regardless of faction
				(assign, ":relation_change", 0),#no change for non-relatives in other factions
				(try_begin),
					(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
					(eq, ":faction_no", ":active_npc_faction"),
					#Auto-exiling someone at -75 relation to his liege gives a -1 base
					#relation penalty from other lords, so the gain is 1 by default.
					(assign, ":relation_change", 1),
				(try_end),
				##(call_script, "script_troop_get_family_relation_to_troop", ":troop_no", ":active_npc"),
				(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":troop_no", ":active_npc"),
				(assign, ":family_relation", reg0),
				(try_begin),
					(gt, ":family_relation", 1),
					(store_div, ":family_modifier", reg0, 3),
					(val_add, ":relation_change", ":family_modifier"),
				(try_end),

				(neq, ":relation_change", 0),

				(call_script, "script_troop_change_relation_with_troop", ":faction_liege", ":active_npc", ":relation_change"),
				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_troop_name, s17, ":active_npc"),
					(str_store_troop_name, s18, ":faction_liege"),
					(assign, reg3, ":relation_change"),
					(display_message, "str_trial_influences_s17s_relation_with_s18_by_reg3"),
				(try_end),
			 (try_end),#end try for range :active_npc

			#Now actually change the faction
			(call_script, "script_change_troop_faction", ":troop_no", ":faction_no"),
			(try_begin), #new-begin
				(neq, ":faction_no", "fac_player_supporters_faction"),
				(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),
					(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_retirement),
					(troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_exile), #SB : revoke exile
				(troop_set_slot, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		    (try_end), #new-end

			#Log event
			(str_store_troop_name_link, s4, ":troop_no"),
			(str_store_faction_name_link, s5, ":faction_no"),
			(str_store_troop_name_link, s6, ":faction_liege"),
			(faction_get_color, ":color", ":faction_no"), #SB : store colour for logs
			(display_log_message, "@{s4} has been granted a pardon by {s6} of {s5} and has returned from exile.", ":color"),

            #SB : spawn full army
            (troop_set_slot, ":troop_no", slot_troop_spawned_before, 0),
			(troop_get_slot, ":led_party", ":troop_no", slot_troop_leaded_party),
			(try_begin),
				(party_is_active, ":led_party"),
				(neq, ":led_party", "p_main_party"),
				(remove_party, ":led_party"),
				(troop_set_slot, ":troop_no", slot_troop_leaded_party, -1),
			(try_end),
		  (try_end),#end NPC king auto-accepts
      (else_try),
	    #Failure.  Perform string register assignment first to avoid differences
		#between debug and non-debug behavior.
		(str_store_troop_name, s5, ":troop_no"),
		(str_store_faction_name, s7, ":faction_no"),
		#(ge, "$cheat_mode", 1),#<-- always show this
		(display_message, "@{!}DEBUG : failure in dplmc_lord_return_from_exile((s5}, {s7})"),
	  (try_end),
    ])
]
