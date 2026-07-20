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

process_alarms_scripts = [
("process_alarms",
    [
      (assign, ":current_modula", "$g_alarm_modula"),
      (val_add, "$g_alarm_modula", 1),
      (try_begin),
        (eq, "$g_alarm_modula", 3),
        (assign, "$g_alarm_modula", 0),
      (try_end),

      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_mod, ":center_modula", ":center_no", 3),
        (eq, ":center_modula", ":current_modula"),

        (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
        (party_set_slot, ":center_no", slot_center_sortie_strength, 0),
        (party_set_slot, ":center_no", slot_center_sortie_enemy_strength, 0),

        (assign, ":spotting_range", 3),
        (try_begin),
          (is_currently_night),
          (assign, ":spotting_range", 2),
        (try_end),

        (try_begin),
          (party_slot_eq, ":center_no", slot_center_has_watch_tower, 1),
          (val_mul, ":spotting_range", 2),
        (else_try),
          (neg|is_between, ":center_no", villages_begin, villages_end),
          (val_add, ":spotting_range", 1),
          (val_mul, ":spotting_range", 2),
        (try_end),

        (store_faction_of_party, ":center_faction", ":center_no"),

        (try_for_parties, ":party_no"),
          (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
          (eq, ":party_no", "p_main_party"),

          (store_faction_of_party, ":party_faction", ":party_no"),

          (try_begin),
            (eq, ":party_no", "p_main_party"),
            (assign, ":party_faction", "$players_kingdom"),
          (try_end),

          (try_begin),
            (eq, ":party_faction", ":center_faction"),

            (store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
            (le, ":distance", ":spotting_range"),

            (party_get_slot, ":cached_strength", ":party_no", slot_party_cached_strength),
            (party_get_slot, ":sortie_strength", ":center_no", slot_center_sortie_strength),
            (val_add, ":sortie_strength", ":cached_strength"),
            (party_set_slot, ":center_no", slot_center_sortie_strength, ":sortie_strength"),
          (else_try),
            (neq, ":party_faction", ":center_faction"),

            (store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),

			(try_begin),
				(lt, ":distance", 10),
				(store_current_hours, ":hours"),
				(store_sub, ":faction_recce_slot", ":party_faction", kingdoms_begin),
				(val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
				(party_set_slot, ":center_no", ":faction_recce_slot", ":hours"),

				#(eq, "$cheat_mode", 1),
				#(str_store_faction_name, s4, ":party_faction"),
				#(str_store_party_name, s5, ":center_no"),
				#(display_message, "@{!}DEBUG -- {s4} reconnoiters {s5}"),
			(try_end),

		    (store_relation, ":reln", ":center_faction", ":party_faction"),
            (lt, ":reln", 0),
			(try_begin),
	            (le, ":distance", ":spotting_range"),

	            (party_get_slot, ":cached_strength", ":party_no", slot_party_cached_strength),
	            (party_get_slot, ":enemy_strength", ":center_no", slot_center_sortie_enemy_strength),
	            (val_add, ":enemy_strength", ":cached_strength"),
	            (party_set_slot, ":center_no", slot_center_sortie_enemy_strength, ":enemy_strength"),
	            (party_set_slot, ":center_no", slot_center_last_spotted_enemy, ":party_no"),
			(try_end),

          (try_end),
        (try_end),
      (try_end),

      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_mod, ":center_modula", ":center_no", 3),
        (eq, ":center_modula", ":current_modula"),

        (try_begin), #eligible units sortie out of castle
          (is_between, ":center_no", walled_centers_begin, walled_centers_end),
          (party_slot_ge, ":center_no", slot_center_last_spotted_enemy, 0),

          (party_get_slot, ":sortie_strength", ":center_no", slot_center_sortie_strength),
          (party_get_slot, ":enemy_strength", ":center_no", slot_center_sortie_enemy_strength),

          #Below two lines are new added by ozan. While AI want to drive nearby besieging enemy parties by making sortie them, they give up current battle if they are already joining one.
          #Lets assume there is a battle inside the castle, because enemies are inside castle and they are so close to castle they will be also added to slot_center_sortie_enemy_strength
          #But in this scenario, they are not outside the castle, so searching/patrolling enemy outside the castle is useless at this point.
          #So if there is already a battle inside the center, do not sortie and search enemy outside.
          (party_get_battle_opponent, ":center_battle_opponent", ":center_no"),
          (try_begin),
		    (ge, "$cheat_mode", 1),
            (ge, ":center_battle_opponent", 0),
            (str_store_party_name, s7, ":center_no"),
            (str_store_party_name, s6, ":center_battle_opponent"),
            (display_message, "@{!}DEBUG : There are already enemies ({s6}) inside {s7}."),
          (try_end),
          (lt, ":center_battle_opponent", 0),
          #New added by ozan ended.

          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_party_name, s4, ":center_no"),
            (assign, reg3, ":sortie_strength"),
            (assign, reg4, ":enemy_strength"),
            (display_message, "@{!}DEBUG -- Calculating_sortie for {s4} strength of {reg3} vs {reg4} enemies"),
          (try_end),

          (store_mul, ":enemy_strength_mul_14_div_10", ":enemy_strength", 14),
          (val_div, ":enemy_strength_mul_14_div_10", 10),
          (gt, ":sortie_strength", ":enemy_strength_mul_14_div_10"),

          (assign, ":at_least_one_party_sorties", 0),
          (try_for_parties, ":sortie_party"),
            (party_get_attached_to, ":town", ":sortie_party"),
            (eq, ":town", ":center_no"),

            (party_slot_eq, ":sortie_party", slot_party_type, spt_kingdom_hero_party),

            (party_get_slot, ":cached_strength", ":sortie_party", slot_party_cached_strength),
            (ge, ":cached_strength", 100),

            (party_detach, ":sortie_party"),
            (call_script, "script_party_set_ai_state", ":sortie_party",  spai_patrolling_around_center, ":center_no"),

            (try_begin),
              (eq, "$cheat_mode", 1),
              (str_store_party_name, s4, ":sortie_party"),
              (display_message, "str_s4_sorties"),
            (try_end),

            (eq, ":at_least_one_party_sorties", 0),
            (assign, ":at_least_one_party_sorties", ":sortie_party"),
          (try_end),

          (try_begin),
            (party_is_in_town, "p_main_party", ":center_no"),
			(eq, "$g_player_is_captive", 0),
            (gt, ":at_least_one_party_sorties", 0),
            (call_script, "script_add_notification_menu", "mnu_notification_sortie_possible", ":center_no", ":sortie_party"),
          (try_end),
		(try_end),

		(store_faction_of_party, ":center_faction", ":center_no"),

		#Send message
		(this_or_next|eq, "$cheat_mode", 1), #this is message
		(this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
		(eq, ":center_faction", "$players_kingdom"),

		(party_get_slot, ":enemy_party", ":center_no", slot_center_last_spotted_enemy),
		(ge, ":enemy_party", 0),
		(store_distance_to_party_from_party, ":dist", "p_main_party", ":center_no"),
		(assign, ":has_messenger", 0),
		(try_begin),
		 ##diplomacy start+ Handle player is co-ruler of faction
		 (assign, ":is_coruler", 0),
		 (try_begin),
			(eq, ":center_faction", "$players_kingdom"),
			(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":is_coruler", 1),
		 (try_end),
		 (this_or_next|eq, ":is_coruler", 1),
		 ##diplomacy end+
		  (this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
		  (eq, ":center_faction", "fac_player_supporters_faction"),
		  (party_slot_eq, ":center_no", slot_center_has_messenger_post, 1),
		  (assign, ":has_messenger", 1),
		(try_end),

		(this_or_next|eq, "$cheat_mode", 1),
		(this_or_next|lt, ":dist", 30),
			(eq, ":has_messenger", 1),

		(str_store_party_name_link, s1, ":center_no"),
        (party_get_slot, ":exact_enemy_strength", ":center_no", slot_center_sortie_enemy_strength),

		(try_begin),
			(lt, ":exact_enemy_strength", 500),
			(display_message, "@Small bands of enemies spotted near {s1}."),
		(else_try),
			(lt, ":exact_enemy_strength", 1000),
			(display_message, "@Enemy patrols spotted near {s1}."),
		(else_try),
			(lt, ":exact_enemy_strength", 2000),
			(display_message, "@Medium-sized group of enemies spotted near {s1}."),
		(else_try),
			(lt, ":exact_enemy_strength", 4000),
			(display_message, "@Significant group of enemies spotted near {s1}."),
		(else_try),
			(lt, ":exact_enemy_strength", 8000),
			(display_message, "@Army of enemies spotted near {s1}."),
		(else_try),
			(lt, ":exact_enemy_strength", 16000),
			(display_message, "@Large army of enemies spotted near {s1}."),
		(else_try),
			(display_message, "@Great host of enemies spotted near {s1}."),
		(try_end),
		#maybe do audio sound?

      (try_end),
     ])
]
