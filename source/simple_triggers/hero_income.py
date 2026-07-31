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



  #Adding net incomes to heroes (once a week)
  #Increasing debts to heroes by 1% (once a week)
  #Adding net incomes to centers (once a week)
  

hero_income_simple_triggers = [
(24*7,
   [
		##diplomacy start+ Save register
		(assign, ":save_reg0", reg0),
		##Change to support kingdom ladies
       #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
	   (try_for_range, ":troop_no", heroes_begin, heroes_end),
	     (this_or_next|is_between, ":troop_no", active_npcs_begin, active_npcs_end),
		 (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	   ##diplomacy end+
         (troop_get_slot, ":cur_debt", ":troop_no", slot_troop_player_debt),#Increasing debt
         
         (try_begin), #dckplmc - lose relation for unpaid debts
            (gt, ":cur_debt", 0),
            (call_script, "script_troop_change_relation_with_troop", "trp_player", ":troop_no", -3),
            (str_store_troop_name, s15, ":troop_no"),
            (assign, reg1, ":cur_debt"),
            (display_message, "@You have an outstanding debt of {reg1} denars with {s15}"),
         (try_end),
         
         (lt, ":cur_debt", dplmc_ransom_debt_mask), #qst_rescue_prisoner does not accumulate
         #SB : aristocracy/plutocracy debt modifier
         (store_faction_of_troop, ":faction_no", ":troop_no"),
         (faction_get_slot, ":aristocracy", ":faction_no", dplmc_slot_faction_aristocracy),
         (val_add, ":aristocracy", 205), #1.01x to 1.04x
         (val_mul, ":cur_debt", ":aristocracy"),
         (val_div, ":cur_debt", 200),
         (troop_set_slot, ":troop_no", slot_troop_player_debt, ":cur_debt"),
         (call_script, "script_calculate_hero_weekly_net_income_and_add_to_wealth", ":troop_no"),#Adding net income
       (try_end),

	   ##diplomacy start+
	   (store_current_hours, ":two_weeks_ago"),
	   (val_sub, ":two_weeks_ago", 24 * 14),
	   ##diplomacy end+

       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         #If non-player center, adding income to wealth
         (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"), #center does not belong to player.
		 ##diplomacy start+
		 #Defer the ownership check so attrition can still occur for unowned centers.
		 #Give a slight grace period first, though.
		 (neg|party_slot_eq, ":center_no", slot_town_lord, 0),
		 (this_or_next|party_slot_ge, ":center_no", dplmc_slot_center_last_transfer_time, ":two_weeks_ago"),
			(party_slot_ge, ":center_no", slot_town_lord, 1), #center belongs to someone.
		 (this_or_next|ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		 ##diplomacy end+
		 (party_slot_ge, ":center_no", slot_town_lord, 1), #center belongs to someone.
         (party_get_slot, ":cur_wealth", ":center_no", slot_town_wealth),
         (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
         (store_mul, ":added_wealth", ":prosperity", 15),
         (val_add, ":added_wealth", 700),
         (try_begin),
           (party_slot_eq, ":center_no", slot_party_type, spt_town),
           (val_mul, ":added_wealth", 3),
           (val_div, ":added_wealth", 2),
         (try_end),
         (val_add, ":cur_wealth", ":added_wealth"),
         (call_script, "script_calculate_weekly_party_wage", ":center_no"),
         (val_sub, ":cur_wealth", reg0),
		 ##diplomacy start+ Allow attrition to occur
		 (try_begin),
			(lt, ":cur_wealth", 0),
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
			(assign, ":cur_weekly_wage", reg0),
			(store_party_size_wo_prisoners, ":garrison_size", ":center_no"),
			(call_script, "script_party_get_ideal_size", ":center_no"),#This script has been modified to support this use
			(val_mul, reg0, 5),
			(val_div, reg0, 4),
			(ge, ":garrison_size", reg0),

			(store_sub, ":percent_under", 0, ":cur_wealth"),
			(val_mul, ":percent_under", 100),
			(val_div, ":percent_under", ":cur_weekly_wage"),
			(val_div, ":percent_under", 5), #Max 20 percent (won't take garrison below ideal size)
			(call_script, "script_party_inflict_attrition", ":center_no", ":percent_under", 1),
		 (try_end),
		 (party_slot_ge, ":center_no", slot_town_lord, 1), #center belongs to someone.
		 ##diplomacy end+
         (val_max, ":cur_wealth", 0),
         (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
       (try_end),
	   ##diplomacy end+
	   (assign, reg0, ":save_reg0"),
	   ##diplomacy end+
    ]),
]
