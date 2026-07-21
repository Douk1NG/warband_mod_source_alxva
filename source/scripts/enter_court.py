# ======================================================================
# SHARED DEPENDENCY
# Entity: enter_court (script)
# Called by menus in 2 domains: siege, town
# ======================================================================

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

enter_court_scripts = [
("enter_court",
    [
      (store_script_param_1, ":center_no"),

      (assign, "$talk_context", tc_court_talk),

      (set_jump_mission,"mt_visit_town_castle"),

      (mission_tpl_entry_clear_override_items, "mt_visit_town_castle", 0),
      #(mission_tpl_entry_set_override_flags, "mt_visit_town_castle", 0, af_override_all),

      (mission_tpl_entry_set_override_flags, "mt_visit_town_castle", 0, af_override_all),
      (assign, ":dest_cloth", "itm_tabard"),
      (assign, ":have_civilian_cloth", 0),
      (assign, ":equipped_body_is_civilian", 0),
      (troop_get_inventory_slot, ":equipped_body", "trp_player", ek_body),
      (try_begin),
        (ge, ":equipped_body", 0),
        (item_has_property, ":equipped_body", itp_civilian),
        (assign, ":dest_cloth", ":equipped_body"),
        (assign, ":have_civilian_cloth", 1),
        (assign, ":equipped_body_is_civilian", 1),
      (else_try),
        (troop_get_inventory_capacity, ":inv_size", "trp_player"),
        (assign, ":end_cond", ":inv_size"),
        (try_for_range, ":i_slot", ek_head, ":end_cond"),
          (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
          (ge, ":item_id", 0),
          (item_get_type, ":i_type", ":item_id"),
          (eq, ":i_type", itp_type_body_armor),
          (item_has_property, ":item_id", itp_civilian),
          (assign, ":dest_cloth", ":item_id"),
          (assign, ":have_civilian_cloth", 1),
          (assign, ":end_cond", 0),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":equipped_body_is_civilian", 1),
      (else_try),
        (eq, ":have_civilian_cloth", 1),
        (display_message, "@You have changed into casual clothes from your inventory."),
      (else_try),
        (display_message, "@You have no casual clothes, so the castle guard provides common clothes temporarily."),
      (try_end),
      (mission_tpl_entry_add_override_item, "mt_visit_town_castle", 0, ":dest_cloth"),

      (party_get_slot, ":castle_scene", ":center_no", slot_town_castle),
      (modify_visitors_at_site,":castle_scene"),
      (reset_visitors),
      #Adding guards
      (store_faction_of_party, ":center_faction", ":center_no"),
      ##diplomacy begin
      (try_begin),
         (eq, ":center_faction", "$players_kingdom"),
         (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
         (faction_get_slot, ":guard_troop", "$g_player_culture", slot_faction_guard_troop),
	  ##nested diplomacy start+
	  (else_try),
	     #Reflect multicultural empires.
		 (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
		 (gt, ":town_lord", "trp_player"),
		 (troop_get_slot, ":lord_original_faction", ":town_lord", slot_troop_original_faction),
		 (neq, ":lord_original_faction", ":center_faction"),
		 (is_between, ":lord_original_faction", npc_kingdoms_begin, npc_kingdoms_end),
		 (this_or_next|party_slot_eq, ":center_no", slot_center_original_faction, ":lord_original_faction"),
			(troop_slot_eq, ":town_lord", slot_troop_home, ":center_no"),
		 (faction_get_slot, ":guard_troop", ":lord_original_faction", slot_faction_guard_troop),
	  ##nested diplomacy end+
      (else_try),
        (faction_get_slot, ":guard_troop", ":center_faction", slot_faction_guard_troop),
      (try_end),
      ##diplomacy end
      (try_begin),
        (le, ":guard_troop", 0),
		#diplomacy start+
		#rubik changes this in Custom Commander, and I agree: the "generic" guard
		#should be non-faction-specific.
		##OLD:
        #(assign, ":guard_troop", "trp_swadian_sergeant"),
		##NEW:
		(assign, ":guard_troop", "trp_hired_blade"),
		##diplomacy end+
      (try_end),
      (set_visitor, 6, ":guard_troop"),
      (set_visitor, 7, ":guard_troop"),

      (assign, ":cur_pos", 16),

	  (try_begin),
		(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
	    (gt, ":player_spouse", 0),
		(troop_slot_eq, ":player_spouse", slot_troop_cur_center, ":center_no"),
        (set_visitor, ":cur_pos", ":player_spouse"),
        (val_add,":cur_pos", 1),
	  (else_try),
		(troop_get_slot, ":player_betrothed", "trp_player", slot_troop_betrothed),
	    (gt, ":player_betrothed", 0),
		(troop_slot_eq, ":player_betrothed", slot_troop_cur_center, ":center_no"),
        (set_visitor, ":cur_pos", ":player_betrothed"),
        (val_add,":cur_pos", 1),
	  (try_end),

	  (try_begin),
		(eq, "$g_player_court", ":center_no"),
		(gt, "$g_player_minister", 0),
		(neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_player_minister"),
        (set_visitor, ":cur_pos", "$g_player_minister"),
        (val_add,":cur_pos", 1),
	  (try_end),
    ##diplomacy begin

    # (try_begin), #dckplmc seneschals
      # (call_script, "script_assign_seneschals"),
      # (party_get_slot, ":town_seneschal", ":center_no", slot_town_seneschal),
      # (gt, ":town_seneschal", -1),
      # (set_visitor, ":cur_pos", ":town_seneschal"),
      # (val_add,":cur_pos", 1),
    # (try_end),

    (try_begin),
      (gt, "$g_player_chamberlain", 0),
      (call_script, "script_dplmc_appoint_chamberlain"),  #fix for wrong troops after update
      (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
      (eq, ":town_lord", "trp_player"),
      (set_visitor, ":cur_pos", "$g_player_chamberlain"),
      (val_add,":cur_pos", 1),
    (try_end),

    (try_begin),
      (gt, "$g_player_constable", 0),
      (call_script, "script_dplmc_appoint_constable"),  #fix for wrong troops after update
      (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
      (eq, ":town_lord", "trp_player"),
      (set_visitor, ":cur_pos", "$g_player_constable"),
      (val_add,":cur_pos", 1),
    (try_end),

    (try_begin),
      (gt, "$g_player_chancellor", 0),
      (call_script, "script_dplmc_appoint_chancellor"), #fix for wrong troops after update
      (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
      (eq, ":town_lord", "trp_player"),
      (set_visitor, ":cur_pos", "$g_player_chancellor"),
      (val_add,":cur_pos", 1),
    (try_end),
    ##diplomacy end

      #Lords wishing to pledge allegiance - inactive, but part of player faction
      #SB : move down to sorted script call
	  (try_begin),
		(eq, "$g_player_court", ":center_no"),
	    (faction_slot_eq, ":center_faction", slot_faction_leader, "trp_player"),
	    (try_for_range, ":active_npc", heroes_begin, heroes_end), #support for upgraded kingdom ladies
	      (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
	      (eq, ":active_npc_faction", "fac_player_supporters_faction"),
	      (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_inactive),
	      (neg|troop_slot_ge, ":active_npc", slot_troop_prisoner_of_party, 0), #if he/she is not prisoner in any center.
	      (neq, ":active_npc", "$g_player_minister"),
	      (set_visitor, ":cur_pos", ":active_npc"),
	      (val_add,":cur_pos", 1),
		(try_end),
	  (try_end),

      ##diplomacy start+
      #Show heroes you haven't seen recently first, to deal with crowded feast halls
      #(call_script, "script_get_heroes_attached_to_center", ":center_no", "p_temp_party"),
      (call_script, "script_dplmc_time_sorted_heroes_for_center", ":center_no", "p_temp_party"),
	  #Reserve a certain number of feast positions for ladies, both for practical
	  #reasons of courtship and for visual variety.
	  (try_begin),
		#If the player is unmarried, reserve zero to 8 slots for women
		(lt, ":player_spouse", 1),
		(store_random_in_range, ":reserved", 0, 9),
	  (else_try),
		#If the player is married, reserve zero to four slots for women
		(store_random_in_range, ":reserved", 0, 5),
	  (try_end),
	  (store_sub, ":non_lady_max", 32, ":reserved"),
      #diplomacy end+
      (party_get_num_companion_stacks, ":num_stacks","p_temp_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop","p_temp_party",":i_stack"),
		##diplomacy start+
        #(lt, ":cur_pos", 32), # spawn up to entry point 32 - is it possible to add another 10 spots?
		(lt, ":cur_pos", ":non_lady_max"),#Leave some room for ladies in huge feasts
		##diplomacy end+
        (set_visitor, ":cur_pos", ":stack_troop"),
        (val_add,":cur_pos", 1),
      (try_end),
      (try_for_range, ":cur_troop", kingdom_ladies_begin, kingdom_ladies_end),
        (neq, ":cur_troop", "trp_knight_1_1_wife"), #The one who should not appear in game
        #(troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_lady),
        (troop_slot_eq, ":cur_troop", slot_troop_cur_center, ":center_no"),

        (assign, ":lady_meets_visitors", 0),
		(assign, ":tribute_entertainer", 0),
        (try_begin),
            (this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":cur_troop"), #player spouse goes in position of honor
            (troop_slot_eq, "trp_player", slot_troop_betrothed, ":cur_troop"), #player spouse goes in position of honor
            (assign, ":lady_meets_visitors", 0), #She is already in the place of honor
            (try_begin), #SB : primary spouse
                (eq, "$cheat_mode", 1),
                (str_store_troop_name, s4, ":cur_troop"),
                (display_message, "str_s4_is_present_at_the_center_and_in_place_of_honor"),
            (try_end),
        (else_try),
            (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_spouse, "trp_player"), #player spouse goes in position of honor
            (troop_slot_eq, ":cur_troop", slot_troop_betrothed, "trp_player"),
            (assign, ":lady_meets_visitors", 1),
            (try_begin), #SB : secondary spouse, normally shadowed due to above behaviour
                (eq, "$cheat_mode", 1),
                (str_store_troop_name, s4, ":cur_troop"),
                (display_message, "str_s4_is_present_at_the_center_and_is_married"),
            (try_end),
        (else_try), #lady is troop
            (store_faction_of_troop, ":lady_faction", ":cur_troop"),
            (neq, ":lady_faction", ":center_faction"),

            (assign, ":lady_meets_visitors", 1),


            (try_begin),
                (eq, "$cheat_mode", 1),
                (str_store_troop_name, s4, ":cur_troop"),
                (try_begin), #SB : distinguish between refugee and prisoner
                  (troop_slot_eq, ":cur_troop", slot_troop_prisoner_of_party, ":center_no"),
                  (display_message, "@{s4} is present at the center as a prisoner"),
				  #Prisoner Entertainer
				  (assign, ":lady_meets_visitors", 1),
                (else_try),
                  (display_message, "str_s4_is_present_at_the_center_as_a_refugee"),
                (try_end),
            (try_end),

        (else_try),
            (troop_slot_ge, ":cur_troop", slot_troop_spouse, 1),

            (try_begin),
             #married ladies at a feast will not mingle - this is ahistorical, as married women and widows probably had much more freedom than unmarried ones, at least in the West, but the game needs to leave slots for them to show off their unmarried daughters
                (faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
                (faction_slot_eq, ":center_faction", slot_faction_ai_object, ":center_no"),
                (assign, ":lady_meets_visitors", 0),

                (try_begin),
                    (eq, "$cheat_mode", 1),
                    (str_store_troop_name, s4, ":cur_troop"),
                    (display_message, "str_s4_is_present_at_the_center_and_not_attending_the_feast"),
                (try_end),
            (else_try),
                (assign, ":lady_meets_visitors", 1),

                (try_begin),
                    (eq, "$cheat_mode", 1),
                    (str_store_troop_name, s4, ":cur_troop"),
                    (display_message, "str_s4_is_present_at_the_center_and_is_married"),
                (try_end),
            (try_end),

		(else_try), #feast is in progress
			(faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
			(faction_slot_eq, ":center_faction", slot_faction_ai_object, ":center_no"),
			(assign, ":lady_meets_visitors", 1),

			(try_begin),
				(store_random_in_range,":r",1,8),
				(eq,":r", 3),
				(assign, ":tribute_entertainer", 1),
			(try_end),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":cur_troop"),
				(display_message, "@{!}DEBUG -- {s4} is present at the center and is attending the feast"),
			(try_end),

		(else_try), #already met - awaits in private
			(troop_slot_ge, ":cur_troop", slot_troop_met, 2),
			(assign, ":lady_meets_visitors", 0),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":cur_troop"),
				(display_message, "@{!}DEBUG -- {s4} is present at the center and is awaiting the player in private"),
			(try_end),

		(else_try),
			(call_script, "script_get_kingdom_lady_social_determinants", ":cur_troop"),
			(call_script, "script_npc_decision_checklist_male_guardian_assess_suitor", reg0, "trp_player"),
			(gt, reg0, 0),
			(assign, ":lady_meets_visitors", 1),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":cur_troop"),
				(display_message, "@{!}DEBUG -- {s4} is_present_at_the_center_and_is_allowed_to_meet_the_player"),
			(try_end),

		(else_try),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":cur_troop"),
				(display_message, "@{!}DEBUG -- {s4}is_present_at_the_center_and_is_not_allowed_to_meet_the_player"),
			(try_end),

		(try_end),

		(eq, ":lady_meets_visitors", 1),

		(try_begin),
			(eq, ":tribute_entertainer", 1),
			(try_begin),
				(eq, "$tep_entertainer1", 69),
				(assign, "$tep_entertainer1", ":cur_troop"),
			(else_try),
				(eq, "$tep_entertainer2", 69),
				(assign, "$tep_entertainer2", ":cur_troop"),
			(else_try),
				(eq, "$tep_entertainer3", 69),
				(assign, "$tep_entertainer3", ":cur_troop"),
			(else_try),
				(eq, "$tep_entertainer4", 69),
				(assign, "$tep_entertainer4", ":cur_troop"),
			(else_try),
				(assign, ":tribute_entertainer", 0),
		(try_end),
			#(troop_set_slot, ":cur_troop", slot_troop_entertainer, 1), Now used for permanently abused ladies
		(try_end),

        (lt, ":cur_pos", 32), # spawn up to entry point 32
        (set_visitor, ":cur_pos", ":cur_troop"),
        (val_add,":cur_pos", 1),
      (try_end),

      (set_jump_entry, 0),

      (jump_to_scene,":castle_scene"),
      (scene_set_slot, ":castle_scene", slot_scene_visited, 1),
      (change_screen_mission),
  ])
]
