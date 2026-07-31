# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *

player_court_captured_simple_triggers = [
(3, #check to see if player's court has been captured
   [
     ##diplomacy start+ The player might be the ruler of another kingdom
     (assign, ":save_reg0", reg0),
	 (assign, ":alt_led_faction", "fac_player_supporters_faction"),
	 (try_begin),
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	    (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(assign, ":alt_led_faction", "$players_kingdom"),
	 (try_end),
	 ##diplomacy end+
     (try_begin), #The old court has been lost
     ##diplomacy begin
       (is_between, "$g_player_court", centers_begin, centers_end),
       (party_slot_eq, "$g_player_court", slot_village_infested_by_bandits, "trp_peasant_woman"),
       (call_script, "script_add_notification_menu", "mnu_notification_court_lost", 0, 0),
     (else_try),
     ##diplomacy end
       (is_between, "$g_player_court", centers_begin, centers_end),
       (store_faction_of_party, ":court_faction", "$g_player_court"),
       (neq, ":court_faction", "fac_player_supporters_faction"),
	   ##diplomacy start+ The player might be ruler of a faction other than fac_player_supporters_faction
	   (neq, ":court_faction", ":alt_led_faction"),
	   ##diplomacy end+
       (call_script, "script_add_notification_menu", "mnu_notification_court_lost", 0, 0),
     (else_try),	#At least one new court has been found
       (lt, "$g_player_court", centers_begin),
       #Will by definition not active until a center is taken by the player faction
       #Player minister must have been appointed at some point
       (this_or_next|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
		(gt, "$g_player_minister", 0),

       (assign, ":center_found", 0),
       (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
         (eq, ":center_found", 0),
         (store_faction_of_party, ":court_faction", ":walled_center"),
		   ##diplomacy start+ The player might be ruler of a faction other than fac_player_supporters_faction
		   (this_or_next|eq, ":court_faction", ":alt_led_faction"),
		   ##diplomacy end+
         (eq, ":court_faction", "fac_player_supporters_faction"),
         (assign, ":center_found", ":walled_center"),
       (try_end),
       (ge, ":center_found", 1),
       (call_script, "script_add_notification_menu", "mnu_notification_court_lost", 0, 0),
     (try_end),
    #Also, piggy-backing on this -- having bandits go to lairs and back
    (try_for_parties, ":party_no"),
      (gt, ":party_no", "p_spawn_points_end"),
      (party_is_active, ":party_no"),
      (party_get_template_id, ":party_template", ":party_no"),
      (try_begin),
        (is_between, ":party_template", bandit_party_templates_begin, bandit_party_templates_end), #SB : template range
        (party_template_get_slot, ":bandit_lair", ":party_template", slot_party_template_lair_party),
        (try_begin),#If party is active and bandit is far away, then move to location
          (gt, ":bandit_lair", "p_spawn_points_end"),
          (store_distance_to_party_from_party, ":distance", ":party_no", ":bandit_lair"), #this is the cause of the error
          (gt, ":distance", 30),
          #All this needs checking
          (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
          (party_get_position, pos5, ":bandit_lair"),
          (party_set_ai_target_position, ":party_no", pos5),
        (else_try), #Otherwise, act freely
          (get_party_ai_behavior, ":behavior", ":party_no"),
          (eq, ":behavior", ai_bhvr_travel_to_point),
          (try_begin),
            (gt, ":bandit_lair", "p_spawn_points_end"),
            (store_distance_to_party_from_party, ":distance", ":party_no", ":bandit_lair"),
            (lt, ":distance", 3),
            (party_set_ai_behavior, ":party_no", ai_bhvr_patrol_party),
            (party_template_get_slot, ":spawnpoint", ":party_template", slot_party_template_lair_spawnpoint),
            (is_between, ":spawnpoint", "p_steppe_bandit_spawn_point", "p_spawn_points_end"),
            (party_set_ai_object, ":party_no", ":spawnpoint"),
            (party_set_ai_patrol_radius, ":party_no", 45),
          (else_try), #why is this identical behavior?
            (lt, ":bandit_lair", "p_spawn_points_end"),
            (party_set_ai_behavior, ":party_no", ai_bhvr_patrol_party),
            (party_template_get_slot, ":spawnpoint", ":party_template", slot_party_template_lair_spawnpoint),
            (is_between, ":spawnpoint", "p_steppe_bandit_spawn_point", "p_spawn_points_end"),
            (party_set_ai_object, ":party_no", ":spawnpoint"),
            (party_set_ai_patrol_radius, ":party_no", 45),
          (try_end),
        (try_end),
      (else_try), #AC : merchant ship
        (eq, ":party_template", "pt_merchant_ship"),
        (party_is_in_any_town, ":party_no"),
        (party_get_cur_town, ":cur_town", ":party_no"),
        (store_random_in_range, ":dest_port", "p_port_1", "p_ports_end"),
        (neq, ":cur_town", ":dest_port"),
        (party_set_flags, ":party_no", pf_default_behavior, 0),
        (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
        (party_set_ai_object, ":party_no", ":dest_port"),
      (else_try), #SB : piggyback to handle reinforcements
        (this_or_next|eq, ":party_template", "pt_center_reinforcements"),
        (eq, ":party_template", "pt_routed_warriors"),
        (party_slot_eq, ":party_no", slot_party_type, spt_reinforcement),
         # (store_distance_to_party_from_party, ":distance", ":cur_center", ":party_no"),
        # (party_get_attached_to, ":cur_attached_town", ":party_no"),
        (party_get_cur_town, ":cur_attached_town", ":party_no"),
         # (this_or_next|lt, ":distance", 3),
        (try_begin),
          (eq, ":party_template", "pt_center_reinforcements"),
          (party_get_slot, ":destination", ":party_no", slot_party_ai_object),
          (neq, ":cur_attached_town", ":destination"),
          (assign, ":cur_attached_town", -1),
          (party_detach, ":party_no"),  # stop and detach
          (party_set_ai_behavior,":party_no",ai_bhvr_travel_to_party),
          (party_set_ai_object,":party_no", ":destination"),
          (party_set_flags, ":party_no", pf_default_behavior, 0),
        (try_end),
        (is_between, ":cur_attached_town", walled_centers_begin, walled_centers_end),
        # (eq, ":cur_attached_town", ":cur_center"),
        
        (try_begin), #weed out undesirables
          (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
          (store_faction_of_party, ":cur_faction", ":cur_attached_town"),
          (try_begin), #player culture
            (this_or_next|eq, ":cur_faction", "fac_player_faction"),
            (this_or_next|eq, ":cur_faction", "fac_player_supporters_faction"),
            (eq, ":cur_faction", "$players_kingdom"),
            (neg|is_between, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end),
            (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
            (assign, ":cur_faction", "$g_player_culture"),
          (try_end),
          (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":troop_no", ":party_no", ":stack_no"),
            (neg|troop_is_hero, ":troop_no"),
            (assign, ":cur_relation", 100),
            (try_begin), #routed parties sometimes contain extraneous units, players may also give random stuff to reinforcements
              (store_faction_of_troop, ":faction_no", ":troop_no"),
              (is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
              (store_relation, ":cur_relation", ":cur_faction", ":faction_no"),
            (try_end),
            (this_or_next|is_between, ":troop_no", "trp_looter", bandits_end), #looters are easy to route, don't let them rejoin
            (lt, ":cur_relation", 0),
            
            (party_stack_get_size, ":stack_size", ":party_no", ":stack_no"),
            (party_remove_members, ":party_no", ":troop_no", ":stack_size"),
            (party_add_prisoners, ":party_no", ":troop_no", ":stack_size"),
          (try_end),
        (try_end),
        (call_script, "script_party_add_party", ":cur_attached_town", ":party_no"),
         # (try_begin),
           # (eq, "$cheat_mode", 2),
           # (str_store_party_name, s1, ":party_no"),
           # (str_store_party_name_link, s2, ":cur_center"),
           # (display_log_message, "@active {s1} arrived at {s2}"),
         # (try_end),
        
        (try_begin), #unset slot before deallocating party
          (eq, ":party_template", "pt_center_reinforcements"),
          (party_get_slot, ":village", ":party_no", slot_party_home_center),
          (party_set_slot, ":village", slot_village_reinforcement_party, -1),
        (try_end),
        (party_detach, ":party_no"),
        (remove_party, ":party_no"),
      (try_end),
    (try_end),
     #Piggybacking on trigger:
     (try_begin),
       (troop_get_slot, ":betrothed", "trp_player", slot_troop_betrothed),
       (gt, ":betrothed", 0),
       (neg|check_quest_active, "qst_wed_betrothed"),
       (neg|check_quest_active, "qst_wed_betrothed_female"),
       (str_store_troop_name, s5, ":betrothed"),
       (display_message, "@Betrothal to {s5} expires"),
       (troop_set_slot, "trp_player", slot_troop_betrothed, -1),
       (troop_set_slot, ":betrothed", slot_troop_betrothed, -1),
     (try_end),
	 ##diplomacy start+
	 (assign, reg0, ":save_reg0"),#revert register
	 ##diplomacy end+
     ]),
]
