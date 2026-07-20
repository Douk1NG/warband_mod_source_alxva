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

cf_troop_can_intrigue_scripts = [
("cf_troop_can_intrigue",
	#This script should be called from dialogs, and also prior to any event which might result in a lord changing sides
    [
      (store_script_param, ":troop", 1),
      (store_script_param, ":skip_player_party", 2),

		##diplomacy start+
		#Use this to filter out lords who are supposed to be "off the board"
		(assign, ":bad_occupation", 0),
		(try_begin),
		   (gt, ":troop", 0),
			(troop_is_hero, ":troop"),
		   (troop_slot_eq, ":troop", slot_lord_reputation_type, dplmc_slto_dead),
		   (assign, ":bad_occupation", 1),#altered 2011-06-08
		(try_end),
		(eq, ":bad_occupation", 0),
		##diplomacy end+

      (troop_get_slot, ":led_party_1", ":troop", slot_troop_leaded_party),
      (party_is_active, ":led_party_1"),

      (try_begin),
        (eq, "$cheat_mode", 1),
        (eq, ":troop", "$g_talk_troop"),
        (display_message, "str_intrigue_test_troop_party_is_active"),
      (try_end),

      (party_get_battle_opponent, ":battle_opponent", ":led_party_1"),
      (le, ":battle_opponent", 0), #battle opponent can be 0 for an attached party?

      (try_begin),
        (eq, "$cheat_mode", 1),
        (eq, ":troop", "$g_talk_troop"),
        (display_message, "str_intrigue_test_troop_party_is_not_in_battle"),
      (try_end),

      (troop_slot_eq, ":troop", slot_troop_prisoner_of_party, -1),

      (try_begin),
        (eq, "$cheat_mode", 1),
        (eq, ":troop", "$g_talk_troop"),
        (display_message, "str_intrigue_test_troop_is_not_prisoner"),
      (try_end),

      (party_get_attached_to, ":led_party_1_attached", ":led_party_1"),

      (store_faction_of_party, ":led_party_1_faction", ":led_party_1"),

      (assign, ":other_lords_nearby", 0),
      (try_for_range, ":troop_2", active_npcs_begin, active_npcs_end),
        (neq, ":troop", ":troop_2"),
        (eq, ":other_lords_nearby", 0),

        (troop_slot_eq, ":troop_2", slot_troop_occupation, slto_kingdom_hero),

        (troop_get_slot, ":led_party_2", ":troop_2", slot_troop_leaded_party),
        (party_is_active, ":led_party_2"),
        (neq, ":led_party_1", ":led_party_2"),

        (store_faction_of_party, ":led_party_2_faction", ":led_party_2"),
        (eq, ":led_party_1_faction", ":led_party_2_faction"),

        (try_begin),
          (eq, ":led_party_1_attached", -1),
          (store_distance_to_party_from_party, ":distance", ":led_party_1", ":led_party_2"),
          (lt, ":distance", 3),
          (assign, ":other_lords_nearby", 1),
        (else_try),
          (is_between, ":led_party_1_attached", walled_centers_begin, walled_centers_end),
          (party_get_attached_to, ":led_party_2_attached", ":led_party_2"),
          (eq, ":led_party_1_attached", ":led_party_2_attached"),
          (assign, ":other_lords_nearby", 1),
        (try_end),
      (try_end),

      (try_begin),
        (eq, "$cheat_mode", 1),
        (eq, ":troop", "$g_talk_troop"),
        (display_message, "str_intrigue_test_troop_is_nearby"),
      (try_end),

      (try_begin),
        (eq, ":skip_player_party", 0),
        #temporary spot
      (try_end),

      (eq, ":other_lords_nearby", 0),
	])
]
