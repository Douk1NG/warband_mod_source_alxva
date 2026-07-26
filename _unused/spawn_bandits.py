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

spawn_bandits_scripts = [
("spawn_bandits",
    [
     (set_spawn_radius,1),

	 (try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "@{!}DEBUG : Doing spawn bandit script"),
	 (try_end),

	 (party_template_set_slot, "pt_steppe_bandits", slot_party_template_lair_type, "pt_steppe_bandit_lair"),
	 (party_template_set_slot, "pt_taiga_bandits", slot_party_template_lair_type, "pt_taiga_bandit_lair"),
	 (party_template_set_slot, "pt_mountain_bandits", slot_party_template_lair_type, "pt_mountain_bandit_lair"),
	 (party_template_set_slot, "pt_forest_bandits", slot_party_template_lair_type, "pt_forest_bandit_lair"),
	 (party_template_set_slot, "pt_sea_raiders", slot_party_template_lair_type, "pt_sea_raider_lair"),
	 (party_template_set_slot, "pt_desert_bandits", slot_party_template_lair_type, "pt_desert_bandit_lair"),

	 (party_template_set_slot, "pt_steppe_bandits", slot_party_template_lair_spawnpoint, "p_steppe_bandit_spawn_point"),
	 (party_template_set_slot, "pt_taiga_bandits", slot_party_template_lair_spawnpoint, "p_taiga_bandit_spawn_point"),
	 (party_template_set_slot, "pt_mountain_bandits", slot_party_template_lair_spawnpoint, "p_mountain_bandit_spawn_point"),
	 (party_template_set_slot, "pt_forest_bandits", slot_party_template_lair_spawnpoint, "p_forest_bandit_spawn_point"),
	 (party_template_set_slot, "pt_sea_raiders", slot_party_template_lair_spawnpoint, "p_sea_raider_spawn_point_1"),
	 (party_template_set_slot, "pt_desert_bandits", slot_party_template_lair_spawnpoint, "p_desert_bandit_spawn_point"),

     (try_begin),
       (party_template_get_slot, ":bandit_lair_party", "pt_mountain_bandits", slot_party_template_lair_party),
	   (gt, ":bandit_lair_party", 1),

       (store_num_parties_of_template, ":num_parties", "pt_mountain_bandits"),
       (lt,":num_parties",16), #was 14 at mount&blade, 18 in warband, 16 last decision
       (store_random,":spawn_point",num_mountain_bandit_spawn_points),
       (val_add,":spawn_point","p_mountain_bandit_spawn_point"),
       (set_spawn_radius, 25),
       (spawn_around_party,":spawn_point","pt_mountain_bandits"),
     (try_end),
     (try_begin),

       (party_template_get_slot, ":bandit_lair_party", "pt_forest_bandits", slot_party_template_lair_party),
	   (gt, ":bandit_lair_party", 1),

       (store_num_parties_of_template, ":num_parties", "pt_forest_bandits"),
       (lt,":num_parties",16), #was 14 at mount&blade, 18 in warband, 16 last decision
       (store_random,":spawn_point",num_forest_bandit_spawn_points),
       (val_add,":spawn_point","p_forest_bandit_spawn_point"),
       (set_spawn_radius, 25),
       (spawn_around_party,":spawn_point","pt_forest_bandits"),
     (try_end),
     (try_begin),

       (party_template_get_slot, ":bandit_lair_party", "pt_sea_raiders", slot_party_template_lair_party),
	   (gt, ":bandit_lair_party", 1),

       (store_num_parties_of_template, ":num_parties", "pt_sea_raiders"),
       (lt,":num_parties",16), #was 14 at mount&blade, 18 in warband, 16 last decision
       (store_random,":spawn_point",num_sea_raider_spawn_points),
       (val_add,":spawn_point","p_sea_raider_spawn_point_1"),
       (set_spawn_radius, 25),
       (spawn_around_party,":spawn_point","pt_sea_raiders"),
     (try_end),
     (try_begin),

       (party_template_get_slot, ":bandit_lair_party", "pt_steppe_bandits", slot_party_template_lair_party),
	   (gt, ":bandit_lair_party", 1),

       (store_num_parties_of_template, ":num_parties", "pt_steppe_bandits"),
       (lt,":num_parties",16), #was 14 at mount&blade, 18 in warband, 16 last decision
       (store_random,":spawn_point",num_steppe_bandit_spawn_points),
       (val_add,":spawn_point","p_steppe_bandit_spawn_point"),
       (set_spawn_radius, 25),
       (spawn_around_party,":spawn_point","pt_steppe_bandits"),
     (try_end),
     (try_begin),

       (party_template_get_slot, ":bandit_lair_party", "pt_taiga_bandits", slot_party_template_lair_party),
	   (gt, ":bandit_lair_party", 1),

       (store_num_parties_of_template, ":num_parties", "pt_taiga_bandits"),
       (lt,":num_parties",16), #was 14 at mount&blade, 18 in warband, 16 last decision
       (store_random,":spawn_point",num_taiga_bandit_spawn_points),
       (val_add,":spawn_point","p_taiga_bandit_spawn_point"),
       (set_spawn_radius, 25),
       (spawn_around_party,":spawn_point","pt_taiga_bandits"),
     (try_end),
     (try_begin),

       (party_template_get_slot, ":bandit_lair_party", "pt_desert_bandits", slot_party_template_lair_party),
	   (gt, ":bandit_lair_party", 1),

       (store_num_parties_of_template, ":num_parties", "pt_desert_bandits"),
       (lt,":num_parties",16), #was 14 at mount&blade, 18 in warband, 16 last decision
       (store_random,":spawn_point",num_desert_bandit_spawn_points),
       (val_add,":spawn_point","p_desert_bandit_spawn_point"),
       (set_spawn_radius, 25),
       (spawn_around_party,":spawn_point","pt_desert_bandits"),
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_looters"),
       (lt,":num_parties",42), #was 33 at mount&blade, 50 in warband, 42 last decision
       (store_random_in_range,":spawn_point",villages_begin,villages_end), #spawn looters twice to have lots of them at the beginning
       (set_spawn_radius, 25),
       (spawn_around_party,":spawn_point","pt_looters"),
       (assign, ":spawned_party_id", reg0),
       (try_begin),
         (check_quest_active, "qst_deal_with_looters"),
         (party_set_flags, ":spawned_party_id", pf_quest_party, 1),
       (else_try),
         (party_set_flags, ":spawned_party_id", pf_quest_party, 0),
       (try_end),
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_deserters"),
       (lt,":num_parties",15),
       (set_spawn_radius, 4),
       (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
	     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 5),
         (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
         (store_troop_faction, ":troop_faction", ":troop_no"),
         (neq, ":troop_faction", "fac_player_supporters_faction"),
         (gt, ":party_no", 0),
         (neg|party_is_in_any_town, ":party_no"),
##         (party_get_attached_to, ":attached_party_no", ":party_no"),
##         (lt, ":attached_party_no", 0),#in wilderness
         (spawn_around_party, ":party_no", "pt_deserters"),
         (assign, ":new_party", reg0),

         ##dckplmc
         (try_begin),
          (is_between, ":troop_faction", npc_kingdoms_begin, kingdoms_end),
          (store_sub, ":fac_offset", ":troop_faction", npc_kingdoms_begin),
          (store_add, ":icon", "icon_kingdom_1_soldier_a", ":fac_offset"),
          (party_set_icon, ":new_party", ":icon"),
         (try_end),
         ##

         (store_troop_faction, ":faction_no", ":troop_no"),
         (faction_get_slot, ":tier_1_troop", ":faction_no", slot_faction_tier_1_troop),
         (store_character_level, ":level", "trp_player"),
         (store_mul, ":max_number_to_add", ":level", 2),
         (val_add, ":max_number_to_add", 11),
         (store_random_in_range, ":number_to_add", 10, ":max_number_to_add"),
         (party_add_members, ":new_party", ":tier_1_troop", ":number_to_add"),
         (store_random_in_range, ":random_no", 1, 4),
         (try_for_range, ":unused", 0, ":random_no"),
           (party_upgrade_with_xp, ":new_party", 1000000, 0),
         (try_end),
##         (str_store_party_name, s1, ":party_no"),
##         (call_script, "script_get_closest_center", ":party_no"),
##         (try_begin),
##           (gt, reg0, 0),
##           (str_store_party_name, s2, reg0),
##         (else_try),
##           (str_store_string, s2, "@unknown place"),
##         (try_end),
##         (assign, reg1, ":number_to_add"),
##         (display_message, "@{reg1} Deserters spawned from {s1}, near {s2}."),
       (try_end),
     (try_end), #deserters ends

	 # AC : Dark Hunters, Black Khergits, NPC Ships
     (try_begin),
       (eq, "$g_dark_hunters_enabled", 1),
       (store_num_parties_of_template, ":num_parties", "pt_dark_hunters"),
       (lt,":num_parties",4),
		(store_random_in_range, ":selected_town", towns_begin, towns_end),
		(set_spawn_radius, 25),
		(spawn_around_party, ":selected_town", "pt_dark_hunters"),
     (try_end),
     (try_begin),
       (eq, "$g_dark_hunters_enabled", 1),
       (store_num_parties_of_template, ":num_parties", "pt_black_khergit_raiders"),
       (lt,":num_parties",4),
       (store_random,":spawn_point",num_steppe_bandit_spawn_points),
       (val_add,":spawn_point","p_steppe_bandit_spawn_point"),
       (set_spawn_radius, 25),
       (spawn_around_party,":spawn_point","pt_black_khergit_raiders"),
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_sea_raiders_ship"),
       (lt,":num_parties",17),
       (set_spawn_radius, 25),
       (spawn_around_party,"p_reserved_1","pt_sea_raiders_ship"),
       (assign, ":party_no", reg0),
       (party_set_slot, ":party_no", slot_party_ship_type, 1),
       # (party_get_position, pos1, "p_town_19"),
       # (map_get_water_position_around_position, pos1, pos0, 10),
       # (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
       # (party_set_ai_target_position, ":party_no", pos1),
       # (party_set_flags, ":party_no", pf_default_behavior, 0),
       # (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
       # (party_set_ai_object, ":party_no", "p_main_party"),
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_corsair_ship"),
       (lt,":num_parties",17),
       (set_spawn_radius, 25),
       (spawn_around_party,"p_reserved_3","pt_corsair_ship"),
       (assign, ":party_no", reg0),
       (party_set_slot, ":party_no", slot_party_ship_type, 2),
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_merchant_ship"),
       (lt,":num_parties",8),
       (set_spawn_radius, 1),
       (store_random_in_range, ":origin_port", "p_port_1", "p_ports_end"),
       (spawn_around_party,":origin_port","pt_merchant_ship"),
       (assign, ":party_no", reg0),
       (party_set_slot, ":party_no", slot_party_ship_type, 3),
       (party_set_flags, ":party_no", pf_default_behavior, 0),
       (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
       # (party_get_slot, ":port_town", ":origin_port", slot_port_town),
       # (store_faction_of_party, ":town_faction", ":port_town"),
       # (faction_get_slot, ":reinforcements_b", ":town_faction", slot_faction_reinforcements_b),
       # (try_begin),
         # (eq, ":town_faction", "fac_player_supporters_faction"),
         # (party_get_slot, ":reinforcement_faction", ":port_town", slot_center_original_faction),
         # (faction_get_slot, ":reinforcements_b", ":reinforcement_faction", slot_faction_reinforcements_b),
       # (try_end),
       # (party_add_template, ":party_no", ":reinforcements_b"),
       # (party_add_template, ":party_no", ":reinforcements_b"),
       # (party_set_faction, ":party_no", ":town_faction"),
       (store_random_in_range, ":dest_port", "p_port_1", "p_ports_end"),
       (party_set_ai_object, ":party_no", ":dest_port"),
     (try_end),
     (try_begin),
       (store_num_parties_of_template, ":num_parties", "pt_pirate_ship"),
       (lt,":num_parties",17),
       (set_spawn_radius, 25),
       (spawn_around_party,"p_reserved_2","pt_pirate_ship"),
       (assign, ":party_no", reg0),
       (party_set_slot, ":party_no", slot_party_ship_type, 4),
     (try_end),


	 #Spawn bandit lairs
	(try_for_range, ":bandit_template", bandit_party_templates_begin, bandit_party_templates_end), #SB : template range
		(party_template_get_slot, ":bandit_lair_party", ":bandit_template", slot_party_template_lair_party),
		(le, ":bandit_lair_party", 1),

        #dckplmc
        (party_template_get_slot, ":next_spawn", ":bandit_template", slot_party_template_lair_next_spawn),
        (val_max, ":next_spawn", 0), #in case -1
        (store_current_hours, ":cur_hours"),
    (val_max, ":cur_hours", 0), #in case -1
        (store_sub, ":time_left", ":cur_hours", ":next_spawn"),
    (ge, ":time_left", 0), #1 week

		(party_template_get_slot, ":bandit_lair_template", ":bandit_template", slot_party_template_lair_type),
		(party_template_get_slot, ":bandit_lair_template_spawnpoint", ":bandit_template", slot_party_template_lair_spawnpoint),

		(set_spawn_radius, 20),

        (spawn_around_party, ":bandit_lair_template_spawnpoint", ":bandit_lair_template"),
		(assign, ":new_camp", reg0),

		(party_set_slot, ":new_camp", slot_party_type, spt_bandit_lair),

		(str_store_party_name, s4, ":new_camp"),

		(party_get_position, pos4, ":new_camp"),
        #(party_set_flags, ":new_camp", pf_icon_mask, 1),

		(party_get_current_terrain, ":new_camp_terrain", ":new_camp"),
		(position_get_z, ":elevation", pos4),
		(position_get_y, ":lair_y", pos4),

		(assign, ":center_too_close", 0),
		(try_for_range, ":center", centers_begin, centers_end),
			(eq, ":center_too_close", 0),
			(store_distance_to_party_from_party, ":distance", ":new_camp", ":center"),
			(lt, ":distance", 3),
			(assign, ":center_too_close", 1),
		(try_end),

		(try_begin),
			(eq, ":center_too_close", 1),
			(party_is_active, ":new_camp"),
			(remove_party, ":new_camp"),
			(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, 0),
		(else_try),
			(eq, ":bandit_template", "pt_sea_raiders"),
			(eq, ":new_camp_terrain", 3),
			(map_get_water_position_around_position, pos5, pos4, 4),
			(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, ":new_camp"),
			(party_set_flags, ":new_camp", pf_disabled, 1),
		(else_try),
			(eq, ":bandit_template", "pt_mountain_bandits"),
			(eq, ":new_camp_terrain", 3),
			(gt, ":elevation", 250),
			(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, ":new_camp"),
			(party_set_flags, ":new_camp", pf_disabled, 1),
		(else_try),
			(eq, ":bandit_template", "pt_desert_bandits"),
			(eq, ":new_camp_terrain", 5),
			(gt, ":lair_y", -9000),
			(gt, ":elevation", 125),
			(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, ":new_camp"),
			(party_set_flags, ":new_camp", pf_disabled, 1),
		(else_try),
			(eq, ":bandit_template", "pt_steppe_bandits"),
			(this_or_next|eq, ":new_camp_terrain", 2),
			(eq, ":new_camp_terrain", 10),
			(this_or_next|eq, ":new_camp_terrain", 10),
			(gt, ":elevation", 200),
			(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, ":new_camp"),
			(party_set_flags, ":new_camp", pf_disabled, 1),
		(else_try),
			(eq, ":bandit_template", "pt_taiga_bandits"),
			(eq, ":new_camp_terrain", 12),
			(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, ":new_camp"),
			(party_set_flags, ":new_camp", pf_disabled, 1),
		(else_try),
			(eq, ":bandit_template", "pt_forest_bandits"),
			(eq, ":new_camp_terrain", 11),
			(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, ":new_camp"),
			(party_set_flags, ":new_camp", pf_disabled, 1),
		(else_try),
			(party_is_active, ":new_camp"),
			(str_store_party_name, s4, ":new_camp"),
			(remove_party, ":new_camp"),
			(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, 0),
		(else_try),
		(try_end),
	(try_end),
     ])
]
