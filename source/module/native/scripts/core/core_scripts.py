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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

####################################################################################################################
# CORE LOOPS & GAME SCRIPTS
# 
# This file contains the foundational scripts of Mount & Blade: Warband.
# Specifically: game_start, game_quick_start, triggers, and initialization loops.
####################################################################################################################

core_scripts = [
  #script_game_start:
  # This script is called when a new game is started
  # INPUT: none
  ("game_start",
   [
      (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),

#Decapitation settings
      (assign, "$g_decapitation_enabled", 0),
#CC
      # hp bars
      (assign, "$g_hp_bar_dis_limit", 30),
      (assign, "$g_hp_bar_ally", 0),
      (assign, "$g_hp_bar_enemy", 0),
      # (assign, "$g_name_of_ally", 0),
      # (assign, "$g_name_of_enemy", 1),

      # minimap off = -1
      # new style = 0
      # old style 60% = 1
      # old style 80% = 2
      # old style 100% = 3
      (assign, "$g_minimap_style", -1),
      (assign, "$g_show_regain_hp_info", 1),
#CC
      (assign, "$first_time", 0),	#squelch compiler warnings
      (assign, "$fuck_stamina", 1),
      (assign, "$g_sexual_content", 0),
	  (assign, "$g_nohomo", 1),
	  (assign, "$g_keep_companions", 0),
      (assign, "$g_dark_hunters_enabled", 0),
      (assign, "$g_realistic_wounding", 0),
      (assign, "$g_polygamy", 0),
    (assign, "$g_feast_dancers", 1),
	  (assign, "$g_enable_shield_bash", 2),
	  (assign, "$f_con", 0),
	  (assign, "$f_player_prost", 0),

	  (assign, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
	  (assign, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
	  (call_script, "script_set_custom_armor_slots"), # Custom armor init

      (try_for_range, ":edible", "itm_raw_date_fruit", food_end),
        (neq, ":edible", "itm_furs"),
        (item_set_slot, ":edible", slot_item_edible, 1),
      (try_end),

      (assign, "$g_player_luck", 200),
      (troop_set_slot, "trp_player", slot_troop_occupation, slto_kingdom_hero),
      (store_random_in_range, ":starting_training_ground", training_grounds_begin, training_grounds_end),
      (party_relocate_near_party, "p_main_party", ":starting_training_ground", 3),
      (str_store_troop_name, s5, "trp_player"),
      (party_set_name, "p_main_party", s5),
      (call_script, "script_update_party_creation_random_limits"),
      (assign, "$g_player_party_icon", -1),

      #Warband changes begin -- set this early
      (try_for_range, ":npc", 0, kingdom_ladies_end),
        (this_or_next|eq, ":npc", "trp_player"),
        (is_between, ":npc", active_npcs_begin, kingdom_ladies_end),
        (troop_set_slot, ":npc", slot_troop_father, -1),
        (troop_set_slot, ":npc", slot_troop_mother, -1),
        (troop_set_slot, ":npc", slot_troop_guardian, -1),
        (troop_set_slot, ":npc", slot_troop_spouse, -1),
        (troop_set_slot, ":npc", slot_troop_betrothed, -1),
        (troop_set_slot, ":npc", slot_troop_prisoner_of_party, -1),
        (troop_set_slot, ":npc", slot_lady_last_suitor, -1),
        (troop_set_slot, ":npc", slot_troop_stance_on_faction_issue, -1),
        (troop_set_slot, ":npc", slot_troop_courtesan, -1),

        (store_random_in_range, ":decision_seed", 0, 10000),
        (troop_set_slot, ":npc", slot_troop_set_decision_seed, ":decision_seed"),	#currently not used
        (troop_set_slot, ":npc", slot_troop_temp_decision_seed, ":decision_seed"),	#currently not used, holds for at least 24 hours
      (try_end),

      (assign, "$g_lord_long_term_count", 0),
      ##diplomacy start+ Clear faction leader/marshall, since 0 is the player
      (try_for_range, ":faction_no", 0, dplmc_factions_end),
         (neq, ":faction_no", "fac_player_faction"),
         (neq, ":faction_no", "fac_player_supporters_faction"),
         (faction_set_slot, ":faction_no", slot_faction_leader, -1),
         (faction_set_slot, ":faction_no", slot_faction_marshall, -1),
      (try_end),
      ##diplomacy end+

      (call_script, "script_initialize_banner_info"),
      (call_script, "script_initialize_item_info"),
      (call_script, "script_initialize_aristocracy"),
      (call_script, "script_initialize_npcs"),
      (assign, "$disable_npc_complaints", 0),
      #NPC companion changes end

      # Setting random feast time
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (store_random_in_range, ":last_feast_time", 0, 312), #240 + 72
        (val_mul, ":last_feast_time", -1),
        (faction_set_slot, ":faction_no", slot_faction_last_feast_start_time, ":last_feast_time"),
      (try_end),

      # Setting the random town sequence:
      (store_sub, ":num_towns", towns_end, towns_begin),
      (assign, ":num_iterations", ":num_towns"),
      (try_for_range, ":cur_town_no", 0, ":num_towns"),
        (troop_set_slot, "trp_random_town_sequence", ":cur_town_no", -1),
      (try_end),
      (assign, ":cur_town_no", 0),
      (try_for_range, ":unused", 0, ":num_iterations"),
        (store_random_in_range, ":random_no", 0, ":num_towns"),
        (assign, ":is_unique", 1),
        (try_for_range, ":cur_town_no_2", 0, ":num_towns"),
          (troop_slot_eq, "trp_random_town_sequence", ":cur_town_no_2", ":random_no"),
          (assign, ":is_unique", 0),
        (try_end),
        (try_begin),
          (eq, ":is_unique", 1),
          (troop_set_slot, "trp_random_town_sequence", ":cur_town_no", ":random_no"),
          (val_add, ":cur_town_no", 1),
        (else_try),
          (val_add, ":num_iterations", 1),
        (try_end),
      (try_end),

      # Cultures:
      (faction_set_slot, "fac_culture_1",  slot_faction_tier_1_troop, "trp_swadian_recruit"),
      (faction_set_slot, "fac_culture_1",  slot_faction_tier_2_troop, "trp_swadian_militia"),
      (faction_set_slot, "fac_culture_1",  slot_faction_tier_3_troop, "trp_swadian_footman"),
      (faction_set_slot, "fac_culture_1",  slot_faction_tier_4_troop, "trp_swadian_infantry"),
      (faction_set_slot, "fac_culture_1",  slot_faction_tier_5_troop, "trp_swadian_knight"),

      (faction_set_slot, "fac_culture_2", slot_faction_tier_1_troop, "trp_vaegir_recruit"),
      (faction_set_slot, "fac_culture_2", slot_faction_tier_2_troop, "trp_vaegir_footman"),
      (faction_set_slot, "fac_culture_2", slot_faction_tier_3_troop, "trp_vaegir_veteran"),
      (faction_set_slot, "fac_culture_2", slot_faction_tier_4_troop, "trp_vaegir_infantry"),
      (faction_set_slot, "fac_culture_2", slot_faction_tier_5_troop, "trp_vaegir_knight"),

      (faction_set_slot, "fac_culture_3", slot_faction_tier_1_troop, "trp_khergit_tribesman"),
      (faction_set_slot, "fac_culture_3", slot_faction_tier_2_troop, "trp_khergit_skirmisher"),
      (faction_set_slot, "fac_culture_3", slot_faction_tier_3_troop, "trp_khergit_horseman"),
      (faction_set_slot, "fac_culture_3", slot_faction_tier_4_troop, "trp_khergit_horse_archer"),
      (faction_set_slot, "fac_culture_3", slot_faction_tier_5_troop, "trp_khergit_veteran_horse_archer"),

      (faction_set_slot, "fac_culture_4", slot_faction_tier_1_troop, "trp_nord_recruit"),
      (faction_set_slot, "fac_culture_4", slot_faction_tier_2_troop, "trp_nord_footman"),
      (faction_set_slot, "fac_culture_4", slot_faction_tier_3_troop, "trp_nord_trained_footman"),
      (faction_set_slot, "fac_culture_4", slot_faction_tier_4_troop, "trp_nord_warrior"),
      (faction_set_slot, "fac_culture_4", slot_faction_tier_5_troop, "trp_nord_veteran"),

      (faction_set_slot, "fac_culture_5", slot_faction_tier_1_troop, "trp_rhodok_tribesman"),
      (faction_set_slot, "fac_culture_5", slot_faction_tier_2_troop, "trp_rhodok_spearman"),
      (faction_set_slot, "fac_culture_5", slot_faction_tier_3_troop, "trp_rhodok_trained_spearman"),
      (faction_set_slot, "fac_culture_5", slot_faction_tier_4_troop, "trp_rhodok_veteran_spearman"),
      (faction_set_slot, "fac_culture_5", slot_faction_tier_5_troop, "trp_rhodok_sergeant"),

      (faction_set_slot, "fac_culture_6", slot_faction_tier_1_troop, "trp_sarranid_recruit"),
      (faction_set_slot, "fac_culture_6", slot_faction_tier_2_troop, "trp_sarranid_footman"),
      (faction_set_slot, "fac_culture_6", slot_faction_tier_3_troop, "trp_sarranid_archer"),
      (faction_set_slot, "fac_culture_6", slot_faction_tier_4_troop, "trp_sarranid_horseman"),
      (faction_set_slot, "fac_culture_6", slot_faction_tier_5_troop, "trp_sarranid_mamluke"),

      (faction_set_slot, "fac_culture_1", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_1", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_1", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_1", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_1", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_1", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_2", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_2", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_2", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_2", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_2", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_2", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_3", slot_faction_town_walker_male_troop, "trp_khergit_townsman"),
      (faction_set_slot, "fac_culture_3", slot_faction_town_walker_female_troop, "trp_khergit_townswoman"),
      (faction_set_slot, "fac_culture_3", slot_faction_village_walker_male_troop, "trp_khergit_townsman"),
      (faction_set_slot, "fac_culture_3", slot_faction_village_walker_female_troop, "trp_khergit_townswoman"),
      (faction_set_slot, "fac_culture_3", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_3", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_4", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_4", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_4", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_4", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_4", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_4", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_5", slot_faction_town_walker_male_troop, "trp_town_walker_1"),
      (faction_set_slot, "fac_culture_5", slot_faction_town_walker_female_troop, "trp_town_walker_2"),
      (faction_set_slot, "fac_culture_5", slot_faction_village_walker_male_troop, "trp_village_walker_1"),
      (faction_set_slot, "fac_culture_5", slot_faction_village_walker_female_troop, "trp_village_walker_2"),
      (faction_set_slot, "fac_culture_5", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_5", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (faction_set_slot, "fac_culture_6", slot_faction_town_walker_male_troop, "trp_sarranid_townsman"),
      (faction_set_slot, "fac_culture_6", slot_faction_town_walker_female_troop, "trp_sarranid_townswoman"),
      (faction_set_slot, "fac_culture_6", slot_faction_village_walker_male_troop, "trp_sarranid_townsman"),
      (faction_set_slot, "fac_culture_6", slot_faction_village_walker_female_troop, "trp_sarranid_townswoman"),
      (faction_set_slot, "fac_culture_6", slot_faction_town_spy_male_troop, "trp_spy_walker_1"),
      (faction_set_slot, "fac_culture_6", slot_faction_town_spy_female_troop, "trp_spy_walker_2"),

      (try_begin),
        (eq, "$cheat_mode", 1),
        (assign, reg3, "$cheat_mode"),
        (display_message, "@{!}DEBUG : Completed faction troop assignments, cheat mode: {reg3}"),
      (try_end),

# Factions:
      (faction_set_slot, "fac_kingdom_1",  slot_faction_culture, "fac_culture_1"),
      (faction_set_slot, "fac_kingdom_1",  slot_faction_leader, "trp_kingdom_1_lord"),
      (troop_set_slot, "trp_kingdom_1_lord", slot_troop_renown, 1200),

      (faction_set_slot, "fac_kingdom_2",  slot_faction_culture, "fac_culture_2"),
      (faction_set_slot, "fac_kingdom_2",  slot_faction_leader, "trp_kingdom_2_lord"),
      (troop_set_slot, "trp_kingdom_2_lord", slot_troop_renown, 1200),

      (faction_set_slot, "fac_kingdom_3",  slot_faction_culture, "fac_culture_3"),
      (faction_set_slot, "fac_kingdom_3",  slot_faction_leader, "trp_kingdom_3_lord"),
      (troop_set_slot, "trp_kingdom_3_lord", slot_troop_renown, 1200),

      (faction_set_slot, "fac_kingdom_4",  slot_faction_culture, "fac_culture_4"),
      (faction_set_slot, "fac_kingdom_4",  slot_faction_leader, "trp_kingdom_4_lord"),
      (troop_set_slot, "trp_kingdom_4_lord", slot_troop_renown, 1200),

      (faction_set_slot, "fac_kingdom_5",  slot_faction_culture, "fac_culture_5"),
      (faction_set_slot, "fac_kingdom_5",  slot_faction_leader, "trp_kingdom_5_lord"),
      (troop_set_slot, "trp_kingdom_5_lord", slot_troop_renown, 1200),

      (faction_set_slot, "fac_kingdom_6",  slot_faction_culture, "fac_culture_6"),
      (faction_set_slot, "fac_kingdom_6",  slot_faction_leader, "trp_kingdom_6_lord"),
      (troop_set_slot, "trp_kingdom_6_lord", slot_troop_renown, 1200),

      (assign, ":player_faction_culture", "fac_culture_1"),
      (faction_set_slot, "fac_player_supporters_faction",  slot_faction_culture, ":player_faction_culture"),
      (faction_set_slot, "fac_player_faction",  slot_faction_culture, ":player_faction_culture"),

      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_set_slot, ":faction_no", slot_faction_marshall, -1),
      (try_end),
      (faction_set_slot, "fac_player_supporters_faction", slot_faction_marshall, "trp_player"),
      (call_script, "script_initialize_faction_troop_types"),
      ##diplomacy begin
      (call_script, "script_dplmc_init_domestic_policy"),
      ##diplomacy end


# Towns:
      (try_for_range, ":item_no", trade_goods_begin, trade_goods_end),
        (store_sub, ":offset", ":item_no", trade_goods_begin),
        (val_add, ":offset", slot_town_trade_good_prices_begin),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (party_set_slot, ":center_no", ":offset", average_price_factor), #1000
        (try_end),
      (try_end),

      (call_script, "script_initialize_trade_routes"),
      (call_script, "script_initialize_town_arena_info"),
      #start some tournaments
      (try_for_range, ":town_no", towns_begin, towns_end),
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", 20),
        (store_random_in_range, ":random_days", 12, 15),
        (party_set_slot, ":town_no", slot_town_has_tournament, ":random_days"),
      (try_end),

      #village products -- at some point we might make it so that the villages supply raw materials to towns, and the towns produce manufactured goods
      #village products designate the raw materials produced in the vicinity
      #right now, just doing a test for grain produced in the swadian heartland


      # fill_village_bound_centers
    #pass 1: Give one village to each castle
      (try_for_range, ":cur_center", castles_begin, castles_end),
        (assign, ":min_dist", 999999),
        (assign, ":min_dist_village", -1),
        (try_for_range, ":cur_village", villages_begin, villages_end),
          (neg|party_slot_ge, ":cur_village", slot_village_bound_center, 1), #skip villages which are already bound.
          (store_distance_to_party_from_party, ":cur_dist", ":cur_village", ":cur_center"),
          (lt, ":cur_dist", ":min_dist"),
          (assign, ":min_dist", ":cur_dist"),
          (assign, ":min_dist_village", ":cur_village"),
        (try_end),
        (party_set_slot, ":min_dist_village", slot_village_bound_center, ":cur_center"),
        (store_faction_of_party, ":town_faction", ":cur_center"),
        (call_script, "script_give_center_to_faction_aux", ":min_dist_village", ":town_faction"),
      (try_end),


    #pass 2: Give other villages to closest town.
      (try_for_range, ":cur_village", villages_begin, villages_end),
        (neg|party_slot_ge, ":cur_village", slot_village_bound_center, 1), #skip villages which are already bound.
        (assign, ":min_dist", 999999),
        (assign, ":min_dist_town", -1),
        (try_for_range, ":cur_town", towns_begin, towns_end),
          (store_distance_to_party_from_party, ":cur_dist", ":cur_village", ":cur_town"),
          (lt, ":cur_dist", ":min_dist"),
          (assign, ":min_dist", ":cur_dist"),
          (assign, ":min_dist_town", ":cur_town"),
        (try_end),
        (party_set_slot, ":cur_village", slot_village_bound_center, ":min_dist_town"),
        (store_faction_of_party, ":town_faction", ":min_dist_town"),
        (call_script, "script_give_center_to_faction_aux", ":cur_village", ":town_faction"),
      (try_end),


    # Towns (loop)
      (try_for_range, ":town_no", towns_begin, towns_end),
        (store_sub, ":offset", ":town_no", towns_begin),
        (party_set_slot,":town_no", slot_party_type, spt_town),
        # (store_add, ":cur_object_no", "trp_town_1_seneschal", ":offset"),
        # (party_set_slot,":town_no", slot_town_seneschal, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_center", ":offset"),
        (party_set_slot,":town_no", slot_town_center, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_castle", ":offset"),
        (party_set_slot,":town_no", slot_town_castle, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_prison", ":offset"),
        (party_set_slot,":town_no", slot_town_prison, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_walls", ":offset"),
        (party_set_slot,":town_no", slot_town_walls, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_tavern", ":offset"),
        (party_set_slot,":town_no", slot_town_tavern, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_store", ":offset"),
        (party_set_slot,":town_no", slot_town_store, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_arena", ":offset"),
        (party_set_slot,":town_no", slot_town_arena, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_alley", ":offset"),
        (party_set_slot,":town_no", slot_town_alley, ":cur_object_no"),
        (store_add, ":cur_object_no", "trp_town_1_mayor", ":offset"),
        (party_set_slot,":town_no", slot_town_elder, ":cur_object_no"),
        (store_add, ":cur_object_no", "trp_town_1_tavernkeeper", ":offset"),
        (party_set_slot,":town_no", slot_town_tavernkeeper, ":cur_object_no"),
        (store_add, ":cur_object_no", "trp_town_1_weaponsmith", ":offset"),
        (party_set_slot,":town_no", slot_town_weaponsmith, ":cur_object_no"),
        (store_add, ":cur_object_no", "trp_town_1_armorer", ":offset"),
        (party_set_slot,":town_no", slot_town_armorer, ":cur_object_no"),
        (store_add, ":cur_object_no", "trp_town_1_merchant", ":offset"),
        (party_set_slot,":town_no", slot_town_merchant, ":cur_object_no"),
        (store_add, ":cur_object_no", "trp_town_1_horse_merchant", ":offset"),
        (party_set_slot,":town_no", slot_town_horse_merchant, ":cur_object_no"),
        (store_add, ":cur_object_no", "scn_town_1_center", ":offset"),
        (party_set_slot,":town_no", slot_town_center, ":cur_object_no"),
        # (party_set_slot,":town_no", slot_town_reinforcement_party_template, "pt_center_reinforcements"),
      (try_end),

      #Zendar
      (party_set_slot, "p_town_23", slot_town_center, "scn_town_11_center"),
      (party_set_slot, "p_town_23", slot_town_castle, "scn_town_1_castle"),
      (party_set_slot, "p_town_23", slot_town_tavern, "scn_town_1_tavern"),
      (party_set_slot, "p_town_23", slot_town_store, "scn_town_1_store"),
      (party_set_slot, "p_town_23", slot_town_arena, "scn_town_11_arena"),
      (party_set_slot, "p_town_23", slot_town_prison, "scn_town_1_prison"),
      (party_set_slot, "p_town_23", slot_town_walls, "scn_town_11_walls"),
      (party_set_slot, "p_town_23", slot_town_alley, "scn_town_11_alley"),

      #ports
      (party_set_slot,"p_town_1", slot_town_port, "p_port_1"),
      (party_set_slot,"p_town_2", slot_town_port, "p_port_2"),
      (party_set_slot,"p_town_6", slot_town_port, "p_port_6"),
      (party_set_slot,"p_town_12", slot_town_port, "p_port_12"),
      (party_set_slot,"p_town_13", slot_town_port, "p_port_13"),
      (party_set_slot,"p_town_15", slot_town_port, "p_port_15"),
      (party_set_slot,"p_town_19", slot_town_port, "p_port_19"),

      (party_set_slot,"p_port_1", slot_port_town, "p_town_1"),
      (party_set_slot,"p_port_2", slot_port_town, "p_town_2"),
      (party_set_slot,"p_port_6", slot_port_town, "p_town_6"),
      (party_set_slot,"p_port_12", slot_port_town, "p_town_12"),
      (party_set_slot,"p_port_13", slot_port_town, "p_town_13"),
      (party_set_slot,"p_port_15", slot_port_town, "p_town_15"),
      (party_set_slot,"p_port_19", slot_port_town, "p_town_19"),

      #Zendar
      (party_set_slot, "p_town_23", slot_town_center, "scn_town_11_center"),
      (party_set_slot, "p_town_23", slot_town_castle, "scn_town_1_castle"),
      (party_set_slot, "p_town_23", slot_town_tavern, "scn_town_1_tavern"),
      (party_set_slot, "p_town_23", slot_town_store, "scn_town_1_store"),
      (party_set_slot, "p_town_23", slot_town_arena, "scn_town_11_arena"),
      (party_set_slot, "p_town_23", slot_town_prison, "scn_town_1_prison"),
      (party_set_slot, "p_town_23", slot_town_walls, "scn_town_11_walls"),
      (party_set_slot, "p_town_23", slot_town_alley, "scn_town_11_alley"),
  #Duh Town Population for Land required // Linked to bank system

	  (try_for_range, ":town_no", towns_begin, towns_end),
		(this_or_next|eq,":town_no","p_town_1"),
		(this_or_next|eq,":town_no","p_town_5"),
		(this_or_next|eq,":town_no","p_town_6"),
		(this_or_next|eq,":town_no","p_town_8"),
		(this_or_next|eq,":town_no","p_town_10"),
		(eq,"$current_town","p_town_19"),
		(store_random_in_range, ":amount", 18000, 22000),
		(party_set_slot, ":town_no", slot_center_population, ":amount"),
		(val_div, ":amount", 200),
		(party_set_slot, ":town_no", slot_town_acres, ":amount"),
	  (else_try),
		(store_random_in_range, ":amount", 8000, 12000),
		(party_set_slot, ":town_no", slot_center_population, ":amount"),
		(val_div, ":amount", 200),
		(party_set_slot, ":town_no", slot_town_acres, ":amount"),
	  (try_end),

	  #Duh Over

# Castles
      (try_for_range, ":castle_no", castles_begin, castles_end),
        (store_sub, ":offset", ":castle_no", castles_begin),
        (val_mul, ":offset", 3),

        (store_add, ":exterior_scene_no", "scn_castle_1_exterior", ":offset"),
        (party_set_slot,":castle_no", slot_castle_exterior, ":exterior_scene_no"),
        (store_add, ":interior_scene_no", "scn_castle_1_interior", ":offset"),
        (party_set_slot,":castle_no", slot_town_castle, ":interior_scene_no"),
        (store_add, ":interior_scene_no", "scn_castle_1_prison", ":offset"),
        (party_set_slot,":castle_no", slot_town_prison, ":interior_scene_no"),

        # (party_set_slot,":castle_no", slot_town_reinforcement_party_template, "pt_center_reinforcements"),
        (party_set_slot,":castle_no", slot_party_type, spt_castle),
        (party_set_slot,":castle_no", slot_center_is_besieged_by, -1),
      (try_end),

      #seneschals - dckplmc
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (store_sub, ":offset", ":center_no", walled_centers_begin),
        (store_add, ":cur_object_no", "trp_town_1_seneschal", ":offset"),
        (troop_set_slot, ":cur_object_no", slot_troop_occupation, slto_kingdom_seneschal),
        (party_set_slot,":center_no", slot_town_seneschal, ":cur_object_no"),
      (try_end),

# Set which castles need to be attacked with siege towers.
      (party_set_slot,"p_town_13", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_town_16", slot_center_siege_with_belfry, 1),

      (party_set_slot,"p_castle_1", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_2", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_4", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_7", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_8", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_9", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_11", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_13", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_21", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_25", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_34", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_35", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_38", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_40", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_41", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_42", slot_center_siege_with_belfry, 1),
      (party_set_slot,"p_castle_43", slot_center_siege_with_belfry, 1),

	  # Villages characters
      (try_for_range, ":village_no", villages_begin, villages_end),
        (store_sub, ":offset", ":village_no", villages_begin),

        (store_add, ":exterior_scene_no", "scn_village_1", ":offset"),
        (party_set_slot,":village_no", slot_castle_exterior, ":exterior_scene_no"),

        (store_add, ":store_troop_no", "trp_village_1_elder", ":offset"),
        (party_set_slot,":village_no", slot_town_elder, ":store_troop_no"),

        (party_set_slot,":village_no", slot_party_type, spt_village),
        (party_set_slot,":village_no", slot_village_raided_by, -1),

        (call_script, "script_refresh_village_defenders", ":village_no"),
        (call_script, "script_refresh_village_defenders", ":village_no"),
        (call_script, "script_refresh_village_defenders", ":village_no"),
        (call_script, "script_refresh_village_defenders", ":village_no"),
      (try_end),

      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
        (party_set_slot, ":center_no", slot_center_is_besieged_by, -1),
        (party_set_slot, ":center_no", slot_center_last_taken_by_troop, -1),
        ##diplomacy start+ Set the home slots for town merchants, elders, etc. for reverse-lookup
        (try_for_range, ":offset", dplmc_slot_town_merchants_begin, dplmc_slot_town_merchants_end),
           (party_get_slot, ":npc", ":center_no", ":offset"),
           (gt, ":npc", 0),
           (neg|troop_slot_ge, ":npc", slot_troop_home, 1),#If the startup script wasn't altered by another mod, we don't have to worry about this condition.
           (troop_set_slot, ":npc", slot_troop_home, ":center_no"),
        (try_end),
        ##diplomacy end+
      (try_end),

      #Zendar Villages
      (party_set_slot, "p_village_111", slot_castle_exterior, "scn_village_80"),
      (party_set_slot, "p_village_112", slot_castle_exterior, "scn_village_62"),

# Troops:

# Assign banners and renown.
# We assume there are enough banners for all kingdom heroes.

      #faction banners
      (faction_set_slot, "fac_kingdom_1", slot_faction_banner, "mesh_banner_kingdom_f"),
      (faction_set_slot, "fac_kingdom_2", slot_faction_banner, "mesh_banner_kingdom_b"),
      (faction_set_slot, "fac_kingdom_3", slot_faction_banner, "mesh_banner_kingdom_c"),
      (faction_set_slot, "fac_kingdom_4", slot_faction_banner, "mesh_banner_kingdom_a"),
      (faction_set_slot, "fac_kingdom_5", slot_faction_banner, "mesh_banner_kingdom_d"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_banner, "mesh_banner_kingdom_e"),

      (try_for_range, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end),
        (faction_get_slot, ":cur_faction_king", ":cur_faction", slot_faction_leader),
        (faction_get_slot, ":cur_faction_banner", ":cur_faction", slot_faction_banner),
        (val_sub, ":cur_faction_banner", banner_meshes_begin),
        (val_add, ":cur_faction_banner", banner_scene_props_begin),
        (troop_set_slot, ":cur_faction_king", slot_troop_banner_scene_prop, ":cur_faction_banner"),
      (try_end),
      (assign, ":num_khergit_lords_assigned", 0),
      (assign, ":num_sarranid_lords_assigned", 0),
      (assign, ":num_other_lords_assigned", 0),

      (try_for_range, ":kingdom_hero", active_npcs_begin, active_npcs_end),
        (this_or_next|troop_slot_eq, ":kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
        (troop_slot_eq, ":kingdom_hero", slot_troop_occupation, slto_inactive_pretender),

        (store_troop_faction, ":kingdom_hero_faction", ":kingdom_hero"),
        (neg|faction_slot_eq, ":kingdom_hero_faction", slot_faction_leader, ":kingdom_hero"),
        (try_begin),
          (eq, ":kingdom_hero_faction", "fac_kingdom_3"), #Khergit Khanate
          (store_add, ":kingdom_3_banners_begin", banner_scene_props_begin, khergit_banners_begin_offset),
          (store_add, ":banner_id", ":kingdom_3_banners_begin", ":num_khergit_lords_assigned"),
          (troop_set_slot, ":kingdom_hero", slot_troop_banner_scene_prop, ":banner_id"),
          (val_add, ":num_khergit_lords_assigned", 1),
        (else_try),
          (eq, ":kingdom_hero_faction", "fac_kingdom_6"), #Sarranid Sultanate
          (store_add, ":kingdom_6_banners_begin", banner_scene_props_begin, sarranid_banners_begin_offset),
          (store_add, ":banner_id", ":kingdom_6_banners_begin", ":num_sarranid_lords_assigned"),
          (troop_set_slot, ":kingdom_hero", slot_troop_banner_scene_prop, ":banner_id"),
          (val_add, ":num_sarranid_lords_assigned", 1),
        (else_try),
          (assign, ":hero_offset", ":num_other_lords_assigned"),
          (try_begin),
            (gt, ":hero_offset", khergit_banners_begin_offset),#Do not add khergit banners to other lords
            (val_add, ":hero_offset", khergit_banners_end_offset),
            (val_sub, ":hero_offset", khergit_banners_begin_offset),
          (try_end),
          (try_begin),
            (gt, ":hero_offset", sarranid_banners_begin_offset),#Do not add sarranid banners to other lords
            (val_add, ":hero_offset", sarranid_banners_end_offset),
            (val_sub, ":hero_offset", sarranid_banners_begin_offset),
          (try_end),
          (store_add, ":banner_id", banner_scene_props_begin, ":hero_offset"),
          (troop_set_slot, ":kingdom_hero", slot_troop_banner_scene_prop, ":banner_id"),
          (val_add, ":num_other_lords_assigned", 1),
        (try_end),
        (try_begin),
          (this_or_next|lt, ":banner_id", banner_scene_props_begin),
          (gt, ":banner_id", banner_scene_props_end_minus_one),
          (display_message, "@{!}ERROR: Not enough banners for heroes!"),
        (try_end),

        (store_character_level, ":level", ":kingdom_hero"),
        (store_mul, ":renown", ":level", ":level"),
        (val_div, ":renown", 4), #for top lord, is about 400

        (troop_get_slot, ":age", ":kingdom_hero", slot_troop_age),
        (store_mul, ":age_addition", ":age", ":age"),
        (val_div, ":age_addition", 8), #for top lord, is about 400
        (val_add, ":renown", ":age_addition"),

        (try_begin),
          (faction_slot_eq, ":kingdom_hero_faction", slot_faction_leader, ":kingdom_hero"),
          (store_random_in_range, ":random_renown", 250, 400),
        (else_try),
          (store_random_in_range, ":random_renown", 0, 100),
        (try_end),
        (val_add, ":renown", ":random_renown"),

        (troop_set_slot, ":kingdom_hero", slot_troop_renown, ":renown"),
      (try_end),

      (try_for_range, ":troop_no", "trp_player", "trp_merchants_end"),
        (add_troop_note_tableau_mesh, ":troop_no", "tableau_troop_note_mesh"),
      (try_end),

      (try_for_range, ":center_no", centers_begin, centers_end),
        (add_party_note_tableau_mesh, ":center_no", "tableau_center_note_mesh"),
      (try_end),

      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (is_between, ":faction_no", "fac_kingdom_1", kingdoms_end), #Excluding player kingdom
        (add_faction_note_tableau_mesh, ":faction_no", "tableau_faction_note_mesh"),
      (else_try),
        (add_faction_note_tableau_mesh, ":faction_no", "tableau_faction_note_mesh_banner"),
      (try_end),

	  #Give centers to factions first, to ensure more equal distributions
	  (call_script, "script_give_center_to_faction_aux", "p_town_1", "fac_kingdom_4"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_2", "fac_kingdom_4"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_3", "fac_kingdom_5"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_4", "fac_kingdom_1"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_5", "fac_kingdom_5"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_6", "fac_kingdom_1"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_7", "fac_kingdom_1"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_8", "fac_kingdom_2"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_9", "fac_kingdom_2"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_10", "fac_kingdom_3"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_11", "fac_kingdom_2"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_12", "fac_kingdom_4"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_13", "fac_kingdom_2"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_14", "fac_kingdom_3"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_15", "fac_kingdom_5"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_16", "fac_kingdom_1"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_17", "fac_kingdom_3"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_18", "fac_kingdom_3"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_19", "fac_kingdom_6"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_20", "fac_kingdom_6"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_21", "fac_kingdom_6"),
	  (call_script, "script_give_center_to_faction_aux", "p_town_22", "fac_kingdom_6"),
    (call_script, "script_give_center_to_faction_aux", "p_town_23", "fac_kingdom_4"),

      (call_script, "script_give_center_to_faction_aux", "p_castle_1", "fac_kingdom_5"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_2", "fac_kingdom_3"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_3", "fac_kingdom_2"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_4", "fac_kingdom_2"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_5", "fac_kingdom_4"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_6", "fac_kingdom_1"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_7", "fac_kingdom_3"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_8", "fac_kingdom_2"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_9", "fac_kingdom_5"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_10", "fac_kingdom_4"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_11", "fac_kingdom_4"),

      (call_script, "script_give_center_to_faction_aux", "p_castle_12", "fac_kingdom_4"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_13", "fac_kingdom_1"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_14", "fac_kingdom_5"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_15", "fac_kingdom_5"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_16", "fac_kingdom_5"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_17", "fac_kingdom_3"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_18", "fac_kingdom_2"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_19", "fac_kingdom_2"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_20", "fac_kingdom_1"),

      (call_script, "script_give_center_to_faction_aux", "p_castle_21", "fac_kingdom_5"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_22", "fac_kingdom_3"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_23", "fac_kingdom_1"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_24", "fac_kingdom_1"),

      (call_script, "script_give_center_to_faction_aux", "p_castle_25", "fac_kingdom_1"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_26", "fac_kingdom_1"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_27", "fac_kingdom_1"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_28", "fac_kingdom_5"),

      (call_script, "script_give_center_to_faction_aux", "p_castle_29", "fac_kingdom_2"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_30", "fac_kingdom_3"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_31", "fac_kingdom_1"),

      (call_script, "script_give_center_to_faction_aux", "p_castle_32", "fac_kingdom_4"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_33", "fac_kingdom_5"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_34", "fac_kingdom_4"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_35", "fac_kingdom_1"),

      (call_script, "script_give_center_to_faction_aux", "p_castle_36", "fac_kingdom_4"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_37", "fac_kingdom_2"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_38", "fac_kingdom_3"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_39", "fac_kingdom_2"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_40", "fac_kingdom_3"),

      (call_script, "script_give_center_to_faction_aux", "p_castle_41", "fac_kingdom_6"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_42", "fac_kingdom_6"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_43", "fac_kingdom_6"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_44", "fac_kingdom_6"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_45", "fac_kingdom_6"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_46", "fac_kingdom_6"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_47", "fac_kingdom_6"),
      (call_script, "script_give_center_to_faction_aux", "p_castle_48", "fac_kingdom_6"),


	  #Now give towns to great lords
	  ##diplomacy+ notes added, otherwise unchanged
      (call_script, "script_give_center_to_lord", "p_town_1",  "trp_kingdom_4_lord", 0),# Sargoth - King Ragnar
      (call_script, "script_give_center_to_lord", "p_town_2",  "trp_knight_4_1", 0),#Tihr - Jarl Aedin
      (call_script, "script_give_center_to_lord", "p_town_3",  "trp_knight_5_1", 0),#Veluca - Count Matheas
      (call_script, "script_give_center_to_lord", "p_town_4",  "trp_knight_1_1", 0),#Suno - Count Klargus
      (call_script, "script_give_center_to_lord", "p_town_5",  "trp_kingdom_5_lord", 0),# Jelkala - King Graveth
      (call_script, "script_give_center_to_lord", "p_town_6",  "trp_kingdom_1_lord", 0),# Praven - King Harlaus
      (call_script, "script_give_center_to_lord", "p_town_7",  "trp_knight_1_2", 0),#Uxkhal - Count Delinard

      (call_script, "script_give_center_to_lord", "p_town_8",  "trp_kingdom_2_lord", 0),# Reyvadin - King Yaroglek
      (call_script, "script_give_center_to_lord", "p_town_9",  "trp_knight_2_1", 0),#Khudan -Boyar Vuldrat
      (call_script, "script_give_center_to_lord", "p_town_10", "trp_kingdom_3_lord", 0),# Tulga - Sanjar Khan
      (call_script, "script_give_center_to_lord", "p_town_11", "trp_knight_2_2", 0),#Curaw - Boyar Naldera
      (call_script, "script_give_center_to_lord", "p_town_12", "trp_knight_4_2", 0),#Wercheg - Jarl Irya
      (call_script, "script_give_center_to_lord", "p_town_13", "trp_knight_2_3", 0),#Rivacheg - Boyar Meriga
      (call_script, "script_give_center_to_lord", "p_town_14", "trp_knight_3_1", 0),#Halmar -Alagur Noyan

      (call_script, "script_give_center_to_lord", "p_town_15", "trp_knight_5_2", 0),#Yalen -Count Gutlans
      (call_script, "script_give_center_to_lord", "p_town_16", "trp_knight_1_4", 0),#Dhirim - Count Clais #changed from 1_3 (Count Harringoth)
      (call_script, "script_give_center_to_lord", "p_town_17", "trp_knight_3_2", 0),#Ichamur - Tonju Noyan
      (call_script, "script_give_center_to_lord", "p_town_18", "trp_knight_3_3", 0),#Narra - Belir Noyan

      (call_script, "script_give_center_to_lord", "p_town_19", "trp_kingdom_6_lord", 0),#Shariz - Sultan Hakim
      (call_script, "script_give_center_to_lord", "p_town_20", "trp_knight_6_1", 0),#Durquba - Emir Uqais
      (call_script, "script_give_center_to_lord", "p_town_21", "trp_knight_6_2", 0),#Ahmerrad - Emir Hamezan
      (call_script, "script_give_center_to_lord", "p_town_22", "trp_knight_6_3", 0),#Bariyye - Emir Atis
	  ##diplomacy end+

      # Give family castles to certain nobles.
      (call_script, "script_give_center_to_lord", "p_castle_29", "trp_knight_2_10", 0), #Nelag_Castle
      (call_script, "script_give_center_to_lord", "p_castle_30", "trp_knight_3_4", 0), #Asugan_Castle
      (call_script, "script_give_center_to_lord", "p_castle_35", "trp_knight_1_3", 0), #Haringoth_Castle
      ##diplomacy start+
      (call_script, "script_give_center_to_lord", "p_castle_33", "trp_knight_5_11", 0), #Etrosq Castle -- why wasn't this being done already?
	  #Add home centers for claimants
	  (troop_set_slot, "trp_kingdom_1_pretender", slot_troop_home, "p_town_4"),#Lady Isolle - Suno
	  (troop_set_slot, "trp_kingdom_2_pretender", slot_troop_home, "p_town_11"),#Prince Valdym - Curaw
      (troop_set_slot, "trp_kingdom_3_pretender", slot_troop_home, "p_town_18"),#Dustum Khan - Narra
      (troop_set_slot, "trp_kingdom_4_pretender", slot_troop_home, "p_town_12"),#Lethwin Far-Seeker - Wercheg
      (troop_set_slot, "trp_kingdom_5_pretender", slot_troop_home, "p_town_3"),#Lord Kastor - Veluca
	  (troop_set_slot, "trp_kingdom_6_pretender", slot_troop_home, "p_town_20"),#Arwa the Pearled One - Durquba
 	  #add ancestral fiefs to home slots (mods not using standard NPCs should remove this)
      (troop_set_slot, "trp_knight_2_10", slot_troop_home, "p_castle_29"), #Nelag_Castle
      (troop_set_slot, "trp_knight_3_4", slot_troop_home, "p_castle_30"), #Asugan_Castle
      (troop_set_slot, "trp_knight_1_3", slot_troop_home, "p_castle_35"), #Haringoth_Castle
      (troop_set_slot, "trp_knight_5_11", slot_troop_home, "p_castle_33"), #Etrosq_Castle
	  #Also the primary six towns:
	  (troop_set_slot, "trp_kingdom_1_lord", slot_troop_home, "p_town_6"),#King Harlaus to Praven
	  (troop_set_slot, "trp_kingdom_2_lord", slot_troop_home, "p_town_8"),#King Yaroglek to Reyvadin
	  (troop_set_slot, "trp_kingdom_3_lord", slot_troop_home, "p_town_10"),#Sanjar Khan to Tulga
	  (troop_set_slot, "trp_kingdom_4_lord", slot_troop_home, "p_town_1"),#King Ragnar to Sargoth
	  (troop_set_slot, "trp_kingdom_5_lord", slot_troop_home, "p_town_5"),#King Graveth to Jelkala
	  (troop_set_slot, "trp_kingdom_6_lord", slot_troop_home, "p_town_19"),#Sultan Hakim to Shariz
      ##Also set home slots for starting quest merchants (merchant of praven, merchant of reyvadin, etc.)
      (try_for_range, ":npc", kings_begin, kings_end),
         (troop_get_slot, ":center_no", ":npc", slot_troop_home),
         (val_sub, ":npc", kings_begin),
         (val_add, ":npc", startup_merchants_begin),
         (is_between, ":npc", startup_merchants_begin, startup_merchants_end),#Right now there's a startup merchant for each faction.  Verify this hasn't unexpectedly changed.
         (neg|troop_slot_ge, ":npc", slot_troop_home, 1),#Verify that the home slot is not already set
         (troop_set_slot, ":npc", slot_troop_home, ":center_no"),
      (try_end),
      ##diplomacy end+

      (call_script, "script_assign_lords_to_empty_centers"),

	  #set original factions
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":original_faction", ":center_no"),
        (faction_get_slot, ":culture", ":original_faction", slot_faction_culture),
        (party_set_slot, ":center_no", slot_center_culture,  ":culture"),
        (party_set_slot, ":center_no", slot_center_original_faction,  ":original_faction"),
        (party_set_slot, ":center_no", slot_center_ex_faction,  ":original_faction"),
		##diplomacy start+ set additional slots
		(party_get_slot, ":town_lord", ":center_no", slot_town_lord),

		(try_begin),
			(eq, ":town_lord", "trp_player"),
			#Use trp_kingdom_heroes_including_player_begin instead of trp_player as a workaround for
			#old saved games (since uninitialized memory is 0).
			(party_set_slot, ":center_no", dplmc_slot_center_ex_lord, "trp_kingdom_heroes_including_player_begin"),
			(troop_slot_eq, "trp_player", slot_troop_home, ":center_no"),
			(neg|party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
			(party_set_slot, ":center_no", dplmc_slot_center_original_lord, "trp_kingdom_heroes_including_player_begin"),
		(else_try),
			(party_set_slot, ":center_no", dplmc_slot_center_ex_lord, ":town_lord"),
			(ge, ":town_lord", 0),
			(troop_slot_eq, ":town_lord", slot_troop_home, ":center_no"),
			(neg|party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
			(party_set_slot, ":center_no", dplmc_slot_center_original_lord, ":town_lord"),
		(try_end),
		##diplomacy end+
      (try_end),

	  #set territorial disputes/outstanding border issues
	  (party_set_slot, "p_castle_10", slot_center_ex_faction, "fac_kingdom_2"), #vaegirs claim nord-held alburq
	  (party_set_slot, "p_castle_13", slot_center_ex_faction, "fac_kingdom_4"), #nords claim swadian-held kelredan
	  (party_set_slot, "p_castle_15", slot_center_ex_faction, "fac_kingdom_1"), #swadians claim rhodok-held ergelon
	  (party_set_slot, "p_castle_46", slot_center_ex_faction, "fac_kingdom_5"), #rhodoks claim sarranid-held weyyah
	  (party_set_slot, "p_castle_40", slot_center_ex_faction, "fac_kingdom_6"), #sarranids claim khergit-held uhhun
	  (party_set_slot, "p_town_11",   slot_center_ex_faction, "fac_kingdom_3"), #Khergits claim vaegir-held curaw
    (party_set_slot, "p_town_23",   slot_center_ex_faction, "fac_kingdom_2"), #vaegirs claim nords-held zendar

	  #Swadians, being in the middle, will have additional claims on two of their neighhbors
	  (party_set_slot, "p_castle_15", slot_center_ex_faction, "fac_kingdom_1"), #swadians claim vaegir-held tilbault
	  (party_set_slot, "p_castle_22", slot_center_ex_faction, "fac_kingdom_1"), #swadians claim khergit-held unuzdaq

      (call_script, "script_update_village_market_towns"),

	  ##diplomacy start+
	  #(1) Assign plausible ancestral homes to some of the lords (not all of them) who didn't have
      #one set before.  Among other things, this is used for a sense of possessiveness.
      #(2) Assign last-transfer-times to the contested centers.
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
		 (try_begin),
			#Assign last-transfer-times to the contested centers.
			(party_get_slot, ":original_faction", ":center_no", slot_center_original_faction),
			(neg|party_slot_eq, ":center_no", slot_center_ex_faction, ":original_faction"),
			(store_random_in_range, ":transfer_time", 1, 181),#some time in the last 180 days (the length of a short game)
			(val_mul, ":transfer_time", -24),
			(party_set_slot, ":center_no", dplmc_slot_center_last_transfer_time, ":transfer_time"),
		 (else_try),
			#For non-contested centers, possibly set the lord's home slot.  Note that because
			#we're iterating in order, lords will get set to towns they own before they get
			#set to cities.
			(party_get_slot, ":town_lord", ":center_no", slot_town_lord),
			(ge, ":town_lord", 1),#only NPCs
			(neg|party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),#If there is an original owner who is dispossessed, such as a claimant
			(neg|troop_slot_ge, ":town_lord", slot_troop_home, 1),
			(troop_set_slot, ":town_lord", slot_troop_home, ":center_no"),
		 (try_end),
      (try_end),

	  # (try_for_range, ":troop_id", heroes_begin, heroes_end),
	  # (try_end),
      #
      #etc.
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
		 #If the original owner of the lord is set, don't apply this
		 (neg|party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
		 #Don't apply this to contested centers.
		 (party_get_slot, ":original_faction", ":center_no", slot_center_original_faction),
		 (party_slot_eq, ":center_no", slot_center_ex_faction, ":original_faction"),
		 #If the owner already has his "home" slot set, don't overwrite it
         (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
		 (neg|troop_slot_ge, ":town_lord", slot_troop_home, 1),
		 #No objections, so go ahead
		 (troop_set_slot, ":town_lord", slot_troop_home, ":center_no"),
      (try_end),
      ##diplomacy end+

	  #this should come after assignment of territorial grievances
      (try_for_range, ":unused", 0, 70),
        (try_begin),
          (eq, "$cheat_mode", 1),
          (display_message, "@{!}DEBUG -- initial war/peace check begins"),
        (try_end),
        (call_script, "script_randomly_start_war_peace_new", 0),
      (try_end),


      #Initialize walkers
      (try_for_range, ":center_no", centers_begin, centers_end),
        (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
                     (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (try_for_range, ":walker_no", 0, num_town_walkers),
          (call_script, "script_center_set_walker_to_type", ":center_no", ":walker_no", walkert_default),
        (try_end),
      (try_end),


	  #This needs to be after market towns
	  (call_script, "script_initialize_economic_information"),

	  (try_for_range, ":village_no", villages_begin, villages_end),
        (call_script, "script_refresh_village_merchant_inventory", ":village_no"),
      (try_end),

      (try_for_range, ":troop_id", original_kingdom_heroes_begin, active_npcs_end),
        (try_begin),
          (store_troop_faction, ":faction_id", ":troop_id"),
          (is_between, ":faction_id", kingdoms_begin, kingdoms_end),
          (troop_set_slot, ":troop_id", slot_troop_original_faction, ":faction_id"),
          (try_begin),
            (is_between, ":troop_id", pretenders_begin, pretenders_end),
            (faction_set_slot, ":faction_id", slot_faction_has_rebellion_chance, 1),
          (try_end),
        (try_end),
        (assign, ":initial_wealth", 6000),
        (try_begin),
          (store_troop_faction, ":faction", ":troop_id"),
          (faction_slot_eq, ":faction", slot_faction_leader, ":troop_id"),
          (assign, ":initial_wealth", 20000),
        (try_end),
        (troop_set_slot, ":troop_id", slot_troop_wealth, ":initial_wealth"),
      (try_end),

      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),#add town garrisons
        #Add initial center wealth
        (assign, ":initial_wealth", 2000),
        (try_begin),
          (is_between, ":center_no", towns_begin, towns_end),
          (val_mul, ":initial_wealth", 2),
        (try_end),
        (party_set_slot, ":center_no", slot_town_wealth, ":initial_wealth"),

        (assign, ":garrison_strength", 15),
        (try_begin),
          (party_slot_eq, ":center_no", slot_party_type, spt_town),
          (assign, ":garrison_strength", 40),
        (try_end),
        (try_for_range, ":unused", 0, ":garrison_strength"),
          (call_script, "script_cf_reinforce_party", ":center_no"),
        (try_end),
        ## ADD some XP initially
        (store_div, ":xp_rounds", ":garrison_strength", 5),
        (val_add, ":xp_rounds", 2),

        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),

        (try_begin), #hard
          (eq, ":reduce_campaign_ai", 0),
          (assign, ":xp_addition_for_centers", 7500),
        (else_try), #moderate
          (eq, ":reduce_campaign_ai", 1),
          (assign, ":xp_addition_for_centers", 5000),
        (else_try), #easy
          (eq, ":reduce_campaign_ai", 2),
          (assign, ":xp_addition_for_centers", 2500),
        (try_end),

        (try_for_range, ":unused", 0, ":xp_rounds"),
          (party_upgrade_with_xp, ":center_no", ":xp_addition_for_centers", 0),
        (try_end),

        #Fill town food stores upto half the limit
        (call_script, "script_center_get_food_store_limit", ":center_no"),
        (assign, ":food_store_limit", reg0),
        (val_div, ":food_store_limit", 2),
        (party_set_slot, ":center_no", slot_party_food_store, ":food_store_limit"),

        #create lord parties
        (party_get_slot, ":center_lord", ":center_no", slot_town_lord),
        (ge, ":center_lord", 1),
        (troop_slot_eq, ":center_lord", slot_troop_leaded_party, 0),
        (assign, "$g_there_is_no_avaliable_centers", 0),
        (call_script, "script_create_kingdom_hero_party", ":center_lord", ":center_no"),
        (assign, ":lords_party", "$pout_party"),
        (party_attach_to_party, ":lords_party", ":center_no"),
        (party_set_slot, ":center_no", slot_town_player_odds, 1000),
      (try_end),

	#More pre-Warband family structures removed here

	  #Warband changes begin - set companions relations
	  (try_for_range, ":companion", companions_begin, companions_end),
		(try_for_range, ":other_companion", companions_begin, companions_end),
			(neq, ":other_companion", ":companion"),
			(neg|troop_slot_eq, ":companion", slot_troop_personalityclash_object, ":other_companion"),
			(neg|troop_slot_eq, ":companion", slot_troop_personalityclash2_object, ":other_companion"),
			(call_script, "script_troop_change_relation_with_troop", ":companion", ":other_companion", 7), #companions have a starting relation of 14, unless they are rivals
		(try_end),
	  (try_end),

	  #Warband changes continue -  sets relations in the same faction
      (try_for_range, ":lord", original_kingdom_heroes_begin, active_npcs_end),
		(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
		(troop_get_slot, ":lord_faction", ":lord", slot_troop_original_faction),

		(try_for_range, ":other_hero", original_kingdom_heroes_begin, active_npcs_end),
			(this_or_next|troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_hero),
				(troop_slot_eq, ":other_hero", slot_troop_occupation, slto_inactive_pretender),
			(troop_get_slot, ":other_hero_faction", ":other_hero", slot_troop_original_faction),
			(eq, ":other_hero_faction", ":lord_faction"),
			(call_script, "script_troop_get_family_relation_to_troop", ":lord", ":other_hero"),
			(call_script, "script_troop_change_relation_with_troop", ":lord", ":other_hero", reg0),

			(store_random_in_range, ":random", 0, 11), #this will be scored twice between two kingdom heroes, so starting relation will average 10. Between lords and pretenders it will average 7.5
			(call_script, "script_troop_change_relation_with_troop", ":lord", ":other_hero", ":random"),
		(try_end),
	  (try_end),

	  ##diplomacy start+
     ##Initialize town "last caravan arrived" times randomly
	  (try_for_range, ":cur_town", towns_begin, towns_end),
	     (try_for_range, ":cur_slot", dplmc_slot_town_trade_route_last_arrivals_begin, dplmc_slot_town_trade_route_last_arrivals_end),
		    (party_slot_eq, ":cur_town", ":cur_slot", 0),
		    (store_random_in_range, ":last_arrived", 1, (24 * 7 * 5) + 1),#some time in the last five weeks
			(val_mul, ":last_arrived", -1),
			(party_get_slot, ":prosperity_factor", ":cur_town", slot_town_prosperity),#modify plus or minus 40% based on prosperity
			(val_clamp, ":prosperity_factor", 0, 101),
			(val_add, ":prosperity_factor", 75),
			(val_mul, ":last_arrived", 125),
			(val_div, ":last_arrived", ":prosperity_factor"),#last arrival some time in the last five weeks, plus or minus 40%
			(party_set_slot, ":cur_town", ":cur_slot", ":last_arrived"),
		 (try_end),
	  (try_end),
      (try_for_range, ":cur_village", villages_begin, villages_end),
          (party_get_slot, ":prosperity_factor", ":cur_town", slot_town_prosperity),#modify plus or minus 40% based on prosperity
          (val_clamp, ":prosperity_factor", 0, 101),
          (val_add, ":prosperity_factor", 75),#average 125, min 75, max 175
          (store_random_in_range, ":last_arrived", 1, (24 * 7) + 1),
          (val_mul, ":last_arrived", -1),#some time in the last 7 days, plus or minus 40%
          (val_mul, ":last_arrived", 125),
          (val_div, ":last_arrived", ":prosperity_factor"),
          (party_set_slot, ":cur_village", dplmc_slot_village_trade_last_returned_from_market, ":last_arrived"),
          (store_random_in_range, ":last_arrived", 1, (24 * 7) + 1),
          (val_mul, ":last_arrived", -1),#some time in the last 7 days
          (val_mul, ":last_arrived", 125),
          (val_div, ":last_arrived", ":prosperity_factor"),
          (party_set_slot, ":cur_village", dplmc_slot_village_trade_last_arrived_to_market, ":last_arrived"),
      (try_end),
      ##diplomacy end+

	  #do about 5 years' worth of political history (assuming 3 random checks a day)
	  (try_for_range, ":unused", 0, 5000),
		(call_script, "script_cf_random_political_event"),
	  (try_end),
	  (assign, "$total_random_quarrel_changes", 0),
	  (assign, "$total_relation_adds", 0),
	  (assign, "$total_relation_subs", 0),

	  (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
		(call_script, "script_evaluate_realm_stability", ":kingdom"),
	  (try_end),
	  #Warband changes end

	  (try_begin),
	    (eq, "$cheat_mode", 1),
	    (assign, reg3, "$cheat_mode"),
	    (display_message, "@{!}DEBUG : Completed political events, cheat mode: {reg3}"),
	  (try_end),

	  #assign love interests to unmarried male lords
	  (try_for_range, ":cur_troop", lords_begin, lords_end),
	    (troop_slot_eq, ":cur_troop", slot_troop_spouse, -1),
##diplomacy start+ Also bypass this for characters that start with manually-assigned fiancees
       (troop_slot_eq, ":cur_troop", slot_troop_betrothed, -1),
##diplomacy end+
		(neg|is_between, ":cur_troop", kings_begin, kings_end),
		(neg|is_between, ":cur_troop", pretenders_begin, pretenders_end),

		(call_script, "script_assign_troop_love_interests", ":cur_troop"),
	  (try_end),

	  (store_random_in_range, "$romantic_attraction_seed", 0, 5),

	  (try_begin),
	    (eq, "$cheat_mode", 1),
	    (assign, reg3, "$romantic_attraction_seed"),
	    (display_message, "@{!}DEBUG : Assigned love interests. Attraction seed: {reg3}"),
	  (try_end),

	  #we need to spawn more bandits in warband, because map is bigger.
      #(try_for_range, ":unused", 0, 7),
      #  (call_script, "script_spawn_bandits"),
      #(try_end),

      #(set_spawn_radius, 50),
      #(try_for_range, ":unused", 0, 25),
      #  (spawn_around_party, "p_main_party", "pt_looters"),
      #(try_end),

      (try_for_range, ":unused", 0, 10),
        (call_script, "script_spawn_bandits"),
      (try_end),

      #we are adding looter parties around each village with 1/5 probability.
      (set_spawn_radius, 5),
      (try_for_range, ":cur_village", villages_begin, villages_end),
        (store_random_in_range, ":random_value", 0, 5),
        (eq, ":random_value", 0),
        (spawn_around_party, ":cur_village", "pt_looters"),
      (try_end),

      (call_script, "script_update_mercenary_units_of_towns"),
      (call_script, "script_update_companion_candidates_in_taverns"),
      (call_script, "script_update_ransom_brokers"),
      (call_script, "script_update_tavern_travellers"),
      (call_script, "script_update_tavern_minstrels"),
      (call_script, "script_update_booksellers"),

      (try_for_range, ":village_no", villages_begin, villages_end),
        (call_script, "script_update_volunteer_troops_in_village", ":village_no"),
      (try_end),

      (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
        (call_script, "script_update_faction_notes", ":cur_kingdom"),
        (store_random_in_range, ":random_no", -60, 0),
        ##diplomacy start+
        #The above is a random time in the last 60 hours, but that's probably a mistake.
        #Change to a time within the last 60 days.
        (val_mul, ":random_no", 24),
        ##diplomacy end+
        (faction_set_slot, ":faction_no", slot_faction_last_offensive_concluded, ":random_no"),
      (try_end),

      (try_for_range, ":cur_troop", original_kingdom_heroes_begin, active_npcs_end),
        (troop_set_slot, ":cur_troop", slot_lord_granted_courtship_permission, 0), #initialize
        (call_script, "script_update_troop_notes", ":cur_troop"),
      (try_end),

      (try_for_range, ":cur_center", centers_begin, centers_end),
        ##diplomacy start+
        (party_get_slot, ":original_faction", ":center_no", slot_center_original_faction),
        (try_begin),
           #Assign plausible last-transfer-times to the contested centers based
           #on the "last offensive concluded" slot of the controlling faction.
           (is_between, ":original_faction", kingdoms_begin, kingdoms_end),
           (neg|party_slot_eq, ":center_no", slot_center_ex_faction, ":original_faction"),
           (faction_get_slot, reg0, ":original_faction", slot_faction_last_offensive_concluded),
           (party_set_slot, ":center_no", dplmc_slot_center_last_transfer_time, reg0),
        (try_end),
        ##diplomacy end+
        (call_script, "script_update_center_notes", ":cur_center"),
      (try_end),

      (call_script, "script_update_troop_notes", "trp_player"),

	  #Place kingdom ladies
      (try_for_range, ":troop_id", kingdom_ladies_begin, kingdom_ladies_end),
		(call_script, "script_get_kingdom_lady_social_determinants", ":troop_id"),
		(troop_set_slot, ":troop_id", slot_troop_cur_center, reg1),
		##diplomacy start+
		#Set their original faction.
		(ge, reg0, 0),
		(troop_get_slot, ":original_faction", reg0, slot_troop_original_faction),
		(troop_set_slot, ":troop_id", slot_troop_original_faction, ":original_faction"),
		##diplomacy end+
	  (try_end),

	  ##diplomacy start+
	  ##Set initial relations between kingdom ladies and their relatives.
	  ##Do *not* initialize their relations with anyone they aren't related to:
	  ##that is used for courtship.
	  ##  The purpose of this initialization is so if a kingdom lady gets promoted,
	  ##her relations aren't a featureless slate.  Also, it would be interesting to
	  ##further develop the idea of ladies as pursuing agendas even if they aren't
	  ##leading warbands, which would benefit from giving them relations with other
	  ##people.
     (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_lady),
		(troop_get_slot, ":lady_faction", ":lady", slot_troop_original_faction),

		(try_for_range, ":other_hero", heroes_begin, heroes_end),
		   (this_or_next|troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_lady),
			(this_or_next|troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_hero),
				(troop_slot_eq, ":other_hero", slot_troop_occupation, slto_inactive_pretender),
			(troop_slot_eq, ":other_hero", slot_troop_original_faction, ":lady_faction"),

			(neq, ":other_hero", ":lady"),
			(try_begin),
			   (this_or_next|troop_slot_eq, ":lady", slot_troop_spouse, ":other_hero"),
				   (troop_slot_eq, ":other_hero", slot_troop_spouse, ":lady"),
				(store_random_in_range, reg0, 0, 11),
			(else_try),
			   (call_script, "script_troop_get_family_relation_to_troop", ":lady", ":other_hero"),
			(try_end),
			(call_script, "script_troop_change_relation_with_troop", ":lady", ":other_hero", reg0),

			#This relation change only applies between kingdom ladies.
			(troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_lady),
			(is_between, ":other_hero", kingdom_ladies_begin, kingdom_ladies_end),

			(store_random_in_range, ":random", 0, 11),
			(call_script, "script_troop_change_relation_with_troop", ":lady", ":other_hero", ":random"),
		(try_end),
	  (try_end),
	  ##diplomacy end+


	  (try_begin),
	    (eq, "$cheat_mode", 1),
	    (assign, reg3, "$cheat_mode"),
	    (display_message, "@{!}DEBUG : Located kingdom ladies, cheat mode: {reg3}"),
	  (try_end),

      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (call_script, "script_faction_recalculate_strength", ":faction_no"),
      (try_end),

	  (faction_set_slot, "fac_kingdom_1", slot_faction_adjective, "str_kingdom_1_adjective"),
	  (faction_set_slot, "fac_kingdom_2", slot_faction_adjective, "str_kingdom_2_adjective"),
	  (faction_set_slot, "fac_kingdom_3", slot_faction_adjective, "str_kingdom_3_adjective"),
	  (faction_set_slot, "fac_kingdom_4", slot_faction_adjective, "str_kingdom_4_adjective"),
	  (faction_set_slot, "fac_kingdom_5", slot_faction_adjective, "str_kingdom_5_adjective"),
	  (faction_set_slot, "fac_kingdom_6", slot_faction_adjective, "str_kingdom_6_adjective"),

##      (assign, "$players_kingdom", "fac_kingdom_1"),
##      (call_script, "script_give_center_to_lord", "p_town_7", "trp_player", 0),
##      (call_script, "script_give_center_to_lord", "p_town_16", "trp_player", 0),
####      (call_script, "script_give_center_to_lord", "p_castle_10", "trp_player", 0),
##      (assign, "$g_castle_requested_by_player", "p_castle_10"),
      (call_script, "script_get_player_party_morale_values"),
      (party_set_morale, "p_main_party", reg0),

      (troop_set_note_available, "trp_player", 1),

      (try_for_range, ":troop_no", kings_begin, kings_end),
        (troop_set_note_available, ":troop_no", 1),
      (try_end),

      (try_for_range, ":troop_no", lords_begin, lords_end),
        (troop_set_note_available, ":troop_no", 1),
      (try_end),

	  (try_for_range, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
        (troop_set_note_available, ":troop_no", 1),
      (try_end),
	  (troop_set_note_available, "trp_knight_1_1_wife", 0),

      (try_for_range, ":troop_no", pretenders_begin, pretenders_end),
        (troop_set_note_available, ":troop_no", 1),
      (try_end),

	  #Lady and companion notes become available as you meet/recruit them

      (try_for_range, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
        (faction_set_note_available, ":faction_no", 1),
      (try_end),
      (faction_set_note_available, "fac_neutral", 0),

      (try_for_range, ":party_no", centers_begin, centers_end),
        (party_set_note_available, ":party_no", 1),
      (try_end),

	##diplomacy start+
    #Perform initialization for autoloot / autosell.
	(call_script, "script_dplmc_initialize_autoloot", 1),#argument "1" forces this to make changes
	#Set the version number (this slot on this troop should never be used for anything else)
	#The lowest 7 bits of the slot are a verification code.  They should always be equal to 68,
	#  unless there is no version number set.  The rest of the slot is the version number.
    (troop_set_slot, "trp_dplmc_chamberlain", dplmc_slot_troop_affiliated, (DPLMC_CURRENT_VERSION_CODE * 128) + DPLMC_VERSION_LOW_7_BITS),#Version number 1
	##diplomacy end+

    #Autotrade begin
    (call_script, "script_initialize_auto_trade"),
    #Autotrade end

    #SB : default parameters for post-battle continuation
    (call_script, "script_setup_camera_keys"),
    (assign, "$g_dplmc_cam_default", camera_mouse),
    (assign, "$g_dplmc_player_disguise", disguise_pilgrim),
    (assign, "$g_dplmc_charge_when_dead", 1),

    #SB : training ground slots
    (try_for_range, ":npc", training_ground_trainers_begin, training_ground_trainers_end),
        #init trainer vars
        (troop_set_slot, ":npc", slot_troop_trainer_met, 0),
        (troop_set_slot, ":npc", slot_troop_trainer_waiting_for_result, 0),
        (troop_set_slot, ":npc", slot_troop_trainer_training_fight_won, 0),
        (troop_set_slot, ":npc", slot_troop_trainer_num_opponents_to_beat, 3),
        (troop_set_slot, ":npc", slot_troop_trainer_training_system_explained, 0),
        (troop_set_slot, ":npc", slot_troop_trainer_opponent_troop, fighters_begin),
        (troop_set_slot, ":npc", slot_troop_trainer_training_difficulty, 0),

        (store_sub, ":offset", ":npc", training_ground_trainers_begin),
        #init grounds vars
        (store_add, ":grounds", ":offset", training_grounds_begin),
        (store_add, ":scene", ":offset", "scn_training_ground_ranged_melee_1"),
        (party_set_slot, ":grounds", slot_grounds_melee, ":scene"),
        (store_add, ":scene", ":offset", "scn_training_ground_horse_track_1"),
        (party_set_slot, ":grounds", slot_grounds_track, ":scene"),
        (party_set_slot, ":grounds", slot_grounds_trainer, ":npc"),
        (party_set_slot, ":grounds", slot_grounds_count, 0),
        (troop_set_slot, ":npc", slot_troop_cur_center, ":grounds"),
    (try_end),
    ]),

  #script_game_get_use_string
  # This script is called from the game engine for getting using information text
  # INPUT: used_scene_prop_id
  # OUTPUT: s0
  ("game_get_use_string",
   [
     (store_script_param, ":instance_id", 1),

     (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),

     (try_begin),
       (this_or_next|eq, ":scene_prop_id", "spr_winch_b"),
       (eq, ":scene_prop_id", "spr_winch"),
       (assign, ":effected_object", "spr_portcullis"),
     (else_try),
       (this_or_next|eq, ":scene_prop_id", "spr_door_destructible"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_b"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_6m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_8m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_10m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_12m"),
       (eq, ":scene_prop_id", "spr_siege_ladder_move_14m"),
       (assign, ":effected_object", ":scene_prop_id"),
     (try_end),

     (scene_prop_get_slot, ":item_situation", ":instance_id", scene_prop_open_or_close_slot),

     (try_begin), #opening/closing portcullis
       (eq, ":effected_object", "spr_portcullis"),

       (try_begin),
         (eq, ":item_situation", 0),
         (str_store_string, s0, "str_open_gate"),
       (else_try),
         (str_store_string, s0, "str_close_gate"),
       (try_end),
     (else_try), #opening/closing door
       (this_or_next|eq, ":effected_object", "spr_door_destructible"),
       (this_or_next|eq, ":effected_object", "spr_castle_f_door_b"),
       (this_or_next|eq, ":effected_object", "spr_castle_e_sally_door_a"),
       (this_or_next|eq, ":effected_object", "spr_castle_f_sally_door_a"),
       (this_or_next|eq, ":effected_object", "spr_earth_sally_gate_left"),
       (this_or_next|eq, ":effected_object", "spr_earth_sally_gate_right"),
       (this_or_next|eq, ":effected_object", "spr_viking_keep_destroy_sally_door_left"),
       (this_or_next|eq, ":effected_object", "spr_viking_keep_destroy_sally_door_right"),
       (eq, ":effected_object", "spr_castle_f_door_a"),

       (try_begin),
         (eq, ":item_situation", 0),
         (str_store_string, s0, "str_open_door"),
       (else_try),
         (str_store_string, s0, "str_close_door"),
       (try_end),
     (else_try), #raising/dropping ladder
       (try_begin),
         (eq, ":item_situation", 0),
         (str_store_string, s0, "str_raise_ladder"),
       (else_try),
         (str_store_string, s0, "str_drop_ladder"),
       (try_end),
     (try_end),
   ]),

  #script_game_quick_start
  # This script is called from the game engine for initializing the global variables for tutorial, multiplayer and custom battle modes.
  # INPUT:
  # none
  # OUTPUT:
  # none
  ("game_quick_start",
    [
      #for quick battle mode
      (assign, "$g_is_quick_battle", 0),
      (assign, "$g_quick_battle_game_type", 0),
      (assign, "$g_quick_battle_troop", quick_battle_troops_begin),
      (assign, "$g_quick_battle_map", quick_battle_scenes_begin),
      (assign, "$g_quick_battle_team_1_faction", "fac_kingdom_1"),
      (assign, "$g_quick_battle_team_2_faction", "fac_kingdom_2"),
      (assign, "$g_quick_battle_army_1_size", 25),
      (assign, "$g_quick_battle_army_2_size", 25),

      (faction_set_slot, "fac_outlaws", slot_faction_quick_battle_tier_1_infantry, "trp_mountain_bandit"),
      (faction_set_slot, "fac_outlaws", slot_faction_quick_battle_tier_2_infantry, "trp_sea_raider"),
      (faction_set_slot, "fac_outlaws", slot_faction_quick_battle_tier_1_archer, "trp_forest_bandit"),
      (faction_set_slot, "fac_outlaws", slot_faction_quick_battle_tier_2_archer, "trp_taiga_bandit"),
      (faction_set_slot, "fac_outlaws", slot_faction_quick_battle_tier_1_cavalry, "trp_steppe_bandit"),
      (faction_set_slot, "fac_outlaws", slot_faction_quick_battle_tier_2_cavalry, "trp_desert_bandit"),
      (faction_set_slot, "fac_kingdom_1", slot_faction_quick_battle_tier_1_infantry, "trp_swadian_footman"),
      (faction_set_slot, "fac_kingdom_1", slot_faction_quick_battle_tier_2_infantry, "trp_swadian_infantry"),
      (faction_set_slot, "fac_kingdom_1", slot_faction_quick_battle_tier_1_archer, "trp_swadian_skirmisher"),
      (faction_set_slot, "fac_kingdom_1", slot_faction_quick_battle_tier_2_archer, "trp_swadian_crossbowman"),
      (faction_set_slot, "fac_kingdom_1", slot_faction_quick_battle_tier_1_cavalry, "trp_swadian_man_at_arms"),
      (faction_set_slot, "fac_kingdom_1", slot_faction_quick_battle_tier_2_cavalry, "trp_swadian_knight"),
      (faction_set_slot, "fac_kingdom_2", slot_faction_quick_battle_tier_1_infantry, "trp_vaegir_footman"),
      (faction_set_slot, "fac_kingdom_2", slot_faction_quick_battle_tier_2_infantry, "trp_vaegir_infantry"),
      (faction_set_slot, "fac_kingdom_2", slot_faction_quick_battle_tier_1_archer, "trp_vaegir_skirmisher"),
      (faction_set_slot, "fac_kingdom_2", slot_faction_quick_battle_tier_2_archer, "trp_vaegir_archer"),
      (faction_set_slot, "fac_kingdom_2", slot_faction_quick_battle_tier_1_cavalry, "trp_vaegir_horseman"),
      (faction_set_slot, "fac_kingdom_2", slot_faction_quick_battle_tier_2_cavalry, "trp_vaegir_knight"),
      (faction_set_slot, "fac_kingdom_3", slot_faction_quick_battle_tier_1_infantry, "trp_khergit_dismounted_lancer_multiplayer_ai"),
      (faction_set_slot, "fac_kingdom_3", slot_faction_quick_battle_tier_2_infantry, "trp_khergit_dismounted_lancer_multiplayer_ai"),
      (faction_set_slot, "fac_kingdom_3", slot_faction_quick_battle_tier_1_archer, "trp_khergit_horse_archer"),
      (faction_set_slot, "fac_kingdom_3", slot_faction_quick_battle_tier_2_archer, "trp_khergit_veteran_horse_archer"),
      (faction_set_slot, "fac_kingdom_3", slot_faction_quick_battle_tier_1_cavalry, "trp_khergit_lancer"),
      (faction_set_slot, "fac_kingdom_3", slot_faction_quick_battle_tier_2_cavalry, "trp_khergit_lancer"),
      (faction_set_slot, "fac_kingdom_4", slot_faction_quick_battle_tier_1_infantry, "trp_nord_warrior"),
      (faction_set_slot, "fac_kingdom_4", slot_faction_quick_battle_tier_2_infantry, "trp_nord_champion"),
      (faction_set_slot, "fac_kingdom_4", slot_faction_quick_battle_tier_1_archer, "trp_nord_archer"),
      (faction_set_slot, "fac_kingdom_4", slot_faction_quick_battle_tier_2_archer, "trp_nord_veteran_archer"),
      (faction_set_slot, "fac_kingdom_4", slot_faction_quick_battle_tier_1_cavalry, "trp_nord_scout_multiplayer_ai"),
      (faction_set_slot, "fac_kingdom_4", slot_faction_quick_battle_tier_2_cavalry, "trp_nord_scout_multiplayer_ai"),
      (faction_set_slot, "fac_kingdom_5", slot_faction_quick_battle_tier_1_infantry, "trp_rhodok_veteran_spearman"),
      (faction_set_slot, "fac_kingdom_5", slot_faction_quick_battle_tier_2_infantry, "trp_rhodok_sergeant"),
      (faction_set_slot, "fac_kingdom_5", slot_faction_quick_battle_tier_1_archer, "trp_rhodok_crossbowman"),
      (faction_set_slot, "fac_kingdom_5", slot_faction_quick_battle_tier_2_archer, "trp_rhodok_veteran_crossbowman"),
      (faction_set_slot, "fac_kingdom_5", slot_faction_quick_battle_tier_1_cavalry, "trp_rhodok_scout_multiplayer_ai"),
      (faction_set_slot, "fac_kingdom_5", slot_faction_quick_battle_tier_2_cavalry, "trp_rhodok_scout_multiplayer_ai"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_quick_battle_tier_1_infantry, "trp_sarranid_veteran_footman"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_quick_battle_tier_2_infantry, "trp_sarranid_infantry"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_quick_battle_tier_1_archer, "trp_sarranid_skirmisher"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_quick_battle_tier_2_archer, "trp_sarranid_archer"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_quick_battle_tier_1_cavalry, "trp_sarranid_horseman"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_quick_battle_tier_2_cavalry, "trp_sarranid_mamluke"),

      #for multiplayer mode
      (assign, "$g_multiplayer_selected_map", multiplayer_scenes_begin),
      (assign, "$g_multiplayer_respawn_period", 5),
      (assign, "$g_multiplayer_round_max_seconds", 300),
      (assign, "$g_multiplayer_game_max_minutes", 30),
      (assign, "$g_multiplayer_game_max_points", 300),

      (server_get_renaming_server_allowed, "$g_multiplayer_renaming_server_allowed"),
      (server_get_changing_game_type_allowed, "$g_multiplayer_changing_game_type_allowed"),
      (assign, "$g_multiplayer_point_gained_from_flags", 100),
      (assign, "$g_multiplayer_point_gained_from_capturing_flag", 5),
      (assign, "$g_multiplayer_game_type", 0),
      (assign, "$g_multiplayer_team_1_faction", "fac_kingdom_1"),
      (assign, "$g_multiplayer_team_2_faction", "fac_kingdom_2"),
      (assign, "$g_multiplayer_next_team_1_faction", "$g_multiplayer_team_1_faction"),
      (assign, "$g_multiplayer_next_team_2_faction", "$g_multiplayer_team_2_faction"),
      (assign, "$g_multiplayer_num_bots_team_1", 0),
      (assign, "$g_multiplayer_num_bots_team_2", 0),
      (assign, "$g_multiplayer_number_of_respawn_count", 0),
      (assign, "$g_multiplayer_num_bots_voteable", 50),
      (assign, "$g_multiplayer_max_num_bots", 101),
      (assign, "$g_multiplayer_factions_voteable", 1),
      (assign, "$g_multiplayer_maps_voteable", 1),
      (assign, "$g_multiplayer_kick_voteable", 1),
      (assign, "$g_multiplayer_ban_voteable", 1),
      (assign, "$g_multiplayer_valid_vote_ratio", 51), #more than 50 percent
      (assign, "$g_multiplayer_auto_team_balance_limit", 3), #auto balance when difference is more than 2
      (assign, "$g_multiplayer_player_respawn_as_bot", 1),
      (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
      (assign, "$g_multiplayer_mission_end_screen", 0),
      (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
      (assign, "$g_multiplayer_welcome_message_shown", 0),
      (assign, "$g_multiplayer_allow_player_banners", 1),
      (assign, "$g_multiplayer_force_default_armor", 1),
      (assign, "$g_multiplayer_disallow_ranged_weapons", 0),

      (assign, "$g_multiplayer_initial_gold_multiplier", 100),
      (assign, "$g_multiplayer_battle_earnings_multiplier", 100),
      (assign, "$g_multiplayer_round_earnings_multiplier", 100),

      #faction banners
      (faction_set_slot, "fac_kingdom_1", slot_faction_banner, "mesh_banner_kingdom_f"),
      (faction_set_slot, "fac_kingdom_2", slot_faction_banner, "mesh_banner_kingdom_b"),
      (faction_set_slot, "fac_kingdom_3", slot_faction_banner, "mesh_banner_kingdom_c"),
      (faction_set_slot, "fac_kingdom_4", slot_faction_banner, "mesh_banner_kingdom_a"),
      (faction_set_slot, "fac_kingdom_5", slot_faction_banner, "mesh_banner_kingdom_d"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_banner, "mesh_banner_kingdom_e"),

      (call_script, "script_initialize_banner_info"),

      (try_for_range, ":cur_item", all_items_begin, all_items_end),
        (try_for_range, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end),
          (store_sub, ":faction_index", ":cur_faction", npc_kingdoms_begin),
          (val_add, ":faction_index", slot_item_multiplayer_faction_price_multipliers_begin),
          (item_set_slot, ":cur_item", ":faction_index", 100), #100 is the default price multiplier
        (try_end),
      (try_end),
      (store_sub, ":swadian_price_slot", "fac_kingdom_1", npc_kingdoms_begin),
      (val_add, ":swadian_price_slot", slot_item_multiplayer_faction_price_multipliers_begin),
      (store_sub, ":vaegir_price_slot", "fac_kingdom_2", npc_kingdoms_begin),
      (val_add, ":vaegir_price_slot", slot_item_multiplayer_faction_price_multipliers_begin),
      (store_sub, ":khergit_price_slot", "fac_kingdom_3", npc_kingdoms_begin),
      (val_add, ":khergit_price_slot", slot_item_multiplayer_faction_price_multipliers_begin),
      (store_sub, ":nord_price_slot", "fac_kingdom_4", npc_kingdoms_begin),
      (val_add, ":nord_price_slot", slot_item_multiplayer_faction_price_multipliers_begin),
      (store_sub, ":rhodok_price_slot", "fac_kingdom_5", npc_kingdoms_begin),
      (val_add, ":rhodok_price_slot", slot_item_multiplayer_faction_price_multipliers_begin),
      (store_sub, ":sarranid_price_slot", "fac_kingdom_6", npc_kingdoms_begin),
      (val_add, ":sarranid_price_slot", slot_item_multiplayer_faction_price_multipliers_begin),

      (item_set_slot, "itm_awlpike", ":swadian_price_slot", 80),
      (item_set_slot, "itm_awlpike_long", ":swadian_price_slot", 90),
      (item_set_slot, "itm_sword_medieval_a", ":swadian_price_slot", 80),
      (item_set_slot, "itm_sword_medieval_b", ":swadian_price_slot", 80),
      (item_set_slot, "itm_sword_medieval_b_small", ":swadian_price_slot", 80),
      (item_set_slot, "itm_sword_medieval_c", ":swadian_price_slot", 80),
      (item_set_slot, "itm_sword_medieval_c_small", ":swadian_price_slot", 80),
      (item_set_slot, "itm_leather_boots", ":swadian_price_slot", 90),
      (item_set_slot, "itm_mail_chausses", ":swadian_price_slot", 80),
      (item_set_slot, "itm_splinted_greaves", ":swadian_price_slot", 80),
      (item_set_slot, "itm_plate_boots", ":swadian_price_slot", 80),
      (item_set_slot, "itm_courser", ":swadian_price_slot", 90),
      (item_set_slot, "itm_hunter", ":swadian_price_slot", 75),
      (item_set_slot, "itm_norman_helmet", ":swadian_price_slot", 75),
      (item_set_slot, "itm_helmet_with_neckguard", ":swadian_price_slot", 75),
      (item_set_slot, "itm_red_gambeson", ":swadian_price_slot", 75),
      (item_set_slot, "itm_darts", ":swadian_price_slot", 50),
      (item_set_slot, "itm_war_darts", ":swadian_price_slot", 50),
      (item_set_slot, "itm_tab_shield_heater_d", ":swadian_price_slot", 80),
      (item_set_slot, "itm_brigandine_red", ":swadian_price_slot", 75),
      (item_set_slot, "itm_bastard_sword_b", ":swadian_price_slot", 65),
      (item_set_slot, "itm_bastard_sword_a", ":swadian_price_slot", 85),

      (item_set_slot, "itm_steppe_horse", ":khergit_price_slot", 120),
      (item_set_slot, "itm_courser", ":khergit_price_slot", 80),
      (item_set_slot, "itm_hunter", ":khergit_price_slot", 80),
      (item_set_slot, "itm_warhorse_steppe", ":khergit_price_slot", 120),
      (item_set_slot, "itm_one_handed_war_axe_a", ":khergit_price_slot", 300),
      (item_set_slot, "itm_tribal_warrior_outfit", ":khergit_price_slot", 140),

      (item_set_slot, "itm_leather_gloves", ":sarranid_price_slot", 50),
      (item_set_slot, "itm_short_bow", ":sarranid_price_slot", 50),
      (item_set_slot, "itm_barbed_arrows", ":sarranid_price_slot", 80),
      (item_set_slot, "itm_jarid", ":sarranid_price_slot", 85),
      (item_set_slot, "itm_javelin", ":sarranid_price_slot", 85),

      (item_set_slot, "itm_lamellar_vest", ":vaegir_price_slot", 130),
      (item_set_slot, "itm_awlpike", ":vaegir_price_slot", 150),
      (item_set_slot, "itm_scimitar", ":vaegir_price_slot", 130),
      (item_set_slot, "itm_scimitar_b", ":vaegir_price_slot", 150),
      (item_set_slot, "itm_tab_shield_kite_a", ":vaegir_price_slot", 120),
      (item_set_slot, "itm_tab_shield_kite_b", ":vaegir_price_slot", 120),
      (item_set_slot, "itm_tab_shield_kite_c", ":vaegir_price_slot", 120),
      (item_set_slot, "itm_tab_shield_kite_d", ":vaegir_price_slot", 120),
      (item_set_slot, "itm_javelin", ":vaegir_price_slot", 120),

      #arrows
      (item_set_slot, "itm_arrows", slot_item_multiplayer_item_class, multi_item_class_type_arrow),
      (item_set_slot, "itm_barbed_arrows", slot_item_multiplayer_item_class, multi_item_class_type_arrow),
      (item_set_slot, "itm_bodkin_arrows", slot_item_multiplayer_item_class, multi_item_class_type_arrow),
      (item_set_slot, "itm_khergit_arrows", slot_item_multiplayer_item_class, multi_item_class_type_arrow),
      #bolts
      (item_set_slot, "itm_bolts", slot_item_multiplayer_item_class, multi_item_class_type_bolt),
      (item_set_slot, "itm_steel_bolts", slot_item_multiplayer_item_class, multi_item_class_type_bolt),
      #bows
      (item_set_slot, "itm_crossbow", slot_item_multiplayer_item_class, multi_item_class_type_bow),
      (item_set_slot, "itm_heavy_crossbow", slot_item_multiplayer_item_class, multi_item_class_type_bow),
      (item_set_slot, "itm_sniper_crossbow", slot_item_multiplayer_item_class, multi_item_class_type_bow),
      (item_set_slot, "itm_nomad_bow", slot_item_multiplayer_item_class, multi_item_class_type_bow),
      (item_set_slot, "itm_khergit_bow", slot_item_multiplayer_item_class, multi_item_class_type_bow),
      (item_set_slot, "itm_strong_bow", slot_item_multiplayer_item_class, multi_item_class_type_bow),
      (item_set_slot, "itm_war_bow", slot_item_multiplayer_item_class, multi_item_class_type_bow),
      (item_set_slot, "itm_short_bow", slot_item_multiplayer_item_class, multi_item_class_type_bow),
      (item_set_slot, "itm_long_bow", slot_item_multiplayer_item_class, multi_item_class_type_bow),
      (item_set_slot, "itm_light_crossbow", slot_item_multiplayer_item_class, multi_item_class_type_bow),
      #swords
      (item_set_slot, "itm_sword_medieval_a", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_sword_medieval_b", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_sword_medieval_b_small", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_sword_medieval_c", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_sword_medieval_c_small", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_scimitar", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_scimitar_b", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_dagger", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_sword_khergit_1", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_sword_khergit_2", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_sword_khergit_3", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_sword_khergit_4", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_sword_viking_1", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_sword_viking_2", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_sword_viking_2_small", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_sword_viking_3", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_sword_viking_3_small", slot_item_multiplayer_item_class, multi_item_class_type_sword),
      (item_set_slot, "itm_bastard_sword_a", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_sword),
      (item_set_slot, "itm_bastard_sword_b", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_sword),
      (item_set_slot, "itm_sword_two_handed_a", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_sword),
      (item_set_slot, "itm_sword_two_handed_b", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_sword),
      (item_set_slot, "itm_arabian_sword_a", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_sword),
      (item_set_slot, "itm_arabian_sword_b", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_sword),
      (item_set_slot, "itm_sarranid_cavalry_sword", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_sword),
      (item_set_slot, "itm_arabian_sword_d", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_sword),

      #axe
      (item_set_slot, "itm_axe", slot_item_multiplayer_item_class, multi_item_class_type_axe),
      (item_set_slot, "itm_battle_axe", slot_item_multiplayer_item_class, multi_item_class_type_axe),
      (item_set_slot, "itm_one_handed_war_axe_a", slot_item_multiplayer_item_class, multi_item_class_type_axe),
      (item_set_slot, "itm_one_handed_war_axe_b", slot_item_multiplayer_item_class, multi_item_class_type_axe),
      (item_set_slot, "itm_one_handed_battle_axe_a", slot_item_multiplayer_item_class, multi_item_class_type_axe),
      (item_set_slot, "itm_one_handed_battle_axe_b", slot_item_multiplayer_item_class, multi_item_class_type_axe),
      (item_set_slot, "itm_one_handed_battle_axe_c", slot_item_multiplayer_item_class, multi_item_class_type_axe),

      (item_set_slot, "itm_two_handed_axe", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_axe),
      (item_set_slot, "itm_two_handed_battle_axe_2", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_axe),
      (item_set_slot, "itm_shortened_voulge", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_axe),
      (item_set_slot, "itm_bardiche", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_axe),
      (item_set_slot, "itm_great_axe", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_axe),
      (item_set_slot, "itm_great_bardiche", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_axe),
      (item_set_slot, "itm_long_axe", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_axe),
      (item_set_slot, "itm_long_axe_b", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_axe),
      (item_set_slot, "itm_long_axe_c", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_axe),
      (item_set_slot, "itm_voulge", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_axe),
      (item_set_slot, "itm_long_bardiche", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_axe),
      (item_set_slot, "itm_great_long_bardiche", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_axe),

      #blunt
      (item_set_slot, "itm_mace_1", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_mace_2", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_mace_3", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_mace_4", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_long_spiked_club", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_long_hafted_spiked_mace", slot_item_multiplayer_item_class, multi_item_class_type_blunt),

      (item_set_slot, "itm_maul", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_sledgehammer", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_warhammer", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_morningstar", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      #picks
      (item_set_slot, "itm_military_sickle_a", slot_item_multiplayer_item_class, multi_item_class_type_war_picks),
      (item_set_slot, "itm_fighting_pick", slot_item_multiplayer_item_class, multi_item_class_type_war_picks),
      (item_set_slot, "itm_military_pick", slot_item_multiplayer_item_class, multi_item_class_type_war_picks),
      (item_set_slot, "itm_club_with_spike_head", slot_item_multiplayer_item_class, multi_item_class_type_war_picks),

	  #Cleavers
	  (item_set_slot, "itm_falchion", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_military_cleaver_b", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_military_cleaver_c", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_two_handed_cleaver", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_hafted_blade_a", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_hafted_blade_b", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),
      (item_set_slot, "itm_shortened_military_scythe", slot_item_multiplayer_item_class, multi_item_class_type_cleavers),

      (item_set_slot, "itm_sarranid_mace_1", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_sarranid_axe_a", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_sarranid_axe_b", slot_item_multiplayer_item_class, multi_item_class_type_blunt),
      (item_set_slot, "itm_sarranid_two_handed_axe_a", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_axe),
      (item_set_slot, "itm_sarranid_two_handed_axe_b", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_axe),
      (item_set_slot, "itm_sarranid_two_handed_mace_1", slot_item_multiplayer_item_class, multi_item_class_type_two_handed_axe),
      (item_set_slot, "itm_bamboo_spear", slot_item_multiplayer_item_class, multi_item_class_type_spear),



      #spears
      (item_set_slot, "itm_double_sided_lance", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_glaive", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_poleaxe", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_polehammer", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_staff", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_quarter_staff", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_iron_staff", slot_item_multiplayer_item_class, multi_item_class_type_spear),

      (item_set_slot, "itm_shortened_spear", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_spear", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_war_spear", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_military_scythe", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_pike", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_ashwood_pike", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_awlpike", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      (item_set_slot, "itm_awlpike_long", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      #lance
      (item_set_slot, "itm_light_lance", slot_item_multiplayer_item_class, multi_item_class_type_lance),
      (item_set_slot, "itm_lance", slot_item_multiplayer_item_class, multi_item_class_type_lance),
      (item_set_slot, "itm_heavy_lance", slot_item_multiplayer_item_class, multi_item_class_type_lance),
      (item_set_slot, "itm_great_lance", slot_item_multiplayer_item_class, multi_item_class_type_lance),
      #shields

      (item_set_slot, "itm_tab_shield_round_a", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_round_b", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_round_c", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_round_d", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_round_e", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_kite_a", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_kite_b", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_kite_c", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_kite_d", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_kite_cav_a", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_kite_cav_b", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_heater_a", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_heater_b", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_heater_c", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_heater_d", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_heater_cav_a", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_heater_cav_b", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_pavise_a", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_pavise_b", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_pavise_c", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_pavise_d", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_small_round_a", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_small_round_b", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_tab_shield_small_round_c", slot_item_multiplayer_item_class, multi_item_class_type_small_shield),
      (item_set_slot, "itm_spear", slot_item_multiplayer_item_class, multi_item_class_type_spear),
      #throwing
      (item_set_slot, "itm_darts", slot_item_multiplayer_item_class, multi_item_class_type_throwing),
      (item_set_slot, "itm_war_darts", slot_item_multiplayer_item_class, multi_item_class_type_throwing),
      (item_set_slot, "itm_javelin", slot_item_multiplayer_item_class, multi_item_class_type_throwing),
      (item_set_slot, "itm_jarid", slot_item_multiplayer_item_class, multi_item_class_type_throwing),
      (item_set_slot, "itm_throwing_spears", slot_item_multiplayer_item_class, multi_item_class_type_throwing),

      (item_set_slot, "itm_throwing_axes", slot_item_multiplayer_item_class, multi_item_class_type_throwing_axe),
      (item_set_slot, "itm_light_throwing_axes", slot_item_multiplayer_item_class, multi_item_class_type_throwing_axe),
      (item_set_slot, "itm_heavy_throwing_axes", slot_item_multiplayer_item_class, multi_item_class_type_throwing_axe),
       #armors
      (item_set_slot, "itm_red_shirt", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_red_tunic", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_aketon_green", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_padded_cloth", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_red_gambeson", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_leather_armor", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_haubergeon", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_coat_of_plates_red", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_brigandine_red", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_mail_with_surcoat", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_linen_tunic", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_leather_vest", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_leather_jerkin", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_studded_leather_coat", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_lamellar_vest", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_lamellar_armor", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_coarse_tunic", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_tribal_warrior_outfit", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_khergit_guard_armor", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_blue_tunic", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_mail_hauberk", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_mail_shirt", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_byrnie", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
	  (item_set_slot, "itm_lamellar_vest_khergit", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
	  (item_set_slot, "itm_steppe_armor", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),


      (item_set_slot, "itm_banded_armor", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_cuir_bouilli", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_scale_armor", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),

      (item_set_slot, "itm_padded_leather", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_green_tunic", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_tunic_with_green_cape", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_aketon_green", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_ragged_outfit", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_surcoat_over_mail", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),

      (item_set_slot, "itm_sarranid_elite_armor", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_skirmisher_armor", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_archers_vest", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_sarranid_leather_armor", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_sarranid_cloth_robe", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_sarranid_mail_shirt", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_sarranid_cavalry_robe", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_arabian_armor_b", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_mamluke_mail", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_khergit_elite_armor", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
      (item_set_slot, "itm_vaegir_elite_armor", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
	  (item_set_slot, "itm_khergit_armor", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),





      #boots
      (item_set_slot, "itm_hide_boots", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_ankle_boots", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_nomad_boots", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_leather_boots", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_splinted_leather_greaves", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_mail_chausses", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_splinted_leather_greaves", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_splinted_greaves", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_mail_boots", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_iron_greaves", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_sarranid_boots_b", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_sarranid_boots_c", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
      (item_set_slot, "itm_sarranid_boots_d", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
	  (item_set_slot, "itm_plate_boots", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
	  (item_set_slot, "itm_khergit_leather_boots", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),
	  (item_set_slot, "itm_khergit_guard_boots", slot_item_multiplayer_item_class, multi_item_class_type_light_foot),








      #helmets


      (item_set_slot, "itm_leather_steppe_cap_a", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_leather_steppe_cap_b", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_steppe_cap", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_khergit_war_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_khergit_guard_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),



      (item_set_slot, "itm_arming_cap", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_padded_coif", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_mail_coif", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_footman_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_norman_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_kettle_hat", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_helmet_with_neckguard", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),

	  (item_set_slot, "itm_bascinet_2", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
	  (item_set_slot, "itm_bascinet_3", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),



      (item_set_slot, "itm_flat_topped_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_guard_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_full_helm", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_great_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_nomad_cap_b", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_skullcap", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_leather_cap", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),

      (item_set_slot, "itm_spiked_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
#      (item_set_slot, "itm_nasal_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_nordic_archer_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_nordic_veteran_archer_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_nordic_footman_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_nordic_fighter_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_nordic_huscarl_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_nordic_warlord_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),

      (item_set_slot, "itm_sarranid_helmet1", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_sarranid_horseman_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_sarranid_felt_hat", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_sarranid_veiled_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_turban", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_desert_turban", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_sarranid_warrior_cap", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_sarranid_mail_coif", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),

      (item_set_slot, "itm_vaegir_fur_cap", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_vaegir_fur_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_vaegir_spiked_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_vaegir_lamellar_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_vaegir_noble_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_vaegir_war_helmet", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),
      (item_set_slot, "itm_vaegir_mask", slot_item_multiplayer_item_class, multi_item_class_type_light_helm),


	  #gloves
      (item_set_slot, "itm_leather_gloves", slot_item_multiplayer_item_class, multi_item_class_type_glove),
      (item_set_slot, "itm_mail_mittens", slot_item_multiplayer_item_class, multi_item_class_type_glove),
      (item_set_slot, "itm_scale_gauntlets", slot_item_multiplayer_item_class, multi_item_class_type_glove),
	  (item_set_slot, "itm_lamellar_gauntlets", slot_item_multiplayer_item_class, multi_item_class_type_glove),
	  (item_set_slot, "itm_gauntlets", slot_item_multiplayer_item_class, multi_item_class_type_glove),

      #horses
      (item_set_slot, "itm_saddle_horse", slot_item_multiplayer_item_class, multi_item_class_type_horse),
      (item_set_slot, "itm_hunter", slot_item_multiplayer_item_class, multi_item_class_type_horse),
      (item_set_slot, "itm_courser", slot_item_multiplayer_item_class, multi_item_class_type_horse),
      (item_set_slot, "itm_hunter", slot_item_multiplayer_item_class, multi_item_class_type_horse),
      (item_set_slot, "itm_warhorse", slot_item_multiplayer_item_class, multi_item_class_type_horse),
      (item_set_slot, "itm_charger", slot_item_multiplayer_item_class, multi_item_class_type_horse),
      (item_set_slot, "itm_steppe_horse", slot_item_multiplayer_item_class, multi_item_class_type_horse),
      (item_set_slot, "itm_arabian_horse_a", slot_item_multiplayer_item_class, multi_item_class_type_horse),
      (item_set_slot, "itm_arabian_horse_b", slot_item_multiplayer_item_class, multi_item_class_type_horse),
	  (item_set_slot, "itm_warhorse_steppe", slot_item_multiplayer_item_class, multi_item_class_type_horse),
	  (item_set_slot, "itm_warhorse_sarranid", slot_item_multiplayer_item_class, multi_item_class_type_horse),


      #1-Swadian Warriors
      #1a-Swadian Crossbowman
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_bolts", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_steel_bolts", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_crossbow", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_heavy_crossbow", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sniper_crossbow", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_a", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_b", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_b_small", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_heater_a", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_heater_b", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_heater_c", "trp_swadian_crossbowman_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_red_shirt", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_padded_cloth", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_armor", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_haubergeon", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_ankle_boots", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_boots", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_chausses", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_swadian_crossbowman_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arming_cap", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_norman_helmet", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_helmet_with_neckguard", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_flat_topped_helmet", "trp_swadian_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_guard_helmet", "trp_swadian_crossbowman_multiplayer"),

      #1b-Swadian Infantry
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_awlpike", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_awlpike_long", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_a", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_b", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_b_small", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_c", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_c_small", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_bastard_sword_a", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_bastard_sword_b", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_two_handed_a", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_two_handed_b", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_darts", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_war_darts", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_heater_a", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_heater_b", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_heater_c", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_heater_d", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_red_tunic", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_red_gambeson", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_armor", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_haubergeon", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_brigandine_red", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_ankle_boots", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_boots", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_chausses", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_greaves", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arming_cap", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_norman_helmet", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_helmet_with_neckguard", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_flat_topped_helmet", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_guard_helmet", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_great_helmet", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_mittens", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scale_gauntlets", "trp_swadian_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gauntlets", "trp_swadian_infantry_multiplayer"),

      #1c-Swadian Man At Arms
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_darts", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_war_darts", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lance", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_heavy_lance", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_great_lance", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_a", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_b", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_b_small", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_c", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_c_small", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_bastard_sword_a", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_bastard_sword_b", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_heater_a", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_heater_b", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_heater_c", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_heater_d", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_red_tunic", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_padded_cloth", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_armor", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_with_surcoat", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_coat_of_plates_red", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_ankle_boots", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_boots", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_chausses", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_greaves", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_plate_boots", "trp_swadian_man_at_arms_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arming_cap", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_norman_helmet", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_helmet_with_neckguard", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_flat_topped_helmet", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_guard_helmet", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_great_helmet", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_mittens", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scale_gauntlets", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gauntlets", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_saddle_horse", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_courser", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hunter", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_warhorse", "trp_swadian_man_at_arms_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_charger", "trp_swadian_man_at_arms_multiplayer"),

      # #1d-Swadian Mounted Crossbowman
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_bolts", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_light_crossbow", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_crossbow", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_heavy_crossbow", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_heater_cav_a", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_heater_cav_b", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_bastard_sword_a", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_red_shirt", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_padded_cloth", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_armor", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_with_surcoat", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_coat_of_plates_red", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hide_boots", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arming_cap", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_norman_helmet", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_helmet_with_neckguard", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_flat_topped_helmet", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_guard_helmet", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_saddle_horse", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_courser", "trp_swadian_mounted_crossbowman_multiplayer"),
      # (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hunter", "trp_swadian_mounted_crossbowman_multiplayer"),

      #2-Vaegir Warriors
      #2a-Vaegir Archer
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arrows", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_barbed_arrows", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mace_1", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mace_2", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_falchion", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nomad_bow", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_khergit_bow", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_strong_bow", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_war_bow", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_linen_tunic", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_jerkin", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_vest", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lamellar_vest", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hide_boots", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nomad_boots", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_leather_greaves", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nomad_cap", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_fur_cap", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_fur_helmet", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_spiked_helmet", "trp_vaegir_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_lamellar_helmet", "trp_vaegir_archer_multiplayer"),

      #2b-Vaegir Spearman
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_spear", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_war_spear", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_awlpike", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_kite_a", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_kite_b", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_kite_c", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_kite_d", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mace_1", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mace_2", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mace_3", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mace_4", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_long_hafted_spiked_mace", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_long_spiked_club", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scimitar", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scimitar_b", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_bardiche", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_great_bardiche", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_long_bardiche", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_great_long_bardiche", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_javelin", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_linen_tunic", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_jerkin", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_vest", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lamellar_vest", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lamellar_armor", "trp_vaegir_spearman_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_elite_armor", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hide_boots", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nomad_boots", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_leather_greaves", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_greaves", "trp_vaegir_spearman_multiplayer"),
#      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_spiked_helmet", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_fur_cap", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_fur_helmet", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_spiked_helmet", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_lamellar_helmet", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_noble_helmet", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_war_helmet", "trp_vaegir_spearman_multiplayer"),
	  #      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nasal_helmet", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_mittens", "trp_vaegir_spearman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scale_gauntlets", "trp_vaegir_spearman_multiplayer"),

      #2c-Vaegir Horseman
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_darts", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_war_darts", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_bardiche", "trp_vaegir_horseman_multiplayer"),
#      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_great_bardiche", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scimitar", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scimitar_b", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lance", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_heavy_lance", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_kite_cav_a", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_kite_cav_b", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_kite_c", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_kite_d", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_linen_tunic", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_vest", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lamellar_vest", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_studded_leather_coat", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lamellar_armor", "trp_vaegir_horseman_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_elite_armor", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hide_boots", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nomad_boots", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_leather_greaves", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_greaves", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_plate_boots", "trp_vaegir_horseman_multiplayer"),
#      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_spiked_helmet", "trp_vaegir_horseman_multiplayer"),
#      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nasal_helmet", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_fur_cap", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_fur_helmet", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_spiked_helmet", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_lamellar_helmet", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_noble_helmet", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_war_helmet", "trp_vaegir_horseman_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_vaegir_mask", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_mittens", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scale_gauntlets", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_saddle_horse", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_courser", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hunter", "trp_vaegir_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_warhorse_steppe", "trp_vaegir_horseman_multiplayer"),

      #3-Khergit Warriors
      #3a-Khergit Veteran Horse Archer
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_khergit_1", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_khergit_2", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_khergit_3", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_khergit_4", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nomad_bow", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_khergit_bow", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_strong_bow", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arrows", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_khergit_arrows", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_steppe_cap_a", "trp_khergit_veteran_horse_archer_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nomad_cap_b", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_steppe_cap_b", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_steppe_cap", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_khergit_armor", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_steppe_armor", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tribal_warrior_outfit", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lamellar_vest_khergit", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hide_boots", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nomad_boots", "trp_khergit_veteran_horse_archer_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_khergit_leather_boots", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_leather_greaves", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_greaves", "trp_khergit_veteran_horse_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_steppe_horse", "trp_khergit_veteran_horse_archer_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_khergit_veteran_horse_archer_multiplayer"),
      #3a-Khergit Dismounted Lancer
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_javelin", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_jarid", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_khergit_1", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_khergit_2", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_khergit_3", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_khergit_4", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_small_round_a", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_small_round_b", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_small_round_c", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_round_b", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_round_c", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_spear", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hafted_blade_a", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hafted_blade_b", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mace_1", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mace_2", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mace_3", "trp_khergit_infantry_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nomad_cap_b", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_steppe_cap_b", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_steppe_cap", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_khergit_war_helmet", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_khergit_guard_helmet", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_steppe_armor", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tribal_warrior_outfit", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lamellar_armor", "trp_khergit_infantry_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_khergit_elite_armor", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hide_boots", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nomad_boots", "trp_khergit_infantry_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_khergit_leather_boots", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_leather_greaves", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_greaves", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_mittens", "trp_khergit_infantry_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scale_gauntlets", "trp_khergit_infantry_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lamellar_gauntlets", "trp_khergit_infantry_multiplayer"),
      #3a-Khergit Lancer
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_javelin", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_khergit_1", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_khergit_2", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_khergit_3", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_khergit_4", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_small_round_a", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_small_round_b", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_small_round_c", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lance", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_heavy_lance", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hafted_blade_a", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hafted_blade_b", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_one_handed_war_axe_a", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_steppe_cap_a", "trp_khergit_lancer_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nomad_cap_b", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_steppe_cap_b", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_steppe_cap", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_khergit_war_helmet", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_khergit_armor", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_steppe_armor", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tribal_warrior_outfit", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lamellar_armor", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hide_boots", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nomad_boots", "trp_khergit_lancer_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_khergit_leather_boots", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_leather_greaves", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_greaves", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_mittens", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scale_gauntlets", "trp_khergit_lancer_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lamellar_gauntlets", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_steppe_horse", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_courser", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hunter", "trp_khergit_lancer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_warhorse_steppe", "trp_khergit_lancer_multiplayer"),

      #Nord Warriors

      #4c-Nord Archer
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arrows", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_barbed_arrows", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_bodkin_arrows", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_viking_1", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_viking_2", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_viking_2_small", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_viking_3", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_viking_3_small", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_one_handed_war_axe_a", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_one_handed_war_axe_b", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_two_handed_axe", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_short_bow", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_long_bow", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_blue_tunic", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_jerkin", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_byrnie", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_boots", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_leather_greaves", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_chausses", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_boots", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nordic_archer_helmet", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nordic_veteran_archer_helmet", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nordic_footman_helmet", "trp_nord_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nordic_fighter_helmet", "trp_nord_archer_multiplayer"),

      #4a-Nord Veteran
#      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_darts", "trp_nord_veteran_multiplayer"),
#      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_war_darts", "trp_nord_veteran_multiplayer"),
#      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_javelin", "trp_nord_veteran_multiplayer"),
#      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_throwing_spears", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_viking_1", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_viking_2", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_viking_2_small", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_viking_3", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_viking_3_small", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_one_handed_war_axe_a", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_one_handed_war_axe_b", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_one_handed_battle_axe_a", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_one_handed_battle_axe_b", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_one_handed_battle_axe_c", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_two_handed_axe", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_two_handed_battle_axe_2", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_great_axe", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_long_axe", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_long_axe_b", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_long_axe_c", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_spear", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_war_spear", "trp_nord_veteran_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_round_a", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_round_b", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_round_c", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_round_d", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_round_e", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_light_throwing_axes", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_throwing_axes", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_heavy_throwing_axes", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nordic_veteran_archer_helmet", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nordic_footman_helmet", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nordic_fighter_helmet", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nordic_huscarl_helmet", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nordic_warlord_helmet", "trp_nord_veteran_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_blue_tunic", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_jerkin", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_shirt", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_hauberk", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_banded_armor", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_boots", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_leather_greaves", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_chausses", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_boots", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_mittens", "trp_nord_veteran_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scale_gauntlets", "trp_nord_veteran_multiplayer"),

      #4b-Nord Scout
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_darts", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_war_darts", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_javelin", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_throwing_spears", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_light_throwing_axes", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_throwing_axes", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_viking_1", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_viking_2", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_viking_3", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_two_handed_axe", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_two_handed_battle_axe_2", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_shortened_voulge", "trp_nord_scout_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_spear", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_war_spear", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_light_lance", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lance", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_small_round_a", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_small_round_b", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_small_round_c", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nordic_archer_helmet", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nordic_veteran_archer_helmet", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nordic_footman_helmet", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nordic_fighter_helmet", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nordic_huscarl_helmet", "trp_nord_scout_multiplayer"),


      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_blue_tunic", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_jerkin", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_shirt", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_hauberk", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_boots", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_leather_greaves", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_chausses", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_boots", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_mittens", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scale_gauntlets", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_saddle_horse", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_courser", "trp_nord_scout_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hunter", "trp_nord_scout_multiplayer"),


      #5-Rhodok Warriors
      #5a-Rhodok Veteran Crossbowman
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_crossbow", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_heavy_crossbow", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sniper_crossbow", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_bolts", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_steel_bolts", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_fighting_pick", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_military_pick", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_club_with_spike_head", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_maul", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sledgehammer", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_a", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_b", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_b_small", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_pavise_a", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_pavise_b", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_pavise_c", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_pavise_d", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_cap", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_padded_coif", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_footman_helmet", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_kettle_hat", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tunic_with_green_cape", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_aketon_green", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_armor", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_ankle_boots", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_boots", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_greaves", "trp_rhodok_veteran_crossbowman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_rhodok_veteran_crossbowman_multiplayer"),

	  #5b-Rhodok Sergeant
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_darts", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_war_darts", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_javelin", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_fighting_pick", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_military_pick", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_morningstar", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_club_with_spike_head", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_military_cleaver_b", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_military_cleaver_c", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_two_handed_cleaver", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_military_sickle_a", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_maul", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sledgehammer", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_warhammer", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_spear", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_pike", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_ashwood_pike", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_war_spear", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_glaive", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_pavise_a", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_pavise_b", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_pavise_c", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_pavise_d", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_cap", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_padded_coif", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_footman_helmet", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_kettle_hat", "trp_rhodok_sergeant_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_bascinet_2", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_full_helm", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_green_tunic", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_aketon_green", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_ragged_outfit", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_armor", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_surcoat_over_mail", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_ankle_boots", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_boots", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_greaves", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_iron_greaves", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_mittens", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scale_gauntlets", "trp_rhodok_sergeant_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gauntlets", "trp_rhodok_sergeant_multiplayer"),

	  #5c-Rhodok Horseman
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_darts", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_war_darts", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_javelin", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_a", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_b", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sword_medieval_c", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_fighting_pick", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_military_pick", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_morningstar", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_military_cleaver_b", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_military_cleaver_c", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_two_handed_cleaver", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_shortened_military_scythe", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_light_lance", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lance", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_heavy_lance", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_heater_cav_a", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_heater_cav_b", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_padded_coif", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_footman_helmet", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_kettle_hat", "trp_rhodok_horseman_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_bascinet_3", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_green_tunic", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_aketon_green", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_ragged_outfit", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_armor", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_surcoat_over_mail", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_ankle_boots", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_boots", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_splinted_greaves", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_plate_boots", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_mittens", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scale_gauntlets", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_gauntlets", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_saddle_horse", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_courser", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_hunter", "trp_rhodok_horseman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_warhorse", "trp_rhodok_horseman_multiplayer"),



      #6-Sarranid Warriors
      #5a-Sarranid archer
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_cloth_robe", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_skirmisher_armor", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_archers_vest", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arabian_armor_b", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_felt_hat", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_turban", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_desert_turban", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_mail_coif", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_horseman_helmet", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_warrior_cap", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_boots_b", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_boots_c", "trp_sarranid_archer_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_short_bow", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_nomad_bow", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arrows", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_barbed_arrows", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scimitar", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mace_1", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arabian_sword_a", "trp_sarranid_archer_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arabian_sword_b", "trp_sarranid_archer_multiplayer"),

	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_sarranid_archer_multiplayer"),



	  #Sarranid footman
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_cloth_robe", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_skirmisher_armor", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_archers_vest", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_leather_armor", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arabian_armor_b", "trp_sarranid_footman_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_elite_armor", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_felt_hat", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_turban", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_desert_turban", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_mail_coif", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_warrior_cap", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_veiled_helmet", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_boots_b", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_boots_c", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_boots_d", "trp_sarranid_footman_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arabian_sword_a", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arabian_sword_b", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arabian_sword_d", "trp_sarranid_footman_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_mace_1", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_axe_a", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_axe_b", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_two_handed_axe_a", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_two_handed_axe_b", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_two_handed_mace_1", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_bamboo_spear", "trp_sarranid_footman_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_spear", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_jarid", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_javelin", "trp_sarranid_footman_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_kite_a", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_kite_b", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_kite_c", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_kite_d", "trp_sarranid_footman_multiplayer"),

	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_sarranid_footman_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_mittens", "trp_sarranid_footman_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scale_gauntlets", "trp_sarranid_footman_multiplayer"),




	  #Sarranid mamluke
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_cloth_robe", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_skirmisher_armor", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_archers_vest", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_mail_shirt", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_cavalry_robe", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mamluke_mail", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_elite_armor", "trp_sarranid_mamluke_multiplayer"),


      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_turban", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_desert_turban", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_horseman_helmet", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_mail_coif", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_veiled_helmet", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_boots_b", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_boots_c", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_boots_d", "trp_sarranid_mamluke_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arabian_sword_a", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arabian_sword_b", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_cavalry_sword", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arabian_sword_d", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_mace_1", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_axe_a", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_axe_b", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_sarranid_two_handed_axe_a", "trp_sarranid_mamluke_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_lance", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_heavy_lance", "trp_sarranid_mamluke_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_jarid", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_javelin", "trp_sarranid_mamluke_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_small_round_a", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_small_round_b", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_tab_shield_small_round_c", "trp_sarranid_mamluke_multiplayer"),

      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_saddle_horse", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arabian_horse_a", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_arabian_horse_b", "trp_sarranid_mamluke_multiplayer"),
      (call_script, "script_multiplayer_set_item_available_for_troop", "itm_warhorse_sarranid", "trp_sarranid_mamluke_multiplayer"),

	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_leather_gloves", "trp_sarranid_mamluke_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_mail_mittens", "trp_sarranid_mamluke_multiplayer"),
	  (call_script, "script_multiplayer_set_item_available_for_troop", "itm_scale_gauntlets", "trp_sarranid_mamluke_multiplayer"),


      ]),

  #script_get_army_size_from_slider_value
  # This script is called from the game engine when user enters "cheatmenu from command console (ctrl+~).
  # INPUT:
  # none
  # OUTPUT:
  # none
  ("game_enable_cheat_menu",
    [
      (store_script_param, ":input", 1),
      (try_begin),
        (eq, ":input", 0),
        (assign, "$cheat_mode", 0),
      (else_try),
        (eq, ":input", 1),
        (assign, "$cheat_mode", 1),
        #SB : flavour text
        (call_script, "script_objectionable_action", tmt_honest, "str_stop_cheating"),
      (try_end),
      (try_begin),
        (neg|is_presentation_active, "prsnt_modify_slots"),
        # (assign, "$g_talk_troop", ":input"),
        (assign, "$g_presentation_state", 0),
        (assign, "$g_presentation_input", rename_companion),
        (start_presentation, "prsnt_modify_slots"),
      (try_end),
      ]),

  #script_game_get_console_command
  # This script is called from the game engine when a console command is entered from the dedicated server.
  # INPUT: anything
  # OUTPUT: s0 = result text
  ("game_get_console_command",
   [
     (store_script_param, ":input", 1),
     (store_script_param, ":val1", 2),
     (try_begin),
       #getting val2 for some commands
       (eq, ":input", 2),
       (store_script_param, ":val2", 3),
     (end_try),
     (try_begin),
       (eq, ":input", 1),
       (assign, reg0, ":val1"),
       (try_begin),
         (eq, ":val1", 1),
         (assign, reg1, "$g_multiplayer_num_bots_team_1"),
         (str_store_string, s0, "str_team_reg0_bot_count_is_reg1"),
       (else_try),
         (eq, ":val1", 2),
         (assign, reg1, "$g_multiplayer_num_bots_team_2"),
         (str_store_string, s0, "str_team_reg0_bot_count_is_reg1"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 2),
       (assign, reg0, ":val1"),
       (assign, reg1, ":val2"),
       (try_begin),
         (eq, ":val1", 1),
         (ge, ":val2", 0),
         (assign, "$g_multiplayer_num_bots_team_1", ":val2"),
         (str_store_string, s0, "str_team_reg0_bot_count_is_reg1"),
       (else_try),
         (eq, ":val1", 2),
         (ge, ":val2", 0),
         (assign, "$g_multiplayer_num_bots_team_2", ":val2"),
         (str_store_string, s0, "str_team_reg0_bot_count_is_reg1"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 3),
       (assign, reg0, "$g_multiplayer_round_max_seconds"),
       (str_store_string, s0, "str_maximum_seconds_for_round_is_reg0"),
     (else_try),
       (eq, ":input", 4),
       (assign, reg0, ":val1"),
       (try_begin),
         (is_between, ":val1", multiplayer_round_max_seconds_min, multiplayer_round_max_seconds_max),
         (assign, "$g_multiplayer_round_max_seconds", ":val1"),
         (str_store_string, s0, "str_maximum_seconds_for_round_is_reg0"),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_round_max_seconds, ":val1"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 5),
       (assign, reg0, "$g_multiplayer_respawn_period"),
       (str_store_string, s0, "str_respawn_period_is_reg0_seconds"),
     (else_try),
       (eq, ":input", 6),
       (assign, reg0, ":val1"),
       (try_begin),
         (is_between, ":val1", multiplayer_respawn_period_min, multiplayer_respawn_period_max),
         (assign, "$g_multiplayer_respawn_period", ":val1"),
         (str_store_string, s0, "str_respawn_period_is_reg0_seconds"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 7),
       (assign, reg0, "$g_multiplayer_num_bots_voteable"),
       (str_store_string, s0, "str_bots_upper_limit_for_votes_is_reg0"),
     (else_try),
       (eq, ":input", 8),
       (try_begin),
         (is_between, ":val1", 0, 51),
         (assign, "$g_multiplayer_num_bots_voteable", ":val1"),
         (store_add, "$g_multiplayer_max_num_bots", ":val1", 1),
         (assign, reg0, "$g_multiplayer_num_bots_voteable"),
         (str_store_string, s0, "str_bots_upper_limit_for_votes_is_reg0"),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_num_bots_voteable, ":val1"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 9),
       (try_begin),
         (eq, "$g_multiplayer_maps_voteable", 1),
         (str_store_string, s0, "str_map_is_voteable"),
       (else_try),
         (str_store_string, s0, "str_map_is_not_voteable"),
       (try_end),
     (else_try),
       (eq, ":input", 10),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_maps_voteable", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_map_is_voteable"),
         (else_try),
           (str_store_string, s0, "str_map_is_not_voteable"),
         (try_end),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_maps_voteable, ":val1"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 11),
       (try_begin),
         (eq, "$g_multiplayer_factions_voteable", 1),
         (str_store_string, s0, "str_factions_are_voteable"),
       (else_try),
         (str_store_string, s0, "str_factions_are_not_voteable"),
       (try_end),
     (else_try),
       (eq, ":input", 12),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_factions_voteable", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_factions_are_voteable"),
         (else_try),
           (str_store_string, s0, "str_factions_are_not_voteable"),
         (try_end),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_factions_voteable, ":val1"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 13),
       (try_begin),
         (eq, "$g_multiplayer_player_respawn_as_bot", 1),
         (str_store_string, s0, "str_players_respawn_as_bot"),
       (else_try),
         (str_store_string, s0, "str_players_do_not_respawn_as_bot"),
       (try_end),
     (else_try),
       (eq, ":input", 14),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_player_respawn_as_bot", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_players_respawn_as_bot"),
         (else_try),
           (str_store_string, s0, "str_players_do_not_respawn_as_bot"),
         (try_end),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_player_respawn_as_bot, ":val1"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 15),
       (try_begin),
         (eq, "$g_multiplayer_kick_voteable", 1),
         (str_store_string, s0, "str_kicking_a_player_is_voteable"),
       (else_try),
         (str_store_string, s0, "str_kicking_a_player_is_not_voteable"),
       (try_end),
     (else_try),
       (eq, ":input", 16),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_kick_voteable", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_kicking_a_player_is_voteable"),
         (else_try),
           (str_store_string, s0, "str_kicking_a_player_is_not_voteable"),
         (try_end),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_kick_voteable, ":val1"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 17),
       (try_begin),
         (eq, "$g_multiplayer_ban_voteable", 1),
         (str_store_string, s0, "str_banning_a_player_is_voteable"),
       (else_try),
         (str_store_string, s0, "str_banning_a_player_is_not_voteable"),
       (try_end),
     (else_try),
       (eq, ":input", 18),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_ban_voteable", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_banning_a_player_is_voteable"),
         (else_try),
           (str_store_string, s0, "str_banning_a_player_is_not_voteable"),
         (try_end),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_ban_voteable, ":val1"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 19),
       (assign, reg0, "$g_multiplayer_valid_vote_ratio"),
       (str_store_string, s0, "str_percentage_of_yes_votes_required_for_a_poll_to_get_accepted_is_reg0"),
     (else_try),
       (eq, ":input", 20),
       (try_begin),
         (is_between, ":val1", 50, 101),
         (assign, "$g_multiplayer_valid_vote_ratio", ":val1"),
         (assign, reg0, ":val1"),
         (str_store_string, s0, "str_percentage_of_yes_votes_required_for_a_poll_to_get_accepted_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 21),
       (assign, reg0, "$g_multiplayer_auto_team_balance_limit"),
       (str_store_string, s0, "str_auto_team_balance_threshold_is_reg0"),
     (else_try),
       (eq, ":input", 22),
       (try_begin),
         (is_between, ":val1", 2, 7),
         (assign, "$g_multiplayer_auto_team_balance_limit", ":val1"),
         (assign, reg0, "$g_multiplayer_auto_team_balance_limit"),
         (str_store_string, s0, "str_auto_team_balance_threshold_is_reg0"),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_auto_team_balance_limit, ":val1"),
         (try_end),
       (else_try),
         (ge, ":val1", 7),
         (assign, "$g_multiplayer_auto_team_balance_limit", 1000),
         (assign, reg0, "$g_multiplayer_auto_team_balance_limit"),
         (str_store_string, s0, "str_auto_team_balance_threshold_is_reg0"),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_auto_team_balance_limit, ":val1"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 23),
       (assign, reg0, "$g_multiplayer_initial_gold_multiplier"),
       (str_store_string, s0, "str_starting_gold_ratio_is_reg0"),
     (else_try),
       (eq, ":input", 24),
       (try_begin),
         (is_between, ":val1", 0, 1001),
         (assign, "$g_multiplayer_initial_gold_multiplier", ":val1"),
         (assign, reg0, "$g_multiplayer_initial_gold_multiplier"),
         (str_store_string, s0, "str_starting_gold_ratio_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 25),
       (assign, reg0, "$g_multiplayer_battle_earnings_multiplier"),
       (str_store_string, s0, "str_combat_gold_bonus_ratio_is_reg0"),
     (else_try),
       (eq, ":input", 26),
       (try_begin),
         (is_between, ":val1", 0, 1001),
         (assign, "$g_multiplayer_battle_earnings_multiplier", ":val1"),
         (assign, reg0, "$g_multiplayer_battle_earnings_multiplier"),
         (str_store_string, s0, "str_combat_gold_bonus_ratio_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 27),
       (assign, reg0, "$g_multiplayer_round_earnings_multiplier"),
       (str_store_string, s0, "str_round_gold_bonus_ratio_is_reg0"),
     (else_try),
       (eq, ":input", 28),
       (try_begin),
         (is_between, ":val1", 0, 1001),
         (assign, "$g_multiplayer_round_earnings_multiplier", ":val1"),
         (assign, reg0, "$g_multiplayer_round_earnings_multiplier"),
         (str_store_string, s0, "str_round_gold_bonus_ratio_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 29),
       (try_begin),
         (eq, "$g_multiplayer_allow_player_banners", 1),
         (str_store_string, s0, "str_player_banners_are_allowed"),
       (else_try),
         (str_store_string, s0, "str_player_banners_are_not_allowed"),
       (try_end),
     (else_try),
       (eq, ":input", 30),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_allow_player_banners", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_player_banners_are_allowed"),
         (else_try),
           (str_store_string, s0, "str_player_banners_are_not_allowed"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 31),
       (try_begin),
         (eq, "$g_multiplayer_force_default_armor", 1),
         (str_store_string, s0, "str_default_armor_is_forced"),
       (else_try),
         (str_store_string, s0, "str_default_armor_is_not_forced"),
       (try_end),
     (else_try),
       (eq, ":input", 32),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_force_default_armor", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_default_armor_is_forced"),
         (else_try),
           (str_store_string, s0, "str_default_armor_is_not_forced"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 33),
       (assign, reg0, "$g_multiplayer_point_gained_from_flags"),
       (str_store_string, s0, "str_point_gained_from_flags_is_reg0"),
     (else_try),
       (eq, ":input", 34),
       (try_begin),
         (is_between, ":val1", 25, 401),
         (assign, "$g_multiplayer_point_gained_from_flags", ":val1"),
         (assign, reg0, "$g_multiplayer_point_gained_from_flags"),
         (str_store_string, s0, "str_point_gained_from_flags_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 35),
       (assign, reg0, "$g_multiplayer_point_gained_from_capturing_flag"),
       (str_store_string, s0, "str_point_gained_from_capturing_flag_is_reg0"),
     (else_try),
       (eq, ":input", 36),
       (try_begin),
         (is_between, ":val1", 0, 11),
         (assign, "$g_multiplayer_point_gained_from_capturing_flag", ":val1"),
         (assign, reg0, "$g_multiplayer_point_gained_from_capturing_flag"),
         (str_store_string, s0, "str_point_gained_from_capturing_flag_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 37),
       (assign, reg0, "$g_multiplayer_game_max_minutes"),
       (str_store_string, s0, "str_map_time_limit_is_reg0"),
     (else_try),
       (eq, ":input", 38),
       (try_begin),
         (is_between, ":val1", 5, 121),
         (assign, "$g_multiplayer_game_max_minutes", ":val1"),
         (assign, reg0, "$g_multiplayer_game_max_minutes"),
         (str_store_string, s0, "str_map_time_limit_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 39),
       (assign, reg0, "$g_multiplayer_game_max_points"),
       (str_store_string, s0, "str_team_points_limit_is_reg0"),
     (else_try),
       (eq, ":input", 40),
       (try_begin),
         (is_between, ":val1", 3, 1001),
         (assign, "$g_multiplayer_game_max_points", ":val1"),
         (assign, reg0, "$g_multiplayer_game_max_points"),
         (str_store_string, s0, "str_team_points_limit_is_reg0"),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 41),
       (assign, reg0, "$g_multiplayer_number_of_respawn_count"),
       (try_begin),
         (eq, reg0, 0),
         (str_store_string, s1, "str_unlimited"),
       (else_try),
         (str_store_string, s1, "str_reg0"),
       (try_end),
       (str_store_string, s0, "str_defender_spawn_count_limit_is_s1"),
     (else_try),
       (eq, ":input", 42),
       (try_begin),
         (is_between, ":val1", 0, 6),
         (assign, "$g_multiplayer_number_of_respawn_count", ":val1"),
         (assign, reg0, "$g_multiplayer_number_of_respawn_count"),
         (try_begin),
           (eq, reg0, 0),
           (str_store_string, s1, "str_unlimited"),
         (else_try),
           (str_store_string, s1, "str_reg0"),
         (try_end),
         (str_store_string, s0, "str_defender_spawn_count_limit_is_s1"),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_respawn_count, ":val1"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (eq, ":input", 43),
       (try_begin),
         (eq, "$g_multiplayer_disallow_ranged_weapons", 1),
         (str_store_string, s0, "str_ranged_weapons_are_disallowed"),
       (else_try),
         (str_store_string, s0, "str_ranged_weapons_are_allowed"),
       (try_end),
     (else_try),
       (eq, ":input", 44),
       (try_begin),
         (is_between, ":val1", 0, 2),
         (assign, "$g_multiplayer_disallow_ranged_weapons", ":val1"),
         (try_begin),
           (eq, ":val1", 1),
           (str_store_string, s0, "str_ranged_weapons_are_disallowed"),
         (else_try),
           (str_store_string, s0, "str_ranged_weapons_are_allowed"),
         (try_end),
       (else_try),
         (str_store_string, s0, "str_input_is_not_correct_for_the_command_type_help_for_more_information"),
       (try_end),
     (else_try),
       (str_store_string, s0, "@{!}DEBUG : SYSTEM ERROR!"),
     (try_end),
  ]),


  # script_game_event_party_encounter:
  # This script is called whenever the game ends the battle between two parties on the map.
  # INPUT:
  # param1: Defender Party
  # param2: Attacker Party
  ("game_event_battle_end",
    [
##       (store_script_param_1, ":root_defender_party"),
##       (store_script_param_2, ":root_attacker_party"),

      #Fixing deleted heroes
      ##diplomacy start+ kingdom ladies may also potentially lead parties
      (try_for_range, ":cur_troop", heroes_begin, heroes_end),#<- changed active_npcs to heroes
      #diplomacy end+
		(this_or_next|troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
        (is_between, ":cur_troop", companions_begin, companions_end),
        (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
        (troop_get_slot, ":cur_prisoner_of_party", ":cur_troop", slot_troop_prisoner_of_party),
        (try_begin),
          (ge, ":cur_party", 0),
          (assign, ":continue", 0),
          (try_begin),
            (neg|party_is_active, ":cur_party"),
            (assign, ":continue", 1),
          (else_try),
            (party_count_companions_of_type, ":amount", ":cur_party", ":cur_troop"),
            (le, ":amount", 0),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_troop_name, s1, ":cur_troop"),
            (display_message, "@{!}DEBUG: {s1} no longer leads a party."),
          (try_end),

          (troop_set_slot, ":cur_troop", slot_troop_leaded_party, -1),
          #(str_store_troop_name, s5, ":cur_troop"),
          #(display_message, "@{!}DEBUG : {s5}'s troop_leaded_party set to -1"),
        (try_end),
        (try_begin),
          (ge, ":cur_prisoner_of_party", 0),
          (assign, ":continue", 0),
          (try_begin),
            (neg|party_is_active, ":cur_prisoner_of_party"),
            (assign, ":continue", 1),
          (else_try),
            (party_count_prisoners_of_type, ":amount", ":cur_prisoner_of_party", ":cur_troop"),
            (le, ":amount", 0),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_troop_name, s1, ":cur_troop"),
            (display_message, "@{!}DEBUG: {s1} is no longer a prisoner."),
          (try_end),
          (call_script, "script_remove_troop_from_prison", ":cur_troop"),
          #searching player
          (try_begin),
            (party_count_prisoners_of_type, ":amount", "p_main_party", ":cur_troop"),
            (gt, ":amount", 0),
            (troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, "p_main_party"),
            (troop_set_slot, ":cur_troop", slot_troop_courtesan, -1),
            (assign, ":continue", 0),
            (try_begin),
              (eq, "$cheat_mode", 1),
              (str_store_troop_name, s1, ":cur_troop"),
              (display_message, "@{!}DEBUG: {s1} is now a prisoner of player."),
            (try_end),
          (try_end),
          (eq, ":continue", 1),
		  ##diplomacy start+
		  #Add increased information for affiliates.
		  (call_script, "script_dplmc_store_troop_is_eligible_for_affiliate_messages", ":cur_troop"),
		  (assign, ":is_affiliated", reg0),
		  ##diplomacy end+
          #searching kingdom heroes
	  ##diplomacy start+ support for promoted kingdom ladies
          (try_for_range, ":cur_troop_2", heroes_begin, heroes_end),#<-- changed active_npcs to heroes
          ##diplomacy end+
			(this_or_next|troop_slot_eq, ":cur_troop_2", slot_troop_occupation, slto_kingdom_hero),
            (is_between, ":cur_troop_2", companions_begin, companions_end),
			(eq, ":continue", 1),
            (troop_get_slot, ":cur_prisoner_of_party_2", ":cur_troop_2", slot_troop_leaded_party),
            (party_is_active, ":cur_prisoner_of_party_2"),
            (party_count_prisoners_of_type, ":amount", ":cur_prisoner_of_party_2", ":cur_troop"),
            (gt, ":amount", 0),
            (troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, ":cur_prisoner_of_party_2"),
            (assign, ":continue", 0),
            (try_begin),
			##diplomacy start+ Show for affiliates
			  (ge, ":is_affiliated", 1),
			  (str_store_troop_name, s1, ":cur_troop"),
			  (str_store_party_name, s2, ":cur_prisoner_of_party_2"),
			  (display_message, "@{s1} is now a prisoner of {s2}."),
			(else_try),
			##diplomacy end+
              (eq, "$cheat_mode", 1),
              (str_store_troop_name, s1, ":cur_troop"),
              (str_store_party_name, s2, ":cur_prisoner_of_party_2"),
              (display_message, "@{!}DEBUG: {s1} is now a prisoner of {s2}."),
            (try_end),
          (try_end),
          #searching walled centers
          (try_for_range, ":cur_prisoner_of_party_2", walled_centers_begin, walled_centers_end),
            (eq, ":continue", 1),
            (party_count_prisoners_of_type, ":amount", ":cur_prisoner_of_party_2", ":cur_troop"),
            (gt, ":amount", 0),
            (troop_set_slot, ":cur_troop", slot_troop_prisoner_of_party, ":cur_prisoner_of_party_2"),
            (assign, ":continue", 0),
            (try_begin),
			##diplomacy start+ Show for affiliates
			  (ge, ":is_affiliated", 1),
			  (str_store_troop_name, s1, ":cur_troop"),
			  (str_store_party_name, s2, ":cur_prisoner_of_party_2"),
			  (display_message, "@{s1} is now a prisoner of {s2}."),
			(else_try),
			##diplomacy end+
              (eq, "$cheat_mode", 1),
              (str_store_troop_name, s1, ":cur_troop"),
              (str_store_party_name, s2, ":cur_prisoner_of_party_2"),
              (display_message, "@{!}DEBUG: {s1} is now a prisoner of {s2}."),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
  ]),

  #script_order_best_besieger_party_to_guard_center:
  # This script is called from the game engine for calculating the buying price of any item.
  # INPUT:
  # param1: item_kind_id
  # OUTPUT:
  # trigger_result and reg0 = price_factor
  ("game_get_item_buy_price_factor",
    [
      (store_script_param_1, ":item_kind_id"),
      (assign, ":price_factor", 100),

      (call_script, "script_get_trade_penalty", ":item_kind_id"),
      (assign, ":trade_penalty", reg0),

      (try_begin),
        (is_between, "$g_encountered_party", centers_begin, centers_end),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":price_factor", "$g_encountered_party", ":item_slot_no"),

		#new
		#(try_begin),
		#	(is_between, "$g_encountered_party", villages_begin, villages_end),
		#	(party_get_slot, ":market_town", "$g_encountered_party", slot_village_market_town),
		#	(party_get_slot, ":price_in_market_town", ":market_town", ":item_slot_no"),
		#	(val_max, ":price_factor", ":price_in_market_town"),
		#(try_end),

		#For villages, the good will be sold no cheaper than in the market town
		#This represents the absence of a permanent market -- ie, the peasants retain goods to sell on their journeys to town, and are not about to do giveaway deals with passing adventurers


        (val_mul, ":price_factor", 100), #normalize price factor to range 0..100
        (val_div, ":price_factor", average_price_factor),
      (try_end),

      (store_add, ":penalty_factor", 100, ":trade_penalty"),

      (val_mul, ":price_factor", ":penalty_factor"),
      (val_div, ":price_factor", 100),

      (assign, reg0, ":price_factor"),
      (set_trigger_result, reg0),
  ]),

  #script_game_get_item_sell_price_factor:
  # This script is called from the game engine for calculating the selling price of any item.
  # INPUT:
  # param1: item_kind_id
  # OUTPUT:
  # trigger_result and reg0 = price_factor
  ("game_get_item_sell_price_factor",
    [
      (store_script_param_1, ":item_kind_id"),
      (assign, ":price_factor", 100),

      (call_script, "script_get_trade_penalty", ":item_kind_id"),
      (assign, ":trade_penalty", reg0),

      (try_begin),
        (is_between, "$g_encountered_party", centers_begin, centers_end),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":price_factor", "$g_encountered_party", ":item_slot_no"),
        (val_mul, ":price_factor", 100),#normalize price factor to range 0..100
        (val_div, ":price_factor", average_price_factor),
      (else_try),
        #increase trade penalty while selling weapons, armor, and horses
        (val_mul, ":trade_penalty", 4),
      (try_end),

	  ##diplomacy start+
	  #If economic changes are enabled, use a lesser trade penalty when selling
 	  #to the correct merchant in town.
	  (try_begin),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		(is_between, "$g_encountered_party", towns_begin, towns_end),
		(gt, "$g_talk_troop", "trp_player"),
		(try_begin),
			#Selling weapons to the weaponsmith
			(party_slot_eq, "$g_encountered_party", slot_town_weaponsmith, "$g_talk_troop"),
			(this_or_next|is_between, ":item_kind_id", weapons_begin, weapons_end),
			(this_or_next|is_between, ":item_kind_id", shields_begin, shields_end),
				(is_between, ":item_kind_id", ranged_weapons_begin, ranged_weapons_end),
			(val_mul, ":trade_penalty", 9),
			(val_div, ":trade_penalty", 10),
		(else_try),
			#Selling armor to the armorer
			(party_slot_eq, "$g_encountered_party", slot_town_armorer, "$g_talk_troop"),
			(is_between, ":item_kind_id", armors_begin, armors_end),
			(val_mul, ":trade_penalty", 9),
			(val_div, ":trade_penalty", 10),
		(else_try),
			#Selling horses to the horse merchant
			(party_slot_eq, "$g_encountered_party", slot_town_horse_merchant, "$g_talk_troop"),
			(is_between, ":item_kind_id", horses_begin, horses_end),
			(val_mul, ":trade_penalty", 9),
			(val_div, ":trade_penalty", 10),
		(try_end),
	  (try_end),

	  #If economic changes are enabled, increase food prices in a town under siege.
	  (try_begin),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		(is_between, "$g_encountered_party", centers_begin, centers_end),
		#Check selling food
		(is_between, ":item_kind_id", food_begin, food_end),
		#Check at a town or castle under siege for at least 48 hours
		(this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
			(party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
		(party_slot_eq, "$g_encountered_party", slot_village_state, svs_under_siege),

		(party_slot_ge, "$g_encountered_party", slot_center_is_besieged_by, 1),
		(party_get_slot, ":siege_start", "$g_encountered_party", slot_center_siege_begin_hours),
		(store_current_hours, ":cur_hours"),
		(store_sub, reg0, ":cur_hours", ":siege_start"),
		(ge, reg0, 48),
		#Check last caravan or village trading party arrival (default to eight weeks ago)
		(store_sub, ":last_arrival", ":cur_hours", 8 * 7 * 24),
		(val_min, ":last_arrival", ":siege_start"),
		(try_for_range, ":village_no", villages_begin, villages_end),
			(party_slot_eq, ":village_no", slot_village_market_town, "$g_encountered_party"),
			(party_get_slot, reg0, ":village_no", dplmc_slot_village_trade_last_arrived_to_market),
			(val_min, reg0, ":cur_hours"),
			(val_max, ":last_arrival", reg0),
		(try_end),
		(try_for_range, ":slot_no", dplmc_slot_town_trade_route_last_arrivals_begin, dplmc_slot_town_trade_route_last_arrivals_end),
			#Not all of these slots correspond to towns, but that doesn't
			#matter since their arrival times won't update after the start
			#of the game.
			(party_get_slot, reg0, "$g_encountered_party", ":slot_no"),
			(val_min, reg0, ":cur_hours"),
			(val_max, ":last_arrival", reg0),
		(try_end),
		##Increase food prices by 10% for every 3 days the siege has been going on,
		#or a minimum of 5%.
		#TODO: Make use of the last caravan arrival time.
		(store_sub, ":hours_since", ":cur_hours", ":siege_start"),
		(store_mul, ":siege_percent", ":hours_since", 10),
		(val_add, ":siege_percent", (3 * 24) // 2),
		(val_div, ":siege_percent", 3 * 24),
		(val_max, ":siege_percent", 5),
		(val_add, ":siege_percent", 100),
		(val_mul, ":price_factor", ":siege_percent"),
		(val_add, ":price_factor", 50),
		(val_div, ":price_factor", 100),
	  (try_end),
	  ##diplomacy end+

      (store_add, ":penalty_divisor", 100, ":trade_penalty"),

      (val_mul, ":price_factor", 100),
	  ##diplomacy start+
	  (try_begin),
		(gt, ":penalty_divisor", 0),
		(store_div, reg0, ":penalty_divisor", 2),
		(val_add, ":price_factor", reg0),#round correctly
	  (try_end),
	  ##diplomacy end+
      (val_div, ":price_factor", ":penalty_divisor"),

      (assign, reg0, ":price_factor"),
      (set_trigger_result, reg0),
  ]),

  # script_get_trade_penalty
  # This script is called from the game engine when player buys an item.
  # INPUT:
  # param1: item_kind_id
  ("game_event_buy_item",
    [
      (store_script_param_1, ":item_kind_id"),
      (store_script_param_2, ":reclaim_mode"),
      (try_begin),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":multiplier", "$g_encountered_party", ":item_slot_no"),
        (try_begin),
          (eq, ":reclaim_mode", 0),
          (val_add, ":multiplier", 20),
        (else_try),
          (val_add, ":multiplier", 30),
        (try_end),

        (store_item_value, ":item_value", ":item_kind_id"),
        (try_begin),
          (ge, ":item_value", 100),
          (store_sub, ":item_value_sub_100", ":item_value", 100),
          (store_div, ":item_value_sub_100_div_8", ":item_value_sub_100", 8),
          (val_add, ":multiplier", ":item_value_sub_100_div_8"),
        (try_end),
        (val_min, ":multiplier", maximum_price_factor),

        (party_set_slot, "$g_encountered_party", ":item_slot_no", ":multiplier"),
      (try_end),
  ]),

  #script_game_event_sell_item:
  # This script is called from the game engine when player sells an item.
  # INPUT:
  # param1: item_kind_id
  ("game_event_sell_item",
    [
      (store_script_param_1, ":item_kind_id"),
      (store_script_param_2, ":return_mode"),
      (try_begin),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":multiplier", "$g_encountered_party", ":item_slot_no"),
        (try_begin),
          (eq, ":return_mode", 0),
          (val_sub, ":multiplier", 30),
        (else_try),
          (val_sub, ":multiplier", 20),
        (try_end),

        (store_item_value, ":item_value", ":item_kind_id"),
        (try_begin),
          (ge, ":item_value", 100),
          (store_sub, ":item_value_sub_100", ":item_value", 100),
          (store_div, ":item_value_sub_100_div_8", ":item_value_sub_100", 8),
          (val_sub, ":multiplier", ":item_value_sub_100_div_8"),
        (try_end),
        (val_max, ":multiplier", minimum_price_factor),

        (party_set_slot, "$g_encountered_party", ":item_slot_no", ":multiplier"),
      (try_end),
  ]),

  #script_start_wedding_cutscene
  # This script is called from the game engine for calculating troop wages.
  # Input:
  # param1: troop_id, param2: party-id
  # Output: reg0: weekly wage

  ("game_get_troop_wage",
    [
      (store_script_param_1, ":troop_id"),
      (call_script, "script_initialize_exchange_screen_extensions", ":troop_id"), 
	  (troop_set_slot, "trp_temp_array_d", slot_last_requested_troop, ":troop_id"),

      (assign,":wage", 0),
      (try_begin),
        (this_or_next|eq, ":troop_id", "trp_player"),
        (eq, ":troop_id", "trp_kidnapped_girl"),
      (else_try),
        (is_between, ":troop_id", pretenders_begin, pretenders_end),
      ##diplomacy start+
      (else_try),
      #Temporarily joined lords and ladies don't require wages.
        (is_between, ":troop_id", heroes_begin, heroes_end),
        (this_or_next|troop_slot_eq, ":troop_id", slot_troop_playerparty_history,dplmc_pp_history_lord_rejoined),
        (this_or_next|troop_slot_eq, ":troop_id", slot_troop_occupation, slto_kingdom_hero),
           (troop_slot_eq, ":troop_id",slot_troop_occupation, slto_kingdom_lady),
      ##diplomacy end+
      (else_try),
        (store_character_level, ":troop_level", ":troop_id"),
        (assign, ":wage", ":troop_level"),
        (val_add, ":wage", 3),
        (val_mul, ":wage", ":wage"),
        (val_div, ":wage", 25),
      (try_end),

      (try_begin), #mounted troops cost 65% more than the normal cost
        (neg|is_between, ":troop_id", companions_begin, companions_end),
        (troop_is_mounted, ":troop_id"),
        (val_mul, ":wage", 5),
        (val_div, ":wage", 3),
      (try_end),

      (try_begin), #mercenaries cost %50 more than the normal cost
        (is_between, ":troop_id", mercenary_troops_begin, mercenary_troops_end),
        (val_mul, ":wage", 3),
        (val_div, ":wage", 2),
      (try_end),

      (try_begin),
        (is_between, ":troop_id", companions_begin, companions_end),
        (val_mul, ":wage", 2),
      (try_end),

      (store_skill_level, ":leadership_level", "skl_leadership", "trp_player"),
      (store_mul, ":leadership_bonus", 5, ":leadership_level"),
      (store_sub, ":leadership_factor", 100, ":leadership_bonus"),
      (val_mul, ":wage", ":leadership_factor"),  #wage = wage * (100 - 5*leadership)/100
	  (val_div, ":wage", 100),

      (try_begin),
        (neq, ":troop_id", "trp_player"),
        (neq, ":troop_id", "trp_kidnapped_girl"),
        (neg|is_between, ":troop_id", pretenders_begin, pretenders_end),
          ##diplomacy start+ For temporarily rejoined lords, and temporarily joined ladies
        (neg|troop_slot_eq, ":troop_id", slot_troop_playerparty_history,dplmc_pp_history_lord_rejoined),
        (neg|troop_slot_eq, ":troop_id", slot_troop_occupation, slto_kingdom_hero),
        (neg|is_between, ":troop_id", kingdom_ladies_begin, kingdom_ladies_end),
          ##diplomacy end+
        (val_max, ":wage", 1),
      (try_end),

      (assign, reg0, ":wage"),
      (set_trigger_result, reg0),
  ]),

  # script_game_get_total_wage
  # This script is called from the game engine for calculating total wage of the player party which is shown at the party window.
  # Input: none
  # Output: reg0: weekly wage

  ("game_get_total_wage",
    [
      (assign, ":total_wage", 0),
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
        (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
        (call_script, "script_game_get_troop_wage", ":stack_troop", 0),
        (val_mul, reg0, ":stack_size"),
        (val_add, ":total_wage", reg0),
      (try_end),
	  ##diplomacy start+
	  #If the player leads a kingdom, take into account centralization.
	  (faction_get_slot, ":centralization", "$players_kingdom", dplmc_slot_faction_centralization),
	  (try_begin),
		  (neq, ":centralization", 0),

		  (assign, reg0, 0),
	     (try_begin),
		     (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
		     (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
		     (ge, ":faction_leader", 0),
		     (this_or_next|eq, ":faction_leader", "trp_player"),
		     (this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
              (troop_slot_eq, "trp_player", slot_troop_spouse, reg0),
           (assign, reg0, 1),
        (try_end),

		  (this_or_next|eq, reg0, 1),
		     (eq, "$players_kingdom", "fac_player_supporters_faction"),
		  (faction_slot_eq, "$players_kingdom", slot_faction_state, sfs_active),

		  #Apply centralization, but limit it for nascent kingdoms
        (val_clamp, ":centralization", -3, 4),
	     (faction_get_slot, ":policy_limit", "$players_kingdom", slot_faction_num_towns),
	     (faction_get_slot, reg0, "$players_kingdom", slot_faction_num_castles),
	     (val_add, ":policy_limit", reg0),

	     (val_max, ":policy_limit", 0),
	     (val_min, ":centralization", ":policy_limit"),
	     (val_mul, ":policy_limit", -1),
	     (val_max, ":centralization", ":policy_limit"),

		  #Now reg0 is going to be the result again
		  (store_mul, reg0, ":centralization", -5),
		  (val_add, reg0, 100),
		  (val_mul, reg0, ":total_wage"),
		  (val_add, reg0, 50),#rounding
		  (val_div, reg0, 100),
	  (try_end),
    ##diplomacy end+
      (assign, reg0, ":total_wage"),
      (set_trigger_result, reg0),
  ]),

  # script_game_get_join_cost
  # This script is called from the game engine for calculating troop join cost.
  # Input:
  # param1: troop_id,
  # Output: reg0: weekly wage

  ("game_get_join_cost",
    [
      (store_script_param_1, ":troop_id"),

      (assign,":join_cost", 0),
      (try_begin),
        (troop_is_hero, ":troop_id"),
      (else_try),
        (store_character_level, ":troop_level", ":troop_id"),
        (store_add, ":join_cost", ":troop_level", 5),
        (val_mul, ":join_cost", ":join_cost"),
        (val_add, ":join_cost", 40),
        (val_div, ":join_cost", 5),
        (try_begin), #mounted troops cost %100 more than the normal cost
          (troop_is_mounted, ":troop_id"),
          (val_mul, ":join_cost", 2),
        (try_end),
      (try_end),
      (assign, reg0, ":join_cost"),
      (set_trigger_result, reg0),
  ]),

  # script_game_get_upgrade_xp
  # This script is called from game engine for calculating needed troop upgrade exp
  # Input:
  # param1: troop_id,
  # Output: reg0 = needed exp for upgrade
  ("game_get_upgrade_xp",
    [
      (store_script_param_1, ":troop_id"),

      (assign, ":needed_upgrade_xp", 0),
      #formula : int needed_upgrade_xp = 2 * (30 + 0.006f * level_boundaries[troops[troop_id].level + 3]);
      (store_character_level, ":troop_level", ":troop_id"),
      (store_add, ":needed_upgrade_xp", ":troop_level", 3),
      (get_level_boundary, reg0, ":needed_upgrade_xp"),
      (val_mul, reg0, 6),
      (val_div, reg0, 1000),
      (val_add, reg0, 30),

      (try_begin), #SB : merge range
        (is_between, ":troop_id", bandits_begin, bandits_end),
        (val_mul, reg0, 2),
      (try_end),

      (set_trigger_result, reg0),
  ]),

  # script_game_get_upgrade_cost
  # This script is called from game engine for calculating needed troop upgrade exp
  # Input:
  # param1: troop_id,
  # Output: reg0 = needed cost for upgrade
  ("game_get_upgrade_cost",
    [
      (store_script_param_1, ":troop_id"),

      (store_character_level, ":troop_level", ":troop_id"),

      (try_begin),
        (is_between, ":troop_level", 0, 6),
        (assign, reg0, 10),
      (else_try),
        (is_between, ":troop_level", 6, 11),
        (assign, reg0, 20),
      (else_try),
        (is_between, ":troop_level", 11, 16),
        (assign, reg0, 40),
      (else_try),
        (is_between, ":troop_level", 16, 21),
        (assign, reg0, 80),
      (else_try),
        (is_between, ":troop_level", 21, 26),
        (assign, reg0, 120),
      (else_try),
        (is_between, ":troop_level", 26, 31),
        (assign, reg0, 160),
      (else_try),
        (assign, reg0, 200),
      (try_end),

      (set_trigger_result, reg0),
  ]),

  # script_game_get_prisoner_price
  # This script is called from the game engine for calculating prisoner price
  # Input:
  # param1: troop_id,
  # Output: reg0
  ("game_get_prisoner_price",
    [
      (store_script_param_1, ":troop_id"),

      (try_begin), #SB : regular prices for constable selling
        (this_or_next|eq, "$g_talk_troop", "$g_player_constable"),
        (is_between, "$g_talk_troop", ransom_brokers_begin, ransom_brokers_end),
        (store_character_level, ":troop_level", ":troop_id"),
        (store_add, ":ransom_amount", ":troop_level", 10),
        # (val_add, ":ransom_amount", 10),
        (val_mul, ":ransom_amount", ":ransom_amount"),
        (val_div, ":ransom_amount", 6),
      (else_try),
        # (eq, "$g_talk_troop", "trp_brothel_madam"),
        # (assign, ":ransom_amount", 0),
      # (else_try),
        (assign, ":ransom_amount", 100),
      (try_end),

      (assign, reg0, ":ransom_amount"),

      (set_trigger_result, reg0),
  ]),


  # script_game_check_prisoner_can_be_sold
  # This script is called from the game engine for checking if a given troop can be sold.
  # Input:
  # param1: troop_id,
  # Output: reg0: 1= can be sold; 0= cannot be sold.

  ("game_check_prisoner_can_be_sold",
    [
      (store_script_param_1, ":troop_id"),
      (assign, reg0, 0),
      (try_begin),
        (neg|troop_is_hero, ":troop_id"),
        (try_begin),
          (check_quest_active, "qst_hunt_down_fugitive"),
          (eq, ":troop_id", "trp_fugitive"), #SB : can't sell quest troops
          (assign, reg0, 0),
        (else_try),
          (check_quest_active, "qst_hunt_down_fugitive"),
          (this_or_next|eq, ":troop_id", "trp_spy"),
          (eq, ":troop_id", "trp_spy_partner"),
          (assign, reg0, 0),
        (else_try),
          (assign, reg0, 1),
        (try_end),
      (try_end),

      #sell women only
      # (try_begin),
          # (eq, "$g_talk_troop", "trp_brothel_madam"),
          # (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_id", 65),
          # (assign, ":is_female", reg65),
          # (neq, ":is_female", 1),
          # (assign, reg0, 0),
      # (try_end),

      (set_trigger_result, reg0),
  ]),

  # script_game_get_morale_of_troops_from_faction
  # This script is called from the game engine when player party inspects another party.
  # INPUT:
  # param1: Party-id
  ("game_event_detect_party",
    [
        (store_script_param_1, ":party_id"),
        (try_begin),
          (party_slot_eq, ":party_id", slot_party_type, spt_kingdom_hero_party),
          (party_stack_get_troop_id, ":leader", ":party_id", 0),
          ##diplomacy start+ support for promoted kingdom ladies
          (is_between, ":leader", heroes_begin, heroes_end),
          (this_or_next|troop_slot_eq, ":leader", slot_troop_occupation, slto_kingdom_hero),
          ##diplomacy end+
          (is_between, ":leader", active_npcs_begin, active_npcs_end),
          (call_script, "script_update_troop_location_notes", ":leader", 0),
        (else_try),
          (is_between, ":party_id", walled_centers_begin, walled_centers_end),
          (party_get_num_attached_parties, ":num_attached_parties",  ":party_id"),
          (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
            (party_get_attached_party_with_rank, ":attached_party", ":party_id", ":attached_party_rank"),
            (party_stack_get_troop_id, ":leader", ":attached_party", 0),
			##diplomacy start+ support for promoted kingdom ladies
			(is_between, ":leader", heroes_begin, heroes_end),
			(this_or_next|troop_slot_eq, ":leader", slot_troop_occupation, slto_kingdom_hero),
			##diplomacy end+
            (is_between, ":leader", active_npcs_begin, active_npcs_end),
            (call_script, "script_update_troop_location_notes", ":leader", 0),
          (try_end),
        (try_end),
  ]),

  #script_game_event_undetect_party:
  # This script is called from the game engine when player party inspects another party.
  # INPUT:
  # param1: Party-id
  ("game_event_undetect_party",
    [
        (store_script_param_1, ":party_id"),
        (try_begin),
          (party_slot_eq, ":party_id", slot_party_type, spt_kingdom_hero_party),
          (party_stack_get_troop_id, ":leader", ":party_id", 0),
          ##diplomacy start+ support for promoted kingdom ladies
          (is_between, ":leader", heroes_begin, heroes_end),
          (this_or_next|troop_slot_eq, ":leader", slot_troop_occupation, slto_kingdom_hero),
          ##diplomacy end+
          (is_between, ":leader", active_npcs_begin, active_npcs_end),
          (call_script, "script_update_troop_location_notes", ":leader", 0),
        (try_end),
  ]),

  #script_game_get_statistics_line:
  # This script is called from the game engine when statistics page is opened.
  # INPUT:
  # param1: line_no
  ("game_get_statistics_line",
    [
      (store_script_param_1, ":line_no"),
      (try_begin),
        (eq, ":line_no", 0),
        (get_player_agent_kill_count, reg1),
        (str_store_string, s1, "str_number_of_troops_killed_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 1),
        (get_player_agent_kill_count, reg1, 1),
        (str_store_string, s1, "str_number_of_troops_wounded_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 2),
        (get_player_agent_own_troop_kill_count, reg1),
        (str_store_string, s1, "str_number_of_own_troops_killed_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 3),
        (get_player_agent_own_troop_kill_count, reg1, 1),
        (str_store_string, s1, "str_number_of_own_troops_wounded_reg1"),
        (set_result_string, s1),
      (try_end),
  ]),

 #script_game_get_date_text:
  # This script is called from the game engine when the date needs to be displayed.
  # INPUT: arg1 = number of days passed since the beginning of the game
  # OUTPUT: result string = date
  ("game_get_date_text",
    [
		(store_script_param_1, ":version"),
      (store_script_param_2, ":num_hours"),
      (store_div, ":num_days", ":num_hours", 24),
      (store_add, ":cur_day", ":num_days", 23),
      (assign, ":cur_month", 3),
      (assign, ":cur_year", 1257),
      (assign, ":try_range", 99999),
      (try_for_range, ":unused", 0, ":try_range"),
        (try_begin),
          (this_or_next|eq, ":cur_month", 1),
          (this_or_next|eq, ":cur_month", 3),
          (this_or_next|eq, ":cur_month", 5),
          (this_or_next|eq, ":cur_month", 7),
          (this_or_next|eq, ":cur_month", 8),
          (this_or_next|eq, ":cur_month", 10),
          (eq, ":cur_month", 12),
          (assign, ":month_day_limit", 31),
        (else_try),
          (this_or_next|eq, ":cur_month", 4),
          (this_or_next|eq, ":cur_month", 6),
          (this_or_next|eq, ":cur_month", 9),
          (eq, ":cur_month", 11),
          (assign, ":month_day_limit", 30),
        (else_try),
          (try_begin),
            (store_div, ":cur_year_div_4", ":cur_year", 4),
            (val_mul, ":cur_year_div_4", 4),
            (eq, ":cur_year_div_4", ":cur_year"),
            (assign, ":month_day_limit", 29),
          (else_try),
            (assign, ":month_day_limit", 28),
          (try_end),
        (try_end),
        (try_begin),
          (gt, ":cur_day", ":month_day_limit"),
          (val_sub, ":cur_day", ":month_day_limit"),
          (val_add, ":cur_month", 1),
          (try_begin),
            (gt, ":cur_month", 12),
            (val_sub, ":cur_month", 12),
            (val_add, ":cur_year", 1),
          (try_end),
        (else_try),
          (assign, ":try_range", 0),
        (try_end),
      (try_end),
      (assign, reg1, ":cur_day"),
      (assign, reg2, ":cur_year"),
      (store_time_of_day, reg3), ## CC
	  (try_begin),
		(this_or_next|eq, ":version", 1),
		(try_begin),
			(eq, ":cur_month", 1),
			(str_store_string, s1, "str_january_reg1_reg2_v2"),
		  (else_try),
			(eq, ":cur_month", 2),
			(str_store_string, s1, "str_february_reg1_reg2_v2"),
		  (else_try),
			(eq, ":cur_month", 3),
			(str_store_string, s1, "str_march_reg1_reg2_v2"),
		  (else_try),
			(eq, ":cur_month", 4),
			(str_store_string, s1, "str_april_reg1_reg2_v2"),
		  (else_try),
			(eq, ":cur_month", 5),
			(str_store_string, s1, "str_may_reg1_reg2_v2"),
		  (else_try),
			(eq, ":cur_month", 6),
			(str_store_string, s1, "str_june_reg1_reg2_v2"),
		  (else_try),
			(eq, ":cur_month", 7),
			(str_store_string, s1, "str_july_reg1_reg2_v2"),
		  (else_try),
			(eq, ":cur_month", 8),
			(str_store_string, s1, "str_august_reg1_reg2_v2"),
		  (else_try),
			(eq, ":cur_month", 9),
			(str_store_string, s1, "str_september_reg1_reg2_v2"),
		  (else_try),
			(eq, ":cur_month", 10),
			(str_store_string, s1, "str_october_reg1_reg2_v2"),
		  (else_try),
			(eq, ":cur_month", 11),
			(str_store_string, s1, "str_november_reg1_reg2_v2"),
		  (else_try),
			(eq, ":cur_month", 12),
			(str_store_string, s1, "str_december_reg1_reg2_v2"),
		  (try_end),
		(else_try),
		  (try_begin),
			(eq, ":cur_month", 1),
			(str_store_string, s1, "str_january_reg1_reg2"),
		  (else_try),
			(eq, ":cur_month", 2),
			(str_store_string, s1, "str_february_reg1_reg2"),
		  (else_try),
			(eq, ":cur_month", 3),
			(str_store_string, s1, "str_march_reg1_reg2"),
		  (else_try),
			(eq, ":cur_month", 4),
			(str_store_string, s1, "str_april_reg1_reg2"),
		  (else_try),
			(eq, ":cur_month", 5),
			(str_store_string, s1, "str_may_reg1_reg2"),
		  (else_try),
			(eq, ":cur_month", 6),
			(str_store_string, s1, "str_june_reg1_reg2"),
		  (else_try),
			(eq, ":cur_month", 7),
			(str_store_string, s1, "str_july_reg1_reg2"),
		  (else_try),
			(eq, ":cur_month", 8),
			(str_store_string, s1, "str_august_reg1_reg2"),
		  (else_try),
			(eq, ":cur_month", 9),
			(str_store_string, s1, "str_september_reg1_reg2"),
		  (else_try),
			(eq, ":cur_month", 10),
			(str_store_string, s1, "str_october_reg1_reg2"),
		  (else_try),
			(eq, ":cur_month", 11),
			(str_store_string, s1, "str_november_reg1_reg2"),
		  (else_try),
			(eq, ":cur_month", 12),
			(str_store_string, s1, "str_december_reg1_reg2"),
		  (try_end),
		(try_end),
      (set_result_string, s1),
  ]),

  #script_game_get_money_text:
  # This script is called from the game engine when an amount of money needs to be displayed.
  # INPUT: arg1 = amount in units
  # OUTPUT: result string = money in text
  ("game_get_money_text",
    [
      (store_script_param_1, ":amount"),
      (try_begin),
        (eq, ":amount", 1),
        (str_store_string, s1, "str_1_denar"),
      (else_try),
        (assign, reg1, ":amount"),
        (str_store_string, s1, "str_reg1_denars"),
      (try_end),
      (set_result_string, s1),
  ]),

  #script_game_get_party_companion_limit:
  # This script is called from the game engine when the player name is changed.
  # INPUT: none
  # OUTPUT: none
  ("game_reset_player_party_name",
    [(str_store_troop_name, s5, "trp_player"),
     (party_set_name, "p_main_party", s5),
     ]),

  #script_game_get_troop_note
  # This script is called from the game engine when the notes of a troop is needed.
  # INPUT: arg1 = troop_no, arg2 = note_index
  # OUTPUT: s0 = note
  ("game_get_troop_note",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":note_index"),
      (set_trigger_result, 0),

      (str_store_troop_name, s54, ":troop_no"),
      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (this_or_next|eq, "$player_has_homage", 1),
        (eq, "$players_kingdom", "fac_player_supporters_faction"),
        (assign, ":troop_faction", "$players_kingdom"),
      (else_try),
        (store_troop_faction, ":troop_faction", ":troop_no"),
      (try_end),
      (str_clear, s49),

	  #Family notes
      (try_begin),
	    ##diplomacy start+ add support for displaying relations with kings and claimants
		#(this_or_next|is_between, ":troop_no", lords_begin, kingdom_ladies_end),
        #(eq, ":troop_no", "trp_player"),
        #(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),

		(this_or_next|eq, ":troop_no", "trp_player"),
		(this_or_next|is_between, ":troop_no", lords_begin, kingdom_ladies_end),#includes pretenders
			(is_between, ":troop_no", kings_begin, kings_end),

		##The following would only show relations for kings and claimants if they are married.
        #(this_or_next|troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
		#	(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),
		#(this_or_next|troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
		#	(neg|is_between, ":troop_no", kings_begin, kings_end),

		##diplomacy end+
        (assign, ":num_relations", 0),

        (try_begin),
          (call_script, "script_troop_get_family_relation_to_troop", "trp_player", ":troop_no"),
          (gt, reg0, 0),
          (val_add, ":num_relations", 1),
        (try_end),
		##diplomacy start+
        #(try_for_range, ":aristocrat", lords_begin, kingdom_ladies_end),
		#Display relations with kings and claimants
		(try_for_range, ":aristocrat", heroes_begin, heroes_end),
		  (this_or_next|is_between, ":aristocrat", lords_begin, kingdom_ladies_end),#includes pretenders
			  (is_between, ":aristocrat", kings_begin, kings_end),
		##diplomacy end+
          (call_script, "script_troop_get_family_relation_to_troop", ":aristocrat", ":troop_no"),
          (gt, reg0, 0),
          (val_add, ":num_relations", 1),
        (try_end),
        (try_begin),
          (gt, ":num_relations", 0),
          (try_begin),
            (eq, ":troop_no", "trp_player"),
            (str_store_string, s49, "str__family_"),
          (else_try),
            (troop_get_slot, reg1, ":troop_no", slot_troop_age),
            (str_store_string, s49, "str__age_reg1_family_"),
          (try_end),
          (try_begin),
            (call_script, "script_troop_get_family_relation_to_troop", "trp_player", ":troop_no"),
            (gt, reg0, 0),
            (str_store_troop_name_link, s12, "trp_player"),
            (val_sub, ":num_relations", 1),
            (try_begin),
              (eq, ":num_relations", 0),
              (str_store_string, s49, "str_s49_s12_s11_end"),
            (else_try),
              (str_store_string, s49, "str_s49_s12_s11"),
            (try_end),
          (try_end),
		  ##diplomacy start+
          #(try_for_range, ":aristocrat", lords_begin, kingdom_ladies_end),
		  #Display relations with kings and claimants
		  (try_for_range, ":aristocrat", heroes_begin, heroes_end),
		    (this_or_next|is_between, ":aristocrat", lords_begin, kingdom_ladies_end),#includes pretenders
			   (is_between, ":aristocrat", kings_begin, kings_end),
		  ##diplomacy end+
            (call_script, "script_troop_get_family_relation_to_troop", ":aristocrat", ":troop_no"),
            (gt, reg0, 0),
            (try_begin),
              (neg|is_between, ":aristocrat", kingdom_ladies_begin, kingdom_ladies_end),
              (eq, "$cheat_mode", 1),
              (str_store_troop_name_link, s12, ":aristocrat"),
              (call_script, "script_troop_get_relation_with_troop", ":aristocrat", ":troop_no"),
              (str_store_string, s49, "str_s49_s12_s11_rel_reg0"),
            (else_try),
              (str_store_troop_name_link, s12, ":aristocrat"),
              (val_sub, ":num_relations", 1),
              (try_begin),
                (eq, ":num_relations", 0),
                (str_store_string, s49, "str_s49_s12_s11_end"),
              (else_try),
                (str_store_string, s49, "str_s49_s12_s11"),
              (try_end),
            (try_end),
          (try_end),
        (try_end),
      (try_end),

      (try_begin),
        (neq, ":troop_no", "trp_player"),
        (neg|is_between, ":troop_faction", kingdoms_begin, kingdoms_end),
        (neg|is_between, ":troop_no", companions_begin, companions_end),
        (neg|is_between, ":troop_no", pretenders_begin, pretenders_end),

        (try_begin),
          (eq, ":note_index", 0),
          (str_store_string, s0, "str_s54_has_left_the_realm"),
          ##diplomacy start+
          #Check for "deceased" instead
          (try_begin),
             (troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_dead),
             (str_store_string, s0, "str_s54_is_deceased"),
          (try_end),
          ##diplomacy end+
          (set_trigger_result, 1),
        (else_try),
          (str_clear, s0),
          (this_or_next|eq, ":note_index", 1),
          (eq, ":note_index", 2),
          (set_trigger_result, 1),
        (try_end),

      (else_try),
        (is_between, ":troop_no", companions_begin, companions_end),
        (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (eq, ":note_index", 0),
        (set_trigger_result, 1),
        (str_clear, s0),
        (assign, ":companion", ":troop_no"),
        (str_store_troop_name, s4, ":companion"),
        (try_begin),
			# (troop_get_slot, ":days_left", ":companion", slot_troop_days_on_mission),

			(this_or_next|main_party_has_troop, ":companion"),
			(this_or_next|troop_slot_ge, ":companion", slot_troop_current_mission, 1),
				(eq, "$g_player_minister", ":companion"),
            #SB : replace the call
            (call_script, "script_companion_get_mission_string", ":companion"),

			# (try_begin),
				# (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_kingsupport),
				# (str_store_string, s8, "str_gathering_support"),
				# (try_begin),
					# (eq, ":days_left", 1),
					# (str_store_string, s5, "str_expected_back_imminently"),
				# (else_try),
					# (assign, reg3, ":days_left"),
					# (str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
				# (try_end),
			# (else_try),
				# (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_gather_intel),
				# (troop_get_slot, ":town_with_contacts", ":companion", slot_troop_town_with_contacts),
				# (str_store_party_name, s11, ":town_with_contacts"),

				# (str_store_string, s8, "str_gathering_intelligence"),
				# (try_begin),
					# (eq, ":days_left", 1),
					# (str_store_string, s5, "str_expected_back_imminently"),
				# (else_try),
					# (assign, reg3, ":days_left"),
					# (str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
				# (try_end),
			# (else_try),

				# (troop_slot_ge, ":companion", slot_troop_current_mission, npc_mission_peace_request),
				# (neg|troop_slot_ge, ":companion", slot_troop_current_mission, npc_mission_rejoin_when_possible), #SB : replace hard constant 8

				# (troop_get_slot, ":faction", ":companion", slot_troop_mission_object),
				# (str_store_faction_name, s9, ":faction"),
				# (str_store_string, s8, "str_diplomatic_embassy_to_s9"),
				# (try_begin),
					# (eq, ":days_left", 1),
					# (str_store_string, s5, "str_expected_back_imminently"),
				# (else_try),
					# (assign, reg3, ":days_left"),
					# (str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
				# (try_end),
			# (else_try),
				# (eq, ":companion", "$g_player_minister"),
				# (str_store_string, s8, "str_serving_as_minister"),
				# (str_store_party_name, s9, "$g_player_court"),
				# (is_between, "$g_player_court", centers_begin, centers_end),
				# (str_store_string, s5, "str_in_your_court_at_s9"),
			# (else_try),
				# (eq, ":companion", "$g_player_minister"),
				# (str_store_string, s8, "str_serving_as_minister"),
				# (str_store_string, s5, "str_awaiting_the_capture_of_a_fortress_which_can_serve_as_your_court"),
			# (else_try),
				# (main_party_has_troop, ":companion"),
				# (str_store_string, s8, "str_under_arms"),
				# (str_store_string, s5, "str_in_your_party"),
			# (try_end),

			# (str_store_string, s0, "str_s4_s8_s5"),
		##diplomacy start+
		#Check for explicit "exiled" and "dead" settings
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_dead),
			(str_store_string, s0, "str_s54_is_deceased"),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_exile),
			(str_store_string, s0, "str_s54_has_left_the_realm"),
		##diplomacy end+
		(else_try),
			(str_store_string, s0, "str_whereabouts_unknown"),
		(try_end),


      (else_try),
        (is_between, ":troop_no", pretenders_begin, pretenders_end),
        (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (neq, ":troop_no", "$supported_pretender"),


        (troop_get_slot, ":orig_faction", ":troop_no", slot_troop_original_faction),
        (try_begin),
          (faction_slot_eq, ":orig_faction", slot_faction_state, sfs_active),
          (faction_slot_eq, ":orig_faction", slot_faction_has_rebellion_chance, 1),
          (try_begin),
            (eq, ":note_index", 0),
            (str_store_faction_name_link, s56, ":orig_faction"),
            ##diplomacy start+ xxx Removed third argument (was it doing anything?)
            #(str_store_string, s0, "@{s54} is a claimant to the throne of {s56}.", 0),
            (str_store_string, s0, "@{s54} is a claimant to the throne of {s56}."),
            ##diplomacy end+
            (set_trigger_result, 1),
          (try_end),
        (else_try),
          (try_begin),
            (str_clear, s0),
            (this_or_next|eq, ":note_index", 0),
            (this_or_next|eq, ":note_index", 1),
            (eq, ":note_index", 2),
            (set_trigger_result, 1),
          (try_end),
        (try_end),

      (else_try),
        (try_begin),
          (eq, ":note_index", 0),
          (faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),
          (str_store_troop_name_link, s55, ":faction_leader"),
          (str_store_faction_name_link, s56, ":troop_faction"),
          (assign, ":troop_is_player_faction", 0),
          (assign, ":troop_is_faction_leader", 0),
          (try_begin),
            (eq, ":troop_faction", "fac_player_faction"),
            (assign, ":troop_is_player_faction", 1),
          (else_try),
            (eq, ":faction_leader", ":troop_no"),
            (assign, ":troop_is_faction_leader", 1),
          (try_end),
          #SB: add marshal check
          (try_begin),
            (faction_slot_eq, ":troop_faction", slot_faction_marshall, ":troop_no"),
            (assign, ":troop_is_marshal", 1),
          (else_try),
            (assign, ":troop_is_marshal", 0),
          (try_end),
          (assign, ":num_centers", 0),
          (str_store_string, s58, "@nowhere"),
          (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
            (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
            (try_begin),
              (eq, ":num_centers", 0),
              (str_store_party_name_link, s58, ":cur_center"),
            (else_try),
              (eq, ":num_centers", 1),
              (str_store_party_name_link, s57, ":cur_center"),
              (str_store_string, s58, "@{s57} and {s58}"),
            (else_try),
              (str_store_party_name_link, s57, ":cur_center"),
              (str_store_string, s58, "@{!}{s57}, {s58}"),
            (try_end),
            (val_add, ":num_centers", 1),
          (try_end),
          ##diplomacy start+ use script for gender
          #(troop_get_type, reg3, ":troop_no"),
          (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 3),
          #(assign, reg3, reg0),
          ##diplomacy end+


          (str_clear, s59),
          (try_begin),
            (call_script, "script_troop_get_player_relation", ":troop_no"),
            (assign, ":relation", reg0),
            (store_add, ":normalized_relation", ":relation", 100),
            (val_add, ":normalized_relation", 5),
            (store_div, ":str_offset", ":normalized_relation", 10),
            (val_clamp, ":str_offset", 0, 20),
            (store_add, ":str_id", "str_relation_mnus_100_ns",  ":str_offset"),
            (neq, ":str_id", "str_relation_plus_0_ns"),
            (str_store_string, s60, "@{reg3?She:He}"),
            (str_store_string, s59, ":str_id"),
            (str_store_string, s59, "@{!}^{s59}"),
          (try_end),
          #lord recruitment changes begin
          #This sends a bunch of political information to s47.

          #refresh registers
          (assign, reg9, ":num_centers"),
          ##diplomacy start+ use script for gender
          #(troop_get_type, reg3, ":troop_no"),
          (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 3),
          ##diplomacy end+

          #SB : rearrange registers a bit
          (assign, reg4, ":troop_is_faction_leader"),
          (assign, reg5, ":troop_is_marshal"),
          (assign, reg6, ":troop_is_player_faction"),

          #SB : TODO, add rounding based on personal relation/time last met?
          (troop_get_slot, reg15, ":troop_no", slot_troop_renown),
          (troop_get_slot, reg16, ":troop_no", slot_troop_controversy),
          #SB : actually use this wealth in string
          (troop_get_slot, reg17, ":troop_no", slot_troop_wealth), #DEBUGS
          (str_store_string, s61, "@unknown"),
          (try_begin),
            (is_between, ":troop_no", active_npcs_begin, active_npcs_end),
            (this_or_next|neq, "$cheat_mode", 0),
            (troop_slot_eq, ":troop_no", slot_troop_met, 1),
            (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
            (store_add, ":rep_string", ":reputation", "str_personality_archetypes"),
            (str_store_string, s61, ":rep_string"),
          (try_end),
          ##diplomacy start+ xxx remove third argument (was it doing anything?)
          #(str_store_string, s0, "str_lord_info_string", 0),
          (str_store_string, s0, "str_lord_info_string"),
          ##diplomacy end+
          #lord recruitment changes end
          (add_troop_note_tableau_mesh, ":troop_no", "tableau_troop_note_mesh"),
          (set_trigger_result, 1),
        (try_end),
      (try_end),
     ]),

  #script_game_get_center_note
  # This script is called from the game engine when the notes of a quest is needed.
  # INPUT: arg1 = quest_no, arg2 = note_index
  # OUTPUT: s0 = note
  ("game_get_quest_note",
    [
##      (store_script_param_1, ":quest_no"),
##      (store_script_param_2, ":note_index"),
      (set_trigger_result, 0), # set it to 1 if this script is wanted to be used rather than static notes
      #SB: TODO set up progress for pretender quests and other long-winding series
     ]),

  #script_game_get_info_page_note
  # This script is called from the game engine when the notes of a info_page is needed.
  # INPUT: arg1 = info_page_no, arg2 = note_index
  # OUTPUT: s0 = note
  ("game_get_info_page_note",
    [
##      (store_script_param_1, ":info_page_no"),
##      (store_script_param_2, ":note_index"),
      (set_trigger_result, 0), # set it to 1 if this script is wanted to be used rather than static notes
      #SB: TODO use actual settings for camera, ai_changes etc
     ]),

  #script_game_get_scene_name
  # This script is called from the game engine when a name for the scene is needed.
  # INPUT: arg1 = scene_no
  # OUTPUT: s0 = name
  ("game_get_scene_name",
    [
      (store_script_param, ":scene_no", 1),
      (try_begin),
        (is_between, ":scene_no", multiplayer_scenes_begin, multiplayer_scenes_end),
        (store_sub, ":string_id", ":scene_no", multiplayer_scenes_begin),
        (val_add, ":string_id", multiplayer_scene_names_begin),
        (str_store_string, s0, ":string_id"),
      (try_end),
     ]),

  #script_game_get_mission_template_name
  # This script is called from the game engine when a name for the mission template is needed.
  # INPUT: arg1 = mission_template_no
  # OUTPUT: s0 = name
  ("game_get_mission_template_name",
    [
      (store_script_param, ":mission_template_no", 1),
      (call_script, "script_multiplayer_get_mission_template_game_type", ":mission_template_no"),
      (assign, ":game_type", reg0),
      (try_begin),
        (is_between, ":game_type", 0, multiplayer_num_game_types),
        (store_add, ":string_id", ":game_type", multiplayer_game_type_names_begin),
        (str_store_string, s0, ":string_id"),
      (try_end),
     ]),

  #script_add_kill_death_counts
("initialize_aristocracy",
	[
	  #LORD OCCUPATIONS, BLOOD RELATIONSHIPS, RENOWN AND REPUTATIONS

	  #King ages
	  (try_for_range, ":cur_troop", kings_begin, kings_end),
		(troop_set_slot, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
		(store_random_in_range, ":age", 50, 60),
		(troop_set_slot, ":cur_troop", slot_troop_age, ":age"),
		##diplomacy start+
		#(eq, ":cur_troop", "trp_kingdom_5_lord"),#<-- There was no reason for this to be in the loop, so moved it out.
		#(troop_set_slot, ":cur_troop", slot_troop_age, 47),
	  (try_end),
	  (troop_set_slot, "trp_kingdom_5_lord", slot_troop_age, 47),#<-- Moved from above
	  ##diplomacy end+

	  #The first thing - family structure
	  #lords 1 to 8 are patriarchs with one live-at-home son and one daughter. They come from one of six possible ancestors, thus making it likely that there will be two sets of siblings
	  #lords 9 to 12 are unmarried landowners with sisters
	  #lords 13 to 20 are sons who still live in their fathers' houses
	  #For the sake of simplicity, we can assume that all male aristocrats in prior generations either married commoners or procured their brides from the Old Country, thus discounting intermarriage

	  (try_for_range, ":cur_troop", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_set_slot, ":cur_troop", slot_troop_occupation, slto_kingdom_lady),
	  (try_end),

	  (assign, ":cur_lady", "trp_kingdom_1_lady_1"),

	  (try_for_range, ":cur_troop", lords_begin, lords_end),
		(troop_set_slot, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),

		(store_random_in_range, ":father_age_at_birth", 23, 26),
#		(store_random_in_range, ":mother_age_at_birth", 19, 22),

		(try_begin),
			(is_between, ":cur_troop", "trp_knight_1_1", "trp_knight_2_1"),
			(store_sub, ":npc_seed", ":cur_troop", "trp_knight_1_1"),
			(assign, ":ancestor_seed", 1),

		(else_try),
			(is_between, ":cur_troop", "trp_knight_2_1", "trp_knight_3_1"),
			(store_sub, ":npc_seed", ":cur_troop", "trp_knight_2_1"),
			(assign, ":ancestor_seed", 7),

		(else_try),
			(is_between, ":cur_troop", "trp_knight_3_1", "trp_knight_4_1"),
			(store_sub, ":npc_seed", ":cur_troop", "trp_knight_3_1"),
			(assign, ":ancestor_seed", 13),

		(else_try),
			(is_between, ":cur_troop", "trp_knight_4_1", "trp_knight_5_1"),
			(store_sub, ":npc_seed", ":cur_troop", "trp_knight_4_1"),
			(assign, ":ancestor_seed", 19),

		(else_try),
			(is_between, ":cur_troop", "trp_knight_5_1", "trp_knight_6_1"),
			(store_sub, ":npc_seed", ":cur_troop", "trp_knight_5_1"),
			(assign, ":ancestor_seed", 25),

		(else_try),
			(is_between, ":cur_troop", "trp_knight_6_1", "trp_kingdom_1_pretender"),
			(store_sub, ":npc_seed", ":cur_troop", "trp_knight_6_1"),
			(assign, ":ancestor_seed", 31),

		(try_end),


		(try_begin),
			(lt, ":npc_seed", 8), #NPC seed is the order in the faction
			##diplomacy start+ do not overwrite reputation if it was already set explicitly
			(troop_get_slot, ":reputation", ":cur_troop", slot_lord_reputation_type),
			(try_begin),
				(lt, ":reputation", 1),
				#Original behavior:
				(assign, ":reputation", ":npc_seed"),
			(try_end),
			##diplomacy end+
			(store_random_in_range, ":age", 45, 64),

			##diplomacy start+ only set father if not already set
			(try_begin),#<- dplmc+ added
				(troop_slot_eq, ":cur_troop", slot_troop_father, -1),#<- dplmc+ added
				(store_random_in_range, ":father", 0, 6), #six possible fathers
				(val_add, ":father", ":ancestor_seed"),
				(troop_set_slot, ":cur_troop", slot_troop_father, ":father"),
			(try_end),#<- dplmc+ added
			##diplomacy end+

			#wife
			##diplomacy start+ do not rebind an already-set wife
			(try_begin),
				(troop_slot_eq, ":cur_troop", slot_troop_spouse, -1),
				#There may be a better solution, but to avoid oddities disable automatic spouses if there is a gender mismatch.
				#Mods that add additional races may want to tweak this (for example if some races shouldn't intermarry).
				(call_script, "script_dplmc_store_is_female_troop_1_troop_2", ":cur_troop", ":cur_lady"),
				#Types are stored to reg0 and reg1.
				(neq, reg0, reg1),#lord and lady aren't both female or both non-female
				(val_mul, reg0, reg1),
				(eq, reg0, 0),#at least one of lord or lady is non-female
			##diplomacy end+
				(troop_set_slot, ":cur_troop", slot_troop_spouse, ":cur_lady"),
				(troop_set_slot, ":cur_lady", slot_troop_spouse, ":cur_troop"),
                (store_faction_of_troop, ":cur_troop_faction", ":cur_troop"),
                (call_script, "script_troop_set_title_according_to_faction", ":cur_lady", ":cur_troop_faction"),
				(store_random_in_range, ":wife_reputation", 20, 26),
				(try_begin),
					(eq, ":wife_reputation", 20),
					(assign, ":wife_reputation", lrep_conventional),
				(try_end),
				(troop_set_slot, ":cur_lady", slot_lord_reputation_type, ":wife_reputation"),


				(call_script, "script_init_troop_age", ":cur_lady", 49),
				(call_script, "script_add_lady_items", ":cur_lady"),

				(val_add, ":cur_lady", 1),
			##diplomacy start+
			(try_end),
			##diplomacy end+

			#daughter
			##diplomacy start+
			(try_begin),
			##diplomacy end+
				(troop_set_slot, ":cur_lady", slot_troop_father, ":cur_troop"),
				(store_sub, ":mother", ":cur_lady", 1),
				(call_script, "script_init_troop_age", ":cur_lady", 19),
			##diplomacy start+
				#fix native bug (daughters are their own mothers)
        # Note: this bug was fixed in native version 1.158
				#(troop_set_slot, ":cur_lady", slot_troop_mother, ":cur_lady"),
				(troop_set_slot, ":cur_lady", slot_troop_mother, ":mother"),
				(try_begin),
					#swap father and mother slots if the lord was female (do nothing if both were female)
					(call_script, "script_dplmc_store_is_female_troop_1_troop_2", ":cur_troop", ":mother"),
					(neq, reg0, 0),#:cur_troop is female
					(eq, reg1, 0),#:mother is not female
					(troop_set_slot, ":cur_lady", slot_troop_mother, ":cur_troop"),
					(troop_set_slot, ":cur_lady", slot_troop_father, ":mother"),
				(try_end),
			##diplomacy end+
				(store_random_in_range, ":lady_reputation", lrep_conventional, 34), #33% chance of father-derived
				(try_begin),
					(le, ":lady_reputation", 25),
					(troop_set_slot, ":cur_lady", slot_lord_reputation_type, ":lady_reputation"),
				(else_try),
					(eq, ":lady_reputation", 26),
					(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_conventional),
				(else_try),
					(eq, ":lady_reputation", 27),
					(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_moralist),
				(else_try),
					(assign, ":guardian_reputation", ":reputation"),
					(try_begin),
						(this_or_next|eq, ":guardian_reputation", lrep_martial),
							(eq, ":guardian_reputation", 0),
						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_conventional),
					(else_try),
						(eq, ":guardian_reputation", lrep_quarrelsome),
						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_otherworldly),
					(else_try),
						(eq, ":guardian_reputation", lrep_selfrighteous),
						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_ambitious),
					(else_try),
						(eq, ":guardian_reputation", lrep_cunning),
						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_adventurous),
					(else_try),
						(eq, ":guardian_reputation", lrep_goodnatured),
						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_adventurous),
					(else_try),
						(eq, ":guardian_reputation", lrep_debauched),
						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_ambitious),
					(else_try),
						(eq, ":guardian_reputation", lrep_upstanding),
						(troop_set_slot, ":cur_lady", slot_lord_reputation_type, lrep_moralist),
					(try_end),
				(try_end),

				(call_script, "script_add_lady_items", ":cur_lady"),
				(val_add, ":cur_lady", 1),
			##diplomacy start+
			(try_end),
			##diplomacy end+
			#high renown

		(else_try),	#Older unmarried lords
			(is_between, ":npc_seed", 8, 12),

			(store_random_in_range, ":age", 25, 36),
			##diplomacy start+ do not overwrite reputation if it was already set explicitly
			(troop_get_slot, ":reputation", ":cur_troop", slot_lord_reputation_type),
			(try_begin),
				(lt, ":reputation", 1),
				#Original behavior:
				(store_random_in_range, ":reputation", 0, 8),
			(try_end),
			##diplomacy end+

			(store_random_in_range, ":sister_reputation", 20, 26),
			(try_begin),
				(eq, ":sister_reputation", 20),
				(assign, ":sister_reputation", lrep_conventional),
			(try_end),
			(troop_set_slot, ":cur_lady", slot_lord_reputation_type, ":sister_reputation"),

			(troop_set_slot, ":cur_lady", slot_troop_guardian, ":cur_troop"),
			##diplomacy start+
			#Initialize parents
			(try_begin),
				(troop_slot_eq, ":cur_troop", slot_troop_father, -1),
				(store_mul, ":new_index", ":cur_troop", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),#defined in module_constants.py
				(val_add, ":new_index", DPLMC_VIRTUAL_RELATIVE_FATHER_OFFSET),#defined in module_constants.py
				(troop_set_slot, ":cur_troop", slot_troop_father, ":new_index"),
				(troop_slot_eq, ":cur_lady", slot_troop_father, -1),
				(troop_set_slot, ":cur_lady", slot_troop_father, ":new_index"),
			(try_end),
			(try_begin),
				(troop_slot_eq, ":cur_troop", slot_troop_mother, -1),
				(store_mul, ":new_index", ":cur_troop", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),#defined in module_constants.py
				(val_add, ":new_index", DPLMC_VIRTUAL_RELATIVE_MOTHER_OFFSET),#defined in module_constants.py
				(troop_set_slot, ":cur_troop", slot_troop_mother, ":new_index"),
				(troop_slot_eq, ":cur_lady", slot_troop_mother, -1),
				(troop_set_slot, ":cur_lady", slot_troop_mother, ":new_index"),
			(try_end),
			##diplomacy end+

			(call_script, "script_init_troop_age", ":cur_lady", 21),
			(call_script, "script_add_lady_items", ":cur_lady"),

			(val_add, ":cur_lady", 1),

		(else_try),	#Younger unmarried lords
			#age is father's minus 20 to 25
			(store_sub, ":father", ":cur_troop", 12),
			##diplomacy start+
			#Some submods don't pay attention to this aspect of the troop list, and
			#so initialization produces absurd or impossible results.  Prevent such
			#things from appearing in the game.
			(try_begin),
				#"father" can be father or mother
				#(troop_get_type, ":parent_type", ":father"),
				(try_begin),
					#(eq, ":parent_type", tf_female),
					(call_script, "script_cf_dplmc_troop_is_female", ":father"),
					(assign, ":parent_slot", slot_troop_mother),
					(assign, ":other_parent_slot", slot_troop_father),
				(else_try),
					(assign, ":parent_slot", slot_troop_father),
					(assign, ":other_parent_slot", slot_troop_mother),
				(try_end),

				(troop_slot_eq, ":cur_troop", ":parent_slot", -1),
				(store_add, ":logical_minimum_age", ":father_age_at_birth", 16),
				(troop_slot_ge, ":father", slot_troop_age, ":logical_minimum_age"),
				#Passed test
				(troop_set_slot, ":cur_troop", ":parent_slot", ":father"),
				#Set mother if not already specified
				(try_begin),
					(troop_slot_eq, ":cur_troop", ":other_parent_slot", -1),
					(troop_get_slot, ":mother", ":father", slot_troop_spouse),
					(troop_set_slot, ":cur_troop", ":other_parent_slot", ":mother"),
				(try_end),

				(troop_get_slot, ":father_age", ":father", slot_troop_age),
				(store_sub, ":age", ":father_age", ":father_age_at_birth"),

				(troop_get_slot, ":reputation", ":cur_troop", slot_lord_reputation_type),
				(try_begin),
					#Don't change reputation if it already has been set
					(lt, ":reputation", 1),
					#50% chance of having father's rep
					(store_random_in_range, ":reputation", 0, 16),

					(gt, ":reputation", 7),
					(troop_get_slot, ":reputation", ":father", slot_lord_reputation_type),
				(try_end),
			(else_try),
				#Average age is [45,63] minus [23,25], so [22, 38]
				(store_random_in_range, ":age", 22, 39),
				(troop_get_slot, ":reputation", ":cur_troop", slot_lord_reputation_type),
				#Don't change reputation if it already has been set
				(lt, ":reputation", 1),
				(store_random_in_range, ":reputation", 0, 8),
			(try_end),
			#diplomacy end+
		(try_end),

		(try_begin),
			(eq, ":reputation", 0),
			(assign, ":reputation", 1),
		(try_end),

        (troop_set_slot, ":cur_troop", slot_lord_reputation_type, ":reputation"),

		(call_script, "script_init_troop_age", ":cur_troop", ":age"),
	  (try_end),

	  (try_begin),
	    (eq, "$cheat_mode", 1),
	    (assign, reg3, "$cheat_mode"),
	    (display_message, "@{!}DEBUG -- Assigned lord reputation and relations"),

#	    (display_message, "str_assigned_lord_reputation_and_relations_cheat_mode_reg3"), #This string can be removed
	  (try_end),

	  (try_for_range, ":cur_troop", pretenders_begin, pretenders_end),
		(troop_set_slot, ":cur_troop", slot_troop_occupation, slto_inactive_pretender),
		(store_random_in_range, ":age", 25, 30),
		(troop_set_slot, ":cur_troop", slot_troop_age, ":age"),
		(eq, ":cur_troop", "trp_kingdom_5_pretender"),
		(troop_set_slot, ":cur_troop", slot_troop_age, 45),
	  (try_end),
	]),





	("initialize_item_info",
    [
	  # Setting food bonuses - these have been changed to incentivize using historical rations. Bread is the most cost-efficient
	  #Staples
      (item_set_slot, "itm_bread", slot_item_food_bonus, 8), #brought up from 4
      (item_set_slot, "itm_grain", slot_item_food_bonus, 2), #new - can be boiled as porridge

	  #Fat sources - preserved
      (item_set_slot, "itm_smoked_fish", slot_item_food_bonus, 4),
      (item_set_slot, "itm_dried_meat", slot_item_food_bonus, 5),
      (item_set_slot, "itm_cheese", slot_item_food_bonus, 5),
      (item_set_slot, "itm_sausages", slot_item_food_bonus, 5),
      (item_set_slot, "itm_butter", slot_item_food_bonus, 4), #brought down from 8

	  #Fat sources - perishable
      (item_set_slot, "itm_chicken", slot_item_food_bonus, 8), #brought up from 7
      (item_set_slot, "itm_cattle_meat", slot_item_food_bonus, 7), #brought down from 7
      (item_set_slot, "itm_pork", slot_item_food_bonus, 6), #brought down from 6

	  #Produce
      (item_set_slot, "itm_raw_olives", slot_item_food_bonus, 1),
      (item_set_slot, "itm_cabbages", slot_item_food_bonus, 2),
      (item_set_slot, "itm_raw_grapes", slot_item_food_bonus, 3),
      (item_set_slot, "itm_apples", slot_item_food_bonus, 4), #brought down from 5

	  #Sweet items
      (item_set_slot, "itm_raw_date_fruit", slot_item_food_bonus, 4), #brought down from 8
      (item_set_slot, "itm_honey", slot_item_food_bonus, 6), #brought down from 12

      (item_set_slot, "itm_wine", slot_item_food_bonus, 5),
      (item_set_slot, "itm_ale", slot_item_food_bonus, 4),

	  #Item economic settings
	  (item_set_slot, "itm_grain", slot_item_urban_demand, 20),
      (item_set_slot, "itm_grain", slot_item_rural_demand, 20),
      (item_set_slot, "itm_grain", slot_item_desert_demand, 20),
      (item_set_slot, "itm_grain", slot_item_production_slot, slot_center_acres_grain),
      (item_set_slot, "itm_grain", slot_item_production_string, "str_acres_grain"),
      (item_set_slot, "itm_grain", slot_item_base_price, 30),

      (item_set_slot, "itm_bread", slot_item_urban_demand, 30),
      (item_set_slot, "itm_bread", slot_item_rural_demand, 30),
      (item_set_slot, "itm_bread", slot_item_desert_demand, 30),
      (item_set_slot, "itm_bread", slot_item_production_slot, slot_center_mills),
      (item_set_slot, "itm_bread", slot_item_production_string, "str_mills"),
      (item_set_slot, "itm_bread", slot_item_primary_raw_material, "itm_grain"),
      (item_set_slot, "itm_bread", slot_item_input_number, 6),
      (item_set_slot, "itm_bread", slot_item_output_per_run, 6),
      (item_set_slot, "itm_bread", slot_item_overhead_per_run, 30),
      (item_set_slot, "itm_bread", slot_item_base_price, 50),
      (item_set_slot, "itm_bread", slot_item_enterprise_building_cost, 1500),

	  (item_set_slot, "itm_ale", slot_item_urban_demand, 10),
	  (item_set_slot, "itm_ale", slot_item_rural_demand, 15),
      (item_set_slot, "itm_ale", slot_item_desert_demand, 0),
      (item_set_slot, "itm_ale", slot_item_production_slot, slot_center_breweries),
      (item_set_slot, "itm_ale", slot_item_production_string, "str_breweries"),
      (item_set_slot, "itm_ale", slot_item_base_price, 120),
      (item_set_slot, "itm_ale", slot_item_primary_raw_material, "itm_grain"),
	  (item_set_slot, "itm_ale", slot_item_input_number, 1),
      (item_set_slot, "itm_ale", slot_item_output_per_run, 2),
      (item_set_slot, "itm_ale", slot_item_overhead_per_run, 50),
      (item_set_slot, "itm_ale", slot_item_base_price, 120),
      (item_set_slot, "itm_ale", slot_item_enterprise_building_cost, 2500),

	  (item_set_slot, "itm_wine", slot_item_urban_demand, 15),
	  (item_set_slot, "itm_wine", slot_item_rural_demand, 10),
      (item_set_slot, "itm_wine", slot_item_desert_demand, 25),
      (item_set_slot, "itm_wine", slot_item_production_slot, slot_center_wine_presses),
      (item_set_slot, "itm_wine", slot_item_production_string, "str_presses"),
      (item_set_slot, "itm_wine", slot_item_primary_raw_material, "itm_raw_grapes"),
      (item_set_slot, "itm_wine", slot_item_input_number, 4),
      (item_set_slot, "itm_wine", slot_item_output_per_run, 2),
	  (item_set_slot, "itm_wine", slot_item_overhead_per_run, 60),
      (item_set_slot, "itm_wine", slot_item_base_price, 220),
      (item_set_slot, "itm_wine", slot_item_enterprise_building_cost, 5000),

	  (item_set_slot, "itm_raw_grapes", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_raw_grapes", slot_item_rural_demand, 0),
      (item_set_slot, "itm_raw_grapes", slot_item_desert_demand, 0),
      (item_set_slot, "itm_raw_grapes", slot_item_production_slot, slot_center_acres_vineyard),
      (item_set_slot, "itm_raw_grapes", slot_item_production_string, "str_acres_orchard"),
      (item_set_slot, "itm_raw_grapes", slot_item_is_raw_material_only_for, "itm_wine"),
      (item_set_slot, "itm_raw_grapes", slot_item_base_price, 75),

	  (item_set_slot, "itm_apples", slot_item_urban_demand, 4),
	  (item_set_slot, "itm_apples", slot_item_rural_demand, 4),
	  (item_set_slot, "itm_apples", slot_item_desert_demand, 0),
      (item_set_slot, "itm_apples", slot_item_production_slot, slot_center_acres_vineyard),
      (item_set_slot, "itm_apples", slot_item_production_string, "str_acres_orchard"),
      (item_set_slot, "itm_apples", slot_item_base_price, 44),

      (item_set_slot, "itm_smoked_fish", slot_item_urban_demand, 16),
      (item_set_slot, "itm_smoked_fish", slot_item_rural_demand, 16),
      (item_set_slot, "itm_smoked_fish", slot_item_desert_demand, 16),
      (item_set_slot, "itm_smoked_fish", slot_item_production_slot, slot_center_fishing_fleet),
      (item_set_slot, "itm_smoked_fish", slot_item_production_string, "str_boats"),

      (item_set_slot, "itm_salt", slot_item_urban_demand, 5),
      (item_set_slot, "itm_salt", slot_item_rural_demand, 3),
      (item_set_slot, "itm_salt", slot_item_desert_demand, -1),
      (item_set_slot, "itm_salt", slot_item_production_slot, slot_center_salt_pans),
      (item_set_slot, "itm_salt", slot_item_production_string, "str_pans"),

      (item_set_slot, "itm_dried_meat", slot_item_urban_demand, 20),
      (item_set_slot, "itm_dried_meat", slot_item_rural_demand, 5),
      (item_set_slot, "itm_dried_meat", slot_item_desert_demand, -1),
      (item_set_slot, "itm_dried_meat", slot_item_production_slot, slot_center_head_cattle),
      (item_set_slot, "itm_dried_meat", slot_item_production_string, "str_head_cattle"),

      (item_set_slot, "itm_cattle_meat", slot_item_urban_demand, 12),
      (item_set_slot, "itm_cattle_meat", slot_item_rural_demand, 3),
      (item_set_slot, "itm_cattle_meat", slot_item_desert_demand, -1),
      (item_set_slot, "itm_cattle_meat", slot_item_production_slot, slot_center_head_cattle),
      (item_set_slot, "itm_cattle_meat", slot_item_production_string, "str_head_cattle"),

      (item_set_slot, "itm_cheese", slot_item_urban_demand, 10),
      (item_set_slot, "itm_cheese", slot_item_rural_demand, 10),
      (item_set_slot, "itm_cheese", slot_item_desert_demand, 10),
      (item_set_slot, "itm_cheese", slot_item_production_slot, slot_center_head_cattle),
      (item_set_slot, "itm_cheese", slot_item_production_string, "str_head_cattle"),

      (item_set_slot, "itm_butter", slot_item_urban_demand, 2),
      (item_set_slot, "itm_butter", slot_item_rural_demand, 2),
      (item_set_slot, "itm_butter", slot_item_desert_demand, 2),
      (item_set_slot, "itm_butter", slot_item_production_slot, slot_center_head_cattle),
      (item_set_slot, "itm_butter", slot_item_production_string, "str_head_cattle"),

      (item_set_slot, "itm_leatherwork", slot_item_urban_demand, 10),
      (item_set_slot, "itm_leatherwork", slot_item_rural_demand, 10),
      (item_set_slot, "itm_leatherwork", slot_item_desert_demand, 10),
      (item_set_slot, "itm_leatherwork", slot_item_production_slot, slot_center_tanneries),
      (item_set_slot, "itm_leatherwork", slot_item_production_string, "str_tanneries"),
      (item_set_slot, "itm_leatherwork", slot_item_primary_raw_material, "itm_raw_leather"),
      (item_set_slot, "itm_leatherwork", slot_item_input_number, 3),
      (item_set_slot, "itm_leatherwork", slot_item_output_per_run, 3),
      (item_set_slot, "itm_leatherwork", slot_item_overhead_per_run, 50),
	  (item_set_slot, "itm_leatherwork", slot_item_base_price, 220),
	  (item_set_slot, "itm_leatherwork", slot_item_enterprise_building_cost, 8000),

      (item_set_slot, "itm_raw_leather", slot_item_urban_demand, 0),
      (item_set_slot, "itm_raw_leather", slot_item_rural_demand, 0),
      (item_set_slot, "itm_raw_leather", slot_item_desert_demand, 0),
      (item_set_slot, "itm_raw_leather", slot_item_production_slot, slot_center_head_cattle),
      (item_set_slot, "itm_raw_leather", slot_item_production_string, "str_head_cattle"),
      (item_set_slot, "itm_raw_leather", slot_item_is_raw_material_only_for, "itm_leatherwork"),
	  (item_set_slot, "itm_raw_leather", slot_item_base_price, 120),

  	  (item_set_slot, "itm_sausages", slot_item_urban_demand, 12),
	  (item_set_slot, "itm_sausages", slot_item_rural_demand, 3),
	  (item_set_slot, "itm_sausages", slot_item_desert_demand, -1),
      (item_set_slot, "itm_sausages", slot_item_production_slot, slot_center_head_sheep),
      (item_set_slot, "itm_sausages", slot_item_production_string, "str_head_sheep"),

	  (item_set_slot, "itm_wool", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_wool", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_wool", slot_item_desert_demand, 0),
      (item_set_slot, "itm_wool", slot_item_production_slot, slot_center_head_sheep),
      (item_set_slot, "itm_wool", slot_item_production_string, "str_head_sheep"),
	  (item_set_slot, "itm_wool", slot_item_is_raw_material_only_for, "itm_wool_cloth"),
	  (item_set_slot, "itm_wool", slot_item_base_price,130),

	  (item_set_slot, "itm_wool_cloth", slot_item_urban_demand, 15),
	  (item_set_slot, "itm_wool_cloth", slot_item_rural_demand, 20),
	  (item_set_slot, "itm_wool_cloth", slot_item_desert_demand, 5),
      (item_set_slot, "itm_wool_cloth", slot_item_production_slot, slot_center_wool_looms),
      (item_set_slot, "itm_wool_cloth", slot_item_production_string, "str_looms"),
	  (item_set_slot, "itm_wool_cloth", slot_item_primary_raw_material, "itm_wool"),
      (item_set_slot, "itm_wool_cloth", slot_item_input_number, 2),
      (item_set_slot, "itm_wool_cloth", slot_item_output_per_run, 2),
      (item_set_slot, "itm_wool_cloth", slot_item_overhead_per_run, 120),
	  (item_set_slot, "itm_wool_cloth", slot_item_base_price, 250),
	  (item_set_slot, "itm_wool_cloth", slot_item_enterprise_building_cost, 6000),

	  (item_set_slot, "itm_raw_flax", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_raw_flax", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_raw_flax", slot_item_desert_demand, 0),
      (item_set_slot, "itm_raw_flax", slot_item_production_slot, slot_center_acres_flax),
      (item_set_slot, "itm_raw_flax", slot_item_production_string, "str_acres_flax"),
      (item_set_slot, "itm_raw_flax", slot_item_is_raw_material_only_for, "itm_linen"),
	  (item_set_slot, "itm_raw_flax", slot_item_base_price, 150),

	  (item_set_slot, "itm_linen", slot_item_urban_demand, 7),
	  (item_set_slot, "itm_linen", slot_item_rural_demand, 3),
	  (item_set_slot, "itm_linen", slot_item_desert_demand, 15),
      (item_set_slot, "itm_linen", slot_item_production_slot, slot_center_linen_looms),
      (item_set_slot, "itm_linen", slot_item_production_string, "str_looms"),
      (item_set_slot, "itm_linen", slot_item_primary_raw_material, "itm_raw_flax"),
      (item_set_slot, "itm_linen", slot_item_input_number, 2),
      (item_set_slot, "itm_linen", slot_item_output_per_run, 2),
      (item_set_slot, "itm_linen", slot_item_overhead_per_run, 120),
	  (item_set_slot, "itm_linen", slot_item_base_price, 250),
	  (item_set_slot, "itm_linen", slot_item_enterprise_building_cost, 6000),

	  (item_set_slot, "itm_iron", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_iron", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_iron", slot_item_desert_demand, 0),
      (item_set_slot, "itm_iron", slot_item_production_slot, slot_center_iron_deposits),
      (item_set_slot, "itm_iron", slot_item_production_string, "str_deposits"),
      (item_set_slot, "itm_iron", slot_item_is_raw_material_only_for, "itm_tools"),
	  (item_set_slot, "itm_iron", slot_item_base_price, 264),

	  (item_set_slot, "itm_tools", slot_item_urban_demand, 7),
	  (item_set_slot, "itm_tools", slot_item_rural_demand, 7),
	  (item_set_slot, "itm_tools", slot_item_desert_demand, 7),
      (item_set_slot, "itm_tools", slot_item_production_slot, slot_center_smithies),
      (item_set_slot, "itm_tools", slot_item_production_string, "str_smithies"),
      (item_set_slot, "itm_tools", slot_item_primary_raw_material, "itm_iron"),
      (item_set_slot, "itm_tools", slot_item_input_number, 2),
      (item_set_slot, "itm_tools", slot_item_output_per_run, 2),
      (item_set_slot, "itm_tools", slot_item_overhead_per_run, 60),
	  (item_set_slot, "itm_tools", slot_item_base_price, 410),
	  (item_set_slot, "itm_tools", slot_item_enterprise_building_cost, 3500),

	  (item_set_slot, "itm_pottery", slot_item_urban_demand, 15),
	  (item_set_slot, "itm_pottery", slot_item_rural_demand, 5),
	  (item_set_slot, "itm_pottery", slot_item_desert_demand, -1),
      (item_set_slot, "itm_pottery", slot_item_production_slot, slot_center_pottery_kilns),
      (item_set_slot, "itm_pottery", slot_item_production_string, "str_kilns"),

	  (item_set_slot, "itm_oil", slot_item_urban_demand, 10),
	  (item_set_slot, "itm_oil", slot_item_rural_demand, 5),
	  (item_set_slot, "itm_oil", slot_item_desert_demand, -1),
      (item_set_slot, "itm_oil", slot_item_production_slot, slot_center_olive_presses),
      (item_set_slot, "itm_oil", slot_item_production_string, "str_presses"),
      (item_set_slot, "itm_oil", slot_item_primary_raw_material, "itm_raw_olives"),
      (item_set_slot, "itm_oil", slot_item_input_number, 6),
      (item_set_slot, "itm_oil", slot_item_output_per_run, 2),
      (item_set_slot, "itm_oil", slot_item_overhead_per_run, 80),
	  (item_set_slot, "itm_oil", slot_item_base_price, 450),
	  (item_set_slot, "itm_oil", slot_item_enterprise_building_cost, 4500),

	  (item_set_slot, "itm_raw_olives", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_raw_olives", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_raw_olives", slot_item_desert_demand, 0),
      (item_set_slot, "itm_raw_olives", slot_item_production_slot, slot_center_acres_olives),
      (item_set_slot, "itm_raw_olives", slot_item_production_string, "str_olive_groves"),
      (item_set_slot, "itm_raw_olives", slot_item_is_raw_material_only_for, "itm_oil"),
	  (item_set_slot, "itm_raw_olives", slot_item_base_price, 100),

	  (item_set_slot, "itm_velvet", slot_item_urban_demand, 5),
	  (item_set_slot, "itm_velvet", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_velvet", slot_item_desert_demand, -1),
      (item_set_slot, "itm_velvet", slot_item_production_slot, slot_center_silk_looms),
      (item_set_slot, "itm_velvet", slot_item_production_string, "str_looms"),
	  (item_set_slot, "itm_velvet", slot_item_primary_raw_material, "itm_raw_silk"),
      (item_set_slot, "itm_velvet", slot_item_input_number, 2),
      (item_set_slot, "itm_velvet", slot_item_output_per_run, 2),
      (item_set_slot, "itm_velvet", slot_item_overhead_per_run, 160),
	  (item_set_slot, "itm_velvet", slot_item_base_price, 1025),
	  (item_set_slot, "itm_velvet", slot_item_secondary_raw_material, "itm_raw_dyes"),
	  (item_set_slot, "itm_velvet", slot_item_enterprise_building_cost, 10000),

	  (item_set_slot, "itm_raw_silk", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_raw_silk", slot_item_rural_demand, 0),
      (item_set_slot, "itm_raw_silk", slot_item_production_slot, slot_center_silk_farms),
      (item_set_slot, "itm_raw_silk", slot_item_production_string, "str_mulberry_groves"),
      (item_set_slot, "itm_raw_silk", slot_item_is_raw_material_only_for, "itm_velvet"),
      (item_set_slot, "itm_raw_silk", slot_item_base_price, 600),

	  (item_set_slot, "itm_raw_dyes", slot_item_urban_demand, 3),
	  (item_set_slot, "itm_raw_dyes", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_raw_dyes", slot_item_desert_demand, -1),
	  (item_set_slot, "itm_raw_dyes", slot_item_production_string, "str_caravans"),
	  (item_set_slot, "itm_raw_dyes", slot_item_base_price, 200),

	  (item_set_slot, "itm_spice", slot_item_urban_demand, 5),
	  (item_set_slot, "itm_spice", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_spice", slot_item_desert_demand, 5),
	  (item_set_slot, "itm_spice", slot_item_production_string, "str_caravans"),

	  (item_set_slot, "itm_furs", slot_item_urban_demand, 5),
	  (item_set_slot, "itm_furs", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_furs", slot_item_desert_demand, -1),
	  (item_set_slot, "itm_furs", slot_item_production_slot, slot_center_fur_traps),
	  (item_set_slot, "itm_furs", slot_item_production_string, "str_traps"),

      (item_set_slot, "itm_honey", slot_item_urban_demand, 12),
      (item_set_slot, "itm_honey", slot_item_rural_demand, 3),
      (item_set_slot, "itm_honey", slot_item_desert_demand, -1),
      (item_set_slot, "itm_honey", slot_item_production_slot, slot_center_apiaries),
      (item_set_slot, "itm_honey", slot_item_production_string, "str_hives"),

      (item_set_slot, "itm_cabbages", slot_item_urban_demand, 7),
      (item_set_slot, "itm_cabbages", slot_item_rural_demand, 7),
      (item_set_slot, "itm_cabbages", slot_item_desert_demand, 7),
      (item_set_slot, "itm_cabbages", slot_item_production_slot, slot_center_household_gardens),
      (item_set_slot, "itm_cabbages", slot_item_production_string, "str_gardens"),

      (item_set_slot, "itm_raw_date_fruit", slot_item_urban_demand, 7),
      (item_set_slot, "itm_raw_date_fruit", slot_item_rural_demand, 7),
      (item_set_slot, "itm_raw_date_fruit", slot_item_desert_demand, 7),
      (item_set_slot, "itm_raw_date_fruit", slot_item_production_slot, slot_center_household_gardens),
      (item_set_slot, "itm_raw_date_fruit", slot_item_production_string, "str_acres_oasis"),

      (item_set_slot, "itm_chicken", slot_item_urban_demand, 40),
      (item_set_slot, "itm_chicken", slot_item_rural_demand, 10),
      (item_set_slot, "itm_chicken", slot_item_desert_demand, -1),

      (item_set_slot, "itm_pork", slot_item_urban_demand, 40),
      (item_set_slot, "itm_pork", slot_item_rural_demand, 10),
      (item_set_slot, "itm_pork", slot_item_desert_demand, -1),

      # Setting book intelligence requirements
      (item_set_slot, "itm_book_tactics", slot_item_intelligence_requirement, 9),
      (item_set_slot, "itm_book_persuasion", slot_item_intelligence_requirement, 8),
      (item_set_slot, "itm_book_leadership", slot_item_intelligence_requirement, 7),
      (item_set_slot, "itm_book_intelligence", slot_item_intelligence_requirement, 10),
      (item_set_slot, "itm_book_trade", slot_item_intelligence_requirement, 11),
      (item_set_slot, "itm_book_weapon_mastery", slot_item_intelligence_requirement, 9),
      (item_set_slot, "itm_book_engineering", slot_item_intelligence_requirement, 12),

      (item_set_slot, "itm_book_wound_treatment_reference", slot_item_intelligence_requirement, 10),
      (item_set_slot, "itm_book_training_reference", slot_item_intelligence_requirement, 10),
      (item_set_slot, "itm_book_surgery_reference", slot_item_intelligence_requirement, 10),
	 ]),


    ("initialize_economic_information",
    [
	    #All towns produce tools, pottery, and wool cloth for sale in countryside
	(try_for_range, ":town_no", towns_begin, towns_end),
		(store_random_in_range, ":random_average_20_variation_10", 10, 31), #10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29 or 30
		(party_set_slot, ":town_no", slot_center_wool_looms, ":random_average_20_variation_10"),

		(store_random_in_range, ":random_average_2_variation_1", 1, 4), #1,2 or 3
		(party_set_slot, ":town_no", slot_center_breweries, ":random_average_2_variation_1"),

		(store_random_in_range, ":random_average_5_variation_3", 3, 9), #2,3,4,5,6,7 or 8
		(party_set_slot, ":town_no", slot_center_pottery_kilns, ":random_average_5_variation_3"),

		(store_random_in_range, ":random_average_15_variation_9", 6, 25), #6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23 or 24
		(party_set_slot, ":town_no", slot_center_smithies, ":random_average_15_variation_9"),

		(store_random_in_range, ":random_average_5_variation_3", 3, 9), #2,3,4,5,6,7 or 8
		(party_set_slot, ":town_no", slot_center_mills, ":random_average_5_variation_3"),

		(store_random_in_range, ":random_average_2_variation_1", 1, 4), #1,2 or 3
		(party_set_slot, ":town_no", slot_center_tanneries, ":random_average_2_variation_1"),

		(store_random_in_range, ":random_average_1_variation_1", 0, 3), #0,1 or 2
		(party_set_slot, ":town_no", slot_center_wine_presses, ":random_average_1_variation_1"),

		(store_random_in_range, ":random_average_2_variation_1", 1, 4), #1,2 or 3
		(party_set_slot, ":town_no", slot_center_olive_presses, ":random_average_2_variation_1"),

		(store_random_in_range, ":random_average_1000_variation_1000", 0, 2001), #0..2000
		(party_set_slot, ":town_no", slot_center_acres_grain, ":random_average_1000_variation_1000"), #0..2000

		(store_random_in_range, ":random_average_1000_variation_1000", 0, 2001), #0..2000
		(party_set_slot, ":town_no", slot_center_acres_vineyard, ":random_average_1000_variation_1000"), #0..2000
    (try_end),

	#Sargoth (linen, wine)
	(party_set_slot, "p_town_1", slot_center_linen_looms, 15),
	(party_set_slot, "p_town_1", slot_center_wine_presses, 4),

	#Tihr (salt, smoked fish, linen)
	(party_set_slot, "p_town_2", slot_center_salt_pans, 3),
	(party_set_slot, "p_town_2", slot_center_fishing_fleet, 25),
	(party_set_slot, "p_town_2", slot_center_linen_looms, 15),

	#Veluca	(wine, velvet)
	(party_set_slot, "p_town_3", slot_center_wine_presses, 10),
	(party_set_slot, "p_town_3", slot_center_silk_looms, 12),

	#Suno (velvet, oil)
	(party_set_slot, "p_town_4", slot_center_silk_looms, 12),
	(party_set_slot, "p_town_4", slot_center_olive_presses, 15),

	#Jelkala (velvet, smoked fish)
	(party_set_slot, "p_town_5", slot_center_silk_looms, 24),
	(party_set_slot, "p_town_5", slot_center_fishing_fleet, 30),

	#Praven (ale, leatherwork, smoked fish)
	(party_set_slot, "p_town_6", slot_center_breweries, 10),
	(party_set_slot, "p_town_6", slot_center_tanneries, 4),
	(party_set_slot, "p_town_6", slot_center_fishing_fleet, 10),

	#Uxkhal (bread, leatherwork, oil)
	(party_set_slot, "p_town_7", slot_center_mills, 15),
	(party_set_slot, "p_town_7", slot_center_tanneries, 4),
	(party_set_slot, "p_town_7", slot_center_olive_presses, 5),

	#Reyvadin (tools, wool cloth, wine)
	(party_set_slot, "p_town_8", slot_center_smithies, 25),
	(party_set_slot, "p_town_8", slot_center_wool_looms, 35),
	(party_set_slot, "p_town_8", slot_center_wine_presses, 4),

	#Khudan (tools, leatherwork, smoked fish)
	(party_set_slot, "p_town_9", slot_center_smithies, 18),
	(party_set_slot, "p_town_9", slot_center_tanneries, 3),
	(party_set_slot, "p_town_9", slot_center_fishing_fleet, 5),

	#Tulga (salt, spice)
	(party_set_slot, "p_town_10", slot_center_salt_pans, 2),
	#also produces 100 spice

	#Curaw (tools, iron, smoked fish)
	(party_set_slot, "p_town_11", slot_center_smithies, 19),
	(party_set_slot, "p_town_11", slot_center_iron_deposits, 10),
	(party_set_slot, "p_town_11", slot_center_fishing_fleet, 10),

	#Wercheg (salt, smoked fish)
    (party_set_slot, "p_town_12", slot_center_salt_pans, 3),
	(party_set_slot, "p_town_12", slot_center_fishing_fleet, 25),

	#Rivacheg (wool cloth, leatherwork, smoked fish)
	(party_set_slot, "p_town_13", slot_center_wool_looms, 30),
	(party_set_slot, "p_town_13", slot_center_tanneries, 5),
	(party_set_slot, "p_town_13", slot_center_fishing_fleet, 20),

	#Halmar (leatherwork, pottery)
	(party_set_slot, "p_town_14", slot_center_tanneries, 3),
	(party_set_slot, "p_town_14", slot_center_pottery_kilns, 18),

	#Yalen (tools, wine, oil, smoked fish)
	(party_set_slot, "p_town_15", slot_center_smithies, 20),
	(party_set_slot, "p_town_15", slot_center_wine_presses, 6),
	(party_set_slot, "p_town_15", slot_center_olive_presses, 5),
	(party_set_slot, "p_town_15", slot_center_fishing_fleet, 25),

	#Dhirim (tools, leatherwork)
	(party_set_slot, "p_town_16", slot_center_smithies, 30),
	(party_set_slot, "p_town_16", slot_center_tanneries, 4),

	#Ichamur (wool cloth, spice)
	(party_set_slot, "p_town_17", slot_center_wool_looms, 40),
	#also produces 50 spice

	#Narra (wool cloth, oil)
	(party_set_slot, "p_town_18", slot_center_wool_looms, 35),
	(party_set_slot, "p_town_18", slot_center_olive_presses, 10),

	#Shariz (leatherwork, smoked fish, oil)
	(party_set_slot, "p_town_19", slot_center_tanneries, 5),
	(party_set_slot, "p_town_19", slot_center_breweries, 0), 	    #no alcohol (ale) in arabic region
	(party_set_slot, "p_town_19", slot_center_wine_presses, 0), 	#no alcohol (wine) in arabic region
	(party_set_slot, "p_town_19", slot_center_fishing_fleet, 5),
	(party_set_slot, "p_town_19", slot_center_olive_presses, 5),
	#also produces 50 spice

	#Darquba (linen, pottery, oil)
	(party_set_slot, "p_town_20", slot_center_breweries, 0), 	    #no alcohol (ale) in arabic region
	(party_set_slot, "p_town_20", slot_center_wine_presses, 0), 	#no alcohol (wine) in arabic region
	(party_set_slot, "p_town_20", slot_center_linen_looms, 15),
	(party_set_slot, "p_town_20", slot_center_pottery_kilns, 12),
	(party_set_slot, "p_town_19", slot_center_olive_presses, 3),

	#Ahmerrad (pottery, salt)
	(party_set_slot, "p_town_21", slot_center_breweries, 0), 	    #no alcohol (ale) in arabic region
	(party_set_slot, "p_town_21", slot_center_wine_presses, 0), 	#no alcohol (wine) in arabic region
	(party_set_slot, "p_town_21", slot_center_pottery_kilns, 24),
	(party_set_slot, "p_town_21", slot_center_salt_pans, 1),

	#Bariyye (salt, pottery, spice)
	(party_set_slot, "p_town_22", slot_center_breweries, 0), 	    #no alcohol (ale) in arabic region
	(party_set_slot, "p_town_22", slot_center_wine_presses, 0), 	#no alcohol (wine) in arabic region
	(party_set_slot, "p_town_22", slot_center_pottery_kilns, 12),
	(party_set_slot, "p_town_22", slot_center_salt_pans, 2),


  #Zendar (iron, leatherwork, tools )
  (party_set_slot, "p_town_23", slot_center_smithies, 19),
	(party_set_slot, "p_town_23", slot_center_iron_deposits, 10),
	(party_set_slot, "p_town_23", slot_center_tanneries, 5),

	#also produces 50 spice

    (try_for_range, ":village_no", villages_begin, villages_end),
      (try_begin),
      ##diplomacy start+ Replace the explicit "is desert" list with a terrain check.
      ##This is less brittle to map changes.
            (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#In Diplomacy this is true at the start of the module, but the player could re-initialize economic stats during the game with cheat codes, or derived mods could change the default.
            (party_get_current_terrain, ":village_is_at_desert", ":village_no"),#Will be changed to either 0 or 1
	    (this_or_next|eq, ":village_is_at_desert", rt_desert),
	    (eq, ":village_is_at_desert", rt_desert_forest),#If false, will fall through and be assigned to 0 below
	    (assign, ":village_is_at_desert", 1),
      (else_try),
	    (lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW), #Fall back to old behavior
      ##diplomacy end+
	    (this_or_next|eq, ":village_no", "p_village_93"), #mazigh
		(this_or_next|eq, ":village_no", "p_village_94"), #sekhtem
		(this_or_next|eq, ":village_no", "p_village_95"), #qalyut
		(this_or_next|eq, ":village_no", "p_village_96"), #tilimsal
		(this_or_next|eq, ":village_no", "p_village_97"), #shibal zumr
		(this_or_next|eq, ":village_no", "p_village_102"), #tamnuh
		(this_or_next|eq, ":village_no", "p_village_109"), #habba
		(this_or_next|eq, ":village_no", "p_village_98"), #mawiti
		(this_or_next|eq, ":village_no", "p_village_103"), #mijayet
		(this_or_next|eq, ":village_no", "p_village_105"), #aab
		(this_or_next|eq, ":village_no", "p_village_99"), #fishara
		(this_or_next|eq, ":village_no", "p_village_100"), #iqbayl
		(this_or_next|eq, ":village_no", "p_village_107"), #unriya
		(this_or_next|eq, ":village_no", "p_village_101"), #uzgha
		(this_or_next|eq, ":village_no", "p_village_104"), #tazjunat
        (this_or_next|eq, ":village_no", "p_village_110"), #rushdigh
		(this_or_next|eq, ":village_no", "p_village_108"), #mit nun
		(eq, ":village_no", "p_village_92"), #dhibbain

		(assign, ":village_is_at_desert", 1),
	  (else_try),
		(assign, ":village_is_at_desert", 0),
	  (try_end),

      (store_random_in_range, ":random_cattle", 20, 100),
	  (try_begin),
	    (eq, ":village_is_at_desert", 1),
		(val_div, ":random_cattle", 5),
	  (try_end),
      (party_set_slot, ":village_no", slot_center_head_cattle, ":random_cattle"), #average : 50, min : 25, max : 75

      (store_random_in_range, ":random_sheep", 40, 200),
	  (try_begin),
	    (eq, ":village_is_at_desert", 1),
		(val_div, ":random_sheep", 5),
	  (try_end),
      (party_set_slot, ":village_no", slot_center_head_sheep, ":random_sheep"), #average : 100, min : 50, max : 150

	  #grain production
      (store_random_in_range, ":random_value_between_0_and_40000", 0, 40000),
	  (store_random_in_range, ":random_value_between_0_and_average_20000", 0, ":random_value_between_0_and_40000"),
	  (try_begin),
	    (eq, ":village_is_at_desert", 1),
		(val_div, ":random_value_between_0_and_average_20000", 5),
	  (try_end),
	  (party_set_slot, ":village_no", slot_center_acres_grain, ":random_value_between_0_and_average_20000"), #average : 10000, min : 0, max : 40000

      #grape production
	  (store_random_in_range, ":random_value_between_0_and_2000", 0, 2000),
	  (store_random_in_range, ":random_value_between_0_and_average_1000", 0, ":random_value_between_0_and_2000"),
	  (try_begin),
	    (eq, ":village_is_at_desert", 1),
		(val_div, ":random_value_between_0_and_average_1000", 5),
	  (try_end),
	  (party_set_slot, ":village_no", slot_center_acres_vineyard, ":random_value_between_0_and_average_1000"), #average : 500, min : 0, max : 2000

	  #olive production
      (store_random_in_range, ":random_value_between_0_and_2000", 0, 2000),
	  (store_random_in_range, ":random_value_between_0_and_average_1000", 0, ":random_value_between_0_and_2000"),
	  (try_begin),
	    (eq, ":village_is_at_desert", 1),
		(val_div, ":random_value_between_0_and_average_1000", 5),
	  (try_end),
	  (party_set_slot, ":village_no", slot_center_acres_olives, ":random_value_between_0_and_average_1000"), #average : 500, min : 0, max : 2000

	  #honey production
	  (store_random_in_range, ":random_value_between_0_and_3", 0, 3),
	  (try_begin),
	    (eq, ":village_is_at_desert", 1),
		(assign, ":random_value_between_0_and_3", 0), #at desert regions no honey production
	  (try_end),
	  (party_set_slot, ":village_no", slot_center_apiaries, ":random_value_between_0_and_3"),

	  #cabbage and fruit production
	  (store_random_in_range, ":random_value_between_0_and_5", 0, 5),
	  (try_begin),
	    (eq, ":village_is_at_desert", 1),
		(assign, ":random_value_between_0_and_5", 0), #at desert regions no cabbage and fruit production
	  (try_end),
	  (party_set_slot, ":village_no", slot_center_household_gardens, ":random_value_between_0_and_5"),

	  #bread production
      (store_random_in_range, ":random_value_between_0_and_3", 0, 3),
	  (party_set_slot, ":village_no", slot_center_mills, ":random_value_between_0_and_3"),

	  #pottery production
	  (store_random_in_range, ":random_value_between_0_and_5", 0, 5),
		(try_begin),
	    (eq, ":village_is_at_desert", 1),
		(val_mul, ":random_value_between_0_and_5", 5), #at desert regions pottery production 4x more than normal (totally 5x)
	  (try_end),
	  (party_set_slot, ":village_no", slot_center_pottery_kilns, ":random_value_between_0_and_5"),

	  #Sargoth (village productions : Ambean, Fearichen and Fenada)
	  (try_begin),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_1"),
		(party_set_slot, ":village_no", slot_center_acres_flax, 4000),
		(party_set_slot, ":village_no", slot_center_acres_vineyard, 8000),

	  #Tihr (village productions : Kulum, Haen and Aldelen)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_2"),
		(party_set_slot, ":village_no", slot_center_acres_vineyard, 8000),
		(party_set_slot, ":village_no", slot_center_household_gardens, 10),

	  #Veluca (village productions : Emer, Fedner, Chaeza and Sarimish)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_3"),
		(party_set_slot, ":village_no", slot_center_acres_vineyard, 6000),
		(party_set_slot, ":village_no", slot_center_acres_olives, 6000),

	  #Suno (village productions : Ruluns and Lyindah)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_4"),
		(party_set_slot, ":village_no", slot_center_fur_traps, 2),
		(party_set_slot, ":village_no", slot_center_acres_olives, 8000),

	  #Jelkala (village productions : Buvran, Ruldi and Chelez)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_5"),
		(party_set_slot, ":village_no", slot_center_silk_farms, 1500),
		(party_set_slot, ":village_no", slot_center_kirmiz_farms, 1500),

	  #Praven (village productions : Azgad, Veidar, Elberl and Gisim)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_6"),
		(party_set_slot, ":village_no", slot_center_acres_flax, 4000),
		(party_set_slot, ":village_no", slot_center_breweries, 4),

	  #Uxkhal (village productions : Nomar, Ibiran and Tahlberl)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_7"),
		(party_set_slot, ":village_no", slot_center_fur_traps, 1),
		(party_set_slot, ":village_no", slot_center_acres_olives, 8000),
		(party_set_slot, ":village_no", slot_center_apiaries, 8),

      #Reyvadin (village productions : Ulburban and Ayyike)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_8"),
		(party_set_slot, ":village_no", slot_center_fur_traps, 2),
			(party_set_slot, ":village_no", slot_center_head_cattle, 100),
		(party_set_slot, ":village_no", slot_center_iron_deposits, 6),

      #Khudan (village productions : Uslum, Shulus and Tismirr)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_9"),
		(party_set_slot, ":village_no", slot_center_fur_traps, 2),
		(party_set_slot, ":village_no", slot_center_acres_olives, 4000),

      #Tulga (village productions : Dusturil and Dashbigha)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_10"),
			(party_set_slot, ":village_no", slot_center_head_sheep, 150),
			(party_set_slot, ":village_no", slot_center_salt_pans, 1),
			(party_set_slot, ":village_no", slot_center_fur_traps, 1),
		(party_set_slot, ":village_no", slot_center_apiaries, 8),

      #Curaw (village productions : Bazeck and Rebache)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_11"),
		(party_set_slot, ":village_no", slot_center_iron_deposits, 6),
		(party_set_slot, ":village_no", slot_center_fur_traps, 2),

      #Wercheg (village productions : Ruvar and Odasan)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_12"),
		(party_set_slot, ":village_no", slot_center_acres_vineyard, 8000),
		(party_set_slot, ":village_no", slot_center_household_gardens, 10),
		(party_set_slot, ":village_no", slot_center_salt_pans, 1),

      #Rivacheg (village productions : Shapeshte, Vezin and Fisdnar)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_13"),
		(party_set_slot, ":village_no", slot_center_fur_traps, 2),
		(party_set_slot, ":village_no", slot_center_head_cattle, 100),
		(party_set_slot, ":village_no", slot_center_silk_farms, 1500),

      #Halmar (village productions : Peshmi)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_14"),
		(party_set_slot, ":village_no", slot_center_acres_grain, 40000),
		(party_set_slot, ":village_no", slot_center_mills, 5),

      #Yalen (village productions : Ilvia, Glunmar, Epeshe and Istiniar)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_15"),
		(party_set_slot, ":village_no", slot_center_acres_vineyard, 8000),
		(party_set_slot, ":village_no", slot_center_acres_olives, 8000),
		(party_set_slot, ":village_no", slot_center_household_gardens, 10),

      #Dhirim (village productions : Burglen, Amere, Ushkuru, Tshibtin and Yalibe)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_16"),
        (party_set_slot, ":village_no", slot_center_acres_grain, 40000),
        (party_set_slot, ":village_no", slot_center_iron_deposits, 3),
		(party_set_slot, ":village_no", slot_center_mills, 5),

      #Ichamur (village productions : Ada Kulun and Drigh Aban)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_17"),
        (party_set_slot, ":village_no", slot_center_acres_grain, 20000),
			(party_set_slot, ":village_no", slot_center_fur_traps, 1),

      #Narra (village productions : Zagush and Kedelke)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_18"),
        (party_set_slot, ":village_no", slot_center_acres_grain, 20000),
        (party_set_slot, ":village_no", slot_center_iron_deposits, 3),
		(party_set_slot, ":village_no", slot_center_apiaries, 8),
		(party_set_slot, ":village_no", slot_center_acres_flax, 4000),

      #Shariz (village productions : Ayn Assuadi, Dhibbain, Qalyut, Tilimsal and Rushdigh)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_19"),
        (party_set_slot, ":village_no", slot_center_acres_grain, 6000), #low grain (partially desert)
			(party_set_slot, ":village_no", slot_center_acres_flax, 2000),
			(party_set_slot, ":village_no", slot_center_acres_olives, 3000),
        (party_set_slot, ":village_no", slot_center_acres_dates, 5000),

      #Durquba (village productions : Tamnuh and Sekhtem)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_20"),
        (party_set_slot, ":village_no", slot_center_acres_grain, 3000), #low grain (heavy desert)
        (party_set_slot, ":village_no", slot_center_acres_dates, 10000),
			(party_set_slot, ":village_no", slot_center_salt_pans, 1),

      #Ahmerrad (village productions : Mawiti, Uzgha and Mijayet)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_21"),
        (party_set_slot, ":village_no", slot_center_acres_grain, 3000), #low grain (heavy desert)
        (party_set_slot, ":village_no", slot_center_acres_dates, 5000),
		(party_set_slot, ":village_no", slot_center_kirmiz_farms, 1500),

      #Bariyye (village productions : Fishara and Iqbayl)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_22"),
        (party_set_slot, ":village_no", slot_center_acres_grain, 2000), #low grain (heavy desert)
			(party_set_slot, ":village_no", slot_center_acres_flax, 2000),
        (party_set_slot, ":village_no", slot_center_acres_dates, 10000),
        (party_set_slot, ":village_no", slot_center_salt_pans, 1),
        (party_set_slot, ":village_no", slot_center_kirmiz_farms, 1500),

      #Zendar (village productions : Hrafnvik and Vargdal)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_23"),
		    (party_set_slot, ":village_no", slot_center_acres_flax, 4000),
		    (party_set_slot, ":village_no", slot_center_fur_traps, 2),
        (party_set_slot, ":village_no", slot_center_iron_deposits, 3),
		(try_end),
    (try_end),

	#determining village productions which are bounded by castle by nearby village productions which are bounded by a town.
	(try_for_range, ":village_no", villages_begin, villages_end),
	  (party_get_slot, ":bound_center", ":village_no", slot_village_bound_center),
	  (is_between, ":bound_center", castles_begin, castles_end),

	  (try_for_range, ":cur_production_source", slot_production_sources_begin, slot_production_sources_end),

		(assign, ":total_averaged_production", 0),
		(try_for_range, ":effected_village_no", villages_begin, villages_end),
		  (party_get_slot, ":bound_center", ":effected_village_no", slot_village_bound_center),
	      (is_between, ":bound_center", towns_begin, towns_end),

		  (store_distance_to_party_from_party, ":dist", ":village_no", ":effected_village_no"),
		  (le, ":dist", 72),

		  (party_get_slot, ":production", ":village_no", ":cur_production_source"),

		  (store_add, ":dist_plus_24", ":dist", 24),
		  (store_mul, ":production_mul_12", ":production", 12),
		  (store_div, ":averaged_production", ":production_mul_12", ":dist_plus_24"), #if close (12/24=1/2) else (12/96=1/8)
		  (val_div, ":averaged_production", 2), #if close (1/4) else (1/16)
		  (val_add, ":total_averaged_production", ":averaged_production"),
		(try_end),

		(party_set_slot, ":village_no", ":cur_production_source", ":total_averaged_production"),
      (try_end),
	(try_end),

	#Ocean and river villages, new map
    (party_set_slot, "p_village_1", slot_center_fishing_fleet, 15), #Yaragar
    (party_set_slot, "p_village_3", slot_center_fishing_fleet, 15), #Azgad
    (party_set_slot, "p_village_5", slot_center_fishing_fleet, 15), #Kulum

    (party_set_slot, "p_village_8", slot_center_fishing_fleet, 15), #Haen
    (party_set_slot, "p_village_9", slot_center_fishing_fleet, 15), #Buvran

    (party_set_slot, "p_village_20", slot_center_fishing_fleet, 15), #Uslum
    (party_set_slot, "p_village_21", slot_center_fishing_fleet, 15), #Bazeck
    (party_set_slot, "p_village_23", slot_center_fishing_fleet, 15), #Ilvia
    (party_set_slot, "p_village_27", slot_center_fishing_fleet, 15), #Glunmar

    (party_set_slot, "p_village_30", slot_center_fishing_fleet, 20), #Ruvar
    (party_set_slot, "p_village_31", slot_center_fishing_fleet, 15), #Ambean
    (party_set_slot, "p_village_35", slot_center_fishing_fleet, 15), #Feacharin

    (party_set_slot, "p_village_47", slot_center_fishing_fleet, 15), #Epeshe
    (party_set_slot, "p_village_49", slot_center_fishing_fleet, 15), #Tismirr

    (party_set_slot, "p_village_51", slot_center_fishing_fleet, 15), #Jelbegi
    (party_set_slot, "p_village_56", slot_center_fishing_fleet, 15), #Fenada

    (party_set_slot, "p_village_66", slot_center_fishing_fleet, 15), #Fisdnar
    (party_set_slot, "p_village_68", slot_center_fishing_fleet, 15), #Ibdeles
    (party_set_slot, "p_village_69", slot_center_fishing_fleet, 15), #Kwynn

    (party_set_slot, "p_village_77", slot_center_fishing_fleet, 25), #Rizi - Estuary
    (party_set_slot, "p_village_79", slot_center_fishing_fleet, 15), #Istiniar

	(party_set_slot, "p_village_81", slot_center_fishing_fleet, 15), #Odasan
    (party_set_slot, "p_village_85", slot_center_fishing_fleet, 15), #Ismirala
    (party_set_slot, "p_village_87", slot_center_fishing_fleet, 15), #Udiniad

    (party_set_slot, "p_village_90", slot_center_fishing_fleet, 15), #Jamiche

	#Initialize pastureland
	(try_for_range, ":center", centers_begin, centers_end),
		(party_get_slot, ":head_cattle", ":center", slot_center_head_cattle),
		(party_get_slot, ":head_sheep", ":center", slot_center_head_sheep),
		(store_mul, ":num_acres", ":head_cattle", 4),
		(val_add, ":num_acres", ":head_sheep"),
		(val_add, ":num_acres", ":head_sheep"),
		(val_mul, ":num_acres", 6),
		(val_div, ":num_acres", 5),

		(store_random_in_range, ":random", 60, 150),
		(val_mul, ":num_acres", ":random"),
		(val_div, ":num_acres", 100),

		(party_set_slot, ":center", slot_center_acres_pasture, ":num_acres"),
	(try_end),

	#Initialize prices based on production, etc
    (try_for_range, ":unused", 0, 3), #15 cycles = 45 days. For a village with -20 production, this should lead to approximate +1000, modified
        (call_script, "script_update_trade_good_prices"), #changes prices based on production
    (try_end),

	#Initialize prosperity based on final prices
    (try_for_range, ":center_no", centers_begin, centers_end),
      (neg|is_between, ":center_no", castles_begin, castles_end),
      (store_random_in_range, ":random_prosperity_adder", -10, 10),
      (call_script, "script_get_center_ideal_prosperity", ":center_no"),
      (assign, ":prosperity", reg0),
      (val_add, ":prosperity", ":random_prosperity_adder"),
      (val_clamp, ":prosperity", 0, 100),
      (party_set_slot, ":center_no", slot_town_prosperity, ":prosperity"),
	(try_end),

	(call_script, "script_calculate_castle_prosperities_by_using_its_villages"),
    ]),

  #script_initialize_all_scene_prop_slots
  # INPUT: arg1 = scene_prop_no
  # OUTPUT: none
  ("initialize_all_scene_prop_slots",
   [
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_6m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_8m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_10m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_12m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_14m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_castle_e_sally_door_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_castle_f_sally_door_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_earth_sally_gate_left"),
     (call_script, "script_initialize_scene_prop_slots", "spr_earth_sally_gate_right"),
     (call_script, "script_initialize_scene_prop_slots", "spr_viking_keep_destroy_sally_door_left"),
     (call_script, "script_initialize_scene_prop_slots", "spr_viking_keep_destroy_sally_door_right"),
     (call_script, "script_initialize_scene_prop_slots", "spr_castle_f_door_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_belfry_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_belfry_b"),
     (call_script, "script_initialize_scene_prop_slots", "spr_winch_b"),
    ]),

  #script_initialize_scene_prop_slots
  # INPUT: arg1 = scene_prop_no
  # OUTPUT: none
  ("initialize_scene_prop_slots",
   [
     (store_script_param, ":scene_prop_no", 1),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", ":scene_prop_no"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", ":scene_prop_no", ":cur_instance"),
       (try_for_range, ":cur_slot", 0, scene_prop_slots_end),
         (scene_prop_set_slot, ":cur_instance_id", ":cur_slot", 0),
       (try_end),
     (try_end),
     ]),

  #script_use_item
  # INPUT: none
  # OUTPUT: none
  ("initialize_objects",
   [
     (assign, ":number_of_players", 0),
     (get_max_players, ":num_players"),
     (try_for_range, ":player_no", 0, ":num_players"),
       (player_is_active, ":player_no"),
       (val_add, ":number_of_players", 1),
     (try_end),

     #1 player = (Sqrt(1) - 1) * 200 + 1200 = 1200, 1800 (minimum)
     #4 player = (Sqrt(4) - 1) * 200 + 1200 = 1400, 2100
     #9 player = (Sqrt(9) - 1) * 200 + 1200 = 1600, 2400
     #16 player = (Sqrt(16) - 1) * 200 + 1200 = 1800, 2700 (general used)
     #25 player = (Sqrt(25) - 1) * 200 + 1200 = 2000, 3000 (average)
     #36 player = (Sqrt(36) - 1) * 200 + 1200 = 2200, 3300
     #49 player = (Sqrt(49) - 1) * 200 + 1200 = 2400, 3600
     #64 player = (Sqrt(49) - 1) * 200 + 1200 = 2600, 3900

     (set_fixed_point_multiplier, 100),
     (val_mul, ":number_of_players", 100),
     (store_sqrt, ":number_of_players", ":number_of_players"),
     (val_sub, ":number_of_players", 100),
     (val_max, ":number_of_players", 0),
     (store_mul, ":effect_of_number_of_players", ":number_of_players", 2),
     (store_add, ":health_catapult", multi_minimum_target_health, ":effect_of_number_of_players"),
     (store_mul, ":health_trebuchet", ":health_catapult", 15), #trebuchet's health is 1.5x of catapult's
     (val_div, ":health_trebuchet", 10),
     (store_mul, ":health_sally_door", ":health_catapult", 18), #sally door's health is 1.8x of catapult's
     (val_div, ":health_sally_door", 10),
     (store_mul, ":health_sally_door_double", ":health_sally_door", 2),

     (assign, "$g_number_of_targets_destroyed", 0),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_catapult_destructible"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_catapult_destructible", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_catapult"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_trebuchet_destructible"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_trebuchet_destructible", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_trebuchet"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_e_sally_door_a"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_e_sally_door_a", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_f_sally_door_a"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_f_sally_door_a", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_earth_sally_gate_left"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_earth_sally_gate_left", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_double"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_earth_sally_gate_right"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_earth_sally_gate_right", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_double"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_viking_keep_destroy_sally_door_left"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_viking_keep_destroy_sally_door_left", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_viking_keep_destroy_sally_door_right"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_viking_keep_destroy_sally_door_right", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),

     (store_div, ":health_sally_door_div_3", ":health_sally_door", 3),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_f_door_a"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_f_door_a", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_div_3"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_f_door_b"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_f_door_b", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_div_3"),
     (try_end),
     ]),

  #script_initialize_objects_clients
  # INPUT: none
  # OUTPUT: none
  ("initialize_objects_clients",
   [
     (assign, ":number_of_players", 0),
     (get_max_players, ":num_players"),
     (try_for_range, ":player_no", 0, ":num_players"),
       (player_is_active, ":player_no"),
       (val_add, ":number_of_players", 1),
     (try_end),

     #1 player = (Sqrt(1) - 1) * 200 + 1200 = 1200, 1800 (minimum)
     #4 player = (Sqrt(4) - 1) * 200 + 1200 = 1400, 2100
     #9 player = (Sqrt(9) - 1) * 200 + 1200 = 1600, 2400
     #16 player = (Sqrt(16) - 1) * 200 + 1200 = 1800, 2700 (general used)
     #25 player = (Sqrt(25) - 1) * 200 + 1200 = 2000, 3000 (average)
     #36 player = (Sqrt(36) - 1) * 200 + 1200 = 2200, 3300
     #49 player = (Sqrt(49) - 1) * 200 + 1200 = 2400, 3600
     #64 player = (Sqrt(49) - 1) * 200 + 1200 = 2600, 3900

     (set_fixed_point_multiplier, 100),
     (val_mul, ":number_of_players", 100),
     (store_sqrt, ":number_of_players", ":number_of_players"),
     (val_sub, ":number_of_players", 100),
     (val_max, ":number_of_players", 0),
     (store_mul, ":effect_of_number_of_players", ":number_of_players", 2),
     (store_add, ":health_catapult", multi_minimum_target_health, ":effect_of_number_of_players"),
     (store_mul, ":health_trebuchet", ":health_catapult", 15), #trebuchet's health is 1.5x of catapult's
     (val_div, ":health_trebuchet", 10),
     (store_mul, ":health_sally_door", ":health_catapult", 18), #trebuchet's health is 1.8x of trebuchet's
     (val_div, ":health_sally_door", 10),
     (store_mul, ":health_sally_door_double", ":health_sally_door", 2),

     (assign, "$g_number_of_targets_destroyed", 0),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_catapult_destructible"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_catapult_destructible", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_catapult"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_trebuchet_destructible"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_trebuchet_destructible", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_trebuchet"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_e_sally_door_a"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_e_sally_door_a", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_f_sally_door_a"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_f_sally_door_a", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_earth_sally_gate_left"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_earth_sally_gate_left", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_double"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_earth_sally_gate_right"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_earth_sally_gate_right", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_double"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_viking_keep_destroy_sally_door_left"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_viking_keep_destroy_sally_door_left", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_viking_keep_destroy_sally_door_right"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_viking_keep_destroy_sally_door_right", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),

     (store_div, ":health_sally_door_div_3", ":health_sally_door", 3),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_f_door_a"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_f_door_a", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_div_3"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_f_door_b"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_f_door_b", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_div_3"),
     (try_end),
     ]),

  #script_show_multiplayer_message
  #response format should be like this:
  #  [a number or a string]|[another number or a string]|[yet another number or a string] ...
  # here is an example response:
  # 12|Player|100|another string|142|323542|34454|yet another string
  # INPUT: arg1 = num_integers, arg2 = num_strings
  # reg0, reg1, reg2, ... up to 128 registers contain the integer values
  # s0, s1, s2, ... up to 128 strings contain the string values
  ("game_receive_url_response",
    [
      #here is an example usage
##      (store_script_param, ":num_integers", 1),
##      (store_script_param, ":num_strings", 2),
##      (try_begin),
##        (gt, ":num_integers", 4),
##        (display_message, "@{reg0}, {reg1}, {reg2}, {reg3}, {reg4}"),
##      (try_end),
##      (try_begin),
##        (gt, ":num_strings", 4),
##        (display_message, "@{s0}, {s1}, {s2}, {s3}, {s4}"),
##      (try_end),
      ]),

  ("game_get_cheat_mode",
  [
    (assign, reg0, "$cheat_mode"),
  ]),

  #script_game_receive_network_message
  # This script is called from the game engine when a new network message is received.
  # INPUT: arg1 = player_no, arg2 = event_type, arg3 = value, arg4 = value_2, arg5 = value_3, arg6 = value_4
  ("game_receive_network_message",
    [
      (store_script_param, ":player_no", 1),
      (store_script_param, ":event_type", 2),
      (try_begin),
        ###############
        #SERVER EVENTS#
        ###############
        (eq, ":event_type", multiplayer_event_set_item_selection),
        (store_script_param, ":slot_no", 3),
        (store_script_param, ":value", 4),
        (try_begin),
          #valid slot check
          (is_between, ":slot_no", slot_player_selected_item_indices_begin, slot_player_selected_item_indices_end),
          #valid item check
          (assign, ":valid_item", 0),
          (try_begin),
            (eq, ":value", -1),
            (assign, ":valid_item", 1),
          (else_try),
            (ge, ":value", 0),
            (player_get_troop_id, ":player_troop_no", ":player_no"),
            (is_between, ":player_troop_no", multiplayer_troops_begin, multiplayer_troops_end),
            (store_sub, ":troop_index", ":player_troop_no", multiplayer_troops_begin),
            (val_add, ":troop_index", slot_item_multiplayer_availability_linked_list_begin),
            (item_get_slot, ":prev_next_item_ids", ":value", ":troop_index"),
            (gt, ":prev_next_item_ids", 0), #0 if the item is not valid for the multiplayer mode
            (assign, ":valid_item", 1),
            (try_begin),
              (neq, "$g_horses_are_avaliable", 1),
              (item_get_slot, ":item_class", ":value", slot_item_multiplayer_item_class),
              (is_between, ":item_class", multi_item_class_type_horses_begin, multi_item_class_type_horses_end),
              (assign, ":valid_item", 0),
            (try_end),
            (try_begin),
              (eq, "$g_multiplayer_disallow_ranged_weapons", 1),
              (item_get_slot, ":item_class", ":value", slot_item_multiplayer_item_class),
              (is_between, ":item_class", multi_item_class_type_ranged_weapons_begin, multi_item_class_type_ranged_weapons_end),
              (assign, ":valid_item", 0),
            (try_end),
          (try_end),
          (eq, ":valid_item", 1),
          #condition checks are done
          (player_set_slot, ":player_no", ":slot_no", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_set_bot_selection),
        (store_script_param, ":slot_no", 3),
        (store_script_param, ":value", 4),
        (try_begin),
          #condition check
          (is_between, ":slot_no", slot_player_bot_type_1_wanted, slot_player_bot_type_4_wanted + 1),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (player_set_slot, ":player_no", ":slot_no", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_change_team_no),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_get_team_no, ":player_team", ":player_no"),
          (neq, ":player_team", ":value"),

          #condition checks are done
          (try_begin),
            #check if available
            (call_script, "script_cf_multiplayer_team_is_available", ":player_no", ":value"),
            #reset troop_id to -1
            (player_set_troop_id, ":player_no", -1),
            (player_set_team_no, ":player_no", ":value"),
            (try_begin),
              (neq, ":value", multi_team_spectator),
              (neq, ":value", multi_team_unassigned),

              (store_mission_timer_a, ":player_last_team_select_time"),
              (player_set_slot, ":player_no", slot_player_last_team_select_time, ":player_last_team_select_time"),

              (multiplayer_send_message_to_player, ":player_no", multiplayer_event_return_confirmation),
            (try_end),
          (else_try),
            #reject request
            (multiplayer_send_message_to_player, ":player_no", multiplayer_event_return_rejection),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_change_troop_id),
        (store_script_param, ":value", 3),
        #troop-faction validity check
        (try_begin),
          (eq, ":value", -1),
          (player_set_troop_id, ":player_no", -1),
        (else_try),
          (is_between, ":value", multiplayer_troops_begin, multiplayer_troops_end),
          (player_get_team_no, ":player_team", ":player_no"),
          (is_between, ":player_team", 0, multi_team_spectator),
          (team_get_faction, ":team_faction", ":player_team"),
          (store_troop_faction, ":new_troop_faction", ":value"),
          (eq, ":new_troop_faction", ":team_faction"),
          (player_set_troop_id, ":player_no", ":value"),
          (call_script, "script_multiplayer_clear_player_selected_items", ":player_no"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_start_map),
        (store_script_param, ":value", 3),
        (store_script_param, ":value_2", 4),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", multiplayer_scenes_begin, multiplayer_scenes_end),
          (is_between, ":value_2", 0, multiplayer_num_game_types),
          (server_get_changing_game_type_allowed, "$g_multiplayer_changing_game_type_allowed"),
          (this_or_next|eq, "$g_multiplayer_changing_game_type_allowed", 1),
          (eq, "$g_multiplayer_game_type", ":value_2"),
          (call_script, "script_multiplayer_fill_map_game_types", ":value_2"),
          (assign, ":num_maps", reg0),
          (assign, ":is_valid", 0),
          (store_add, ":end_cond", multi_data_maps_for_game_type_begin, ":num_maps"),
          (try_for_range, ":i_map", multi_data_maps_for_game_type_begin, ":end_cond"),
            (troop_slot_eq, "trp_multiplayer_data", ":i_map", ":value"),
            (assign, ":is_valid", 1),
            (assign, ":end_cond", 0),
          (try_end),
          (eq, ":is_valid", 1),
          #condition checks are done
          (assign, "$g_multiplayer_game_type", ":value_2"),
          (assign, "$g_multiplayer_selected_map", ":value"),
          (team_set_faction, 0, "$g_multiplayer_next_team_1_faction"),
          (team_set_faction, 1, "$g_multiplayer_next_team_2_faction"),
          (call_script, "script_game_multiplayer_get_game_type_mission_template", "$g_multiplayer_game_type"),
          (start_multiplayer_mission, reg0, "$g_multiplayer_selected_map", 1),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_max_num_players),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 2, 201),
          #condition checks are done
          (server_set_max_num_players, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_num_bots_in_team),
        (store_script_param, ":value", 3),
        (store_script_param, ":value_2", 4),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 1, 3),
          (is_between, ":value_2", 0, "$g_multiplayer_max_num_bots"),
          #condition checks are done
          (try_begin),
            (eq, ":value", 1),
            (assign, "$g_multiplayer_num_bots_team_1", ":value_2"),
          (else_try),
            (assign, "$g_multiplayer_num_bots_team_2", ":value_2"),
          (try_end),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_return_num_bots_in_team, ":value", ":value_2"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_anti_cheat),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (server_set_anti_cheat, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_friendly_fire),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (server_set_friendly_fire, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_melee_friendly_fire),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (server_set_melee_friendly_fire, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_friendly_fire_damage_self_ratio),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 101),
          #condition checks are done
          (server_set_friendly_fire_damage_self_ratio, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_friendly_fire_damage_friend_ratio),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 101),
          #condition checks are done
          (server_set_friendly_fire_damage_friend_ratio, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_ghost_mode),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 4),
          #condition checks are done
          (server_set_ghost_mode, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_control_block_dir),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (server_set_control_block_dir, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_combat_speed),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 5),
          #condition checks are done
          (server_set_combat_speed, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_respawn_count),
        (store_script_param, ":value", 3),
        #validity check
        (player_is_admin, ":player_no"),
        (is_between, ":value", 0, 6),
        #condition checks are done
        (assign, "$g_multiplayer_number_of_respawn_count", ":value"),
        (get_max_players, ":num_players"),
        (try_for_range, ":cur_player", 1, ":num_players"),
          (player_is_active, ":cur_player"),
          (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_respawn_count, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_add_to_servers_list),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          #condition checks are done
          (server_set_add_to_game_servers_list, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_respawn_period),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 3, 31),
          #condition checks are done
          (assign, "$g_multiplayer_respawn_period", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_respawn_period, ":value"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_game_max_minutes),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 5, 121),
          #condition checks are done
          (assign, "$g_multiplayer_game_max_minutes", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_round_max_seconds),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 60, 901),
          #condition checks are done
          (assign, "$g_multiplayer_round_max_seconds", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_round_max_seconds, ":value"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_player_respawn_as_bot),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_player_respawn_as_bot", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_player_respawn_as_bot, ":value"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_game_max_points),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 3, 1001),
          #condition checks are done
          (assign, "$g_multiplayer_game_max_points", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_point_gained_from_flags),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 25, 401),
          #condition checks are done
          (assign, "$g_multiplayer_point_gained_from_flags", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_point_gained_from_capturing_flag),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 11),
          #condition checks are done
          (assign, "$g_multiplayer_point_gained_from_capturing_flag", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_initial_gold_multiplier),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 1001),
          #condition checks are done
          (assign, "$g_multiplayer_initial_gold_multiplier", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_battle_earnings_multiplier),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 1001),
          #condition checks are done
          (assign, "$g_multiplayer_battle_earnings_multiplier", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_round_earnings_multiplier),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 1001),
          #condition checks are done
          (assign, "$g_multiplayer_round_earnings_multiplier", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_server_name),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (server_get_renaming_server_allowed, "$g_multiplayer_renaming_server_allowed"),
          (eq, "$g_multiplayer_renaming_server_allowed", 1),
          #condition checks are done
          (server_set_name, s0), #validity is checked inside this function
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_game_password),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          #condition checks are done
          (server_set_password, s0), #validity is checked inside this function
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_welcome_message),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          #condition checks are done
          (server_set_welcome_message, s0), #validity is checked inside this function
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_team_faction),
        (store_script_param, ":value", 3),
        (store_script_param, ":value_2", 4),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 1, 3),
          (is_between, ":value_2", npc_kingdoms_begin, npc_kingdoms_end),
##          (assign, ":is_valid", 0),
##          (try_begin),
##            (eq, ":value", 1),
##            (neq, ":value_2", "$g_multiplayer_next_team_2_faction"),
##            (assign, ":is_valid", 1),
##          (else_try),
##            (neq, ":value_2", "$g_multiplayer_next_team_1_faction"),
##            (assign, ":is_valid", 1),
##          (try_end),
##          (eq, ":is_valid", 1),
          #condition checks are done
          (try_begin),
            (eq, ":value", 1),
            (assign, "$g_multiplayer_next_team_1_faction", ":value_2"),
          (else_try),
            (assign, "$g_multiplayer_next_team_2_faction", ":value_2"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_open_game_rules),
        (try_begin),
          #no validity check
          (server_get_max_num_players, ":max_num_players"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_max_num_players, ":max_num_players"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_next_team_faction, 1, "$g_multiplayer_next_team_1_faction"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_next_team_faction, 2, "$g_multiplayer_next_team_2_faction"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_num_bots_in_team, 1, "$g_multiplayer_num_bots_team_1"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_num_bots_in_team, 2, "$g_multiplayer_num_bots_team_2"),
          (server_get_anti_cheat, ":server_anti_cheat"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_anti_cheat, ":server_anti_cheat"),
          (server_get_friendly_fire, ":server_friendly_fire"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_friendly_fire, ":server_friendly_fire"),
          (server_get_melee_friendly_fire, ":server_melee_friendly_fire"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_melee_friendly_fire, ":server_melee_friendly_fire"),
          (server_get_friendly_fire_damage_self_ratio, ":friendly_fire_damage_self_ratio"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_friendly_fire_damage_self_ratio, ":friendly_fire_damage_self_ratio"),
          (server_get_friendly_fire_damage_friend_ratio, ":friendly_fire_damage_friend_ratio"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_friendly_fire_damage_friend_ratio, ":friendly_fire_damage_friend_ratio"),
          (server_get_ghost_mode, ":server_ghost_mode"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_ghost_mode, ":server_ghost_mode"),
          (server_get_control_block_dir, ":server_control_block_dir"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_control_block_dir, ":server_control_block_dir"),
          (server_get_combat_speed, ":server_combat_speed"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_combat_speed, ":server_combat_speed"),
          (server_get_add_to_game_servers_list, ":server_add_to_servers_list"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_add_to_servers_list, ":server_add_to_servers_list"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_respawn_period, "$g_multiplayer_respawn_period"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_game_max_minutes, "$g_multiplayer_game_max_minutes"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_round_max_seconds, "$g_multiplayer_round_max_seconds"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_player_respawn_as_bot, "$g_multiplayer_player_respawn_as_bot"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_game_max_points, "$g_multiplayer_game_max_points"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_point_gained_from_flags, "$g_multiplayer_point_gained_from_flags"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_point_gained_from_capturing_flag, "$g_multiplayer_point_gained_from_capturing_flag"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_initial_gold_multiplier, "$g_multiplayer_initial_gold_multiplier"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_battle_earnings_multiplier, "$g_multiplayer_battle_earnings_multiplier"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_round_earnings_multiplier, "$g_multiplayer_round_earnings_multiplier"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_valid_vote_ratio, "$g_multiplayer_valid_vote_ratio"),
          (str_store_server_name, s0),
          (multiplayer_send_string_to_player, ":player_no", multiplayer_event_return_server_name, s0),
          (multiplayer_send_message_to_player, ":player_no", multiplayer_event_return_open_game_rules),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_open_admin_panel),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          #condition checks are done
          (server_get_renaming_server_allowed, "$g_multiplayer_renaming_server_allowed"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_renaming_server_allowed, "$g_multiplayer_renaming_server_allowed"),
          (server_get_changing_game_type_allowed, "$g_multiplayer_changing_game_type_allowed"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_changing_game_type_allowed, "$g_multiplayer_changing_game_type_allowed"),
          (server_get_max_num_players, ":max_num_players"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_max_num_players, ":max_num_players"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_next_team_faction, 1, "$g_multiplayer_next_team_1_faction"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_next_team_faction, 2, "$g_multiplayer_next_team_2_faction"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_num_bots_in_team, 1, "$g_multiplayer_num_bots_team_1"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_num_bots_in_team, 2, "$g_multiplayer_num_bots_team_2"),
          (server_get_anti_cheat, ":server_anti_cheat"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_anti_cheat, ":server_anti_cheat"),
          (server_get_friendly_fire, ":server_friendly_fire"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_friendly_fire, ":server_friendly_fire"),
          (server_get_melee_friendly_fire, ":server_melee_friendly_fire"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_melee_friendly_fire, ":server_melee_friendly_fire"),
          (server_get_friendly_fire_damage_self_ratio, ":friendly_fire_damage_self_ratio"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_friendly_fire_damage_self_ratio, ":friendly_fire_damage_self_ratio"),
          (server_get_friendly_fire_damage_friend_ratio, ":friendly_fire_damage_friend_ratio"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_friendly_fire_damage_friend_ratio, ":friendly_fire_damage_friend_ratio"),
          (server_get_ghost_mode, ":server_ghost_mode"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_ghost_mode, ":server_ghost_mode"),
          (server_get_control_block_dir, ":server_control_block_dir"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_control_block_dir, ":server_control_block_dir"),
          (server_get_combat_speed, ":server_combat_speed"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_combat_speed, ":server_combat_speed"),
          (server_get_add_to_game_servers_list, ":server_add_to_servers_list"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_add_to_servers_list, ":server_add_to_servers_list"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_respawn_period, "$g_multiplayer_respawn_period"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_game_max_minutes, "$g_multiplayer_game_max_minutes"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_round_max_seconds, "$g_multiplayer_round_max_seconds"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_player_respawn_as_bot, "$g_multiplayer_player_respawn_as_bot"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_game_max_points, "$g_multiplayer_game_max_points"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_point_gained_from_flags, "$g_multiplayer_point_gained_from_flags"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_point_gained_from_capturing_flag, "$g_multiplayer_point_gained_from_capturing_flag"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_initial_gold_multiplier, "$g_multiplayer_initial_gold_multiplier"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_battle_earnings_multiplier, "$g_multiplayer_battle_earnings_multiplier"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_round_earnings_multiplier, "$g_multiplayer_round_earnings_multiplier"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_valid_vote_ratio, "$g_multiplayer_valid_vote_ratio"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_max_num_bots, "$g_multiplayer_max_num_bots"),
          (str_store_server_name, s0),
          (multiplayer_send_string_to_player, ":player_no", multiplayer_event_return_server_name, s0),
          (str_store_server_password, s0),
          (multiplayer_send_string_to_player, ":player_no", multiplayer_event_return_game_password, s0),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_start_new_poll),
        (try_begin),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
           #validity check
          (eq, "$g_multiplayer_poll_running", 0),
          (store_mission_timer_a, ":mission_timer"),
          (player_get_slot, ":poll_disable_time", ":player_no", slot_player_poll_disabled_until_time),
          (ge, ":mission_timer", ":poll_disable_time"),
          (assign, ":continue", 0),
          (try_begin),
            (eq, ":value", 1), # kicking a player
            (try_begin),
              (eq, "$g_multiplayer_kick_voteable", 1),
              (player_is_active, ":value_2"),
              (assign, ":continue", 1),
            (try_end),
          (else_try),
            (eq, ":value", 2), # banning a player
            (try_begin),
              (eq, "$g_multiplayer_ban_voteable", 1),
              (player_is_active, ":value_2"),
              (save_ban_info_of_player, ":value_2"),
              (assign, ":continue", 1),
            (try_end),
          (else_try), # vote for map
            (eq, ":value", 0),
            (try_begin),
              (eq, "$g_multiplayer_maps_voteable", 1),
              (call_script, "script_multiplayer_fill_map_game_types", "$g_multiplayer_game_type"),
              (assign, ":num_maps", reg0),
              (try_for_range, ":i_map", 0, ":num_maps"),
                (store_add, ":map_slot", ":i_map", multi_data_maps_for_game_type_begin),
                (troop_slot_eq, "trp_multiplayer_data", ":map_slot", ":value_2"),
                (assign, ":continue", 1),
                (assign, ":num_maps", 0), #break
              (try_end),
            (try_end),
          (else_try),
            (eq, ":value", 3), #vote for map and factions
            (try_begin),
              (eq, "$g_multiplayer_factions_voteable", 1),
              (store_script_param, ":value_3", 5),
              (store_script_param, ":value_4", 6),
              (call_script, "script_multiplayer_fill_map_game_types", "$g_multiplayer_game_type"),
              (assign, ":num_maps", reg0),
              (try_for_range, ":i_map", 0, ":num_maps"),
                (store_add, ":map_slot", ":i_map", multi_data_maps_for_game_type_begin),
                (troop_slot_eq, "trp_multiplayer_data", ":map_slot", ":value_2"),
                (assign, ":continue", 1),
                (assign, ":num_maps", 0), #break
              (try_end),
              (try_begin),
                (eq, ":continue", 1),
                (this_or_next|neg|is_between, ":value_3", npc_kingdoms_begin, npc_kingdoms_end),
                (this_or_next|neg|is_between, ":value_4", npc_kingdoms_begin, npc_kingdoms_end),
                (eq, ":value_3", ":value_4"),
                (assign, ":continue", 0),
              (try_end),
            (try_end),
          (else_try),
            (eq, ":value", 4), #vote for number of bots
            (store_script_param, ":value_3", 5),
            (store_add, ":upper_limit", "$g_multiplayer_num_bots_voteable", 1),
            (is_between, ":value_2", 0, ":upper_limit"),
            (is_between, ":value_3", 0, ":upper_limit"),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          #condition checks are done
          (str_store_player_username, s0, ":player_no"),
          (try_begin),
            (eq, ":value", 1), #kicking a player
            (str_store_player_username, s1, ":value_2"),
            (server_add_message_to_log, "str_poll_kick_player_s1_by_s0"),
          (else_try),
            (eq, ":value", 2), #banning a player
            (str_store_player_username, s1, ":value_2"),
            (server_add_message_to_log, "str_poll_ban_player_s1_by_s0"),
          (else_try),
            (eq, ":value", 0), #vote for map
            (store_sub, ":string_index", ":value_2", multiplayer_scenes_begin),
            (val_add, ":string_index", multiplayer_scene_names_begin),
            (str_store_string, s1, ":string_index"),
            (server_add_message_to_log, "str_poll_change_map_to_s1_by_s0"),
          (else_try),
            (eq, ":value", 3), #vote for map and factions
            (store_sub, ":string_index", ":value_2", multiplayer_scenes_begin),
            (val_add, ":string_index", multiplayer_scene_names_begin),
            (str_store_string, s1, ":string_index"),
            (str_store_faction_name, s2, ":value_3"),
            (str_store_faction_name, s3, ":value_4"),
            (server_add_message_to_log, "str_poll_change_map_to_s1_and_factions_to_s2_and_s3_by_s0"),
          (else_try),
            (eq, ":value", 4), #vote for number of bots
            (assign, reg0, ":value_2"),
            (assign, reg1, ":value_3"),
            (server_add_message_to_log, "str_poll_change_number_of_bots_to_reg0_and_reg1_by_s0"),
          (try_end),
          (assign, "$g_multiplayer_poll_running", 1),
          (assign, "$g_multiplayer_poll_ended", 0),
          (assign, "$g_multiplayer_poll_num_sent", 0),
          (assign, "$g_multiplayer_poll_yes_count", 0),
          (assign, "$g_multiplayer_poll_no_count", 0),
          (assign, "$g_multiplayer_poll_to_show", ":value"),
          (assign, "$g_multiplayer_poll_value_to_show", ":value_2"),
          (try_begin),
            (eq, ":value", 3),
            (assign, "$g_multiplayer_poll_value_2_to_show", ":value_3"),
            (assign, "$g_multiplayer_poll_value_3_to_show", ":value_4"),
          (else_try),
            (eq, ":value", 4),
            (assign, "$g_multiplayer_poll_value_2_to_show", ":value_3"),
            (assign, "$g_multiplayer_poll_value_3_to_show", -1),
          (else_try),
            (assign, "$g_multiplayer_poll_value_2_to_show", -1),
            (assign, "$g_multiplayer_poll_value_3_to_show", -1),
          (try_end),
          (store_add, ":poll_disable_until", ":mission_timer", multiplayer_poll_disable_period),
          (player_set_slot, ":player_no", slot_player_poll_disabled_until_time, ":poll_disable_until"),
          (store_add, "$g_multiplayer_poll_end_time", ":mission_timer", 60),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 0, ":num_players"),
            (player_is_active, ":cur_player"),
            (player_set_slot, ":cur_player", slot_player_can_answer_poll, 1),
            (val_add, "$g_multiplayer_poll_num_sent", 1),
            (multiplayer_send_4_int_to_player, ":cur_player", multiplayer_event_ask_for_poll, "$g_multiplayer_poll_to_show", "$g_multiplayer_poll_value_to_show", "$g_multiplayer_poll_value_2_to_show", "$g_multiplayer_poll_value_3_to_show"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_answer_to_poll),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (eq, "$g_multiplayer_poll_running", 1),
          (is_between, ":value", 0, 2),
          (player_slot_eq, ":player_no", slot_player_can_answer_poll, 1),
          #condition checks are done
          (player_set_slot, ":player_no", slot_player_can_answer_poll, 0),
          (try_begin),
            (eq, ":value", 0),
            (val_add, "$g_multiplayer_poll_no_count", 1),
          (else_try),
            (eq, ":value", 1),
            (val_add, "$g_multiplayer_poll_yes_count", 1),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_kick_player),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (player_is_active, ":value"),
          #condition checks are done
          (kick_player, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_ban_player),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (player_is_active, ":value"),
          #condition checks are done
          (ban_player, ":value", 0, ":player_no"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_valid_vote_ratio),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 50, 101),
          #condition checks are done
          (assign, "$g_multiplayer_valid_vote_ratio", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_auto_team_balance_limit),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (this_or_next|is_between, ":value", 2, 7),
          (eq, ":value", 1000),
          #condition checks are done
          (assign, "$g_multiplayer_auto_team_balance_limit", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_auto_team_balance_limit, ":value"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_num_bots_voteable),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 51),
          (is_between, ":value", 0, "$g_multiplayer_max_num_bots"),
          #condition checks are done
          (assign, "$g_multiplayer_num_bots_voteable", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_num_bots_voteable, ":value"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_factions_voteable),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_factions_voteable", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_factions_voteable, ":value"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_maps_voteable),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_maps_voteable", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_maps_voteable, ":value"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_kick_voteable),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_kick_voteable", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_kick_voteable, ":value"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_ban_voteable),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_ban_voteable", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_ban_voteable, ":value"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_allow_player_banners),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_allow_player_banners", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_force_default_armor),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_force_default_armor", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_offer_duel),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (eq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
          (agent_is_active, ":value"),
          (agent_is_alive, ":value"),
          (agent_is_human, ":value"),
          (player_get_agent_id, ":player_agent_no", ":player_no"),
          (agent_is_active, ":player_agent_no"),
          (agent_is_alive, ":player_agent_no"),
          (agent_get_position, pos0, ":player_agent_no"),
          (agent_get_position, pos1, ":value"),
          (get_sq_distance_between_positions_in_meters, ":agent_dist_sq", pos0, pos1),
          (le, ":agent_dist_sq", 49),
          #allow duelists to receive new offers
          (this_or_next|agent_check_offer_from_agent, ":player_agent_no", ":value"),
          (agent_slot_eq, ":player_agent_no", slot_agent_in_duel_with, -1),
          (neg|agent_slot_eq, ":player_agent_no", slot_agent_in_duel_with, ":value"), #don't allow spamming duel offers during countdown
          #condition checks are done
          (try_begin),
            #accepting a duel
            (agent_check_offer_from_agent, ":player_agent_no", ":value"),
            (call_script, "script_multiplayer_accept_duel", ":player_agent_no", ":value"),
          (else_try),
            #sending a duel request
            (assign, ":display_notification", 1),
            (try_begin),
              (agent_check_offer_from_agent, ":value", ":player_agent_no"),
              (assign, ":display_notification", 0),
            (try_end),
            (agent_add_offer_with_timeout, ":value", ":player_agent_no", 10000), #10 second timeout
            (agent_get_player_id, ":value_player", ":value"),
            (try_begin),
              (player_is_active, ":value_player"), #might be AI
              (try_begin),
                (eq, ":display_notification", 1),
                (multiplayer_send_int_to_player, ":value_player", multiplayer_event_show_duel_request, ":player_agent_no"),
              (try_end),
            (else_try),
              (call_script, "script_multiplayer_accept_duel", ":value", ":player_agent_no"),
            (try_end),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_disallow_ranged_weapons),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_disallow_ranged_weapons", ":value"),
        (try_end),
      (else_try),
        ###############
        #CLIENT EVENTS#
        ###############
        (neg|multiplayer_is_dedicated_server),
        (try_begin),
          (eq, ":event_type", multiplayer_event_return_renaming_server_allowed),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_renaming_server_allowed", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_changing_game_type_allowed),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_changing_game_type_allowed", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_max_num_players),
          (store_script_param, ":value", 3),
          (server_set_max_num_players, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_next_team_faction),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (try_begin),
            (eq, ":value", 1),
            (assign, "$g_multiplayer_next_team_1_faction", ":value_2"),
          (else_try),
            (assign, "$g_multiplayer_next_team_2_faction", ":value_2"),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_num_bots_in_team),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (try_begin),
            (eq, ":value", 1),
            (assign, "$g_multiplayer_num_bots_team_1", ":value_2"),
          (else_try),
            (assign, "$g_multiplayer_num_bots_team_2", ":value_2"),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_anti_cheat),
          (store_script_param, ":value", 3),
          (server_set_anti_cheat, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_friendly_fire),
          (store_script_param, ":value", 3),
          (server_set_friendly_fire, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_melee_friendly_fire),
          (store_script_param, ":value", 3),
          (server_set_melee_friendly_fire, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_friendly_fire_damage_self_ratio),
          (store_script_param, ":value", 3),
          (server_set_friendly_fire_damage_self_ratio, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_friendly_fire_damage_friend_ratio),
          (store_script_param, ":value", 3),
          (server_set_friendly_fire_damage_friend_ratio, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_ghost_mode),
          (store_script_param, ":value", 3),
          (server_set_ghost_mode, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_control_block_dir),
          (store_script_param, ":value", 3),
          (server_set_control_block_dir, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_add_to_servers_list),
          (store_script_param, ":value", 3),
          (server_set_add_to_game_servers_list, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_respawn_period),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_respawn_period", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_game_max_minutes),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_game_max_minutes", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_round_max_seconds),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_round_max_seconds", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_player_respawn_as_bot),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_player_respawn_as_bot", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_game_max_points),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_game_max_points", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_point_gained_from_flags),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_point_gained_from_flags", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_point_gained_from_capturing_flag),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_point_gained_from_capturing_flag", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_initial_gold_multiplier),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_initial_gold_multiplier", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_battle_earnings_multiplier),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_battle_earnings_multiplier", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_round_earnings_multiplier),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_round_earnings_multiplier", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_respawn_count),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_number_of_respawn_count", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_server_name),
          (server_set_name, s0),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_game_password),
          (server_set_password, s0),
          #this is the last option in admin panel, so start the presentation
          (start_presentation, "prsnt_game_multiplayer_admin_panel"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_open_game_rules),
          #this is the last message for game rules, so start the presentation
          (assign, "$g_multiplayer_show_server_rules", 1),
          (start_presentation, "prsnt_multiplayer_welcome_message"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_game_type),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_game_type", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_valid_vote_ratio),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_valid_vote_ratio", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_max_num_bots),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_max_num_bots", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_server_mission_timer_while_player_joined),
          (store_script_param, ":value", 3),
          (assign, "$server_mission_timer_while_player_joined", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_auto_team_balance_limit),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_auto_team_balance_limit", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_num_bots_voteable),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_num_bots_voteable", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_factions_voteable),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_factions_voteable", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_maps_voteable),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_maps_voteable", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_kick_voteable),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_kick_voteable", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_ban_voteable),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_ban_voteable", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_allow_player_banners),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_allow_player_banners", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_force_default_armor),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_force_default_armor", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_disallow_ranged_weapons),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_disallow_ranged_weapons", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_confirmation),
          (assign, "$g_confirmation_result", 1),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_rejection),
          (assign, "$g_confirmation_result", -1),
        (else_try),
          (eq, ":event_type", multiplayer_event_show_multiplayer_message),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (call_script, "script_show_multiplayer_message", ":value", ":value_2"),
        (else_try),
          (eq, ":event_type", multiplayer_event_draw_this_round),
          (store_script_param, ":value", 3),
          (call_script, "script_draw_this_round", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_set_attached_scene_prop),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (call_script, "script_set_attached_scene_prop", ":value", ":value_2"),
          (try_begin),
            (eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
            (try_begin),
              (neq, ":value_2", -1),
              (agent_set_horse_speed_factor, ":value", 75),
            (else_try),
              (agent_set_horse_speed_factor, ":value", 100),
            (try_end),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_set_team_flag_situation),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (call_script, "script_set_team_flag_situation", ":value", ":value_2"),
        (else_try),
          (eq, ":event_type", multiplayer_event_set_team_score),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (call_script, "script_team_set_score", ":value", ":value_2"),
        (else_try),
          (eq, ":event_type", multiplayer_event_set_player_score_kill_death),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (store_script_param, ":value_3", 5),
          (store_script_param, ":value_4", 6),
          (call_script, "script_player_set_score", ":value", ":value_2"),
          (call_script, "script_player_set_kill_count", ":value", ":value_3"),
          (call_script, "script_player_set_death_count", ":value", ":value_4"),
        (else_try),
          (eq, ":event_type", multiplayer_event_set_num_agents_around_flag),
          (store_script_param, ":flag_no", 3),
          (store_script_param, ":current_owner_code", 4),
          (call_script, "script_set_num_agents_around_flag", ":flag_no", ":current_owner_code"),
        (else_try),
          (eq, ":event_type", multiplayer_event_ask_for_poll),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (store_script_param, ":value_3", 5),
          (store_script_param, ":value_4", 6),
          (assign, ":continue_to_poll", 0),
          (try_begin),
            (this_or_next|eq, ":value", 1),
            (eq, ":value", 2),
            (player_is_active, ":value_2"), #might go offline before here
            (assign, ":continue_to_poll", 1),
          (else_try),
            (assign, ":continue_to_poll", 1),
          (try_end),
          (try_begin),
            (eq, ":continue_to_poll", 1),
            (assign, "$g_multiplayer_poll_to_show", ":value"),
            (assign, "$g_multiplayer_poll_value_to_show", ":value_2"),
            (assign, "$g_multiplayer_poll_value_2_to_show", ":value_3"),
            (assign, "$g_multiplayer_poll_value_3_to_show", ":value_4"),
            (store_mission_timer_a, ":mission_timer"),
            (store_add, "$g_multiplayer_poll_client_end_time", ":mission_timer", 60),
            (start_presentation, "prsnt_multiplayer_poll"),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_change_flag_owner),
          (store_script_param, ":flag_no", 3),
          (store_script_param, ":owner_code", 4),
          (call_script, "script_change_flag_owner", ":flag_no", ":owner_code"),
        (else_try),
          (eq, ":event_type", multiplayer_event_use_item),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (call_script, "script_use_item", ":value", ":value_2"),
        (else_try),
          (eq, ":event_type", multiplayer_event_set_scene_prop_open_or_close),
          (store_script_param, ":instance_id", 3),

          (scene_prop_set_slot, ":instance_id", scene_prop_open_or_close_slot, 1),

          (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),

          (try_begin),
            (eq, ":scene_prop_id", "spr_winch_b"),
            (assign, ":effected_object", "spr_portcullis"),
          (else_try),
            (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),
            (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),
            (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
            (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),
            (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
            (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),
            (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_a"),
            (this_or_next|eq, ":scene_prop_id", "spr_door_destructible"),
            (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_b"),
            (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_6m"),
            (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_8m"),
            (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_10m"),
            (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_12m"),
            (eq, ":scene_prop_id", "spr_siege_ladder_move_14m"),
            (assign, ":effected_object", ":scene_prop_id"),
          (try_end),

          (try_begin),
            (eq, ":effected_object", "spr_portcullis"),

            (assign, ":smallest_dist", -1),
            (prop_instance_get_position, pos0, ":instance_id"),
            (scene_prop_get_num_instances, ":num_instances_of_effected_object", ":effected_object"),
            (try_for_range, ":cur_instance", 0, ":num_instances_of_effected_object"),
              (scene_prop_get_instance, ":cur_instance_id", ":effected_object", ":cur_instance"),
              (prop_instance_get_position, pos1, ":cur_instance_id"),
              (get_sq_distance_between_positions, ":dist", pos0, pos1),
              (this_or_next|eq, ":smallest_dist", -1),
              (lt, ":dist", ":smallest_dist"),
              (assign, ":smallest_dist", ":dist"),
              (assign, ":effected_object_instance_id", ":cur_instance_id"),
            (try_end),

            (ge, ":smallest_dist", 0),
            (prop_instance_is_animating, ":is_animating", ":effected_object_instance_id"),
            (eq, ":is_animating", 0),

            (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),
            (position_move_z, pos0, 375),
            (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 1),
          (else_try),
            (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),
            (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),
            (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
            (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),
            (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
            (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),
            (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_a"),
            (this_or_next|eq, ":scene_prop_id", "spr_door_destructible"),
            (eq, ":scene_prop_id", "spr_castle_f_door_b"),
            (assign, ":effected_object_instance_id", ":instance_id"),
            (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),
            (position_rotate_z, pos0, -80),
            (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 1),
          (else_try),
            (assign, ":effected_object_instance_id", ":instance_id"),
            (prop_instance_is_animating, ":is_animating", ":effected_object_instance_id"),
            (eq, ":is_animating", 0),
            (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),
            (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 1),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_set_round_start_time),
          (store_script_param, ":value", 3),

          (try_begin),
            (neq, ":value", -9999),
            (assign, "$g_round_start_time", ":value"),
          (else_try),
            (store_mission_timer_a, "$g_round_start_time"),

            #if round start time is assigning to current time (so new round is starting) then also initialize moveable object slots too.
            (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_6m"),
            (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_8m"),
            (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_10m"),
            (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_12m"),
            (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_14m"),
            (call_script, "script_initialize_scene_prop_slots", "spr_winch_b"),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_force_start_team_selection),
          (try_begin),
            (is_presentation_active, "prsnt_multiplayer_item_select"),
            (assign, "$g_close_equipment_selection", 1),
          (try_end),
          (start_presentation, "prsnt_multiplayer_troop_select"),
        (else_try),
          (eq, ":event_type", multiplayer_event_start_death_mode),
          (assign, "$g_battle_death_mode_started", 2),
          (start_presentation, "prsnt_multiplayer_flag_projection_display_bt"),
          (call_script, "script_start_death_mode"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_player_respawn_spent),
          (store_script_param, ":value", 3),
          (try_begin),
            (gt, "$g_my_spawn_count", 0),
            (store_add, "$g_my_spawn_count", "$g_my_spawn_count", ":value"),
          (else_try),
            (assign, "$g_my_spawn_count", ":value"),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_show_duel_request),
          (store_script_param, ":value", 3),
          (try_begin),
            (agent_is_active, ":value"),
            (agent_get_player_id, ":value_player_no", ":value"),
            (try_begin),
              (player_is_active, ":value_player_no"),
              (str_store_player_username, s0, ":value_player_no"),
            (else_try),
              (str_store_agent_name, s0, ":value"),
            (try_end),
            (display_message, "str_s0_offers_a_duel_with_you"),
            (try_begin),
              (get_player_agent_no, ":player_agent"),
              (agent_is_active, ":player_agent"),
              (agent_add_offer_with_timeout, ":player_agent", ":value", 10000), #10 second timeout
            (try_end),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_start_duel),
          (store_script_param, ":value", 3),
          (store_mission_timer_a, ":mission_timer"),
          (try_begin),
            (agent_is_active, ":value"),
            (get_player_agent_no, ":player_agent"),
            (agent_is_active, ":player_agent"),
            (agent_get_player_id, ":value_player_no", ":value"),
            (try_begin),
              (player_is_active, ":value_player_no"),
              (str_store_player_username, s0, ":value_player_no"),
            (else_try),
              (str_store_agent_name, s0, ":value"),
            (try_end),
            (display_message, "str_a_duel_between_you_and_s0_will_start_in_3_seconds"),
            (assign, "$g_multiplayer_duel_start_time", ":mission_timer"),
            (start_presentation, "prsnt_multiplayer_duel_start_counter"),
            (agent_set_slot, ":player_agent", slot_agent_in_duel_with, ":value"),
            (agent_set_slot, ":value", slot_agent_in_duel_with, ":player_agent"),
            (agent_set_slot, ":player_agent", slot_agent_duel_start_time, ":mission_timer"),
            (agent_set_slot, ":value", slot_agent_duel_start_time, ":mission_timer"),
            (agent_clear_relations_with_agents, ":player_agent"),
            (agent_clear_relations_with_agents, ":value"),
##            (agent_add_relation_with_agent, ":player_agent", ":value", -1),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_cancel_duel),
          (store_script_param, ":value", 3),
          (try_begin),
            (agent_is_active, ":value"),
            (agent_get_player_id, ":value_player_no", ":value"),
            (try_begin),
              (player_is_active, ":value_player_no"),
              (str_store_player_username, s0, ":value_player_no"),
            (else_try),
              (str_store_agent_name, s0, ":value"),
            (try_end),
            (display_message, "str_your_duel_with_s0_is_cancelled"),
          (try_end),
          (try_begin),
            (get_player_agent_no, ":player_agent"),
            (agent_is_active, ":player_agent"),
            (agent_set_slot, ":player_agent", slot_agent_in_duel_with, -1),
            (agent_clear_relations_with_agents, ":player_agent"),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_show_server_message),
          (display_message, "str_server_s0", 0xFFFF6666),
        (try_end),
      (try_end),
     ]),

  # script_cf_multiplayer_evaluate_poll
  # This script is called from the game engine when the prisoner limit is needed for a party.
  # INPUT: arg1 = party_no
  # OUTPUT: reg0 = prisoner_limit
  ("game_get_party_prisoner_limit",
    [
#      (store_script_param_1, ":party_no"),
      (assign, ":troop_no", "trp_player"),

      (assign, ":limit", 0),
      (store_skill_level, ":skill", "skl_prisoner_management", ":troop_no"),
      (store_mul, ":limit", ":skill", 5),
      (try_begin), #SB : override with diplomacy_var2
        (eq, "$diplomacy_var", DPLMC_CURRENT_VERSION_CODE),
        (assign, ":limit", "$diplomacy_var2"),
      (try_end),
      (assign, reg0, ":limit"),
      (set_trigger_result, reg0),
  ]),

  #script_game_get_item_extra_text:
  # This script is called from the game engine when an item's properties are displayed.
  # INPUT: arg1 = item_no, arg2 = extra_text_id (this can be between 0-7 (7 included)), arg3 = item_modifier
  # OUTPUT: result_string = item extra text, trigger_result = text color (0 for default)
  ("game_get_item_extra_text",
    [
      (store_script_param, ":item_no", 1),
      (store_script_param, ":extra_text_id", 2),
      (store_script_param, ":item_modifier", 3),
      (try_begin),
        (is_between, ":item_no", "itm_raw_date_fruit", food_end),
        (neq, ":item_no", "itm_furs"),
        (try_begin),
          (eq, ":extra_text_id", 0),
          (assign, ":continue", 1),
          (try_begin),
            (this_or_next|eq, ":item_no", "itm_cattle_meat"),
            (this_or_next|eq, ":item_no", "itm_pork"),
            (eq, ":item_no", "itm_chicken"),

            (eq, ":item_modifier", imod_rotten),
            (assign, ":continue", 0),
          (try_end),
          (eq, ":continue", 1),
          (item_get_slot, ":food_bonus", ":item_no", slot_item_food_bonus),
          (assign, reg1, ":food_bonus"),
          (set_result_string, "@+{reg1} to party morale"),
          (set_trigger_result, 0x4444FF),
        (else_try),
          (eq, ":extra_text_id", 1),
          (assign, ":quest_no", -1), #no quest selected
          (try_begin),
            (check_quest_active, "qst_deliver_wine"),
            (quest_slot_eq, "qst_deliver_wine", slot_quest_target_item, ":item_no"),
            (assign, ":quest_no", "qst_deliver_wine"),
            (quest_get_slot, ":quest_target_center", ":quest_no", slot_quest_target_center),
          (try_end),

          (try_begin), #prioritize town missions
            (eq, ":quest_no", -1),
            (check_quest_active, "qst_deliver_grain"),
            (quest_slot_eq, "qst_deliver_grain", slot_quest_target_item, ":item_no"),
            (assign, ":quest_no", "qst_deliver_grain"),
            (quest_get_slot, ":quest_target_center", ":quest_no", slot_quest_giver_center),
          (try_end),
          (neq, ":item_modifier", imod_rotten),
          (neq, ":quest_no", -1),
          (quest_get_slot, reg5, ":quest_no", slot_quest_target_amount),
          #probably do a x/n items counter here or something
          (str_store_party_name, s5, ":quest_target_center"),
          (set_result_string, "@Deliver {reg5} units to {s5}"),
          (set_trigger_result, message_alert),
        (try_end),
      (else_try),
        (is_between, ":item_no", readable_books_begin, readable_books_end),
        (try_begin),
          (eq, ":extra_text_id", 0),
          (item_get_slot, reg1, ":item_no", slot_item_intelligence_requirement),
          (set_result_string, "@Requires {reg1} intelligence to read"),
          (set_trigger_result, 0xFFEEDD),
        (else_try),
          (eq, ":extra_text_id", 1),
          (item_get_slot, ":progress", ":item_no", slot_item_book_reading_progress),
          (val_div, ":progress", 10),
          (assign, reg1, ":progress"),
          (set_result_string, "@Reading Progress: {reg1}%"),
          (set_trigger_result, 0xFFEEDD),
        (try_end),
      (else_try),
        (is_between, ":item_no", reference_books_begin, reference_books_end),
        (try_begin),
          (eq, ":extra_text_id", 0),
          (try_begin),
            (eq, ":item_no", "itm_book_wound_treatment_reference"),
            (str_store_string, s1, "@wound treament"),
          (else_try),
            (eq, ":item_no", "itm_book_training_reference"),
            (str_store_string, s1, "@trainer"),
          (else_try),
            (eq, ":item_no", "itm_book_surgery_reference"),
            (str_store_string, s1, "@surgery"),
          (try_end),
          (set_result_string, "@+1 to {s1} while in inventory"),
          (set_trigger_result, 0xFFEEDD),
        (try_end),
      (else_try),

      # sb : debug
        (try_begin),
          (ge, "$cheat_mode", 1),
          (eq, ":extra_text_id", 4),
          (call_script, "script_dplmc_get_item_value_with_imod", ":item_no", ":item_modifier"),
          (assign, ":value", reg0),
          (call_script, "script_dplmc_get_item_score_with_imod", ":item_no", ":item_modifier"),
          (store_div, reg1, ":value", 100),
          (set_result_string, "@item score:{reg0}, value:{reg1}"),
          (set_trigger_result, 0x0DDEEE),
        (try_end),

        (try_begin), #SB : display this block when in item pool mode
          (eq, ":extra_text_id", 2),
          (eq, "$pool_troop", "trp_temp_troop"), #new exit code resets condition
          (this_or_next|eq, "$lord_selected", "trp_player"),
          (is_between, "$lord_selected", companions_begin, companions_end),
          (call_script, "script_item_get_type_aux", ":item_no"),
          (assign, ":meta_type", reg0),
          (gt, ":meta_type", meta_itp_mask), #has a valid meta-type
          (assign, ":string", "str_empty_string"),
          (try_begin), #doesn't need it, Native item type already shows
            # (eq, ":meta_type", dplmc_itp_morningstar),
            # (assign, ":string", "str_dplmc_hero_wpn_slot_two_handed_one_handed"),
          # (else_try),
            (eq, ":meta_type", dplmc_itp_lance),
            (assign, ":string", "str_dplmc_hero_wpn_slot_lance"),
          (else_try),
            (eq, ":meta_type", dplmc_itp_pike),
            (assign, ":string", "str_dplmc_hero_wpn_slot_pikes"),
          (else_try),
            (eq, ":meta_type", dplmc_itp_halberd),
            (assign, ":string", "str_dplmc_hero_wpn_slot_halberd"),
          (try_end),
          (gt, ":string", "str_empty_string"), #could use directly
          (set_result_string, ":string"),
          (set_trigger_result, 0xDDEEFF),
        (try_end),
      (try_end),

  ]),

  #script_game_on_disembark:
  # This script is called from the game engine when the player reaches the shore with a ship.
  # INPUT: pos0 = disembark position
  # OUTPUT: none
  ("game_on_disembark",
   [(jump_to_menu, "mnu_disembark"),
  ]),


  #script_game_context_menu_get_buttons:
  # This script is called from the game engine when the player clicks the right mouse button over a party on the map.
  # INPUT: arg1 = party_no
  # OUTPUT: none, fills the menu buttons
  ("game_context_menu_get_buttons",
   [
     (store_script_param, ":party_no", 1),
     (try_begin),
       (neq, ":party_no", "p_main_party"),
       (context_menu_add_item, "@Move here", cmenu_move),
     (try_end),

     (try_begin),
       (is_between, ":party_no", centers_begin, centers_end),
       (context_menu_add_item, "@View notes", cmenu_notes),
     (else_try),
       (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
       (gt, ":num_stacks", 0),
       (party_stack_get_troop_id, ":troop_no", ":party_no", 0),
       ##diplomacy start+ support for promoted kingdom ladies
       (is_between, ":troop_no", heroes_begin, heroes_end),
       (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
       ##diplomacy end+
       (is_between, ":troop_no", active_npcs_begin, active_npcs_end),
       (context_menu_add_item, "@View notes", cmenu_notes), #move this to same slot
       # Lav modifications start (custom lord notes)
       (context_menu_add_item, "@Add custom note", 3),
       # Lav modifications end (custom lord notes)
     (try_end),

     (try_begin),
       (neq, ":party_no", "p_main_party"),
       (store_faction_of_party, ":party_faction", ":party_no"),

       (this_or_next|eq, ":party_faction", "$players_kingdom"),
       (this_or_next|eq, ":party_faction", "fac_player_supporters_faction"),
       (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_caravan),

       (neg|is_between, ":party_no", centers_begin, centers_end),

       (context_menu_add_item, "@Accompany", cmenu_follow),
     (try_end),

      #SB : debug cheats
      (try_begin),
        (ge, "$cheat_mode", 1),
        (try_begin),
           (neq, ":party_no", "p_main_party"),
           (context_menu_add_item, "@Attach", cmenu_attach),
           # (context_menu_add_item, "@Reinforce", cmenu_reinforce),
           (context_menu_add_item, "@Inspect", cmenu_encounter),
           # (context_menu_add_item, "@Exchange", cmenu_exchange),
        (try_end),
        (try_begin),
          (party_get_num_attached_parties, ":num_attached", ":party_no"),
          (gt, ":num_attached", 0),
          (try_begin),
            (eq, ":party_no", "p_main_party"),
            (party_get_attached_party_with_rank, ":attached_party", "p_main_party", 0),
            (str_store_party_name, s1, ":attached_party"),
            (set_fixed_point_multiplier, 1000),
            (party_get_position, pos1, ":party_no"),
            (position_get_x, reg1, pos1),
            (position_get_y, reg2, pos1),
            (context_menu_add_item, "@Detach {s1} at {reg1},{reg2}", cmenu_attach),
          (try_end),
          (context_menu_add_item, "@Detach All", cmenu_detach),
        (try_end),

        (try_begin),
          (party_get_battle_opponent, ":other_party", ":party_no"),
          (party_is_active, ":other_party"),
          (context_menu_add_item, "@Win Battle", cmenu_winbattle),
          (context_menu_add_item, "@Lose Battle", cmenu_losebattle),
        # (else_try),
          # (context_menu_add_item, "@Wound All", cmenu_wound),
          # (context_menu_add_item, "@Heal All", cmenu_heal),
        (try_end),

        # (try_begin),
          # (is_between, ":party_no", centers_begin, centers_end),
          # (context_menu_add_item, "@Spawn Bandits", cmenu_spawnbandit),
        # (try_end),
      (try_end),
  ]),

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
  ]),

  #script_game_get_skill_modifier_for_troop
  # This script is called from the game engine when a skill's modifiers are needed
  # INPUT: arg1 = troop_no, arg2 = skill_no
  # OUTPUT: trigger_result = modifier_value
  ("game_get_skill_modifier_for_troop",
   [(store_script_param, ":troop_no", 1),
    (store_script_param, ":skill_no", 2),
    (assign, ":modifier_value", 0),
    (try_begin),
      (eq, ":skill_no", "skl_wound_treatment"),
      (call_script, "script_get_troop_item_amount", ":troop_no", "itm_book_wound_treatment_reference"),
      (gt, reg0, 0),
      (val_add, ":modifier_value", 1),
    (else_try),
      (eq, ":skill_no", "skl_trainer"),
      (call_script, "script_get_troop_item_amount", ":troop_no", "itm_book_training_reference"),
      (gt, reg0, 0),
      (val_add, ":modifier_value", 1),
    (else_try),
      (eq, ":skill_no", "skl_surgery"),
      (call_script, "script_get_troop_item_amount", ":troop_no", "itm_book_surgery_reference"),
      (gt, reg0, 0),
      (val_add, ":modifier_value", 1),
    (try_end),
    (set_trigger_result, ":modifier_value"),
    ]),

# Note to modders: Uncomment these if you'd like to use the following.

##  #script_game_check_party_sees_party
##  # This script is called from the game engine when a party is inside the range of another party
##  # INPUT: arg1 = party_no_seer, arg2 = party_no_seen
##  # OUTPUT: trigger_result = true or false (1 = true, 0 = false)
##  ("game_check_party_sees_party",
##   [
##     (store_script_param, ":party_no_seer", 1),
##     (store_script_param, ":party_no_seen", 2),
##     (set_trigger_result, 1),
##    ]),
##

##diplomacy start+
#Enable script_game_check_party_sees_party to prevent compassionate lords from
#attacking villagers and merchant caravans.

#script_game_check_party_sees_party
# This script is called from the game engine when a party is inside the range of another party
# INPUT: arg1 = party_no_seer, arg2 = party_no_seen
# OUTPUT: trigger_result = true or false (1 = true, 0 = false)
	("game_check_party_sees_party",
	[
	(store_script_param_1, ":party_no_seer"),
	(store_script_param_2, ":party_no_seen"),

	(assign, ":trigger_result", 1),
	(assign, ":save_reg0", reg0),

	#Lords who dislike raiding caravans should not attack village_farmer or kingdom_caravan
	#parties.  Achieve this by stopping them from seeing them.
	(try_begin),
		(gt, ":party_no_seer", spawn_points_end),
		(gt, ":party_no_seen", spawn_points_end),

		#Only apply this when the "seer" is a kingdom hero party
		(party_slot_eq, ":party_no_seer", slot_party_type, spt_kingdom_hero_party),

		#Only needed if the seen party is of a hostile faction
		(call_script, "script_get_relation_between_parties", ":party_no_seer", ":party_no_seen"),
		(lt, reg0, 0),

		#Only apply this when the seen party is a merchant caravan or villagers
		(party_get_template_id, ":template", ":party_no_seen"),
		(this_or_next|party_slot_eq, ":party_no_seen", slot_party_type, spt_kingdom_caravan),
		(this_or_next|party_slot_eq,":party_no_seen", slot_party_type, dplmc_spt_gift_caravan),#custom diplomacy caravan
		(this_or_next|eq,":template", "pt_refugees"),
			(party_slot_eq, ":party_no_seen", slot_party_type, spt_village_farmer),

		#Never apply this when the seen party is engaging in hostile actions
		(party_get_battle_opponent, reg0, ":party_no_seen"),
		(lt, reg0, 0),
		(neg|party_slot_eq, ":party_no_seen", slot_party_ai_state, spai_besieging_center),
		(neg|party_slot_eq, ":party_no_seen", slot_party_ai_state, spai_raiding_around_center),
		(neg|party_slot_eq, ":party_no_seen", slot_party_ai_state, spai_engaging_army),
		(neg|party_slot_eq, ":party_no_seen", slot_party_ai_state, spai_accompanying_army),
		(neg|party_slot_eq, ":party_no_seen", slot_party_ai_state, spai_screening_army),


		#Only apply this when the leader is tmt_humanitarian, lrep_benefactor, or lrep_moralist
		(party_get_num_companion_stacks, ":num_stacks", ":party_no_seer"),
		(ge, ":num_stacks", 1),
		(party_stack_get_troop_id, ":leader", ":party_no_seer", 0),
		(ge, ":leader", 1),
		(troop_is_hero, ":leader"),
		(call_script, "script_dplmc_get_troop_morality_value", ":leader", tmt_humanitarian),
		(ge, reg0, 0),# (never apply for leaders who like raiding caravans and attacking villagers)
		(this_or_next|ge, reg0, 1),
		(this_or_next|troop_slot_eq, ":leader", slot_lord_reputation_type, lrep_benefactor),
			(troop_slot_eq, ":leader", slot_lord_reputation_type, lrep_moralist),
		(assign, ":trigger_result", 0),
	(try_end),

	(assign, reg0, ":save_reg0"),
	(set_trigger_result, ":trigger_result"),
	]),
##diplomacy end+

##  #script_game_check_party_sees_party
##  # This script is called from the game engine when a party is inside the range of another party
##  # INPUT: arg1 = party_no_seer, arg2 = party_no_seen
##  # OUTPUT: trigger_result = true or false (1 = true, 0 = false)
##  ("game_check_party_sees_party",
##   [
##     (store_script_param, ":party_no_seer", 1),
##     (store_script_param, ":party_no_seen", 2),
##     (set_trigger_result, 1),
##    ]),
##diplomacy begin
  #script_game_get_party_speed_multiplier
  # This script is called from the game engine when a skill's modifiers are needed
  # INPUT: arg1 = party_no
  # OUTPUT: trigger_result = multiplier (scaled by 100, meaning that giving 100 as the trigger result does not change the party speed)
("game_get_party_speed_multiplier",
  [
    (store_script_param_1, ":party_no"),

    (assign,":speed_multiplier",100),

    (try_begin),
      #(this_or_next|eq,":party_no","p_main_party"),
      (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
      (party_get_skill_level, ":pathfinding_skill", ":party_no", skl_pathfinding),
      (val_mul,":pathfinding_skill",3),
      (val_add,":speed_multiplier",":pathfinding_skill"),
    (try_end),

    (try_begin),
      #(party_has_flag, ":party_no", pf_is_ship),
      (party_get_slot, ":ship_type", ":party_no", slot_party_ship_type),
      (gt, ":ship_type", 0),
      (try_begin),
        (eq, ":ship_type", 1),
        (val_add, ":speed_multiplier", 15),
      (else_try),
        (eq, ":ship_type", 2),
        (val_add, ":speed_multiplier", 20),
      (else_try),
        (eq, ":ship_type", 3),
        (val_add, ":speed_multiplier", 5),
      (else_try),
        (eq, ":ship_type", 4),
        (val_add, ":speed_multiplier", 10),
      (try_end),
    (try_end),

    # (try_begin),
      # (eq,":party_no","p_main_party"),
      # (eq,"$g_move_fast", 1),
      # (val_mul,":speed_multiplier",2),
    # (try_end),

    (try_begin),
        (get_party_ai_behavior, ":behavior", ":party_no"),
        (eq, ":behavior", ai_bhvr_driven_by_party),
        (val_add,":speed_multiplier",10),
    (try_end),

    (val_max, ":speed_multiplier", 0),
    (set_trigger_result, ":speed_multiplier"),
   ]),
##diplomacy end
]
