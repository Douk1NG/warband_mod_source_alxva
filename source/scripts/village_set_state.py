# ======================================================================
# SHARED DEPENDENCY
# Entity: village_set_state (script)
# Called by menus in 3 domains: cheats, diplomacy, village
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

village_set_state_scripts = [
# script_village_set_state
# Input: arg1 = center_no arg2:new_state
# Output: reg0: food consumption (1 food item counts as 100 units)
("village_set_state",
    [
      (store_script_param_1, ":village_no"),
      (store_script_param_2, ":new_state"),
      ##diplomacy start+
      (store_current_hours, ":hours"),
      (party_get_slot, ":attacker_party", ":village_no", slot_village_raided_by),
      (try_begin),
        (ge, ":attacker_party", 0),
        (party_is_active, ":attacker_party"),#added 2011-06-07
        (party_stack_get_troop_id, ":attack_leader", ":attacker_party", 0),
        (ge, ":attack_leader", 0),
        (party_set_slot, ":village_no", dplmc_slot_center_last_attacked_time, ":hours"),
        (party_set_slot, ":village_no", dplmc_slot_center_last_attacker, ":attack_leader"),


        (try_begin),
          (this_or_next|eq, ":new_state", svs_looted),
          (eq, ":new_state", svs_deserted),
          #SB : there's a fire whether real or fake, we set the bounding center to have guards investigate
          (try_begin),
            (party_get_slot, ":bound_center", ":village_no", slot_village_bound_center),
            (is_between, ":bound_center", centers_begin, centers_end),
            (party_set_slot, ":bound_center", slot_town_last_nearby_fire_time, ":hours"),
          (try_end),
          #SB : quest state
          (try_begin),
            (check_quest_active, "qst_hunt_down_fugitive"),
            (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, ":village_no"),
            #if we found and knocked him out in mission template this won't fire
            (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
            (neg|check_quest_failed, "qst_hunt_down_fugitive"),
            (quest_set_slot, "qst_hunt_down_fugitive", slot_quest_current_state, 3),
            (try_begin), #conclude quest if village raided
              (neq, ":attacker_party", "p_main_party"),
              (call_script, "script_conclude_quest", "qst_hunt_down_fugitive"),
            (else_try), #player raided village for some reason
              (call_script, "script_succeed_quest", "qst_hunt_down_fugitive"),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
      ##diplomacy end+

      (try_begin),
        (eq, ":new_state", svs_normal),
        (party_set_extra_text, ":village_no", "str_empty_string"),
        #SB : redo village recruits immediately
        (try_begin),
          (this_or_next|le, ":attacker_party", 0),
          (neg|party_is_active, ":attacker_party"),
          (is_between, ":village_no", villages_begin, villages_end), #dckplmc
          (call_script, "script_update_volunteer_troops_in_village", ":village_no"),
          (call_script, "script_update_npc_volunteer_troops_in_village", ":village_no"),
        (try_end),
        (party_set_slot, ":village_no", slot_village_raided_by, -1),
      (else_try),
        (eq, ":new_state", svs_being_raided),
        (party_set_extra_text, ":village_no", "@(Being Raided)"),
      (else_try), #SB : deserted state as alternative to full looting
        (eq, ":new_state", svs_deserted),
        (party_set_extra_text, ":village_no", "@(Deserted)"),

        (party_set_slot, ":village_no", slot_village_raided_by, -1),
        (call_script, "script_change_center_prosperity", ":village_no", -20),
		(val_add, "$newglob_total_prosperity_from_villageloot", -20),
      (else_try),
        (eq, ":new_state", svs_looted),
        (party_set_extra_text, ":village_no", "@(Looted)"),

        (party_set_slot, ":village_no", slot_village_raided_by, -1),
        (call_script, "script_change_center_prosperity", ":village_no", -60),
		(val_add, "$newglob_total_prosperity_from_villageloot", -60),

		# (try_begin), #optional - lowers the relationship between a lord and his liege if his fief is looted
			# (eq, 5, 0),
			# (party_get_slot, ":town_lord", ":village_no", slot_town_lord),
			# (is_between, ":town_lord", active_npcs_begin, active_npcs_end),
			# (store_faction_of_troop, ":town_lord_faction", ":town_lord"),
			# (faction_get_slot, ":faction_leader", ":town_lord_faction", slot_faction_leader),
			# (call_script, "script_troop_change_relation_with_troop", ":town_lord", ":faction_leader", -1),
			# (val_add, "$total_battle_ally_changes", -1),
		# (try_end),
      (else_try),
        (eq, ":new_state", svs_under_siege),
        (party_set_extra_text, ":village_no", "@(Under Siege)"),

		#Divert all caravans heading to the center
		#Note that occasionally, no alternative center will be found. In that case, the caravan will try to run the blockade
		(try_for_parties, ":party_no"),
			(gt, ":party_no", "p_spawn_points_end"),
			(party_slot_eq, ":party_no", slot_party_type, spt_kingdom_caravan),
            (party_slot_eq, ":party_no", slot_party_ai_object, ":village_no"),

			(party_get_slot, ":origin", ":party_no", slot_party_last_traded_center),
			(store_faction_of_party, ":merchant_faction", ":party_no"),
            ##diplomacy start+ added new third parameter, the caravan party itself
            (call_script, "script_cf_select_most_profitable_town_at_peace_with_faction_in_trade_route", ":origin", ":merchant_faction",":party_no"),
			##diplomacy end+
            (assign, ":target_center", reg0),
			(is_between, ":target_center", centers_begin, centers_end),

            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":party_no", ":target_center"),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
            (party_set_slot, ":party_no", slot_party_ai_state, spai_trading_with_town),
            (party_set_slot, ":party_no", slot_party_ai_object, ":target_center"),
		(try_end),
      (try_end),
      (party_set_slot, ":village_no", slot_village_state, ":new_state"),
  ])
]
