# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

sneak_into_town_caught_ran_away_menu = [
(
    "sneak_into_town_caught_ran_away",0,
    "You make your way back through the gates and quickly retreat to the safety of the countryside.{s11}",
    "none",
    [

	(str_clear, s11),
	(assign, ":at_least_one_escaper_caught", 0),

	(assign, ":end_cond", kingdom_ladies_end),
	(try_for_range, ":prisoner", active_npcs_begin, ":end_cond"),
	  (try_begin),
        (troop_slot_eq, ":prisoner", slot_troop_mission_participation, mp_prison_break_escaped),
        (assign, "$talk_context", tc_hero_freed),
        (assign, reg14, ":prisoner"),
        (call_script, "script_setup_troop_meeting", ":prisoner", -1),
        (troop_set_slot, ":prisoner", slot_troop_mission_participation, -1),

        (troop_get_slot, ":prison_center", ":prisoner", slot_troop_prisoner_of_party),
        (party_remove_prisoners, ":prison_center", ":prisoner", 1),
        (troop_set_slot, ":prisoner", slot_troop_prisoner_of_party, -1),

        (assign, ":end_cond", -1), #maybe more than 1 should be able to escape?
	  (else_try),
		(troop_slot_eq, ":prisoner", slot_troop_mission_participation, mp_prison_break_caught),
		(str_store_troop_name, s12, ":prisoner"),
		(try_begin),
			(eq, ":at_least_one_escaper_caught", 0),
			(str_store_string, s11, "str_s11_unfortunately_s12_was_wounded_and_had_to_be_left_behind"),
		(else_try),
			(str_store_string, s11, "str_s11_also_s12_was_wounded_and_had_to_be_left_behind"),
		(try_end),
		(assign, ":at_least_one_escaper_caught", 1),
	  (try_end),

	  (troop_set_slot, ":prisoner", slot_troop_mission_participation, 0), #new
	(try_end),
	],
    [
      ("continue",[],"Continue...",
       [
           (assign,"$auto_menu",-1),
           (store_encountered_party,"$last_sneak_attempt_town"),
           (store_current_hours,"$last_sneak_attempt_time"),
           (change_screen_return),
        ]),
    ]
  )
]
