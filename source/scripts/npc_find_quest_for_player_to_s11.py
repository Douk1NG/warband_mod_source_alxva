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

npc_find_quest_for_player_to_s11_scripts = [
("npc_find_quest_for_player_to_s11",
  [
  (store_script_param, ":faction", 1),

  (assign, ":quest_giver_found", -1),
  (try_for_range, ":quest_giver", active_npcs_begin, mayors_end),
    (eq, ":quest_giver_found", -1),

	(neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":quest_giver"),

	(gt, ":quest_giver", "$g_troop_list_no"),

	(assign, "$g_troop_list_no", ":quest_giver"),

	(this_or_next|troop_slot_eq, ":quest_giver", slot_troop_occupation, slto_kingdom_hero),
		(is_between, ":quest_giver", mayors_begin, mayors_end),

	(neg|troop_slot_ge, ":quest_giver", slot_troop_prisoner_of_party, centers_begin),

	(try_begin),
		(is_between, ":quest_giver", mayors_begin, mayors_end),
		(assign, ":quest_giver_faction", -1),
		(try_for_range,":town", towns_begin, towns_end),
			(party_slot_eq, ":town", slot_town_elder, ":quest_giver"),
			(store_faction_of_party, ":quest_giver_faction", ":town"),
		(try_end),
	(else_try),
		(store_faction_of_troop, ":quest_giver_faction", ":quest_giver"),
	(try_end),
	(eq, ":faction", ":quest_giver_faction"),

	(call_script, "script_get_dynamic_quest", ":quest_giver"),
    (gt, reg0, -1),

    (assign, ":quest_giver_found", ":quest_giver"),
	(try_begin),
          (eq, "$cheat_mode", 1),
	  (str_store_troop_name, s4, ":quest_giver_found"),
	  (display_message, "str_test_diagnostic_quest_found_for_s4"),
        (try_end),

  (try_end),

  (assign, reg0, ":quest_giver_found"),

    ])
]
