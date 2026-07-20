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

game_start_scripts = [
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
      (assign, "$game_key_manage_inventory", key_m),
      (call_script, "script_init_item_modifier_value_multiplier"),

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
    ])
]
