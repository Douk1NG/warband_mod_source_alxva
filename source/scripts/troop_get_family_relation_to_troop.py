# ======================================================================
# SHARED DEPENDENCY
# Entity: troop_get_family_relation_to_troop (script)
# Called by menus in 4 domains: castle, notifications, town, village
# ======================================================================

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

troop_get_family_relation_to_troop_scripts = [
# script_write_family_relation_as_s3s_s2_to_s4
# Inputs: arg1 = troop_no, arg2 = family_no (valid slot no after slot_troop_family_begin)
# Outputs: s11 = what troop_1 is to troop_2, reg0 = strength of relationship. Normally, "$g_talk_troop" should be troop_2
("troop_get_family_relation_to_troop",
    [
    (store_script_param_1, ":troop_1"),
    (store_script_param_2, ":troop_2"),

    ##diplomacy start+ use gender script
    #(troop_get_type, ":gender_1", ":troop_1"),
	(call_script, "script_dplmc_store_troop_is_female", ":troop_1"),
	(assign, ":gender_1", reg0),
	##diplomacy end+
	(assign, ":relation_strength", 0),

    (troop_get_slot, ":spouse_of_1", ":troop_1", slot_troop_spouse),
    (troop_get_slot, ":spouse_of_2", ":troop_2", slot_troop_spouse),

	(try_begin),
		(gt, ":spouse_of_1", -1),
		(troop_get_slot, ":father_of_spouse_of_1", ":spouse_of_1", slot_troop_father),
	(else_try),
		(assign, ":father_of_spouse_of_1", -1),
	(try_end),

	(try_begin),
		(gt, ":spouse_of_2", -1),
		(troop_get_slot, ":father_of_spouse_of_2", ":spouse_of_2", slot_troop_father),
	(else_try),
		(assign, ":father_of_spouse_of_2", -1),
	(try_end),

	(try_begin),
		(gt, ":spouse_of_2", -1),
		(troop_get_slot, ":mother_of_spouse_of_2", ":spouse_of_2", slot_troop_mother),
	(else_try),
		(assign, ":mother_of_spouse_of_2", -1),
	(try_end),

    (troop_get_slot, ":father_of_1", ":troop_1", slot_troop_father),
    (troop_get_slot, ":father_of_2", ":troop_2", slot_troop_father),

	#For the sake of simplicity, we can assume that all male aristocrats in prior generations either married commoners or procured their brides from the Old Country, thus discounting intermarriage
    (troop_get_slot, ":mother_of_1", ":troop_1", slot_troop_mother),
    (troop_get_slot, ":mother_of_2", ":troop_2", slot_troop_mother),

    ##diplomacy start+
	#Fix a native bug where daughters are their own mothers
        #(fixed in this mod, but still affects old saved games)
        #REMOVED - Instead this occurs once in simple triggers

	##Adding paternal grandmother (begin mostly-unaltered section)
	(try_begin),
		(this_or_next|eq, ":father_of_1", "trp_player"),#dplmc+ added
		(is_between, ":father_of_1", companions_begin, kingdom_ladies_end),
		(troop_get_slot, ":paternal_grandfather_of_1", ":father_of_1", slot_troop_father),
		(troop_get_slot, ":paternal_grandmother_of_1", ":father_of_1", slot_troop_mother),#added
	(else_try),
		(assign, ":paternal_grandfather_of_1", -1),
		(assign, ":paternal_grandmother_of_1", -1),#added
	(try_end),

	(try_begin),
		(this_or_next|eq, ":father_of_2", "trp_player"),#dplmc+ added
		(is_between, ":father_of_2", companions_begin, kingdom_ladies_end),
		(troop_get_slot, ":paternal_grandfather_of_2", ":father_of_2", slot_troop_father),
		(troop_get_slot, ":paternal_grandmother_of_2", ":father_of_2", slot_troop_mother),#added
	(else_try),
		(assign, ":paternal_grandfather_of_2", -1),
		(assign, ":paternal_grandmother_of_2", -1),#added
	(try_end),
	#(end mostly-unaltered section)

	##Adding maternal grandfather and maternal grandmother
	(try_begin),
		(this_or_next|eq, ":mother_of_1", "trp_player"),#dplmc+ added
		(is_between, ":mother_of_1", companions_begin, kingdom_ladies_end),
		(troop_get_slot, ":maternal_grandfather_of_1", ":mother_of_1", slot_troop_father),
		(troop_get_slot, ":maternal_grandmother_of_1", ":mother_of_1", slot_troop_mother),
	(else_try),
		(assign, ":maternal_grandfather_of_1", -1),
		(assign, ":maternal_grandmother_of_1", -1),
	(try_end),

	(try_begin),
		(this_or_next|eq, ":mother_of_2", "trp_player"),#dplmc+ added
		(is_between, ":mother_of_2", companions_begin, kingdom_ladies_end),
		(troop_get_slot, ":maternal_grandfather_of_2", ":mother_of_2", slot_troop_father),
		(troop_get_slot, ":maternal_grandmother_of_2", ":mother_of_2", slot_troop_mother),
	(else_try),
		(assign, ":maternal_grandfather_of_2", -1),
		(assign, ":maternal_grandmother_of_2", -1),
	(try_end),
	##diplomacy end+

    (troop_get_slot, ":guardian_of_1", ":troop_1", slot_troop_guardian),
    (troop_get_slot, ":guardian_of_2", ":troop_2", slot_troop_guardian),

	(str_store_string, s11, "str_no_relation"),

	(try_begin),
	  (eq, ":troop_1", ":troop_2"),
	  #self
	(else_try),
	  ##diplomacy start+
      (this_or_next|eq, ":spouse_of_2", ":troop_1"),#polygamy helper
	  ##diplomacy end+
	  (eq, ":spouse_of_1", ":troop_2"),
	  (assign, ":relation_strength", 20),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_wife"),
	  (else_try),
	    (str_store_string, s11, "str_husband"),
	  (try_end),
	(else_try),
	  (eq, ":father_of_2", ":troop_1"),
	  (assign, ":relation_strength", 15),
	  (str_store_string, s11, "str_father"),
	(else_try),
	  (eq, ":mother_of_2", ":troop_1"),
	  (assign, ":relation_strength", 15),
	  (str_store_string, s11, "str_mother"),
	(else_try),
	  (this_or_next|eq, ":father_of_1", ":troop_2"),
	  (eq, ":mother_of_1", ":troop_2"),
	  (assign, ":relation_strength", 15),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_daughter"),
	  (else_try),
	    (str_store_string, s11, "str_son"),
	  (try_end),
	##diplomacy start+
	(else_try),
	   #Check for half-siblings: sharing a father
	   (neq, ":father_of_1", -1),
	   (eq, ":father_of_1", ":father_of_2"),
	   (neq, ":mother_of_1", ":mother_of_2"),
	   (assign, ":relation_strength", 10),
	   (try_begin),
	     (eq, ":gender_1", tf_female),
	     (str_store_string, s11, "str_dplmc_half_sister"),
	   (else_try),
	     (str_store_string, s11, "str_dplmc_half_brother"),
	   (try_end),
   (else_try),
	   #Check for half-siblings: sharing a mother
	   (neq, ":mother_of_1", -1),
	   (eq, ":mother_of_1", ":mother_of_2"),
	   (neq, ":father_of_1", ":father_of_2"),
	   (assign, ":relation_strength", 10),
	   (try_begin),
	     (eq, ":gender_1", tf_female),
	     (str_store_string, s11, "str_dplmc_half_sister"),
	   (else_try),
	     (str_store_string, s11, "str_dplmc_half_brother"),
	   (try_end),
	##diplomacy end+
	(else_try),
	  #(gt, ":father_of_1", -1), #necessary, as some lords do not have the father registered #dplmc+ replaced
	  (neq, ":father_of_1", -1), #dplmc+ added
	  (eq, ":father_of_1", ":father_of_2"),
	  (assign, ":relation_strength", 10),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_sister"),
	  (else_try),
	    (str_store_string, s11, "str_brother"),
	  (try_end),
	(else_try),
	  (eq, ":guardian_of_2", ":troop_1"),
	  (assign, ":relation_strength", 10),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_sister"),
	  (else_try),
	    (str_store_string, s11, "str_brother"),
	  (try_end),
	(else_try),
	  (eq, ":guardian_of_1", ":troop_2"),
	  (assign, ":relation_strength", 10),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_sister"),
	  (else_try),
	    (str_store_string, s11, "str_brother"),
	  (try_end),
	##diplomacy start+
    (else_try),#polygamy, between two people married to the same person
	   (neq, ":spouse_of_1", -1),
	   (eq, ":spouse_of_2", ":spouse_of_1"),
	   (assign, ":relation_strength", 10),
	   (try_begin),
	      (eq, ":gender_1", tf_female),
	      (str_store_string, s11, "str_dplmc_sister_wife"),
	   (else_try),
	      (str_store_string, s11, "str_dplmc_co_husband"),
	   (try_end),
	##diplomacy end+
	(else_try),
	  #(gt, ":paternal_grandfather_of_1", -1),#dplmc+ replaced
	  (neq, ":father_of_2", -1),#dplmc+ added
	  (this_or_next|eq, ":maternal_grandfather_of_1", ":father_of_2"),#dplmc+ added
	  (eq, ":paternal_grandfather_of_1", ":father_of_2"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_niece"),
	  (else_try),
	    (str_store_string, s11, "str_nephew"),
	  (try_end),
	##diplomacy start+: add niece/nephew through mother
	(else_try),
	  (neq, ":mother_of_2", -1),
  	  (this_or_next|eq, ":maternal_grandmother_of_1", ":mother_of_2"),
	  (eq, ":paternal_grandmother_of_1", ":mother_of_2"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_niece"),
	  (else_try),
	    (str_store_string, s11, "str_nephew"),
	  (try_end),
	##diplomacy end+
	(else_try), #specifically aunt and uncle by blood -- i assume that in a medieval society with lots of internal family conflicts, they would not include aunts and uncles by marriage
	  #(gt, ":paternal_grandfather_of_2", -1),#dplmc+ replaced
	  (neq, ":father_of_1", -1),#dplmc+ added
	  (this_or_next|eq, ":maternal_grandfather_of_2", ":father_of_1"),#dplmc+ added
	  (eq, ":paternal_grandfather_of_2", ":father_of_1"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_aunt"),
	  (else_try),
	    (str_store_string, s11, "str_uncle"),
	  (try_end),
	##diplomacy start+
	#blood uncles & blood aunts, continued (via mother)
	(else_try),
	  (neq, ":mother_of_1", -1),
	  (this_or_next|eq, ":maternal_grandmother_of_2", ":mother_of_1"),
	  (eq, ":paternal_grandmother_of_2", ":mother_of_1"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_aunt"),
	  (else_try),
	    (str_store_string, s11, "str_uncle"),
	  (try_end),
	##diplomacy end+
	(else_try),
	  #(gt, ":paternal_grandfather_of_1", 0),#dplmc+ replaced (why was this one "gt 0" but the previous "gt -1"?)
	  (neq, ":paternal_grandfather_of_1", -1),#dplmc+ added
	  (this_or_next|eq, ":maternal_grandfather_of_2", ":paternal_grandfather_of_1"),#dplmc+ added
	  (eq, ":paternal_grandfather_of_2", ":paternal_grandfather_of_1"),
	  (assign, ":relation_strength", 2),
	  (str_store_string, s11, "str_cousin"),
	##diplomacy start+
	#Add cousin via paternal grandmother or maternal grandparents
	(else_try),
	  (neq, ":maternal_grandfather_of_1", -1),
	  (this_or_next|eq, ":maternal_grandfather_of_2", ":maternal_grandfather_of_1"),
	  (eq, ":paternal_grandfather_of_2", ":maternal_grandfather_of_1"),
	  (assign, ":relation_strength", 2),
	  (str_store_string, s11, "str_cousin"),
	(else_try),
	  (neq, ":paternal_grandmother_of_1", -1),
	  (this_or_next|eq, ":maternal_grandmother_of_2", ":paternal_grandmother_of_1"),
	  (eq, ":paternal_grandmother_of_2", ":paternal_grandmother_of_1"),
	  (assign, ":relation_strength", 2),
	  (str_store_string, s11, "str_cousin"),
	(else_try),
	  (neq, ":maternal_grandmother_of_1", -1),
	  (this_or_next|eq, ":maternal_grandmother_of_2", ":maternal_grandmother_of_1"),
	  (eq, ":paternal_grandmother_of_2", ":maternal_grandmother_of_1"),
	  (assign, ":relation_strength", 2),
	  (str_store_string, s11, "str_cousin"),
	##diplomacy end+
   	(else_try),
   	  (eq, ":father_of_spouse_of_1", ":troop_2"),
   	  (assign, ":relation_strength", 5),
   	  (try_begin),
   	    (eq, ":gender_1", tf_female),
   	    (str_store_string, s11, "str_daughterinlaw"),
   	  (else_try),
   	    (str_store_string, s11, "str_soninlaw"),
   	  (try_end),
	(else_try),
	  (eq, ":father_of_spouse_of_2", ":troop_1"),
	  (assign, ":relation_strength", 5),
	  (str_store_string, s11, "str_fatherinlaw"),
	(else_try),
	  (eq, ":mother_of_spouse_of_2", ":troop_1"),
	  (neq, ":mother_of_spouse_of_2", "trp_player"), #May be necessary if mother for troops not set to -1
	  (assign, ":relation_strength", 5),
	  (str_store_string, s11, "str_motherinlaw"),

	(else_try),
	  #(gt, ":father_of_spouse_of_1", -1), #necessary #dplmc+ replaced
	  (neq, ":father_of_spouse_of_1", -1), #dplmc+ added
	  (eq, ":father_of_spouse_of_1", ":father_of_2"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_sisterinlaw"),
	  (else_try),
	    (str_store_string, s11, "str_brotherinlaw"),
	  (try_end),
	(else_try),
	  #(gt, ":father_of_spouse_of_2", -1), #necessary #dplmc+ replaced
	  (neq, ":father_of_spouse_of_2", -1), #dplmc+ added
	  (eq, ":father_of_spouse_of_2", ":father_of_1"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_sisterinlaw"),
	  (else_try),
	    (str_store_string, s11, "str_brotherinlaw"),
	  (try_end),
	(else_try),
#	  (gt, ":spouse_of_2", -1), #necessary to avoid bug #dplmc+ replaced
	  (neq, ":spouse_of_2", -1), #dplmc+ added
	  (troop_slot_eq, ":spouse_of_2", slot_troop_guardian, ":troop_1"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    #(eq, ":gender_1", tf_female),#dplmc+ replaced
	    (eq, ":gender_1", tf_female),#dplmc+ added
	    (str_store_string, s11, "str_sisterinlaw"),
	  (else_try),
	    (str_store_string, s11, "str_brotherinlaw"),
	  (try_end),
	(else_try),
	  #(gt, ":spouse_of_1", -1), #necessary to avoid bug #dplmc+ replaced
	  (neq, ":spouse_of_1", -1), #dplmc+ added
	  (troop_slot_eq, ":spouse_of_1", slot_troop_guardian, ":troop_2"),
	  (assign, ":relation_strength", 5),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_sisterinlaw"),
	  (else_try),
	    (str_store_string, s11, "str_brotherinlaw"),
	  (try_end),
	(else_try),
	  #grandchild
	  (neq, ":troop_2", -1),
	   (this_or_next|eq, ":paternal_grandfather_of_1", ":troop_2"),
	   (this_or_next|eq, ":maternal_grandfather_of_1", ":troop_2"),
	   (this_or_next|eq, ":paternal_grandmother_of_1", ":troop_2"),
		   (eq, ":maternal_grandmother_of_1", ":troop_2"),
	   (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_dplmc_granddaughter"),
	  (else_try),
	    (str_store_string, s11, "str_dplmc_grandson"),
	  (try_end),
	(else_try),
	   #grandparent
	   (neq, ":troop_1", -1),
	   (this_or_next|eq, ":paternal_grandfather_of_2", ":troop_1"),
	   (this_or_next|eq, ":maternal_grandfather_of_2", ":troop_1"),
	   (this_or_next|eq, ":paternal_grandmother_of_2", ":troop_1"),
		   (eq, ":maternal_grandmother_of_2", ":troop_1"),
	  (assign, ":relation_strength", 4),
	  (try_begin),
	    (eq, ":gender_1", tf_female),
	    (str_store_string, s11, "str_dplmc_grandmother"),
	  (else_try),
	    (str_store_string, s11, "str_dplmc_grandfather"),
	  (try_end),
	(try_end),

	##diplomacy start+
	##Add relations for rulers not already encoded
	(try_begin),
		(eq, ":relation_strength", 0),
		(neq, ":troop_1", ":troop_2"),
		(try_begin),
			#Lady Isolla of Suno's father King Esterich was King Harlaus's cousin,
			#making them first cousins once removed.  Assign a weight of "1"
			#to this (for reference, the lowest value normally given in Native is 2).
			(this_or_next|eq, ":troop_1", "trp_kingdom_1_lord"),
			    (eq, ":troop_1", "trp_kingdom_1_pretender"),
			(this_or_next|eq, ":troop_2", "trp_kingdom_1_lord"),
			    (eq, ":troop_2", "trp_kingdom_1_pretender"),
			(assign, ":relation_strength", 1),
			(str_store_string, s11, "str_cousin"),
		(else_try),
			#Prince Valdym's uncle was Regent Burelek, father of King Yaroglek,
			#making the two of them first cousins.
			(this_or_next|eq, ":troop_1", "trp_kingdom_2_lord"),
			    (eq, ":troop_1", "trp_kingdom_2_pretender"),
			(this_or_next|eq, ":troop_2", "trp_kingdom_2_lord"),
				(eq, ":troop_2", "trp_kingdom_2_pretender"),
			(assign, ":relation_strength", 2),
			(str_store_string, s11, "str_cousin"),
		(else_try),
			#Sanjar Khan and Dustum Khan were both sons of Janakir Khan
			#(although by different mothers) making them half-brothers.
			(this_or_next|eq, ":troop_1", "trp_kingdom_3_lord"),
			    (eq, ":troop_1", "trp_kingdom_3_pretender"),
			(this_or_next|eq, ":troop_2", "trp_kingdom_3_lord"),
				(eq, ":troop_2", "trp_kingdom_3_pretender"),
			(assign, ":relation_strength", 10),
			(str_store_string, s11, "str_dplmc_half_brother"),
			#Adjust their parentage to make this work automatically
			(try_begin),
		      	(troop_slot_eq, ":troop_1", slot_troop_father, -1),
				(troop_slot_eq, ":troop_2", slot_troop_father, -1),
				#Set their "father" slot to a number guaranteed not to have spurious collisions
				(store_mul, ":janakir_khan", "trp_kingdom_3_lord", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),#defined in module_constants.py
				(val_add, ":janakir_khan", DPLMC_VIRTUAL_RELATIVE_FATHER_OFFSET),#defined in module_constants.py
				(troop_set_slot, ":troop_1", slot_troop_father, ":janakir_khan"),
				(troop_set_slot, ":troop_2", slot_troop_father, ":janakir_khan"),
				#Differentiate their mothers, so they are half-brothers instead of full-brothers
				(try_begin),
					(troop_slot_eq, ":troop_1", slot_troop_mother, -1),
					(store_mul, reg0, ":troop_1", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),
					(val_add, reg0, DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),
					(troop_set_slot, ":troop_1", slot_troop_mother, reg0),
				(try_end),
				(try_begin),
					(troop_slot_eq, ":troop_2", slot_troop_mother, -1),
					(store_mul, reg0, ":troop_2", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),
					(val_add, reg0, DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),
					(troop_set_slot, ":troop_2", slot_troop_mother, reg0),
				(try_end),
			(try_end),
		(try_end),
	(try_end),
	##Add uncles and aunts by marriage.
	##In Native, the relation strength for blood uncles/aunts is 4, and for cousins is 2.
	##In light of this I've decided to set the relation strength for aunts/uncles by marriage to 2.
	(try_begin),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_1 is married to a sibling of one of troop_2's parents, pt. 1
		(ge, ":spouse_of_1", 0),
		(neg|troop_slot_eq, ":spouse_of_1", slot_troop_father, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_1", slot_troop_father, ":paternal_grandfather_of_2"),
			(troop_slot_eq, ":spouse_of_1", slot_troop_father, ":maternal_grandfather_of_2"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(str_store_string, s11, "str_aunt"),
		(else_try),
			(str_store_string, s11, "str_uncle"),
		(try_end),
	(else_try),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_1 is married to a sibling of one of troop_2's parents, pt. 2
		(ge, ":spouse_of_1", 0),
		(neg|troop_slot_eq, ":spouse_of_1", slot_troop_mother, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_1", slot_troop_mother, ":paternal_grandmother_of_2"),
			(troop_slot_eq, ":spouse_of_1", slot_troop_mother, ":maternal_grandmother_of_2"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(str_store_string, s11, "str_aunt"),
		(else_try),
			(str_store_string, s11, "str_uncle"),
		(try_end),
	(else_try),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_2 is married to a sibling of one of troop_1's parents, pt. 1
		(ge, ":spouse_of_2", 0),
		(neg|troop_slot_eq, ":spouse_of_2", slot_troop_father, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_2", slot_troop_father, ":paternal_grandfather_of_1"),
			(troop_slot_eq, ":spouse_of_2", slot_troop_father, ":maternal_grandfather_of_1"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(str_store_string, s11, "str_niece"),
		(else_try),
			(str_store_string, s11, "str_nephew"),
		(try_end),
	(else_try),
		(lt, ":relation_strength", 2),#Skip this check if a stronger relation has been found.
		#Test if troop_2 is married to a sibling of one of troop_1's parents, pt. 2
		(ge, ":spouse_of_2", 0),
		(neg|troop_slot_eq, ":spouse_of_2", slot_troop_mother, -1),
		(this_or_next|troop_slot_eq, ":spouse_of_2", slot_troop_mother, ":paternal_grandmother_of_1"),
			(troop_slot_eq, ":spouse_of_2", slot_troop_mother, ":maternal_grandmother_of_1"),
		(assign, ":relation_strength", 2),
		(try_begin),
			(eq, ":gender_1", tf_female),
			(str_store_string, s11, "str_niece"),
		(else_try),
			(str_store_string, s11, "str_nephew"),
		(try_end),
	(try_end),
	##diplomacy end+
    (assign, reg4, ":gender_1"),
	(assign, reg0, ":relation_strength"),
	])
]
