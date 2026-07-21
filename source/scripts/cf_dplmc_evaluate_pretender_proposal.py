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

cf_dplmc_evaluate_pretender_proposal_scripts = [
#script_cf_dplmc_evaluate_pretender_proposal
# INPUT: arg1 = troop_id for pretender
# OUTPUT: reg0 = answer
#
# Writes reason to s14
# May clobber s0, s1
#
("cf_dplmc_evaluate_pretender_proposal",
    [
      (store_script_param_1, ":pretender"),
	  (assign, ":answer", -1),
	  (assign, ":save_reg1", reg1),
	  (assign, ":save_reg65", reg65),
	  (call_script, "script_dplmc_store_troop_is_female", ":pretender"),
	  (assign, reg65, reg0),

	  (str_store_string, s14, "str_ERROR_string"),

	  (is_between, ":pretender", pretenders_begin, pretenders_end),
	  (troop_slot_eq, ":pretender", slot_troop_occupation, slto_kingdom_hero),

	  (store_troop_faction, ":pretender_faction", ":pretender"),
	  (is_between, ":pretender_faction", npc_kingdoms_begin, npc_kingdoms_end),
	  (troop_slot_eq, ":pretender", slot_troop_original_faction, ":pretender_faction"),
	  (faction_slot_eq, ":pretender_faction", slot_faction_leader, ":pretender"),
	  (faction_slot_eq, ":pretender_faction", slot_faction_state, sfs_active),

	  (troop_slot_eq, ":pretender", slot_troop_spouse, -1),
	  (troop_slot_eq, ":pretender", slot_troop_betrothed, -1),

	  (troop_get_slot, ":pretender_renown", ":pretender", slot_troop_renown),
	  (val_max, ":pretender_renown", 1),

	  #There, we've covered the preliminaries: this should be a standard post-rebellion
	  #setup.  Now verify that the player is in a correct state.

	  (eq, "$players_kingdom", ":pretender_faction"),
	  (eq, "$player_has_homage", 1),
    (this_or_next|eq, "$g_polygamy", 1),
	  (troop_slot_eq, "trp_player", slot_troop_spouse, -1),
	  (troop_slot_eq, "trp_player", slot_troop_betrothed, -1),

	  (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
	  (call_script, "script_troop_get_player_relation", ":pretender"),
	  (assign, ":player_relation", reg0),

	  #Find competitors
	  (assign, ":b", -1),
	  (assign, ":b_relation", -101),
	  (assign, ":c", -1),
	  (assign, ":c_renown", -1),

	  (store_add, ":faction_renown", ":pretender_renown", ":player_renown"),
	  (assign, ":faction_lords", 2),#the player and the pretender

	  (troop_set_slot, ":pretender", slot_troop_temp_slot, 0),#clear
	  (troop_set_slot, "trp_player", slot_troop_temp_slot, 0),#clear

      (try_for_range_backwards, ":competitor", heroes_begin, heroes_end),
        (troop_slot_eq, ":competitor", slot_troop_occupation, slto_kingdom_hero),
        (store_faction_of_troop, ":competitor_faction", ":competitor"),
        (eq, ":competitor_faction", ":pretender_faction"),
        (try_begin),
          (is_between, ":competitor", kings_begin, kings_end), #SB : exclude former monarchs
          (troop_slot_eq, ":competitor", slot_troop_original_faction, ":pretender_faction"),
          (troop_set_slot, ":competitor", slot_troop_temp_slot, -99999),#low value
          (assign, ":competitor_renown", 0), #do not factor in
        (else_try),
          (troop_set_slot, ":competitor", slot_troop_temp_slot, 0),#clear
          (troop_get_slot, ":competitor_renown", ":competitor", slot_troop_renown),
        (try_end),

        (neq, ":competitor", active_npcs_including_player_begin),
        (neq, ":competitor", ":pretender"),

        (call_script, "script_troop_get_relation_with_troop", ":competitor", ":pretender"),
        (assign, ":competitor_relation", reg0),

        (val_add, ":faction_renown", ":competitor_renown"),
        (val_add, ":faction_lords", 1),

        (try_begin),
           (ge, ":competitor_relation", ":b_relation"),
           (neg|troop_slot_eq, ":competitor", slot_troop_spouse, "trp_player"),
           (neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":competitor"),
           (assign, ":b", ":competitor"),
           (assign, ":b_relation", ":competitor_relation"),
        (try_end),
        (try_begin),
           (ge, ":competitor_renown", ":c_renown"),
           (assign, ":c", ":competitor"),
           (assign, ":c_renown", ":competitor_renown"),
        (try_end),
      (try_end),

      (assign, ":pretender_towns", 0),
      (assign, ":pretender_castles", 0),
      (assign, ":pretender_villages", 0),

      (assign, ":player_towns", 0),
      (assign, ":player_castles", 0),
      (assign, ":player_villages", 0),

      (assign, ":faction_towns", 0),
      (assign, ":faction_castles", 0),
      (assign, ":faction_villages", 0),

      (assign, ":original_towns", 0),
      (assign, ":original_castles", 0),
      (assign, ":original_villages", 0),

   	  #(store_sub, ":global_towns", towns_end, towns_begin),
	  #(store_sub, ":global_castles", castles_end, castles_begin),
	  #(store_sub, ":global_villages", villages_end, villages_begin),

	  (assign, ":highest_score", -1),
	  (assign, ":highest_score_lord", -1),

	  (try_for_range, ":center_no", towns_begin, towns_end),
		(store_faction_of_party, ":center_faction", ":center_no"),
		(try_begin),
			(party_slot_eq, ":center_no", slot_town_lord, ":pretender"),
			(val_add, ":pretender_towns", 1),
			(val_add, ":faction_towns", 1),
		(else_try),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(val_add, ":player_towns", 1),
			(val_add, ":faction_towns", 1),
		(else_try),
			(this_or_next|eq, ":center_faction", ":pretender_faction"),
				(eq, ":center_faction", "fac_player_supporters_faction"),
			(val_add, ":faction_towns", 1),
			(party_get_slot, ":town_lord", ":center_no", slot_town_lord),
			(this_or_next|eq, ":town_lord", "trp_player"),
				(is_between, ":town_lord", heroes_begin, heroes_end),
			(troop_get_slot, ":local_temp", ":town_lord", slot_troop_temp_slot),
			(val_add, ":local_temp", 3),
			(troop_set_slot, ":town_lord", slot_troop_temp_slot, ":local_temp"),
			(ge, ":local_temp", ":highest_score"),
			(assign, ":highest_score", ":local_temp"),
			(assign, ":highest_score_lord", ":town_lord"),
		(try_end),
		(try_begin),
			(party_slot_eq, ":center_no", slot_center_original_faction, ":pretender_faction"),
			(val_add, ":original_towns", 1),
		(try_end),
	  (try_end),

	  (try_for_range, ":center_no", castles_begin, castles_end),
		(store_faction_of_party, ":center_faction", ":center_no"),
		(try_begin),
			(party_slot_eq, ":center_no", slot_town_lord, ":pretender"),
			(val_add, ":pretender_castles", 1),
			(val_add, ":faction_castles", 1),
		(else_try),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(val_add, ":player_castles", 1),
			(val_add, ":faction_castles", 1),
		(else_try),
			(this_or_next|eq, ":center_faction", ":pretender_faction"),
				(eq, ":center_faction", "fac_player_supporters_faction"),
			(val_add, ":faction_castles", 1),
			(party_get_slot, ":town_lord", ":center_no", slot_town_lord),
			(this_or_next|eq, ":town_lord", "trp_player"),
				(is_between, ":town_lord", heroes_begin, heroes_end),
			(troop_get_slot, ":local_temp", ":town_lord", slot_troop_temp_slot),
			(val_add, ":local_temp", 2),
			(troop_set_slot, ":town_lord", slot_troop_temp_slot, ":local_temp"),
			(ge, ":local_temp", ":highest_score"),
			(assign, ":highest_score", ":local_temp"),
			(assign, ":highest_score_lord", ":town_lord"),
		(try_end),
		(try_begin),
			(party_slot_eq, ":center_no", slot_center_original_faction, ":pretender_faction"),
			(val_add, ":original_castles", 1),
		(try_end),
	  (try_end),

	  (try_for_range, ":center_no", villages_begin, villages_end),
		(store_faction_of_party, ":center_faction", ":center_no"),
		(try_begin),
			(party_slot_eq, ":center_no", slot_town_lord, ":pretender"),
			(val_add, ":pretender_villages", 1),
			(val_add, ":faction_villages", 1),
		(else_try),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(val_add, ":player_villages", 1),
			(val_add, ":faction_villages", 1),
		(else_try),
			(this_or_next|eq, ":center_faction", ":pretender_faction"),
				(eq, ":center_faction", "fac_player_supporters_faction"),
			(val_add, ":faction_villages", 1),
			(party_get_slot, ":town_lord", ":center_no", slot_town_lord),
			(this_or_next|eq, ":town_lord", "trp_player"),
				(is_between, ":town_lord", heroes_begin, heroes_end),
			(troop_get_slot, ":local_temp", ":town_lord", slot_troop_temp_slot),
			(val_add, ":local_temp", 1),
			(troop_set_slot, ":town_lord", slot_troop_temp_slot, ":local_temp"),
			(ge, ":local_temp", ":highest_score"),
			(assign, ":highest_score", ":local_temp"),
			(assign, ":highest_score_lord", ":town_lord"),
		(try_end),
		(try_begin),
			(party_slot_eq, ":center_no", slot_center_original_faction, ":pretender_faction"),
			(val_add, ":original_villages", 1),
		(try_end),
	  (try_end),

	  #Update stats
	  (faction_set_slot, ":pretender_faction", slot_faction_num_castles, ":faction_castles"),
	  (faction_set_slot, ":pretender_faction", slot_faction_num_towns, ":faction_towns"),

	  #Point totals used below
	  #Faction Score A: (4 * towns) + (2 * castles) + villages
	  (store_mul, ":faction_score_a", ":faction_towns", 4),
	  (val_add, ":faction_score_a", ":faction_castles"),
	  (val_add, ":faction_score_a", ":faction_castles"),
	  (val_add, ":faction_score_a", ":faction_villages"),

	  #Faction Score B: (3 * towns) + (2 * castles) + villages
	  (store_sub, ":faction_score_b", ":faction_score_a", ":faction_towns"),

	  #Original Score A: (4 * towns) + (2 * castles) + villages
	  (store_mul, ":original_score_a", ":original_towns", 4),
	  (val_add, ":original_score_a", ":original_castles"),
	  (val_add, ":original_score_a", ":original_castles"),
	  (val_add, ":original_score_a", ":original_villages"),

	  #Original Score B: (3 * towns) + (2 * castles) + villages
	  (store_sub, ":original_score_b", ":faction_score_b", ":faction_towns"),

	  #The first fail-condition encountered will be the explanation used,
	  #so make sure the most pressing ones go first.
	  (try_begin),
	      #relation low: using the same cutoff normally used for becoming a vassal
		  (lt, ":player_relation", 0),
		  (assign, ":answer", -1),
		  (str_store_string, s14, "@Given the way things stand between us at the moment, {playername}, I would not consider it prudent to enter into such an arrangement."),
	  (else_try),
         #check player right to rule
		 (store_add, ":player_score", "$player_right_to_rule", ":player_relation"),
		 (this_or_next|lt, "$player_right_to_rule", 20),#the level required for your spouse to join a rebellion
			(lt, ":player_score", 100),
		 (assign, ":answer", -1),
		 (str_store_string, s14, "@{playername}, I am grateful to you, but in the eyes of the people you do not have sufficient legitimacy as a potential co-ruler.  Marrying you would undermine my own claim to the throne."),
	  (else_try),
         #check player renown
		 (store_mul, ":min_score", ":pretender_renown", 2),
		 (val_div, ":min_score", 3),#2/3 pretender renown, 750 by default
		 (val_clamp, ":min_score", 500, 1200),#500 is the minimum to begin the claimant quest; 1200 is the initial value for original lords #SB fixed comment

		 (lt, ":player_renown", ":min_score"),
		 (assign, ":answer", -1),
		 (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":player_renown"),
			(assign, reg1, ":min_score"),
			(display_message, "@{!}DEBUG - player renown {reg0}, required renown {reg1}"),
		  (try_end),
		 (str_store_string, s14, "@{playername}, I know that if it were not for you I would not sit on this throne, but your name is little renowned in Calradia.  Marrying you would be perceived as an uneven match and would call into question my own claim to the throne."),
	  (else_try),
		  #check player has sufficient fiefs
		  (store_mul, ":player_score", ":player_towns", 3),
		  (val_add, ":player_score", ":player_castles"),
		  (val_add, ":player_score", ":player_castles"),
		  (val_add, ":player_score", ":player_villages"),# player_score = (3 * towns) + (2 * castles) + villages

		  (assign, ":min_score", 6),#A town, a castle, and a village; two towns; three castles; six villages; etc...

		  (try_begin),
			#Ensure the minimum is not unreasonable on small maps.
			(lt, ":original_score_b", 18),
			(lt, ":faction_score_b", 18),
			(assign, reg0, ":original_score_b"),
			(val_max, reg0, ":faction_score_b"),
			(store_div, ":min_score", reg0, 3),
		  (try_end),

		  (troop_get_slot, ":two_thirds_pretender_score", ":pretender", slot_troop_temp_slot),
		  (val_mul, ":two_thirds_pretender_score", 2),
		  (val_add, ":two_thirds_pretender_score", 1),
		  (val_div, ":two_thirds_pretender_score", 3),
		  (val_max, ":min_score", ":two_thirds_pretender_score"),

		  (lt, ":player_score", ":min_score"),
		  (assign, ":answer", -1),
		  (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":player_score"),
			(assign, reg1, ":min_score"),
			(display_message, "@{!}DEBUG - player score {reg0} out of a required {reg1}"),
		  (try_end),
		  (str_store_string, s14, "@{playername}, I am grateful for your assistance in regaining my rightful throne, but you do not have sufficient personal holdings to be a suitable match for me.  It would be an uneven partnership."),
     (else_try),
	      #does the player have as much renown as competitors?
		  (lt, ":player_renown", ":c_renown"),
	      (assign, ":answer", -1),
		  (str_store_troop_name, s14, ":c"),
		  (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":player_renown"),
			(assign, reg1, ":c_renown"),
			(display_message, "@{!}DEBUG - player score {reg0}, competitor score {reg1}"),
		  (try_end),
		  (str_store_string_reg, s0, s15),#clobber s0, save s15
		  (call_script, "script_troop_describes_troop_to_s15", ":pretender", ":c"),
		  (str_store_string, s14, "@{playername}, I am grateful to you, but if I were to accept at this time I would risk offending powerful lords such as {s15}, who may consider themselves to have honor equal to or greater than your own."),
		  (str_store_string_reg, s15, s0),#revert s15
	 (else_try),
	      #is the player outfieffed by a competitor?
          (gt, ":highest_score_lord", "trp_player"),
          (neq, ":highest_score_lord", ":pretender"),

		  (store_mul, ":player_score", ":player_towns", 3),
		  (val_add, ":player_score", ":player_castles"),
		  (val_add, ":player_score", ":player_castles"),
		  (val_add, ":player_score", ":player_villages"),# player_score = (3 * towns) + (2 * castles) + villages
             (lt, ":player_score", ":highest_score"),

		  (store_mul, reg0, ":highest_score", 3),#allow small differences
		  (val_add, reg0, 2),
		  (val_div, reg0, 4),
		  (gt, reg0, ":player_score"),

	     (assign, ":answer", -1),
		  (str_store_troop_name, s14, ":highest_score_lord"),
		  (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":player_score"),
			(assign, reg1, ":highest_score"),
			(display_message, "@{!}DEBUG - player score {reg0}, competitor score {reg1}"),
		  (try_end),
		  (str_store_string_reg, s0, s15),#clobber s0, save s15
		  (call_script, "script_troop_describes_troop_to_s15", ":pretender", ":highest_score_lord"),
		  (str_store_string, s14, "@{playername}, I am grateful to you, but if I were to accept at this time I would risk offending great lords such as {s15}, who may consider themselves to have honor equal to or greater than your own."),
		  (str_store_string_reg, s15, s0),#revert s15
      (else_try),
		  #does the player have as much relation as competitors?
		  (lt, ":player_relation", ":b_relation"),
		  (ge, ":b_relation", 5),
		  (assign, ":answer", -1),
		 (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":player_relation"),
			(assign, reg1, ":b_relation"),
			(display_message, "@{!}DEBUG - player relation {reg0}, rival relation {reg1}"),
		  (try_end),
		  (str_store_string_reg, s0, s15),#clobber s0, save s15
		  (call_script, "script_troop_describes_troop_to_s15", ":pretender", ":b"),
		  (str_store_string, s14, "@{playername}, while I am grateful to you, I must confess I am fond of {s15}."),
		  (str_store_string_reg, s15, s0),#revert s15
	  (else_try),
		  #check: sufficient lords?
		  (assign, ":needed_lords", 1),
		  (try_for_range, ":troop_no", lords_begin, lords_end),
			(troop_slot_eq, ":troop_no", slot_troop_original_faction, ":pretender_faction"),
			(val_add, ":needed_lords", 1),
		  (try_end),
		  #Must be at least 75% of original size
		  (val_mul, ":needed_lords", 3),
		  (val_div, ":needed_lords", 4),

		  (lt, ":faction_lords", ":needed_lords"),
		  (assign, ":answer", -1),
		  (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":faction_lords"),
			(assign, reg1, ":needed_lords"),
			(display_message, "@{!}DEBUG - lords in faction {reg0}, required lords {reg1}"),
		  (try_end),

		  (str_store_string, s14, "@Our realm has too few vassals.  In the current precarious state of the affairs I must use the lure of a potential political alliance to attract new vassals, and cannot yet be seen to commit to any single {reg65?suitor:candidate}."),
	  (else_try),
		  #check: pretender has enough fiefs?
		  #Must not be exceeded in fiefs by anyone in the faction.
		  (store_mul, ":pretender_score", ":pretender_towns", 3),
		  (val_add, ":pretender_score", ":pretender_castles"),
		  (val_add, ":pretender_score", ":pretender_castles"),
		  (val_add, ":pretender_score", ":pretender_villages"),
		  (troop_set_slot, ":pretender", slot_troop_temp_slot, ":pretender_score"),

		  (store_mul, reg0, ":highest_score", 3),#allow small differences
		  (val_add, reg0, 2),
		  (val_div, reg0, 4),

		  (gt, reg0, ":pretender_score"),

		  (assign, ":answer", -1),
		  (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg1, reg0),
			(assign, reg0, ":pretender_score"),
			(display_message, "@{!}DEBUG - liege has {reg0} center points, needs at least {reg1}"),
		  (try_end),
		  (str_store_string_reg, s0, s15),#clobber s0, save s15
		  (call_script, "script_troop_describes_troop_to_s15", ":pretender", ":highest_score_lord"),
		  (str_store_string, s14, "@Because I have insufficient personal holdings compared to {s15}, if I entered into such an arrangement I would risk appearing to be a puppet, throwing the stability of the realm into jeopardy."),
		  (str_store_string_reg, s15, s0),#revert s15
	 (else_try),
		  #Check if pretender has enough fiefs, part 2.
		  #Must not have fewer fief points than the number of faction points divided by the
		  #number of lords (so this condition can't be bypassed by just failing to assign
		  #centers to anyone during the rebellion)
		  (store_mul, ":points_per_lord", ":faction_towns", 3),
		  (val_add, ":points_per_lord", ":faction_castles"),
		  (val_add, ":points_per_lord", ":faction_castles"),
		  (val_add, ":points_per_lord", ":faction_villages"),
		  (val_div, ":points_per_lord", ":faction_lords"),#includes pretender so cannot be zero

		  (gt, ":points_per_lord", ":pretender_score"),

		  (assign, ":answer", -1),
		  (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":pretender_score"),
			(assign, reg1, ":points_per_lord"),
			(display_message, "@{!}DEBUG - liege has {reg0} center points, needs at least {reg1}"),
		  (try_end),
		  (str_store_faction_name, s14, ":pretender_faction"),
		  (str_store_string, s14, "@Because my personal holdings are insufficiently large compared to other lords of the {s14}, if I entered into such an arrangement I would risk appearing to be a puppet, throwing the stability of the realm into jeopardy."),
	  (else_try),
		  #check if player is widely hated in faction
		  (assign, ":total_negative", 0),
		  (assign, ":total_enemies", 0),
		  (assign, ":total_positive", 0),
		  (assign, ":total_friends", 0),
		  (try_for_range, ":troop_no", heroes_begin, heroes_end),
		     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (store_troop_faction, reg0, ":troop_no"),
			 (eq, reg0, ":pretender_faction"),
			 (call_script, "script_troop_get_player_relation", ":troop_no"),
			 (try_begin),
				(lt, reg0, 0),
				(val_add, ":total_negative", 1),
				(lt, reg0, -19),
				(val_add, ":total_enemies", 1),
			 (else_try),
				(gt, reg0, 0),
				(val_add, ":total_positive", 1),
				(gt, reg0, 19),
				(val_add, ":total_friends", 1),
			 (try_end),
		  (try_end),
		  #Must not have a "disapproval rating" of over 33%
		  (val_mul, ":total_enemies", 2),
		  (val_mul, ":total_negative", 2),
		  (this_or_next|gt, ":total_enemies", ":total_friends"),
		     (gt, ":total_negative", ":total_positive"),

		  (assign, ":answer", -1),
		  (str_store_faction_name, s14, ":pretender_faction"),
		  (str_store_string, s14, "@I am grateful to you, {playername}, but you have too many enemies among the lords of the {s14} for your proposal to be politically viable.  If I were to accept, there might be a revolt."),
	  (else_try),
		  #controversy must be less than 25, and less than half the relation with the liege
		  (troop_get_slot, ":controversy_2", "trp_player", slot_troop_controversy),
		  (ge, ":controversy_2", 1),
		  (val_mul, ":controversy_2", 2),
		  (this_or_next|ge, ":controversy_2", 50),
		     (ge, ":controversy_2", ":player_relation"),
		  (assign, ":answer", -1),
		  (str_store_faction_name, s14, ":pretender_faction"),
		  (str_store_string, s14, "@You have engendered too much controversy recently, {playername} .  If I were to accept at this time, there might be a revolt among the lords of the {s14}.  Let us speak of this later when the furor has died down."),
	  (else_try),
		  #check is marshall
		  (neg|faction_slot_eq, ":pretender_faction", slot_faction_marshall, "trp_player"),
		  (assign, ":answer", -2),#<-- negative two, not -1
		  (str_store_faction_name, s14, ":pretender_faction"),
		  (str_store_string, s14, "@If you desire to lead the {s14} alongside me, gather support among my vassals to become marshall, and demonstrate to them your abilities as a war leader."),
	  (else_try),
		  #player is marshall: is the territory sufficient?

		  #The faction must have at least 80% of its former territory under scoring system A or scoring system B.
		  (store_mul, ":four_fifths_original_score_a", ":original_score_a", 4),
		  (val_div, ":four_fifths_original_score_a", 5),

		  (store_mul, ":four_fifths_original_score_b", ":original_score_b", 4),
		  (val_div, ":four_fifths_original_score_b", 5),

		  (lt, ":faction_score_a", ":four_fifths_original_score_a"),
		  (lt, ":faction_score_b", ":four_fifths_original_score_b"),
		  (assign, ":answer", -3),

		  (call_script, "script_dplmc_print_centers_in_numbers_to_s0", ":original_towns", ":original_castles", ":original_villages"),
		  (str_store_string_reg, s1, s0),
		  (call_script, "script_dplmc_print_centers_in_numbers_to_s0", ":faction_towns", ":faction_castles", ":faction_villages"),

		  (str_store_faction_name, s14, ":pretender_faction"),
		  (str_store_string, s14, "@Our realm has lost too much territory.  We once held {s1} but now only hold {s0}.  In the current precarious state of affairs I must retain the possibility of a political alliance to use as a bargaining chip with the other sovereigns, so I yet be seen to commit to any single {reg65?suitor:candidate}.  Restore the {s14} to its former glory, and I will gladly have you rule beside me as my {husband/wife}."),
	  (else_try),
		 #player is marshall: are any native centers lost?

		 (str_clear, s0),
		 (str_clear, s1),
		 (assign, ":num_lost_towns_and_castles", 0),

		 (try_for_range, ":center_no", centers_begin, centers_end),
			(party_slot_eq, ":center_no", slot_center_original_faction, ":pretender_faction"),
			(store_faction_of_party, ":center_faction", ":center_no"),
			(neq, ":center_faction", ":pretender_faction"),
			(neq, ":center_faction", "fac_player_supporters_faction"),
			(try_begin),
				(eq, ":num_lost_towns_and_castles", 0),
				(str_store_party_name, s0, ":center_no"),
			(else_try),
				(eq, ":num_lost_towns_and_castles", 1),
				(str_store_party_name, s1, ":center_no"),
			(else_try),
				(str_store_string, s0, "str_dplmc_s0_comma_s1"),
				(str_store_party_name, s1, ":center_no"),
			(try_end),
			(val_add, ":num_lost_towns_and_castles", 1),
		 (try_end),
		 #post-loop cleanup
		 (try_begin),
			(ge, ":num_lost_towns_and_castles", 2),
			(str_store_string, s0, "str_dplmc_s0_and_s1"),
		 (try_end),
		 #native towns lost
		 (ge, ":num_lost_towns_and_castles", 1),
		 (store_sub, reg0, ":num_lost_towns_and_castles", 1),
		 (str_store_faction_name, s14, ":pretender_faction"),
		 (str_store_string, s14, "@{s0} {reg0?have:has} been lost to foreign hands.  Restore the {s14} to its rightful boundaries, and I will gladly have you rule beside me as my {husband/wife}."),
		 (assign, ":answer", -3),
	  (else_try),
	  #Timer answer
	     (lt, "$g_player_days_as_marshal", 14),
		  (assign, reg0, "$g_player_days_as_marshal"),
		  (store_sub, reg1, reg0, 1),
		  (str_store_faction_name, s14, ":pretender_faction"),
		  (str_store_string, s14, "@You have only been marshall for {reg0} {reg1?days:day}.  Let us speak of this after you have held the post for at least two weeks."),
		  (assign, ":answer", -4),
	  (else_try),
		#In the future we may need a proper quest of some kind, or at least a timer, but this will do for now.
		(assign, ":answer", 1),
		(str_store_faction_name, s14, ":pretender_faction"),
		(str_store_string, s14, "@If not for you I would not sit on this throne, {playername}.  When we started our long walk, few people had the courage to support me.  And fewer still would be willing to put their lives at risk for my cause.  But you didn't hesitate for a moment in throwing yourself at my enemies. We have gone through a lot together, and with God's help, we prevailed.  I will gladly accept you as both my {husband/wife} and co-ruler of the {s14}."),
	  (try_end),

	  (assign, reg65, ":save_reg65"),
	  (assign, reg1, ":save_reg1"),
	  (assign, reg0, ":answer"),
  ])
]
