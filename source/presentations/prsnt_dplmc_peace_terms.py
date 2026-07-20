# -*- coding: cp1254 -*-
import string
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
#SB: import skills from ID_skills import *
from module_constants import *
##diplomacy start+ Import for use with terrain advantage
from header_terrain_types import *
from module_items import *
#SB : import colors
from module_factions import *
from header_items import *
##diplomacy end
from compiler import *

dplmc_peace_terms = ("dplmc_peace_terms",0,mesh_load_window,[
      (ti_on_presentation_load,
       [
        (set_fixed_point_multiplier, 1000),
        (presentation_set_duration, 999999),

        # done
        (create_game_button_overlay, "$g_presentation_obj_10", "str_done"),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 25),
        (overlay_set_position, "$g_presentation_obj_10", pos1),

        #cancel
        (create_game_button_overlay, "$g_presentation_obj_9", "@Cancel"),
        (position_set_x, pos1, 100),
        (overlay_set_position, "$g_presentation_obj_9", pos1),

        # title
        (create_text_overlay, reg1, "@Dictate the peace terms", tf_center_justify|tf_vertical_align_center),
        (position_set_x, pos1, 445),
        (position_set_y, pos1, 700),
        (overlay_set_position, reg1, pos1),

        (position_set_y, pos1, 550),
        (create_text_overlay, "$g_presentation_obj_2", "@Select the castle and the amount of money and check the boxes to activate the demand. The demands are combined if both boxes are checked."),
        (position_set_x, pos1, 50),
        (overlay_set_position, "$g_presentation_obj_2", pos1),

        (create_slider_overlay, "$g_presentation_obj_sliders_1", 1, 10),
        (overlay_set_val, "$g_presentation_obj_sliders_1", 1),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, 350),
        (overlay_set_position, "$g_presentation_obj_sliders_1", pos1),
        (assign, "$demanded_money", 1000),
        (assign, "$diplomacy_var", 1),

        (create_text_overlay, "$g_presentation_obj_sliders_2", "@1000 denars"),
        (position_set_x, pos1, 500),
        (overlay_set_position, "$g_presentation_obj_sliders_2", pos1),

        (create_check_box_overlay, "$g_presentation_obj_battle_check0", "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 700),
        (overlay_set_position, "$g_presentation_obj_battle_check0", pos1),
        (overlay_set_val, "$g_presentation_obj_battle_check0", 1),

        (assign, "$demanded_castle", 0),
        (assign, ":castle_count", 0),
        (create_combo_button_overlay, "$g_presentation_obj_1"),
        (try_for_range, ":castle", castles_begin, castles_end),
		  ##diplomacy start+
		  (party_slot_eq, ":castle", slot_party_type, spt_castle),
		  ##diplomacy end+
          (store_faction_of_party, ":castle_faction", ":castle"),
          (eq, ":castle_faction", "$g_notification_menu_var1"),
          (str_store_party_name, s2, ":castle"),
          (overlay_add_item, "$g_presentation_obj_1", s2),
          (assign, "$demanded_castle", ":castle"),
          (val_add, ":castle_count", 1),
        (end_try),
        (assign, "$diplomacy_var2", 0),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, 250),
        (overlay_set_position, "$g_presentation_obj_1", pos1),
        (overlay_set_val, "$g_presentation_obj_1", ":castle_count"),

        (create_check_box_overlay, "$g_presentation_obj_battle_check1", "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 700),
        (overlay_set_position, "$g_presentation_obj_battle_check1", pos1),

        ]),
      (ti_on_presentation_run,
       [
        ]),
      (ti_on_presentation_event_state_change,
       [(store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_1"),

          (assign, ":cur", 0),
          (try_for_range, ":castle", castles_begin, castles_end),
            (store_faction_of_party, ":castle_faction", ":castle"),
            (eq, ":castle_faction", "$g_notification_menu_var1"),
            (try_begin),
              (eq, ":cur", ":value"),
              (assign, "$demanded_castle", ":castle"),
            (try_end),
            (val_add, ":cur", 1),
          (try_end),

        (else_try),
          (eq, ":object", "$g_presentation_obj_battle_check0"),
          (assign, "$diplomacy_var", ":value"),

        (else_try),
          (eq, ":object", "$g_presentation_obj_battle_check1"),
          (assign, "$diplomacy_var2", ":value"),

        (else_try),
          (eq, ":object", "$g_presentation_obj_sliders_1"),
          (store_mul, "$demanded_money",":value", 1000),
		  ##diplomacy start+
		  ##OLD:
          #(assign, reg0, "$demanded_money"),
          #(overlay_set_text, "$g_presentation_obj_sliders_2", "@{reg0} denars"),
		  ##NEW:
		  (assign, reg1, "$demanded_money"),
		  (overlay_set_text, "$g_presentation_obj_sliders_2", "str_reg1_denars"),
		  ##diplomacy end+

        (else_try),
          (eq, ":object", "$g_presentation_obj_9"),
          (presentation_set_duration, 0),
        (else_try),
          (eq, ":object", "$g_presentation_obj_10"),
          (presentation_set_duration, 0),

          (try_begin),
            (eq, "$diplomacy_var", 0),
            (assign, "$demanded_money", 0),
          (try_end),

          (try_begin),
            (eq, "$diplomacy_var2", 0),
            (assign, "$demanded_castle", 0),
          (try_end),

          (assign, ":demand", 0),
          (try_begin),
            (gt, "$demanded_money", 0),
            (store_div, ":demand", "$demanded_money", 1000),
          (try_end),
		  ##nested diplomacy start+
		  #OLD:
		  #(try_begin),
          #   (is_between, "$demanded_castle", castles_begin, castles_end),
          #   (val_add, ":demand", 12),
          #(try_end),
		  #NEW:
		  #
		  #Not all castles are created equal.
		  (assign, ":npc_faction", "$g_notification_menu_var1"),

		  (assign, ":player_faction", "fac_player_supporters_faction"),
		  (try_begin),
		     (neg|faction_slot_eq, ":player_faction", slot_faction_state, sfs_active),
			 (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
			 (assign, ":player_faction", "$players_kingdom"),
		  (try_end),

		  #(assign, ":castle_value", 0),
		  (assign, ":was_taken_recently", 0),
		  (assign, ":would_make_lord_fiefless", 0),
		  (assign, ":distance_factor", 100),#If positive, 100 times the ratio of distance of closest friendly center to closest enemy center; if negative, 100 times the ratio of the distance of the closest enemy center to the closest friendly center.
		  (try_begin),
			(is_between, "$demanded_castle", castles_begin, castles_end),
			## (1) Determine whether or not the demanded castle was taken recently.
			(try_begin),
				#This version of Diplomacy+ saves transfer times, so we can check directly.
				(neg|party_slot_eq, "$demanded_castle", dplmc_slot_center_last_transfer_time, 0),
				(store_current_hours, ":hours_since_capture"),
				(party_get_slot, reg0, "$demanded_castle", dplmc_slot_center_last_transfer_time),
				(val_sub, ":hours_since_capture", reg0),
				(try_begin),
					#In the last month (i.e. about a war)
					(lt, ":hours_since_capture", 31 * 24),
					(assign, ":was_taken_recently", 1),
				(else_try),
					#For non-core castles, extend the definition of recent to the last three months
					(neg|party_slot_eq, "$demanded_castle", slot_center_original_faction, ":npc_faction"),
					(lt, ":hours_since_capture", 91 * 24),
					(assign, ":was_taken_recently", 1),
				(else_try),
					(assign, ":was_taken_recently", 0),
				(try_end),
			(else_try),
				#This is an old saved game, so use some rules of thumb.
				#If the player faction is the original or previous owner, it might have been taken recently.
				(this_or_next|party_slot_eq, "$demanded_castle", slot_center_original_faction, "$players_kingdom"),
				(this_or_next|party_slot_eq, "$demanded_castle", slot_center_ex_faction, "$players_kingdom"),
					(party_slot_eq, "$demanded_castle", slot_center_ex_faction, "fac_player_supporters_faction"),
				(assign, ":was_taken_recently", 1),
			(else_try),
				#If the original owner is at war with the current owner, it might have been taken recently.
				(neg|party_slot_eq, "$demanded_castle", slot_center_original_faction, ":npc_faction"),
				(party_get_slot, ":third_faction", "$demanded_castle", slot_center_original_faction),
				(is_between, ":third_faction", kingdoms_begin, kingdoms_end),
				(faction_slot_eq, ":third_faction", slot_faction_state, sfs_active),
				(store_relation, reg0, ":npc_faction", ":third_faction"),
				(lt, reg0, 0),
				(assign, ":was_taken_recently", 1),
			(else_try),
				#If the ex-owner is at war with the current owner, it might have been taken recently.
				(neg|party_slot_eq, "$demanded_castle", slot_center_ex_faction, ":npc_faction"),
				(party_get_slot, ":third_faction", "$demanded_castle", slot_center_ex_faction),
				(is_between, ":third_faction", kingdoms_begin, kingdoms_end),
				(faction_slot_eq, ":third_faction", slot_faction_state, sfs_active),
				(store_relation, reg0, ":npc_faction", ":third_faction"),
				(lt, reg0, 0),
				(assign, ":was_taken_recently", 1),
			(else_try),
				#If there is no assigned lord, it was taken recently.
				(neg|party_slot_ge, "$demanded_castle", slot_town_lord, 0),
				(assign, ":was_taken_recently", 1),
			(try_end),##End "Was taken recently?"
			## (2) Determine whether handing over the demanded castle would cost any lord his last fief.
			## (2a: At the same time, calculate the closest friendly & enemy walled centers)
			(party_slot_ge, "$demanded_castle", slot_town_lord, 1),
			(party_get_slot, ":lord_a", "$demanded_castle", slot_town_lord),
			(assign, ":lord_b", -1),
			(assign, ":would_make_lord_fiefless", 1),
			(assign, ":distance_to_friendly_fortress", 10000),
			(assign, ":distance_to_enemy_fortress", 10000),
			(try_for_range, ":center_no", centers_begin, centers_end),
				(neq, ":center_no", "$demanded_castle"),
				#Check for fieflessness
				(try_begin),
					(party_slot_eq, ":center_no", slot_village_bound_center, "$demanded_castle"),
					(neg|party_slot_eq, ":center_no", slot_town_lord, ":lord_a"),
					(party_slot_ge, ":center_no", slot_town_lord, 1),
					(party_get_slot, ":lord_b", ":center_no", slot_town_lord),
				(else_try),
					(party_slot_eq, ":center_no", slot_town_lord, ":lord_a"),
					(neg|party_slot_eq, ":center_no", slot_village_bound_center, "$demanded_castle"),
					(assign, ":would_make_lord_fiefless", 0),
				(try_end),
				#For walled centers check distance
				(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
					(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_castle),

				(store_faction_of_party, ":center_faction", ":center_no"),
				(store_distance_to_party_from_party, ":cur_distance", ":center_no", "$demanded_castle"),

				(call_script, "script_dplmc_get_faction_truce_length_with_faction", ":center_faction", ":npc_faction"),
				(try_begin),
					(this_or_next|gt, reg0, dplmc_treaty_defense_days_expire),
					(eq, ":center_faction", ":npc_faction"),
					(val_min, ":distance_to_friendly_fortress", ":cur_distance"),
				(else_try),
					(store_relation, reg0, ":center_faction", ":npc_faction"),
					(val_min, ":distance_to_enemy_fortress", ":cur_distance"),
				(try_end),
			(try_end),
			#(2a, set distance factor based on closest other fortress)
			(assign, ":distance_factor", 100),
			(try_begin),
				(this_or_next|ge, ":distance_to_friendly_fortress", 10000),
					(ge, ":distance_to_enemy_fortress", 10000),
				#No fortress found for one or both
			(else_try),
				#Friendly is closer
				(lt, ":distance_to_friendly_fortress", ":distance_to_enemy_fortress"),
				(gt, ":distance_to_enemy_fortress", 25),#Within 25 ignore differences
				(val_max, ":distance_to_friendly_fortress", 1),
				(store_mul, ":distance_factor", ":distance_to_enemy_fortress", 100),
				(val_div, ":distance_factor", ":distance_to_friendly_fortress"),
				(try_begin),
					(le, ":distance_to_enemy_fortress", 50),
					(val_min, ":distance_factor", 200),
				(try_end),
			(else_try),
				#Enemy is closer
				(lt, ":distance_to_enemy_fortress", ":distance_to_friendly_fortress"),
				(gt, ":distance_to_friendly_fortress", 25),#Within 25 ignore differences
				(val_max, ":distance_to_enemy_fortress", 1),
				(store_mul, ":distance_factor", ":distance_to_friendly_fortress", 100),
				(val_div, ":distance_factor", ":distance_to_enemy_fortress"),
				(try_begin),
					(le, ":distance_to_friendly_fortress", 50),
					(val_min, ":distance_factor", 200),
				(try_end),
				(val_mul, ":distance_factor", -1),
			(try_end),##end 2a: distance factor

			(neq, ":would_make_lord_fiefless", 1),#If we already know it would make the castle owner fiefless, stop.
			(ge, ":lord_b", 1),
			(assign, ":would_make_lord_fiefless", 1),
			(try_for_range, ":center_no", centers_begin, centers_end),
				(party_slot_eq, ":center_no", slot_town_lord, ":lord_b"),
				(this_or_next|neg|is_between, ":center_no", villages_begin, villages_end),
					(neg|party_slot_eq, ":center_no", slot_village_bound_center, "$demanded_castle"),
					(assign, ":would_make_lord_fiefless", 0),
			(try_end),
		  (try_end),##end 2: would make lord fiefless?
		  (assign, ":castle_strength_ratio", 100),
		  (assign, ":high_ratio", 150),
		  (try_begin),
			(is_between, "$demanded_castle", castles_begin, castles_end),
			#(3) Determine typical castle strength
			(assign, ":typical_strength", 0),
			(assign, ":high_ratio", 0),#<- for now, store max strength seen
			(try_for_range, ":center_no", castles_begin, castles_end),
				(try_begin),
					(eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
					(call_script, "script_dplmc_party_calculate_strength_in_terrain", ":center_no", dplmc_terrain_code_siege, 0, 1),
					#Outputs to reg0 (using terrain) and reg1 (not using terrain).  We'll be using reg1,
					#but the function will be updating the cached strength using the terrain version (as I want).
					(assign, reg0, reg1),
				(else_try),
					#Use the non-terrain-modified strength script.
					(call_script, "script_party_calculate_strength", ":center_no", dplmc_terrain_code_siege, 0),
				(try_end),

				(val_max, reg0, 250),#A certain minimum scale is assumed
				(val_add, ":typical_strength", reg0),
				(val_max, ":high_ratio", reg0),#keep track of max
				(eq, ":center_no", "$demanded_castle"),
				(assign, ":castle_strength_ratio", reg0),
			(try_end),
			(try_begin),
				(gt, castles_end, castles_begin),
				(store_sub, reg0, castles_end, castles_begin),
				(val_div, ":typical_strength", reg0),
			(try_end),
			(val_max, ":typical_strength", 300),#<- A certain minimum scale is assumed
			(val_mul, ":castle_strength_ratio", 100),
			(val_mul, ":high_ratio", 100),

			(store_div, reg0, ":typical_strength", 2),

			(val_add, ":castle_strength_ratio", reg0),
			(val_add, ":high_ratio", reg0),

			(val_div, ":castle_strength_ratio", ":typical_strength"),
			(val_div, ":high_ratio", ":typical_strength"),

			(assign, reg0, ":castle_strength_ratio"),
			(val_max, reg0, 100),
			(val_mul, reg0, 12),#Scale so that 100 is 12, 200 is 24, etc.
			(val_add, reg0, 50),
			(val_div, reg0, 100),
			(val_add, ":demand", reg0),

			(val_sub, ":high_ratio", 100),
			(val_div, ":high_ratio", 2),
			(val_add, ":high_ratio", 100),
			(val_clamp, ":high_ratio", 110, 400),
		  (try_end),##end (3) determine typical castle strength

		  ##Next line: replace fac_player_supporters_faction with :player_faction
          (call_script, "script_npc_decision_checklist_peace_or_war", "$g_notification_menu_var1", ":player_faction", -1),

		  ##Save the unmodified numbers for later
		  (assign, ":check_peace_war_result", reg0),
		  #(assign, ":original_demand", ":demand"),
		  ##diplomacy end+
          (assign, ":goodwill", reg0),
          (val_mul, ":goodwill", 2),
          (store_random_in_range, ":random", 0, ":demand"),

          (val_div, ":demand", -2),

          (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", ":demand"),
		  ##diplomacy start+
		  #Count "third party" kingdoms: kingdoms that aren't either the player's kingdom
		  #or the other kingdom in the negotiations, and that aren't allied to either.
		  #(faction_get_slot, ":npc_faction_leader", ":npc_faction", slot_faction_leader),
		  (assign, ":other_players", 0),
		  (try_for_range, ":third_faction", kingdoms_begin, kingdoms_end),
			 #Active faction
		     (faction_slot_eq, ":third_faction", slot_faction_state, sfs_active),
			 (neq, ":third_faction", ":npc_faction"),
			 (neq, ":third_faction", "fac_player_supporters_faction"),
			 (neq, ":third_faction", "$players_kingdom"),
			 #Not allied (full alliance or defensive alliance) to either faction
			 (call_script, "script_dplmc_get_faction_truce_length_with_faction", ":third_faction", ":npc_faction"),
			 (le, reg0, dplmc_treaty_defense_days_expire),
			 (call_script, "script_dplmc_get_faction_truce_length_with_faction", ":third_faction", "$players_kingdom"),
			 (le, reg0, dplmc_treaty_defense_days_expire),
			 (val_add, ":other_players", 1),
		  (try_end),
		  #Improve the AI's decision-making somewhat.
		  (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
		  (val_clamp, ":reduce_campaign_ai", 0, 3),#0 is hard, 1 is medium, 2 is easy
		  (try_begin),
            #This should never be reached.
				(lt, ":check_peace_war_result", 0),
            (this_or_next|is_between, "$demanded_castle", castles_begin, castles_end),
               (gt, "$demanded_money", 0),
			(jump_to_menu,"mnu_dplmc_deny_terms"),
        (else_try),
            (is_between, "$demanded_castle", castles_begin, castles_end),
				(lt, ":check_peace_war_result", 2),
            #Don't enable "fishing" for fiefs, hoping to get a lucky
            #result.  Make the chance of giving a fief zero.
            (this_or_next|party_slot_eq,"$demanded_castle",slot_center_original_faction,":npc_faction"),
            (this_or_next|eq, ":would_make_lord_fiefless", 1),
            (this_or_next|ge, ":castle_strength_ratio", ":high_ratio"),
				(this_or_next|eq, ":was_taken_recently", 0),
               (eq, ":other_players", 0),
			(jump_to_menu,"mnu_dplmc_deny_terms"),
        (else_try),
            (is_between, "$demanded_castle", castles_begin, castles_end),
            #Some things will just never be agreed to.
				#If three or more of the following are true, reject:
				#- The demanded castle was not taken recently
				#- The demanded castle is one of the faction's original castles
				#- Giving the castle would make some lords fiefless
				#- The castle has an especially large garrison
				#- Aside from the player's faction and the NPC faction (and their allies),
				#  there are no other kingdoms.
				#- The demanded castle is significantly deeper within the NPC kingdom's territory
				#  than it is close to enemy territory
            (assign, reg0, 1),
			(val_sub, reg0, ":was_taken_recently"),
			(val_max, reg0, 0),
            (try_begin),#Check: is the castle part of the faction's original territory?
               (party_slot_eq,"$demanded_castle",slot_center_original_faction,":npc_faction"),
			   (val_add, reg0, 1),
            (try_end),
			(val_max, ":would_make_lord_fiefless", 0),
			(val_add, reg0, ":would_make_lord_fiefless"),
			(try_begin),#Check: castle has high strength compared to average?
				 (ge, ":castle_strength_ratio", ":high_ratio"),
				 (val_add, reg0, 1),
			(try_end),
			(try_begin),#Check: no one else remaining?
				 (eq, ":other_players", 0),
				 (val_add, reg0, 1),
			(try_end),
			(try_begin),#Check: is it much closer to friendly centers than enemy centers?
				(ge, ":distance_factor", 190),
				(val_add, reg0, 1),
			(try_end),
			(val_add, ":random", reg0),#Even if less than 3 are met, other factors will still decrease likelihood of acceptance.

			(ge, reg0, 3),
			(jump_to_menu,"mnu_dplmc_deny_terms"),
        (else_try),
			#SPECIAL CASE: Two Kingdoms Remain
			(eq, ":other_players", 0),
			(this_or_next|is_between, "$demanded_castle", castles_begin, castles_end),
				(gt, "$demanded_money", 0),
			(is_between, ":npc_faction", kingdoms_begin, kingdoms_end),
			(assign, ":minimum_peace_war_result", 2),
			(try_begin),
				#Hard: never accept.
				(eq, ":reduce_campaign_ai", 0),
				(store_add, ":minimum_peace_war_result", ":check_peace_war_result", 1),
				(val_max, ":minimum_peace_war_result", 4),
			(else_try),
				#Medium: never give up fiefs, sometimes accept other deals.
				(eq, ":reduce_campaign_ai", 1),
				(is_between, "$demanded_castle", castles_begin, castles_end),
				(store_add, ":minimum_peace_war_result", ":check_peace_war_result", 1),
				(val_max, ":minimum_peace_war_result", 4),
			(else_try),
				#Easy: sometimes accept.
				(eq, ":reduce_campaign_ai", 2),
			(try_end),
			(lt, ":check_peace_war_result", ":minimum_peace_war_result"),
			(jump_to_menu,"mnu_dplmc_deny_terms"),
		  (else_try),
		  #fall through to other behavior
		  ##diplomacy end+
            (le, ":random", ":goodwill"),
            (try_begin),
              (is_between, "$demanded_castle", castles_begin, castles_end),
				  ##diplomacy start+
				  #Relation hit with the owner of the surrendered castle and its village,
				  #if there was a valid owner.
				  (try_begin),
					(party_slot_ge, "$demanded_castle", slot_town_lord, 1),
					(party_get_slot, reg0, ":center_no", slot_town_lord),
					(call_script, "script_change_player_relation_with_troop", reg0, -1),
				  (try_end),
				  (try_for_range, ":center_no", villages_begin, villages_end),
					(party_slot_eq, ":center_no", slot_village_bound_center, "$demanded_castle"),
					(party_slot_ge, ":center_no", slot_town_lord, 1),
					(party_get_slot, reg0, ":center_no", slot_town_lord),
					(call_script, "script_change_player_relation_with_troop", reg0, -1),
				  (try_end),
			  ##Change next to use :player_faction instead of fac_player_supporters_faction
              (call_script, "script_give_center_to_faction", "$demanded_castle", ":player_faction"),
			  ##diplomacy end+
            (try_end),
            (try_begin),
              (gt, "$demanded_money", 0),
              (call_script, "script_dplmc_pay_into_treasury", "$demanded_money"),
			  ##diplomacy start+ other faction loses money
			  #Since setting terms for surrender is a non-native feature, there is no need to make this optional.
			  (faction_get_slot, ":faction_leader", "$g_notification_menu_var1", slot_faction_leader),
			  (try_begin),
				(ge, ":faction_leader", 1),
				(neq, "$g_notification_menu_var1", "$players_kingdom"),
				(neq, "$g_notification_menu_var1", "fac_player_supporters_faction"),
				(ge, "$demanded_money", 1),
				(assign, ":cost_to_leader", "$demanded_money"),
				#(try_begin),
				#	 (faction_get_slot, ":marshall", "$g_notification_menu_var1", slot_faction_marshall),
				#	 (neq, ":marshall", "trp_player"),
				#	 (neq, ":marshall", ":faction_leader"),
				#	 (ge, ":marshall", 0),
				#	 (store_troop_gold, reg0, ":marshall"),
				#	 (store_troop_gold, reg1, ":faction_leader"),
				#	 (val_add, reg1, reg0),
				#	 (gt, reg1, 0),
				#	 (store_mul, ":cost_to_marshall", "$demanded_money", reg0),
				#	 (val_div, ":cost_to_marshall", reg1),
				#	 (store_div, reg0, "$demanded_money", 2),
				#	 (val_min, ":cost_to_marshall", reg0),#no more than 1/2
				#	 (store_mul, reg0, "$demanded_money", 3),
				#	 (val_div, reg0, 13),#no less than 3/13 (6/26 marshall, 20/26 leader)
				#	 (val_max, ":cost_to_marshall", reg0),
				#	 (gt, ":cost_to_marshall", 0),
				#	 (call_script, "script_dplmc_remove_gold_from_lord_and_holdings", ":cost_to_marshall", ":marshall"),
				#	 (val_sub, ":cost_to_leader", ":cost_to_marshall"),
				#	 (store_random_in_range, reg0, 0, 1000),
				#	 (val_add, reg0, ":cost_to_marshall"),
				#	 (val_div, reg0, 1000),
				#	 (ge, reg0, 1),
				#	 (val_mul, reg0, -1),
				#	 (call_script, "script_change_player_relation_with_troop", ":marshall", reg0),
				#(try_end),
				(ge, ":cost_to_leader", 1),
				(call_script, "script_dplmc_remove_gold_from_lord_and_holdings", ":cost_to_leader", ":faction_leader"),
				(store_random_in_range, reg0, 0, 1000),
				(val_add, reg0, ":cost_to_leader"),
				(val_div, reg0, 1000),
				(ge, reg0, 1),
				(val_mul, reg0, -1),
				(call_script, "script_change_player_relation_with_troop", ":faction_leader", reg0),
			  (try_end),
			  ##diplomacy end+
            (try_end),
			##diplomacy start+
            (call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_notification_menu_var1", ":player_faction", 1),
			##diplomacy end+
            (presentation_set_duration, 0),
            (change_screen_return),
          (else_try),
            (jump_to_menu,"mnu_dplmc_deny_terms"),
          (try_end),

        (try_end),
    ]),
  ])
