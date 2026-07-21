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

process_village_raids_scripts = [
# script_process_village_raids
# Input: none
# Output: none
# called from triggers every two hours
("process_village_raids",
    [
       ##diplomacy start+
       (store_current_hours, ":hours"),
       ##diplomacy end+
       (game_get_reduce_campaign_ai, ":reduce_campaign_ai"), #SB: also move to top
       (try_for_range, ":village_no", villages_begin, villages_end),
        ##CABA Fix
        (try_begin),
          # Snow Check
          (this_or_next|is_between, ":village_no", "p_village_16", "p_village_23"), #Shapeshte through Shulus (up to Ilvia)
          (this_or_next|is_between, ":village_no", "p_village_49", "p_village_51"), #Tismirr and Karindi
          (this_or_next|eq, ":village_no", "p_village_75"), #Bhulaban
          (this_or_next|is_between, ":village_no", "p_village_85", "p_village_87"), #Ismirala and Slezkh
          (eq, ":village_no", "p_village_112"),
          (assign, ":normal_village_icon", "icon_village_snow_a"),
          (assign, ":burnt_village_icon", "icon_village_snow_burnt_a"),
          (assign, ":deserted_village_icon", "icon_village_snow_deserted_a"),
        (else_try),
          # Desert Check (Exclude your new villages from the catch-all group)
          (is_between, ":village_no", "p_village_91", "p_village_111"), #Ayn Assuadi through Rushdigh
          (assign, ":normal_village_icon", "icon_village_c"),
          (assign, ":burnt_village_icon", "icon_village_burnt_c"),
          (assign, ":deserted_village_icon", "icon_village_deserted_c"),
        (else_try),
          # Catch-all Default (This now handles standard plain villages
          (assign, ":normal_village_icon", "icon_village_a"),
          (assign, ":burnt_village_icon", "icon_village_burnt_a"),
          (assign, ":deserted_village_icon", "icon_village_deserted_a"),
        (try_end),
        ##CABA Fix
         (party_get_slot, ":village_raid_progress", ":village_no", slot_village_raid_progress),
         (try_begin),
           (party_slot_eq, ":village_no", slot_village_state, svs_normal), #village is normal
           (val_sub, ":village_raid_progress", 5),
           (val_max, ":village_raid_progress", 0),
           (party_set_slot, ":village_no", slot_village_raid_progress, ":village_raid_progress"),
           (try_begin),
             (lt, ":village_raid_progress", 50),

             (try_begin),
              (party_get_icon, ":village_icon", ":village_no"),
              (neq, ":village_icon", ":normal_village_icon"), ##CABA FIX
              (party_set_icon, ":village_no", ":normal_village_icon"), ##CABA FIX
             (try_end),

             (party_slot_ge, ":village_no", slot_village_smoke_added, 1),
             (party_set_slot, ":village_no", slot_village_smoke_added, 0),
             (party_clear_particle_systems, ":village_no"),
           (try_end),
         (else_try),
           (party_slot_eq, ":village_no", slot_village_state, svs_being_raided), #village is being raided
           #End raid unless there is an enemy party nearby
           (assign, ":raid_ended", 1),
           (party_get_slot, ":raider_party", ":village_no", slot_village_raided_by),
           # (call_script, "script_party_count_fit_regulars", ":village_no"), #SB : calculate cur size
           # (assign, ":villager_count", reg0),
           # (party_get_num_companions, ":villager_count", ":village_no"), #SB : calculate cur size, including wounded
           (call_script, "script_party_calculate_strength", ":village_no", 0),
           (store_div, ":village_strength", reg0, 2),
           (try_begin),
             (ge, ":raider_party", 0),
             (party_is_active, ":raider_party"),
             (party_stack_get_troop_id, ":raid_leader", ":raider_party", 0), #SB : moved to top
             (this_or_next|neq, ":raider_party", "p_main_party"),
             (eq, "$g_player_is_captive", 0),
             #SB : strength conditional, player bypasses this however since they actually fought
             (call_script, "script_party_calculate_strength", ":raider_party", 0),
             (this_or_next|eq, ":raider_party", "p_main_party"), #player raiding conditions are different
             (ge, reg0, ":village_strength"),
             # (party_slot_ge, ":raider_party", slot_party_cached_strength, ":village_strength"),
             (store_distance_to_party_from_party, ":distance", ":village_no", ":raider_party"),
             (lt, ":distance", raid_distance),
             (party_get_battle_opponent, ":raid_opponent", ":raider_party"), #dckplmc
             (lt, ":raid_opponent", 0), #continue raid only if there is no opposition
             (assign, ":raid_ended", 0),
           (try_end),

           (try_begin),
             (eq, ":raid_ended", 1),
             (call_script, "script_village_set_state", ":village_no", svs_normal), #clear raid flag
             (party_set_slot, ":village_no", slot_village_smoke_added, 0),
             (party_clear_particle_systems, ":village_no"),
           (else_try),
             (assign, ":raid_progress_increase", 11),
             (party_get_slot, ":looter_party", ":village_no", slot_village_raided_by),
             (try_begin),
               (party_get_skill_level, ":looting_skill", ":looter_party", "skl_looting"),
               (val_add, ":raid_progress_increase", ":looting_skill"),
             (try_end),
             (try_begin),
               (party_slot_eq, ":village_no", slot_center_has_watch_tower, 1),
               (val_mul, ":raid_progress_increase", 2),
               (val_div, ":raid_progress_increase", 3),
             (try_end),
             (val_add, ":village_raid_progress", ":raid_progress_increase"),
             #SB : delay construction while being looted
             (try_begin),
               (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
               (party_slot_ge, ":village_no", slot_center_current_improvement, 1),
               (party_get_slot, ":cur_improvement_end_time", ":village_no", slot_center_improvement_end_hour),
               (store_div, ":delay", ":raid_progress_increase", 3),
               (try_begin),
                 (party_slot_eq, ":village_no", slot_town_lord, "trp_player"),
                 (val_sub, ":delay", ":reduce_campaign_ai"),
               (try_end),
               (val_clamp, ":delay", 2, 8), #delayed for at least duration of raid
               (val_add, ":cur_improvement_end_time", ":delay"),
             (try_end),
             (party_set_slot, ":village_no", slot_village_raid_progress, ":village_raid_progress"),
             (try_begin),
               (ge, ":village_raid_progress", 50),
               (party_slot_eq, ":village_no", slot_village_smoke_added, 0),
               (party_add_particle_system, ":village_no", "psys_map_village_fire"),
               (party_add_particle_system, ":village_no", "psys_map_village_fire_smoke"),
               (party_set_icon, ":village_no", ":burnt_village_icon"), ##CABA FIX
               (party_set_slot, ":village_no", slot_village_smoke_added, 1),
             (try_end),
			 ##diplomacy start+ set values of slots
			 (try_begin),
				(ge, ":looter_party", 0),
				# (party_stack_get_troop_id, ":raid_leader", ":looter_party", 0),
				(ge, ":raid_leader", 0),
				(party_set_slot, ":village_no", dplmc_slot_center_last_attacked_time, ":hours"),
				(party_set_slot, ":village_no", dplmc_slot_center_last_attacker, ":raid_leader"),
			 (try_end),
             (assign, ":raid_total_captured", 0),
             (try_begin), #SB : enslavement mode
               (eq, ":looter_party", "p_main_party"),
               (party_slot_eq, ":village_no", slot_town_last_nearby_fire_time, 2), #enslavement mode

               #do some wounding first, in the first iteration all wounded from the initial encounter will be grabbed
               (store_random_in_range, ":random_no", ":reduce_campaign_ai", 4), #0 to 2 up to 3 per iteration
               (party_wound_members, ":village_no", "trp_farmer", ":random_no"),
               #(val_mul, ":random_no", 2),
               #(val_div, ":random_no", 3),
               (party_wound_members, ":village_no", "trp_peasant_woman", ":random_no"),

               #this is only effective for p_main_party anyway
               (call_script, "script_game_get_party_prisoner_limit", ":looter_party"),
               (assign, ":prisoner_limit", reg0),
               (party_get_num_prisoners, ":num_prisoners", ":looter_party"),
               (val_sub, ":prisoner_limit", ":num_prisoners"),

               (party_get_num_companion_stacks, ":num_stacks", ":village_no"),
               # (assign, ":num_wounded", 0),
               (party_get_slot, ":village_raid_progress", ":village_no", slot_village_raid_progress),
               (try_for_range_backwards, ":stack_no", 0, ":num_stacks"), #backwards to enslave women first
                 (party_stack_get_num_wounded, ":cur_wounded",":village_no",":stack_no"),
                 (gt, ":cur_wounded", 0),
                 (party_stack_get_troop_id, ":stack_troop",":village_no",":stack_no"),

                 (try_begin),
                    (lt, ":prisoner_limit", ":cur_wounded"),
                    (val_add, ":raid_total_captured", ":prisoner_limit"),
                    (party_remove_members_wounded_first, ":village_no", ":stack_troop", ":prisoner_limit"),
                    (party_add_prisoners, "p_main_party", ":stack_troop", ":prisoner_limit"),
                 (else_try),
                    (val_add, ":raid_total_captured", ":cur_wounded"),
                    (party_remove_members_wounded_first, ":village_no", ":stack_troop", ":cur_wounded"),
                    (party_add_prisoners, "p_main_party", ":stack_troop", ":cur_wounded"),
                 (try_end),

                 (try_begin),
                   (val_sub, ":prisoner_limit", ":cur_wounded"),
                   (le, ":prisoner_limit", 0),
                   (assign, ":num_stacks", 0),
                 (try_end),
               (try_end),
               (assign, reg1, ":raid_total_captured"),
               (try_begin),
                 (neq, reg1, 0),
                 (display_message, "@Captured {reg1} villagers."),
                 (val_add, "$qst_eliminate_bandits_infesting_village_num_villagers", ":raid_total_captured"),
               (try_end),
               (try_begin),
                 (party_get_num_companions, ":amount", ":village_no"),
                 (this_or_next|eq, ":amount", 0), #we have captured all
                 (eq, ":num_stacks", 0), #we have captured too many and broke the loop
                 (assign, ":raid_total_captured", -1), #mark this condition for later
               (else_try),
                 #for each three prisoner taken we move back the counter a bit
                 (store_div, ":amount", ":raid_total_captured", 3),
                 (val_sub, ":village_raid_progress", ":amount"),
                 (party_set_slot, ":village_no", slot_village_raid_progress, ":village_raid_progress"),
               (try_end),
             (try_end),
             #SB : probably spawn random refugees here as the raid progresses
             ##diplomacy end+
             #SB : add in enslavement function at around 75% completion, simulate each level taking off 0.5 hour
             #if the looting skill is too high we won't capture as many peasants
             (try_begin),
               (eq, ":looter_party", "p_main_party"),
               (party_slot_eq, ":village_no", slot_town_last_nearby_fire_time, 2), #enslavement mode
               (party_get_skill_level, ":management", ":looter_party", "skl_prisoner_management"),
               (val_mul, ":management", 5), #0 to 50 to 75
               (val_div, ":management", 3), #around 25
               (store_sub, ":threshold", 90, ":management"), #make sure this is before regular looting completes
               # (party_get_num_companions, ":amount", ":village_no"),
               # (party_get_free_prisoners_capacity, ":capacity", "p_main_party"), #or use previous calculation
               # (this_or_next|le, ":amount", 0), #we have wounded and captured all inhabitants
               # (this_or_next|le, ":capacity", 0), #we have no more room for capturing
               (this_or_next|eq, ":raid_total_captured", -1),
               (gt, ":village_raid_progress", ":threshold"),

               (str_store_party_name_link, s1, ":village_no"),
               (str_store_troop_name_link, s2, ":raid_leader"),
               (store_faction_of_party, ":village_faction", ":village_no"),
               (faction_get_color, ":color", ":village_faction"),
               (display_log_message, "@The village of {s1} has been sacked by {s2}.", ":color"),

               (try_begin),
                 (party_get_slot, ":village_lord", ":village_no", slot_town_lord),
                 (is_between, ":village_lord", active_npcs_begin, active_npcs_end),
                 (call_script, "script_troop_change_relation_with_troop", ":raid_leader", ":village_lord", -1),
                 (val_add, "$total_battle_enemy_changes", -1),
               (try_end),
               (call_script, "script_village_set_state",  ":village_no", svs_deserted), #not svs_looted, less prosperity decrease
               # (party_set_slot, ":village_no", slot_center_accumulated_rents, 0),
               # (party_set_slot, ":village_no", slot_center_accumulated_tariffs, 0),
               (party_set_slot, ":village_no", slot_village_raid_progress, 0),
               (party_set_slot, ":village_no", slot_village_recover_progress, 50), #SB : jumps directly to deserted icon, not burnt
               (party_set_slot, ":village_no", slot_village_smoke_added, 2), #to force trigger the icon

               (try_begin), #SB : this crippled lords too much
                 (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
                 (party_set_slot, ":village_no", slot_center_volunteer_troop_type, -1),
                 (party_set_slot, ":village_no", slot_center_volunteer_troop_amount, -1),
                 (party_set_slot, ":village_no", slot_center_npc_volunteer_troop_type, -1),
                 (party_set_slot, ":village_no", slot_center_npc_volunteer_troop_amount, -1),
               (try_end),
               (call_script, "script_add_log_entry", logent_village_raided, ":raid_leader",  ":village_no", -1, -1),
               (store_faction_of_party, ":looter_faction", ":looter_party"), #enslavement less severe than plundering
               (call_script, "script_faction_inflict_war_damage_on_faction", ":looter_faction", ":village_faction", 4),
             (else_try),
               (gt, ":village_raid_progress", 100),
               (str_store_party_name_link, s1, ":village_no"),
               # (party_stack_get_troop_id, ":raid_leader", ":looter_party", 0), #SB : move to top
               (ge, ":raid_leader", 0),
               #SB : colorize, string link
               # (str_store_party_name, s2, ":looter_party"),
               (try_begin),
                 (troop_is_hero, ":raid_leader"),
                 (str_store_troop_name_link, s2, ":raid_leader"),
               (else_try),
                 (str_store_party_name, s2, ":looter_party"),
               (try_end),
               (store_faction_of_party, ":village_faction", ":village_no"),
               (faction_get_color, ":color", ":village_faction"),
               (display_log_message, "@The village of {s1} has been looted by {s2}.", ":color"),

               #refugees
               (set_spawn_radius, 2),
               (spawn_around_party, ":village_no", "pt_refugees"),
               (assign, ":refugee_party", reg0),
               (party_add_template, ":refugee_party", "pt_village_farmers"),
               (party_add_template, ":refugee_party", "pt_village_farmers"),
               (party_set_faction, ":refugee_party", ":village_faction"),
               (assign, ":minimum_distance", 1000000),
               #SB : get rid of useless range
               (store_random_in_range, ":nearest_ally_city", walled_centers_begin, walled_centers_end),
               (try_for_range, ":party_no", walled_centers_begin, walled_centers_end),
                 (party_get_position, pos1, ":party_no"),
                 (store_distance_to_party_from_party, ":dist", ":party_no", ":village_no"),
                 (try_begin),
                   (lt, ":dist", ":minimum_distance"),
                   (assign, ":minimum_distance", ":dist"),
                   (assign, ":nearest_ally_city", ":party_no"),
                 (try_end),
               (try_end),
               (party_set_ai_behavior, ":refugee_party", ai_bhvr_travel_to_party),
               (party_set_ai_object, ":refugee_party", ":nearest_ally_city"),
               (party_set_slot, ":refugee_party", slot_party_home_center, ":village_no"),

               (try_begin),
                 (party_get_slot, ":village_lord", ":village_no", slot_town_lord),
                 (is_between, ":village_lord", active_npcs_begin, active_npcs_end),
                 (call_script, "script_troop_change_relation_with_troop", ":raid_leader", ":village_lord", -1),
                 (val_add, "$total_battle_enemy_changes", -1),
               (try_end),

               #give loot gold to raid leader
               (troop_get_slot, ":raid_leader_gold", ":raid_leader", slot_troop_wealth),
			   ##diplomacy start+
			   #How did the next line ever work?  isn't it missing a slot number?!
               #  (party_get_slot, ":village_prosperity", ":village_no"),
			   #Replace it with the following:
			   (party_get_slot, ":village_prosperity", ":village_no", slot_town_prosperity),
			   ##diplomacy end+
               (store_mul, ":value_of_loot", ":village_prosperity", 60), #average is 3000
               (val_add, ":raid_leader_gold", ":value_of_loot"),
               (troop_set_slot, ":raid_leader", slot_troop_wealth, ":raid_leader_gold"),
			   (try_begin),
				   (eq, "$cheat_mode", 2),
				   (assign, reg2, ":raid_leader_gold"),
				   (str_store_troop_name_link, s2, ":raid_leader"),
				   (display_message, "@{s2} now has {reg2} denars from raiding"),#SB : debug
               (try_end),
               #take loot gold from village lord #new 1.126
			   ##diplomacy start+
			   #With economic changes enabled, this will first withdraw from accumulated taxes at center
               (try_begin),
				 #To support the possibility of kingdom_ladies becoming enfeoffed, changed the
				 #below line from active_npcs_begin/active_npcs_end to heroes_begin/heroes_end
                 (is_between, ":village_lord", heroes_begin, heroes_end),
				 (neq, ":village_lord", "trp_kingdom_heroes_including_player_begin"),
                 (troop_get_slot, ":village_lord_gold", ":village_lord", slot_troop_wealth),
				 (try_begin),
					#Optional behavior: subtract the looted wealth from the village's uncollected
					#rents and tariffs
					(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),#<-- check experimental changes are enabled
					(assign, ":gold_lost_by_lord", ":value_of_loot"),
					#Accumulated rents & tariffs get zeroed further down, so we don't need to worry
					#about modifying the slot's value to reflect the loss.
					(party_get_slot, ":x", ":village_no", slot_center_accumulated_rents),
					(val_max, ":x", 0),
					(val_sub, ":gold_lost_by_lord", ":x"),
					(party_get_slot, ":x", ":village_no", slot_center_accumulated_tariffs),
					(val_max, ":x", 0),
					(val_sub, ":gold_lost_by_lord", ":x"),
					#Only then subtract the remainder from the lord
					(val_max, ":gold_lost_by_lord", 0),
					(val_sub, ":village_lord_gold", ":gold_lost_by_lord"),
				 (else_try),
					#Unaltered behavior
					(val_sub, ":village_lord_gold", ":value_of_loot"),
				 (try_end),
				 #Apply the gold change
                 (val_max, ":village_lord_gold", 0),
                 (troop_set_slot, ":village_lord", slot_troop_wealth, ":village_lord_gold"),
                 (try_begin),
                    (eq, "$cheat_mode", 2),
                     (assign, reg2, ":village_lord_gold"),
                     (str_store_troop_name_link, s2, ":village_lord"),
                     (display_message, "@{s2} now has {reg2} denars from being raided"),#SB : debug
                 (try_end),
			   (else_try),
			      #Option: player loses gold when his fiefs are raided, just as an NPC does
				  #(default behavior in Native is the player loses no gold).  The gold is
				  #lost from the treasury, and is reduced by uncollected taxes.
				  #
				  #Only do this if the option is explicitly enabled and the player has
				  # a chamberlain.
				  (eq, ":village_lord", "trp_player"),
				  (gt, "$g_player_chamberlain", 0),#check the player has a chamberlain
			      (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),#<-- check experimental changes are enabled
				  (party_slot_eq, ":village_no", slot_town_lord, "trp_player"),
				  #Do some double-checking, to avoid potential erroneous gold loss
				  #if some careless code has improperly left the "slot_town_lord"
				  #slot of the village initialized to zero.
				  (store_faction_of_party, ":village_faction", ":village_no"),
				 ##diplomacy start+ Handle player is co-ruler of faction
				 (assign, ":is_coruler", 0),
 				 (try_begin),
				    (eq, ":village_faction", "$players_kingdom"),
					(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
					(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
					(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
					(assign, ":is_coruler", 1),
				 (try_end),
				 (this_or_next|eq, ":is_coruler", 1),
				 ##diplomacy end+
				  (this_or_next|eq, "fac_player_supporters_faction", ":village_faction"),
				     (eq, "$players_kingdom", ":village_faction"),
				  #Adjust the amount lost by difficulty setting.
				  (assign, ":gold_lost_by_lord", ":value_of_loot"),
				  # (game_get_reduce_campaign_ai, ":reduce_campaign_ai"), #SB: move to top
				  (try_begin),
				    (eq, ":reduce_campaign_ai", 0),#hard, 125% loss
					(val_mul, ":gold_lost_by_lord", 5),
					(val_div, ":gold_lost_by_lord", 4),
				  (else_try),
					(eq, ":reduce_campaign_ai", 1),#medium, 100% loss
				  (else_try),
					(eq, ":reduce_campaign_ai", 2),#easy, 50% loss
					(val_div, ":gold_lost_by_lord", 2),
				  (try_end),

				  #First defray the lost gold with rents and tarriffs from the village
				  (party_get_slot, ":x", ":village_no", slot_center_accumulated_rents),
				  (val_max, ":x", 0),
				  (val_sub, ":gold_lost_by_lord", ":x"),
				  (party_get_slot, ":x", ":village_no", slot_center_accumulated_tariffs),
				  (val_max, ":x", 0),
				  (val_sub, ":gold_lost_by_lord", ":x"),
				  (val_max, ":gold_lost_by_lord", 0),
				  #Remove the remainder (if any) from the player's treasury
				  (store_troop_gold, ":x", "trp_household_possessions"),
				  (val_min, ":gold_lost_by_lord", ":x"),
				  (ge, ":gold_lost_by_lord", 1),
				  (call_script, "script_dplmc_withdraw_from_treasury", ":gold_lost_by_lord"),
               (try_end),
			   ##diplomacy end+

               (call_script, "script_village_set_state",  ":village_no", svs_looted),
               (party_set_slot, ":village_no", slot_center_accumulated_rents, 0), #new 1.126
               (party_set_slot, ":village_no", slot_center_accumulated_tariffs, 0), #new 1.126

               (party_set_slot, ":village_no", slot_village_raid_progress, 0),
               (party_set_slot, ":village_no", slot_village_recover_progress, 0),

               #SB : also get rid of recruits, technically they should have perished in the fighting
               (try_begin), #SB : this crippled lords too much
                 (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
                 (party_set_slot, ":village_no", slot_center_volunteer_troop_type, -1),
                 (party_set_slot, ":village_no", slot_center_volunteer_troop_amount, -1),
                 (party_set_slot, ":village_no", slot_center_npc_volunteer_troop_type, -1),
                 (party_set_slot, ":village_no", slot_center_npc_volunteer_troop_amount, -1),
               (try_end),
               #finally clear the party
               # (party_clear, ":village_no"),
               (call_script, "script_party_wound_all_members", ":village_no"),
               (try_begin),
                 (store_faction_of_party, ":village_faction", ":village_no"),
				 ##diplomacy start+ Handle player is co-ruler of faction
				 (assign, ":is_coruler", 0),
 				 (try_begin),
				    (eq, ":village_faction", "$players_kingdom"),
					(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
					(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
					(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
					(assign, ":is_coruler", 1),
				 (try_end),
				 (this_or_next|eq, ":is_coruler", 1),
				 ##diplomacy end+
                 (this_or_next|party_slot_eq, ":village_no", slot_town_lord, "trp_player"),
                 (eq, ":village_faction", "fac_player_supporters_faction"),
                 (call_script, "script_add_notification_menu", "mnu_notification_village_raided", ":village_no", ":raid_leader"),
               (try_end),
               (call_script, "script_add_log_entry", logent_village_raided, ":raid_leader",  ":village_no", -1, -1),
               (store_faction_of_party, ":looter_faction", ":looter_party"),
               (call_script, "script_faction_inflict_war_damage_on_faction", ":looter_faction", ":village_faction", 5),
             (try_end),
           (try_end),
         (else_try),
           (this_or_next|party_slot_eq, ":village_no", slot_village_state, svs_looted), #village is looted
           (party_slot_eq, ":village_no", slot_village_state, svs_deserted), #SB : village is deserted
           (party_get_slot, ":recover_progress", ":village_no", slot_village_recover_progress),
           (val_add, ":recover_progress", 1),
           (party_set_slot, ":village_no", slot_village_recover_progress, ":recover_progress"), #village looted

           (try_begin), #SB : add some looters, around twice per lifetime
             (store_mod, ":looter_chance", ":recover_progress", 10),
             (eq, ":looter_chance", 0),
             (store_random_in_range, ":random_value", 0, 5),
             (eq, ":random_value", 0),
             (set_spawn_radius, 5),
             (spawn_around_party, ":village_no", "pt_looters"),
           (try_end),
           (try_begin),
             (ge, ":recover_progress", 10),
             (party_slot_eq, ":village_no", slot_village_smoke_added, 1),
             (party_clear_particle_systems, ":village_no"),
             (party_add_particle_system, ":village_no", "psys_map_village_looted_smoke"),
             (party_set_slot, ":village_no", slot_village_smoke_added, 2),
           (try_end),
           (try_begin),
             (gt, ":recover_progress", 50),
             (party_slot_eq, ":village_no", slot_village_smoke_added, 2),
             (party_clear_particle_systems, ":village_no"),
             (party_set_slot, ":village_no", slot_village_smoke_added, 3),
             (party_set_icon, ":village_no", ":deserted_village_icon"), ##CABA FIX
           (try_end),
           (try_begin),
             (gt, ":recover_progress", 100),
             (call_script, "script_village_set_state",  ":village_no", svs_normal),#village back to normal
             (party_set_slot, ":village_no", slot_village_recover_progress, 0),
             (party_clear_particle_systems, ":village_no"),
             (party_set_slot, ":village_no", slot_village_smoke_added, 0),
             (party_set_icon, ":village_no", ":normal_village_icon"), ##CABA FIX
           (try_end),
         (try_end),
       (try_end),
  ])
]
