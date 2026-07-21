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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

game_event_context_menu_button_clicked_scripts = [
#script_game_event_context_menu_button_clicked:
# This script is called from the game engine when the player clicks on a button at the right mouse menu.
# INPUT: arg1 = party_no, arg2 = button_value
# OUTPUT: none
("game_event_context_menu_button_clicked",
   [(store_script_param, ":party_no", 1),
    (store_script_param, ":button_value", 2),
    (try_begin),
      (eq, ":button_value", cmenu_notes),
      #SB : unify this under a single constant
      (try_begin),
        (is_between, ":party_no", centers_begin, centers_end),
        (change_screen_notes, 3, ":party_no"),
      (else_try),
        (party_stack_get_troop_id, ":troop_no", ":party_no", 0),
        (change_screen_notes, 1, ":troop_no"),
      (try_end),
    (else_try), #SB : lots of cheats
      (eq, ":button_value", cmenu_attach),
      (try_begin),
        (neq, ":party_no", "p_main_party"),
        (party_set_next_battle_simulation_time, ":party_no", -1),
        (party_leave_cur_battle, ":party_no"),
        (party_set_flags, ":party_no", pf_is_static, 0),
        (party_attach_to_party, ":party_no", "p_main_party"),
      (else_try),
        (party_get_attached_party_with_rank, ":attached_party", "p_main_party", 0),
        (party_get_position, pos1, "p_main_party"),
        (party_detach, ":attached_party"),
        (party_set_position, ":attached_party", pos1),
        (try_begin),
          (is_between, ":attached_party", centers_begin, centers_end),
          (party_set_flags, ":attached_party", pf_is_static, 1),
        (try_end),
      (try_end),
    (else_try),
      (eq, ":button_value", cmenu_detach),
      (party_get_num_attached_parties, ":num_stacks", ":party_no"),
      (try_for_range_backwards, ":stacks", 0, ":num_stacks"),
        (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":stacks"),
        (party_detach, ":attached_party"),
        (party_set_ai_behavior, ":attached_party", ai_bhvr_hold),
        (party_set_flags, ":attached_party", pf_default_behavior, 1),
        (party_relocate_near_party, ":attached_party", ":party_no", 3),
        (try_begin),
          (is_between, ":attached_party", centers_begin, centers_end),
          (party_set_flags, ":attached_party", pf_is_static, 1),
        (try_end),
      (try_end),
    (else_try),
      (eq, ":button_value", cmenu_encounter),
      (assign, "$new_encounter", 2), #this lets us branch to a different menu
      (start_encounter, ":party_no"),
      # (set_encountered_party, ":party_no"),
      # (assign, "$g_encountered_party", ":party_no"),
      # (change_screen_exchange_with_party, ":party_no"),
      # (jump_to_menu, "mnu_auto_return"),
    # (else_try),
      # (eq, ":button_value", cmenu_encounter),
      # (start_encounter, ":party_no"),
    # (else_try),
      # (eq, ":button_value", cmenu_spawnbandit),
      # (set_spawn_radius, 25),
      # (try_for_range, ":unused", 0, 10),
        # (store_random_in_range, ":party_template", bandit_party_templates_begin, bandit_party_templates_end),
        # (spawn_around_party, ":party_no", ":party_template"),
      # (try_end),
      #(call_script, "script_update_bandit_pressure"),
    (else_try), #too lazy to invoke magical commands, screw around with composition
      (eq, ":button_value", cmenu_losebattle),
      (call_script, "script_party_wound_all_members", ":party_no"),
      (party_set_next_battle_simulation_time, ":party_no", -1),
    (else_try), #winning is half the battle
      (eq, ":button_value", cmenu_winbattle),
      (party_get_battle_opponent, ":other_party", ":party_no"),
      (call_script, "script_party_wound_all_members", ":other_party"),
      (party_set_next_battle_simulation_time, ":party_no", 0),
    ## Moved the following to a menu instead
    # (else_try), #refill or double-up
      # (eq, ":button_value", cmenu_reinforce),
      # (store_faction_of_party, ":faction_no", ":party_no"),
      # (try_begin), #
        # (is_between, ":party_no", villages_begin, villages_end),
        # (party_add_template, ":party_no", "pt_village_defenders"),
      # (else_try),
        # (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        # (call_script, "script_cf_reinforce_party", ":party_no"),
      # (else_try),
        # (eq, ":faction_no", "fac_deserters"),
        # (party_stack_get_troop_id, ":troop_id", ":party_no", 0),
        # (store_faction_of_troop, ":faction_no", ":troop_id"),
        # (store_random_in_range, ":slot_no", slot_faction_reinforcements_a, slot_faction_num_armies),
        # (faction_get_slot, ":party_template", ":faction_no", ":slot_no"),
        # (party_add_template, ":party_no", ":party_template"),
      # (else_try),
        # # (this_or_next|eq, ":faction_no", "fac_outlaws"),
        # # (is_between, ":faction_no", bandit_factions_begin, bandit_factions_end),
        # (party_get_template_id, ":party_template", ":party_no"),
        # (party_add_template, ":party_no", ":party_template"),
      # (try_end),
    # (else_try),
      # (eq, ":button_value", cmenu_wound),
      # (call_script, "script_party_wound_all_members", ":party_no"),
    # (else_try),
      # (eq, ":button_value", cmenu_heal),
      # # (heal_party, ":party_no"), #this does NOT work, any calls will only affect the main party
      # (try_begin),
        # (eq, ":party_no", "p_main_party"),
        # (heal_party, "p_main_party"),
      # (else_try),
        # (call_script, "script_party_heal_all_members_aux", ":party_no"),
      # (try_end),
    (try_end),
  ])
]
