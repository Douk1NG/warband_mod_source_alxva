# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

battle_results_menus = [
  (
    "battle_debrief",mnf_scale_picture|mnf_disable_all_keys,
    "{s11}^^Your Casualties:{s8}{s10}^^Enemy Casualties:{s9}",
    "none",
    [
     (try_begin),
       (eq, "$g_battle_result", 1),
       (call_script, "script_change_troop_renown", "trp_player", "$battle_renown_value"),
       #SB : also distribute amount to companions, maybe pretender/spouse in party as well
       (assign, ":amount", 0),
       (try_for_range, ":companions", companions_begin, companions_end),
         (main_party_has_troop, ":companions"),
         (val_add, ":amount", 1),
       (try_end),
       (try_begin),
         (gt, ":amount", 0),
         (store_div, ":amount", "$battle_renown_value", ":amount"),
         (val_max, ":amount", dplmc_companion_battle_renown),
         (try_for_range, ":companions", companions_begin, companions_end),
           (main_party_has_troop, ":companions"),
           # (neg|troop_is_wounded, ":companions"), #survived, or stayed at the back
           (call_script, "script_change_troop_renown", ":companions", ":amount"),
         (try_end),
       (try_end),

       (try_begin),
         (ge, "$g_encountered_party", 0),
         (party_is_active, "$g_encountered_party"),
         (party_get_template_id, ":encountered_party_template", "$g_encountered_party"),
         (eq, ":encountered_party_template", "pt_kingdom_caravan_party"),

         (get_achievement_stat, ":number_of_village_raids", ACHIEVEMENT_THE_BANDIT, 0),
         (get_achievement_stat, ":number_of_caravan_raids", ACHIEVEMENT_THE_BANDIT, 1),
         (val_add, ":number_of_caravan_raids", 1),
         (set_achievement_stat, ACHIEVEMENT_THE_BANDIT, 1, ":number_of_caravan_raids"),

         (try_begin),
           (ge, ":number_of_village_raids", 3),
           (ge, ":number_of_caravan_raids", 3),
           (unlock_achievement, ACHIEVEMENT_THE_BANDIT),
         (try_end),
       (try_end),

       (try_begin),
         (party_get_current_terrain, ":cur_terrain", "p_main_party"),
         (eq, ":cur_terrain", rt_snow),
         (get_achievement_stat, ":number_of_victories_at_snowy_lands", ACHIEVEMENT_BEST_SERVED_COLD, 0),
         (val_add, ":number_of_victories_at_snowy_lands", 1),
         (set_achievement_stat, ACHIEVEMENT_BEST_SERVED_COLD, 0, ":number_of_victories_at_snowy_lands"),

         (try_begin),
           (eq, ":number_of_victories_at_snowy_lands", 10),
           (unlock_achievement, ACHIEVEMENT_BEST_SERVED_COLD),
         (try_end),
       (try_end),

       (try_begin),
         (ge, "$g_enemy_party", 0),
         (party_is_active, "$g_enemy_party"),
         (party_stack_get_troop_id, ":stack_troop", "$g_enemy_party", 0),
         (eq, ":stack_troop", "trp_mountain_bandit"),

         (get_achievement_stat, ":number_of_victories_aganist_mountain_bandits", ACHIEVEMENT_MOUNTAIN_BLADE, 0),
         (val_add, ":number_of_victories_aganist_mountain_bandits", 1),
         (set_achievement_stat, ACHIEVEMENT_MOUNTAIN_BLADE, 0, ":number_of_victories_aganist_mountain_bandits"),

         (try_begin),
           (eq, ":number_of_victories_aganist_mountain_bandits", 10),
           (unlock_achievement, ACHIEVEMENT_MOUNTAIN_BLADE),
         (try_end),
       (try_end),

       (try_begin),
         (is_between, "$g_ally_party", walled_centers_begin, walled_centers_end),
         (unlock_achievement, ACHIEVEMENT_NONE_SHALL_PASS),
       (try_end),

       (try_begin),
         (eq, "$g_joined_battle_to_help", 1),
         (unlock_achievement, ACHIEVEMENT_GOOD_SAMARITAN),
       (try_end),
     (try_end),

     (assign, "$g_joined_battle_to_help", 0),
     (call_script, "script_count_casualties_and_adjust_morale"),#new
     (call_script, "script_encounter_calculate_fit"),

     (call_script, "script_party_count_fit_regulars", "p_main_party"),
     (assign, "$playerparty_postbattle_regulars", reg0),

     (try_begin),
       (eq, "$g_battle_result", 1),
       (eq, "$g_enemy_fit_for_battle", 0),
       (str_store_string, s11, "@You were victorious!"),
#       (play_track, "track_bogus"), #clear current track.
#       (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
       (try_begin),
         (gt, "$g_friend_fit_for_battle", 1),
         (set_background_mesh, "mesh_pic_victory"),
       (try_end),
     (else_try),
       (eq, "$g_battle_result", -1),
       (ge, "$g_enemy_fit_for_battle",1),
       (this_or_next|le, "$g_friend_fit_for_battle",0),
       (le, "$playerparty_postbattle_regulars", 0),
       (str_store_string, s11, "@The battle was lost. Your forces were utterly crushed."), #SB : "The battle"
       (set_background_mesh, "mesh_pic_defeat"),
     (else_try),
       (eq, "$g_battle_result", -1),
       (str_store_string, s11, "@Your companions carry you away from the fighting."),
		 ##diplomacy start+ Test gender with script
       #(troop_get_type, ":is_female", "trp_player"),#<- replaced
       (try_begin),
         #(eq, ":is_female", 1),#<- replaced
         (eq, tf_female, "$character_gender"),#<- added
         (set_background_mesh, "mesh_pic_wounded_fem"),
       (else_try),
         (set_background_mesh, "mesh_pic_wounded"),
       (try_end),
		 ##diplomacy end+
     (else_try),
       (eq, "$g_battle_result", 1),
       (str_store_string, s11, "@You have defeated the enemy."),
       (try_begin),
         (gt, "$g_friend_fit_for_battle", 1),
         (set_background_mesh, "mesh_pic_victory"),
       (try_end),
     (else_try),
       (eq, "$g_battle_result", 0),
       (str_store_string, s11, "@You have retreated from the fight."),
     (try_end),
#NPC companion changes begin
##check for excessive casualties, more forgiving if battle result is good
     (try_begin),
        (gt, "$playerparty_prebattle_regulars", 9),
        (store_add, ":divisor", 3, "$g_battle_result"),
        (store_div, ":half_of_prebattle_regulars", "$playerparty_prebattle_regulars", ":divisor"),
        (lt, "$playerparty_postbattle_regulars", ":half_of_prebattle_regulars"),
        (call_script, "script_objectionable_action", tmt_egalitarian, "str_excessive_casualties"),
     (try_end),
#NPC companion changes end

     (call_script, "script_print_casualties_to_s0", "p_player_casualties", 0),
     (str_store_string_reg, s8, s0),
     (call_script, "script_print_casualties_to_s0", "p_enemy_casualties", 0),
     (str_store_string_reg, s9, s0),
     (str_clear, s10),
     (try_begin),
       (eq, "$any_allies_at_the_last_battle", 1),
       (call_script, "script_print_casualties_to_s0", "p_ally_casualties", 0),
       (str_store_string, s10, "@^^Ally Casualties:{s0}"),
     (try_end),
     ],
    [
      ("continue",[],"Continue...",[(jump_to_menu, "$g_next_menu"),]),
    ]
  ),
  (
    "total_victory", 0,
    "You shouldn't be reading this... {s9}",
    "none",
    [
        # We exploit the menu condition system below.
        # The conditions should make sure that always another screen or menu is called.
        (assign, ":break", 0),
        (try_begin),
          (eq, "$routed_party_added", 0), #new
          (assign, "$routed_party_added", 1),

           #add new party to map (routed_warriors)
          (call_script, "script_add_routed_party"),
        (try_end),

		(try_begin),
			(check_quest_active, "qst_track_down_bandits"),
			(neg|check_quest_succeeded, "qst_track_down_bandits"),
			(neg|check_quest_failed, "qst_track_down_bandits"),

			(quest_get_slot, ":quest_party", "qst_track_down_bandits", slot_quest_target_party),
			(party_is_active, ":quest_party"),
			(party_get_attached_to, ":quest_party_attached"),
			(this_or_next|eq, ":quest_party", "$g_enemy_party"),
				(eq, ":quest_party_attached", "$g_enemy_party"),
			(call_script, "script_succeed_quest", "qst_track_down_bandits"),
		(try_end),

		(try_begin),
			(gt, "$g_private_battle_with_troop", 0),
			(troop_slot_eq, "$g_private_battle_with_troop", slot_troop_leaded_party, "$g_encountered_party"),
			(assign, "$g_private_battle_with_troop", 0),
			##diplomacy start+
			#g_disable_condescending_comments is also used to track the "enhanced/diminished prejudice" setting
			(try_begin),
				(eq, "$g_disable_condescending_comments", 0),
				(assign, "$g_disable_condescending_comments", 1),
			(else_try),
				(eq, "$g_disable_condescending_comments", 2),
				(assign, "$g_disable_condescending_comments", 3),
			##diplomacy end+
			(try_end),
		(try_end),

        #new - begin
        (party_get_num_companion_stacks, ":num_stacks", "p_collective_enemy"),
        (try_for_range, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":stack_troop", "p_collective_enemy", ":i_stack"),
          ###(((add wounded kings to p_total_enemy_casualties FIX
          (is_between, ":stack_troop", active_npcs_begin, active_npcs_end),
          ###)))
          (troop_is_wounded, ":stack_troop"),
          (party_add_members, "p_total_enemy_casualties", ":stack_troop", 1),
        (try_end),
        #new - end

        (try_begin),
          # Talk to ally leader
          (eq, "$thanked_by_ally_leader", 0),
          (assign, "$thanked_by_ally_leader", 1),

          (gt, "$g_ally_party", 0),
          #(store_add, ":total_str_without_player", "$g_starting_strength_ally_party", "$g_starting_strength_enemy_party"),

          (store_add, ":total_str_without_player", "$g_starting_strength_friends", "$g_starting_strength_enemy_party"),
          (val_sub, ":total_str_without_player", "$g_starting_strength_main_party"),

          (store_sub, ":ally_strength_without_player", "$g_starting_strength_friends", "$g_starting_strength_main_party"),

          (store_mul, ":ally_advantage", ":ally_strength_without_player", 100),
          (val_add, ":total_str_without_player", 1),
          (val_div, ":ally_advantage", ":total_str_without_player"),
          #Ally advantage=50  means battle was evenly matched

          (store_sub, ":enemy_advantage", 100, ":ally_advantage"),

          (store_mul, ":faction_reln_boost", ":enemy_advantage", "$g_starting_strength_enemy_party"),
          (val_div, ":faction_reln_boost", 3000),
          (val_min, ":faction_reln_boost", 4),

          (store_mul, "$g_relation_boost", ":enemy_advantage", ":enemy_advantage"),
          (val_div, "$g_relation_boost", 700),
          (val_clamp, "$g_relation_boost", 0, 20),

          (party_get_num_companion_stacks, ":num_ally_stacks", "$g_ally_party"),
          (gt, ":num_ally_stacks", 0),
          (store_faction_of_party, ":ally_faction","$g_ally_party"),
          (call_script, "script_change_player_relation_with_faction", ":ally_faction", ":faction_reln_boost"),
          (party_stack_get_troop_id, ":ally_leader", "$g_ally_party"),
          (party_stack_get_troop_dna, ":ally_leader_dna", "$g_ally_party", 0),
          (try_begin),
            (troop_is_hero, ":ally_leader"),
            (troop_get_slot, ":hero_relation", ":ally_leader", slot_troop_player_relation),
            (assign, ":rel_boost", "$g_relation_boost"),
            (try_begin),
              (lt, ":hero_relation", -5),
              (val_div, ":rel_boost", 3),
            (try_end),
            (call_script,"script_change_player_relation_with_troop", ":ally_leader", ":rel_boost"),
          (try_end),
          (assign, "$talk_context", tc_ally_thanks),
          (call_script, "script_setup_troop_meeting", ":ally_leader", ":ally_leader_dna"),
        (else_try),
          # Talk to enemy leaders
          (assign, ":break", 0),

          (party_get_num_companion_stacks, ":num_stacks", "p_total_enemy_casualties"), #p_encountered changed to total_enemy_casualties
          (try_for_range, ":stack_no", "$last_defeated_hero", ":num_stacks"), #May 31 bug note -- this now returns some heroes in victorious party as well as in the other party
            (eq, ":break", 0),
            (party_stack_get_troop_id, ":stack_troop", "p_total_enemy_casualties", ":stack_no"),
            (party_stack_get_troop_dna, ":stack_troop_dna", "p_total_enemy_casualties", ":stack_no"),

            (troop_is_hero, ":stack_troop"),

            (store_troop_faction, ":defeated_faction", ":stack_troop"),
            #steve post 0912 changes begin - removed, this is duplicated elsewhere in game menus
            #(call_script, "script_add_log_entry", logent_lord_defeated_by_player, "trp_player",  -1, ":stack_troop", ":defeated_faction"),
            (try_begin),
   			  (store_relation, ":relation", ":defeated_faction", "fac_player_faction"),
			  (ge, ":relation", 0),
			  (str_store_troop_name, s4, ":stack_troop"),

			  (try_begin),
				(eq, "$cheat_mode", 1),
				(display_message, "@{!}{s4} skipped in p_total_enemy_casualties capture queue because is friendly"),
			  (try_end),
			(else_try),
              (try_begin),
                (party_stack_get_troop_id, ":party_leader", "$g_encountered_party", 0),
                (is_between, ":party_leader", active_npcs_begin, active_npcs_end),
                (troop_slot_eq, ":party_leader", slot_troop_occupation, slto_kingdom_hero),
                (store_sub, ":kingdom_hero_id", ":party_leader", active_npcs_begin),
                (get_achievement_stat, ":was_he_defeated_player_before", ACHIEVEMENT_BARON_GOT_BACK, ":kingdom_hero_id"),
                (eq, ":was_he_defeated_player_before", 1),

                (unlock_achievement, ACHIEVEMENT_BARON_GOT_BACK),
              (try_end),

              (store_add, "$last_defeated_hero", ":stack_no", 1),
              (call_script, "script_remove_troop_from_prison", ":stack_troop"),
              (troop_set_slot, ":stack_troop", slot_troop_leaded_party, -1),

              (call_script, "script_cf_check_hero_can_escape_from_player", ":stack_troop"),

              (str_store_troop_name, s1, ":stack_troop"),
              (str_store_faction_name, s3, ":defeated_faction"),
              (str_store_string, s17, "@{s1} of {s3} managed to escape."),
              (display_log_message, "@{!}{s17}"),
              (jump_to_menu, "mnu_enemy_slipped_away"),
              (assign, ":break", 1),
			(else_try),
              (store_add, "$last_defeated_hero", ":stack_no", 1),
              (call_script, "script_remove_troop_from_prison", ":stack_troop"),
              (troop_set_slot, ":stack_troop", slot_troop_leaded_party, -1),

              (assign, "$talk_context", tc_hero_defeated),

              (call_script, "script_setup_troop_meeting", ":stack_troop", ":stack_troop_dna"),
              (assign, ":break", 1),
            (try_end),
          (try_end),

          (eq, ":break", 1),
        (else_try),
          # Talk to freed heroes
          (assign, ":break", 0),
          (party_get_num_prisoner_stacks, ":num_prisoner_stacks", "p_collective_enemy"),
          (try_for_range, ":stack_no", "$last_freed_hero", ":num_prisoner_stacks"),
            (eq, ":break", 0),
            (party_prisoner_stack_get_troop_id, ":stack_troop", "p_collective_enemy", ":stack_no"),
            (troop_is_hero, ":stack_troop"),
            (party_prisoner_stack_get_troop_dna, ":stack_troop_dna", "p_collective_enemy", ":stack_no"),
            (store_add, "$last_freed_hero", ":stack_no", 1),
            (assign, "$talk_context", tc_hero_freed),
            (call_script, "script_setup_troop_meeting", ":stack_troop", ":stack_troop_dna"),
            (assign, ":break", 1),
          (try_end),
          (eq, ":break", 1),
        (else_try),
          (eq, "$capture_screen_shown", 0),
          (assign, "$capture_screen_shown", 1),
          (party_clear, "p_temp_party"),
          (assign, "$g_move_heroes", 0),
          #(call_script, "script_party_prisoners_add_party_companions", "p_temp_party", "p_collective_enemy"),

          #p_total_enemy_casualties deki yarali askerler p_temp_party'e prisoner olarak eklenecek.
          (call_script, "script_party_add_wounded_members_as_prisoners", "p_temp_party", "p_total_enemy_casualties"),

          (call_script, "script_party_add_party_prisoners", "p_temp_party", "p_collective_enemy"),
          (try_begin),
            (call_script, "script_party_calculate_strength", "p_collective_friends_backup",0),
            (assign,":total_initial_strength", reg(0)),
            (gt, ":total_initial_strength", 0),
            #(gt, "$g_ally_party", 0),
            (call_script, "script_party_calculate_strength", "p_main_party_backup",0),
            (assign,":player_party_initial_strength", reg(0)),
            # move ally_party_initial_strength/(player_party_initial_strength + ally_party_initial_strength) prisoners to ally party.
            # First we collect the share of prisoners of the ally party and distribute those among the allies.
            (store_sub, ":ally_party_initial_strength", ":total_initial_strength", ":player_party_initial_strength"),

            #(call_script, "script_party_calculate_strength", "p_ally_party_backup"),
            #(assign,":ally_party_initial_strength", reg(0)),
            #(store_add, ":total_initial_strength", ":player_party_initial_strength", ":ally_party_initial_strength"),
            (store_mul, ":ally_share", ":ally_party_initial_strength", 1000),
            (val_div, ":ally_share", ":total_initial_strength"),
            (assign, "$pin_number", ":ally_share"), #we send this as a parameter to the script.
            (party_clear, "p_temp_party_2"),
            (call_script, "script_move_members_with_ratio", "p_temp_party", "p_temp_party_2"),

            #TODO: This doesn't handle prisoners if our allies joined battle after us.
            (try_begin),
              (gt, "$g_ally_party", 0),
              (distribute_party_among_party_group, "p_temp_party_2", "$g_ally_party"),
            (try_end),
            #next if there's anything left, we'll open up the party exchange screen and offer them to the player.
          (try_end),
          (party_get_num_companions, ":num_rescued_prisoners", "p_temp_party"),
          (party_get_num_prisoners,  ":num_captured_enemies", "p_temp_party"),

          (store_add, ":total_capture_size", ":num_rescued_prisoners", ":num_captured_enemies"),

          (gt, ":total_capture_size", 0),

          ###(((auto_take_captured_enemies (always on)
          (try_begin),
            (gt, ":num_captured_enemies", 0),
            (call_script, "script_party_prisoners_add_party_prisoners", "p_temp_party", "p_main_party"),
            (call_script, "script_party_remove_all_prisoners", "p_main_party"),

            (party_get_free_prisoners_capacity, ":free_prisoners_capacity", "p_main_party"),
            (gt, ":free_prisoners_capacity", 0),
            (try_begin),
              (check_quest_active, "qst_follow_spy"),
              (party_count_prisoners_of_type, ":num_spies", "p_temp_party", "trp_spy"),
              (party_count_prisoners_of_type, ":num_spy_partners", "p_temp_party", "trp_spy_partner"),
              (try_begin),
                (gt, ":num_spies", 0),
                (party_remove_prisoners, "p_temp_party", "trp_spy", 1),
                (party_add_prisoners, "p_main_party", "trp_spy", 1),
                (val_sub, ":free_prisoners_capacity", 1),
              (try_end),
              (gt, ":free_prisoners_capacity", 0),
              (try_begin),
                (gt, ":num_spy_partners", 0),
                (party_remove_prisoners, "p_temp_party", "trp_spy_partner", 1),
                (party_add_prisoners, "p_main_party", "trp_spy_partner", 1),
                (val_sub, ":free_prisoners_capacity", 1),
              (try_end),
            (try_end),

            (gt, ":free_prisoners_capacity", 0),
            (try_begin),
              (check_quest_active, "qst_capture_prisoners"),
              (quest_get_slot, ":quest_target_amount", "qst_capture_prisoners", slot_quest_target_amount),
              (quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
              (party_count_prisoners_of_type, ":num_target_troop", "p_temp_party", ":quest_target_troop"),
              (gt, ":num_target_troop", 0),
              (val_min, ":num_target_troop", ":quest_target_amount"),
              (val_min, ":num_target_troop", ":free_prisoners_capacity"),
              (party_remove_prisoners, "p_temp_party", ":quest_target_troop", ":num_target_troop"),
              (party_add_prisoners, "p_main_party", ":quest_target_troop", ":num_target_troop"),
              (val_sub, ":free_prisoners_capacity", ":num_target_troop"),
            (try_end),

            # auto-return prisoners to p_main_party by prisoner' level as many as possible
            (gt, ":free_prisoners_capacity", 0),
            (party_get_num_prisoner_stacks, ":num_prisoner_stacks", "p_temp_party"),
            (assign, ":end_cond", ":num_prisoner_stacks"),
            (try_for_range, ":unused", 0, ":end_cond"),
              (assign, ":best_stack", -1),
              (assign, ":best_level", -1),
              (party_get_num_prisoner_stacks, ":num_stacks", "p_temp_party"),
              (try_for_range, ":cur_stack", 0, ":num_stacks"),
                (party_prisoner_stack_get_troop_id, ":prisoner_troop", "p_temp_party", ":cur_stack"),
                (store_character_level, ":cur_level", ":prisoner_troop"),
                (gt, ":cur_level", ":best_level"),
                (assign, ":best_stack", ":cur_stack"),
                (assign, ":best_level", ":cur_level"),
              (try_end),
              (gt, ":best_stack", -1),
              (party_prisoner_stack_get_troop_id, ":best_prisoner", "p_temp_party", ":best_stack"),
              (party_prisoner_stack_get_size, ":stack_size", "p_temp_party", ":best_stack"),
              (val_min, ":stack_size", ":free_prisoners_capacity"),
              (party_remove_prisoners, "p_temp_party", ":best_prisoner", ":stack_size"),
              (party_add_prisoners, "p_main_party", ":best_prisoner", ":stack_size"),
              (val_sub, ":free_prisoners_capacity", ":stack_size"),
              (le, ":free_prisoners_capacity", 0),
              (assign, ":end_cond", 0),
            (try_end),
          (try_end),
          ###)))

          (troop_set_slot, "trp_temp_array_d", slot_adv_transfer_mode, 10),
          (change_screen_exchange_with_party, "p_temp_party"),
        (else_try),
          (eq, "$loot_screen_shown", 0),
          (assign, "$loot_screen_shown", 1),
#          (try_begin),
#            (gt, "$g_ally_party", 0),
#            (call_script, "script_party_add_party", "$g_ally_party", "p_temp_party"), #Add remaining prisoners to ally TODO: FIX it.
#          (else_try),
#            (party_get_num_attached_parties, ":num_quick_attachments", "p_main_party"),
#            (gt, ":num_quick_attachments", 0),
#            (party_get_attached_party_with_rank, ":helper_party", "p_main_party", 0),
#            (call_script, "script_party_add_party", ":helper_party", "p_temp_party"), #Add remaining prisoners to our reinforcements
#          (try_end),
          (troop_clear_inventory, "trp_temp_troop"),
          (call_script, "script_party_calculate_loot", "p_total_enemy_casualties"), #p_encountered_party_backup changed to total_enemy_casualties
          (gt, reg0, 0),
          (troop_sort_inventory, "trp_temp_troop"),
		  ##diplomacy start+
		  #Here: we jump to rubik's autoloot from CC if applicable instead of using the standard loot screen
		  (try_begin),
			(call_script, "script_cf_dplmc_player_party_meets_autoloot_conditions"),
			(assign, "$dplmc_return_menu", "mnu_total_victory"),
			(assign, "$lord_selected", "trp_player"),
			(jump_to_menu, "mnu_dplmc_manage_loot_pool"),
		  (else_try),
			#Old behavior:
			(change_screen_loot, "trp_temp_troop"),
		  (try_end),
		  ##diplomacy end+
        (else_try),
          #finished all
          (try_begin),
            (le, "$g_ally_party", 0),
            (end_current_battle),
          (try_end),
          (call_script, "script_party_give_xp_and_gold", "p_total_enemy_casualties"), #p_encountered_party_backup changed to total_enemy_casualties
          (try_begin),
            (eq, "$g_enemy_party", 0),
            (display_message,"str_error_string"),
          (try_end),

		  (try_begin),
		    (party_is_active, "$g_ally_party"),
			(call_script, "script_battle_political_consequences", "$g_enemy_party", "$g_ally_party"),
		  (else_try),
			(call_script, "script_battle_political_consequences", "$g_enemy_party", "p_main_party"),
		  (try_end),

          (call_script, "script_event_player_defeated_enemy_party", "$g_enemy_party"),
          (call_script, "script_clear_party_group", "$g_enemy_party"),
          (try_begin),
            (eq, "$g_next_menu", -1),

            #NPC companion changes begin
            (call_script, "script_post_battle_personality_clash_check"),
            #NPC companion changes end

            #Post 0907 changes begin
            (party_stack_get_troop_id, ":enemy_leader", "p_encountered_party_backup",0),
            (try_begin),
              (is_between, ":enemy_leader", active_npcs_begin, active_npcs_end),
              (neg|is_between, "$g_encountered_party", centers_begin, centers_end),
              (store_troop_faction, ":enemy_leader_faction", ":enemy_leader"),

              (try_begin),
                (eq, "$g_ally_party", 0),
                (call_script, "script_add_log_entry", logent_lord_defeated_by_player, "trp_player",  -1, ":enemy_leader", ":enemy_leader_faction"),
                (try_begin),
                  (eq, "$cheat_mode", 1),
                  (display_message, "@{!}Victory comment. Player was alone"),
                (try_end),
              (else_try),
                (ge, "$g_strength_contribution_of_player", 40),
                (call_script, "script_add_log_entry", logent_lord_defeated_by_player, "trp_player",  -1, ":enemy_leader", ":enemy_leader_faction"),
                (try_begin),
                  (eq, "$cheat_mode", 1),
                  (display_message, "@{!}Ordinary victory comment. The player provided at least 40 percent forces."),
                (try_end),
              (else_try),
                (gt, "$g_starting_strength_enemy_party", 1000),
                (call_script, "script_get_closest_center", "p_main_party"),
                (assign, ":battle_of_where", reg0),
                (call_script, "script_add_log_entry", logent_player_participated_in_major_battle, "trp_player",  ":battle_of_where", -1, ":enemy_leader_faction"),
                (call_script, "script_change_player_relation_with_lords_after_battle"),
                (try_begin),
                  (eq, "$cheat_mode", 1),
                  (display_message, "@{!}Player participation comment. The enemy had at least 1k starting strength."),
                (try_end),
              (else_try),
                (eq, "$cheat_mode", 1),
                (display_message, "@{!}No victory comment. The battle was small, and the player provided less than 40 percent of allied strength"),
              (try_end),
            (try_end),
            #Post 0907 changes end
            (val_add, "$g_total_victories", 1),
            (leave_encounter),
            (change_screen_return),
          (else_try),
            (try_begin), #my kingdom
            ##diplomacy begin
              (eq, "$g_next_menu", "mnu_dplmc_town_riot_removed"),
              (jump_to_menu, "$g_next_menu"),
            (else_try),
            ##diplomacy end
              #(change_screen_return),
              (eq, "$g_next_menu", "mnu_castle_taken"),

              (call_script, "script_add_log_entry", logent_castle_captured_by_player, "trp_player", "$g_encountered_party", -1, "$g_encountered_party_faction"),
              (call_script, "script_change_player_relation_with_lords_after_battle"),
              (store_current_hours, ":hours"),
			  (faction_set_slot, "$players_kingdom", slot_faction_ai_last_decisive_event, ":hours"),

              (try_begin), #player took a walled center while he is a vassal of npc kingdom.
  			  ##diplomacy start+ Handle player is co-ruler of NPC faction
				(assign, ":is_coruler", 0),
                (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
                (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
                (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
				(assign, ":is_coruler", 1),

				(assign, "$g_center_taken_by_player_faction", "$g_encountered_party"),
				(faction_get_slot, ":faction_leader", "fac_player_supporters_faction", slot_faction_leader),
				(try_begin),
					(eq, ":faction_leader", "trp_player"),
					(assign, ":faction_leader", heroes_end),
					(try_for_range, ":troop_no", heroes_begin, ":faction_leader"),
						(this_or_next|troop_slot_eq, slot_troop_spouse, "trp_player"),
							(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_no"),
						(neg|troop_slot_ge, ":faction_leader", slot_troop_prisoner_of_party, 0),#Not a prisoner
						(neg|troop_slot_ge, ":faction_leader", slot_troop_occupation, slto_retirement),#Not retired, exiled, dead
						(assign, ":faction_leader", ":troop_no"),#assign and break the loop
					(try_end),
				(try_end),

				(is_between, ":faction_leader", heroes_begin, heroes_end),#Not the player, and not a bogus value
				(neg|troop_slot_ge, ":faction_leader", slot_troop_prisoner_of_party, 0),#Not a prisoner
				(neg|troop_slot_ge, ":faction_leader", slot_troop_occupation, slto_retirement),#Not retired, exiled, dead

				(change_screen_return),
				(start_map_conversation, ":faction_leader", -1),
			  (else_try),
			  #player took a walled center while he is a vassal of npc kingdom.
			    (neq, ":is_coruler", 1),
			  ##diplomacy end+
                (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
                (jump_to_menu, "$g_next_menu"),
              (else_try), #player took a walled center while he is a vassal of rebels.
                (eq, "$players_kingdom", "fac_player_supporters_faction"),
                (assign, "$g_center_taken_by_player_faction", "$g_encountered_party"),
                (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
                (faction_get_slot, ":faction_leader", "fac_player_supporters_faction", slot_faction_leader),
                (change_screen_return),
                # (start_map_conversation, ":faction_leader", -1), #SB : script call
                (assign, "$talk_context", tc_give_center_to_fief),
                (call_script, "script_start_court_conversation", ":faction_leader", "$current_town"),
              (else_try), #player took a walled center for player's kingdom
			    ##diplomacy start+ Handle player is co-ruler of faction
				(this_or_next|eq, ":is_coruler", 1),
				##diplomacy end+
                (neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
                (assign, "$g_center_taken_by_player_faction", "$g_encountered_party"),
                (assign, "$talk_context", tc_give_center_to_fief),
                (change_screen_return),

                (assign, ":best_troop", "trp_hired_blade"),
				##diplomacy start+
				#Trivial aesthetic change, change the default troop to be appropriate to the
				#culture of the player kingdom (instead of defaulting always to a Swadian troop).
				(assign, ":players_culture", "$players_kingdom"),
				(try_begin),
					#If not the co-ruler of an NPC kingdom, use the player faction culture.
				   (neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
				   # (assign, ":best_troop", "trp_mercenary_crossbowman"),#<- while we're at it, use a mercenary default #SB : hired blade
				   (assign, ":players_culture", "$g_player_culture"),
				   (this_or_next|is_between, ":players_culture", npc_kingdoms_begin, npc_kingdoms_end),
					(is_between, ":players_culture", cultures_begin, cultures_end),
				(else_try),
					#If not the co-ruler of an NPC kingdom, and there wasn't a valid player faction
					#culture, try to use the faction of the player's court.
					(neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
					(is_between, "$g_player_court", centers_begin, centers_end),
					(party_slot_ge, "$g_player_court", slot_center_original_faction, 1),
					(party_get_slot, ":players_culture", "$g_player_court", slot_center_original_faction),
				(try_end),
				(try_begin),
					#Resolve from kingdom to culture if necessary
				   (is_between, ":players_culture", kingdoms_begin, kingdoms_end),
				   (faction_get_slot, ":players_culture", ":players_culture", slot_faction_culture),
				(try_end),
				(try_begin),
					#If the final result is a culture, get the best troop if valid
				   (is_between, ":players_culture", cultures_begin, cultures_end),
				   # (neq, ":players_culture", "fac_culture_1"), #SB : allow swadian culture
				   (faction_get_slot, reg0, ":players_culture", slot_faction_guard_troop),
				   (ge, reg0, soldiers_begin),
				   (assign, ":best_troop", reg0),
				(try_end),
				##diplomacy end+
                #SB : fix this, otherwise previously calculated troop is useless
                (try_begin),
                  (neq, ":best_troop", "trp_hired_blade"),
                  (store_character_level, ":maximum_troop_score", ":best_troop"),
                (else_try),
                  (assign, ":maximum_troop_score", 0),
                (try_end),

                (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
                (try_for_range, ":stack_no", 0, ":num_stacks"),
                  (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":stack_no"),
                  (neq, ":stack_troop", "trp_player"),

                  (party_stack_get_size, ":stack_size", "p_main_party", ":stack_no"),
                  (party_stack_get_num_wounded, ":num_wounded", "p_main_party", ":stack_no"),
                  (troop_get_slot, ":num_routed", "p_main_party", slot_troop_player_routed_agents),

                  (assign, ":continue", 0),
                  (try_begin),
                    (neg|troop_is_hero, ":stack_troop"),
                    (store_add, ":agents_which_cannot_speak", ":num_wounded", ":num_routed"),
                    (gt, ":stack_size", ":agents_which_cannot_speak"),
                    (assign, ":continue", 1),
                  (else_try),
                    (troop_is_hero, ":stack_troop"),
                    (neg|troop_is_wounded, ":stack_troop"),
                    (assign, ":continue", 1),
                  (try_end),
                  (eq, ":continue", 1),

                  (try_begin),
                    (troop_is_hero, ":stack_troop"),
                    (troop_get_slot, ":troop_renown", ":stack_troop", slot_troop_renown),
                    (store_mul, ":troop_score", ":troop_renown", 100),
                    (val_add, ":troop_score", 1000),
                  (else_try),
                    (store_character_level, ":troop_level", ":stack_troop"),
                    (assign, ":troop_score", ":troop_level"),
                  (try_end),

                  (try_begin),
                    (gt, ":troop_score", ":maximum_troop_score"),
                    (assign, ":maximum_troop_score", ":troop_score"),
                    (assign, ":best_troop", ":stack_troop"),
                    (party_stack_get_troop_dna, ":best_troop_dna", "p_main_party", ":stack_no"),
                  (try_end),
                (try_end),
                (call_script, "script_start_court_conversation", ":best_troop", "$current_town", ":best_troop_dna"),
                # (start_map_conversation, ":best_troop", ":best_troop_dna"),
              (try_end),
            (try_end),
          (try_end),
        (try_end),
      ],
    [
      ("continue",[],"Continue...",[]),
        ]
  ),
  (
    "enemy_slipped_away",0,
    "{s17}",
    "none",
    [],
    [
      ("continue",[],"Continue...",[(jump_to_menu,"mnu_total_victory")]),
    ]
  ),
  (
    "total_defeat",0,
    "{!}You shouldn't be reading this...",
    "none",
    [
        (play_track, "track_captured", 1),
           # Free prisoners
          (party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_main_party"),
          (try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
            (party_prisoner_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
            (troop_is_hero, ":stack_troop"),
            (call_script, "script_remove_troop_from_prison", ":stack_troop"),
          (try_end),

		  (try_begin),
		    (party_is_active, "$g_ally_party"),
			(call_script, "script_battle_political_consequences", "$g_ally_party", "$g_enemy_party"),
		  (else_try),
			(call_script, "script_battle_political_consequences", "p_main_party", "$g_enemy_party"),
		  (try_end),

          (call_script, "script_loot_player_items", "$g_enemy_party"),

          (assign, "$g_move_heroes", 0),
          (party_clear, "p_temp_party"),
          (call_script, "script_party_add_party_prisoners", "p_temp_party", "p_main_party"),
          (call_script, "script_party_prisoners_add_party_companions", "p_temp_party", "p_main_party"),
          (distribute_party_among_party_group, "p_temp_party", "$g_enemy_party"),

		  (try_begin),
			(neq, "$g_keep_companions", 1), # Setting to keep companions on defeat!
			(assign, "$g_prison_heroes", 1),
		  (else_try),
			(assign, "$g_prison_heroes", 0),
		  (try_end),
          (call_script, "script_party_remove_all_companions", "p_main_party"),
          (assign, "$g_prison_heroes", 0),
          (assign, "$g_move_heroes", 1),
          (call_script, "script_party_remove_all_prisoners", "p_main_party"),

          (val_add, "$g_total_defeats", 1),

          (try_begin),
            (neq, "$g_player_surrenders", 1),
            (store_random_in_range, ":random_no", 0, 100),
            (ge, ":random_no", "$g_player_luck"),
            (jump_to_menu, "mnu_permanent_damage"),
          (else_try),
            (try_begin),
              (eq, "$g_next_menu", -1),
              (leave_encounter),
              (change_screen_return),
            (else_try),
              (jump_to_menu, "$g_next_menu"),
            (try_end),
          (try_end),
          (try_begin),
            (gt, "$g_ally_party", 0),
            (call_script, "script_party_wound_all_members", "$g_ally_party"),
          (try_end),

#Troop commentary changes begin
          (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
          (try_for_range, ":stack_no", 0, ":num_stacks"),
            (party_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
            (is_between, ":stack_troop", active_npcs_begin, active_npcs_end),
			(troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
            (store_troop_faction, ":victorious_faction", ":stack_troop"),
            (call_script, "script_add_log_entry", logent_player_defeated_by_lord, "trp_player",  -1, ":stack_troop", ":victorious_faction"),
          (try_end),
#Troop commentary changes end

      ],
    []
  ),
  (
    "permanent_damage",mnf_disable_all_keys,
    "{s0}",
    "none",
    [
      (assign, ":end_cond", 1),
      (try_for_range, ":unused", 0, ":end_cond"),
        (store_random_in_range, ":random_attribute", 0, 4),
        (store_attribute_level, ":attr_level", "trp_player", ":random_attribute"),
        (try_begin),
          (gt, ":attr_level", 3),
          (neq, ":random_attribute", ca_charisma),
          (try_begin),
            (eq, ":random_attribute", ca_strength),
            (str_store_string, s0, "@Some of your tendons have been damaged in the battle. You lose 1 strength."),
          (else_try),
            (eq, ":random_attribute", ca_agility),
            (str_store_string, s0, "@You took a nasty wound which will cause you to limp slightly even after it heals. You lose 1 agility."),
##          (else_try),
##            (eq, ":random_attribute", ca_charisma),
##            (str_store_string, s0, "@After the battle you are aghast to find that one of the terrible blows you suffered has left a deep, disfiguring scar on your face, horrifying those around you. Your charisma is reduced by 1."),
          (else_try),
##            (eq, ":random_attribute", ca_intelligence),
            (str_store_string, s0, "@You have trouble thinking straight after the battle, perhaps from a particularly hard hit to your head, and frequent headaches now plague your existence. Your intelligence is reduced by 1."),
          (try_end),
        (else_try),
          (lt, ":end_cond", 200),
          (val_add, ":end_cond", 1),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":end_cond", 200),
        (try_begin),
          (eq, "$g_next_menu", -1),
          (leave_encounter),
          (change_screen_return),
        (else_try),
          (jump_to_menu, "$g_next_menu"),
        (try_end),
      (else_try),
        (troop_raise_attribute, "trp_player", ":random_attribute", -1),
      (try_end),
      ],
    [
      ("s0",
       [
         (store_random_in_range, ":random_no", 0, 4),
         (try_begin),
           (eq, ":random_no", 0),
           (str_store_string, s0, "@Perhaps I'm getting unlucky..."),
         (else_try),
           (eq, ":random_no", 1),
           (str_store_string, s0, "@Retirement is starting to sound better and better."),
         (else_try),
           (eq, ":random_no", 2),
           (str_store_string, s0, "@No matter! I will persevere!"),
         (else_try),
           (eq, ":random_no", 3),
			  ##diplomacy start+ Don't use troop_get_type for gender
			  #(troop_get_type, ":is_female", "trp_player"),#<- replaced
           (try_begin),
             #(eq, ":is_female", 1),#<- replaced
			 (eq, "$character_gender", tf_female),#<- added
             (str_store_string, s0, "@What did I do to deserve this?"),
           (else_try),
             (str_store_string, s0, "@I suppose it'll make for a good story, at least..."),
           (try_end),
			  ##diplomacy end+
         (try_end),
         ],
       "{s0}",
       [
         (try_begin),
           (eq, "$g_next_menu", -1),
           (leave_encounter),
           (change_screen_return),
         (else_try),
           (jump_to_menu, "$g_next_menu"),
         (try_end),
         ]),
      ]
  ),
]
