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

cf_troop_get_romantic_attraction_to_troop_scripts = [
("cf_troop_get_romantic_attraction_to_troop", #source is lady, target is man
    [

	(store_script_param, ":source_lady", 1),
	(store_script_param, ":target_lord", 2),

	(assign, ":weighted_romantic_assessment", 0),
    ##diplomacy start+
	(assign, ":save_reg1", reg1),
	#Use gender script
	#(troop_get_type, ":source_is_female", ":source_lady"),
	#(eq, ":source_is_female", 1),
	#(troop_get_type, ":target_is_female", ":target_lord"),
	#(eq, ":target_is_female", 0),
	(call_script, "script_dplmc_store_is_female_troop_1_troop_2", ":source_lady", ":target_lord"),
	(assign, ":source_is_female", reg0),
	(assign, ":target_is_female", reg1),
	(assign, reg1, ":save_reg1"),
    #(assign, reg0, -15), #dckplmc
	(neq, ":source_is_female", ":target_is_female"),
	##diplomacy end+

	(call_script, "script_troop_get_romantic_chemistry_with_troop", ":source_lady", ":target_lord"),
	(assign, ":romantic_chemistry", reg0),


	#objective attraction - average renown
	(troop_get_slot, ":modified_renown", ":target_lord", slot_troop_renown),
	(assign, ":lady_status", 60),
   ##diplomacy start+ adjust status based on who they are
	(try_begin),
      #The renown bonus is decreased the more important the lady's relatives are.
      (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
      (troop_get_slot, ":best_renown", ":source_lady", slot_troop_renown),
      (try_begin),
        (troop_get_slot, ":relative", ":source_lady", slot_troop_father),
        (ge, ":relative", 0),
        (troop_get_slot, ":other_renown", ":relative", slot_troop_renown),
        (val_max, ":best_renown", ":other_renown"),
   	(try_end),
   	(try_begin),
		  (troop_get_slot, ":relative", ":source_lady", slot_troop_guardian),
        (ge, ":relative", 0),
        (troop_get_slot, ":other_renown", ":relative", slot_troop_renown),
        (val_max, ":best_renown", ":other_renown"),
   	(try_end),
   	(try_begin),
		  (troop_get_slot, ":relative", ":source_lady", slot_troop_mother),
        (ge, ":relative", 0),
        (troop_get_slot, ":other_renown", ":relative", slot_troop_renown),
        (val_max, ":best_renown", ":other_renown"),
   	(try_end),
   	(try_begin),
		  (ge, ":best_renown", 600),
        (store_div, ":lady_status", ":best_renown", 10),
   	(else_try),
		  (lt, ":best_renown", 400),
        (store_div, ":lady_status", ":best_renown", 10),
		  (val_add, ":lady_status", 20),
   	(try_end),
   	(val_clamp, ":lady_status", 30, 90),
   (try_end),
   ##diplomacy end+
	(val_div, ":modified_renown", 5),
	(val_sub, ":modified_renown", ":lady_status"),
	(val_min, ":modified_renown", 60),



	#weight values
	(try_begin),
		(assign, ":personality_match", 0),
		(call_script, "script_cf_test_lord_incompatibility_to_s17", ":source_lady", ":target_lord"),
		(store_sub, ":personality_match", 0, reg0),
	(try_end),

	(troop_get_slot, ":lady_reputation", ":source_lady", slot_lord_reputation_type),
	(try_begin),
		(eq, ":lady_reputation", lrep_ambitious),
		(val_mul, ":modified_renown", 2),
		(val_div, ":romantic_chemistry", 2),
	(else_try),
		(eq, ":lady_reputation", lrep_otherworldly),
		(val_div, ":modified_renown", 2),
		(val_mul, ":romantic_chemistry", 2),
	(else_try),
		(eq, ":lady_reputation", lrep_adventurous),
		(val_div, ":modified_renown", 2),
	(else_try),
		(eq, ":lady_reputation", lrep_moralist),
		(val_div, ":modified_renown", 2),
		(val_div, ":romantic_chemistry", 2),
	(try_end),

	(val_add, ":weighted_romantic_assessment", ":romantic_chemistry"),
	(val_add, ":weighted_romantic_assessment", ":personality_match"),
	(val_add, ":weighted_romantic_assessment", ":modified_renown"),

	(assign, reg0, ":weighted_romantic_assessment"),

	])
]
