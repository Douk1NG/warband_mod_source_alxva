# ======================================================================
# SHARED DEPENDENCY
# Entity: let_nearby_parties_join_current_battle (script)
# Called by menus in 3 domains: battle, castle, siege
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

let_nearby_parties_join_current_battle_scripts = [
("let_nearby_parties_join_current_battle",
    [
      (store_script_param, ":besiege_mode", 1),
      (store_script_param, ":dont_add_friends_other_than_accompanying", 2),

      (store_character_level, ":player_level", "trp_player"),
      (try_for_parties, ":party_no"),
        (party_is_active, ":party_no"),
        (party_get_battle_opponent, ":opponent",":party_no"),
        (lt, ":opponent", 0), #party is not itself involved in a battle
        (party_get_attached_to, ":attached_to",":party_no"),
        (lt, ":attached_to", 0), #party is not attached to another party
        (get_party_ai_behavior, ":behavior", ":party_no"),
        (neq, ":behavior", ai_bhvr_in_town),

        (party_stack_get_troop_id, ":stack_troop", ":party_no", 0),
        (party_get_template_id,":template_id",":party_no"),
        #SB : exclude certain templates, quest, prisoners/routers
        (neq, ":template_id", "pt_troublesome_bandits"),
        (neq, ":template_id", "pt_bandits_awaiting_ransom"),
        (neq, ":template_id", "pt_rescued_prisoners"),
        (neq, ":template_id", "pt_routed_warriors"),

        (try_begin),
          (this_or_next|is_between, ":stack_troop", "trp_looter", bandits_end),
          (is_between, ":template_id", bandit_party_templates_begin, bandit_party_templates_end), #SB : template range
          (assign, ":is_bandit", 1),
        (else_try),
          (assign, ":is_bandit", 0),
        (try_end),
        (game_get_reduce_campaign_ai, ":join_sub"), #easier = smaller distance bandits
        (try_begin),#Native behaviour
          (eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_DISABLE),
          (try_begin),
            (eq, ":is_bandit", 1),
            (assign, ":join_distance", 5), #day/not bandit
            (try_begin),
              (is_currently_night),
              (assign, ":join_distance", 3), #nigh/not bandit
            (try_end),
          (else_try),
            (assign, ":join_distance", 3), #day/bandit
            (try_begin),
              (is_currently_night),
              (assign, ":join_distance", 2), #night/bandit
            (try_end),
          (try_end),
        (else_try), #SB : new distance calculation, based on spotting
          (party_get_skill_level, ":join_distance", ":party_no", "skl_spotting"), #Native lords have none
          (val_div, ":join_distance", 3),
          (val_add, ":join_distance", 4), #from 4 to 7
          (try_begin), #global night deduction
            (is_currently_night),
            (val_sub, ":join_distance", 2), #night/not bandit
          (try_end),
          (try_begin),
            (eq, ":is_bandit", 1),
            (val_sub, ":join_distance", 1), #day/bandit, value of 3
            (val_sub, ":join_distance", ":join_sub"), #can reduce it down to 1 on easy mode
            (is_currently_night), #night/bandit
            (val_add, ":join_distance", 1), #less sharp penalty, value of 2
          (try_end),
          #booster to patrols etc. that makes up for new base of 4
          (try_begin),
            (eq, ":template_id", "pt_patrol_party"),
            (val_add, ":join_distance", 1), #always true
            (try_begin),
              (get_party_ai_object, ":obj", ":party_no"),#just in case
              (eq, ":behavior", ai_bhvr_escort_party),
              (eq, ":obj", "p_main_party"),
              (val_add, ":join_distance", ":join_sub"),#they stray off easily
            (try_end),
          # (else_try), #other behaviour score
            # (eq, ":behavior", ai_bhvr_avoid_party), #fleeing
            # (val_sub, ":join_distance", 1),
          (else_try), #representing preparedness to join battle
            (this_or_next|eq, ":behavior", ai_bhvr_patrol_party),
            (this_or_next|eq, ":behavior", ai_bhvr_patrol_location),
            (eq, ":behavior", ai_bhvr_escort_party),
            (val_add, ":join_distance", 1),
          (try_end),
        (try_end),


		# #Quest bandits do not join battle
		# (this_or_next|neg|check_quest_active, "qst_track_down_bandits"),
			# (neg|quest_slot_eq, "qst_track_down_bandits", slot_quest_target_party, ":party_no"),
		# (this_or_next|neg|check_quest_active, "qst_troublesome_bandits"),
			# (neg|quest_slot_eq, "qst_troublesome_bandits", slot_quest_target_party, ":party_no"),



        (store_distance_to_party_from_party, ":distance", ":party_no", "p_main_party"),
        (lt, ":distance", ":join_distance"),

        (store_faction_of_party, ":faction_no", ":party_no"),
        (store_faction_of_party, ":enemy_faction", "$g_enemy_party"),
        (try_begin),
          (eq, ":faction_no", "fac_player_supporters_faction"),
          (assign, ":reln_with_player", 100),
        (else_try),
          (store_relation, ":reln_with_player", ":faction_no", "fac_player_supporters_faction"),
        (try_end),
        (try_begin),
          (eq, ":faction_no", ":enemy_faction"),
          (assign, ":reln_with_enemy", 100),
        (else_try),
          (store_relation, ":reln_with_enemy", ":faction_no", ":enemy_faction"),
        (try_end),

        (assign, ":enemy_side", 1),
        (try_begin),
          (neq, "$g_enemy_party", "$g_encountered_party"),
          (assign, ":enemy_side", 2),
        (try_end),

        (try_begin),
          (eq, ":besiege_mode", 0),
          (lt, ":reln_with_player", 0),
          (gt, ":reln_with_enemy", 0),
          ##zerilius changes begin
          ##wrong use of operation (native bug)
          #(party_get_slot, ":party_type", ":party_no"),
          (party_get_slot, ":party_type", ":party_no", slot_party_type),
          ##zerilius changes end

          (assign, ":enemy_is_bandit_party_and_level_is_greater_than_6", 0),
          (try_begin), #SB : is_bandit
            # (party_stack_get_troop_id, ":stack_troop", ":party_no", 0),
            # (is_between, ":stack_troop", "trp_looter", "trp_black_khergit_horseman"),
            (eq, ":is_bandit", 1),
            (gt, ":player_level", 6),
            (assign, ":enemy_is_bandit_party_and_level_is_greater_than_6", 1),
          (try_end),

          (this_or_next|eq, ":party_type", spt_kingdom_hero_party),
          (eq, ":enemy_is_bandit_party_and_level_is_greater_than_6", 1),

          (get_party_ai_behavior, ":ai_bhvr", ":party_no"),
          (neq, ":ai_bhvr", ai_bhvr_avoid_party),
          (party_quick_attach_to_current_battle, ":party_no", ":enemy_side"), #attach as enemy
          (str_store_party_name, s1, ":party_no"),
          #SB : colorize
          (display_message, "str_s1_joined_battle_enemy", message_negative),
        (else_try),
          (try_begin),
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
            (party_slot_eq, ":party_no", slot_party_ai_object, "trp_player"),
            (assign, ":party_is_accompanying_player", 1),
          (else_try),
            (assign, ":party_is_accompanying_player", 0),
          (try_end),

          (this_or_next|eq, ":dont_add_friends_other_than_accompanying", 0),
          (eq, ":party_is_accompanying_player", 1),
          (gt, ":reln_with_player", 0),
          (lt, ":reln_with_enemy", 0),

          (assign, ":following_player", 0),
          (try_begin),
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
            (party_slot_eq, ":party_no", slot_party_ai_object, "p_main_party"),
            (assign, ":following_player", 1),
          (try_end),

          (assign, ":do_join", 1),
          (try_begin),
            (eq, ":besiege_mode", 1),
            (eq, ":following_player", 0),
            (assign, ":do_join", 0),
            (eq, ":faction_no", "$players_kingdom"),
            (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
            (assign, ":do_join", 1),
          (try_end),
          (eq, ":do_join", 1),

          ##zerilius changes begin
          ##wrong use of operation (native bug)
          #(party_get_slot, ":party_type", ":party_no"),
          (party_get_slot, ":party_type", ":party_no", slot_party_type),
          ##zerilius changes end
          (this_or_next|eq, ":party_type", spt_kingdom_hero_party), #dckplmc
          (eq, ":template_id", "pt_hero_party"),
          (party_stack_get_troop_id, ":leader", ":party_no", 0),
          #(troop_get_slot, ":player_relation", ":leader", slot_troop_player_relation),
          (call_script, "script_troop_get_player_relation", ":leader"),
          (assign, ":player_relation", reg0),

          (assign, ":join_even_you_do_not_like_player", 0),
          (try_begin),
            (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"), #new added, if player is marshal and if he is accompanying then join battle even lord do not like player
            (eq, ":following_player", 1),
            (assign, ":join_even_you_do_not_like_player", 1),
          ##diplomacy start+
	  #Affiliates will assist the player.
	   (else_try),
             (lt, ":player_relation", 0),
	     (call_script, "script_dplmc_is_affiliated_family_member", ":leader"),
	     (val_max, ":player_relation", reg0),
          ##diplomacy end+
          (try_end),

          (this_or_next|ge, ":player_relation", 0),
          (eq, ":join_even_you_do_not_like_player", 1),

          (party_quick_attach_to_current_battle, ":party_no", 0), #attach as friend
          (str_store_party_name, s1, ":party_no"),
          # ## SB : colorize
          # (faction_get_color, ":color", ":faction_no"),
          (display_message, "str_s1_joined_battle_friend", message_positive),

          (troop_get_slot, ":limit", "$g_player_troop", slot_troop_renown),
          (val_sub, ":limit", dplmc_command_renown_limit),
          (game_get_reduce_campaign_ai, ":bonus"),
          (val_mul, ":bonus", "$player_right_to_rule"),
          (val_add, ":limit", ":bonus"),

          (assign, ":continue", -1), #by default, not under command

          (try_begin), #under command if marshal
            (eq, ":faction_no", "$players_kingdom"),
            (troop_slot_eq, ":leader", slot_troop_occupation, slto_kingdom_hero),
            (try_begin), #as marshal
               # (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
               # (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
               # (assign, ":continue", 0),
            # (else_try), #as ruler/pretender marshal
               # (faction_slot_eq, ":party_faction", slot_faction_state, sfs_active),
               (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
               (ge, reg0, DPLMC_FACTION_STANDING_MARSHALL),

               (display_message, "@marshall {reg0}"),
               # (this_or_next|faction_slot_eq, ":party_faction", slot_faction_marshall, "trp_player"),
               # (faction_slot_eq, ":party_faction", slot_faction_leader, "$g_player_troop"),
               (assign, ":continue", 0),
            (try_end),
            (eq, ":continue", -1), #If still not satisfied, check other conditions
          (else_try), #or high enough renown
            (troop_slot_eq, ":leader", slot_troop_occupation, slto_kingdom_hero),
            (troop_get_slot, ":renown", ":leader", slot_troop_renown),
            (call_script, "script_troop_get_relation_with_troop", ":leader", "$g_player_troop"),
            (val_sub, ":renown", reg0), #higher relation means less renown needed.
            (le, ":renown", ":limit"),

            (assign, ":continue", 0),
          (else_try), #straggler parties - patrols, caravans, etc.
            (neg|is_between, ":leader", active_npcs_begin, active_npcs_end),

            (assign, ":continue", 0),
          (try_end),
          (party_set_slot, ":party_no", slot_party_temp_slot_1, ":continue"),
          (try_begin),
            (ge, "$cheat_mode", 1),
            (assign, reg0, ":continue"),
            # (str_store_party_name, s0, ":party_no"),
            (str_store_party_name, s0, ":party_no"),
            (faction_get_color, ":color", ":faction_no"),
            (display_message, "@{s0} will {reg0?not :}be under your command", ":color"),
          (try_end),

        (try_end),
      (try_end),
  ])
]
