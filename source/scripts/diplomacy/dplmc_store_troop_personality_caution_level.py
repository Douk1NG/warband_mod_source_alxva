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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_store_troop_personality_caution_level_scripts = [
#"script_dplmc_store_troop_personality_caution_level"
#
# INPUT:
#   arg1 :troop_no
# OUTPUT:
#   reg0 -1 for aggressive
#         0 for neither
#         1 for cautious
("dplmc_store_troop_personality_caution_level", [
	#Used a number of places to determine whether a lord is cautious
	#or aggressive.  The standard is something like:
	#
	#For cautious:
	#(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
    #    (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
    #    (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
    #    (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
	#
	#For aggressive:
	#(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
    #    (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
    #    (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
	#
	#I've expanded this for companion/lady personalities.
	#The result can be either:
	# -1  =  aggressive
	#  0  =  neutral
	#  1  =  cautious
	(store_script_param_1, ":troop_no"),

	(try_begin),
		(neg|is_between, ":troop_no", heroes_begin, heroes_end),#The player or troops that don't have slot_lord_reputation_type
		(assign, reg0, 0),#neither cautious nor aggressive
	(else_try),
		(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_aristocratic),
		(lt, reg0, 0),#compliments when the player retreats
		(assign, reg0, 1),#cautious
	(else_try),
		(gt, reg0, 0),#complains when the player retreats
		(assign, reg0, -1),#aggressive
	(else_try),
		(troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
		(this_or_next|eq, ":reputation", lrep_adventurous),
		(this_or_next|eq, ":reputation", lrep_martial),
		(this_or_next|eq, ":reputation", lrep_quarrelsome),
			(eq, ":reputation", lrep_selfrighteous),
		(assign, reg0, -1),#aggressive
	(else_try),
		(this_or_next|ge, ":reputation", lrep_conventional),
		(this_or_next|eq, ":reputation", lrep_upstanding),
		(this_or_next|eq, ":reputation", lrep_debauched),
		(this_or_next|eq, ":reputation", lrep_goodnatured),
			(eq, ":reputation", lrep_cunning),
		(assign, reg0, 1),#cautious
	(else_try),
		(assign, reg0, 0),#neither cautious nor aggressive
	(try_end),
])
]
