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

party_commander_error_check_simple_triggers = [
(2, #Error check for multiple parties on the map
	[
	(eq, "$cheat_mode", 1),
	(assign, ":debug_menu_noted", 0),
	(try_for_parties, ":party_no"),
		(gt, ":party_no", "p_spawn_points_end"),
		(party_stack_get_troop_id, ":commander", ":party_no", 0),
		##diplomacy start+
		(is_between, ":commander", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":commander", slot_troop_occupation, slto_kingdom_hero),
		##diplomacy end+
		(is_between, ":commander", active_npcs_begin, active_npcs_end),
		(troop_get_slot, ":commander_party", ":commander", slot_troop_leaded_party),
        (str_store_troop_name, s3, ":commander"),
        (try_begin),
          (neq, ":party_no", ":commander_party"),
          (assign, reg4, ":party_no"),
          (assign, reg5, ":commander_party"),

          (display_message, "@{!}{s3} commander of party #{reg4} which is not his troop_leaded party {reg5}"),
          ##diplomacy start+ Make it clear what the error was
          (try_begin),
            (gt, reg4, 0),
            (gt, reg5, 0),
            (str_store_party_name, s3, reg4),
            (str_store_party_name, s65, reg5),
            (display_message, "@{!} Commanded party #{reg4} is {s3}, troop_leaded party #{reg5} is {s65}"),
            (str_store_troop_name, s3, ":commander"),
          (try_end),
          ##diplomacy end+
          (str_store_string, s65, "str_party_with_commander_mismatch__check_log_for_details_"),
        # (else_try), #SB : piggyback to check lord wealth
          # (troop_get_slot, reg3, ":commander", slot_troop_wealth),
          # (le, reg3, 0),
          # (party_get_cur_town, ":town_no", ":party_no"),
          # (try_begin),
            # (is_between, ":town_no", centers_begin, centers_end),
            # (str_store_party_name_link, s2, ":town_no"),
          # (else_try),
            # (str_store_string, s2, "@large"),
          # (try_end),
          # (str_store_string, s65, "@{s3} is bankrupt ({reg3} denars) while at {s2}!"),
        # (try_end),

		# (try_begin),
			(eq, ":debug_menu_noted", 0),
			(call_script, "script_add_notification_menu", "mnu_debug_alert_from_s65", 0, 0),
			(assign, ":debug_menu_noted", 1),
		(try_end),
	(try_end),
	]),
]
