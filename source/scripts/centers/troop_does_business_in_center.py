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

troop_does_business_in_center_scripts = [
# script_process_sieges
#It is used for lord to (1)Court ladies (2)Collect rents (3)Look for volunteers
## Upgrade equipment (by quality) and hire mercenaries (if Martial personality)
("troop_does_business_in_center",
  [
    (store_script_param, ":troop_no", 1),
    (store_script_param, ":center_no", 2),
	##diplomacy start+
	#Call this once and reuse below.
	(call_script, "script_dplmc_is_affiliated_family_member", ":troop_no"),
	(assign, ":is_affiliated", reg0),
	#Also enable for the spouse, unless you're on bad terms
	(try_begin),
		(lt, ":is_affiliated", 0),
		(this_or_next|troop_slot_eq,":troop_no",slot_troop_spouse, "trp_player"),
			(troop_slot_eq,"trp_player",slot_troop_spouse, ":troop_no"),
		(call_script, "script_troop_get_player_relation", ":troop_no"),
		(store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
		(val_add, reg0, ":persuasion"),
		#reduce magnitude, since >= 0 succeeds
		(store_sub, ":persuasion_modifier", 20, ":persuasion"),
		(val_mul, reg0, ":persuasion_modifier"),
		(val_div, reg0, 20),
		#final number must be >= -5
		(ge, reg0, -5),
		(assign, ":is_affiliated", 1),
	(try_end),
	##diplomacy end+

    (troop_get_slot, ":led_party", ":troop_no", slot_troop_leaded_party),
    (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth), #SB : moved up
    (assign, ":initial_wealth", ":troop_wealth"), #DEBUG

    (store_current_hours, ":current_time"),
    (try_begin),
#      (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"), #this was added to get lords in centers out and visiting their fiefs, but I've adjusted the decision checklist
      (is_between, ":center_no", walled_centers_begin, walled_centers_end),
      (party_set_slot, ":led_party", slot_party_last_in_any_center, ":current_time"),
      (try_begin),
        (call_script, "script_lord_get_home_center", ":troop_no"),
        (eq, ":center_no", reg0),
        (party_set_slot, ":led_party", slot_party_last_in_home_center, ":current_time"),
      (try_end),
    (try_end),

    #Collect the rents
    (try_begin),
      (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),

      (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
      (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
      # (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth),
      (val_add, ":troop_wealth", ":accumulated_rents"),
      (val_add, ":troop_wealth", ":accumulated_tariffs"),

      (troop_set_slot, ":troop_no", slot_troop_wealth, ":troop_wealth"),
      (party_set_slot, ":center_no", slot_center_accumulated_rents, 0),
      (party_set_slot, ":center_no", slot_center_accumulated_tariffs, 0),

      ## upgrade owned centers

      (call_script, "script_calculate_improvement_limit", ":troop_no", ":center_no"),
      (assign, ":limit", reg0),

      (try_begin),
        (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
        (gt, ":troop_wealth", ":limit"), #surplus cash
        (party_slot_eq, ":center_no", slot_center_current_improvement, 0), #not already building
        (assign, ":continue", 1),
        #this randomization applies so that there is a chance of not building an improvement (1/6) or (4/6)
        (store_random_in_range, ":improvement_no", village_improvements_begin, walled_center_improvements_end),
        (party_slot_eq, ":center_no", ":improvement_no", 0), #not already built
        (try_begin), #villages
          (party_slot_eq, ":center_no", slot_party_type, spt_village),
          (ge, ":improvement_no", village_improvements_end),
          (assign, ":continue", 0),
        (else_try), #towns, castles
          (lt, ":improvement_no", walled_center_improvements_begin),
          (assign, ":continue", 0),
        (try_end),
        (eq, ":continue", 1),
        (call_script, "script_get_improvement_details", ":improvement_no"),
        (assign, ":improvement_cost", reg0), # 4000-9000
        # calculate cost offset from lord
        (store_attribute_level, ":int", ":troop_no", ca_intelligence), #10-70
        (store_skill_level, ":skill", "skl_engineer", ":troop_no"), #0 to 15
        (val_mul, ":skill", ":int"), # 0 to 105
        (store_character_level, ":level", ":troop_no"), #22-50
        (val_add, ":skill", ":level"),
        (val_sub, ":improvement_cost", ":skill"),

        #get working strength
        (party_get_num_companions, ":divider", ":center_no"), #0~300, ignoring wounded
        (party_get_num_prisoners, ":num_prisoners", ":center_no"), #possibly up to 100
        (val_min, ":num_prisoners", 100),

        #account for serfs, each level past base adds 25 effective manpower
        (store_faction_of_party, ":faction_no", ":center_no"),
        (faction_get_slot, ":serfdom", ":faction_no", dplmc_slot_faction_serfdom),
        (val_add, ":serfdom", 3),
        (val_mul, ":serfdom", 25),
        (val_add, ":divider", ":serfdom"),
        (gt, ":divider", ":num_prisoners"),

        #calculate time - manpower, prosperity, and int/level-based
        (party_get_slot, ":multiplier", ":center_no", slot_town_prosperity), #0 to 100
        (val_sub, ":multiplier", ":num_prisoners"), #feeding drags prosperity down
        (store_sub, ":multiplier", 300, ":multiplier"), #300 to 100
        (val_add, ":divider", ":skill"), #total 30~500 added from lord

        (store_mul, ":improvement_time", ":improvement_cost", ":multiplier"), #400000 - 2700000
        (val_div, ":improvement_time", 100),
        (val_div, ":improvement_time", ":divider"), #18.18~800
        (lt, ":improvement_time", 160), #feasible
        (val_max, ":improvement_time", 3), #not instantaneous

        (val_sub, ":troop_wealth", ":improvement_cost"),
        (troop_set_slot, ":troop_no", slot_troop_wealth, ":troop_wealth"),
        (try_begin),
          (this_or_next|eq, "$cheat_mode", 3),
          (ge, ":is_affiliated", 1),#<-- dplmc+ added
          (assign, reg6, ":improvement_time"),
          (str_store_troop_name_link, s10, ":troop_no"),
          #s0 comes from improvement_details
          (display_log_message, "@{s10} constructs a {s0} in {s4}", message_alert),
        (try_end),
        (assign, "$g_improvement_type", ":improvement_no"),
        # (assign, reg6, ":improvement_time"),
        (call_script, "script_improve_center", ":center_no", ":troop_no", ":improvement_time"),
      (try_end),
      ##
      ##diplomacy start+
      #Modify the next block to display for affiliates
      (try_begin),
        (this_or_next|ge, ":is_affiliated", 1),#<-- dplmc+ added
        (this_or_next|eq, "$cheat_mode", 1),
        (eq, "$cheat_mode", 3),
        (assign, reg1, ":troop_wealth"),
        (str_store_party_name_link, s4, ":center_no"),
        (add_troop_note_from_sreg, ":troop_no", 1, "str_current_wealth_reg1_taxes_last_collected_from_s4", 0),
        #New section, print a message for affiliates:
        (ge, ":is_affiliated", 1),
        (store_add, reg0, ":accumulated_rents", ":accumulated_tariffs"),
        (str_store_troop_name_link, s0, ":troop_no"),
        (try_begin),
           (gt, reg0, 0),
           (display_log_message, "@{s0} collects {reg0} denars from {s4}, current wealth: {reg1} denars"),
        (try_end),
      (try_end),
      ##diplomacy end+
    (try_end),

    #Recruit volunteers
    (try_begin),
        (is_between, ":center_no", villages_begin, villages_end),
        (party_get_slot, ":troop_amount", ":center_no", slot_center_npc_volunteer_troop_amount),
        (gt, ":troop_amount", 0),

        (party_get_slot, ":troop_type", ":center_no", slot_center_npc_volunteer_troop_type),
        (party_set_slot, ":center_no", slot_center_npc_volunteer_troop_amount, -1),
        ##diplomacy begin
        (try_begin),
          (store_faction_of_party, ":party_faction", ":led_party"),
          (eq, ":party_faction", "fac_player_supporters_faction"),
          (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
          (faction_get_slot, ":troop_type", "$g_player_culture", slot_faction_tier_1_troop),
        (try_end),

        (try_begin), #debug
          ##nested diplomacy start+
          (this_or_next|ge, ":is_affiliated", 1),#<- Show for affiliates
          (eq, "$cheat_mode", 1),
          ##nested diplomacy end+
          (assign, reg2, ":troop_amount"),
          # (str_store_string, s11, "@{reg2}"),
          (str_store_troop_name, s12, ":troop_type"),
          (str_store_faction_name_link, s13, ":party_faction"),
          (str_store_party_name_link, s14, ":center_no"),
          (str_store_party_name, s10, ":led_party"),
          (display_log_message, "@ {s10} of {s13} recruits {reg2} {s12} in {s14}"),
        (try_end),

        ##diplomacy end
        (party_add_members, ":led_party", ":troop_type", ":troop_amount"),
    (else_try), ##do business in centers
      (is_between, ":center_no", towns_begin, towns_end),
      (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),

      (try_begin), #hiring mercenaries
        (this_or_next|troop_slot_eq, ":troop_no", slot_troop_morality_type, tmt_egalitarian),
        (this_or_next|troop_slot_eq, ":troop_no", slot_troop_2ary_morality_type, tmt_egalitarian),
        (this_or_next|troop_slot_eq, ":troop_no", slot_troop_2ary_morality_type, tmt_aristocratic),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
        (party_get_slot, ":mercenary_troop", ":center_no", slot_center_mercenary_troop_type),
        (gt, ":mercenary_troop", 0),
        (store_character_level, ":level", ":mercenary_troop"),
        #chance of not hiring
        (store_random_in_range, ":reduce", ":level", 100),
        (gt, ":reduce", 69), #favors high-level
        # (game_get_reduce_campaign_ai, ":reduce"), #0 to 2
        # (val_mul, ":reduce", 5), #0 to 10
        # (store_sub, ":reduce", 26, ":reduce"), #26 to 16
        # (lt, ":level", ":reduce"), #no special mercs - on hard can hire top-tier, on easy caravan guard/xbow/lower
        (party_get_slot, ":mercenary_amount", ":center_no", slot_center_mercenary_troop_amount),
        (call_script, "script_game_get_join_cost", ":mercenary_troop"),
        (assign, ":troop_cost", reg0),
        # (try_begin), #slight discount for improvement
          # (party_get_slot, ":reduce", ":center_no", slot_center_has_mercenary_hall),
          # (val_add, ":reduce", 5),
          # (val_mul, ":troop_cost", 5),
          # (val_div, ":troop_cost", ":reduce"),
        # (try_end),
        #test wealth levels - a tenth normally can be used
        (store_faction_of_troop, ":faction_no", ":troop_no"),
        (faction_get_slot, ":quality", ":faction_no", dplmc_slot_faction_quality),
        (val_add, ":quality", 10),
        #use faction quality to determine percentage of wealth used for mercenaries
        (store_div, ":divider", ":troop_wealth", ":quality"),
        (val_div, ":divider", ":troop_cost"),
        (val_min, ":divider", ":mercenary_amount"),


        #set the proper slots
        (try_begin),
          (gt, ":divider", 0),
          (party_add_members, ":led_party", ":mercenary_troop", ":divider"),
          (val_mul, ":troop_cost", ":divider"),
          (val_sub, ":troop_wealth", ":troop_cost"),
          (store_sub, ":mercenary_amount", ":mercenary_amount", ":divider"),
          (party_set_slot, ":center_no", slot_center_mercenary_troop_amount, ":mercenary_amount"),
          (try_begin),
            (le, ":mercenary_amount", 0),
            (party_set_slot, ":center_no", slot_center_mercenary_troop_amount, -1),
            (party_set_slot, ":center_no", slot_center_mercenary_troop_type, -1),
          (else_try),
            (party_set_slot, ":center_no", slot_center_mercenary_troop_amount, ":mercenary_amount"),
          (try_end),
          (try_begin), #debug
            (this_or_next|ge, ":is_affiliated", 1),#<- Show for affiliates
            (ge, "$cheat_mode", 1),
            (assign, reg2, ":divider"),
            (str_store_troop_name_by_count, s12, ":mercenary_troop", reg2),
            (display_log_message, "@{s10} hires {reg2} {s12} in {s4}"),
          (try_end),
        (try_end),
      (try_end),
      ##upgrade equipment from merchants
      (call_script, "script_calculate_equipment_limit", ":troop_no", ":center_no"),
      (assign, ":equipment_limit", reg0),
      #we assume startup gear is sufficient - only quality matters
      # (try_for_range, ":slot", ek_item_0, ek_food), #can't only check equipment, it'll reload if you visit lord's hall
      (troop_get_inventory_capacity, ":cap", ":troop_no"),
      (try_for_range, ":slot", ek_item_0, ":cap"),
        (gt, ":troop_wealth", ":equipment_limit"), #has spare cash
        (troop_get_inventory_slot, ":item_no", ":troop_no", ":slot"),
        (neq, ":item_no", -1),
        (neg|item_has_property, ":item_no", itp_unique),
        (neg|item_has_property, ":item_no", itp_civilian), #why bother upgrading underwear
        (item_has_property, ":item_no", itp_merchandise), #can be sold, although player can drop loot off
        (troop_get_inventory_slot_modifier, ":old_imod", ":troop_no", ":slot"),
        # (item_get_slot, ":imod_mult", ":old_imod", slot_item_modifier_multiplier),
        (call_script, "script_dplmc_get_item_value_with_imod", ":item_no", ":old_imod"),
        (assign, ":imod_mult", reg0),
        (try_begin),
          (is_between, ":slot", ek_item_0, ek_head),
          (assign, ":merchant", slot_town_weaponsmith),
        (else_try),
          (is_between, ":slot", ek_item_0, ek_head),
          (assign, ":merchant", slot_town_armorer),
        (else_try),
          (eq, ":slot", ek_horse),
          (assign, ":merchant", slot_town_horse_merchant),
        (try_end),
        (party_get_slot, ":merchant", ":center_no", ":merchant"),
        #valid merchant
        (is_between, ":merchant", armor_merchants_begin, mayors_begin),
        (troop_get_inventory_capacity, ":cap", ":merchant"),
        (try_for_range, ":i_slot", 10, ":cap"),
          (troop_get_inventory_slot, ":item_id", ":merchant", ":i_slot"),
          (eq, ":item_id", ":item_no"), #same item found
          (troop_get_inventory_slot_modifier, ":imod", ":merchant", ":i_slot"),
          (neq, ":imod", ":old_imod"), ## in general higher imod = upgrade

          # (is_between, ":imod", imod_balanced, imod_large_bag + 1), #eliminate bad+plain ones
          # (item_get_slot, ":imod_cost", ":imod", slot_item_modifier_multiplier),
          (call_script, "script_dplmc_get_item_value_with_imod", ":item_id", ":imod"),
          (assign, ":imod_cost", reg0),
          (gt, ":imod_cost", ":imod_mult"), #superior price not necessarily better quality
          #troop can use item
          (call_script, "script_dplmc_troop_can_use_item", ":troop_no", ":item_id", ":imod"),
          (eq, reg0, 1),
          #we go for a pure value ratio - get_trade_penalty applies to player only
          (store_item_value, ":val", ":item_no"),
          (store_sub, ":cost", ":imod_cost", ":imod_mult"),
          (val_mul, ":cost", ":val"),
          (val_div, ":cost", 100),#base
          (gt, ":troop_wealth", ":cost"),
          (try_begin), #debug
            (eq, "$cheat_mode", 2),
            #(str_store_string, s11, "@{reg2}"),

            # (str_store_party_name_link, s14, ":center_no"),
            (str_store_item_name, s11, ":item_no"),
            (str_store_troop_name_link, s10, ":troop_no"),
            (str_store_party_name_link, s4, ":center_no"),
            (store_add, ":string", ":old_imod", "str_imod_plain"),
            (str_store_string, s3, ":string"),
            (call_script, "script_game_get_money_text", ":cost"),
            (assign, reg0, ":troop_wealth"),
            (display_log_message, "@{s10} upgrades {s3}{s11} (costing {s1}) in {s4}, {reg0} denars remaining."),
          (try_end),
          (val_sub, ":troop_wealth", ":cost"),
          (troop_set_inventory_slot_modifier, ":troop_no", ":slot", ":imod"),
          (troop_set_inventory_slot_modifier, ":merchant", ":i_slot", ":old_imod"),
          (troop_add_gold, ":merchant", ":cost"),
          (assign, ":cap", 10), #one item has one upgrade at a time
        (try_end),
      (try_end),
      ##upgrade end
    (try_end),

    # SB : set wealth after tax and consumption
    (troop_set_slot, ":troop_no", slot_troop_wealth, ":troop_wealth"),
    #DEBUG
    (try_begin),
	  (eq, "$cheat_mode", 2),
      (neq, ":troop_wealth", ":initial_wealth"),
      (assign, reg1, ":initial_wealth"),
      (str_store_troop_name_link, s1, ":troop_no"),
      (str_store_party_name_link, s2, ":center_no"),
      (assign, reg2, ":troop_wealth"),
      (display_message, "@{s1} spends time in {s2}, {reg1} -> {reg2} denars"),
    (try_end),
    #Courtship
    (try_begin),
		(party_get_slot, ":time_of_last_courtship", ":led_party", slot_party_leader_last_courted),
		(store_sub, ":hours_since_last_courtship", ":current_time", ":time_of_last_courtship"),
		(gt, ":hours_since_last_courtship", 72),

		(troop_slot_eq, ":troop_no", slot_troop_spouse, -1),
		##diplomacy start+ Disable this for inappropriate types
		(neg|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),#They use the last visited slots for other purposes
		(neg|is_between, ":troop_no", kings_begin, kings_end),#They should not be participating in this system
		(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),#They should not be participating in this system
		##diplomacy end+
		(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
			(troop_get_slot, ":love_interest", ":troop_no", ":love_interest_slot"),
			(gt, ":love_interest", 0),
			(troop_get_slot, ":love_interest_town", ":love_interest", slot_troop_cur_center),
			(eq, ":center_no", ":love_interest_town"),

			(call_script, "script_courtship_event_troop_court_lady", ":troop_no", ":love_interest"),
			(party_set_slot, ":led_party", slot_party_leader_last_courted, ":current_time"),
		(try_end),
    (try_end),

    ])
]
