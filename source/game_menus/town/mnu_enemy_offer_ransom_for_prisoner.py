# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

enemy_offer_ransom_for_prisoner_menu = [
(
    "enemy_offer_ransom_for_prisoner",0,
##diplomacy start+ Since s2 is the name of a kingdom rather than a person, change "sell him" to "sell them"
    "{s2} offers you a sum of {reg12} denars in silver if you are willing to sell them {s1}.",
##diplomacy end+
    "none",
    [ (call_script, "script_calculate_ransom_amount_for_troop", "$g_ransom_offer_troop"),
      (assign, reg12, reg0),
      (str_store_troop_name, s1, "$g_ransom_offer_troop"),
      (store_troop_faction, ":faction_no", "$g_ransom_offer_troop"),
      (str_store_faction_name, s2, ":faction_no"),

       #SB : add tableau
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 70),
      (position_set_y, pos0, 5),
      (position_set_z, pos0, 75),
      (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", "$g_ransom_offer_troop", pos0),
     ],
    [
      ("ransom_accept",[],"Accept the offer.",
       [ ##diplomacy begin

        (troop_set_slot, "$g_ransom_offer_troop", slot_troop_courtesan, -1),
        (try_begin),
          (gt, "$g_player_chamberlain", 0),
          (call_script, "script_dplmc_pay_into_treasury", reg12),
        (else_try),
        ##diplomacy end
          (troop_add_gold, "trp_player", reg12),
        ##diplomacy begin
        (try_end),
        ##diplomacy end
		##diplomacy start+
		#The enemy actually loses the gold paid.
		(assign, ":gold_paid", reg12),
		(assign, ":lord_who_pays", "$g_ransom_offer_troop"),
		(store_troop_faction, ":faction_no", "$g_ransom_offer_troop"),
		#For kingdom ladies, someone else might pay.
		(try_begin),
			(is_between, "$g_ransom_offer_troop", kingdom_ladies_begin, kingdom_ladies_end),
			(neg|troop_slot_eq, "$g_ransom_offer_troop", slot_troop_occupation, slto_kingdom_hero),#I think at this step even for heroes it's 0
			(neg|troop_slot_ge, "$g_ransom_offer_troop", slot_troop_wealth, 1),
			(try_begin),
				#Check spouse pays
				(troop_get_slot, ":lord", "$g_ransom_offer_troop", slot_troop_spouse),
				(this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
				(store_troop_faction, ":lord_faction", ":lord"),
				(eq, ":faction_no", ":lord_faction"),
				(neg|troop_slot_ge, ":lord", slot_troop_occupation, slto_retirement),
				(assign, ":lord_who_pays", ":lord"),
			(else_try),
				#Check father pays
				(troop_get_slot, ":lord", "$g_ransom_offer_troop", slot_troop_father),
				(this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
				(store_troop_faction, ":lord_faction", ":lord"),
				(eq, ":faction_no", ":lord_faction"),
				(neg|troop_slot_ge, ":lord", slot_troop_occupation, slto_retirement),
				(assign, ":lord_who_pays", ":lord"),
			(else_try),
				#Check guardian pays
				(troop_get_slot, ":lord", "$g_ransom_offer_troop", slot_troop_guardian),
				(this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
				(store_troop_faction, ":lord_faction", ":lord"),
				(eq, ":faction_no", ":lord_faction"),
				(neg|troop_slot_ge, ":lord", slot_troop_occupation, slto_retirement),
				(assign, ":lord_who_pays", ":lord"),
			(else_try),
				#Check mother pays
				(troop_get_slot, ":lord", "$g_ransom_offer_troop", slot_troop_mother),
				(this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
				(store_troop_faction, ":lord_faction", ":lord"),
				(eq, ":faction_no", ":lord_faction"),
				(neg|troop_slot_ge, ":lord", slot_troop_occupation, slto_retirement),
				(assign, ":lord_who_pays", ":lord"),
			(try_end),
            #SB : copy from dialogues
            (call_script, "script_get_kingdom_lady_social_determinants", "$g_ransom_offer_troop"),
            (assign, ":new_location", reg1),
            (troop_set_slot, "$g_ransom_offer_troop", slot_troop_cur_center, ":new_location"),
		(try_end),
		(try_begin),
			(ge, ":gold_paid", 0),
			(ge, ":lord_who_pays", 1),
			(troop_is_hero, ":lord_who_pays"),
			#Remove the gold.  The lady has her own funds (e.g. from her dower)
			#that will partially defray the expense to the lord, depending on
			#the campaign difficulty.
		    (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
		    (try_begin),
			   (eq, ":reduce_campaign_ai", 0), #hard: lord pays 50%, lady's resources pay for 50%
			   (val_div, ":gold_paid", 2),
		    (else_try),
			   (eq, ":reduce_campaign_ai", 1), #medium: lord pays 75%, lady's resources pay for 25%
			   (val_mul, ":gold_paid", 3),
			   (val_div, ":gold_paid", 4),
		    (try_end),#easy: lord pays 100%, lady pays nothing
			(call_script, "script_dplmc_remove_gold_from_lord_and_holdings", ":gold_paid", ":lord_who_pays"),
		(try_end),
		##diplomacy end+
        (party_remove_prisoners, "$g_ransom_offer_party", "$g_ransom_offer_troop", 1),
        (call_script, "script_remove_troop_from_prison", "$g_ransom_offer_troop"),
        (try_begin),
            (troop_get_type, ":is_female", "trp_player"),
            (eq, ":is_female", tf_female),
            #SB : add condition here
            (troop_get_type, ":is_female", "$g_ransom_offer_troop"),
            (eq, ":is_female", tf_male),
            (get_achievement_stat, ":number_of_lords_sold", ACHIEVEMENT_MAN_HANDLER, 0),
            (val_add, ":number_of_lords_sold", 1),
            (set_achievement_stat, ACHIEVEMENT_MAN_HANDLER, 0, ":number_of_lords_sold"),

            (eq, ":number_of_lords_sold", 3),
            (unlock_achievement, ACHIEVEMENT_MAN_HANDLER),
        (try_end),

        (change_screen_return),
        ]),
      ("ransom_reject",[],"Reject the offer.",
       [
	    ##diplomacy start+
		#Relation loss altered by lord personality type.
		#OLD:
        #(call_script, "script_change_player_relation_with_troop", "$g_ransom_offer_troop", -4),
		#NEW:
		(try_begin),
			(troop_slot_eq, "$g_ransom_offer_troop", slot_lord_reputation_type, lrep_quarrelsome),
			(call_script, "script_change_player_relation_with_troop", "$g_ransom_offer_troop", -6),
		(else_try),
			(troop_slot_eq, "$g_ransom_offer_troop", slot_lord_reputation_type, lrep_debauched),
			(call_script, "script_change_player_relation_with_troop", "$g_ransom_offer_troop", -5),
		(else_try),
			(call_script, "script_change_player_relation_with_troop", "$g_ransom_offer_troop", -4),
		(try_end),
		##diplomacy end+
        (call_script, "script_change_player_honor", -1),
        (assign, "$g_ransom_offer_rejected", 1),
		##diplomacy start+
		#TODO: Review this, it was partway through a redesign when I stopped.
		#Also apply a negative reaction modifier to other lords
		(assign, ":save_reg0", reg0),

		(store_faction_of_troop, ":captive_faction", "$g_ransom_offer_troop"),
		#For kingdom ladies:
		(try_begin),
			(is_between, "$g_ransom_offer_troop", kingdom_ladies_begin, kingdom_ladies_end),
			#(troop_slot_eq, "$g_ransom_offer_troop", slot_troop_occupation, slto_kingdom_lady),
			(call_script, "script_get_kingdom_lady_social_determinants", "$g_talk_troop"),
			(assign, ":guardian", reg0),
			(store_faction_of_troop, ":captive_faction", ":guardian"),

			(try_for_range, ":troop_no", heroes_begin, heroes_end),
				(troop_slot_ge, ":troop_no", slot_troop_occupation, slto_kingdom_hero),#lowest valid
				(neg|troop_slot_ge, ":troop_no", slot_troop_occupation, slto_inactive_pretender),#end of valid range
				(neq, "$g_ransom_offer_troop", ":troop_no"),
				(store_faction_of_troop, ":troop_faction", ":troop_no"),

				(assign, ":disapproval_threshold", 20),
				(try_begin),
					(neq, ":troop_faction", ":captive_faction"),
					(neg|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
					(assign, ":disapproval_threshold", 40),
				(try_end),
				#(this_or_next|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
				#	(eq, ":troop_faction", ":captive_faction"),
				(assign, ":relation_change", 0),

				#family
				(try_begin),
					(this_or_next|troop_slot_eq, ":troop_no", slot_troop_spouse, "$g_ransom_offer_troop"),
					(this_or_next|troop_slot_eq, "$g_ransom_offer_troop", slot_troop_spouse, ":troop_no"),
					(eq, ":guardian", ":troop_no"),
					(assign, ":relation_change", -4),
				(else_try),
					(eq, ":troop_no", slot_troop_betrothed, "$g_ransom_offer_troop"),
					(assign, ":relation_change", -4),
				(else_try),
					(call_script, "script_troop_get_family_relation_to_troop", "$g_ransom_offer_troop", ":troop_no"),
					(ge, reg0, 14),
					(assign, ":relation_change", -3),
				(else_try),
					(ge, reg0, 10),
					(assign, ":relation_change", -2),
				(else_try),
					(ge, reg0, 2),
					(assign, ":relation_change", -1),
				(else_try),
					(call_script, "script_troop_get_relation_with_troop", ":troop_no", "$g_ransom_offer_troop"),
					(ge, reg0, ":disapproval_threshold"),
					(this_or_next|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
						(eq, ":troop_faction", ":captive_faction"),
					(assign, ":relation_change", -1),
				(else_try),
					(ge, ":guardian", 1),
					(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":guardian"),
					(ge, reg0, ":disapproval_threshold"),
					(assign, ":relation_change", -1),
				(try_end),

				(lt, ":relation_change", 0),
				(try_begin),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
					(val_mul, ":relation_change", 3),#-1 to -2, -2 to -3, -3 to -5, -4 to -6
					(val_sub, ":relation_change", 1),
					(val_div, ":relation_change", 2),
				(try_end),
				(call_script, "script_change_player_relation_with_troop", ":troop_no", ":relation_change"),
			(try_end),
		(else_try),
		#For others:
			(is_between, "$g_ransom_offer_troop", active_npcs_begin, active_npcs_end),
			(try_for_range, ":hero", heroes_begin, heroes_end),
				(this_or_next|is_between, ":hero", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_hero),
				(neg|troop_slot_eq, ":hero", slot_troop_occupation, dplmc_slto_dead),
				(neg|troop_slot_ge, ":hero", slot_troop_occupation, slto_retirement),

				(neq, ":hero", "$g_ransom_offer_troop"),

				(store_faction_of_troop, ":troop_faction", ":hero"),

				(assign, ":relation_change", 0),

				(call_script, "script_troop_get_family_relation_to_troop", "$g_ransom_offer_troop", ":hero"),
				(try_begin),
					(ge, reg0, 10),
					(assign, ":relation_change", -1),
				(try_end),

				(call_script, "script_troop_get_relation_with_troop", ":hero", "$g_ransom_offer_troop"),
				(try_begin),
					(ge, reg0, 20),
					(eq, ":troop_faction", ":captive_faction"),
					(val_sub, ":relation_change", 1),
				(else_try),
					(ge, reg0, 40),
					(val_sub, ":relation_change", 1),
				(else_try),
					(lt, reg0, 0),
					(assign, ":relation_change", 0),
				(try_end),

				(lt, ":relation_change", 0),
				(try_begin),
					(troop_slot_eq, ":hero", slot_lord_reputation_type, lrep_quarrelsome),
					(val_mul, ":relation_change", 3),#-1 to -2, -2 to -3, -3 to -5, -4 to -6
					(val_sub, ":relation_change", 1),
					(val_div, ":relation_change", 2),
				(try_end),
				(call_script, "script_change_player_relation_with_troop", ":hero", ":relation_change"),
			(try_end),

			(try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
				(neg|troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_hero),
				(neg|troop_slot_eq, ":lady", slot_troop_occupation, dplmc_slto_dead),
				(neg|troop_slot_ge, ":lady", slot_troop_occupation, slto_retirement),

				(neq, ":lady", "$g_ransom_offer_troop"),

				(assign, ":relation_change", 0),
				(call_script, "script_troop_get_family_relation_to_troop", ":lady", "$g_ransom_offer_troop"),
				(try_begin),
					(ge, reg0, 14),
					(assign, ":relation_change", -3),
				(else_try),
					(ge, reg0, 10),
					(assign, ":relation_change", -2),
				(else_try),
					(ge, reg0, 2),
					(assign, ":relation_change", -1),
				(else_try),
					(call_script, "script_troop_get_relation_with_troop", ":lady", "$g_ransom_offer_troop"),
					(ge, reg0, 20),
					(assign, ":relation_change", -1),
				(try_end),

				(lt, ":relation_change", 0),
				(call_script, "script_change_player_relation_with_troop", ":lady", ":relation_change"),
			(try_end),
		(try_end),

		(assign, reg0, ":save_reg0"),
		##diplomacy end+
        (change_screen_return),
        ]),
    ]
  )
]
