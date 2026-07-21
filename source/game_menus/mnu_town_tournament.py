# ======================================================================
# SHARED DEPENDENCY
# Entity: town_tournament (menu)
# Called by menus in 3 domains: cheats, tournament, town
# ======================================================================

# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

town_tournament_menu = [
(
    "town_tournament",mnf_disable_all_keys,
    "{s1}You are at tier {reg0} of the tournament, with {reg1} participants remaining. In the next round, there will be {reg2} teams with {reg3} {reg4?fighters:fighter} each.",
    "none",
    [
        (party_set_slot, "$current_town", slot_town_has_tournament, 0), #No way to return back if this menu is left
        (call_script, "script_sort_tournament_participant_troops"),#Moving trp_player to the top of the list
        (call_script, "script_get_num_tournament_participants"),
        (assign, ":num_participants", reg0),
        (try_begin),
          (neg|troop_slot_eq, "trp_tournament_participants", 0, 0),#Player is defeated

          (assign, ":player_odds_add", 0),
          (store_div, ":player_odds_add", "$g_tournament_bet_placed", 5),
          (party_get_slot, ":player_odds", "$current_town", slot_town_player_odds),
          (val_add, ":player_odds", ":player_odds_add"),
          (val_min, ":player_odds", 4000),
          (party_set_slot, "$current_town", slot_town_player_odds, ":player_odds"),

          (jump_to_menu, "mnu_town_tournament_lost"),
        (else_try),
          (eq, ":num_participants", 1),#Tournament won
          (jump_to_menu, "mnu_town_tournament_won"),
        (else_try),
          (try_begin),
            (le, "$g_tournament_next_num_teams", 0),
            (call_script, "script_get_random_tournament_team_amount_and_size"),
            (assign, "$g_tournament_next_num_teams", reg0),
            (assign, "$g_tournament_next_team_size", reg1),
          (try_end),
          (assign, reg2, "$g_tournament_next_num_teams"),
          (assign, reg3, "$g_tournament_next_team_size"),
          (store_sub, reg4, reg3, 1),
          (str_clear, s1),
          (try_begin),
            (eq, "$g_tournament_player_team_won", 1),
            (str_store_string, s1, "@Victory is yours! You have won this melee, but now you must prepare yourself for the next round. "),
          (else_try),
            (eq, "$g_tournament_player_team_won", 0),
            (str_store_string, s1, "@You have been bested in this melee, but the master of ceremonies declares a recognition of your skill and bravery, allowing you to take part in the next round. "),
          (try_end),
          (assign, reg1, ":num_participants"),
          (store_add, reg0, "$g_tournament_cur_tier", 1),
        (try_end),
        ],
    [
      ("host_tournament",
      [(ge, "$cheat_mode", 1),],
      "{!}Cheat : Win tournament",
      [
           (jump_to_menu, "mnu_town_tournament_won"),
           (assign, "$g_player_eligible_feast_center_no", "$current_town"),
		   (assign, "$g_player_tournament_placement", 100),
      ]),
      ("tournament_view_participants", [], "View participants.",
       [(jump_to_menu, "mnu_tournament_participants"),
        ]),
      ("tournament_bet", [(neq, "$g_tournament_cur_tier", "$g_tournament_last_bet_tier")], "Place a bet on yourself.",
       [(jump_to_menu, "mnu_tournament_bet"),
        ]),
      ("tournament_join_next_fight", [], "Fight in the next round.",
       [
           (party_get_slot, ":arena_scene", "$current_town", slot_town_arena),
           (modify_visitors_at_site, ":arena_scene"),
           (reset_visitors),
           #Assuming that there are enough participants for the teams
		   (assign, "$g_player_tournament_placement", "$g_tournament_cur_tier"),
		   (try_begin),
		     (gt, "$g_player_tournament_placement", 4),
		     (assign, "$g_player_eligible_feast_center_no", "$current_town"),
		   (try_end),
           (val_add, "$g_tournament_cur_tier", 1),

           (store_mul, "$g_tournament_num_participants_for_fight", "$g_tournament_next_num_teams", "$g_tournament_next_team_size"),
           (troop_set_slot, "trp_tournament_participants", 0, -1),#Removing trp_player from the list
           (troop_set_slot, "trp_temp_array_a", 0, "trp_player"),
           (try_for_range, ":slot_no", 1, "$g_tournament_num_participants_for_fight"),
             (call_script, "script_get_random_tournament_participant"),
             (troop_set_slot, "trp_temp_array_a", ":slot_no", reg0),
           (try_end),
           (call_script, "script_shuffle_troop_slots", "trp_temp_array_a", 0, "$g_tournament_num_participants_for_fight"),


           (try_for_range, ":slot_no", 0, 4),#shuffle teams
             (troop_set_slot, "trp_temp_array_b", ":slot_no", ":slot_no"),
           (try_end),
           (call_script, "script_shuffle_troop_slots", "trp_temp_array_b", 0, 4),

           (assign, ":cur_slot", 0),
           (assign, ":player_slot", -1), #SB : find player's slot
           (try_for_range, ":cur_team_offset", 0, "$g_tournament_next_num_teams"),
             (troop_get_slot, ":cur_team", "trp_temp_array_b", ":cur_team_offset"),

             (try_for_range, ":slot_no", 0, 8),#shuffle entry_points
               (troop_set_slot, "trp_temp_array_c", ":slot_no", ":slot_no"),
             (try_end),
             (call_script, "script_shuffle_troop_slots", "trp_temp_array_c", 0, 8),

             (try_for_range, ":cur_index", 0, "$g_tournament_next_team_size"),
               (store_mul, ":cur_entry_point", ":cur_team", 8),
               (troop_get_slot, ":entry_offset", "trp_temp_array_c", ":cur_index"),
               (val_add, ":cur_entry_point", ":entry_offset"),
               (troop_get_slot, ":troop_no", "trp_temp_array_a", ":cur_slot"),
               (set_visitor, ":cur_entry_point", ":troop_no"),
               (try_begin), #SB : set player's slot
                 (eq, ":troop_no", "trp_player"),
                 (assign, ":player_slot", ":cur_entry_point"),
               (try_end),
               (val_add, ":cur_slot", 1),
             (try_end),
           (try_end),

           (assign, "$g_tournament_next_num_teams", 0),
           (assign, "$g_tournament_next_team_size", 0),

           (assign, "$g_mt_mode", abm_tournament),
           #SB : pass on as global
           (try_begin),
             (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$g_encountered_party_faction"),
             (this_or_next|ge, reg0, DPLMC_FACTION_STANDING_MEMBER),
             (party_slot_ge, "$current_town", slot_center_player_relation, 15),
             (assign, "$g_player_entry_point", ":player_slot"),
           (else_try),
             (assign, "$g_player_entry_point", -1),
           (try_end),

           (party_get_slot, ":town_original_faction", "$current_town", slot_center_original_faction),
           (assign, ":town_index_within_faction", 0),
           (assign, ":end_cond", towns_end),
           (try_for_range, ":cur_town", towns_begin, ":end_cond"),
             (try_begin),
               (eq, ":cur_town", "$current_town"),
               (assign, ":end_cond", 0), #break
             (else_try),
               (party_slot_eq, ":cur_town", slot_center_original_faction, ":town_original_faction"),
               (val_add, ":town_index_within_faction", 1),
             (try_end),
           (try_end),

           (set_jump_mission, "mt_arena_melee_fight"),

           (try_begin),
             (eq, ":town_original_faction", "fac_kingdom_1"),
             #Swadia
             (store_mod, ":mod", ":town_index_within_faction", 4),
             (try_begin), #parameters: horse, lance, sword, axe, bow, javelin, horse-archer, crossbow, armor begin, helm begin
               (eq, ":mod", 0),
               (call_script, "script_set_items_for_tournament", 40, 80, 50, 20, 0, 0, 0, 0, "itm_arena_armor_red", "itm_tourney_helm_red"),
             (else_try),
               (eq, ":mod", 1),
               (call_script, "script_set_items_for_tournament", 100, 100, 0, 0, 0, 0, 0, 0, "itm_arena_armor_red", "itm_tourney_helm_red"),
             (else_try),
               (eq, ":mod", 2),
               (call_script, "script_set_items_for_tournament", 100, 0, 100, 0, 0, 0, 0, 0, "itm_arena_armor_red", "itm_tourney_helm_red"),
             (else_try),
               (eq, ":mod", 3),
               (call_script, "script_set_items_for_tournament", 40, 80, 50, 20, 40, 0, 0, 0, "itm_arena_armor_red", "itm_tourney_helm_red"),
             (try_end),
           (else_try),
             (eq, ":town_original_faction", "fac_kingdom_2"),
             #Vaegirs
             (store_mod, ":mod", ":town_index_within_faction", 4),
             (try_begin),
               (eq, ":mod", 0),
               (call_script, "script_set_items_for_tournament", 40, 80, 50, 20, 0, 0, 0, 0, "itm_arena_armor_red", "itm_steppe_helmet_red"),
             (else_try),
               (eq, ":mod", 1),
               (call_script, "script_set_items_for_tournament", 100, 50, 0, 0, 0, 20, 30, 0, "itm_arena_armor_red", "itm_steppe_helmet_red"),
             (else_try),
               (eq, ":mod", 2),
               (call_script, "script_set_items_for_tournament", 100, 0, 50, 0, 0, 20, 30, 0, "itm_arena_armor_red", "itm_steppe_helmet_red"),
             (else_try),
               (eq, ":mod", 3),
               (call_script, "script_set_items_for_tournament", 40, 80, 50, 20, 30, 0, 60, 0, "itm_arena_armor_red", "itm_steppe_helmet_red"),
             (try_end),
           (else_try),
             (eq, ":town_original_faction", "fac_kingdom_3"),
             #Khergit
             (store_mod, ":mod", ":town_index_within_faction", 2),
             (try_begin),
               (eq, ":mod", 0),
               (call_script, "script_set_items_for_tournament", 100, 0, 0, 0, 0, 40, 60, 0, "itm_arena_tunic_red", "itm_steppe_helmet_red"),
             (else_try),
               (eq, ":mod", 1),
               (call_script, "script_set_items_for_tournament", 100, 50, 25, 0, 0, 30, 50, 0, "itm_arena_tunic_red", "itm_steppe_helmet_red"),
             (try_end),
           (else_try),
             (eq, ":town_original_faction", "fac_kingdom_4"),
             #Nords
             (store_mod, ":mod", ":town_index_within_faction", 3),
             (try_begin),
               (eq, ":mod", 0),
               (call_script, "script_set_items_for_tournament", 0, 0, 50, 80, 0, 0, 0, 0, "itm_arena_armor_red", -1),
             (else_try),
               (eq, ":mod", 1),
               (call_script, "script_set_items_for_tournament", 0, 0, 50, 80, 50, 0, 0, 0, "itm_arena_armor_red", -1),
             (else_try),
               (eq, ":mod", 2),
               (call_script, "script_set_items_for_tournament", 40, 0, 0, 100, 0, 0, 0, 0, "itm_arena_armor_red", -1),
             (try_end),
           (else_try),
             #Rhodoks
             (eq, ":town_original_faction", "fac_kingdom_5"),
             (call_script, "script_set_items_for_tournament", 25, 100, 60, 0, 30, 0, 30, 50, "itm_arena_tunic_red", "itm_arena_helmet_red"),
           (else_try),
             #Sarranids
             (store_mod, ":mod", ":town_index_within_faction", 2),
             (try_begin),
               (eq, ":mod", 0),
               (call_script, "script_set_items_for_tournament", 100, 40, 60, 0, 30, 30, 0, 0, "itm_arena_tunic_red", "itm_arena_turban_red"),
             (else_try),
               (call_script, "script_set_items_for_tournament", 50, 0, 60, 0, 30, 30, 0, 0, "itm_arena_tunic_red", "itm_arena_turban_red"),
             (try_end),
           (try_end),
           (jump_to_scene, ":arena_scene"),
           (change_screen_mission),
        ]),
      ("leave_tournament",[],"Withdraw from the tournament.",
       [
           (jump_to_menu, "mnu_tournament_withdraw_verify"),
        ]),
    ]
  )
]
