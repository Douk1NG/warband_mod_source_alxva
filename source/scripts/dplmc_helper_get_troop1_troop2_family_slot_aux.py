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

dplmc_helper_get_troop1_troop2_family_slot_aux_scripts = [
##"script_cf_dplmc_faction_has_bias_against_gender"
##
## Helper function that does something specific that I want in
## script_dplmc_troop_get_family_relation_to_troop.
##
## Gets the slot value, but for troops that aren't trp_player
## and are not within (heroes_begin, heroes_end), values of "0"
## are transformed to -1.  Also gives a result of -1 (instead of
## an error) for negative troop IDs, which is what I want in
## this situation (otherwise I'd be explicitly checking this and
## setting the result to -1 if it was bad).
##
## Also, values equal to "active_npcs_including_player_begin" are
## transformed to "trp_player" (i.e. 0), to allow storing that
## value.
##
##INPUT:  arg1   :troop_1
##        arg2   :troop_2
##        arg3   :slot_no
##
##OUTPUT: reg0   value of slot for troop_1, or -1
##        reg1   value of slot for troop_2, or -1
("dplmc_helper_get_troop1_troop2_family_slot_aux",
	[
		(store_script_param, ":troop_1", 1),
		(store_script_param, ":troop_2", 2),
		(store_script_param, ":slot_no", 3),

		#(1) Get the value for the first troop into reg0
		(try_begin),
			#Negative numbers are placeholders for invalid family members
			(lt, ":troop_1", 0),
			(assign, reg0, -1),
		(else_try),
			#For active_npcs_including_player_begin, use the family slot from trp_player
			(eq, ":troop_1", active_npcs_including_player_begin),
			(troop_get_slot, reg0, "trp_player", ":slot_no"),
		(else_try),
			#Otherwise get the family member slot
			(troop_get_slot, reg0, ":troop_1", ":slot_no"),
			#However, for non-heroes, the memory might not be initialized,
			#so don't take a value of 0 at face-value.
			(eq, reg0, 0),
			(neg|is_between, ":troop_1", heroes_begin, heroes_end),
			(neq, ":troop_1", "trp_player"),
			(assign, reg0, -1),
		(try_end),

		#Translate from active_npcs_including_player_begin to trp_player
		(try_begin),
			(eq, reg0, active_npcs_including_player_begin),
			(assign, reg0, "trp_player"),
		(try_end),

		#(2) Get the value for the second troop into reg1
		(try_begin),
			#Negative numbers are placeholders for invalid family members
			(lt, ":troop_2", 0),
			(assign, reg1, -1),
		(else_try),
			#For active_npcs_including_player_begin, use the family slot from trp_player
			(eq, ":troop_2", active_npcs_including_player_begin),
			(troop_get_slot, reg1, "trp_player", ":slot_no"),
		(else_try),
			#Otherwise get the family member slot
			(troop_get_slot, reg1, ":troop_2", ":slot_no"),
			#However, for non-heroes, the memory might not be initialized,
			#so don't take a value of 0 at face-value.
			(eq, reg1, 0),
			(neg|is_between, ":troop_2", heroes_begin, heroes_end),
			(neq, ":troop_2", "trp_player"),
			(assign, reg1, -1),
		(try_end),

		#Translate from active_npcs_including_player_begin to trp_player
		(try_begin),
			(eq, reg1, active_npcs_including_player_begin),
			(assign, reg1, "trp_player"),
		(try_end),
	])
]
