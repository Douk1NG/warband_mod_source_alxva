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

calculate_hero_weekly_net_income_and_add_to_wealth_scripts = [
# script_cf_get_random_lord_from_another_faction_in_a_center
# Input: arg1 = troop_no
# Output: none
("calculate_hero_weekly_net_income_and_add_to_wealth",
    [
      (store_script_param_1, ":troop_no"),

      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),

      (assign, ":weekly_income", 750), #let every hero receive 750 denars by default

      (store_character_level, ":troop_level", ":troop_no"),
      (store_mul, ":level_income", ":troop_level", 10),
      (val_add, ":weekly_income", ":level_income"),

      (store_troop_faction,":faction_no", ":troop_no"),

	  ##diplomacy start+
	  #Bonus for marshall and/or faction leader (is 1000 in native)
	  (assign, ":leader_bonus_gold", 1000),
	  (assign, ":bonus_applied", 0),
	  (try_begin),
		   #OPTIONAL CHANGE (HIGH)
		   (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
 		   #Scale marshall and king bonus gold by number of remaining kingdoms,
           #so the total amount paid out remains the same even as kingdoms disappear.
           #This is only enabled if changes are on "HIGH".
           (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
           (store_sub, ":original_kingdoms", npc_kingdoms_end, npc_kingdoms_begin),#deliberately excludes player kingdom
           (ge, ":original_kingdoms", 2),
           (assign, ":current_kingdoms", 0),
           (try_for_range, ":other_fac", kingdoms_begin, kingdoms_end),#deliberately include player kingdom
             (faction_slot_eq, ":other_fac", slot_faction_state, sfs_active),
             (val_add, ":current_kingdoms", 1),
           (try_end),
           (ge, ":current_kingdoms", 1),
           (lt, ":current_kingdoms", ":original_kingdoms"),
           (val_mul, ":leader_bonus_gold", ":original_kingdoms"),
           (val_div, ":leader_bonus_gold", ":current_kingdoms"),
		   #Examples, assuming 6 starting kingdoms and no player kingdom:
		   #6 kingdoms: 1000 each, 1000 * 6 = 6000 total
		   #5 kingdoms: 1200 each, 1200 * 5 = 6000 total
		   #4 kingdoms: 1500 each, 1500 * 4 = 6000 total
		   #3 kingdoms: 2000 each, 2000 * 3 = 6000 total
		   #2 kingdoms: 3000 each, 3000 * 2 = 6000 total
		   #1 kingdom:  6000 each, 6000 * 1 = 6000 total
      (try_end),
	  ##diplomacy end+

      (try_begin), #check if troop is kingdom leader
        (faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),
        ##diplomacy start+
		#OLD BEHAVIOR:
        #(val_add, ":weekly_income", 1000),
		#NEW BEHAVIOR:
		(val_add, ":weekly_income", ":leader_bonus_gold"),
		(val_add, ":bonus_applied", 1),
        ##diplomacy end+
      (try_end),

      (try_begin), #check if troop is marshall
        (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
        ##diplomacy start+
		#OLD BEHAVIOR:
        #(val_add, ":weekly_income", 1000),
		#NEW BEHAVIOR:
	    (val_add, ":weekly_income", ":leader_bonus_gold"),
		(val_add, ":bonus_applied", 1),
        ##diplomacy end+
      (try_end),

	  ##diplomacy start+
	  (try_begin),
	  	  #OPTIONAL CHANGE (MEDIUM)
		  (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		  #If the lord is the spouse of the faction leader and no better bonus
		  #applied, the lord gets half of the bonus if either (1) there is no
		  #marshall, or (2) the faction leader is the player.
		  (eq, ":bonus_applied", 0),
		  (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
  		  #Don't do the usual polygamy check: the bonus only applies to
		  #one of the spouses.
		  (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
		  (ge, ":faction_leader", 0),
		  (troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),
		  #Don't apply the bonus unless the faction leader bonus is going
		  #all/partially uncollected, or the marshal bonus is going uncollected.
		  (this_or_next|neg|faction_slot_ge, ":faction_no", slot_faction_marshall, 0),
			(eq, ":faction_leader", "trp_player"),
		  #Apply bonus
		  (val_add, ":bonus_applied", 1),
		  (store_div, reg0, ":leader_bonus_gold", 2),
		  (val_add, ":weekly_income", reg0),
	  (try_end),
	  ##diplomacy end+

      (assign, ":cur_weekly_wage", 0),
      (try_begin),
        (gt, ":party_no",0),
        (call_script, "script_calculate_weekly_party_wage", ":party_no"),
        (assign, ":cur_weekly_wage", reg0),
      (try_end),
      ##diplomacy start+
      (try_begin),
	     #take into account leader's leadership skill, like in CC
	     #economics changes must be enabled
         (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
         (store_skill_level, ":leadership_level", "skl_leadership", ":troop_no"),
         (val_clamp, ":leadership_level", 0, 11),
         (store_mul, ":leadership_bonus", 5, ":leadership_level"),
         (store_sub, ":leadership_factor", 100, ":leadership_bonus"),
         (val_mul, ":cur_weekly_wage", ":leadership_factor"),  #wage = wage * (100 - 5*leadership)/100
         (val_div, ":cur_weekly_wage", 100),
      (try_end),

	  #Store the change in income for use below
	  (store_sub, ":net_income", ":weekly_income", ":cur_weekly_wage"),
      ##diplomacy end+
      (val_sub, ":weekly_income", ":cur_weekly_wage"),

      (val_add, ":cur_wealth", ":weekly_income"),

	  (try_begin),
		(lt, ":cur_wealth", 0),
		(store_sub, ":percent_under", 0, ":cur_wealth"),
		(val_mul, ":percent_under", 100),
		(val_div, ":percent_under", ":cur_weekly_wage"),
		(val_div, ":percent_under", 5), #Max 20 percent
		##diplomacy start+
		#The above assumption could be violated if the lord entered this
		#script with a negative wealth.  Add a failsafe.
		(val_clamp, ":percent_under", 0, 21),
		##diplomacy end+
		(call_script, "script_party_inflict_attrition", ":party_no", ":percent_under", 1),
	  (try_end),

	  ##diplomacy start+
	  #Apply gold change
	  (try_begin),
	     #If the wealth change was positive, some of it may go to the lord's holdings.
	     (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
	     (ge, ":net_income", 1),
		 (call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":net_income", ":troop_no"),
	  (else_try),
	     #Fall through to old version:
		 #OLD VERSION:
         (val_max, ":cur_wealth", 0),
         (troop_set_slot, ":troop_no", slot_troop_wealth, ":cur_wealth"),
	  (try_end),
	  ##diplomacy end+
  ])
]
