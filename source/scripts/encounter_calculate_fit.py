# ======================================================================
# SHARED DEPENDENCY
# Entity: encounter_calculate_fit (script)
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

encounter_calculate_fit_scripts = [
# script_map_get_random_position_around_position_within_range
# Input: arg1 = troop_no
# Output: none
("encounter_calculate_fit",
    [
      #(assign, "$g_enemy_fit_for_battle_old",  "$g_enemy_fit_for_battle"),
      #(assign, "$g_friend_fit_for_battle_old", "$g_friend_fit_for_battle"),
      #(assign, "$g_main_party_fit_for_battle_old", "$g_main_party_fit_for_battle"),
      (call_script, "script_party_count_fit_for_battle", "p_main_party"),
      #(assign, "$g_main_party_fit_for_battle", reg(0)),
      (call_script, "script_collect_friendly_parties"),
      (call_script, "script_party_count_fit_for_battle", "p_collective_friends"),
      (assign, "$g_friend_fit_for_battle", reg(0)),

      (party_clear, "p_collective_ally"),
      (try_begin),
        (gt, "$g_ally_party", 0),
        (party_is_active, "$g_ally_party"),
        (party_collect_attachments_to_party, "$g_ally_party", "p_collective_ally"),
        #(call_script, "script_party_count_fit_for_battle", "p_collective_ally"),
        #(val_add, "$g_friend_fit_for_battle", reg(0)),
        #SB : pre-process command structure here
        (party_get_num_attached_parties, ":attached", "$g_ally_party"),
        (troop_get_slot, ":limit", "$g_player_troop", slot_troop_renown),
        (val_sub, ":limit", dplmc_command_renown_limit),
        (game_get_reduce_campaign_ai, ":bonus"),
        (val_mul, ":bonus", "$player_right_to_rule"),
        (val_add, ":limit", ":bonus"),

        (assign, reg0, ":attached"),
        (val_add, ":attached", 1),
        (try_for_range, ":rank", 0, ":attached"),
          (party_get_attached_party_with_rank, ":party_no", "$g_ally_party", ":rank"),
          (try_begin),
            (eq, ":party_no", -1),
            (assign, ":party_no", "$g_ally_party"),
          (try_end),
          (assign, ":continue", -1),

          (store_faction_of_party, ":party_faction", ":party_no"),
          (party_stack_get_troop_id, ":leader_troop_id", ":party_no", 0),

          (try_begin),
            (eq, ":party_no", "p_main_party"),
            (assign, ":continue", 0),
          (else_try),
            (assign, ":continue", -1), #by default, not under command
          (try_end),

          (try_begin), #under command if marshal
            (eq, ":party_faction", "$players_kingdom"),
            (troop_slot_eq, ":leader_troop_id", slot_troop_occupation, slto_kingdom_hero),

            (try_begin), #as marshal
               # (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
               # (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
               # (assign, ":continue", 0),
            # (else_try), #as ruler/pretender marshal
               # (faction_slot_eq, ":party_faction", slot_faction_state, sfs_active),
               (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":party_faction"),
               (ge, reg0, DPLMC_FACTION_STANDING_MARSHALL),
               # (this_or_next|faction_slot_eq, ":party_faction", slot_faction_marshall, "trp_player"),
               # (faction_slot_eq, ":party_faction", slot_faction_leader, "$g_player_troop"),
               (assign, ":continue", 0),
            (try_end),
            (eq, ":continue", -1), #If still not satisfied, check other conditions
          (else_try), #or high enough renown
            (troop_slot_eq, ":leader_troop_id", slot_troop_occupation, slto_kingdom_hero),
            (troop_get_slot, ":renown", ":leader_troop_id", slot_troop_renown),
            (call_script, "script_troop_get_relation_with_troop", ":leader_troop_id", "$g_player_troop"),
            (val_sub, ":renown", reg0), #higher relation means less renown needed.
            (le, ":renown", ":limit"),
            (assign, ":continue", 0),
          (else_try), #straggler parties - patrols, caravans, etc.
            (neg|troop_slot_eq, ":leader_troop_id", slot_troop_occupation, slto_kingdom_hero),
            (assign, ":continue", 0),
          (try_end),
          (party_set_slot, ":party_no", slot_party_temp_slot_1, ":continue"),
          (try_begin),
            (ge, "$cheat_mode", 1),
            (assign, reg0, ":continue"),
            # (str_store_party_name, s0, ":party_no"),
            (str_store_party_name, s0, ":party_no"),
            (faction_get_color, ":color", ":party_faction"),
            (display_message, "@{s0} will {reg0?not :} be under your command", ":color"),
          (try_end),
        (try_end),
      (try_end),

      (party_clear, "p_collective_enemy"),
      (try_begin),
        (party_is_active, "$g_enemy_party"),
        (party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),
      (try_end),
      (call_script, "script_party_count_fit_for_battle", "p_collective_enemy"),
      (assign, "$g_enemy_fit_for_battle", reg(0)),
      (assign, reg11, "$g_enemy_fit_for_battle"),
      (assign, reg10, "$g_friend_fit_for_battle"),
  ])
]
