# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *
from compiler import *

from game_menus.mnu_arena_duel_conclusion import arena_duel_conclusion_menu
from game_menus.mnu_arena_duel_fight import arena_duel_fight_menu
from game_menus.mnu_auto_return import auto_return_menu
from game_menus.mnu_auto_return_to_map import auto_return_to_map_menu
from game_menus.mnu_auto_trade import auto_trade_menu
from game_menus.mnu_bandit_lair import bandit_lair_menu
from game_menus.mnu_battle_debrief import battle_debrief_menu
from game_menus.mnu_battlefields import battlefields_menu
from game_menus.mnu_besiegers_camp_with_allies import besiegers_camp_with_allies_menu
from game_menus.mnu_buy_ship import buy_ship_menu
from game_menus.mnu_camp import camp_menu
from game_menus.mnu_camp_action import camp_action_menu
from game_menus.mnu_camp_action_read_book import camp_action_read_book_menu
from game_menus.mnu_camp_action_read_book_start import camp_action_read_book_start_menu
from game_menus.mnu_camp_action_sort_inventory import camp_action_sort_inventory_menu
from game_menus.mnu_camp_cheat import camp_cheat_menu
# from game_menus.mnu_camp_cheat_adv import camp_cheat_adv_menu # unused - merged into camp_cheat
from game_menus.mnu_camp_cheat_player_stats import camp_cheat_player_stats_menu
from game_menus.mnu_camp_cheat_party import camp_cheat_party_menu
from game_menus.mnu_camp_cheat_world import camp_cheat_world_menu
from game_menus.mnu_camp_cheat_player_kingdom import camp_cheat_player_kingdom_menu
from game_menus.mnu_camp_cheat_debug import camp_cheat_debug_menu
from game_menus.mnu_camp_no_prisoners import camp_no_prisoners_menu
from game_menus.mnu_camp_recruit_prisoners import camp_recruit_prisoners_menu
from game_menus.mnu_cannot_enter_court import cannot_enter_court_menu
from game_menus.mnu_captivity_avoid_wilderness import captivity_avoid_wilderness_menu
from game_menus.mnu_captivity_castle_check import captivity_castle_check_menu
from game_menus.mnu_captivity_castle_remain import captivity_castle_remain_menu
from game_menus.mnu_captivity_castle_taken_prisoner import captivity_castle_taken_prisoner_menu
from game_menus.mnu_captivity_end_exchanged_with_prisoner import captivity_end_exchanged_with_prisoner_menu
from game_menus.mnu_captivity_end_propose_ransom import captivity_end_propose_ransom_menu
from game_menus.mnu_captivity_end_wilderness_escape import captivity_end_wilderness_escape_menu
from game_menus.mnu_captivity_rescue_lord_taken_prisoner import captivity_rescue_lord_taken_prisoner_menu
from game_menus.mnu_captivity_start_castle_defeat import captivity_start_castle_defeat_menu
from game_menus.mnu_captivity_start_castle_surrender import captivity_start_castle_surrender_menu
from game_menus.mnu_captivity_start_under_siege_defeat import captivity_start_under_siege_defeat_menu
from game_menus.mnu_captivity_start_wilderness import captivity_start_wilderness_menu
from game_menus.mnu_captivity_start_wilderness_defeat import captivity_start_wilderness_defeat_menu
from game_menus.mnu_captivity_start_wilderness_surrender import captivity_start_wilderness_surrender_menu
from game_menus.mnu_captivity_wilderness_check import captivity_wilderness_check_menu
from game_menus.mnu_captivity_wilderness_taken_prisoner import captivity_wilderness_taken_prisoner_menu
from game_menus.mnu_castle_attack_walls_simulate import castle_attack_walls_simulate_menu
from game_menus.mnu_castle_attack_walls_with_allies_simulate import castle_attack_walls_with_allies_simulate_menu
from game_menus.mnu_castle_besiege import castle_besiege_menu
from game_menus.mnu_castle_besiege_inner_battle import castle_besiege_inner_battle_menu
from game_menus.mnu_castle_entry_denied import castle_entry_denied_menu
from game_menus.mnu_castle_entry_granted import castle_entry_granted_menu
from game_menus.mnu_castle_guard import castle_guard_menu
from game_menus.mnu_castle_meeting import castle_meeting_menu
from game_menus.mnu_castle_meeting_selected import castle_meeting_selected_menu
from game_menus.mnu_castle_outside import castle_outside_menu
from game_menus.mnu_castle_taken import castle_taken_menu
from game_menus.mnu_castle_taken_2 import castle_taken_2_menu
from game_menus.mnu_castle_taken_by_friends import castle_taken_by_friends_menu
from game_menus.mnu_cattle_herd import cattle_herd_menu
from game_menus.mnu_cattle_herd_kill import cattle_herd_kill_menu
from game_menus.mnu_cattle_herd_kill_end import cattle_herd_kill_end_menu
from game_menus.mnu_center_improve import center_improve_menu
from game_menus.mnu_center_manage import center_manage_menu
from game_menus.mnu_center_reports import center_reports_menu
from game_menus.mnu_character_report import character_report_menu
from game_menus.mnu_cheat_change_weather import cheat_change_weather_menu
from game_menus.mnu_cheat_find_item import cheat_find_item_menu
from game_menus.mnu_cheat_reports import cheat_reports_menu
from game_menus.mnu_choose_banner import choose_banner_menu
from game_menus.mnu_choose_skill import choose_skill_menu
from game_menus.mnu_close import close_menu
from game_menus.mnu_collect_taxes import collect_taxes_menu
from game_menus.mnu_collect_taxes_complete import collect_taxes_complete_menu
from game_menus.mnu_collect_taxes_failed import collect_taxes_failed_menu
from game_menus.mnu_collect_taxes_rebels_killed import collect_taxes_rebels_killed_menu
from game_menus.mnu_collect_taxes_revolt import collect_taxes_revolt_menu
from game_menus.mnu_collect_taxes_revolt_warning import collect_taxes_revolt_warning_menu
from game_menus.mnu_companion_report import companion_report_menu
from game_menus.mnu_construct_ladders import construct_ladders_menu
from game_menus.mnu_construct_siege_tower import construct_siege_tower_menu
from game_menus.mnu_content_options import content_options_menu
from game_menus.mnu_courtship_relations import courtship_relations_menu
from game_menus.mnu_custom_battle_end import custom_battle_end_menu
from game_menus.mnu_custom_battle_scene import custom_battle_scene_menu
from game_menus.mnu_cut_siege_without_fight import cut_siege_without_fight_menu
from game_menus.mnu_debug_alert_from_s65 import debug_alert_from_s65_menu
from game_menus.mnu_dhorak_keep import dhorak_keep_menu
from game_menus.mnu_dickplo_town_manage import dickplo_town_manage_menu
from game_menus.mnu_disembark import disembark_menu
from game_menus.mnu_display_party_slots import display_party_slots_menu
from game_menus.mnu_display_troop_slots import display_troop_slots_menu
from game_menus.mnu_dplmc_affiliate_end import dplmc_affiliate_end_menu
from game_menus.mnu_dplmc_affiliated_family_report import dplmc_affiliated_family_report_menu
from game_menus.mnu_dplmc_auto_loot import dplmc_auto_loot_menu
from game_menus.mnu_dplmc_chamberlain_confirm import dplmc_chamberlain_confirm_menu
from game_menus.mnu_dplmc_chancellor_confirm import dplmc_chancellor_confirm_menu
from game_menus.mnu_dplmc_choose_disguise import dplmc_choose_disguise_menu
from game_menus.mnu_dplmc_constable_confirm import dplmc_constable_confirm_menu
from game_menus.mnu_dplmc_deny_terms import dplmc_deny_terms_menu
from game_menus.mnu_dplmc_deserters import dplmc_deserters_menu
from game_menus.mnu_dplmc_dictate_terms import dplmc_dictate_terms_menu
from game_menus.mnu_dplmc_domestic_policy import dplmc_domestic_policy_menu
from game_menus.mnu_dplmc_economic_report import dplmc_economic_report_menu
from game_menus.mnu_dplmc_manage_loot_pool import dplmc_manage_loot_pool_menu
from game_menus.mnu_dplmc_messenger import dplmc_messenger_menu
from game_menus.mnu_dplmc_negotiate_besieger import dplmc_negotiate_besieger_menu
from game_menus.mnu_dplmc_notification_alliance_declared import dplmc_notification_alliance_declared_menu
from game_menus.mnu_dplmc_notification_alliance_expired import dplmc_notification_alliance_expired_menu
from game_menus.mnu_dplmc_notification_appoint_chamberlain import dplmc_notification_appoint_chamberlain_menu
from game_menus.mnu_dplmc_notification_appoint_chancellor import dplmc_notification_appoint_chancellor_menu
from game_menus.mnu_dplmc_notification_appoint_constable import dplmc_notification_appoint_constable_menu
from game_menus.mnu_dplmc_notification_defensive_declared import dplmc_notification_defensive_declared_menu
from game_menus.mnu_dplmc_notification_defensive_expired import dplmc_notification_defensive_expired_menu
from game_menus.mnu_dplmc_notification_nonaggression_declared import dplmc_notification_nonaggression_declared_menu
from game_menus.mnu_dplmc_notification_riot import dplmc_notification_riot_menu
from game_menus.mnu_dplmc_notification_trade_declared import dplmc_notification_trade_declared_menu
from game_menus.mnu_dplmc_notification_trade_expired import dplmc_notification_trade_expired_menu
from game_menus.mnu_dplmc_preferences import dplmc_preferences_menu
from game_menus.mnu_dplmc_question_alliance_offer import dplmc_question_alliance_offer_menu
from game_menus.mnu_dplmc_question_defensive_offer import dplmc_question_defensive_offer_menu
from game_menus.mnu_dplmc_question_nonaggression_offer import dplmc_question_nonaggression_offer_menu
from game_menus.mnu_dplmc_question_trade_offer import dplmc_question_trade_offer_menu
from game_menus.mnu_dplmc_riot_negotiate import dplmc_riot_negotiate_menu
from game_menus.mnu_dplmc_scout import dplmc_scout_menu
from game_menus.mnu_dplmc_start_select_prejudice import dplmc_start_select_prejudice_menu
from game_menus.mnu_dplmc_town_riot_removed import dplmc_town_riot_removed_menu
from game_menus.mnu_dplmc_trade_auto_buy_food_begin import dplmc_trade_auto_buy_food_begin_menu
from game_menus.mnu_dplmc_trade_auto_sell_begin import dplmc_trade_auto_sell_begin_menu
from game_menus.mnu_dplmc_village_riot_removed import dplmc_village_riot_removed_menu
from game_menus.mnu_dplmc_village_riot_result import dplmc_village_riot_result_menu
from game_menus.mnu_encounter_retreat import encounter_retreat_menu
from game_menus.mnu_encounter_retreat_confirm import encounter_retreat_confirm_menu
from game_menus.mnu_end_game import end_game_menu
from game_menus.mnu_enemy_offer_ransom_for_prisoner import enemy_offer_ransom_for_prisoner_menu
from game_menus.mnu_enemy_slipped_away import enemy_slipped_away_menu
from game_menus.mnu_enter_your_own_castle import enter_your_own_castle_menu
from game_menus.mnu_establish_court import establish_court_menu
from game_menus.mnu_export_import import export_import_menu
from game_menus.mnu_faction_orders import faction_orders_menu
from game_menus.mnu_faction_relations_report import faction_relations_report_menu
from game_menus.mnu_four_ways_inn import four_ways_inn_menu
from game_menus.mnu_fuck import fuck_menu
from game_menus.mnu_fuck_2 import fuck_2_menu
from game_menus.mnu_fuck_3 import fuck_3_menu
from game_menus.mnu_fuck_encounter import fuck_encounter_menu
from game_menus.mnu_fucked_by_enemy import fucked_by_enemy_menu
from game_menus.mnu_fucked_by_enemy_prison import fucked_by_enemy_prison_menu
from game_menus.mnu_garden import garden_menu
from game_menus.mnu_give_center_to_player import give_center_to_player_menu
from game_menus.mnu_give_center_to_player_2 import give_center_to_player_2_menu
from game_menus.mnu_invite_player_to_faction import invite_player_to_faction_menu
from game_menus.mnu_invite_player_to_faction_accepted import invite_player_to_faction_accepted_menu
from game_menus.mnu_invite_player_to_faction_without_center import invite_player_to_faction_without_center_menu
from game_menus.mnu_join_battle import join_battle_menu
from game_menus.mnu_join_order_attack import join_order_attack_menu
from game_menus.mnu_join_siege_outside import join_siege_outside_menu
from game_menus.mnu_kill_local_merchant_begin import kill_local_merchant_begin_menu
from game_menus.mnu_kingdom_army_follow_failed import kingdom_army_follow_failed_menu
from game_menus.mnu_kingdom_army_quest_join_siege_order import kingdom_army_quest_join_siege_order_menu
from game_menus.mnu_kingdom_army_quest_messenger import kingdom_army_quest_messenger_menu
from game_menus.mnu_kingdom_army_quest_report_to_army import kingdom_army_quest_report_to_army_menu
from game_menus.mnu_lady_visit import lady_visit_menu
from game_menus.mnu_leave_faction import leave_faction_menu
from game_menus.mnu_lord_relations import lord_relations_menu
from game_menus.mnu_lost_tavern_duel import lost_tavern_duel_menu
from game_menus.mnu_marshall_selection_candidate_ask import marshall_selection_candidate_ask_menu
from game_menus.mnu_minister_confirm import minister_confirm_menu
from game_menus.mnu_notification_border_incident import notification_border_incident_menu
from game_menus.mnu_notification_casus_belli_expired import notification_casus_belli_expired_menu
from game_menus.mnu_notification_center_lost import notification_center_lost_menu
from game_menus.mnu_notification_center_under_siege import notification_center_under_siege_menu
from game_menus.mnu_notification_court_lost import notification_court_lost_menu
from game_menus.mnu_notification_faction_defeated import notification_faction_defeated_menu
from game_menus.mnu_notification_feast_quest_expired import notification_feast_quest_expired_menu
from game_menus.mnu_notification_lady_requests_visit import notification_lady_requests_visit_menu
from game_menus.mnu_notification_lord_defects import notification_lord_defects_menu
from game_menus.mnu_notification_oath_renounced_faction_defeated import notification_oath_renounced_faction_defeated_menu
from game_menus.mnu_notification_one_faction_left import notification_one_faction_left_menu
from game_menus.mnu_notification_peace_declared import notification_peace_declared_menu
from game_menus.mnu_notification_player_faction_active import notification_player_faction_active_menu
from game_menus.mnu_notification_player_faction_deactive import notification_player_faction_deactive_menu
from game_menus.mnu_notification_player_faction_political_issue_resolved import notification_player_faction_political_issue_resolved_menu
from game_menus.mnu_notification_player_faction_political_issue_resolved_for_player import notification_player_faction_political_issue_resolved_for_player_menu
from game_menus.mnu_notification_player_feast_in_progress import notification_player_feast_in_progress_menu
from game_menus.mnu_notification_player_kingdom_holds_feast import notification_player_kingdom_holds_feast_menu
from game_menus.mnu_notification_player_should_consult import notification_player_should_consult_menu
from game_menus.mnu_notification_player_wedding_day import notification_player_wedding_day_menu
from game_menus.mnu_notification_rebels_switched_to_faction import notification_rebels_switched_to_faction_menu
from game_menus.mnu_notification_relieved_as_marshal import notification_relieved_as_marshal_menu
from game_menus.mnu_notification_sortie_possible import notification_sortie_possible_menu
from game_menus.mnu_notification_treason_indictment import notification_treason_indictment_menu
from game_menus.mnu_notification_troop_joined_players_faction import notification_troop_joined_players_faction_menu
from game_menus.mnu_notification_troop_left_players_faction import notification_troop_left_players_faction_menu
from game_menus.mnu_notification_truce_expired import notification_truce_expired_menu
from game_menus.mnu_notification_village_raid_started import notification_village_raid_started_menu
from game_menus.mnu_notification_village_raided import notification_village_raided_menu
from game_menus.mnu_notification_war_declared import notification_war_declared_menu
from game_menus.mnu_oath_fulfilled import oath_fulfilled_menu
from game_menus.mnu_order_attack_2 import order_attack_2_menu
from game_menus.mnu_order_attack_begin import order_attack_begin_menu
from game_menus.mnu_party_cheat import party_cheat_menu
from game_menus.mnu_past_life_explanation import past_life_explanation_menu
from game_menus.mnu_permanent_damage import permanent_damage_menu
from game_menus.mnu_pre_join import pre_join_menu
from game_menus.mnu_price_and_production import price_and_production_menu
from game_menus.mnu_question_peace_offer import question_peace_offer_menu
from game_menus.mnu_recruit_volunteers import recruit_volunteers_menu
from game_menus.mnu_recruit_volunteers_dickplo_main import recruit_volunteers_dickplo_main_menu
from game_menus.mnu_rename_court import rename_court_menu
from game_menus.mnu_reports import reports_menu
from game_menus.mnu_reports_character import reports_character_menu
from game_menus.mnu_reports_economy import reports_economy_menu
from game_menus.mnu_reports_faction import reports_faction_menu
from game_menus.mnu_requested_castle_granted_to_another import requested_castle_granted_to_another_menu
from game_menus.mnu_requested_castle_granted_to_another_female import requested_castle_granted_to_another_female_menu
from game_menus.mnu_requested_castle_granted_to_player import requested_castle_granted_to_player_menu
from game_menus.mnu_requested_castle_granted_to_player_husband import requested_castle_granted_to_player_husband_menu
from game_menus.mnu_retirement_verify import retirement_verify_menu
from game_menus.mnu_salt_mine import salt_mine_menu
from game_menus.mnu_ship_reembark import ship_reembark_menu
from game_menus.mnu_siege_attack_meets_sally import siege_attack_meets_sally_menu
from game_menus.mnu_siege_join_defense import siege_join_defense_menu
from game_menus.mnu_siege_started_defender import siege_started_defender_menu
from game_menus.mnu_simple_encounter import simple_encounter_menu
from game_menus.mnu_sneak_into_town_caught import sneak_into_town_caught_menu
from game_menus.mnu_sneak_into_town_caught_dispersed_guards import sneak_into_town_caught_dispersed_guards_menu
from game_menus.mnu_sneak_into_town_caught_ran_away import sneak_into_town_caught_ran_away_menu
from game_menus.mnu_sneak_into_town_suceeded import sneak_into_town_suceeded_menu
from game_menus.mnu_start_character_1 import start_character_1_menu
from game_menus.mnu_start_character_2 import start_character_2_menu
from game_menus.mnu_start_character_3 import start_character_3_menu
from game_menus.mnu_start_character_4 import start_character_4_menu
from game_menus.mnu_start_game_0 import start_game_0_menu
from game_menus.mnu_start_game_1 import start_game_1_menu
from game_menus.mnu_start_game_3 import start_game_3_menu
from game_menus.mnu_start_phase_2 import start_phase_2_menu
from game_menus.mnu_start_phase_2_5 import start_phase_2_5_menu
from game_menus.mnu_start_phase_3 import start_phase_3_menu
from game_menus.mnu_start_phase_4 import start_phase_4_menu
from game_menus.mnu_startgame_mod_options import startgame_mod_options_menu
from game_menus.mnu_test_scene import test_scene_menu
from game_menus.mnu_total_defeat import total_defeat_menu
from game_menus.mnu_total_victory import total_victory_menu
from game_menus.mnu_tournament_bet import tournament_bet_menu
from game_menus.mnu_tournament_bet_confirm import tournament_bet_confirm_menu
from game_menus.mnu_tournament_participants import tournament_participants_menu
from game_menus.mnu_tournament_withdraw_verify import tournament_withdraw_verify_menu
from game_menus.mnu_town import town_menu
from game_menus.mnu_town_bandits_failed import town_bandits_failed_menu
from game_menus.mnu_town_bandits_succeeded import town_bandits_succeeded_menu
from game_menus.mnu_town_cheats import town_cheats_menu
from game_menus.mnu_town_cheats_2 import town_cheats_2_menu
from game_menus.mnu_town_hire_cutthroats import town_hire_cutthroats_menu
from game_menus.mnu_town_hire_farmers import town_hire_farmers_menu
from game_menus.mnu_town_hire_knights import town_hire_knights_menu
from game_menus.mnu_town_hire_troops import town_hire_troops_menu
from game_menus.mnu_town_pre_hire_troops import town_pre_hire_troops_menu
from game_menus.mnu_town_tavern_prostitution import town_tavern_prostitution_menu
from game_menus.mnu_town_tavern_prostitution_results import town_tavern_prostitution_results_menu
from game_menus.mnu_town_tournament import town_tournament_menu
from game_menus.mnu_town_tournament_lost import town_tournament_lost_menu
from game_menus.mnu_town_tournament_won import town_tournament_won_menu
from game_menus.mnu_town_tournament_won_by_another import town_tournament_won_by_another_menu
from game_menus.mnu_town_trade import town_trade_menu
from game_menus.mnu_town_trade_assessment import town_trade_assessment_menu
from game_menus.mnu_town_trade_assessment_begin import town_trade_assessment_begin_menu
from game_menus.mnu_train_peasants_against_bandits import train_peasants_against_bandits_menu
from game_menus.mnu_train_peasants_against_bandits_attack import train_peasants_against_bandits_attack_menu
from game_menus.mnu_train_peasants_against_bandits_attack_result import train_peasants_against_bandits_attack_result_menu
from game_menus.mnu_train_peasants_against_bandits_ready import train_peasants_against_bandits_ready_menu
from game_menus.mnu_train_peasants_against_bandits_success import train_peasants_against_bandits_success_menu
from game_menus.mnu_train_peasants_against_bandits_training_result import train_peasants_against_bandits_training_result_menu
from game_menus.mnu_training_ground import training_ground_menu
from game_menus.mnu_training_ground_description import training_ground_description_menu
from game_menus.mnu_training_ground_selection_details_melee_1 import training_ground_selection_details_melee_1_menu
from game_menus.mnu_training_ground_selection_details_melee_2 import training_ground_selection_details_melee_2_menu
from game_menus.mnu_training_ground_selection_details_mounted import training_ground_selection_details_mounted_menu
from game_menus.mnu_training_ground_selection_details_ranged_1 import training_ground_selection_details_ranged_1_menu
from game_menus.mnu_training_ground_selection_details_ranged_2 import training_ground_selection_details_ranged_2_menu
from game_menus.mnu_training_ground_training_result import training_ground_training_result_menu
from game_menus.mnu_tutorial import tutorial_menu
from game_menus.mnu_village import village_menu
from game_menus.mnu_village_enslave_complete import village_enslave_complete_menu
from game_menus.mnu_village_hostile_action import village_hostile_action_menu
from game_menus.mnu_village_hunt_down_fugitive_defeated import village_hunt_down_fugitive_defeated_menu
from game_menus.mnu_village_hunt_down_fugitive_persuaded import village_hunt_down_fugitive_persuaded_menu
from game_menus.mnu_village_infest_bandits_result import village_infest_bandits_result_menu
from game_menus.mnu_village_infestation_removed import village_infestation_removed_menu
from game_menus.mnu_village_loot_complete import village_loot_complete_menu
from game_menus.mnu_village_loot_continue import village_loot_continue_menu
from game_menus.mnu_village_loot_defeat import village_loot_defeat_menu
from game_menus.mnu_village_loot_no_resist import village_loot_no_resist_menu
from game_menus.mnu_village_start_attack import village_start_attack_menu
from game_menus.mnu_village_steal_cattle import village_steal_cattle_menu
from game_menus.mnu_village_steal_cattle_confirm import village_steal_cattle_confirm_menu
from game_menus.mnu_village_take_food import village_take_food_menu
from game_menus.mnu_village_take_food_confirm import village_take_food_confirm_menu
from game_menus.mnu_zendar import zendar_menu

game_menus = []
# CRITICAL: The order of .extend() calls determines menu IDs at compile time.
# The Warband engine hardcodes menu ID 0 as the new-game start menu.
# This ordering must match the original pre-atomization ID_menus.py exactly.
# DO NOT sort alphabetically — doing so will break the game.
game_menus.extend(start_game_0_menu)                                              # 0
game_menus.extend(start_phase_2_menu)                                             # 1
game_menus.extend(start_game_3_menu)                                              # 2
game_menus.extend(tutorial_menu)                                                  # 3
game_menus.extend(reports_menu)                                                   # 4
game_menus.extend(custom_battle_scene_menu)                                       # 5
game_menus.extend(custom_battle_end_menu)                                         # 6
game_menus.extend(start_game_1_menu)                                              # 7
game_menus.extend(start_character_1_menu)                                         # 8
game_menus.extend(start_character_2_menu)                                         # 9
game_menus.extend(start_character_3_menu)                                         # 10
game_menus.extend(start_character_4_menu)                                         # 11
game_menus.extend(choose_skill_menu)                                              # 12
game_menus.extend(past_life_explanation_menu)                                     # 13
game_menus.extend(auto_return_menu)                                               # 14
# game_menus.extend(morale_report_menu)                                           # 15 (unused - replaced by combined report)
game_menus.extend(courtship_relations_menu)                                       # 16
game_menus.extend(lord_relations_menu)                                            # 17
game_menus.extend(companion_report_menu)                                          # 18
game_menus.extend(faction_orders_menu)                                            # 19
game_menus.extend(character_report_menu)                                          # 20
# game_menus.extend(party_size_report_menu)                                       # 21 (unused - replaced by combined report)
game_menus.extend(faction_relations_report_menu)                                  # 22
game_menus.extend(camp_menu)                                                      # 23
game_menus.extend(camp_cheat_menu)                                                # 24
game_menus.extend(camp_cheat_player_stats_menu)                                   # 25
game_menus.extend(camp_cheat_party_menu)
game_menus.extend(camp_cheat_world_menu)
game_menus.extend(camp_cheat_player_kingdom_menu)
game_menus.extend(camp_cheat_debug_menu)
# game_menus.extend(camp_cheat_adv_menu)                                          # 25 (unused - merged into camp_cheat)
game_menus.extend(cheat_find_item_menu)                                           # 26
game_menus.extend(cheat_change_weather_menu)                                      # 27
game_menus.extend(camp_action_menu)                                               # 28
game_menus.extend(camp_recruit_prisoners_menu)                                    # 29
game_menus.extend(camp_no_prisoners_menu)                                         # 30
game_menus.extend(camp_action_sort_inventory_menu)                                # 31
game_menus.extend(camp_action_read_book_menu)                                     # 32
game_menus.extend(camp_action_read_book_start_menu)                               # 33
game_menus.extend(retirement_verify_menu)                                         # 34
game_menus.extend(end_game_menu)                                                  # 35
game_menus.extend(cattle_herd_menu)                                               # 36
game_menus.extend(cattle_herd_kill_menu)                                          # 37
game_menus.extend(cattle_herd_kill_end_menu)                                      # 38
game_menus.extend(arena_duel_fight_menu)                                          # 39
game_menus.extend(arena_duel_conclusion_menu)                                     # 40
game_menus.extend(simple_encounter_menu)                                          # 41
game_menus.extend(encounter_retreat_confirm_menu)                                 # 42
game_menus.extend(encounter_retreat_menu)                                         # 43
game_menus.extend(order_attack_begin_menu)                                        # 44
game_menus.extend(order_attack_2_menu)                                            # 45
game_menus.extend(battle_debrief_menu)                                            # 46
game_menus.extend(total_victory_menu)                                             # 47
game_menus.extend(enemy_slipped_away_menu)                                        # 48
game_menus.extend(total_defeat_menu)                                              # 49
game_menus.extend(permanent_damage_menu)                                          # 50
game_menus.extend(pre_join_menu)                                                  # 51
game_menus.extend(join_battle_menu)                                               # 52
game_menus.extend(join_order_attack_menu)                                         # 53
game_menus.extend(zendar_menu)                                                    # 54
game_menus.extend(salt_mine_menu)                                                 # 55
game_menus.extend(four_ways_inn_menu)                                             # 56
game_menus.extend(test_scene_menu)                                                # 57
game_menus.extend(battlefields_menu)                                              # 58
game_menus.extend(dhorak_keep_menu)                                               # 59
game_menus.extend(join_siege_outside_menu)                                        # 60
game_menus.extend(cut_siege_without_fight_menu)                                   # 61
game_menus.extend(besiegers_camp_with_allies_menu)                                # 62
game_menus.extend(castle_outside_menu)                                            # 63
game_menus.extend(castle_guard_menu)                                              # 64
game_menus.extend(castle_entry_granted_menu)                                      # 65
game_menus.extend(castle_entry_denied_menu)                                       # 66
game_menus.extend(castle_meeting_menu)                                            # 67
game_menus.extend(castle_meeting_selected_menu)                                   # 68
game_menus.extend(castle_besiege_menu)                                            # 69
game_menus.extend(siege_attack_meets_sally_menu)                                  # 70
game_menus.extend(castle_besiege_inner_battle_menu)                               # 71
game_menus.extend(construct_ladders_menu)                                         # 72
game_menus.extend(construct_siege_tower_menu)                                     # 73
game_menus.extend(castle_attack_walls_simulate_menu)                              # 74
game_menus.extend(castle_attack_walls_with_allies_simulate_menu)                  # 75
game_menus.extend(castle_taken_by_friends_menu)                                   # 76
game_menus.extend(castle_taken_menu)                                              # 77
game_menus.extend(castle_taken_2_menu)                                            # 78
game_menus.extend(requested_castle_granted_to_player_menu)                        # 79
game_menus.extend(requested_castle_granted_to_player_husband_menu)                # 80
game_menus.extend(requested_castle_granted_to_another_menu)                       # 81
game_menus.extend(requested_castle_granted_to_another_female_menu)                # 82
game_menus.extend(leave_faction_menu)                                             # 83
game_menus.extend(give_center_to_player_menu)                                     # 84
game_menus.extend(give_center_to_player_2_menu)                                   # 85
game_menus.extend(oath_fulfilled_menu)                                            # 86
game_menus.extend(siege_started_defender_menu)                                    # 87
game_menus.extend(siege_join_defense_menu)                                        # 88
game_menus.extend(enter_your_own_castle_menu)                                     # 89
game_menus.extend(village_menu)                                                   # 90
game_menus.extend(village_hostile_action_menu)                                    # 91
game_menus.extend(recruit_volunteers_dickplo_main_menu)                           # 92
game_menus.extend(recruit_volunteers_menu)                                        # 93
game_menus.extend(village_hunt_down_fugitive_defeated_menu)                       # 94
game_menus.extend(village_hunt_down_fugitive_persuaded_menu)                      # 95
game_menus.extend(village_infest_bandits_result_menu)                             # 96
game_menus.extend(village_infestation_removed_menu)                               # 97
game_menus.extend(center_manage_menu)                                             # 98
game_menus.extend(center_improve_menu)                                            # 99
game_menus.extend(town_bandits_failed_menu)                                       # 100
game_menus.extend(town_bandits_succeeded_menu)                                    # 101
game_menus.extend(village_steal_cattle_confirm_menu)                              # 102
game_menus.extend(village_steal_cattle_menu)                                      # 103
game_menus.extend(village_take_food_confirm_menu)                                 # 104
game_menus.extend(village_take_food_menu)                                         # 105
game_menus.extend(village_start_attack_menu)                                      # 106
game_menus.extend(village_loot_no_resist_menu)                                    # 107
game_menus.extend(village_loot_complete_menu)                                     # 108
game_menus.extend(village_enslave_complete_menu)                                  # 109
game_menus.extend(village_loot_defeat_menu)                                       # 110
game_menus.extend(village_loot_continue_menu)                                     # 111
game_menus.extend(close_menu)                                                     # 112
game_menus.extend(town_menu)                                                      # 113
game_menus.extend(cannot_enter_court_menu)                                        # 114
game_menus.extend(lady_visit_menu)                                                # 115
game_menus.extend(town_tournament_lost_menu)                                      # 116
game_menus.extend(town_tournament_won_menu)                                       # 117
game_menus.extend(town_tournament_won_by_another_menu)                            # 118
game_menus.extend(town_tournament_menu)                                           # 119
game_menus.extend(tournament_withdraw_verify_menu)                                # 120
game_menus.extend(tournament_bet_menu)                                            # 121
game_menus.extend(tournament_bet_confirm_menu)                                    # 122
game_menus.extend(tournament_participants_menu)                                   # 123
game_menus.extend(collect_taxes_menu)                                             # 124
game_menus.extend(collect_taxes_complete_menu)                                     # 125
game_menus.extend(collect_taxes_rebels_killed_menu)                               # 126
game_menus.extend(collect_taxes_failed_menu)                                      # 127
game_menus.extend(collect_taxes_revolt_warning_menu)                              # 128
game_menus.extend(collect_taxes_revolt_menu)                                      # 129
game_menus.extend(train_peasants_against_bandits_menu)                            # 130
game_menus.extend(train_peasants_against_bandits_ready_menu)                      # 131
game_menus.extend(train_peasants_against_bandits_training_result_menu)            # 132
game_menus.extend(train_peasants_against_bandits_attack_menu)                     # 133
game_menus.extend(train_peasants_against_bandits_attack_result_menu)              # 134
game_menus.extend(train_peasants_against_bandits_success_menu)                    # 135
game_menus.extend(disembark_menu)                                                 # 136
game_menus.extend(ship_reembark_menu)                                             # 137
game_menus.extend(center_reports_menu)                                            # 138
game_menus.extend(price_and_production_menu)                                      # 139
game_menus.extend(town_trade_menu)                                                # 140
game_menus.extend(dickplo_town_manage_menu)                                       # 141
game_menus.extend(dplmc_trade_auto_sell_begin_menu)                               # 142
game_menus.extend(dplmc_trade_auto_buy_food_begin_menu)                           # 143
game_menus.extend(town_trade_assessment_begin_menu)                               # 144
game_menus.extend(town_pre_hire_troops_menu)                                      # 145
game_menus.extend(town_hire_troops_menu)                                          # 146
game_menus.extend(town_hire_farmers_menu)                                         # 147
game_menus.extend(town_hire_cutthroats_menu)                                      # 148
game_menus.extend(town_hire_knights_menu)                                         # 149
game_menus.extend(town_trade_assessment_menu)                                     # 150
game_menus.extend(sneak_into_town_suceeded_menu)                                  # 151
game_menus.extend(sneak_into_town_caught_menu)                                    # 152
game_menus.extend(sneak_into_town_caught_dispersed_guards_menu)                   # 153
game_menus.extend(sneak_into_town_caught_ran_away_menu)                           # 154
game_menus.extend(enemy_offer_ransom_for_prisoner_menu)                           # 155
game_menus.extend(training_ground_menu)                                           # 156
game_menus.extend(training_ground_selection_details_melee_1_menu)                 # 157
game_menus.extend(training_ground_selection_details_melee_2_menu)                 # 158
game_menus.extend(training_ground_selection_details_mounted_menu)                 # 159
game_menus.extend(training_ground_selection_details_ranged_1_menu)                # 160
game_menus.extend(training_ground_selection_details_ranged_2_menu)                # 161
game_menus.extend(training_ground_description_menu)                               # 162
game_menus.extend(training_ground_training_result_menu)                           # 163
game_menus.extend(marshall_selection_candidate_ask_menu)                          # 164
game_menus.extend(captivity_avoid_wilderness_menu)                                # 165
game_menus.extend(captivity_start_wilderness_menu)                                # 166
game_menus.extend(captivity_start_wilderness_surrender_menu)                      # 167
game_menus.extend(captivity_start_wilderness_defeat_menu)                         # 168
game_menus.extend(captivity_start_castle_surrender_menu)                          # 169
game_menus.extend(captivity_start_castle_defeat_menu)                             # 170
game_menus.extend(captivity_start_under_siege_defeat_menu)                        # 171
game_menus.extend(captivity_wilderness_taken_prisoner_menu)                       # 172
game_menus.extend(captivity_wilderness_check_menu)                                # 173
game_menus.extend(captivity_end_wilderness_escape_menu)                           # 174
game_menus.extend(captivity_castle_taken_prisoner_menu)                           # 175
game_menus.extend(captivity_rescue_lord_taken_prisoner_menu)                      # 176
game_menus.extend(captivity_castle_check_menu)                                    # 177
game_menus.extend(captivity_end_exchanged_with_prisoner_menu)                     # 178
game_menus.extend(captivity_end_propose_ransom_menu)                              # 179
game_menus.extend(captivity_castle_remain_menu)                                   # 180
game_menus.extend(kingdom_army_quest_report_to_army_menu)                         # 181
game_menus.extend(kingdom_army_quest_messenger_menu)                              # 182
game_menus.extend(kingdom_army_quest_join_siege_order_menu)                       # 183
game_menus.extend(kingdom_army_follow_failed_menu)                                # 184
game_menus.extend(invite_player_to_faction_without_center_menu)                   # 185
game_menus.extend(invite_player_to_faction_menu)                                  # 186
game_menus.extend(invite_player_to_faction_accepted_menu)                         # 187
game_menus.extend(question_peace_offer_menu)                                      # 188
game_menus.extend(notification_truce_expired_menu)                                # 189
game_menus.extend(notification_feast_quest_expired_menu)                          # 190
game_menus.extend(notification_sortie_possible_menu)                              # 191
game_menus.extend(notification_casus_belli_expired_menu)                          # 192
game_menus.extend(notification_lord_defects_menu)                                 # 193
game_menus.extend(notification_treason_indictment_menu)                           # 194
game_menus.extend(notification_border_incident_menu)                              # 195
game_menus.extend(notification_player_faction_active_menu)                        # 196
game_menus.extend(minister_confirm_menu)                                          # 197
game_menus.extend(notification_court_lost_menu)                                   # 198
game_menus.extend(notification_player_faction_deactive_menu)                      # 199
game_menus.extend(notification_player_wedding_day_menu)                           # 200
game_menus.extend(notification_player_kingdom_holds_feast_menu)                   # 201
game_menus.extend(notification_center_under_siege_menu)                           # 202
game_menus.extend(notification_village_raided_menu)                               # 203
game_menus.extend(notification_village_raid_started_menu)                         # 204
game_menus.extend(notification_one_faction_left_menu)                             # 205
game_menus.extend(notification_oath_renounced_faction_defeated_menu)              # 206
game_menus.extend(notification_center_lost_menu)                                  # 207
game_menus.extend(notification_troop_left_players_faction_menu)                   # 208
game_menus.extend(notification_troop_joined_players_faction_menu)                 # 209
game_menus.extend(notification_war_declared_menu)                                 # 210
game_menus.extend(notification_peace_declared_menu)                               # 211
game_menus.extend(notification_faction_defeated_menu)                             # 212
game_menus.extend(notification_rebels_switched_to_faction_menu)                   # 213
game_menus.extend(notification_player_should_consult_menu)                        # 214
game_menus.extend(notification_player_feast_in_progress_menu)                     # 215
game_menus.extend(notification_lady_requests_visit_menu)                          # 216
game_menus.extend(garden_menu)                                                    # 217
game_menus.extend(kill_local_merchant_begin_menu)                                 # 218
game_menus.extend(debug_alert_from_s65_menu)                                      # 219
game_menus.extend(auto_return_to_map_menu)                                        # 220
game_menus.extend(bandit_lair_menu)                                               # 221
game_menus.extend(notification_player_faction_political_issue_resolved_menu)      # 222
game_menus.extend(notification_player_faction_political_issue_resolved_for_player_menu) # 223
game_menus.extend(start_phase_2_5_menu)                                           # 224
game_menus.extend(start_phase_3_menu)                                             # 225
game_menus.extend(start_phase_4_menu)                                             # 226
game_menus.extend(lost_tavern_duel_menu)                                          # 227
game_menus.extend(establish_court_menu)                                           # 228
game_menus.extend(notification_relieved_as_marshal_menu)                          # 229
game_menus.extend(dplmc_manage_loot_pool_menu)                                    # 230
game_menus.extend(dplmc_auto_loot_menu)                                           # 231
game_menus.extend(dplmc_notification_alliance_declared_menu)                      # 232
game_menus.extend(dplmc_notification_defensive_declared_menu)                     # 233
game_menus.extend(dplmc_notification_trade_declared_menu)                         # 234
game_menus.extend(dplmc_notification_nonaggression_declared_menu)                 # 235
game_menus.extend(dplmc_question_alliance_offer_menu)                             # 236
game_menus.extend(dplmc_question_defensive_offer_menu)                            # 237
game_menus.extend(dplmc_question_trade_offer_menu)                                # 238
game_menus.extend(dplmc_question_nonaggression_offer_menu)                        # 239
game_menus.extend(dplmc_notification_alliance_expired_menu)                       # 240
game_menus.extend(dplmc_notification_defensive_expired_menu)                      # 241
game_menus.extend(dplmc_notification_trade_expired_menu)                          # 242
game_menus.extend(dplmc_dictate_terms_menu)                                       # 243
game_menus.extend(dplmc_deny_terms_menu)                                          # 244
game_menus.extend(dplmc_village_riot_result_menu)                                 # 245
game_menus.extend(dplmc_village_riot_removed_menu)                                # 246
game_menus.extend(dplmc_town_riot_removed_menu)                                   # 247
game_menus.extend(dplmc_riot_negotiate_menu)                                      # 248
game_menus.extend(dplmc_notification_riot_menu)                                   # 249
game_menus.extend(dplmc_notification_appoint_chamberlain_menu)                    # 250
game_menus.extend(dplmc_chamberlain_confirm_menu)                                 # 251
game_menus.extend(dplmc_notification_appoint_constable_menu)                      # 252
game_menus.extend(dplmc_constable_confirm_menu)                                   # 253
game_menus.extend(dplmc_notification_appoint_chancellor_menu)                     # 254
game_menus.extend(dplmc_chancellor_confirm_menu)                                  # 255
game_menus.extend(dplmc_deserters_menu)                                           # 256
game_menus.extend(dplmc_negotiate_besieger_menu)                                  # 257
game_menus.extend(dplmc_messenger_menu)                                           # 258
game_menus.extend(dplmc_scout_menu)                                               # 259
game_menus.extend(dplmc_domestic_policy_menu)                                     # 260
game_menus.extend(dplmc_affiliate_end_menu)                                       # 261
game_menus.extend(dplmc_preferences_menu)                                         # 262
game_menus.extend(dplmc_affiliated_family_report_menu)                            # 263
game_menus.extend(dplmc_start_select_prejudice_menu)                              # 264
game_menus.extend(dplmc_economic_report_menu)                                     # 265
game_menus.extend(town_cheats_menu)                                               # 266
game_menus.extend(town_cheats_2_menu)                                             # 267
game_menus.extend(rename_court_menu)                                              # 268
game_menus.extend(export_import_menu)                                             # 269
game_menus.extend(display_party_slots_menu)                                       # 270
game_menus.extend(party_cheat_menu)                                               # 271
game_menus.extend(display_troop_slots_menu)                                       # 272
game_menus.extend(dplmc_choose_disguise_menu)                                     # 273
game_menus.extend(fuck_menu)                                                      # 274
game_menus.extend(fuck_2_menu)                                                    # 275
game_menus.extend(fuck_3_menu)                                                    # 276
game_menus.extend(fucked_by_enemy_menu)                                           # 277
game_menus.extend(fucked_by_enemy_prison_menu)                                    # 278
game_menus.extend(choose_banner_menu)                                             # 279
game_menus.extend(content_options_menu)                                           # 280
game_menus.extend(fuck_encounter_menu)                                            # 281
game_menus.extend(town_tavern_prostitution_menu)                                  # 282
game_menus.extend(town_tavern_prostitution_results_menu)                          # 283
game_menus.extend(buy_ship_menu)                                                  # 284
game_menus.extend(startgame_mod_options_menu)                                     # 285
game_menus.extend(auto_trade_menu)                                                # 286
# --- New menus added after atomization (not in original ID_menus.py) ---
game_menus.extend(cheat_reports_menu)
game_menus.extend(reports_character_menu)
game_menus.extend(reports_economy_menu)
game_menus.extend(reports_faction_menu)

import header_scenes
from template_tools import *
from module_scenes import scenes

sorted_scenes = sorted(scenes)
for i in xrange(len(sorted_scenes)):
  current_scene = list(sorted_scenes[i])
  current_scene[1] = get_flags_from_bitmap(header_scenes, "sf_", current_scene[1])
  sorted_scenes[i] = tuple(current_scene)

choose_scene_template = Game_Menu_Template(
  id="choose_scenes_",
  text="Choose a scene: (Page {current_page} of {num_pages})",
  optn_id="choose_scene_",
  optn_text="{list_item[0]}{list_item[1]}",
  optn_consq = [
    (jump_to_scene, "scn_{list_item[0]}"),
    (change_screen_mission)
  ]
)

game_menus += choose_scene_template.generate_menus(sorted_scenes)

# modmerger_start version=201 type=2
try:
    component_name = "game_menus"
    var_set = { "game_menus" : game_menus }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
try:
    var_set = { "game_menus" : game_menus }
    from xgm_mod_options_game_menus import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end
