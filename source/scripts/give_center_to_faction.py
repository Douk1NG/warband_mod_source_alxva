# ======================================================================
# SHARED DEPENDENCY
# Entity: give_center_to_faction (script)
# Called by menus in 2 domains: castle, diplomacy
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

give_center_to_faction_scripts = [
##
##  # script_cf_get_party_leader
##  # Input: arg1 = party_no
##  # Output: reg0 = troop_no of the leader (Can fail)
##  ("cf_get_party_leader",
##    [
##      (store_script_param_1, ":party_no"),
##
##      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
##      (gt, ":num_stacks", 0),
##      (party_stack_get_troop_id, ":stack_troop", ":party_no", 0),
##      (troop_is_hero, ":stack_troop"),
##      (assign, reg0, ":stack_troop"),
##  ]),
# script_give_center_to_faction
# Input: arg1 = center_no, arg2 = faction
("give_center_to_faction",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":faction_no"),

      ##diplomacy begin
      (party_set_slot, ":center_no", dplmc_slot_center_taxation, 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
        (party_set_slot, ":center_no", slot_village_infested_by_bandits, 0),
      (try_end),
      (try_begin),
        (eq, "$g_constable_training_center", ":center_no"),
        (assign, "$g_constable_training_center", -1),
      (try_end),
      ##diplomacy end
      (try_begin),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (faction_get_slot, ":player_faction_king", "fac_player_supporters_faction", slot_faction_leader),
        (eq, ":player_faction_king", "trp_player"),

        (try_begin),
          (is_between, ":center_no", walled_centers_begin, walled_centers_end),
          (assign, ":number_of_walled_centers_players_kingdom_has", 1),
        (else_try),
          (assign, ":number_of_walled_centers_players_kingdom_has", 0),
        (try_end),

        (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
          (store_faction_of_party, ":owner_faction_no", ":walled_center"),
          (eq, ":owner_faction_no", "fac_player_supporters_faction"),
          (val_add, ":number_of_walled_centers_players_kingdom_has", 1),
        (try_end),

        (ge, ":number_of_walled_centers_players_kingdom_has", 10),
        (unlock_achievement, ACHIEVEMENT_VICTUM_SEQUENS),
      (try_end),

      (try_begin),
        (check_quest_active, "qst_join_siege_with_army"),
        (quest_slot_eq, "qst_join_siege_with_army", slot_quest_target_center, ":center_no"),
        (call_script, "script_abort_quest", "qst_join_siege_with_army", 0),
        #Reactivating follow army quest
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (str_store_troop_name_link, s9, ":faction_marshall"),
        (setup_quest_text, "qst_follow_army"),
        (str_store_string, s2, "@{s9} wants you to resume following his army until further notice."),
        (call_script, "script_start_quest", "qst_follow_army", ":faction_marshall"),
        (assign, "$g_player_follow_army_warnings", 0),
      (try_end),

      #(store_faction_of_party, ":old_faction", ":center_no"),
      (call_script, "script_give_center_to_faction_aux", ":center_no", ":faction_no"),
      (call_script, "script_update_village_market_towns"),

      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (call_script, "script_faction_recalculate_strength", ":cur_faction"),
      (try_end),
      (assign, "$g_recalculate_ais", 1),

	  (try_begin),
        (eq, ":faction_no", "fac_player_supporters_faction"),
		(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
		(call_script, "script_activate_player_faction", "trp_player"),
	  (try_end),

      #(call_script, "script_activate_deactivate_player_faction", ":old_faction"),
      #(try_begin),
      #(eq, ":faction_no", "fac_player_supporters_faction"),
      #(faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
      #(call_script, "script_give_center_to_lord", ":center_no", "trp_player", 0),

      #check with Armagan -- what is this here for?
      #(try_for_range, ":cur_village", villages_begin, villages_end),
      #(store_faction_of_party, ":cur_village_faction", ":cur_village"),
      #(eq, ":cur_village_faction", "fac_player_supporters_faction"),
      #(neg|party_slot_eq, ":cur_village", slot_town_lord, "trp_player"),
      #(call_script, "script_give_center_to_lord", ":cur_village", "trp_player", 0),
      #(try_end),
      #(try_end),
    ])
]
