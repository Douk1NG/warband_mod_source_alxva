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

dplmc_get_truce_pay_amount_scripts = [
# Input: arg1 = faction_no_1, arg2 = faction_no_2
("dplmc_get_truce_pay_amount",
   [
       (store_script_param, ":faction_no_1", 1),
       (store_script_param, ":faction_no_2", 2),
       (store_script_param, ":check_peace_war_result", 3),
	   ##diplomacy start+
	   #Since "fac_player_supporters_faction" is used as a shorthand for the faction
	   #run by the player, intercept that here instead of the various places this is
	   #called from.
	   (call_script, "script_dplmc_translate_inactive_player_supporter_faction_2", ":faction_no_1", ":faction_no_2"),
	   (assign, ":faction_no_1", reg0),
	   (assign, ":faction_no_2", reg1),
	   ##diplomacy end+

       (try_begin),
         (eq, "$cheat_mode", 1),
         (assign, reg0, ":check_peace_war_result"), #debug
         (display_message, "@{!}DEBUG : peace_war_result: {reg0}"),#debug
       (try_end),

       ##nested diplomacy start+
       #Improve this script; costs were too low befow.
       #faction_no_1 is player faction asking for peace
       #faction_no_2 is NPC faction that already considered peace and considers
       #      it a bad idea, so the price should not be nominal.

       #(Also, a sign error meant that the amount asked was almost always
       #zero.)

       #Because the PC wants peace and the NPC doesn't, we aren't going to
       #bother calculating relative strength or the like.  Instead, we are
       #going to assume the NPC can achieve his strategic objectives if he
       #does not make peace, and set the price accordingly.

       #Add a generic cost for check_peace_war_result
       #These are the same as in Wahiti's original script.
       (assign, ":base_cost",  4000),
       (try_begin),
          #It's dubious that this is ever currently called if the check-peace-war
          #result was >= 0, but include this for completeness.
          (ge, ":check_peace_war_result", 0),
          (assign, ":base_cost", 4000),
       (else_try),
          (ge, ":check_peace_war_result", -1),
          (assign, ":base_cost", 8000),
       (else_try),
          (ge, ":check_peace_war_result", -2),
          (assign, ":base_cost", 12000),
       (else_try),
          #It shouldn't be used with this parameter; this is for the
          #sake of completeness.
          (le, ":check_peace_war_result", -3),
          (store_mul, ":base_cost", -6000, ":check_peace_war_result"),
       (try_end),

       #Get reparations for held centers.  A truce lasts 20 days, so the
       #value "lost" in rents and tarriffs by declaring peace now cannot be
       #is not greater than 3 times the weekly average (that upper bound is
       #if the NPC is in a position to immediately recapture all of them).

       #If the NPC kingdom is currently attacking a specific village or walled
       #center, even if it isn't an ex-possession it effectively becomes one.
       #(Also, assign it or its center as a demanded fief if there wasn't one
       #already.)
       (assign, ":target_fief", -1),
       (try_begin),
          (lt, ":check_peace_war_result", 1),#This should always be true anyway, but still.
          (this_or_next|faction_slot_eq, ":faction_no_2", slot_faction_ai_state, sfai_attacking_center),
          (faction_slot_eq, ":faction_no_2", slot_faction_ai_state, sfai_raiding_village),
          (faction_get_slot, reg0, ":faction_no_2", slot_faction_ai_object),
          (is_between, reg0, centers_begin, centers_end),
          (assign, ":target_fief", reg0),
       (try_end),

       (assign, ":center_cost", 0),
       (assign, ":concession_value", 0),
       #This this old are newer are considered "recently conquered", meaning that
       #faction_no_2 thinks there's a good chance they could reclaim them if the
       #fighting continued.
       (store_current_hours, ":recently_conquered"),
       (try_begin),
          (ge, ":check_peace_war_result", 1),#ordinarily this should not be true
          (val_sub, ":recently_conquered", 24 * 2),#only the last two days
       (else_try),
          (eq, ":check_peace_war_result", 0),
          (val_sub, ":recently_conquered", 24 * 15),#last 15 days
       (else_try),
          (eq, ":check_peace_war_result", -1),
          (val_sub, ":recently_conquered", 24 * 20),#last 20 days
       (else_try),
          (eq, ":check_peace_war_result", -2),
          (val_sub, ":recently_conquered", 24 * 30),#last 30 days
       (else_try),
          (val_sub, ":recently_conquered", 24 * 60),#last 60 days
       (try_end),

       (try_for_range, ":party_no", centers_begin, centers_end),
          (store_faction_of_party, ":party_current_faction", ":party_no"),
          (eq, ":party_current_faction", ":faction_no_1"),

          #party_value is the estimated weekly income of the fief,
          #applied three times and time discounted
          (call_script, "script_dplmc_estimate_center_weekly_income", ":party_no"),
          (store_mul, ":party_value", reg0, 3),

          (try_begin),
             (ge, "$g_concession_demanded", spawn_points_begin),
             (this_or_next|eq, "$g_concession_demanded", ":party_no"),
             (party_slot_eq, ":party_no", slot_village_bound_center, "$g_concession_demanded"),
             (val_add, ":concession_value", ":party_value"),
          (try_end),

          (assign, ":continue", 0),

          (try_begin),
             #A former possession of faction 2 (must have recently changed hands, or
             #faction 2 must be enthusiastic about the war)
             (party_slot_eq, ":party_no", slot_center_original_faction, ":faction_no_2"),
             (party_slot_ge, ":party_no", dplmc_slot_center_last_transfer_time, ":recently_conquered"),
             (assign, ":continue", 1),
          (else_try),
             #A former possession of faction 2 (must have recently changed hands, or
             #faction 2 must be enthusiastic about the war)
             (party_slot_eq, ":party_no", slot_center_ex_faction, ":faction_no_2"),
             (party_slot_ge, ":party_no", dplmc_slot_center_last_transfer_time, ":recently_conquered"),
             (assign, ":continue", 1),
          (else_try),
             #The center is being attacked by faction 2, or is a village whose castle
             #or town is being attacked by faction 2.
             (ge, ":target_fief", centers_begin),
             (this_or_next|eq, ":party_no", ":target_fief"),
             (party_slot_eq, ":party_no", slot_village_bound_center, ":target_fief"),
             (assign, ":continue", 1),
          (else_try),
             #The center is under siege by faction 2.
             (party_get_slot, reg0, ":party_no", slot_center_is_besieged_by),
             (gt, reg0, 0),
             (party_is_active, reg0),
             (store_faction_of_party, reg0, reg0),
             (eq, reg0, ":faction_no_2"),
             (assign, ":continue", 1),
          (else_try),
             #The center is a village, and the castle or town it is bound to
             #is under siege by faction 2.
             (is_between, ":party_no", villages_begin, villages_end),
             (party_get_slot, reg0, ":party_no", slot_village_bound_center),
             (is_between, reg0, centers_begin, centers_end),
             (party_get_slot, reg0, reg0, slot_center_is_besieged_by),
             (gt, reg0, -1),
             (party_is_active, reg0),
             (store_faction_of_party, reg0, reg0),
             (eq, reg0, ":faction_no_2"),
             (assign, ":continue", 1),
          (try_end),

          (gt, ":continue", 0),

          (val_add, ":center_cost", ":party_value"),
       (try_end),

       #If no held centers were found, assume the campaign objective is to
       #conquer territory rather than recover lost territory, if the
       #NPC is sufficiently enthusiastic about the war.
       (try_begin),
          #Equivalent of a castle and a village
          (eq, ":check_peace_war_result", -1),
          (val_max, ":center_cost", (1500 + 750) * 3),
       (else_try),
          #Equivalent of two castles with two villages
          (le, ":check_peace_war_result", -2),
          (val_max, ":center_cost", (1500 + 750) * 3 * 2),
       (try_end),

	   #If the war started very recently, or a center changed hands very recently,
	   #increase the cost.  The reasoning behind this is to make the AI less prone
	   #to whipsawing.
	   #
	   #The multiplier is 2x for the first 48 hours, then decreases linearly from
       #the two-day mark until it reaches zero at the 8-day mark.
	   #
	   #As an example, here is how a cost of 10,000 would scale over this time:
	   # 1 day  - 20000
	   # 2 days - 20000
	   # 3 days - 18333
	   # 4 days - 16667
	   # 5 days - 15000
	   # 6 days - 13333
	   # 7 days - 11667
	   # 8 days - 10000
	   # 9 days - 10000
	   (store_current_hours, ":cur_hours"),
       (faction_get_slot, ":faction_ai_last_decisive_event", ":faction_no_2", slot_faction_ai_last_decisive_event),
       (store_sub, ":hours_since_last_decisive_event", ":cur_hours", ":faction_ai_last_decisive_event"),
	   (val_max, ":hours_since_last_decisive_event", 0),
	   (try_begin),
	      #First 48 hours, the base & center costs are doubled.
	      (lt, ":hours_since_last_decisive_event", 48 + 1),
		  (val_mul, ":base_cost", 2),
		  (val_mul, ":center_cost", 2),
	   (else_try),
	      #From 2 days to 8 days, the cost multiplier goes from 2 to 1
		  (lt, ":hours_since_last_decisive_event", 24 * 8),
		  (store_sub, reg0, 24 * 2, ":hours_since_last_decisive_event"),#0 to 6 days
		  (store_sub, ":multiplier", 24 * 12, reg0),# 6 to 12 days

		  (val_mul, ":base_cost", ":multiplier"),
		  (val_add, ":base_cost", (24 * 6) // 2),
		  (val_div, ":base_cost", 24 * 6),

		  (val_mul, ":center_cost", ":multiplier"),
		  (val_add, ":center_cost", (24 * 6) // 2),
		  (val_div, ":center_cost", 24 * 6),
	   (try_end),

       #Get (value of ransoms held by faction #1) - (value of ransoms held by faction #2)
       (call_script, "script_dplmc_get_prisoners_value_between_factions", ":faction_no_1", ":faction_no_2"),

       (try_begin),
         (eq, "$cheat_mode", 1),
         (display_message, "@{!}DEBUG : prisoner_value: {reg0}"),#debug
       (try_end),
       (assign, ":prisoner_value", reg0),

       #Write result to reg0
       (store_add, reg0, ":base_cost", ":center_cost"),

	   #Scale for the player's wealth, to partially mitigate the problem
	   #of the cost becoming meaningless as the player's wealth increases.
	   #(Scale less than 1-to-1, so it is possible to become richer in real
	   #terms.)  This is also aimed at reducing the necessity of replacing
	   #the values in mods that alter gold scarcity.
	   (store_troop_gold, ":player_gold", "trp_household_possessions"),
	   (store_troop_gold, reg1, "trp_player"),
	   (val_add, ":player_gold", reg1),
	   (try_begin),
		  #Arbitrarily pick 100,000 as the target wealth, since that's when
		  #you get the Steam "gold farmer" achievement.
	      (gt, ":player_gold", 100000),
		  (store_div, reg1, ":player_gold", 1000),
		  (val_mul, reg1, reg0),
		  (val_div, reg1, 100),

		  (val_add, reg0, reg1),
		  (val_div, reg0, 2),

		  #Apply the same scaling to the concession value
		  (store_div, reg1, ":player_gold", 1000),
		  (val_mul, reg1, ":concession_value"),
		  (val_div, reg1, 100),

		  (val_add, ":concession_value", reg1),
		  (val_div, ":concession_value", 2),
	   (try_end),

       #Take into account campaign difficulty
	   (assign, ":min_cost", reg0),
       (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
       (try_begin),
           (eq, ":reduce_campaign_ai", 0), #hard (1.5x)
           (val_mul, reg0, 3),
           (val_div, reg0, 2),
		   (val_mul, ":min_cost", 87),#set min_cost to 87% of the original base_cost + center_cost
		   (val_div, ":min_cost", 100),
       (else_try),
           (eq, ":reduce_campaign_ai", 1), #moderate (1.0x)
		   (val_mul, ":min_cost", 3),
		   (val_div, ":min_cost", 4),#set min_cost to 75% (base cost + center cost)
       (else_try),
            (eq, ":reduce_campaign_ai", 2), #easy (0.75x)
            (val_mul, reg0, 3),
			(val_div, reg0, 4),
			(val_mul, ":min_cost", 9),
			(val_div, ":min_cost", 16),#set min_cost to (75% squared) of (base cost + center cost)
       (try_end),

       (val_sub, reg0, ":prisoner_value"),

       #Because the NPC kingdom doesn't want peace, it will not agree to peace
       #for free, as that would be a contradiction.
       (val_max, reg0, ":min_cost"),

       (try_begin),
         (eq, "$cheat_mode", 1),
         (display_message, "@{!}DEBUG : peace_war_result after prisoners: {reg0}"),#debug
       (try_end),

       #The value of the concession (if any) was already calculated above
       (assign, reg1, -1),
       (try_begin),
          (gt, "$g_concession_demanded", 0),
       	  (gt, ":concession_value", 0),
          (store_sub, reg1, reg0, ":concession_value"),
          (val_max, reg1, 0),
          #Only accept cash alone in lieu of a fief if you don't partcularly
          #want war, or if the AI is on "easy".
          (try_begin),
             (neq, ":reduce_campaign_ai", 2),#hard or medium
             (lt, ":check_peace_war_result", 0),
             (assign, reg0, -1),
          (try_end),
       (try_end),

     (try_begin), #debug
       (eq, "$cheat_mode", 1),
	     (display_message, "@{!}DEBUG : truce_pay_amount0: {reg0}"),
	     (display_message, "@{!}DEBUG : truce_pay_amount1: {reg1}"),
     (try_end),
     ##nested diplomacy end+
    ])
]
