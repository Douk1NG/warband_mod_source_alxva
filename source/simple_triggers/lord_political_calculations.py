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



	#Individual lord political calculations
	#Check for lords without fiefs, auto-defections, etc
   

lord_political_calculations_simple_triggers = [
(0.5,
    [
	##diplomacy start+
	#This is fairly complicated, and it was getting nearly unreadable so I reformatted it.
	#The old version is visible in version control.
	(assign, ":save_reg0", reg0),
	(val_add, "$g_lord_long_term_count", 1),
	(try_begin),
		(neg|is_between, "$g_lord_long_term_count", active_npcs_including_player_begin, active_npcs_end),
		(assign, "$g_lord_long_term_count", active_npcs_including_player_begin),
	(try_end),

	##Add political calculations for kingdom ladies.  Just extending the range would
	##slow down the political calculations cycle, which would have possibly-unforeseen results.
	##Instead, add a second iteration to deal with extensions.
	(try_for_range, ":iteration", 0, 2),
		(assign, ":troop_no", "$g_lord_long_term_count"),
		(try_begin),
			(eq, ":iteration", 1),
			(val_sub, ":troop_no", active_npcs_including_player_begin),
			(val_add, ":troop_no", active_npcs_end),
		(try_end),
		#Crude check to make sure that a careless modder (i.e. me) didn't decide it
		#would be a good idea to redefine active_npcs to include kingdom_ladies,
		#which would make the second iteration run off the end of the heroes list.
		(is_between, ":troop_no", active_npcs_including_player_begin, heroes_end),

		#Special handling for trp_player, and get the troop's faction
		(try_begin),
			(eq, ":troop_no", "trp_kingdom_heroes_including_player_begin"),
			(assign, ":troop_no", "trp_player"),
			(assign, ":faction", "$players_kingdom"),
		(else_try),
			(store_faction_of_troop, ":faction", ":troop_no"),
		(try_end),

		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_troop_name, s9, ":troop_no"),
			(display_message, "@{!}DEBUG -- Doing political calculations for {s9}"),
		(try_end),

        #Tally the fiefs owned by the hero, and cache the value in slot.
		#If a lord owns no fiefs, his relations with his liege may deteriorate.
        (try_begin),
			(assign, reg0, 1),#Center points + 1
			(try_for_range, ":center", centers_begin, centers_end),
				(party_slot_eq, ":center", slot_town_lord, ":troop_no"),
				(try_begin),
					(is_between, ":center", towns_begin, towns_end),
					(val_add, reg0, 3),#3 points per town
				(else_try),
					(is_between, ":center", walled_centers_begin, walled_centers_end),
					(val_add, reg0, 2),#2 points per castle
				(else_try),
					(val_add, reg0, 1),#1 point per village
				(try_end),
			(try_end),
			#Update cached total
			(troop_set_slot, ":troop_no", dplmc_slot_troop_center_points_plus_one, reg0),
			#If a lord has no fiefs, relation loss potentially results.
			#Do not apply this to the player.
			(eq, reg0, 1),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(neq, ":troop_no", "trp_player"),

			#Don't apply this to the leader
			(faction_get_slot, ":faction_leader", ":faction", slot_faction_leader),
			(gt, ":faction_leader", -1),
			(neq, ":faction_leader", ":troop_no"),
			(neg|troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),
			(neg|troop_slot_eq, ":troop_no", slot_troop_spouse, ":faction_leader"),

			(troop_get_slot, ":troop_reputation", ":troop_no", slot_lord_reputation_type),
			(try_begin),
				(this_or_next|eq, ":troop_reputation", lrep_quarrelsome),
				(this_or_next|eq, ":troop_reputation", lrep_selfrighteous),
				(this_or_next|eq, ":troop_reputation", lrep_cunning),
				(eq, ":troop_reputation", lrep_debauched),
				(call_script, "script_troop_change_relation_with_troop", ":troop_no", ":faction_leader", -4),
				(val_add, "$total_no_fief_changes", -4),
			(else_try),
				(this_or_next|eq, ":troop_reputation", lrep_ambitious),#add support for lady personalities
				(eq, ":troop_reputation", lrep_martial),
				(call_script, "script_troop_change_relation_with_troop", ":troop_no", ":faction_leader", -2),
				(val_add, "$total_no_fief_changes", -2),
			(try_end),
        (try_end),

        #Auto-indictment or defection
        (try_begin),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(eq, ":troop_no", "trp_player"),

			#There must be a valid faction leader.  The faction leader won't defect from his own kingdom.
			#To avoid certain potential complications, also skip the defection/indictment check for the
			#spouse of the faction leader.  (Code to make that possible can be added elsewhere if
			#necessary.)
			(faction_get_slot, ":faction_leader", ":faction", slot_faction_leader),
			(gt, ":faction_leader", -1),
			(neq, ":troop_no", ":faction_leader"),
			(neg|troop_slot_eq, ":troop_no", slot_troop_spouse, ":faction_leader"),
			(neg|troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),

          #I don't know why these are necessary, but they appear to be
			(neg|is_between, ":troop_no", "trp_kingdom_1_lord", "trp_knight_1_1"),
			(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),

		  (assign, ":num_centers", 0),		  
		  (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),		    
		    (store_faction_of_party, ":faction_of_center", ":cur_center"),
			(eq, ":faction_of_center", ":faction"),			
			(val_add, ":num_centers", 1),
		  (try_end),

		  #we are counting num_centers to allow defection although there is high relation between faction leader and troop. 
		  #but this rule should not applied for player's faction and player_supporters_faction so thats why here 1 is added to num_centers in that case.
		  (try_begin), 
		    (this_or_next|eq, ":faction", "$players_kingdom"),
			(eq, ":faction", "fac_player_supporters_faction"),
			(val_add, ":num_centers", 1),
		  (try_end),
			
			(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
          (this_or_next|le, reg0, -50), #was -75
		  (eq, ":num_centers", 0), #if there is no walled centers that faction has defection happens 100%.

			(call_script, "script_cf_troop_can_intrigue", ":troop_no", 0), #Should include battle, prisoner, in a castle with others
      		(store_random_in_range, ":who_moves_first", 0, 2),

			#The more centralized the faction, the greater the chance the liege will indict
			#the lord before he defects.
			(faction_get_slot, reg0, ":faction", dplmc_slot_faction_centralization),
			(val_clamp, reg0, -3, 4),
			(val_add, reg0, 10),#7 minimum, 13 maximum
			(store_random_in_range, ":random", 0, reg0),
			#Random  < 5: The lord defects
			#Random >= 5: The liege indicts the lord for treason

			(try_begin),
	            (this_or_next|eq, ":num_centers", 0), #Thanks Caba`drin & Osviux
	            (neq, ":who_moves_first", 0),
				(lt, ":random", 5),
				(neq, ":troop_no", "trp_player"),
				#do a defection
                        (try_begin), 
                          (neq, ":num_centers", 0), 
						  #Note that I assign the troop number instead of 1 as is done in Native
                          (assign, "$g_give_advantage_to_original_faction", ":troop_no"),
                        (try_end),
			#(assign, "$g_give_advantage_to_original_faction", 1),
        
			(store_faction_of_troop, ":orig_faction", ":troop_no"),
				(call_script, "script_lord_find_alternative_faction", ":troop_no"),
				(assign, ":new_faction", reg0),
				(assign, "$g_give_advantage_to_original_faction", 0),
			(try_begin),
			  (neq, ":new_faction", ":orig_faction"),
				(is_between, ":new_faction", kingdoms_begin, kingdoms_end),
				(call_script, "script_change_troop_faction", ":troop_no", ":new_faction"),
				(str_store_troop_name_link, s1, ":troop_no"),
				(str_store_faction_name_link, s2, ":new_faction"),
				(str_store_faction_name_link, s3, ":faction"),
				(try_begin),
					(ge, "$cheat_mode", 1),
					(str_store_troop_name, s4, ":troop_no"),
					(display_message, "@{!}DEBUG - {s4} faction changed in defection"),
				(try_end),
				(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
				(assign, reg4, reg0),
                #SB : factionalize colors
				(str_store_string, s4, "str_lord_defects_ordinary"),
                (faction_get_color, ":color", ":new_faction"),
				(display_log_message, s4, ":color"),
				(try_begin),
					(eq, "$cheat_mode", 1),
					(this_or_next|eq, ":new_faction", "$players_kingdom"),
					(eq, ":faction", "$players_kingdom"),
					(call_script, "script_add_notification_menu", "mnu_notification_lord_defects", ":troop_no", ":faction"),
				(try_end),
			(try_end),
			(else_try),
				(neq, ":faction_leader", "trp_player"),
                (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
			(le, reg0, -50), #was -75
				(call_script, "script_indict_lord_for_treason", ":troop_no", ":faction"),
			(try_end),

			#Update :faction if it has changed
			(try_begin),
				(eq, ":troop_no", "trp_player"),
				(assign, reg0, "$players_kingdom"),
			(else_try),
				(store_faction_of_troop, reg0, ":troop_no"),
			(try_end),
			(neq, reg0, ":faction"),#Fall through if indictment/defection didn't happen
			(assign, ":faction", reg0),
		(else_try),  #Take a stand on an issue
			(neq, ":troop_no", "trp_player"),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(faction_slot_ge, ":faction", slot_faction_political_issue, 1),
			#This bit of complication is needed for savegame compatibility -- if zero is in the slot, they'll choose anyway
			(neg|troop_slot_ge, ":troop_no", slot_troop_stance_on_faction_issue, 1),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_stance_on_faction_issue, -1),
				(neq, "$players_kingdom", ":faction"),

			(call_script, "script_npc_decision_checklist_take_stand_on_issue", ":troop_no"),
			(troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, reg0),
        (else_try),
			#OPTIONAL CHANGE (AI CHANGES HIGH):
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
			#If an AI kingdom has fiefless lords and no free fiefs, the king
			#will consider giving up a village.  The king will not give up fiefs if
			#doing so would give him less territory than another lord of his faction.
			#(For simplicity, the AI will not do this while a marshall appointment
			#is pending.)
			(faction_slot_eq, ":faction", slot_faction_leader, ":troop_no"),
			(neq, ":troop_no", "trp_player"),
			#With fewer than 3 points we don't need to bother continuing, since 2 points means he only owns a single village.
         (troop_get_slot, ":local_temp", ":troop_no", dplmc_slot_troop_center_points_plus_one),
			(ge, ":local_temp", 3),
			#Don't do this while other business is pending
			(neg|faction_slot_ge, ":faction", slot_faction_political_issue, 1),
			#Find the fiefless lord of his faction that the king likes best.
			#Terminate the search early if he finds another lord whose fiefs
			#equal or exceed his own, or a lord whose fief point slot is not
			#initialized.
			(assign, ":end_cond", heroes_end),
			(assign, ":any_found", -200),
			(assign, ":best_active_npc", -1),
			(try_for_range, ":active_npc", heroes_begin, ":end_cond"),
				(neq, ":active_npc", ":troop_no"),
				(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
				(store_faction_of_troop, reg0, ":active_npc"),
				(eq, reg0, ":faction"),
				(troop_get_slot, reg0, ":active_npc", dplmc_slot_troop_center_points_plus_one),
				(try_begin),
					#Terminate.  The king cannot give up any points without being outfieffed (if he isn't already)
					(ge, reg0, ":local_temp"),
					(assign, ":end_cond", ":active_npc"),
				(else_try),
					#Terminate.  The first pass of political calculations aren't done, or things are in flux.
					(lt, reg0, 1),
					(assign, ":end_cond", ":active_npc"),
				(else_try),
					(eq, reg0, 1),
					(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":active_npc"),
					(gt, reg0, ":any_found"),
					(assign, ":any_found", reg0),
					(assign, ":best_active_npc", ":active_npc"),
				(try_end),
			(try_end),
			(eq, ":end_cond", heroes_end),
			(is_between, ":best_active_npc", heroes_begin, heroes_end),
			(gt, ":any_found", -10),
			#Give up the least prosperous fief.
			(assign, ":local_temp", 101),
			(assign, ":any_found", -1),
			(try_for_range, ":center", villages_begin, villages_end),
				(party_slot_eq, ":center", slot_town_lord, ":troop_no"),
				(party_get_slot, reg0, ":center", slot_town_prosperity),
				(this_or_next|eq, ":any_found", -1),
				(lt, reg0, ":local_temp"),
				(assign, ":local_temp", reg0),
				(assign, ":any_found", ":center"),
			(try_end),
			#Clear village's lord
			(is_between, ":any_found", centers_begin, centers_end),
			(party_set_slot, ":any_found", slot_town_lord, -1),
			(troop_get_slot, reg0, ":troop_no", dplmc_slot_troop_center_points_plus_one),
			(val_sub, reg0, 1),
			(troop_set_slot, ":troop_no", dplmc_slot_troop_center_points_plus_one, reg0),
			(str_store_party_name_link, s4, ":any_found"),
			(str_store_troop_name_link, s5, ":troop_no"),
			(str_store_faction_name_link, s7, ":faction"),
			(display_log_message, "@{s5} has decided to grant {s4} to another lord of the {s7}."),
			#Reset faction issue
			(try_for_range, ":active_npc", heroes_begin, heroes_end),
				(store_faction_of_troop, reg0, ":active_npc"),
				(eq, reg0, ":faction"),
				(troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
			(try_end),
			(store_current_hours, reg0),
			(faction_set_slot, ":faction", slot_faction_political_issue_time, reg0),
			(faction_set_slot, ":faction", slot_faction_political_issue, ":any_found"),
			#Set the liege's position on the issue, since he gave up the village with
			#something specific in mind.
			(troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, ":best_active_npc"),
		(try_end),

		#Reduce grudges over time
		(try_begin),
			#Skip this for the dead
			(neg|troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_dead),
			#Do not perform this for kingdom ladies, since it will potentially mess up courtship.
			(neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),

			(try_for_range, ":active_npc", heroes_begin, heroes_end),
				(neq, ":active_npc", ":troop_no"),
				(neg|troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_lady),#Don't do for ladies
				(neg|troop_slot_eq, ":active_npc", slot_troop_occupation, dplmc_slto_dead),#Don't do for the dead

				#Fix: there are some NPCs that have "initial" relations with the player set,
				#but they can decay before ever meeting him, so keep them until the first meeting.
				(this_or_next|neq, ":troop_no", "trp_player"),
				(troop_slot_ge, ":troop_no", slot_troop_met, 1),

				(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":active_npc"),
				(lt, reg0, 0),
				(store_sub, ":chance_of_convergence", 0, reg0),
				(store_random_in_range, ":random", 0, 300),
				(lt, ":random", ":chance_of_convergence"),
				(call_script, "script_troop_change_relation_with_troop", ":troop_no", ":active_npc", 1),
				(val_add, "$total_relation_changes_through_convergence", 1),
			(try_end),

			#Accelerate forgiveness for lords in exile (with their original faction only)
			(neq, ":troop_no", "trp_player"),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_exile),
			(troop_get_slot, ":original_faction", ":troop_no", slot_troop_original_faction),
			(gt, ":original_faction", 0),

			(try_for_range, ":active_npc", heroes_begin, heroes_end),
				(neq, ":active_npc", ":troop_no"),
				(neg|troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_lady),#Don't do for ladies
				(neg|troop_slot_eq, ":active_npc", slot_troop_occupation, dplmc_slto_dead),#Don't do for the dead
				#Only apply to heroes with the same original faction
				(troop_slot_eq, ":active_npc", slot_troop_original_faction, ":original_faction"),
				(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":active_npc"),
				(lt, reg0, 0),
				(store_sub, ":chance_of_convergence", 0, reg0),
				(store_random_in_range, ":random", 0, 300),
				(lt, ":random", ":chance_of_convergence"),
				(call_script, "script_troop_change_relation_with_troop", ":troop_no", ":active_npc", 1),
				(val_add, "$total_relation_changes_through_convergence", 1),
			(try_end),
		(try_end),
	#Finish loop over the ":iteration" variable.
	(try_end),
	(assign, reg0, ":save_reg0"),
	##diplomacy end+
   ]),
]
