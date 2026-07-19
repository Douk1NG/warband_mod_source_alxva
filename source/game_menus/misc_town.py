# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

misc_town_menus = [
  (
    "town_bandits_failed",mnf_disable_all_keys,
    "{s4} {s5}",
    "none",
    [
#      (call_script, "script_loot_player_items", 0),
      (store_troop_gold, ":total_gold", "trp_player"),
      (store_div, ":gold_loss", ":total_gold", 30),
      (store_random_in_range, ":random_loss", 40, 100),
      (val_add, ":gold_loss", ":random_loss"),
      (val_min, ":gold_loss", ":total_gold"),
      (troop_remove_gold, "trp_player",":gold_loss"),
      (party_set_slot, "$current_town", slot_center_has_bandits, 0),
      (party_get_num_companions, ":num_companions", "p_main_party"),
      (str_store_string, s4, "@The assasins beat you down and leave you for dead. ."),
      (str_store_string, s4, "@You have fallen. The bandits quickly search your body for every coin they can find,\
 then vanish into the night. They have left you alive, if only barely."),
      (try_begin),
        (gt, ":num_companions", 2),
        (str_store_string, s5, "@Luckily some of your companions come to search for you when you do not return, and find you lying by the side of the road. They hurry you to safety and dress your wounds."),
      (else_try),
        (str_store_string, s5, "@Luckily some passing townspeople find you lying by the side of the road, and recognise you as something other than a simple beggar. They carry you to the nearest inn and dress your wounds."),
      (try_end),
    ],
    [
      ("continue",[],"Continue...",[(change_screen_return),
      #SB : lose renown for easy encounters
      (call_script, "script_change_troop_renown", "trp_player", -2),
      ]),
    ],
  ),
  (
    "town_bandits_succeeded",mnf_disable_all_keys,
    "The {s4} fall before you as wheat to a scythe! Soon you stand alone in the streets\
 while {reg4?most of your attackers: the bandit} lie unconscious, dead or dying.\
 Searching the {reg4?bodies:body}, you find a purse which must have belonged to a previous victim of {reg4?these brute:this lowlife}.\
 Or perhaps, it was {reg4?given to them:provided} by someone who wanted to arrange a suitable ending to your life.",
    "none",
    [
      # (party_set_slot, "$current_town", slot_center_has_bandits, 0), #we need this
      (party_get_slot, ":bandit_troop", "$current_town", slot_center_has_bandits),
      (assign, "$g_last_defeated_bandits_town", "$g_encountered_party"),
      (try_begin),
        (check_quest_active, "qst_deal_with_night_bandits"),
        (neg|check_quest_succeeded, "qst_deal_with_night_bandits"),
        (quest_slot_eq, "qst_deal_with_night_bandits", slot_quest_target_center, "$g_encountered_party"),
        (call_script, "script_succeed_quest", "qst_deal_with_night_bandits"),
      (try_end),
      #SB : variable rewards, since we have different bandits in play
      (call_script, "script_game_get_join_cost", ":bandit_troop"),
      (store_mul, ":xp_reward", "$num_center_bandits", reg0),
      (try_begin), #reduce bonus exp, since town missions troops don't use horses
        (troop_is_mounted, ":bandit_troop"),
        (val_div, ":xp_reward", 2),
      (try_end),
      (add_xp_to_troop, ":xp_reward", "trp_player"),
      (call_script, "script_game_get_upgrade_cost", ":bandit_troop"), #20, 40, 80
      (store_mul, ":gold_reward", "$num_center_bandits", reg0),
      (call_script, "script_troop_add_gold", "trp_player", ":gold_reward"),
      #SB : string setup
      (str_store_troop_name_by_count,s4, ":bandit_troop", "$num_center_bandits"),
      (store_sub, reg4, "$num_center_bandits", 1),
    ],
    [
      ("continue",[],"Continue...",[
        (party_set_slot, "$current_town", slot_center_has_bandits, 0),
        (change_screen_return),
      ]),
    ],
  ),


   (
    "village_steal_cattle_confirm",0,
    "As the party member with the highest looting skill ({reg2}), {reg3?you reckon:{s1} reckons} that you can steal as many as {reg4} heads of village's cattle.",
    "none",
    [
      (call_script, "script_get_max_skill_of_player_party", "skl_looting"),
      (assign, reg2, reg0),
      (assign, ":max_skill_owner", reg1),
      (try_begin),
        (eq, ":max_skill_owner", "trp_player"),
        (assign, reg3, 1),
      (else_try),
        (assign, reg3, 0),
        (str_store_troop_name, s1, ":max_skill_owner"),
      (try_end),
      (call_script, "script_calculate_amount_of_cattle_can_be_stolen", "$current_town"),
      (assign, reg4, reg0),
      ],
    [
      ("village_steal_cattle_confirm",[],"Go on.",
       [
         (rest_for_hours_interactive, 3, 5, 1), #rest while attackable
         (assign, "$auto_menu", "mnu_village_steal_cattle"),
         (change_screen_return),
       ]),
      ("forget_it",[],"Forget it.",[(change_screen_return)]),
    ],
  ),
  (
    "cannot_enter_court",0,
    "There is a feast in progress in the lord's hall, but you are not of sufficient status to be invited inside. Perhaps increasing your renown would win you admittance -- or you might also try distinguishing yourself at a tournament while the feast is in progress...",
    "none",
    [],
    [
    ("continue", [],"Continue",
       [
        (jump_to_menu, "mnu_town"),
        ]),
    ]),
  (
    "lady_visit",0,
    "Whom do you wish to visit?",
    "none",
    [],
    [

	("visit_lady_1", [
	(gt, "$love_interest_in_town", 0),
	(str_store_troop_name, s12, "$love_interest_in_town"),
	],
	  "Visit {s12}",
       [
	    (assign, "$love_interest_in_town", "$love_interest_in_town"),
        (jump_to_menu, "mnu_garden"),
        ]),



	("visit_lady_2", [
	(gt, "$love_interest_in_town_2", 0),
	(str_store_troop_name, s12, "$love_interest_in_town_2"),
	],
	  "Visit {s12}",
       [
	    (assign, "$love_interest_in_town", "$love_interest_in_town_2"),
        (jump_to_menu, "mnu_garden"),
        ]),

	("visit_lady_3", [
	(gt, "$love_interest_in_town_3", 0),
	(str_store_troop_name, s12, "$love_interest_in_town_3"),
	],
	  "Visit {s12}",
       [
	    (assign, "$love_interest_in_town", "$love_interest_in_town_3"),
        (jump_to_menu, "mnu_garden")], "Door to the garden."),


	("visit_lady_4", [(gt, "$love_interest_in_town_4", 0),(str_store_troop_name, s12, "$love_interest_in_town_4"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_4"),(jump_to_menu, "mnu_garden"),]),

	("visit_lady_5", [(gt, "$love_interest_in_town_5", 0),(str_store_troop_name, s12, "$love_interest_in_town_5"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_5"),(jump_to_menu, "mnu_garden"),]),

	("visit_lady_6",[(gt, "$love_interest_in_town_6", 0),(str_store_troop_name, s12, "$love_interest_in_town_6"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_6"),(jump_to_menu, "mnu_garden"),]),

	("visit_lady_7",[(gt, "$love_interest_in_town_7", 0),(str_store_troop_name, s12, "$love_interest_in_town_7"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_7"),(jump_to_menu, "mnu_garden"),]),

	("visit_lady_8",[(gt, "$love_interest_in_town_8", 0),(str_store_troop_name, s12, "$love_interest_in_town_8"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_8"),(jump_to_menu, "mnu_garden"),]),


	("leave",[], "Leave",[(jump_to_menu, "mnu_town")]),

    ]
	),
  (
    "disembark",0,
    "Do you wish to disembark?",
    "none",
    [],
    [
      ("disembark_yes", [], "Yes.",
       [(assign, "$g_player_icon_state", pis_normal),
        (party_set_flags, "p_main_party", pf_is_ship, 0),
        (party_get_position, pos1, "p_main_party"),
        (party_set_position, "p_main_party", pos0),
        (party_get_slot, ":ship_type", "p_main_party", slot_party_ship_type),
        (try_begin),
          (le, "$g_main_ship_party", 0),
          (set_spawn_radius, 0),
          (spawn_around_party, "p_main_party", "pt_none"),
          (assign, "$g_main_ship_party", reg0),
          (party_set_flags, "$g_main_ship_party", pf_is_static|pf_always_visible|pf_hide_defenders|pf_is_ship, 1),
          (str_store_troop_name, s1, "trp_player"),
          (party_set_slot, "$g_main_ship_party", slot_party_ship_type, ":ship_type"),
          (party_set_name, "$g_main_ship_party", "@{s1}'s Ship"),
          (party_set_icon, "$g_main_ship_party", "icon_ship"),
          (party_set_slot, "$g_main_ship_party", slot_party_type, spt_ship),

          (try_begin),
            (eq, ":ship_type", 1),
            (party_set_name, "$g_main_ship_party", "@{s1}'s Longship"),
          (else_try),
            (eq, ":ship_type", 2),
            (party_set_name, "$g_main_ship_party", "@{s1}'s Galley"),
          (else_try),
            (eq, ":ship_type", 3),
            (party_set_name, "$g_main_ship_party", "@{s1}'s Cog"),
          (else_try),
            (eq, ":ship_type", 4),
            (party_set_name, "$g_main_ship_party", "@{s1}'s Dhow"),
          (try_end),


        (try_end),
        (enable_party, "$g_main_ship_party"),
        (party_set_position, "$g_main_ship_party", pos0),
        (party_set_icon, "$g_main_ship_party", "icon_ship_on_land"),
        (assign, "$g_main_ship_party", -1),
        (party_set_slot, "p_main_party", slot_party_ship_type, 0),
        (change_screen_return),
        ]),
      ("disembark_no", [
        (party_get_position, pos1, "p_main_party"),
        (map_get_water_position_around_position, pos2, pos1, 3),
        (get_distance_between_positions_in_meters, ":dist", pos1, pos2),
        (lt, ":dist", 3),
      ], "No.",
       [
        #(map_get_water_position_around_position, pos1, pos0, 6),
        #(party_set_position, "p_main_party", pos2),
        (rest_for_hours_interactive, 1, 20, 1),
        (change_screen_return),
        ]),
    ]
  ),
  (
    "ship_reembark",0,
    "Do you wish to embark?",
    "none",
    [],
    [
      ("reembark_yes", [
        (party_get_position, pos1, "$g_encountered_party"),
        (map_get_water_position_around_position, pos2, pos1, 3),
        (get_distance_between_positions_in_meters, ":dist", pos1, pos2),
        (lt, ":dist", 3),
        #(neq, "$g_player_icon_state", pis_ship),
        ], "Yes.",
       [(assign, "$g_player_icon_state", pis_ship),
        (party_set_flags, "p_main_party", pf_is_ship, 1),
        #(party_get_position, pos1, "p_main_party"),
        #(map_get_water_position_around_position, pos2, pos1, 6),
        (party_set_position, "p_main_party", pos2),

        (party_get_slot, ":ship_type", "$g_encountered_party", slot_party_ship_type),
        (party_set_slot, "p_main_party", slot_party_ship_type, ":ship_type"),

        (assign, "$g_main_ship_party", "$g_encountered_party"),
        (disable_party, "$g_encountered_party"),
        (change_screen_return),
        ]),
      ("reembark_no", [], "No.",
       [(change_screen_return),
        ]),
    ]
  ),
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
  ),
  (
    "town_cheats",0,
    "Select an option to interact with troops here",
    "none",[(call_script, "script_set_town_picture"),],
    [
      ("page",
      [],
      "Next Page.",
      [
        (jump_to_menu, "mnu_town_cheats_2"),
      ]),

      ("debug",
      [],
      "Party Cheats.",
      [
        (jump_to_menu, "mnu_party_cheat"),
      ]),
      ("host_tournament",
      [(party_slot_eq, "$current_town", slot_party_type, spt_town),],
      "Host a tournament",
      [
           (call_script, "script_fill_tournament_participants_troop", "$current_town", 1),
           (assign, "$g_tournament_cur_tier", 0),
           (assign, "$g_tournament_player_team_won", -1),
           (assign, "$g_tournament_bet_placed", 0),
           (assign, "$g_tournament_bet_win_amount", 0),
           (assign, "$g_tournament_last_bet_tier", -1),
           (assign, "$g_tournament_next_num_teams", 0),
           (assign, "$g_tournament_next_team_size", 0),
           (jump_to_menu, "mnu_town_tournament"),
      ]),

      ("camp_cheat_gather",[(party_slot_eq, "$current_town", slot_party_type, spt_town),],"Gather all inactive NPCs.",
       [ (assign, "$npc_to_rejoin_party", -1),
         (try_for_range, ":troop_no", companions_begin, companions_end),
           (neg|main_party_has_troop, ":troop_no"),
           (troop_slot_eq, ":troop_no", slot_troop_days_on_mission, 0),
           (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),
            # (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
           (troop_set_slot, ":troop_no", slot_troop_cur_center, "$current_town"),
           (troop_set_slot, ":troop_no", slot_troop_turned_down_twice, 0),
         (try_end),
         # (jump_to_menu, "mnu_camp_cheat"),
        ]
        ),

      # ("camp_cheat_gather",[(party_slot_eq, "$current_town", slot_party_type, spt_town),],"Gather all NPCs not in main party (cancel missions).",
       # [ (assign, "$npc_to_rejoin_party", -1),
         # (try_for_range, ":troop_no", companions_begin, companions_end),
            # (neg|main_party_has_troop, ":troop_no"),
            # (call_script, "script_remove_troop_from_prison", ":troop_no"),
            # (try_for_range, ":slots", slot_troop_days_on_mission, slot_troop_recruit_price),
              # (troop_set_slot, ":troop_no", ":slots", 0),
            # (try_end),
            # (troop_set_slot, ":troop_no", slot_troop_cur_center, "$current_town"),
         # (try_end),
        # ]
        # ),

      ("summon_drunk",
      [(party_slot_eq, "$current_town", slot_party_type, spt_town),
       # (troop_get_slot, ":town", "trp_belligerent_drunk", slot_troop_cur_center),
       (try_begin),
         # (is_between, ":town", towns_begin, towns_end),
         (troop_slot_eq, "trp_belligerent_drunk", slot_troop_cur_center, "$current_town"),
         (assign, reg10, 1),
       (else_try),
         (assign, reg10, 0),
       (try_end),
       ],
      "{reg10?Dismiss:Get} a drunkard.",
      [
        (try_begin),
          (eq, reg10, 1),
          (troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, -1),
        (else_try),
          (troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, "$current_town"),
        (try_end),
      ]),


      ("summon_ass",
      [(party_slot_eq, "$current_town", slot_party_type, spt_town),
       (try_begin),
         # (is_between, ":town", towns_begin, towns_end),
         (troop_slot_eq, "trp_hired_assassin", slot_troop_cur_center, "$current_town"),
         (assign, reg11, 1),
       (else_try),
         (assign, reg11, 0),
       (try_end),
      ],
      "{reg11?Scare away:Hire} an assassin.",
      [
        (try_begin),
          (eq, reg11, 1),
          (troop_set_slot, "trp_hired_assassin", slot_troop_cur_center, -1),
        (else_try),
          (troop_set_slot, "trp_hired_assassin", slot_troop_cur_center, "$current_town"),
        (try_end),
      ]),

      ("summon_bandit",
      [
       (neg|party_slot_eq, "$current_town", slot_party_type, spt_castle),
       (party_get_slot, reg12, "$current_town", slot_center_has_bandits),
       # (try_begin),
         # (party_slot_ge, "$current_town", slot_center_has_bandits, 1),
         # (assign, reg12, 1),
       # (else_try),
         # (assign, reg12, 0),
       # (try_end).
       (try_begin), #none present
         (eq, reg12, 0),
         (str_store_string, s12, "str_bandits"),
       (else_try),
         (str_store_troop_name_plural, s12, reg12),
       (try_end),
      ],
      "{reg12?Kick out:Get ambushed by} some {s12}.",
      [
       (try_begin), #cleanse
         (party_slot_ge, "$current_town", slot_center_has_bandits, 1),
         (party_set_slot, "$current_town", slot_center_has_bandits, 0),
       (else_try), #ambush
         (store_random_in_range, ":bandit", bandits_begin, bandits_end),
         (party_set_slot, "$current_town", slot_center_has_bandits, ":bandit"),
         (assign, "$town_nighttime", 1),
         (assign, "$sneaked_into_town", 0),
         (assign, "$g_defending_against_siege", 0),
         (call_script, "script_cf_enter_center_location_bandit_check"),
         # (assign, "$town_nighttime", 1),
       (try_end),
      ]),

      ("summon_village_bandit",
      [
       (party_slot_eq, "$current_town", slot_party_type, spt_village),
       (party_get_slot, reg13, "$current_town", slot_village_infested_by_bandits),
       (try_begin),
         (le, reg13, 0),
         (str_store_troop_name_plural, s13, "trp_bandit"),
       (else_try),
         (str_store_troop_name_plural, s13, reg13),
       (try_end),
      ],
      "{reg13?Cleanse:Infest} the village {reg13?of:with} {s13}.",
      [
        (try_begin), #cleanse
          (party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
          (party_set_slot, "$current_town", slot_village_infested_by_bandits, 0),
        (else_try), #infest
          (call_script, "script_center_get_bandits", "$current_town", 0),
          (party_set_slot, "$current_town", slot_village_infested_by_bandits, reg0),
          (jump_to_menu, "mnu_village"),
        (try_end),
      ]),

      ("summon_insurgent",
      [ (party_slot_eq, "$current_town", slot_village_infested_by_bandits, 0),
      ],
      "Spearhead a peasant revolution.",
      [
        (party_set_slot, "$current_town", slot_village_infested_by_bandits, "trp_peasant_woman"),

        #add additional troops
        (store_character_level, ":player_level", "trp_player"),
        (store_div, ":player_leveld2", ":player_level", 2),
        (store_mul, ":player_levelx2", ":player_level", 2),
        (try_begin),
          (is_between, "$current_town", villages_begin, villages_end),
          (store_random_in_range, ":random",0, ":player_level"),
          (party_add_members, "$current_town", "trp_mercenary_swordsman", ":random"),
          (store_random_in_range, ":random", 0, ":player_leveld2"),
          (party_add_members, "$current_town", "trp_hired_blade", ":random"),
        (else_try),
          (party_set_banner_icon, "$current_town", 0),
          (party_get_num_companion_stacks, ":num_stacks","$current_town"),
          (try_for_range, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_size, ":stack_size","$current_town",":i_stack"),
            (val_div, ":stack_size", 2),
            (party_stack_get_troop_id, ":troop_id", "$current_town", ":i_stack"),
            (party_remove_members, "$current_town", ":troop_id", ":stack_size"),
          (try_end),
          (store_random_in_range, ":random",":player_leveld2", ":player_levelx2"),
          (party_add_members, "$current_town", "trp_townsman", ":random"),
          (store_random_in_range, ":random",0, ":player_level"),
          (party_add_members, "$current_town", "trp_watchman", ":random"),
        (try_end),
      ]),

      ("center_refresh",
      [(party_slot_eq, "$current_town", slot_party_type, spt_town),],
      "Refresh merchants (global).",
      [
        # (party_get_slot, g.selected_troop,"$current_town", slot_town_weaponsmith),
        (call_script, "script_refresh_center_weaponsmiths"),
        # (party_get_slot, g.selected_troop,"$current_town", slot_town_armorer),
        (call_script, "script_refresh_center_armories"),
        # (party_get_slot, g.selected_troop,"$current_town", slot_town_horse_merchant),
        (call_script, "script_refresh_center_stables"),
        # (party_get_slot, g.selected_troop,"$current_town", slot_town_merchant),
        (call_script, "script_refresh_center_inventories"),
        # (assign, g.selected_troop, -1),
      ]),

      ("village_refresh",
      [(party_slot_eq, "$current_town", slot_party_type, spt_village),],
      "Refresh village goods.",
      [
        (call_script, "script_refresh_village_merchant_inventory", "$current_town"),
      ]),

      ("village_recruits",
      [(party_slot_eq, "$current_town", slot_party_type, spt_village),],
      "Refresh recruits.",
      [
        (call_script, "script_update_volunteer_troops_in_village", "$current_town"),
      ]),
      ("center_recruits",
      [(party_slot_eq, "$current_town", slot_party_type, spt_town),],
      "Refresh mercenaries.",
      [
        (store_random_in_range, ":troop_no", mercenary_troops_begin, mercenary_troops_end),
        (party_set_slot, "$current_town", slot_center_mercenary_troop_type, ":troop_no"),
        (store_random_in_range, ":amount", 3, 8),
        (try_begin),
          (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
          (store_character_level, ":level", "trp_player"), #increase limits a little bit as the game progresses.
          (store_add, ":level_factor", 80, ":level"),
          (val_mul, ":amount", ":level_factor"),
          (val_div, ":amount", 80),
        (try_end),
        (party_set_slot, "$current_town", slot_center_mercenary_troop_amount, ":amount"),
      ]),

      ("go_back",
      [(neg|party_slot_eq,"$current_town",slot_party_type, spt_village),],
      "Go Back.",
      [
        (jump_to_menu,"mnu_town"),
      ]),

      ("continue",
      [(party_slot_eq,"$current_town",slot_party_type, spt_village),],
      "Continue.",
      [
        (jump_to_menu,"mnu_village"),
      ]),
    ]),
  (
    "town_cheats_2",0,
    "Select an option to interact with the center itself. Prosperity is {reg1}, Relation is {reg2}, there are {reg3} parties in town.",
    "none",[
        (call_script, "script_set_town_picture"),
        (party_get_slot, reg1, "$current_town", slot_town_prosperity),
        (party_get_slot, reg2, "$current_town", slot_center_player_relation),

        (assign, ":count", 0),
        (try_for_parties, ":party_no"),
          (party_is_active, ":party_no"),
          (party_is_in_town, ":party_no", "$current_town"),
          (val_add, ":count", 1),
        (try_end),
        (assign, reg3, ":count"),
      ],
      [
          ("page",
          [],
          "Previous Page.",
          [
            (jump_to_menu, "mnu_town_cheats"),
          ]),

          ("toggle_state",
          [(party_slot_eq, "$current_town", slot_party_type, spt_village),
           (party_get_slot, reg1, "$current_town", slot_village_state),],
          "{reg1?Restore:Raze} this village.",
          [
            (try_begin),
              (party_slot_eq, "$current_town", slot_village_state, svs_normal),
              (call_script, "script_village_set_state", "$current_town", svs_looted),
            (else_try),
              (call_script, "script_village_set_state", "$current_town", svs_normal),
            (try_end),
          ]),

          ("village_manage",
          [], "Manage this center.",
          [
           (assign, "$g_next_menu", "mnu_town_cheats_2"),
           (jump_to_menu, "mnu_center_manage"),
          ]),
          ("increase_rel",
          [],
          "Increase Relation.",
          [
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_change_player_relation_with_center", "$current_town", 1),
            (else_try),
              (call_script, "script_change_player_relation_with_center", "$current_town", 5),
            (try_end),
          ]),

          ("decrease_rel",
          [],
          "Decrease Relation.",
          [
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_change_player_relation_with_center", "$current_town", -1),
            (else_try),
              (call_script, "script_change_player_relation_with_center", "$current_town", -5),
            (try_end),
          ]),

          ("increase_prosp",
          [],
          "Increase Prosperity.",
          [
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_change_center_prosperity", "$current_town", 1),
            (else_try),
              (call_script, "script_change_center_prosperity", "$current_town", 5),
            (try_end),
          ]),

          ("decrease_prosp",
          [],
          "Decrease Prosperity.",
          [
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_change_center_prosperity", "$current_town", -1),
            (else_try),
              (call_script, "script_change_center_prosperity", "$current_town", -5),
            (try_end),
          ]),

          ("castle_cheat_interior",
          [(neg|party_slot_eq, "$current_town", slot_party_type, spt_village)],
          "{!}Interior.",
          [
            (set_jump_mission,"mt_ai_training"),
            (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
            (jump_to_scene,":castle_scene"),
            (change_screen_mission),
          ]),

          ("castle_cheat_town_exterior",
          [],
          "{!}Exterior.",
          [
            # (try_begin),
              # (party_slot_eq, "$current_town",slot_party_type, spt_castle),
              # (party_get_slot, ":scene", "$current_town", slot_castle_exterior),
            # (else_try),
              # (party_get_slot, ":scene", "$current_town", slot_town_center),
            # (try_end),
            (party_get_slot, ":scene", "$current_town", slot_town_center),
            (set_jump_mission,"mt_ai_training"),
            (jump_to_scene,":scene"),
            (change_screen_mission),
          ]),

          ("castle_cheat_dungeon",
          [(neg|party_slot_eq, "$current_town", slot_party_type, spt_village)],
          "{!}Prison.",
          [
            (set_jump_mission,"mt_ai_training"),
            (party_get_slot, ":castle_scene", "$current_town", slot_town_prison),
            (jump_to_scene,":castle_scene"),
            (change_screen_mission),
          ]),

          ("castle_cheat_town_walls",
          [
            (party_slot_eq,"$current_town",slot_party_type, spt_town),
          ],
          "{!}Town Walls.",
          [
            (party_get_slot, ":scene", "$current_town", slot_town_walls),
            (set_jump_mission,"mt_ai_training"),
            (jump_to_scene,":scene"),
            (change_screen_mission),
          ]),

          ("cheat_town_start_siege",
          [ (neg|party_slot_eq, "$current_town", slot_party_type, spt_village),
            (party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
            (lt, "$g_encountered_party_2", 1),
            # (call_script, "script_party_count_fit_for_battle","p_main_party"),
            # (gt, reg(0), 1),
            # (try_begin),
              # (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
              # (assign, reg6, 1),
            # (else_try),
              # (assign, reg6, 0),
            # (try_end),
          ],
          "Besiege the center...",
          [
            (assign,"$g_player_besiege_town","$g_encountered_party"),
            (jump_to_menu, "mnu_castle_besiege"),
          ]),

          ("center_reports",
          [],
          "Show reports.",
          [
            (jump_to_menu,"mnu_center_reports"),
          ]),

          ("sail_from_port",
          [
            (party_slot_eq,"$current_town",slot_party_type, spt_town),
            (party_get_position, pos1, "$current_town"),
            (map_get_water_position_around_position, pos2, pos1, 8),
            (get_distance_between_positions_in_meters, ":dist", pos1, pos2),
            (lt, ":dist", 8),
            # (party_set_position, "p_main_party", pos2),
            # (ge, "$cheat_mode", 1),
            #(party_slot_eq,"$current_town",slot_town_near_shore, 1),
          ],
          "{!}Sail from port.",
          [
            (assign, "$g_player_icon_state", pis_ship),
            (party_set_flags, "p_main_party", pf_is_ship, 1),
            # (party_get_position, pos1, "p_main_party"),
            # (map_get_water_position_around_position, pos2, pos1, 6),
            (party_set_position, "p_main_party", pos2),
            (assign, "$g_main_ship_party", -1),
            (change_screen_return),
          ]),


          ("go_back",
          [(neg|party_slot_eq,"$current_town",slot_party_type, spt_village),],
          "Go Back.",
          [
            (jump_to_menu,"mnu_town"),
          ]),

          ("continue",
          [(party_slot_eq,"$current_town",slot_party_type, spt_village),],
          "Continue.",
          [
            (jump_to_menu,"mnu_village"),
          ]),
      ]
    ),

  #rename_court to set a capital,
  (
    "rename_court",0,
    "{!}This menu jumps to the rename presentation",
    "none",
    [
    # (call_script, "script_change_player_right_to_rule", 1), #handled in dialogues
    (assign, reg0, "$temp"),
    (display_message, "@{reg0}"),
    (try_begin),
        #(eq, "$temp", 1), #avoid menus getting stuck
        (jump_to_menu, "mnu_auto_return_to_map"),
    (try_end),
    (assign, "$g_presentation_state", rename_center),
    (call_script, "script_add_log_entry", logent_player_renamed_capital, "trp_player", "$g_player_court", -1, -1),
    (assign, "$temp", 1),
    (start_presentation, "prsnt_name_kingdom"),

    ],
    []),
  ( #export/import from prsnt_companion_overview
    "export_import", mnf_enable_hot_keys,
    "Press C to access {s1}'s character screen and then the statistics button on the bottom left.",
    "none",
    [
    (set_background_mesh, "mesh_pic_mb_warrior_1"),
    # # (set_player_troop, "trp_player"),
    # (change_screen_view_character),
    # # (change_screen_return),
    # (assign, "$talk_context", tc_town_talk),
    # (start_map_conversation, "$g_player_troop"),
    (set_player_troop, "$g_player_troop"),
    (str_store_troop_name_plural, s1, "$g_player_troop"),
    ],
    [
      ("rename",
      [],
      "I never liked the name {s1}...",
      [
        (assign, "$g_presentation_state", rename_companion),
        (start_presentation, "prsnt_name_kingdom"),
      ]),

      ("display_slots",
      [(ge, "$cheat_mode", 1)], "Show me all your secrets...",
      [
        (assign, "$g_talk_troop", "$g_player_troop"),
        (jump_to_menu, "mnu_display_troop_slots"),
      ]),
      ("continue",
      [],
      "Continue...",
      [
        (set_player_troop, "trp_player"),
        (jump_to_menu, "$g_next_menu"),
      ]),
    ]
  ),

  ( #helper menu to show all slots
    "display_party_slots", menu_text_color(0xFF990000),
    "{s1}",
    "none",
    [
    (set_background_mesh, "mesh_pic_messenger"),
    (str_store_party_name, s1, "$g_encountered_party"),
    (assign, reg1, "$g_encountered_party"),
    (assign, "$pout_party", 0),
    (try_for_parties, ":party_no"),
      # (assign, "$pout_party", ":party_no"),
      (party_is_active, ":party_no"),
      (gt, ":party_no", "$pout_party"),
      (assign, "$pout_party", ":party_no"),
    (try_end),
    (assign, reg2, "$pout_party"),
    (str_store_string, s1, "@{reg1}/{reg2}: {s1}"),
    #There's probably too many slots (and conflicting ones) to actually output the slot names to string
    (try_for_range, reg1, 0, 1000), #slot_town_trade_good_productions_begin
      (party_get_slot, reg0, "$g_encountered_party", reg1),
      (neq, reg0, 0), #if there's a value in here
      (str_store_string, s1, "@{s1}^{reg1}: {reg0}"),
    (try_end),

    # Process the prev and next parties
    # (assign, "$diplomacy_var",  "$g_encountered_party"),
    # (assign, "$diplomacy_var2", "$g_encountered_party"),
    # (try_for_parties, ":party_no"),
      # (party_is_active, ":party_no"),
      # (eq, "$diplomacy_var2", "$g_encountered_party"),
      # (try_begin), #find last party before current one
        # (lt, ":party_no", "$g_encountered_party"),
        # (assign, "$diplomacy_var", ":party_no"),
      # (else_try), #find first party after current one
        # (gt, ":party_no", "$g_encountered_party"),
        # (assign, "$diplomacy_var2", ":party_no"),
      # (try_end),
    # (try_end),
    (store_sub, "$diplomacy_var",  "$g_encountered_party", 1),
    (store_add, "$diplomacy_var2", "$g_encountered_party", 1),
    (try_begin), #find first
      (neg|party_is_active, "$diplomacy_var"),
      (assign, "$diplomacy_var", 0),
      (assign, ":end", "$g_encountered_party"),
      (try_for_range_backwards, ":party_no", 0, ":end"),
        (party_is_active, ":party_no"),
        (lt, ":party_no", "$g_encountered_party"),
        (gt, ":party_no", "$diplomacy_var"),
        (assign, "$diplomacy_var", ":party_no"),
        (assign, ":end", 0),
      (try_end),
    (try_end),
    # (val_max, "$diplomacy_var", "p_main_party"), #lock as first party

    (try_begin), #look for next
      (neg|party_is_active, "$diplomacy_var2"),
      (assign, "$diplomacy_var2", "$pout_party"), #this was previous checked as highest party
      (assign, ":end", "$pout_party"),
      (try_for_range, ":party_no", "$g_encountered_party", ":end"),
        (party_is_active, ":party_no"),
        (gt, ":party_no", "$g_encountered_party"),
        (le, ":party_no", "$diplomacy_var2"),
        (assign, "$diplomacy_var2", ":party_no"),
        (assign, ":end", "$g_encountered_party"),
      (try_end),
    (try_end),

    ],
    [

      ("notes",
      [(is_between, "$g_encountered_party", centers_begin, centers_end),],
      "View Notes.",
      [
        (change_screen_notes, 3, "$g_encountered_party"),
      ]),
      ("previous",
      [
        (ge, "$diplomacy_var", "p_main_party"),
        (lt, "$diplomacy_var", "$g_encountered_party"),
        (party_is_active, "$diplomacy_var"),
        (str_store_party_name, s2, "$diplomacy_var"),
      ],
      "Previous Party ({s2}).",
      [
        # (jump_to_menu, "mnu_party_cheat"),
        (assign, "$g_encountered_party", "$diplomacy_var"),
      ]),

      ("next",
      [
        (le, "$diplomacy_var2", "$pout_party"),
        (gt, "$diplomacy_var2", "$g_encountered_party"),
        (party_is_active, "$diplomacy_var2"),
        (str_store_party_name, s2, "$diplomacy_var2"),
      ],
      "Next Party ({s2}).",
      [
        (assign, "$g_encountered_party", "$diplomacy_var2"),
      ]),


      ("change",
      [],
      "Modify slots.",
      [
        (assign, "$g_presentation_state", 0), #start off at first slot
        (assign, "$g_presentation_input", rename_center),
        (start_presentation, "prsnt_modify_slots"),
      ]),

      ("continue",
      [],
      "Continue.",
      [
        # (jump_to_menu, "mnu_party_cheat"),
        (assign, "$new_encounter", 2),
        (set_encountered_party, "$g_encountered_party"),
        (call_script, "script_game_event_party_encounter", "$g_encountered_party", -1),
        # (change_screen_map),
        # (start_encounter, "$g_encountered_party"),
      ]),
    ]
  ),
  ( #exchange cheat from cmenu_encounter
    "party_cheat",0,
    "{!}{s10} is a {reg10?holding:member} of {s11} with relation {reg11}{reg6? (player relation {reg6}):} at ({reg8},{reg9}) {reg7} km away.^\
 It has {reg12}/{reg13} soldiers {reg13?in {reg14} stacks:}{reg15? and {reg15} prisoners in {reg16} stacks:{reg17? and {reg17} attached parties:}.^\
 AI Behaviour is {s13}{reg18? (currently {s14}):}, Object is {s15}{reg19? (currently {s16}):} at ({reg20},{reg21})",
    "none",
    [
    (assign, "$new_encounter", 0), #this undoes the cheat toggle global immediately
    (set_fixed_point_multiplier, 1000),
    #basic world info first line
    (str_store_party_name, s10, "$g_encountered_party"),
    (str_store_faction_name, s11, "$g_encountered_party_faction"),
    (try_begin),
      (this_or_next|is_between, "$g_encountered_party", centers_begin, centers_end),
      (is_between, "$g_encountered_party", training_grounds_begin, training_grounds_end),
      (assign, reg10, 1),
      (party_get_slot, reg6, "$g_encountered_party", slot_center_player_relation),
    (else_try),
      (assign, reg10, 0),
      (try_begin),
        (party_stack_get_troop_id, ":leader_troop", "$g_encountered_party", 0),
        (troop_is_hero, ":leader_troop"),
        (call_script, "script_troop_get_relation_with_troop", ":leader_troop", "trp_player"),
        (assign, reg6, reg0),
      (try_end),
    (try_end),
    (party_get_position, pos1, "$g_encountered_party"),
    (position_get_x, reg8, pos1),
    (position_get_y, reg9, pos1),
    (assign, reg11, "$g_encountered_party_relation"),
    (store_distance_to_party_from_party, reg7, "$g_encountered_party", "p_main_party"),

    #party composition second line
    (call_script, "script_party_count_fit_for_battle", "$g_encountered_party"),
    (assign, reg12, reg0),
    (party_get_num_companions, reg13, "$g_encountered_party"),
    (party_get_num_companion_stacks, reg14, "$g_encountered_party"),
    (party_get_num_prisoners, reg15, "$g_encountered_party"),
    (party_get_num_prisoner_stacks, reg16, "$g_encountered_party"),
    (party_get_num_attached_parties, reg17, "$g_encountered_party"),

    #AI info third line
    (get_party_ai_behavior, ":behaviour", "$g_encountered_party"),
    (val_add, ":behaviour", "str_ai_bhvr_hold"),
    (str_store_string, s13, ":behaviour"),
    (get_party_ai_current_behavior, ":cur_behaviour", "$g_encountered_party"),
    (val_add, ":cur_behaviour", "str_ai_bhvr_hold"),
    (try_begin),
      (neq, ":cur_behaviour", ":behaviour"),
      (str_store_string, s14, ":cur_behaviour"),
      (assign, reg18, 1),
    (else_try),
      (str_clear, s14),
      (assign, reg18, 0),
    (try_end),

    (get_party_ai_object, ":object", "$g_encountered_party"),
    (try_begin),
      (this_or_next|le, ":object", 0),
      (neg|party_is_active, ":object"),
      (str_store_string, s15, "str_dplmc_none"),
    (else_try),
      (str_store_party_name, s15, ":object"),
    (try_end),
    (get_party_ai_current_object, ":cur_object", "$g_encountered_party"),
    (assign, reg19, 1),
    (try_begin),
      (eq, ":cur_object", ":object"),
      (assign, reg19, 0), #disable display
    (else_try),
      (this_or_next|le, ":cur_object", 0),
      (neg|party_is_active, ":cur_object"),
      (str_store_string, s16, "str_dplmc_none"),
    (else_try),
      (str_store_party_name, s16, ":cur_object"),
    (try_end),

    (party_get_ai_target_position, pos2, "$g_encountered_party"),
    (position_get_x, reg20, pos2),
    (position_get_y, reg21, pos2),

    #grab the background mesh stuff
    (try_begin),
      (is_between, "$g_encountered_party", centers_begin, centers_end),
      (assign, "$current_town", "$g_encountered_party"),
      (call_script, "script_set_town_picture"),
    (else_try),
      (eq, "$g_encountered_party_template", "pt_looters"),
      (set_background_mesh, "mesh_pic_bandits"),
    (else_try),
      (eq, "$g_encountered_party_template", "pt_mountain_bandits"),
      (set_background_mesh, "mesh_pic_mountain_bandits"),
    (else_try),
      (eq, "$g_encountered_party_template", "pt_steppe_bandits"),
      (set_background_mesh, "mesh_pic_steppe_bandits"),
    (else_try),
      (eq, "$g_encountered_party_template", "pt_taiga_bandits"),
      (set_background_mesh, "mesh_pic_steppe_bandits"),
    (else_try),
      (eq, "$g_encountered_party_template", "pt_sea_raiders"),
      (set_background_mesh, "mesh_pic_sea_raiders"),
    (else_try),
      (eq, "$g_encountered_party_template", "pt_forest_bandits"),
      (set_background_mesh, "mesh_pic_forest_bandits"),
    (else_try),
      (this_or_next|eq, "$g_encountered_party_template", "pt_deserters"),
      (eq, "$g_encountered_party_template", "pt_routed_warriors"),
      (set_background_mesh, "mesh_pic_deserters"),
    #SB : dplmc party templates
    (else_try),
      (eq, "$g_encountered_party_template", "pt_center_reinforcements"),
      (set_background_mesh, "mesh_pic_recruits"),
    (else_try),
      (eq, "$g_encountered_party_template", "pt_kingdom_hero_party"),
      (party_stack_get_troop_id, ":leader_troop", "$g_encountered_party", 0),
      (ge, ":leader_troop", 1),
      (troop_get_slot, ":leader_troop_faction", ":leader_troop", slot_troop_original_faction),
      (try_begin),
        (eq, ":leader_troop_faction", fac_kingdom_1),
        (set_background_mesh, "mesh_pic_swad"),
      (else_try),
        (eq, ":leader_troop_faction", fac_kingdom_2),
        (set_background_mesh, "mesh_pic_vaegir"),
      (else_try),
        (eq, ":leader_troop_faction", fac_kingdom_3),
        (set_background_mesh, "mesh_pic_khergit"),
      (else_try),
        (eq, ":leader_troop_faction", fac_kingdom_4),
        (set_background_mesh, "mesh_pic_nord"),
      (else_try),
        (eq, ":leader_troop_faction", fac_kingdom_5),
        (set_background_mesh, "mesh_pic_rhodock"),
      (else_try),
        (eq, ":leader_troop_faction", fac_kingdom_6),
        (set_background_mesh, "mesh_pic_sarranid_encounter"),
      (try_end),
    (try_end),
    ],
    [

      ("talk",
      [],
      "Encounter the party.",
      [
        (call_script, "script_game_event_party_encounter", "$g_encountered_party", -1),
        # (change_screen_map),
      ]),

      ("slots",
      [],
      "Dump all slot values.",
      [ #g_encountered_party is the input
        (jump_to_menu, "mnu_display_party_slots"),
      ]),


      ("reinf",
      [],
      "Reinforce party.",
      [

      (try_begin),
        (is_between, "$g_encountered_party", villages_begin, villages_end),
        # (party_add_template, "$g_encountered_party", "pt_village_defenders"),
        (call_script, "script_refresh_village_defenders", "$g_encountered_party"),
      (else_try),
        (is_between, "$g_encountered_party_faction", kingdoms_begin, kingdoms_end),
        (call_script, "script_cf_reinforce_party", "$g_encountered_party"),
      (else_try), #if the above falls through by not reinforcing we grab a random template
        (this_or_next|eq, "$g_encountered_party_faction", "fac_deserters"),
        (is_between, "$g_encountered_party_faction", npc_kingdoms_begin, kingdoms_end),
        (party_stack_get_troop_id, ":troop_id", "$g_encountered_party", 0),
        (store_faction_of_troop, "$g_encountered_party_faction", ":troop_id"),
        (store_random_in_range, ":slot_no", slot_faction_reinforcements_a, slot_faction_num_armies),
        (faction_get_slot, ":party_template", "$g_encountered_party_faction", ":slot_no"),
        (party_add_template, "$g_encountered_party", ":party_template"),
      (else_try),
        # (this_or_next|eq, "$g_encountered_party_faction", "fac_outlaws"),
        # (is_between, "$g_encountered_party_faction", bandit_factions_begin, bandit_factions_end),
        (party_get_template_id, ":party_template", "$g_encountered_party"),
        (party_add_template, "$g_encountered_party", ":party_template"),
      (try_end),
      ]),

    ("exp",
      [],
      "Upgrade party.",
      [
        (party_get_num_companion_stacks, ":num_stacks", "$g_encountered_party"),
        (party_clear, "p_temp_party"),
         (try_for_range_backwards, ":stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":id", "$g_encountered_party", ":stack"),
            (try_begin),
              (party_stack_get_size, ":size", "$g_encountered_party", ":stack"),
              # (call_script, "script_game_get_upgrade_xp", ":id"),
              # (store_mul, ":xp", reg0, ":size"),
              (try_begin),
                (troop_is_hero, ":id"),
                (store_character_level, ":level", ":id"),
                (assign, ":end", 100),
                (try_begin), #assign block of exp
                  (le, ":level", 10),
                  (assign, ":xp", 100),
                (else_try),
                  (le, ":level", 25),
                  (assign, ":xp", 1000),
                (else_try), #most people stop before level 30
                  (le, ":level", 35),
                  (assign, ":xp", 10000),
                (else_try),
                  (le, ":level", 50),
                  (assign, ":xp", 30000),
                (else_try),
                  (le, ":level", 60),
                  (assign, ":xp", 1000000),
                (else_try), #good luck, level caps at 63
                  (assign, ":xp", 10000000),
                (try_end),
                (try_for_range, ":unused", 0, ":end"),
                  (party_add_xp_to_stack, "$g_encountered_party", ":stack", ":xp"),
                  (add_xp_to_troop, 1, ":id"), #this actually upgrades the level
                  # (add_xp_as_reward, ":xp"),
                  (store_character_level, ":cur_level", ":id"),
                  (lt, ":level", ":cur_level"), #done
                  (assign, ":end", 0),
                (try_end),
              (else_try),
                (troop_get_upgrade_troop, ":upgrade_troop", ":id", 0),
                (gt, ":upgrade_troop", 0),
                (troop_get_upgrade_troop, ":upgrade_2", ":id", 1),
                (try_begin),
                  (gt, ":upgrade_2", 0),
                  (store_random_in_range, ":random_no", 0, 2),
                  (eq, ":random_no", 0),
                  (assign, ":upgrade_troop", ":upgrade_2"),
                (try_end),
                (party_add_members, "p_temp_party", ":upgrade_troop", ":size"),
                (party_stack_get_num_wounded, ":num_wounded", "$g_encountered_party", ":stack"),
                (party_wound_members, "p_temp_party", ":upgrade_troop", ":num_wounded"),
                (party_remove_members, "$g_encountered_party", ":id", ":size"),
                # (party_add_xp_to_stack, "$g_encountered_party", ":stack", ":xp"),
              (try_end),
            (try_end),
         (try_end),
         (call_script, "script_party_add_party_companions", "$g_encountered_party", "p_temp_party"),
      ]),

      ("wound",
      [],
      "Wound party.",
      [
        (call_script, "script_party_wound_all_members", "$g_encountered_party"),
      ]),
    ("heal",
      [],
      "Heal party.",
      [
        (call_script, "script_party_heal_all_members_aux", "$g_encountered_party"),
      ]),

     ("rename",[],"Rename party.",
       [(assign, "$g_presentation_state", rename_party),
       # (assign, "$g_encountered_party", "p_main_party"),
       (start_presentation, "prsnt_name_kingdom"),
       ]
       ),
      ("exchange",
      [],
      "Exchange with party.",
      [
        (change_screen_exchange_members,1),
      ]),

      ("bandits",
      [(is_between, "$g_encountered_party", centers_begin, centers_end),],
      "Spawn bandits nearby.",
      [
      (set_spawn_radius, 25),
      (try_for_range, ":unused", 0, 10),
        (store_random_in_range, ":party_template", bandit_party_templates_begin, bandit_party_templates_end),
        (spawn_around_party, "$g_encountered_party", ":party_template"),
      (try_end),
      ]),

      ("leave",[],"Leave.",
       [
        (assign, "$g_leave_encounter", 1),
        (change_screen_return),
       ]
      ),
    ]
  ),


  ( #helper menu to show all troop slots
    "display_troop_slots", menu_text_color(0xFF009900),
    "{s1}^{s2}",
    "none",
    [
    # (set_background_mesh, "mesh_pic_cattle"),
    (assign, reg1, "$g_talk_troop"),
    (str_store_troop_name, s1, "$g_talk_troop"),
    (str_store_troop_name_plural, s2, "$g_talk_troop"),
    (store_troop_faction, ":faction_no", "$g_talk_troop"),
    (str_store_faction_name, s3, ":faction_no"),
    (troop_get_class, ":class", "$g_talk_troop"),
    (str_store_class_name, s4, ":class"),
    (store_character_level, reg2, "$g_talk_troop"),
    (str_store_string, s1, "@{reg1}: {s1}, {s2} classified as level {reg2} {s3} {s4}"),
    (try_begin), #upgrades
      (neg|troop_is_hero, "$g_talk_troop"),
      (try_begin),
        (troop_get_upgrade_troop, ":upgrade_0", "$g_talk_troop", 0),
        (gt, ":upgrade_0", 0),
        (str_store_troop_name_plural, s2, ":upgrade_0"),
        (str_store_string, s1, "@{s1}^becomes {s2}"),
        (troop_get_upgrade_troop, ":upgrade_1", "$g_talk_troop", 1),
        (gt, ":upgrade_1", 0),
        (str_store_troop_name_plural, s2, ":upgrade_1"),
        (str_store_string, s1, "@{s1} and {s2}"),
      (try_end),

      (call_script, "script_game_get_upgrade_xp", "$g_talk_troop"),
      (assign, reg10, reg0),
      (call_script, "script_game_get_upgrade_cost", "$g_talk_troop"),
      (assign, reg11, reg0),
      (str_store_string, s1, "@{s1}^costs {reg11} to upgrade with {reg10} xp"),

      (call_script, "script_game_get_troop_wage", "$g_talk_troop", -1),
      (assign, reg12, reg0),
      (call_script, "script_game_get_join_cost", "$g_talk_troop"),
      (assign, reg13, reg0),

      #this is because this script ties a global to the price
      (assign, ":troop_no", "$g_talk_troop"),
      (assign, "$g_talk_troop", ransom_brokers_begin),
      (call_script, "script_game_get_prisoner_price", ":troop_no"),
      (assign, reg14, reg0),
      (assign, "$g_talk_troop", ":troop_no"),

      (str_store_string, s1, "@{s1}^wage of {reg12}, buy costs {reg13} sell costs {reg14}"),
    (else_try),
      (troop_is_hero, "$g_talk_troop"),
      (str_store_string, s2, "@hero"),
      (call_script, "script_cf_troop_debug_range", "$g_talk_troop", s2, 0),
      (str_store_string, s1, "@{s1} is a {s2}"),
      (try_begin),
        (store_troop_gold, ":gold", "$g_talk_troop"),
        (gt, ":gold", 0),
        (assign, reg1, ":gold"),
        (str_store_string, s1, "@{s1} with {reg1} gold"),
      (try_end),
      # (try_begin),
        # (store_partner_quest, ":quest_no"),
        # (ge, ":quest_no", 0),
        # (str_store_quest_name, s2, ":quest_no"),
        # (str_store_string, s1, "@{s1} tasking you with {s2}"),
      # (try_end),
    (try_end),

    (str_clear, s2),
    (try_for_range, reg1, 0, 1000),
      (troop_get_slot, reg0, "$g_talk_troop", reg1),
      (neq, reg0, 0), #if there's a value in here
      (str_store_string, s2, "@{s2}^{reg1}: {reg0}"),
    (try_end),

    (set_fixed_point_multiplier, 100),
    (init_position, pos0),
    (try_begin),
      (str_is_empty, s2),
      (position_set_x, pos0, 17),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 100),
    (else_try),
      (position_set_x, pos0, 60),
      (position_set_y, pos0, 20),
      (position_set_z, pos0, 100),
    (try_end),
    (store_mul, ":troop_no", "$g_talk_troop", 2),
    (set_game_menu_tableau_mesh, "tableau_game_party_window", ":troop_no", pos0),
    ],
    [

    #So apparently this one needs to re-jump to the menu
      ("notes",
      [(is_between, "$g_talk_troop", heroes_begin, heroes_end),],
      "View Notes.",
      [
        (change_screen_notes, 1, "$g_talk_troop"),
      ]),

      ("prev_range",
      [
        (gt, "$g_talk_troop", "trp_player"),
        (call_script, "script_cf_troop_debug_range", "$g_talk_troop", s3, -1),
        (str_store_troop_name, s3, reg0),
      ],
      "Head ({s3}).",
      [
        (call_script, "script_cf_troop_debug_range", "$g_talk_troop", s0, -1),
        (assign, "$g_talk_troop", reg0),
        (jump_to_menu, "mnu_display_troop_slots"),
      ]),

      ("next_range",
      [
        (call_script, "script_cf_troop_debug_range", "$g_talk_troop", s3, 1),
        (str_store_troop_name, s3, reg0),
      ],
      "Tail ({s3}).",
      [
        (call_script, "script_cf_troop_debug_range", "$g_talk_troop", s0, 1),
        (assign, "$g_talk_troop", reg0),
        (jump_to_menu, "mnu_display_troop_slots"),
      ]),

      ("prev",
      [
        (gt, "$g_talk_troop", "trp_player"),
        (store_sub, ":troop_no", "$g_talk_troop", 1),
        (str_store_troop_name, s2, ":troop_no"),
      ],
      "Previous Troop ({s2}).",
      [
        (val_sub, "$g_talk_troop", 1),
        (jump_to_menu, "mnu_display_troop_slots"),
      ]),

      ("next",
      [
        (lt, "$g_talk_troop", "trp_dplmc_recruiter"), #last troop apparently
        (store_add, ":troop_no", "$g_talk_troop", 1),
        (str_store_troop_name, s2, ":troop_no"),
      ],
      "Next Troop ({s2}).",
      [
        (val_add, "$g_talk_troop", 1),
        (jump_to_menu, "mnu_display_troop_slots"),
      ]),

      ("rename",
      [],
      "Rename.",
      [
        (assign, "$g_player_troop", "$g_talk_troop"),
        (assign, "$g_presentation_state", rename_companion),
        (start_presentation, "prsnt_name_kingdom"),
      ]),

      ("change",
      [],
      "Modify slots.",
      [
        (assign, "$g_presentation_state", 0), #start off at first slot
        (assign, "$g_presentation_input", rename_companion),
        (start_presentation, "prsnt_modify_slots"),
      ]),

      ("inventory",
      [],
      "Modify inventory.",
      [
        (change_screen_loot, "$g_talk_troop"),
      ]),

      ("continue",
      [],
      "Continue.",
      [
        (change_screen_map),
      ]),
    ]
  ),
  (
    "town_tavern_prostitution",0,
    "{s15}",
    "none",
    [#Auto-exectued
	(try_begin),
		(party_slot_eq, "$current_town", slot_town_has_brothel, 1),
		(str_store_string,s15,"@Your room is luxuriant, comfortable from the linen sheets to the smoothed flooring. The rose-stained glass window illuminates the bed, casting a soft pink glow about the chamber which itself radiates with a mood of pleasure and relaxation."),
	(else_try),
		(str_store_string,s15,"@Your room is nice, if old and worn down. The window holds a dissapointing, but convienent view of a stone wall from the neighboring building. A dim candle lights the otherwise mellow room to provide a somewhat romantic atmosphere."),
	(try_end),
	(set_background_mesh, "mesh_pic_custom_01"),
	(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
	(try_begin),
		(gt, "$g_currently_soliciting", 0),
		(str_store_string,s15,"@The hours drag on as you practice your craft..."), # Everything else has the stupid pluralities, this should too at some point.
		(set_background_mesh, "mesh_pic_custom_02"),
		(assign, ":fems", 0),
		(try_for_range, ":i_stack", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":troop_id", "p_main_party", ":i_stack"),
			(troop_is_hero, ":troop_id"),
			(call_script, "script_cf_dplmc_troop_is_female", ":troop_id"),
			(val_add, ":fems", 1),
		(try_end),
		(store_random_in_range, ":ff", 0, ":fems"),
		(try_begin),
			(try_for_range, ":i_stack", 0, ":num_stacks"),
				(party_stack_get_troop_id, ":troop_id", "p_main_party", ":i_stack"),
				(troop_is_hero, ":troop_id"),
				(call_script, "script_cf_dplmc_troop_is_female", ":troop_id"),
				(try_begin),
					(gt, ":ff", 0),
					(val_sub, ":ff", 1),
				(else_try),
					(eq, ":ff", 0),
					(val_sub, ":ff", 1),
					(assign, "$f_temp_var", ":troop_id"),
					(str_store_troop_name,s4,":troop_id"),
				(try_end),
			(try_end),
		(try_end),
	(try_end),
	],
	[
	 ("solicit_clients",
	 [(le, "$g_currently_soliciting", 0),],
	 "Solicit customers.",
		[
		(assign, "$g_currently_soliciting", "$current_town"),
		(try_begin),
			(party_slot_eq, "$current_town", slot_town_has_brothel, 1),
			(rest_for_hours, 24, 6, 0),
		(else_try),
			(rest_for_hours, 24, 3, 0),
		(try_end),
		(change_screen_return),
		],
	 ),

	 ("just_do_it",[(gt, "$g_currently_soliciting", 0),],"Watch {s4} with her customer.",
		[
		(assign, "$g_currently_soliciting", 0),
		(assign, ":workgirl", "$f_temp_var"),

		(party_get_slot, ":center_faction", "$current_town", slot_center_original_faction),
		(faction_get_slot, ":center_culture", ":center_faction", slot_faction_culture),
		(assign, ":customer1", 0),
		(assign, ":dna1", 0),
		(assign, ":customer2", 0),
		(assign, ":dna2", 0),

		(try_for_range,":entry",0,2), #generate 2 townspeople
			(faction_get_slot, ":town_walker", ":center_culture", slot_faction_town_walker_male_troop),
			(store_random_in_range,":rand",0,9), #dckplmc - randomly male or female
			(try_begin),
				(eq, ":rand", 1),
				(store_add, ":town_walker", 1, ":town_walker"),
			(try_end),
			(store_random_in_range,":dna",0,1000),
			(try_begin),
				(eq, ":customer1", 0),
				(assign, ":customer1", ":town_walker"),
				(assign, ":dna1", ":dna"),
			(else_try),
				(assign, ":customer2", ":town_walker"),
				(assign, ":dna2", ":dna"),
			(try_end),
		(try_end),

		(troop_set_slot, "trp_temp_array_a", 0, ":workgirl"),
		(troop_set_slot, "trp_temp_array_b", 0, -1), #Will always be a hero, so no dna needed
		(troop_set_slot, "trp_temp_array_a", 1, ":customer1"),
		(troop_set_slot, "trp_temp_array_b", 1, ":dna1"),
		(troop_set_slot, "trp_temp_array_a", 2, -1), #observer
		(troop_set_slot, "trp_temp_array_b", 2, -1),
		(troop_set_slot, "trp_temp_array_a", 3, ":customer2"),
		(troop_set_slot, "trp_temp_array_b", 3, ":dna2"),

		(assign, "$f_cons1", 0), #Con
		(assign, "$f_cons2", 0), #Con
		(assign, "$f_cons3", 0), #Con
		(assign, "$f_cons4", 0), #Con

		(assign, "$f_encountertype", 2),

		(store_random_in_range,"$g_sex_position",0,3), #Random position type
		(try_begin),
			(eq, "$g_sex_position", 2),
			(assign, ":pos", 4),
		(else_try),
			(assign, ":pos", 2),
		(try_end),

		(assign, ":scene", "scn_tavern"),
		(call_script, "script_start_fucking", ":pos", ":scene"),
		],
	 ),

	 ("back_to_town",
	 [
	 	(try_begin),
			(party_slot_eq, "$current_town", slot_town_has_brothel, 1),
			(str_store_string,s16,"@Leave your brothel."),
		(else_try),
			(str_store_string,s16,"@Leave the tavern."),
		(try_end),
	 ]
	 ,"{s16}",
		[
		(jump_to_menu, "mnu_town"),
		],
	 ),
	],
  ),
  (
    "town_tavern_prostitution_results",0,
    "{s10}",
    "none",
    [
		(set_background_mesh, "mesh_pic_custom_01"),
		(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
		(assign, ":fems", 0),
		(try_for_range, ":i_stack", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":troop_id", "p_main_party", ":i_stack"),
			(troop_is_hero, ":troop_id"),
			(call_script, "script_cf_dplmc_troop_is_female", ":troop_id"),
			(val_add, ":fems", 1),
			(str_store_troop_name,s5,":troop_id"),
		(try_end),

		(try_begin),
		(gt, ":fems", 2),
		(str_store_string, s10, "@After a hard night's work, everyone returns to your room and pools the earnings..."),
		(else_try),
		(eq, ":fems", 2),
		(str_store_string, s10, "@After a hard night's work, {s5} meets you in your room to pool the earnings..."),
		(else_try),
		(str_store_string, s10, "@After a hard night's work, you retire to your room to go over the earnings..."),
		(try_end),
    ],
	[
		(
			"continue_to_room",
			[],
			"Collect payment and clean yourself up.",
			[
			(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
			(assign, ":cash", 0),
			(try_for_range, ":i_stack", 0, ":num_stacks"),
				(party_stack_get_troop_id, ":troop_id", "p_main_party", ":i_stack"),
				(troop_is_hero, ":troop_id"),
				(call_script, "script_cf_dplmc_troop_is_female", ":troop_id"),

				(try_begin),
					(neq, "$f_temp_var", ":troop_id"),
					(troop_get_slot, ":encounters", ":troop_id", slot_troop_encounters),
					(val_add, ":encounters", 1),
					(troop_set_slot, ":troop_id", slot_troop_encounters, ":encounters"),
				(try_end),

				(store_attribute_level, ":cha", ":troop_id", ca_charisma),
				(val_mul, ":cha", 5), # This is really a dumb thing to do but I'm not sure this command takes floats
				(val_div, ":cha", 4), # Ends up being 1.25 multiplier, +/- however rounding works.
				(store_random_in_range, ":rand", -3, 6),
				(val_add, ":cha", ":rand"),
				(val_clamp, ":cha", 1, 1000),
				(val_add, ":cash", ":cha"),
				(assign, reg5, ":cha"),
				(str_store_troop_name,s4,":troop_id"),

				(display_message, "@{s4}'s customer paid her {reg5} denars.",0xFFFFD800),
			(try_end),
			(try_begin), # Now the tavernkeepers actually do take a third.
				(neg|party_slot_eq, "$current_town", slot_town_has_brothel, 1),
				(store_div, ":fee", ":cash", 3),
				(assign, reg5, ":fee"),
				(display_message, "@The tavernkeep's fee is {reg5} denars.", message_negative),
				(val_sub, ":cash", ":fee"),
				(val_clamp, ":cash", 1, 1000),
			(try_end),

			(assign, "$f_temp_var", 0),
			(play_sound, "snd_money_received"),
			(troop_add_gold, "trp_player", ":cash"),
			(jump_to_menu, "mnu_town_tavern_prostitution"),
			],
		),
	],
  ),
  (
    "buy_ship",0,
    "{s22}",
    "none",
    [  # I'd like to make this a full scene, or at least a dialogue with more to it than a simple menu.
	(try_begin), # For now I settle with not breaking the disguise feature.
		(gt, "$sneaked_into_town", disguise_none),
		(str_store_string, s22, "@After further consideration, a large purchace such as commisioning an entire ship will certianly attract too much attention..."),
	(else_try),
		(str_store_string, s22, "@Which ship do you want to buy?"),
	(try_end),
	],
    [
      ("ship_a",[(le, "$sneaked_into_town", disguise_none),],"Longship (5000 denars)",[
        (try_begin),
          (store_troop_gold, ":gold", "trp_player"),
          (ge, ":gold", 5000),
          (assign, "$g_player_icon_state", pis_ship),
          (party_set_flags, "p_main_party", pf_is_ship, 1),
          #
          (party_get_slot, ":port", "$current_town", slot_town_port),
          (party_get_position, pos2, ":port"),
          (party_set_position, "p_main_party", pos2),
          # (party_get_position, pos1, "p_main_party"),
          # (map_get_water_position_around_position, pos2, pos1, 8),
          # (party_set_position, "p_main_party", pos2),
          (assign, "$g_main_ship_party", -1),
          (party_set_slot, "p_main_party", slot_party_ship_type, 1),
          (troop_remove_gold, "trp_player", 5000),
          (change_screen_return),
        (else_try),
          (display_message, "@Not enough money to buy that."),
        (try_end),
      ]),
      ("ship_b",[(le, "$sneaked_into_town", disguise_none),],"Galley (7,000 denars)",[
        (try_begin),
          (store_troop_gold, ":gold", "trp_player"),
          (ge, ":gold", 7000),
          (assign, "$g_player_icon_state", pis_ship),
          (party_set_flags, "p_main_party", pf_is_ship, 1),
          #
          (party_get_slot, ":port", "$current_town", slot_town_port),
          (party_get_position, pos2, ":port"),
          (party_set_position, "p_main_party", pos2),
          # (party_get_position, pos1, "p_main_party"),
          # (map_get_water_position_around_position, pos2, pos1, 8),
          # (party_set_position, "p_main_party", pos2),
          (assign, "$g_main_ship_party", -1),
          (party_set_slot, "p_main_party", slot_party_ship_type, 2),
          (troop_remove_gold, "trp_player", 7000),
          (change_screen_return),
        (else_try),
          (display_message, "@Not enough money to buy that."),
        (try_end),
      ]),
      ("ship_c",[(le, "$sneaked_into_town", disguise_none),],"Cog (10,000 denars)",[
        (try_begin),
          (store_troop_gold, ":gold", "trp_player"),
          (ge, ":gold", 10000),
          (assign, "$g_player_icon_state", pis_ship),
          (party_set_flags, "p_main_party", pf_is_ship, 1),
          #
          (party_get_slot, ":port", "$current_town", slot_town_port),
          (party_get_position, pos2, ":port"),
          (party_set_position, "p_main_party", pos2),
          # (party_get_position, pos1, "p_main_party"),
          # (map_get_water_position_around_position, pos2, pos1, 8),
          # (party_set_position, "p_main_party", pos2),
          (assign, "$g_main_ship_party", -1),
          (party_set_slot, "p_main_party", slot_party_ship_type, 3),
          (troop_remove_gold, "trp_player", 10000),
          (change_screen_return),
        (else_try),
          (display_message, "@Not enough money to buy that."),
        (try_end),
      ]),
      ("ship_d",[(le, "$sneaked_into_town", disguise_none),],"Dhow (8,000 denars)",[
        (try_begin),
          (store_troop_gold, ":gold", "trp_player"),
          (ge, ":gold", 8000),
          (assign, "$g_player_icon_state", pis_ship),
          (party_set_flags, "p_main_party", pf_is_ship, 1),
          #
          (party_get_slot, ":port", "$current_town", slot_town_port),
          (party_get_position, pos2, ":port"),
          (party_set_position, "p_main_party", pos2),
          # (party_get_position, pos1, "p_main_party"),
          # (map_get_water_position_around_position, pos2, pos1, 8),
          # (party_set_position, "p_main_party", pos2),
          (assign, "$g_main_ship_party", -1),
          (party_set_slot, "p_main_party", slot_party_ship_type, 4),
          (troop_remove_gold, "trp_player", 8000),
          (change_screen_return),
        (else_try),
          (display_message, "@Not enough money to buy that."),
        (try_end),
      ]),
      ("leave",[],"Leave the shipyard.",[(jump_to_menu, "mnu_town")]),
    ]
  ),

# Here for reference, but we have our own options for this sort of thing.
#
#DtheHun
#  ("queens_blade",0,
#   "Select a action:",
#   "none",
#   [
#     ],
#    [
#      #("cenzura_level",[(neq, cenzura, 1),], "Set level of censure",
#      # [
#      #  (jump_to_menu, "mnu_cenzura_level"),
#	  # ]
#      # ),
#
#      ("set_troop_custom_armor_slots",[], "Set custom armor slots for troops random",
#       [
#		 (call_script, "script_set_custom_armor_slots"),
#         (jump_to_menu, "mnu_camp"),
#	   ]
#       ),
#
#      ("return",[],"Return",
#       [
#         (jump_to_menu, "mnu_camp"),
#        ]
#       ),
#     ]
#   ),
#  ("cenzura_level",0,
#   "Current setting is {s1}. Set the level of censorship:",
#   "none",
#	[
#  	  (str_clear, s1),
#	  (try_begin),
#		(eq, "$g_cenzura", 1),
#		(str_store_string, s1, "@Censored"),
#	  (else_try),
#		(eq, "$g_cenzura", 2),
#		(str_store_string, s1, "@Uncensored with permanent armor lose"),
#	  (else_try),
#		(str_store_string, s1, "@Uncensored"),
#	  (try_end),
#     ],
#    [
#      ("cenzura_1",[(neq, "$g_cenzura", 1),], "Censored",
#       [
#		(assign, "$g_cenzura", 1),
#		(display_message, "@Set game mode to Censored DONE"),
#		(jump_to_menu, "mnu_camp_action"),
#	   ]
#      ),
#      ("cenzura_0",[(neq, "$g_cenzura", 0),], "Uncensored",
#       [
#		(assign, "$g_cenzura", 0),
#		(display_message, "@Set game mode to Uncensored DONE"),
#        (jump_to_menu, "mnu_camp_action"),
#	   ]
#      ),
#      ("cenzura_2",[(neq, "$g_cenzura", 2),], "Uncensored with prermanent armor lose",
#       [
#		(assign, "$g_cenzura", 2),
#		(display_message, "@Set game mode to Uncensored with permanent armor lose DONE"),
#        (jump_to_menu, "mnu_camp_action"),
#	   ]
#      ),
#      ("return",[],"Return",
#       [
#         (jump_to_menu, "mnu_camp_action"),
#        ]
#       ),
#    ]
#  ),
#/DtheHun,
]
