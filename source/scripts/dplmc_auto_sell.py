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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_auto_sell_scripts = [
# script_dplmc_calculate_troop_score_for_center_aux
#auto sell credit rubik (CC) begin:
#
# script_dplmc_auto_sell
# INPUTS:
#    arg1 :customer (the one selling the stuff)
#    arg2 :merchant (the one buying the stuff)
#    arg3 :auto_sell_price_limit (only sell stuff less expensive than this)
#    arg4 :valid_items_begin (use this to only sell a limited range of things)
#    arg5 :valid_items_end   (use this to only sell a limited range of things)
#    arg6 :actually_sell_items (set to 0 for a "dry run"; set to 2 to print a descriptive message;
#          set to 4 for center autosell cleanup that skips backup-equipment protection)
#
# OUTPUTS:
#    reg0 amount of gold gained by customer (not actually gained if this was a dry run)
#    reg1 number of items sold by customer (not actually sold if this was a dry run)
("dplmc_auto_sell", [
	#This script has various changes from the CC version.
	#In particular, all parameters other than "customer" and "merchant",
	#and reporting the number of items & gold change.
	(store_script_param, ":customer", 1),
	(store_script_param, ":merchant", 2),
	#dplmc+ start added parameters
	(store_script_param, ":auto_sell_price_limit", 3),
	(store_script_param, ":valid_items_begin", 4),
	(store_script_param, ":valid_items_end", 5),
	(store_script_param, ":actually_sell_items", 6),
	#dplmc+ end added parameters

	#dplmc+ added section begin
	(assign, ":save_reg2", reg2),
	(assign, ":save_reg3", reg3),
	(assign, ":save_reg65", reg65),
	(assign, ":save_talk_troop", "$g_talk_troop"),
	#The talk troop is used for price information, but it's possible for this to be called
	#from other contexts (like a menu).
	(assign, "$g_talk_troop", ":merchant"),

	(assign, ":gold_gained", 0),
	(assign, ":items_sold", 0),
	#(assign, ":most_expensive_sold_item", -1),
	#(assign, ":most_expensive_sold_imod", -1),
	#(assign, ":most_expensive_sold_price", -1),
	#dplmc+ added section end

    (troop_get_inventory_capacity, ":inv_cap", ":customer"),
    (assign, ":first_sell_slot", dplmc_ek_alt_items_end),
    (try_begin),
      (eq, ":actually_sell_items", 4),
      (assign, ":first_sell_slot", dplmc_ek_alt_items_begin),
    (try_end),
	(set_show_messages, 0),#<-dplmc+ added
    (try_for_range_backwards, ":i_slot", ":first_sell_slot", ":inv_cap"),#conservative autosell reserves several "safe" slots in the beginning of the inventory
      (troop_get_inventory_slot, ":item", ":customer", ":i_slot"),
      (troop_get_inventory_slot_modifier, ":imod", ":customer", ":i_slot"),
      (gt, ":item", -1),
      (item_get_type, ":type", ":item"),
      (item_slot_eq, ":type", dplmc_slot_item_type_not_for_sell, 0),
	  #dplmc+ begin added constraints
	  (is_between, ":item", ":valid_items_begin", ":valid_items_end"),
	  (neg|is_between, ":type", books_begin, books_end),
	  (this_or_next|neg|is_between, ":item", food_begin, food_end),
	     (eq, ":imod", imod_rotten),
	  (neg|is_between, ":item", trade_goods_begin, trade_goods_end),
	  (neq, ":imod", imod_lordly),#dplmc+: never sell "lordly" items
	  #dplmc+ end added constraints

      (call_script, "script_dplmc_get_item_value_with_imod", ":item", ":imod"),
      (assign, ":score", reg0),
      (val_div, ":score", 100),
      (call_script, "script_game_get_item_sell_price_factor", ":item"),
      (assign, ":sell_price_factor", reg0),
      (val_mul, ":score", ":sell_price_factor"),
      (val_div, ":score", 100),
      (val_max, ":score",1),

	  #dplmc+ start changed section
	  (le, ":score", ":auto_sell_price_limit"),

	  #For equipment, in general don't sell the item unless you have a better one,
	  #or the item is useless to you.  (The idea is to stop from accidentally
	  #selling the player's own equipment.)
	  (item_get_type, ":this_item_type", ":item"),

	  #Normally, we would do the following:

	  #(try_begin),
	  #   (item_slot_eq, ":item", dplmc_slot_two_handed_one_handed, 1),
	  #	 (assign, ":this_item_type", 11), # type 11 = two-handed/one-handed
	  #(try_end),

	  #However, we are delaying that step until later, because type 11 is the
	  #same as itp_type_goods.


	  #Don't sell items if there's a reasonable chance that they might
	  #be the player's alternate personal equipment.  It goes without saying
	  #that items the player can't use aren't counted.
	  #
	  #(Items the player has equipped will not even be considered for sale,
	  #but it is common for players to have a variety of items they use in
	  #different circumstances, which might not all be equipped.)
	  #
	  #For melee weapons: don't sell the best weapon or the second-best of a type
	  #   (it might be a backup, or there might be a variety of weapons of
	  #   the same type in situational use)
	  #For shields: don't sell the best or second-best shield
	  #For thrown weapons: don't sell the best three thrown weapons
	  #For ammunition: don't sell the best three of the ammunition kind (arrows,
	  #   bolts) unless you lack a weapon that uses the ammunition.
	  #For armor: don't sell the best armor of a kind.
	  #For horses: don't sell the best or second-best horse
	  #For bows and crossbows: don't sell the best item of a kind (all bows are
	  #   very similar, so there's little chance someone would carry an alternate)
	  #For muskets and pistols: don't sell the best or second-best weapon of
	  #   a kind.

	  (assign, ":can_sell", 1),

	  (try_begin),
		 (eq, ":actually_sell_items", 4),
	  (else_try),
		 #Damaged or low-quality inventory items should not be preserved as backup gear.
	     (this_or_next|eq, ":imod", imod_cracked),
	     (this_or_next|eq, ":imod", imod_rusty),
	     (this_or_next|eq, ":imod", imod_bent),
	     (this_or_next|eq, ":imod", imod_chipped),
	     (this_or_next|eq, ":imod", imod_battered),
	     (this_or_next|eq, ":imod", imod_poor),
	     (this_or_next|eq, ":imod", imod_crude),
	     (this_or_next|eq, ":imod", imod_old),
	     (eq, ":imod", imod_cheap),
	  (else_try),
		 #Ammunition type: arrows (if you have a bow you can use, don't sell the best 3 arrow packs you have)
	     (eq, ":this_item_type", itp_type_arrows),
		 (call_script, "script_dplmc_scan_for_best_item_of_type", ":customer", itp_type_bow, ":customer"),
		 (try_begin),
			(ge, reg0, 0),
			(call_script, "script_dplmc_count_better_items_of_same_type", ":customer", ":item", ":imod", ":customer"),
			(lt, reg0, 3),#must not be best (0), second-best (1), or third-best (2)
			(assign, ":can_sell", 0),
		 (try_end),
	  (else_try),
		#Ammunition type: bolts (if you have a crossbow you can use, don't sell the best 3 bolt packs you have)
	     (eq, ":this_item_type", itp_type_bolts),
		 (call_script, "script_dplmc_scan_for_best_item_of_type", ":customer", itp_type_crossbow, ":customer"),
		 (try_begin),
			(ge, reg0, 0),
			(call_script, "script_dplmc_count_better_items_of_same_type", ":customer", ":item", ":imod", ":customer"),
			(lt, reg0, 3),#must not be best (0), second-best (1), or third-best (2)
			(assign, ":can_sell", 0),
		 (try_end),
	  (else_try),
		#Ammunition type: bullets (if you have a pistol or musket you can use, don't sell the best 3 bullet packs you have)
	     (eq, ":this_item_type", itp_type_bullets),
		 #Do muskets and pistols both use bullets?  I'll assume so.
		 (call_script, "script_dplmc_scan_for_best_item_of_type", ":customer", itp_type_musket, ":customer"),
		 (assign, reg1, reg0),
		 (call_script, "script_dplmc_scan_for_best_item_of_type", ":customer", itp_type_pistol, ":customer"),
		 (try_begin),
			(this_or_next|ge, reg0, 0),
				(ge, reg1, 0),
			(call_script, "script_dplmc_count_better_items_of_same_type", ":customer", ":item", ":imod", ":customer"),
			(lt, reg0, 3),
			(assign, ":can_sell", 0),
		 (try_end),
	  (else_try),
		#Catch: all non-usable equipment
		(is_between, ":this_item_type", itp_type_horse, itp_type_musket + 1),
		(neq, ":this_item_type", itp_type_goods),
		(call_script, "script_dplmc_troop_can_use_item", ":customer", ":item", ":imod"),
		(eq, reg0, 0),#Past here, we don't have to check for usability
	  (else_try),
		#Thrown weapons: don't sell best 3 you can use
		(eq, ":this_item_type", itp_type_thrown),
		(call_script, "script_dplmc_count_better_items_of_same_type", ":customer", ":item", ":imod", ":customer"),
		(store_sub, ":can_sell", reg0, 2),#must not be best (0) or second-best (1) or third-best (2)
	  (else_try),
		#Types where both the best and the second-best aren't sold
		#Horses, shields, melee weapons, and firearms
		(this_or_next|is_between, ":this_item_type", itp_type_horse, itp_type_polearm + 1),
		(this_or_next|eq, ":this_item_type", itp_type_shield),
		(this_or_next|eq, ":this_item_type", itp_type_pistol),
			(eq, ":this_item_type", itp_type_musket),
		(call_script, "script_dplmc_count_better_items_of_same_type", ":customer", ":item", ":imod", ":customer"),
		(store_sub, ":can_sell", reg0, 1),#must not be best (0) or second best (1)
 	  (else_try),
		#Types where the best isn't sold (armor, not including shields)
		(is_between, ":this_item_type", itp_type_head_armor, itp_type_hand_armor + 1),
		(call_script, "script_dplmc_count_better_items_of_same_type", ":customer", ":item", ":imod", ":customer"),
		(assign, ":can_sell", reg0),#must not be best (0)
	  (try_end),

	  #(try_begin),
	  #   (lt, ":can_sell", 1),
	  #	 (gt, "$cheat_mode", 0),
	  #	 (call_script, "script_dplmc_count_better_items_of_same_type", ":customer", ":item", ":imod", ":customer"),
 	  #	 (assign, reg1, ":i_slot"),
	  #	 (str_store_item_name, s0, ":item"),
	  #	 (display_message, "@{!} DEBUG - Will not sell item {s0} at slot {reg1}.  Better items of same kind: {reg0}"),
	  #(try_end),

	  (ge, ":can_sell", 1),

	  #(try_begin),
	  #	(ge, ":score", ":most_expensive_sold_price"),
	  #	(assign, ":most_expensive_sold_item", ":item"),
	  #	(assign, ":most_expensive_sold_imod", ":imod"),
	  #	(assign, ":most_expensive_sold_price", ":score"),
	  #(try_end),

	  #Log the transaction even if in dry run mode
	  (val_add, ":gold_gained", ":score"),
	  (val_add, ":items_sold", 1),

	  #If not a dry run, apply the transaction
	  (neq, ":actually_sell_items", 0),
	  (troop_set_inventory_slot, ":customer", ":i_slot", -1),
	  (troop_add_gold, ":customer", ":score"),
      #dplmc+ end changed section
    (try_end),

	(set_show_messages, 1),#<- dplmc+ added

	#dplmc+ added section begin
	#Print a message if appropriate
	(try_begin),
		(is_between, ":actually_sell_items", 2, 5),#2, 3, or 4
		(this_or_next|ge, ":items_sold", 1),
			(eq, ":actually_sell_items", 3),
		(assign, reg0, ":gold_gained"),
		(assign, reg1, ":items_sold"),
		(store_sub, reg3, reg1, 1),
		(str_store_troop_name, s0, ":merchant"),
		(try_begin),
			(this_or_next|is_between, ":merchant", quick_battle_troops_begin, quick_battle_troops_end),
			(this_or_next|is_between, ":merchant", heroes_begin, heroes_end),
			(this_or_next|is_between, ":merchant", dplmc_employees_begin, dplmc_employees_end),
			(is_between, ":merchant", walkers_end, tournament_champions_end),
			(display_message, "@You sold {reg1} {reg3?items:item} to {s0} and gained {reg0} {reg3?denars:denar}."),
		(else_try),
			(display_message, "@You sold {reg1} {reg3?items:item} to the {s0} and gained {reg0} {reg3?denars:denar}."),
		(try_end),
	(try_end),

	#Revert variables
	(assign, reg2, ":save_reg2"),
	(assign, reg3, ":save_reg3"),
	(assign, reg65, ":save_reg65"),
	(assign, "$g_talk_troop", ":save_talk_troop"),

	#Return diagnostics
	(assign, reg0, ":gold_gained"),
	(assign, reg1, ":items_sold"),
	#dplmc+ added section end
  ])
]
