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

process_hero_ai_scripts = [
# script_process_hero_ai
# This is called more frequently than script_decide_kingdom_party_ais
#Handles sieges, raids, etc -- does not change the party's basic mission.
# Input: none
# Output: none
#called from triggers
("process_hero_ai",
    [
      (store_script_param_1, ":troop_no"),
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (try_begin),
        (party_is_active, ":party_no"),
        (store_faction_of_party, ":faction_no", ":party_no"),
        (party_get_slot, ":ai_state", ":party_no", slot_party_ai_state),
        (party_get_slot, ":ai_object", ":party_no", slot_party_ai_object),
        (try_begin),
          (eq, ":ai_state", spai_besieging_center),
          (try_begin),
            (party_slot_eq, ":ai_object", slot_center_is_besieged_by, -1),
            (store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
            (lt, ":distance", 3),
            (try_begin),
              (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
              (party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
              (party_set_slot, ":ai_object", slot_center_is_besieged_by, ":commander_party"),
            (else_try),
              (party_set_slot, ":ai_object", slot_center_is_besieged_by, ":party_no"),
            (try_end),
            (store_current_hours, ":cur_hours"),
            (party_set_slot, ":ai_object", slot_center_siege_begin_hours, ":cur_hours"),


            (try_begin),
              (store_faction_of_party, ":ai_object_faction", ":ai_object"),
				 ##diplomacy start+ Handle player is co-ruler of faction
				 (assign, ":is_coruler", 0),
				 (try_begin),
					(eq, ":ai_object_faction", "$players_kingdom"),
					(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
					(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
					(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
					(assign, ":is_coruler", 1),
				 (try_end),
				 (this_or_next|eq, ":is_coruler", 1),
				 ##diplomacy end+
              (this_or_next|party_slot_eq, ":ai_object", slot_town_lord, "trp_player"),
              (eq, ":ai_object_faction", "fac_player_supporters_faction"),
              (call_script, "script_add_notification_menu", "mnu_notification_center_under_siege", ":ai_object", ":troop_no"),
            (try_end),
            (str_store_party_name_link, s1, ":ai_object"),
            (str_store_troop_name_link, s2, ":troop_no"),
            (str_store_faction_name_link, s3, ":faction_no"),
            #SB : store color of center object
            (faction_get_color, ":color", ":ai_object_faction"),
            (display_log_message, "@{s1} has been besieged by {s2} of {s3}.", ":color"),
            (call_script, "script_village_set_state", ":ai_object", svs_under_siege),
            (assign, "$g_recalculate_ais", 1),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_raiding_around_center),
          (party_slot_eq, ":party_no", slot_party_ai_substate, 0),
          (assign, ":selected_village", 0),
          (try_for_range, ":enemy_village_no", villages_begin, villages_end),
            (eq, ":selected_village", 0),
            (store_faction_of_party, ":enemy_village_faction", ":enemy_village_no"),
            (try_begin),
              (party_slot_eq, ":enemy_village_no", slot_town_lord, "trp_player"),
              (store_relation, ":reln", "fac_player_supporters_faction", ":faction_no"),
            (else_try),
              (store_relation, ":reln", ":enemy_village_faction", ":faction_no"),
            (try_end),
            (lt, ":reln", 0),
            (store_distance_to_party_from_party, ":dist", ":enemy_village_no", ":party_no"),
            (lt, ":dist", 15),
            (party_slot_eq, ":enemy_village_no", slot_village_state, svs_normal), #village is not already raided
            #CHANGE STATE TO RAID THIS VILLAGE
            (assign, ":selected_village", ":enemy_village_no"),
          (try_end),
          (try_begin),
            (eq, ":selected_village", 0),
            (is_between, ":ai_object", villages_begin, villages_end),
            (assign, ":selected_village", ":ai_object"),
          (try_end),
          (try_begin),
            (gt, ":selected_village", 0),
            #SB : minimum of 15 in raiding party, although in process_village_raids we calculate actual ratio
            (party_get_num_companions, ":num_troops", ":party_no"),
            (ge, ":num_troops", 15), #about 2 party template of reinforcements
            (call_script, "script_party_set_ai_state", ":party_no", spai_raiding_around_center, ":selected_village"),
            (try_begin),
              (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
              (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
              (faction_set_slot, ":faction_no", slot_faction_ai_object, ":selected_village"),
            (try_end),
            (party_get_position, pos1, ":selected_village"),
            (map_get_random_position_around_position, pos2, pos1, 1),
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
            (party_set_ai_target_position, ":party_no", pos2),
            (party_set_ai_object, ":party_no", ":selected_village"),
            (party_set_slot, ":party_no", slot_party_ai_substate, 1),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_raiding_around_center),#substate is 1
          (try_begin),
            (store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
            (lt, ":distance", 2),
            (try_begin),
              (party_slot_eq, ":ai_object", slot_village_state, svs_normal),
              (call_script, "script_village_set_state", ":ai_object", svs_being_raided),
              (party_set_slot, ":ai_object", slot_village_raided_by, ":party_no"),
              (try_begin),
                (store_faction_of_party, ":village_faction", ":ai_object"),
				 ##diplomacy start+ Handle player is co-ruler of faction
				 (assign, ":is_coruler", 0),
				 (try_begin),
					(eq, ":village_faction", "$players_kingdom"),
					(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
					(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
					(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
					(assign, ":is_coruler", 1),
				 (try_end),
				 (this_or_next|eq, ":is_coruler", 1),
				 ##diplomacy end+
                (this_or_next|party_slot_eq, ":ai_object", slot_town_lord, "trp_player"),
                (eq, ":village_faction", "fac_player_supporters_faction"),
                (store_distance_to_party_from_party, ":dist", "p_main_party", ":ai_object"),
                (this_or_next|lt, ":dist", 30),
                (party_slot_eq, ":ai_object", slot_center_has_messenger_post, 1),
                (call_script, "script_add_notification_menu", "mnu_notification_village_raid_started", ":ai_object", ":troop_no"),
              (try_end),
            (else_try),
              (party_slot_eq, ":ai_object", slot_village_state, svs_being_raided),
            (else_try),
              #if anything other than being_raided leave
              (party_set_slot, ":party_no", slot_party_ai_substate, 0),
            (try_end),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_retreating_to_center),
          (try_begin),
            (party_get_battle_opponent, ":enemy_party", ":party_no"),
            (ge, ":enemy_party", 0), #we are in a battle! we may be caught in a loop!
            (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
            (party_set_slot, ":party_no", slot_party_commander_party, -1),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_patrolling_around_center),

          (try_begin),
            (party_slot_eq, ":party_no", slot_party_ai_substate, 0),
            (store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
            (lt, ":distance", 6),
            (party_set_slot, ":party_no", slot_party_ai_substate, 1),

	        (party_set_aggressiveness, ":party_no", 8),
	        (party_set_courage, ":party_no", 8),
	        (party_set_ai_initiative, ":party_no", 100),

            (party_set_ai_behavior, ":party_no", ai_bhvr_patrol_party),
            (party_set_ai_object, ":party_no", ":ai_object"),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_holding_center),
        (try_end),
      (try_end),
  ])
]
