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

assign_troop_love_interests_scripts = [
("assign_troop_love_interests", #Called at the beginning, or whenever a lord is spurned
    [
	(store_script_param, ":cur_troop", 1),
    ##diplomacy start+
	#wrap the entire thing in a try-statement: do nothing when called erroneously
	(assign, ":save_reg0", reg0),
	(assign, ":save_reg1", reg1),
	(try_begin),
	(this_or_next|is_between, ":cur_troop", lords_begin, lords_end),
	(this_or_next|is_between, ":cur_troop", companions_begin, companions_end),
	(troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),#kingdom heroes only
	(troop_slot_eq, ":cur_troop", slot_troop_spouse, -1),#not married, engaged
	(troop_slot_eq, ":cur_troop", slot_troop_betrothed, -1),

	#avoid unintentional erroneous pairings (intentional exceptions can be added)
	#(troop_get_type, ":troop_type", ":cur_troop"),
	(call_script, "script_dplmc_store_troop_is_female", ":cur_troop"),
	(assign, ":troop_type", reg0),

	(try_begin),
	    #Certain personality types don't care about flouting convention.
		(this_or_next|troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_debauched),
        (this_or_next|troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_roguish),
        (troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_adventurous),
		(assign, ":troop_type", abs(tf_male) + abs(tf_female) + 1),#guaranteed not to equal tf_male or tf_female
	(try_end),
	(store_faction_of_troop, ":troop_faction", ":cur_troop"),
	#assign default initial courtships for companions
	(try_begin),
		(is_between, ":cur_troop", companions_begin, companions_end),
        (troop_get_slot, ":cur_lady", ":cur_troop", slot_troop_personalitymatch_object),
        (is_between, ":cur_lady", heroes_begin, heroes_end),

		(store_faction_of_troop, ":lady_faction", ":cur_lady"),
		(eq, ":troop_faction", ":lady_faction"),
		#(call_script, "script_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
		(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
		(lt, reg0, 2),#check not a close relative
        #(troop_get_type, reg0, ":cur_lady"),
		(call_script, "script_dplmc_store_troop_is_female", ":cur_lady"),
        (neq, ":troop_type", reg0),#check gender compatability
		(neq, ":cur_lady", ":cur_troop"),#check not yourself
		(neg|troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_retirement),#check in the game and not retired, exiled, dead, etc.
		(troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_kingdom_hero),
		(call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":cur_lady"),
		(ge, reg0, 0), #do not develop love interest if already spurned (but DO allow re-courting)

		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
		(try_begin),
		    (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, -1),
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(else_try),
		    (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, -1),
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(else_try),
		    (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, -1),
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
		(try_end),
    (try_end),
    ##diplomacy end+
	(try_for_range, ":unused", 0, 50),
		(store_random_in_range, ":cur_lady", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_slot_eq, ":cur_lady", slot_troop_spouse, -1),
		(store_faction_of_troop, ":lady_faction", ":cur_lady"),
		(eq, ":troop_faction", ":lady_faction"),
		##diplomacy start+
		##(call_script, "script_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
        (call_script, "script_dplmc_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
		#(eq, reg0, 0),
		#right now nothing gives a value of 1, but change this check in case more distant relations are reported
		(lt, reg0, 2),#check not a close relative
		#(troop_get_type, reg0, ":cur_lady"),
		(call_script, "script_dplmc_store_troop_is_female", ":cur_lady"),
        (neq, ":troop_type", reg0),#check gender compatability
		(neq, ":cur_lady", ":cur_troop"),#check not yourself
		(neg|troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_retirement),#check in the game and not retired, exiled, dead, etc.
		(troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_kingdom_hero),
        ##diplomacy end+
		(call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":cur_lady"),

		(eq, reg0, 0), #do not develop love interest if already spurned or courted

		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
	##diplomacy start+ also allow -1 to signify no-one courted
		(try_begin),
			(this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, -1),#< added
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(else_try),
			(this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, -1),#< added
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(else_try),
			(this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, -1),#< added
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
		(try_end),
	(try_end),
        (try_end),
	(assign, reg1, ":save_reg1"),
	(assign, reg0, ":save_reg0"),#revert register
	##diplomacy end+
	])
]
