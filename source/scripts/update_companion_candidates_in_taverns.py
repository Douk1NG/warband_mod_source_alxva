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

update_companion_candidates_in_taverns_scripts = [
#script_update_companion_candidates_in_taverns
# INPUT: none
# OUTPUT: none
("update_companion_candidates_in_taverns",
    [
      (try_begin),
        (eq, "$cheat_mode", 1),
        (display_message, "str_shuffling_companion_locations"),
      (try_end),

      (try_for_range, ":troop_no", companions_begin, companions_end),
	    ##diplomacy start+ Move this *after* the checks!
        #  (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
		##diplomacy end+
        (troop_slot_eq, ":troop_no", slot_troop_days_on_mission, 0),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),

        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
		##diplomacy start+
		(troop_get_slot, ":town_no", ":troop_no", slot_troop_cur_center),
		(try_begin),
			(is_between, ":town_no", towns_begin, towns_end),
			(party_get_slot, ":town_lord", ":town_no", slot_town_lord),
			##zerilius changes begin
			##bug fix for red text
			(ge, ":town_lord", 0),
			##zerilius changes end
			(this_or_next|eq, ":town_lord", "trp_player"),
			(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),
				(troop_slot_eq, ":town_lord", slot_troop_spouse, "trp_player"),
		(else_try),
			#Moved from above:
			(troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
		(try_end),
		(neg|troop_slot_ge, ":troop_no", slot_troop_cur_center, 1),
		##diplomacy end+
        (store_random_in_range, ":town_no", towns_begin, towns_end),
        (try_begin),
		  ##diplomacy start+ Remove the "you can't go home again" condition if the player owns the town
		  (assign, ":veto", 0),
		  (try_begin),
			(store_faction_of_party, ":town_faction", ":town_no"),
			(eq, ":town_faction", "fac_player_supporters_faction"),
		  (else_try),
			(party_get_slot, ":town_lord", ":town_no", slot_town_lord),
			(ge, ":town_lord", 0),
			(this_or_next|eq, ":town_lord", "trp_player"),
			(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),
				(troop_slot_eq, ":town_lord", slot_troop_spouse, "trp_player"),
		  (else_try),
			#Native veto:
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_home, ":town_no"),
				(troop_slot_eq, ":troop_no", slot_troop_first_encountered, ":town_no"),
			(assign, ":veto", 1),
		  (try_end),
		  (eq, ":veto", 0),
                  ##diplomacy end+
          (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_troop_name, 4, ":troop_no"),
            (str_store_party_name, 5, ":town_no"),
            (display_message, "@{!}{s4} is in {s5}"),
          (try_end),
        (try_end),
      (try_end),
     ])
]
