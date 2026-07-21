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

lord_comment_to_s43_scripts = [
# script_fill_tournament_participants_troop
("lord_comment_to_s43",
    [(store_script_param, ":lord", 1),
     (store_script_param, ":default_string", 2),

    (troop_get_slot,":reputation", ":lord", slot_lord_reputation_type),

		#some default strings will have added comments for the added commons reputation types
		##diplomacy start+
		(try_begin),
		#Don't reassign personalities of lords
			(is_between, ":reputation", lrep_none, lrep_upstanding + 1),
       		(else_try),
		#Special case for anti-humanitarians (Klethi in Native)
		    (neg|is_between, ":reputation", lrep_none, lrep_upstanding + 1),
	            (neq, ":reputation", lrep_benefactor),
	            (neq, ":reputation", lrep_moralist),
	            (neq, ":reputation", lrep_conventional),
		    (call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_humanitarian),
	      	    (lt, reg0, 0),#<- In Native, this only applies to Klethi
		    #Use lrep_debauched by default, and refine further below.
		    (assign, ":reputation", lrep_debauched),
		    (try_begin),
			#If pious, anti-humanitarians use lrep_selfrighteous
		    	(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_pious),
			(ge, reg0, 1),#<- Describes no one in Native
			(assign, ":reputation", lrep_selfrighteous),
		    (else_try),
			#If aggressive, anti-humanitarians use lrep_quarrelsome
		    	(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_aristocratic),
			(this_or_next|eq, ":reputation", lrep_adventurous),
				(ge, reg0, 1),#<- In Native describes Alayen, Matheld, Rolf, Nizar, Lezalit, Klethi (but only Klethi can even reach here)
			(assign, ":reputation", lrep_quarrelsome),
		    (try_end),
		(else_try),
		#Special case for "pious" characters (no one in Native)
			(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_pious),
			(ge, reg0, 1),
			(try_begin),
				#Handle these separately to prevent inappropriate reassignment
				(this_or_next|eq, ":reputation", lrep_benefactor),
					(eq, ":reputation", lrep_moralist),
				(assign, ":reputation", lrep_upstanding),
			(else_try),
				#Ordinarily upstanding
				(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_humanitarian),
				(ge, reg0, 0),#<- In Native describes all but Klethi
				(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_egalitarian),
				(ge, reg0, 0),#<- In Native describes all but Lezalit
				(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_honest),
				(ge, reg0, 0),#<- In Native describes all but Rolf
				(assign, ":reputation", lrep_upstanding),
		    	(else_try),
				#If vicious, self-righteous is also a possibility
			        (assign, ":reputation", lrep_selfrighteous),
		     	(try_end),
		(else_try),
		#Special case for dishonest commoners.
		#Pragmatic-style amoral: lrep_cunning
		#Jerk-style amoral: lrep_debauched
	 	 	(neg|is_between, ":reputation", lrep_none, lrep_upstanding + 1),
	            	(neq, ":reputation", lrep_moralist),
	            	(neq, ":reputation", lrep_benefactor),
			(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_honest),
			(lt, reg0, 0),#<- In Native only describes Rolf (who wouldn't reach here, since he is lrep_cunning)
			(try_begin),
				(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_egalitarian),
				(lt, reg0, 1),
				(assign, ":egalitarian", reg0),
				(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_humanitarian),
				(lt, reg0, 1),
				(this_or_next|lt, reg0, 0),
					(lt, ":egalitarian", 0),
				(assign, ":reputation", lrep_debauched),
			(else_try),
				(assign, ":reputation", lrep_cunning),
			(try_end),
		(else_try),
			(eq, ":reputation", lrep_roguish),
			(assign, ":reputation", lrep_goodnatured),
		(else_try),
			(eq, ":reputation", lrep_custodian),
			(assign, ":reputation", lrep_cunning),
		(else_try),
			(eq, ":reputation", lrep_benefactor),
			(assign, ":reputation", lrep_goodnatured),
        #add support for lady personalities
        (else_try),
            (eq, ":reputation", lrep_ambitious),
            (assign, ":reputation", lrep_cunning),
	(else_try),
	    (this_or_next|eq, ":reputation", lrep_conventional),
	    	(eq, ":reputation", lrep_otherworldly),
	    (assign, ":reputation", lrep_goodnatured),
	(else_try),
	    (eq, ":reputation", lrep_adventurous),
   	    (assign, ":reputation", lrep_martial),
  	    (call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_egalitarian),
	    (try_begin),
		    (lt, reg0, 0),#<- In Native describes no one
		    (assign, ":reputation", lrep_quarrelsome),
	    (try_end),
	(else_try),
	    (eq, ":reputation", lrep_moralist),
	    (assign, ":reputation", lrep_upstanding),
	(try_end),
	##diplomacy end+

	##diplomacy start+ Add some variability
	#For non-companion, non-monarchs who don't have any tmt_* morality values, this
	# just amounts to a 5% chance to use lrep_none instead of their real reputation
	# (except where that would cause problems).
	#Otherwise,
	# 16,17:
	#   tmt_pious > 0, with lrep_debauched or lrep_quarrelsome or lrep_selfrighteous: lrep_selfrighteous
	#   tmt_pious > 0, with one of (tmt_egalitarian, tmt_honest, tmt_humanitarian) < 0 and none > 0: lrep_selfrighteous
	#   (tmt_pious >= 0 and tmt_honest >= 0) and (tmt_pious > 0 or tmt_honest > 0): lrep_upstanding
	#   tmt_honest < 0: lrep_cunning
	#   lrep_none and is a king or pretender: lrep_cunning
	#
	# 18,19:
	#   tmt_aristocratic > 0, with lrep_debauched or lrep_quarrelsome: lrep_quarrelsome
	#   lrep_martial, with (tmt_honest, tmt_egalitarian, tmt_humanitarian) all non-positive and
	#      at least one negative, and tmt_pious < 1 (so not to overlap with 16,17): lrep_quarrelsome
	#   tmt_aristocratic > 0: lrep_martial
	#   lrep_none and is a king or pretender: lrep_martial
	(store_random_in_range, ":random_chance", 0, 20),
	(assign, ":new_reputation", ":reputation"),
	(try_begin),
		(eq, 1, 1),#Disable this feature for now.
	(else_try),
		#Disable the first time you're talking to someone, or if you haven't
		#spoken to this NPC recently.
		(store_current_hours, ":recently"),
		(val_sub, ":recently", 24),
		(this_or_next|neq, "$g_talk_troop_met", 1),
		(this_or_next|neg|troop_slot_ge, ":lord", slot_troop_met, 1),
		(this_or_next|neg|troop_slot_ge, ":lord", slot_troop_last_talk_time, ":recently"),
		#Disable for things that come in sequences
		(this_or_next|eq, ":default_string", "str_rebellion_dilemma_default"),
			(eq, ":default_string", "str_rebellion_dilemma_2_default"),
		#Set this value to signal to the debug message at the end
		(assign, ":random_chance", -1),
	(else_try),
		#10% chance of lrep_martial or lrep_quarrelsome if appropriate...
		#if already lrep_martial, check separately here for possible conversion
		#to lrep_quarrelsome
		(is_between, ":random_chance", 18, 20),
		(eq, ":reputation", lrep_martial),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_egalitarian),
		(lt, reg0, 1),
		(assign, ":bad_sum", reg0),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_humanitarian),
		(lt, reg0, 1),
		(val_add, ":bad_sum", reg0),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_honest),
		(lt, reg0, 1),
		(val_add, ":bad_sum", reg0),
		#at least one of tmt_egalitarian, tmt_humanitarian, and tmt_honest were negative (and none were positive)
		(lt, ":bad_sum", 0),
		#disable for positive tmt_pious, since that's handled separately as an alternative to lrep_upstanding for [16,17]
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_honest),
		(lt, reg0, 1),
		(assign, ":new_reputation", lrep_quarrelsome),
     	(else_try),
		#10% chance of lrep_martial or lrep_quarrelsome if appropriate
		#Applies to: Rolf, Nizar, Lezalit, Klethi
		#(Also Alayen and Matheld, but they are already lrep_martial)
		(is_between, ":random_chance", 18, 20),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_aristocratic),
		(ge, reg0, 1),
		(try_begin),
			#some personalities use lrep_quarrelsome (only Klethi in Native)
			(this_or_next|eq, ":reputation", lrep_debauched),
				(eq, ":reputation", lrep_quarrelsome),#<-- i.e. no change
			(assign, ":new_reputation", lrep_quarrelsome),
		(else_try),
			#other personalities use lrep_martial
	      		(assign, ":new_reputation", lrep_martial),
		(try_end),
	(else_try),
		#10% chance of lrep_upstanding or lrep_selfrighteous if appropriate
		#Applies to: Marnid, Alayen, Artimenner
		#(Also Firentis, but he is already lrep_upstanding)
		(is_between, ":random_chance", 16, 18),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_honest),
		(assign, ":honest", reg0),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_pious),
		(assign, ":pious", reg0),
		(this_or_next|ge, ":honest", 1),#one or the other must be greater than zero
			(ge, ":pious", 1),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_egalitarian),
		(assign, ":egalitarian", reg0),
		(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_humanitarian),
		(assign, ":humanitarian", reg0),
		(try_begin),
			#Unpleasant personalities use "selfrighteous" instead
			#(Applies to no one in Native)
			(this_or_next|eq, ":reputation", lrep_debauched),
			(this_or_next|eq, ":reputation", lrep_quarrelsome),
			(this_or_next|eq, ":reputation", lrep_selfrighteous),#<- i.e. no change
			(this_or_next|lt, ":honest", 0),
			(this_or_next|lt, ":egalitarian", 0),
				(lt, ":humanitarian", 0),
			(assign, ":new_reputation", lrep_selfrighteous),
		(else_try),
		   	#Other personalities use upstanding
			(assign, ":new_reputation", lrep_upstanding),
		(try_end),
	(else_try),
		#10% chance of lrep_cunning if appropriate
		(is_between, ":random_chance", 16, 18),
		(lt, ":honest", 0),#<- In Native only Rolf satisfies this, but he is already lrep_cunning
		(assign, ":reputation", lrep_cunning),
	(else_try),
		#Ruler, if personality triggers not met: 10% cunning, 10% martial
		(is_between, ":random_chance", 16, 20),
		(eq, ":reputation", lrep_none),
		(this_or_next|is_between, ":lord", kings_begin, kings_end),
			(is_between, ":lord", pretenders_begin, pretenders_end),
		(try_begin),
			(is_between, ":random_chance", 16, 18),
			(assign, ":new_reputation", lrep_cunning),
		(else_try),
			(is_between, ":random_chance", 18, 20),
			(call_script, "script_dplmc_get_troop_morality_value", ":lord", tmt_aristocratic),
			(ge, reg0, 0),#Won't reach here if positive, so you could just check if it equals zero
			(assign, ":new_reputation", lrep_martial),
		(try_end),
	(else_try),
		#Others, if personality triggers not met: 5% chance of null
		(is_between, ":random_chance", 16, 20),#base 20%
		(store_mod, ":rand_mod", ":random_chance",4),
		(troop_get_slot, reg0, ":lord", slot_troop_temp_decision_seed),
		(val_mod, reg0, 4),
		(eq, ":rand_mod", reg0),#1/4 of the time, 5%
		#disable for things that don't have a "lrep_none" version defined
		(neq, ":default_string", "str_rebellion_dilemma_default"),
		(neq, ":default_string", "str_rebellion_dilemma_2_default"),
		(neq, ":default_string", "str_changed_my_mind_default"),
		(neq, ":default_string", "str_political_philosophy_default"),
		(neq, ":default_string", "str_rebellion_rival_default"),
		(neq, ":default_string", "str_rebellion_agree_default"),
		(neq, ":default_string", "str_rebellion_refuse_default"),
		(neq, ":default_string", "str_talk_later_default"),
		(neq, ":default_string", "str_npc_claim_throne_liege"),
		#use lrep_none
		(assign, ":new_reputation", lrep_none),
	(try_end),
	(try_begin),
		(eq, 1, 0),#Disable this feature for now.
		(ge, "$cheat_mode", 1),
		(assign, ":save_reg1", reg1),
		(assign, ":save_reg2", reg2),
		(assign, reg0, ":random_chance"),
		(assign, reg1, ":reputation"),
		(assign, reg2, ":new_reputation"),
		(try_begin),
			(neq, ":reputation", ":new_reputation"),
			(display_message, "@{!} DEBUG - random {reg0} (0 to 20), used reputation {reg2} instead of {reg1}"),
		(else_try),
			(lt, ":random_chance", 0),
			(display_message, "@{!} DEBUG - variable responses disabled, kept reputation {reg2}"),
		(else_try),
			(display_message, "@{!} DEBUG - random {reg0} (0 to 20), kept reputation {reg2}"),
		(try_end),
		(assign, reg1, ":save_reg1"),
		(assign, reg2, ":save_reg2"),
	(try_end),
	(assign, ":reputation", ":new_reputation"),
	##diplomacy end+

    (store_add, ":result", ":reputation", ":default_string"),

    (str_store_string, 43, ":result"),
	(assign, reg0, ":result"),


	])
]
