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

dplmc_player_center_surrender_scripts = [
("dplmc_player_center_surrender",
  [
    (store_script_param, ":center_no", 1),

    #protect player for 24 hours
    (store_current_hours,":protected_until"),
    (val_add, ":protected_until", 48),
    (party_get_slot, ":besieger", ":center_no", slot_center_is_besieged_by),
    (store_faction_of_party, ":besieger_faction",":besieger"),
    ##nested diplomacy start+
    #In this version this variable currently isn't used for anything
    #(party_stack_get_troop_id, ":enemy_party_leader", ":besieger", 0),
    ##nested diplomacy end+

    (party_set_slot,":besieger",slot_party_ignore_player_until,":protected_until"),
    (party_ignore_player, ":besieger", 48),
	##nested diplomacy start+
	#Add support for promoted kingdom ladies
    #(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
	(try_for_range, ":lord", heroes_begin, heroes_end),
	  (this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
	  (troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
	##nested diplomacy end+
      (store_faction_of_troop, ":lord_faction", ":lord"),
      (eq, ":lord_faction", ":besieger_faction"),
      (troop_get_slot, ":led_party", ":lord", slot_troop_leaded_party),
      (party_is_active, ":led_party"),

      (party_slot_eq, ":led_party", slot_party_ai_state, spai_accompanying_army),
      (party_slot_eq, ":led_party", slot_party_ai_object, ":besieger"),

      (party_is_active, ":besieger"),
      (store_distance_to_party_from_party, ":distance_to_marshal", ":led_party", ":besieger"),
      (lt, ":distance_to_marshal", 20),

      (party_set_slot,":led_party",slot_party_ignore_player_until,":protected_until"),
      (party_ignore_player, ":led_party", 48),
    (try_end),

    (party_set_faction,"$current_town","fac_neutral"), #temporarily erase faction so that it is not the closest town
    (party_get_num_attached_parties, ":num_attached_parties_to_castle",":center_no"),
    (try_for_range_backwards, ":iap", 0, ":num_attached_parties_to_castle"),
      (party_get_attached_party_with_rank, ":attached_party", ":center_no", ":iap"),
      (party_detach, ":attached_party"),
      (party_get_slot, ":attached_party_type", ":attached_party", slot_party_type),
      (eq, ":attached_party_type", spt_kingdom_hero_party),
      (neq, ":attached_party_type", "p_main_party"),
      (store_faction_of_party, ":attached_party_faction", ":attached_party"),
      (call_script, "script_get_closest_walled_center_of_faction", ":attached_party", ":attached_party_faction"),
      (try_begin),
        (gt, reg0, 0),
        (call_script, "script_party_set_ai_state", ":attached_party", spai_holding_center, reg0),
      (else_try),
        (call_script, "script_party_set_ai_state", ":attached_party", spai_patrolling_around_center, ":center_no"),
      (try_end),
    (try_end),
    (call_script, "script_party_remove_all_companions", ":center_no"),
    (change_screen_return),
    (party_collect_attachments_to_party, ":center_no", "p_collective_enemy"), #recalculate so that
    (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"), #leaving troops will not be considered as captured

	##nested diplomacy start+
	#Anyone who lost a fief due to your surrender will be irritated
	(try_for_range, ":village_no", centers_begin, centers_end),
       (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
	   (party_get_slot, ":village_lord", ":village_no", slot_town_lord),
	   (neq, ":village_lord", "trp_player"),
	   (is_between, ":village_lord", heroes_begin, heroes_end),
	   (call_script, "script_change_player_relation_with_troop", ":village_lord", -1),
    (try_end),
	##nested diplomacy end+
    ##diplomacy
    (call_script, "script_give_center_to_faction", "$current_town", ":besieger_faction"),
    (call_script, "script_order_best_besieger_party_to_guard_center", ":center_no", ":besieger_faction"),

    #relation and controversy
    ##nested diplomacy start+, There should be no relation bonus with the enemy lord
    #(call_script, "script_change_player_relation_with_troop", ":enemy_party_leader", 2),
    ##nested diplomacy end+
    (try_begin),
      (gt, "$players_kingdom", 0),
      (neq, "$players_kingdom", "fac_player_supporters_faction"),
      (neq, "$players_kingdom", "fac_player_faction"),
      (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
  	  ##diplomacy start+
	  ##OLD:
      #(neq, ":faction_leader", "trp_player"),
	  ##NEW:
	  #Also guard against faction leader being some invalid negative number
	  (gt, ":faction_leader", "trp_player"),
	  ##diplomacy end+
      (call_script, "script_change_player_relation_with_troop", ":faction_leader", -2),
    (try_end),

  	(troop_get_slot, ":controversy", "trp_player", slot_troop_controversy),
  	(val_add, ":controversy", 4),
  	(val_min, ":controversy", 100),
  	(troop_set_slot, "trp_player", slot_troop_controversy, ":controversy"),
    ##nested diplmacy start+ add garrison to fief
    #The average # of troops added by script_cf_reinforce_party is 11.5.
    (assign, ":garrison_strength", 3),#easy: 34.5 for a castle
    (try_begin),
       (party_slot_eq, ":center_no", slot_party_type, spt_town),
       (assign, ":garrison_strength", 9),#easy: 103.5 for a town
    (try_end),
    #Take into account campaign difficulty.
    (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
    (try_begin),
       (eq, ":reduce_campaign_ai", 0), #hard 166% + 3 waves
       (val_mul, ":garrison_strength", 5),
       (val_div, ":garrison_strength", 3),
       (val_add, ":garrison_strength", 3),
    (else_try),
       (eq, ":reduce_campaign_ai", 1), #moderate 166%
       (val_mul, ":garrison_strength", 5),
       (val_div, ":garrison_strength", 3),
    #(else_try),
    #   (eq, ":reduce_campaign_ai", 2), #easy 100%
    #   (store_mul, ":garrison_strength", 1),
    (try_end),

    (try_for_range, ":unused", 0, ":garrison_strength"),
       (call_script, "script_cf_reinforce_party", ":center_no"),
    (try_end),
    (try_for_range, ":unused", 0, 7),# ADD some XP initially
       (store_mul, ":xp_range_min", 150, ":garrison_strength"),
       (store_mul, ":xp_range_max", 200, ":garrison_strength"),
       (store_random_in_range, ":xp", ":xp_range_min", ":xp_range_max"),
       (party_upgrade_with_xp, ":center_no", ":xp", 0),
    (try_end),
    ##nested diplomacy end+
  ])
]
