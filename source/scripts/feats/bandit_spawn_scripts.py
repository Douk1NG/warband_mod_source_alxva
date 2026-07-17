# -*- coding: cp1254 -*-
# Bandit / pirate / deserter population control and respawn logic for update 010.
# Holds the trickle-respawn helper, the combined pirate-ship spawner, and the
# spawn diagnostics report-line builder. `script_spawn_bandits` (in misc_scripts.py)
# is the caller that wires these together.
from header_common import *
from header_operations import *
from module_constants import *
from header_parties import *
from header_troops import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

#script_spawn_party_type_with_cooldown
# INPUT: arg1 = party_template, arg2 = base_spawn_point, arg3 = num_spawn_points,
#        arg4 = max_parties, arg5 = respawn_cooldown_hours
# OUTPUT: reg0 = new party id (or -1 if no spawn happened)
bandit_spawn_scripts = [

#script_spawn_bandits
# Spawns and maintains all roaming world parties: land bandits (lair-gated), looters,
# deserters, pirate ships (combined pool), dark hunters / black khergits, merchant ships,
# and bandit lairs. Uses the trickle helpers defined below.
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

        (call_script, "script_spawn_party_type_with_cooldown", "pt_mountain_bandits", "p_mountain_bandit_spawn_point", num_mountain_bandit_spawn_points, num_max_bandit_parties_per_type, bandit_respawn_cooldown_hours),
     (try_end),
     (try_begin),

       (party_template_get_slot, ":bandit_lair_party", "pt_forest_bandits", slot_party_template_lair_party),
	   (gt, ":bandit_lair_party", 1),

        (call_script, "script_spawn_party_type_with_cooldown", "pt_forest_bandits", "p_forest_bandit_spawn_point", num_forest_bandit_spawn_points, num_max_bandit_parties_per_type, bandit_respawn_cooldown_hours),
     (try_end),
     (try_begin),

       (party_template_get_slot, ":bandit_lair_party", "pt_sea_raiders", slot_party_template_lair_party),
	   (gt, ":bandit_lair_party", 1),

        (call_script, "script_spawn_party_type_with_cooldown", "pt_sea_raiders", "p_sea_raider_spawn_point_1", num_sea_raider_spawn_points, num_max_bandit_parties_per_type, bandit_respawn_cooldown_hours),
     (try_end),
     (try_begin),

       (party_template_get_slot, ":bandit_lair_party", "pt_steppe_bandits", slot_party_template_lair_party),
	   (gt, ":bandit_lair_party", 1),

        (call_script, "script_spawn_party_type_with_cooldown", "pt_steppe_bandits", "p_steppe_bandit_spawn_point", num_steppe_bandit_spawn_points, num_max_bandit_parties_per_type, bandit_respawn_cooldown_hours),
     (try_end),
     (try_begin),

       (party_template_get_slot, ":bandit_lair_party", "pt_taiga_bandits", slot_party_template_lair_party),
	   (gt, ":bandit_lair_party", 1),

        (call_script, "script_spawn_party_type_with_cooldown", "pt_taiga_bandits", "p_taiga_bandit_spawn_point", num_taiga_bandit_spawn_points, num_max_bandit_parties_per_type, bandit_respawn_cooldown_hours),
     (try_end),
     (try_begin),

       (party_template_get_slot, ":bandit_lair_party", "pt_desert_bandits", slot_party_template_lair_party),
	   (gt, ":bandit_lair_party", 1),

        (call_script, "script_spawn_party_type_with_cooldown", "pt_desert_bandits", "p_desert_bandit_spawn_point", num_desert_bandit_spawn_points, num_max_bandit_parties_per_type, bandit_respawn_cooldown_hours),
     (try_end),
      (try_begin),
        (store_sub, ":num_villages", villages_end, villages_begin),
        (call_script, "script_spawn_party_type_with_cooldown", "pt_looters", villages_begin, ":num_villages", num_max_looters, bandit_respawn_cooldown_hours),
        (assign, ":spawned_party_id", reg0),
        (gt, ":spawned_party_id", 0),
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
         (spawn_around_party, ":party_no", "pt_deserters"),
         (assign, ":new_party", reg0),

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
          (val_min, ":max_number_to_add", num_max_deserter_party_size), #SB : keep deserter parties small
          (store_random_in_range, ":number_to_add", 10, ":max_number_to_add"),
         (party_add_members, ":new_party", ":tier_1_troop", ":number_to_add"),
         (store_random_in_range, ":random_no", 1, 4),
         (try_for_range, ":unused", 0, ":random_no"),
           (party_upgrade_with_xp, ":new_party", 1000000, 0),
         (try_end),
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
       # Pirate ships: ONE bandit type (combined cap), trickle respawn.
       # Shared next-spawn time tracked on pt_sea_raiders_ship's slot.
       (store_num_parties_of_template, ":n_sr", "pt_sea_raiders_ship"),
       (store_num_parties_of_template, ":n_co", "pt_corsair_ship"),
       (store_num_parties_of_template, ":n_pi", "pt_pirate_ship"),
       (store_add, ":total_ships", ":n_sr", ":n_co"),
       (val_add, ":total_ships", ":n_pi"),

       (try_begin),
         (lt, ":total_ships", num_max_pirate_ships),
         (party_template_get_slot, ":next_ship", "pt_sea_raiders_ship", slot_party_template_respawn_cooldown),
         (store_current_hours, ":cur_ship"),
         (try_begin),
           # initial seed: never spawned yet (slot == 0) -> fill straight to cap
           (eq, ":next_ship", 0),
           (assign, ":to_spawn", num_max_pirate_ships),
           (val_sub, ":to_spawn", ":total_ships"),
           (try_for_range, ":si", 0, ":to_spawn"),
             (call_script, "script_spawn_one_pirate_ship"),
           (try_end),
           (party_template_set_slot, "pt_sea_raiders_ship", slot_party_template_respawn_cooldown, ":cur_ship"),
         (else_try),
           # ongoing trickle: 1 ship per bandit_respawn_interval_hours
           (ge, ":cur_ship", ":next_ship"),
           (call_script, "script_spawn_one_pirate_ship"),
           (store_current_hours, ":cur2"),
           (val_add, ":cur2", bandit_respawn_interval_hours),
           (party_template_set_slot, "pt_sea_raiders_ship", slot_party_template_respawn_cooldown, ":cur2"),
         (try_end),
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
       (store_random_in_range, ":dest_port", "p_port_1", "p_ports_end"),
        (party_set_ai_object, ":party_no", ":dest_port"),
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

		(assign, ":center_too_close", 0),
		(try_for_range, ":center", centers_begin, centers_end),
			(eq, ":center_too_close", 0),
			(store_distance_to_party_from_party, ":distance", ":new_camp", ":center"),
			(lt, ":distance", 3),
			(assign, ":center_too_close", 1),
		(try_end),

		(try_begin),
			(eq, ":center_too_close", 0),
			(party_set_slot, ":new_camp", slot_party_template_lair_party, 2),
		(else_try),
			(remove_party, ":new_camp"),
			(party_template_set_slot, ":bandit_template", slot_party_template_lair_party, 0),
		(else_try),
		(try_end),
	(try_end),
     ]),

("spawn_party_type_with_cooldown",
  [
   (store_script_param, ":party_template", 1),
   (store_script_param, ":base_spawn_point", 2),
   (store_script_param, ":num_spawn_points", 3),
   (store_script_param, ":max_parties", 4),

   (assign, reg0, -1),
  (store_num_parties_of_template, ":num", ":party_template"),

  (try_begin),
    (lt, ":num", ":max_parties"),
    (party_template_get_slot, ":next", ":party_template", slot_party_template_respawn_cooldown),
    (store_current_hours, ":cur"),

    (try_begin),
      # initial seed: never spawned yet (slot == 0) -> fill straight to cap at once
      (eq, ":next", 0),
      (assign, ":to_spawn", ":max_parties"),
      (val_sub, ":to_spawn", ":num"),
      (try_for_range, ":i", 0, ":to_spawn"),
        (store_random, ":sp", ":num_spawn_points"),
        (val_add, ":sp", ":base_spawn_point"),
        (set_spawn_radius, 25),
        (spawn_around_party, ":sp", ":party_template"),
      (try_end),
      (party_template_set_slot, ":party_template", slot_party_template_respawn_cooldown, ":cur"),
    (else_try),
      # ongoing trickle: at most 1 party per bandit_respawn_interval_hours
      (ge, ":cur", ":next"),
      (store_random, ":sp", ":num_spawn_points"),
      (val_add, ":sp", ":base_spawn_point"),
      (set_spawn_radius, 25),
      (spawn_around_party, ":sp", ":party_template"),
      (store_current_hours, ":cur2"),
      (val_add, ":cur2", bandit_respawn_interval_hours),
      (party_template_set_slot, ":party_template", slot_party_template_respawn_cooldown, ":cur2"),
    (try_end),
  (try_end),
 ]),

#script_spawn_one_pirate_ship
# Spawns ONE ship of the currently least-represented pirate type and tags it.
("spawn_one_pirate_ship",
 [
  (store_num_parties_of_template, ":n_sr", "pt_sea_raiders_ship"),
  (store_num_parties_of_template, ":n_co", "pt_corsair_ship"),
  (store_num_parties_of_template, ":n_pi", "pt_pirate_ship"),
  (assign, ":spawn_tpl", "pt_sea_raiders_ship"),
  (assign, ":spawn_tag", 1),
  (assign, ":min_n", ":n_sr"),
  (try_begin),
    (lt, ":n_co", ":min_n"),
    (assign, ":spawn_tpl", "pt_corsair_ship"),
    (assign, ":spawn_tag", 2),
    (assign, ":min_n", ":n_co"),
  (try_end),
  (try_begin),
    (lt, ":n_pi", ":min_n"),
    (assign, ":spawn_tpl", "pt_pirate_ship"),
    (assign, ":spawn_tag", 4),
    (assign, ":min_n", ":n_pi"),
  (try_end),
  (try_begin),
    (eq, ":spawn_tpl", "pt_sea_raiders_ship"),
    (assign, ":spawn_point", "p_reserved_1"),
  (else_try),
    (eq, ":spawn_tpl", "pt_corsair_ship"),
    (assign, ":spawn_point", "p_reserved_3"),
  (else_try),
    (assign, ":spawn_point", "p_reserved_2"),
  (try_end),
  (set_spawn_radius, 25),
  (spawn_around_party, ":spawn_point", ":spawn_tpl"),
  (assign, ":party_no", reg0),
  (gt, ":party_no", 0),
  (party_set_slot, ":party_no", slot_party_ship_type, ":spawn_tag"),
 ]),

#script_get_spawn_report_line
# INPUT: arg1 = party_template, arg2 = max_parties (cap), arg3 = has_lair (1/0)
# OUTPUT: s0 = "<count>/<cap>  cd <hours>h  lair <0/1>"  (reg1..reg4 also set)
("get_spawn_report_line",
 [
  (store_script_param, ":party_template", 1),
  (store_script_param, ":cap", 2),
  (store_script_param, ":has_lair", 3),

  (store_num_parties_of_template, ":num", ":party_template"),

  (party_template_get_slot, ":cd", ":party_template", slot_party_template_respawn_cooldown),
  (val_max, ":cd", 0),
  (store_current_hours, ":cur_hours"),
  (store_sub, ":cd_left", ":cd", ":cur_hours"),
  (try_begin),
    (lt, ":cd_left", 0),
    (assign, ":cd_left", 0),
  (try_end),

  (assign, ":lair_active", 0),
  (try_begin),
    (eq, ":has_lair", 1),
    (party_template_get_slot, ":lair_party", ":party_template", slot_party_template_lair_party),
    (gt, ":lair_party", 1),
    (assign, ":lair_active", 1),
  (try_end),

   (assign, reg1, ":num"),
   (assign, reg2, ":cap"),
   (assign, reg3, ":cd_left"),
   (assign, reg4, ":lair_active"),
    (str_store_string, s0, "@{reg1}/{reg2}  cd {reg3}h  lair {reg4}"),
   ]),
]
