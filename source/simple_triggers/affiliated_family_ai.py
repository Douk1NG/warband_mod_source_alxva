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



  # affilated family ai
   

affiliated_family_ai_simple_triggers = [
(24 * 7,
   [
	##nested diplomacy start+ (piggyback on this trigger) allow lords to return from exile
	(assign, ":save_reg0", reg0),
	(assign, ":save_reg1", reg1),
	(assign, ":save_reg4", reg4),
	(try_begin),
		#only proceed if setting is enabled
		(ge, "$g_dplmc_lord_recycling", DPLMC_LORD_RECYCLING_ENABLE),
		#Kings/pretenders do not return in this manner (it should be different if it does happen).
		#Companions have a separate mechanism for return.
		(assign, ":chosen_lord", -1),
		(assign, ":best_score", -101),
		(assign, ":num_exiles", 0),
		#iterate over lords from a random start point, wrapping back to zero
		(store_random_in_range, ":rand_no", lords_begin, lords_end),
		(try_for_range, ":index", lords_begin, lords_end),
		  (store_add, ":troop_no", ":rand_no", ":index"),
		  (try_begin),
			 #wrap back around when you go off the end
			  (ge, ":troop_no", lords_end),
			(val_sub, ":troop_no", lords_end),
			(val_add, ":troop_no", lords_begin),
		  (try_end),
		  #Elsewhere we do the bookkeeping of ensuring that when a lord gets exiled
		  #his occupation changes to dplmc_slto_exile, and when loading a Native
		  #saved gamed with diplomacy we make this change for any lords required.
		  (troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_exile),

		  (store_troop_faction, ":faction_no", ":troop_no"),
		  (this_or_next|eq, ":faction_no", -1),
		  (this_or_next|eq, ":faction_no", "fac_commoners"),
			 (eq, ":faction_no", "fac_outlaws"),
		  (val_add, ":num_exiles", 1),
		  (try_begin),
		     #Pick the lord with the best relation with his original liege.
			  #In most cases this will be the lord that has been in exile
			  #the longest.
			  (troop_get_slot, ":new_faction", ":troop_no", slot_troop_original_faction),
			  (is_between, ":new_faction", kingdoms_begin, kingdoms_end),
			  (faction_get_slot, ":faction_leader", ":new_faction", slot_faction_leader),
			  (gt, ":faction_leader", 0),
			  (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
			  (this_or_next|eq, ":chosen_lord", -1),
			     (gt, reg0, ":best_score"),
			  (assign, ":chosen_lord", ":troop_no"),
			  (assign, ":best_score", reg0),
		  (else_try),
		     (eq, ":chosen_lord", -1),
			 (assign, ":chosen_lord", ":troop_no"),
		  (try_end),
      (try_end),
		#search is done
		(try_begin),
		 #no lord found
		 (eq, ":chosen_lord", -1),
		 (try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "@{!}DEBUG - no eligible lords in exile"),
		 (try_end),
	    (else_try),
			#If there were fewer than 3 lords in exile, random chance that none will return.
			(lt, ":num_exiles", 3),
			(store_random_in_range, ":random", 0, 256),
			(ge, ":random", 128),
			(try_begin),
				(ge, "$cheat_mode", 1),
				(assign, reg0, ":num_exiles"),
				(display_message, "@{!}DEBUG - {reg0} lords found in exile; randomly decided not to try to return anyone."),
			(try_end),
		(else_try),
		 #found a lord
		 (neq, ":chosen_lord", -1),
		 (try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":chosen_lord"),
			(assign, reg0, ":best_score"),
			(assign, reg1, ":num_exiles"),
			(display_message, "@{!}DEBUG - {reg1} lords found in exile; {s4} chosen to return, score was {reg0}"),
		 (try_end),
		 #To decrease the displeasing fragmentation of lord cultures, bias towards assigning
		 #the lord back to his original faction if possible.
		 (troop_get_slot, ":new_faction", ":chosen_lord", slot_troop_original_faction),
		 (try_begin),
			 #If the original faction is not active, or the lord's relation is too low, use a different faction
			 (this_or_next|lt, ":best_score", -50),
			 (this_or_next|neg|is_between, ":new_faction", kingdoms_begin, kingdoms_end),
			    (neg|faction_slot_eq, ":new_faction", slot_faction_state, sfs_active),
		    (call_script, "script_lord_find_alternative_faction", ":chosen_lord"),
			(assign, ":new_faction", reg0),
		 (try_end),
		 (try_begin),
		   (neg|is_between, ":new_faction", kingdoms_begin, kingdoms_end),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":chosen_lord"),
			(display_message, "@{!}DEBUG - {s4} found no faction to return to!"),
		 (try_end),
		 (is_between, ":new_faction", kingdoms_begin, kingdoms_end),
		 (assign, ":num_inactive", 0),
		 (try_begin),
			(eq, ":new_faction", "$players_kingdom"),
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":num_inactive", 0),
			(try_for_range, ":other_lord", lords_begin, lords_end),
			   (store_troop_faction, ":other_lord_faction", ":other_lord"),
			   (this_or_next|eq, ":other_lord_faction", "fac_player_supporters_faction"),
				(eq, ":other_lord_faction", "$players_kingdom"),
			   (troop_slot_eq, ":other_lord", slot_troop_occupation, slto_inactive),
			   (val_add, ":num_inactive", 1),
			(try_end),
			(gt, ":num_inactive", 1),
			(try_begin),
				(ge, "$cheat_mode", 1),
				(assign, reg0, ":num_inactive"),
				(display_message, "@{!}DEBUG - Not returning a lord to the player's kingdom, since there are already {reg0} lords waiting for their petitions to be heard."),
			(try_end),
		 (else_try),
			(call_script, "script_dplmc_lord_return_from_exile", ":chosen_lord", ":new_faction"),
		 (try_end),
		(try_end),
	(try_end),
	##More piggybacking
	##
	(assign, reg0, ":save_reg0"),
	(assign, reg1, ":save_reg1"),
	(assign, reg4, ":save_reg4"),
	##nested diplomacy end+
    (is_between, "$g_player_affiliated_troop", lords_begin, kingdom_ladies_end),
	##nested diplomacy start+
	(assign, ":best_relation", -101),
	(assign, ":worst_relation", 101),

	(assign, ":num_at_least_20", 0),
	(assign, ":num_below_0", 0),

	(assign, ":good_relation", 0),
	##nested diplomacy end+

    (assign, ":bad_relation", 0),
    (try_for_range, ":family_member", lords_begin, kingdom_ladies_end),
      (call_script, "script_dplmc_is_affiliated_family_member", ":family_member"),
      (gt, reg0, 0),
      (call_script, "script_troop_get_player_relation", ":family_member"),
	  ##nested diplomacy start+
	  #(le, reg0, -20),
	  #(assign, ":bad_relation", ":family_member"),
  	  (try_begin),
		(lt, reg0, 0),
		(val_add, ":num_below_0", 1),
		(le, reg0, ":worst_relation"),
		(assign, ":bad_relation", ":family_member"),
	  (else_try),
		(ge, reg0, 20),
		(val_add, ":num_at_least_20", 1),
		(gt, reg0, ":best_relation"),
		(assign, ":good_relation", ":family_member"),
	  (try_end),

	  (val_max, ":best_relation", reg0),
	  (val_min, ":worst_relation", reg0),
	  ##nested diplomacy end+
    (try_end),
	##nested diplomacy start+
	(try_begin),
		(gt, ":worst_relation", -15),
		(assign, ":bad_relation", 0),#suppress with no message
	(else_try),
		(gt, ":worst_relation", -20),
		(str_store_troop_name_link, s0, ":bad_relation"),  #SB : link message, no colours
		(display_message, "@{s0} is grumbling against you.  Your affiliation could be jeopardized if this continues."),
		(str_clear, s0),
	(else_try),
		(neq, ":bad_relation", 0),
		(ge, ":num_at_least_20", ":num_below_0"),
		(store_add, reg0, ":worst_relation", ":best_relation"),
		(ge, reg0, 0),
		(str_store_troop_name_link, s0, ":bad_relation"),
		(str_store_troop_name_link, s1, ":good_relation"),  #SB : link message
		(display_message, "@{s0} is grumbling against you, but with {s1}'s support you remain affiliated for now."),
		(str_clear, s0),
		(str_clear, s1),
		(assign, ":bad_relation", 0),
	(try_end),
	##nested diplomacy end+
    (try_begin),
      (eq, ":bad_relation", 0),

      (try_for_range, ":family_member", lords_begin, kingdom_ladies_end),
        (call_script, "script_dplmc_is_affiliated_family_member", ":family_member"),
        (gt, reg0, 0),
        (try_begin),
           (troop_slot_ge, ":family_member", slot_troop_prisoner_of_party, 0),
           ##diplomacy start+ skip relationship decay for imprisonment when the player himself is imprisoned or wounded
           (neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 1),
           (neg|troop_is_wounded, "trp_player"),
           ##diplomacy end+
           (call_script, "script_change_player_relation_with_troop", ":family_member", -1),
        (else_try),
          (call_script, "script_change_player_relation_with_troop", ":family_member", 1),
        (try_end),
      (try_end),
    (else_try),
      (call_script, "script_add_notification_menu", "mnu_dplmc_affiliate_end", ":bad_relation", 0),
      (call_script, "script_dplmc_affiliate_end", 1),
    (try_end),
    ##nested diplomacy start+
    (assign, reg0, ":save_reg0"),
    (assign, reg1, ":save_reg1"),
    (assign, reg4, ":save_reg4"),
    ##nested diplomacy end+
    ]),
]
