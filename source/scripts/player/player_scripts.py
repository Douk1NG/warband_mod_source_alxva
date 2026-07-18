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

player_scripts = [

(
   "change_player_right_to_rule",
   [
     (store_script_param_1, ":right_to_rule_dif"),
     (val_add, "$player_right_to_rule", ":right_to_rule_dif"),
     (val_clamp, "$player_right_to_rule", 0, 100),
     (try_begin),
       (gt, ":right_to_rule_dif", 0),
       (display_message, "@You gain right to rule.", message_positive),
     (else_try),
       (lt, ":right_to_rule_dif", 0),
       (display_message, "@You lose right to rule.", message_negative),
     (try_end),
   ]),

("player_arrived",
   [
      # (assign, ":player_faction_culture", "fac_culture_1"),
      #SB : align start faction culture
      (party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
      (party_get_slot, ":player_faction_culture", "$g_starting_town", slot_center_culture),
      (faction_set_slot, "fac_player_supporters_faction",  slot_faction_culture, ":player_faction_culture"),
      (faction_set_slot, "fac_player_faction",  slot_faction_culture, ":player_faction_culture"),
      (party_set_morale, "p_main_party", 100),
    ]),

("setup_talk_info",
    [
      # ##diplomacy start+ Ensure $character_gender is set correctly (it should have been set during character creation)
      # (try_begin),
         # (call_script, "script_cf_dplmc_troop_is_female", "trp_player"),
         # (assign, "$character_gender", tf_female),
      # (else_try),
         # (assign, "$character_gender", tf_male),
      # (try_end),
      # ##diplomacy end+
      #SB : redo order
      (talk_info_set_relation_bar, "$g_talk_troop_relation"),
      (str_store_troop_name, s61, "$g_talk_troop"),
      # (str_store_string, s61, "@{!} {s61}"),
      (assign, reg1, "$g_talk_troop_relation"),
      # (str_store_string, s62, "str_relation_reg1"),
      (talk_info_set_line, 0, "@{!} {s61}"),
      (talk_info_set_line, 1, "str_relation_reg1"),
      (call_script, "script_describe_relation_to_s63", "$g_talk_troop_relation"),
      (talk_info_set_line, 3, s63),
  ]),

("loot_player_items",
    [
      (store_script_param, ":enemy_party_no", 1),
	  ##diplomacy start+ some enemy lords will not loot the personal equipment of a player who surrendered
	  (assign, ":save_reg0", reg0),
	  (assign, ":extra_gold", 0),
	  #I am not sure if this is historical or not, but it gives the player a reason to
	  #surrender (rather than fight to the end) even before permanent attribute loss is
	  #a possibility (or even if it is disabled outright).
	  #
	  #This also adds another layer of interaction, and makes different lords feel
	  #different from each other.
	  #
	  #Other changes:
	  # Enemy lords will receive gold they loot from the player,
	  # Books will not be looted from the player (it turns out a bug was responsible for this being possible)
	  # The enemy leader's looting skill will affect the amount of gold lootable.
	  (assign, ":merciful", 0),
	  (assign, ":party_leader", -1),
	  (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
	  (try_begin),
 	    (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#only use this if it is explicitly enabled
	    #Possibility the player's personal equipment will be untouched if he surrendered
  	    (ge, "$g_player_surrenders", 1),
   	    (gt, ":enemy_party_no", 0),
		(party_stack_get_troop_id, ":party_leader", ":enemy_party_no", 0),
	   #(party_slot_eq, ":enemy_party_no", slot_party_type, spt_kingdom_hero_party),
		(ge, ":party_leader", walkers_end),
		(troop_is_hero, ":party_leader"),
		(call_script, "script_troop_get_player_relation", ":party_leader"),
		(assign, ":relation", reg0),
		(assign, ":probability_modifier", 0),
		(try_begin),
			#Upstanding lords are inclined to honor deals in general, and will automatically
			#do so with honorable lords they do not extremely dislike.  However, this does not
			#extend to commoners.
			(troop_slot_ge, "trp_player", slot_troop_banner_scene_prop, 1),# the player has a coat of arms
			(troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_upstanding),
			(val_max, ":probability_modifier", 10),#set to +10 unless already higher
			#They will automatically honor deals with the honorable, if they do not
			#excessively dislike them.
			(ge, "$player_honor", 1),
			(val_add, reg0, 10),
			(val_clamp, reg0, 11, 21),
			(val_max, ":probability_modifier", reg0),#set somewhere from +11 to +20 unless already higher
			(ge, ":relation", -10),
			(assign, ":merciful", 1),
		(else_try),
			#Martial lords are inclined to honor deals with lords who likewise follow the rules of war,
			#and will do so as long as they are neutral or friendly towards them.  This does not extend
			#to commoners.
			(troop_slot_ge, "trp_player", slot_troop_banner_scene_prop, 1),# the player has a coat of arms
			(this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_moralist),
			(troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_martial),
			(ge, "$player_honor", 1),
			(assign, reg0, "$player_honor"),
			(val_clamp, reg0, 1, 6),
			(val_max, ":probability_modifier", reg0),#set somewhere from +1 to +5 unless already higher
			(ge, ":relation", 0),
			(assign, ":merciful", 1),
		(else_try),
			#Good-natured lords are inclined to honor deals with everyone, commoner or not.
			#They will do so automatically unless they particularly dislike someone.
			#This also goes for Moralist ladies if they someone end up accepting your surrender.
			(this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_goodnatured),
			(troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_moralist),
			(val_max, ":probability_modifier", 21),#set to +20 unless already higher
			(ge, ":relation", -10),
			(assign, ":merciful", 1),
		(else_try),
			#Honest lords are inclined honor deals with everyone, commoner or not.
			#They will do so automatically unless they particularly dislike someone.
			(call_script, "script_dplmc_get_troop_morality_value", ":party_leader", tmt_honest),
			(assign, ":honest_val", reg0),
			(ge, ":honest_val", 1),
			(store_add, reg0, ":honest_val", 14),
			(val_max, ":probability_modifier", reg0),#set to (14 + honesty ) unless already higher
			(ge, "$player_honor", 1),
			(val_mul, reg0, -1),
			(ge, ":relation", reg0),
			(assign, ":merciful", 1),
		(else_try),
			(try_begin),
				#Penalty instead of bonus for vicious lord personalities, unless they are
				#explicitly set as honest.  (None are by default.)
				(lt, ":honest_val", 1),#Must either be negative or not given
				(this_or_next|lt, ":honest_val", 0),
				(this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_debauched),
				(this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_selfrighteous),
				(this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_cunning),
				(troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_quarrelsome),
				(val_min, ":probability_modifier", -10),#set to -10 unless already lower
			(try_end),
			#Now store into reg0 the percent chance of mercy
			(try_begin),
				(le, ":reduce_campaign_ai", 0),#Hard: base chance 25% + relation
				(store_add, reg0, ":relation", 25),
			(else_try),
				(eq, ":reduce_campaign_ai", 1),#Medium: base chance 50% + relation
				(store_add, reg0, ":relation", 50),
			(else_try),
				(ge, ":reduce_campaign_ai", 2),#Easy: base chance 75% + relation
				(store_add, reg0, ":relation", 75),
			(try_end),
			(val_add, reg0, ":probability_modifier"),#modify the chance based on the captor's personality
			(val_max, reg0, ":probability_modifier"),#at least this much of a chance
			(val_max, reg0, 5),#at least a 5% chance
			(store_random_in_range, ":probability_modifier", 1, 101),
			(lt, reg0, ":probability_modifier"),
			(assign, ":merciful", 1),
		(try_end),
	  (else_try),
  	   (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#only use this if it is explicitly enabled
		#Surrendered to a non-hero party
		(gt, ":enemy_party_no", 0),
		(ge, "$g_player_surrenders", 1),
		(store_random_in_range, reg0, 1, 101),
		(this_or_next|lt, reg0, 25),#Hard: 25% chance
			(ge, ":reduce_campaign_ai", 1),
		(this_or_next|lt, reg0, 50),#Medium: 50% chance
			(ge, ":reduce_campaign_ai", 2),
		(lt, reg0, 75),#Easy: 75% chance
		(assign, ":merciful", 1),
	  (try_end),
	  (try_begin),
		(ge, "$cheat_mode", 1),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#don't display when nonapplicable
		(assign, ":save_reg1", reg1),
		(assign, reg0, "$g_player_surrenders"),
		(assign, reg1, ":merciful"),
		(display_message, "@{!} DEBUG loot_player_items: g_player_surrenders = {reg0}, merciful = {reg1}"),
        (assign, reg1, ":save_reg1"),
	  (try_end),
	  ##diplomacy end+
      (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
      (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
        (ge, ":item_id", 0),
		##diplomacy start+ looting changes
		(neg|is_between, ":item_id", books_begin, books_end),#shouldn't be necessary, but just in case
		(assign, ":randomness", 0),#properly initialize variables
		##diplomacy end+
        (troop_get_inventory_slot_modifier, ":item_modifier", "trp_player", ":i_slot"),
        (try_begin),
          (is_between, ":item_id", trade_goods_begin, trade_goods_end),
          (assign, ":randomness", 20),
        (else_try),
          (this_or_next|is_between, ":item_id", horses_begin, horses_end),
          (this_or_next|eq, ":item_id", "itm_warhorse_sarranid"),
          (eq, ":item_id", "itm_warhorse_steppe"),
          (assign, ":randomness", 15),
        (else_try),
          (this_or_next|is_between, ":item_id", weapons_begin, weapons_end),
          (is_between, ":item_id", ranged_weapons_begin, ranged_weapons_end),
          (assign, ":randomness", 5),
        (else_try),
          (this_or_next|is_between, ":item_id", armors_begin, armors_end),
		  (this_or_next|eq, ":item_id", "itm_plate_boots"), #added to the end because of not breaking the save games
          (is_between, ":item_id", shields_begin, shields_end),
          (assign, ":randomness", 5),
        (try_end),
        (store_random_in_range, ":random_no", 0, 100),
        (lt, ":random_no", ":randomness"),
		##diplomacy start+ changes
		(try_begin),
			#If this option is enabled, personal items may be spared, and instead
			#sligthly more gold is taken (but not as much as the thing's worth).
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
			(ge, ":merciful", 1),
			(is_between, ":i_slot", ek_item_0, dplmc_ek_alt_items_end),
			(assign, ":random_no", 101),
			#(store_item_value, reg0, ":item_id"),#don't bother with imods #don't bother with the rest of this
			#(val_div, reg0, 2),
			#(ge, reg0, 1),
			#(val_add, ":extra_gold", reg0),##disable, as it defeats the point!
		(try_end),
		(lt, ":random_no", ":randomness"),
		##diplomacy end+
        (troop_remove_item, "trp_player", ":item_id"),

        (try_begin),
          (gt, ":enemy_party_no", 0),
          (party_get_slot, ":cur_loot_slot", ":enemy_party_no", slot_party_next_looted_item_slot),
          (val_add, ":cur_loot_slot", slot_party_looted_item_1),
          (party_set_slot, ":enemy_party_no", ":cur_loot_slot", ":item_id"),
          (val_sub, ":cur_loot_slot", slot_party_looted_item_1),
          (val_add, ":cur_loot_slot", slot_party_looted_item_1_modifier),
          (party_set_slot, ":enemy_party_no", ":cur_loot_slot", ":item_modifier"),
          (val_sub, ":cur_loot_slot", slot_party_looted_item_1_modifier),
          (val_add, ":cur_loot_slot", 1),
          (val_mod, ":cur_loot_slot", num_party_loot_slots),
          (party_set_slot, ":enemy_party_no", slot_party_next_looted_item_slot, ":cur_loot_slot"),
        (try_end),
      (try_end),
      (store_troop_gold, ":cur_gold", "trp_player"),
      (store_div, ":max_lost", ":cur_gold", 5),
      (store_div, ":min_lost", ":cur_gold", 10),
      (store_random_in_range, ":lost_gold", ":min_lost", ":max_lost"),
	  ##diplomacy start+
	  (try_begin),
		#This does nothing unless the option is enabled.
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		#add extra gold from enemy's looting skill
		(gt, ":enemy_party_no", 0),
		(party_get_skill_level, reg0, ":enemy_party_no", "skl_looting"),
		(val_clamp, reg0, 0, 11),#allow range +0 to +10
		(val_add, reg0, 10),
		(val_mul, ":lost_gold", reg0),
		(val_div, ":lost_gold", 10),
		#Add any gold from items not looted.
		(val_add, ":lost_gold", ":extra_gold"),
		#gold looted can't exceed player's actual gold
		(val_min, ":lost_gold", ":cur_gold"),
		(val_max, ":lost_gold", 0),
      (try_end),
	  #diplomacy end+
      (troop_remove_gold, "trp_player", ":lost_gold"),
	  ##diplomacy start+
	  (try_begin),
	    #add looted gold to the enemy, if he's a valid hero
		(is_between, ":party_leader", heroes_begin, heroes_end),
		(troop_is_hero, ":party_leader"),
		(neq, ":party_leader", "trp_player"),
		(neq, ":party_leader", "trp_kingdom_heroes_including_player_begin"),
		(ge, ":lost_gold", 1),
		#(call_script, "script_troop_add_gold", ":party_leader", ":lost_gold"),#add looted gold to enemy
		(troop_get_slot, reg0, ":party_leader", slot_troop_wealth),
		(val_add, reg0, ":lost_gold"),
		(val_max, reg0, 0),
		(troop_set_slot, ":party_leader", slot_troop_wealth, reg0),#add looted gold to enemy
	  (try_end),
	  (assign, reg0, ":save_reg0"),#revert register
	  ##diplomacy end+
      ]),

("party_give_xp_and_gold",
    [
      (store_script_param_1, ":enemy_party"), #Party_id

      (call_script, "script_calculate_main_party_shares"),
      (assign, ":num_player_party_shares", reg0),

      (assign, ":total_gain", 0),
      (party_get_num_companion_stacks, ":num_stacks",":enemy_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":enemy_party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size, ":stack_size",":enemy_party",":i_stack"),
        (store_character_level, ":level", ":stack_troop"),
        (store_add, ":gain", ":level", 10),
        (val_mul, ":gain", ":gain"),
        (val_div, ":gain", 10),
        (store_mul, ":stack_gain", ":gain", ":stack_size"),
        (val_add, ":total_gain", ":stack_gain"),
      (try_end),

      (val_mul, ":total_gain", "$g_strength_contribution_of_player"),
      (val_div, ":total_gain", 100),

      (val_min, ":total_gain", 40000), #eliminate negative results

      (assign, ":player_party_xp_gain", ":total_gain"),

      (store_random_in_range, ":r", 50, 100),
      (val_mul, ":player_party_xp_gain", ":r"),
      (val_div, ":player_party_xp_gain", 100),

      (party_add_xp, "p_main_party", ":player_party_xp_gain"),

      (store_mul, ":player_gold_gain", ":total_gain", player_loot_share),
      (val_min, ":player_gold_gain", 60000), #eliminate negative results
      (store_random_in_range, ":r", 50, 100),
      (val_mul, ":player_gold_gain", ":r"),
      (val_div, ":player_gold_gain", 100),
      (val_div, ":player_gold_gain", ":num_player_party_shares"),

      #add gold now
      (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (call_script, "script_troop_add_gold", ":stack_troop", ":player_gold_gain"),
        (try_end),
      (try_end),
  ]),

("setup_troop_meeting",
    [
      (store_script_param_1, ":meeting_troop"),
      (store_script_param_2, ":troop_dna"),
      (call_script, "script_get_meeting_scene"),
      (assign, ":meeting_scene", reg0),
      (modify_visitors_at_site,":meeting_scene"),
      (reset_visitors),
      (set_visitor,0,"trp_player"),
	  (try_begin),
		(gt, ":troop_dna", -1),
        (troop_set_slot, "trp_temp_array_c", 17, ":troop_dna"),
        (set_visitor,17,":meeting_troop",":troop_dna"),
	  (else_try),
        (set_visitor,17,":meeting_troop"),
	  (try_end),
      (set_jump_mission,"mt_conversation_encounter"),
      (jump_to_scene,":meeting_scene"),
      (change_screen_map_conversation, ":meeting_troop"),
  ]),

("setup_party_meeting",
    [
      (store_script_param_1, ":meeting_party"),
      (try_begin),
        (lt, "$g_encountered_party_relation", 0), #hostile
#        (call_script, "script_music_set_situation_with_culture", mtf_sit_encounter_hostile),
      (try_end),
      (call_script, "script_get_meeting_scene"), (assign, ":meeting_scene", reg0),
      (modify_visitors_at_site,":meeting_scene"),(reset_visitors),
      (set_visitor,0,"trp_player"),
      (party_stack_get_troop_id, ":meeting_troop",":meeting_party",0),
      (party_stack_get_troop_dna,":troop_dna",":meeting_party",0),
      (set_visitor,17,":meeting_troop",":troop_dna"),
      (set_jump_mission,"mt_conversation_encounter"),
      (jump_to_scene,":meeting_scene"),
      (change_screen_map_conversation, ":meeting_troop"),
  ]),

("troop_get_player_relation",
      [
        (store_script_param_1, ":troop_no"),
        (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
        (troop_get_slot, ":effective_relation", ":troop_no", slot_troop_player_relation),
        (assign, ":honor_bonus", 0),
        (try_begin),
          (eq,  ":reputation", lrep_quarrelsome),
          (val_add, ":effective_relation", -3),
        (try_end),
        (try_begin),
          (ge, "$player_honor", 0),
          (try_begin),
            (this_or_next|eq,  ":reputation", lrep_upstanding),
            (             eq,  ":reputation", lrep_goodnatured),
             (store_div, ":honor_bonus", "$player_honor", 3),
		  ##diplomacy start+
		  (else_try),
			#In general this should not apply to ladies, as they operate by different
			#reputation rules, but if a "kingdom lady" has become a "kingdom hero" instead,
			#it should apply.
		     (eq,  ":reputation", lrep_moralist),#-- verify that the lady is effectively a lord:
		     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (store_div, ":honor_bonus", "$player_honor", 3),
		  (else_try),
			 #Personality type that values keeping your word
			 (call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_honest),
			 (ge, reg0, 1),
			 (store_div, ":honor_bonus", "$player_honor", 3),
		  ##diplomacy end+
          (try_end),
        (try_end),
        (try_begin),
          (lt, "$player_honor", 0),
          (try_begin),
            (this_or_next|eq,  ":reputation", lrep_upstanding),
            (             eq,  ":reputation", lrep_goodnatured),
            (store_div, ":honor_bonus", "$player_honor", 3),
          ##diplomacy start+
		  (else_try),
			(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_honest),
			(ge, reg0, 1),#Personality type that values keeping your word
			(store_div, ":honor_bonus", "$player_honor", 3),
		  (else_try),
		  	 #"My kind of scum" - a few rare individuals might actively approve.
		  	 (lt, reg0, 0),#<-- must have negative value for tmt_honest; by default this is only Rolf.
		  	 (this_or_next|eq, ":reputation", lrep_roguish),
		  	 (this_or_next|eq, ":reputation", lrep_custodian),
		  	 (this_or_next|eq, ":reputation", lrep_debauched),
		  	 (this_or_next|eq, ":reputation", lrep_ambitious),
		  		(eq, ":reputation", lrep_cunning),
		  	 (store_div, ":honor_bonus", "$player_honor", -5),
		  	 (val_clamp, ":honor_bonus", 1, 6),
          (else_try),
			#"Honorable" lords can be awful people, so no bonus with benefactors,
			#but dishonorable lords are *guaranteed* to be awful.
            (eq, ":reputation", lrep_benefactor),
            (store_div, ":honor_bonus", "$player_honor", 5),
		  (else_try),
			#Self-righteous lords are moralizing but hypocritical.
			(eq, ":reputation", lrep_selfrighteous),
			(store_div, ":honor_bonus", "$player_honor", 5),
		  (else_try),
			 #In general this should not apply to ladies, as they operate by different
			 #reputation rules, but if a "kingdom lady" has become a "kingdom hero" instead,
			 #it should apply.
			 (eq,  ":reputation", lrep_moralist),#-- verify that the lady is effectively a lord:
		     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (store_div, ":honor_bonus", "$player_honor", 3),
		  (else_try),
			 (eq,  ":reputation", lrep_conventional),#-- verify that the lady is effectively a lord:
		     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (store_div, ":honor_bonus", "$player_honor", 5),
          ##diplomacy end+
          (else_try),
            (eq,  ":reputation", lrep_martial),
            (store_div, ":honor_bonus", "$player_honor", 5),
          (try_end),
        (try_end),
        (val_add, ":effective_relation", ":honor_bonus"),
        (val_clamp, ":effective_relation", -100, 101),
        (assign, reg0, ":effective_relation"),
    ]),

("change_troop_renown",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":renown_change"),

      (troop_get_slot, ":old_renown", ":troop_no", slot_troop_renown),

	  (try_begin),
		(gt, ":renown_change", 0),
		(assign, reg4, ":renown_change"),

		(store_div, ":subtraction", ":old_renown", 200),
	    (val_sub, ":renown_change", ":subtraction"),
	    (val_max, ":renown_change", 0),

	    (eq, ":troop_no", "trp_player"),
	    (assign, reg5, ":renown_change"),

		(eq, "$cheat_mode", 1),
	    (display_message, "str_renown_change_of_reg4_reduced_to_reg5_because_of_high_existing_renown"),
	  (try_end),

      (store_add, ":new_renown", ":old_renown", ":renown_change"),
      (val_max, ":new_renown", 0),
      (troop_set_slot, ":troop_no", slot_troop_renown, ":new_renown"),

      (try_begin),
        (eq, ":troop_no", "trp_player"),

		(try_begin),
		  (ge, ":new_renown", 50),

          (try_begin),
            (troop_get_type, ":is_female", "trp_player"),
            (eq, ":is_female", 1),
            (unlock_achievement, ACHIEVEMENT_TALK_OF_THE_TOWN),
          (try_end),
		(try_end),

        # (str_store_troop_name, s1, ":troop_no"),
        (assign, reg12, ":renown_change"),
        (val_abs, reg12),
        (try_begin),
         (gt, ":renown_change", 0),
         (display_message, "@You gained {reg12} renown.", message_positive),
        (else_try),
          (lt, ":renown_change", 0),
          (display_message, "@You lose {reg12} renown.", message_negative),
        (try_end),
      (try_end),
      (call_script, "script_update_troop_notes", ":troop_no"),
  ]),

("change_player_relation_with_troop",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":difference"),

      (try_begin),
        (neq, ":troop_no", "trp_player"),
        (neg|is_between, ":troop_no", soldiers_begin, soldiers_end),
        ##diplomacy start+
		  (neq, ":troop_no", "trp_kingdom_heroes_including_player_begin"),
		  #(neq, ":troop_no", -1),#OLD
		  (ge, ":troop_no", 1),#NEW
        ##diplomacy end+
        (neq, ":difference", 0),
        (call_script, "script_troop_get_player_relation", ":troop_no"),
        (assign, ":old_effective_relation", reg0),
        (troop_get_slot, ":player_relation", ":troop_no", slot_troop_player_relation),
        (val_add, ":player_relation", ":difference"),
        (val_clamp, ":player_relation", -100, 101),
        (try_begin),
          (troop_set_slot, ":troop_no", slot_troop_player_relation, ":player_relation"),

          (try_begin),
            (le, ":player_relation", -50),
            (unlock_achievement, ACHIEVEMENT_OLD_DIRTY_SCOUNDREL),
          (try_end),

          (str_store_troop_name_link, s1, ":troop_no"),
          (call_script, "script_troop_get_player_relation", ":troop_no"),
          (assign, ":new_effective_relation", reg0),
          (neq, ":old_effective_relation", ":new_effective_relation"),
          (assign, reg1, ":old_effective_relation"),
          (assign, reg2, ":new_effective_relation"),
          (try_begin),
			##diplomacy start+ Suppress this message for dead people except in cheat mode
            (lt, "$cheat_mode", 1),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_dead),
			(neq, ":troop_no", "$g_talk_troop"),
		  (else_try),
		  ##diplomacy end+
            (gt, ":difference", 0),
            (display_message, "str_troop_relation_increased", message_positive),
          (else_try),
            (lt, ":difference", 0),
            (display_message, "str_troop_relation_detoriated", message_negative),
          (try_end),
          (try_begin),
            (eq, ":troop_no", "$g_talk_troop"),
            (assign, "$g_talk_troop_relation", ":new_effective_relation"),
            (call_script, "script_setup_talk_info"),
          (try_end),
          (call_script, "script_update_troop_notes", ":troop_no"),
        (try_end),
      (try_end),
  ]),

("change_player_honor",
    [
      (store_script_param_1, ":honor_dif"),
      ##diplomacy start+
      #Exacerbate the effect of honor losses as the player's honor increases
      (try_begin),
         (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),#<-- experimental settings must be enabled
         (ge, "$player_honor", 10),
         (lt, ":honor_dif", 0),
         (store_add, ":honor_multiplier", "$player_honor", 100),
         (val_mul, ":honor_dif", ":honor_multiplier"),
         (val_sub, ":honor_dif", 50),
         (val_div, ":honor_dif", 100),
      (try_end),
      ##diplomacy end+
      (val_add, "$player_honor", ":honor_dif"),
      (try_begin),
        (gt, ":honor_dif", 0),
        (display_message, "@You gain honour.", message_positive),
      (else_try),
        (lt, ":honor_dif", 0),
        (display_message, "@You lose honour.", message_negative),
      (try_end),

##      (val_mul, ":honor_dif", 1000),
##      (assign, ":temp_honor", 0),
##      (assign, ":num_nonlinear_steps", 10),
##      (try_begin),
##        (gt, "$player_honor", 0),
##        (lt, ":honor_dif", 0),
##        (assign, ":num_nonlinear_steps", 0),
##      (else_try),
##        (lt, "$player_honor", 0),
##        (gt, ":honor_dif", 0),
##        (assign, ":num_nonlinear_steps", 3),
##      (try_end),
##
##      (try_begin),
##        (ge, "$player_honor", 0),
##        (assign, ":temp_honor", "$player_honor"),
##      (else_try),
##        (val_sub, ":temp_honor", "$player_honor"),
##      (try_end),
##      (try_for_range, ":unused",0,":num_nonlinear_steps"),
##        (ge, ":temp_honor", 10000),
##        (val_div, ":temp_honor", 2),
##        (val_div, ":honor_dif", 2),
##      (try_end),
##      (val_add, "$player_honor", ":honor_dif"),
  ]),

("search_troop_prisoner_of_party",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":prisoner_of", -1),
      (try_for_parties, ":party_no"),
        (eq,  ":prisoner_of", -1),
        (this_or_next|eq, ":party_no", "p_main_party"),
        (ge, ":party_no", centers_begin),
        (party_count_prisoners_of_type, ":troop_found", ":party_no", ":troop_no"),
        (gt, ":troop_found", 0),
        (assign, ":prisoner_of", ":party_no"),
      (try_end),
      (assign, reg0, ":prisoner_of"),
  ]),

("calculate_renown_value",
   [
      ##diplomacy start+
	  #If terrain advantage is enabled, use it to avoid messing up cached
	  #strength values, but do not take it into consideration for renown
	  #granted.
	  (assign, ":main_party_strength", 1),
	  (assign, ":enemy_strength", 1),
	  (assign, ":friends_strength", 1),
	  (assign, ":terrain_code", -1),
	  (try_begin),
	     (eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
	     (try_begin),
	        (encountered_party_is_attacker),
		    (call_script, "script_dplmc_get_terrain_code_for_battle", "$g_encountered_party", "p_main_party"),
	     (else_try),
	        (call_script, "script_dplmc_get_terrain_code_for_battle", "p_main_party", "$g_encountered_party"),
		 (try_end),
		 (assign, ":terrain_code", reg0),
		 ##Alternate option: calculate with terrain, but don't use it for renown
		 #(but do use it to update the cached strength for the party)
		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_main_party", ":terrain_code",0,1),
		 (assign, ":main_party_strength", reg1),#use non-terrain version!
		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_enemy", ":terrain_code",0,1),
		 (assign, ":enemy_strength", reg1),#use non-terrain version!
		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_friends", ":terrain_code",0,1),
		 (assign, ":friends_strength", reg1),#use non-terrain version!
	  (else_try),
	      ##Original option: calculate without terrain
		  (call_script, "script_party_calculate_strength", "p_main_party", 0),
		  (assign, ":main_party_strength", reg0),
		  (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
		  (assign, ":enemy_strength", reg0),
		  (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
		  (assign, ":friends_strength", reg0),
	  (try_end),
	  ##diplomacy end+

      (val_add, ":friends_strength", 1),
      (store_mul, ":enemy_strength_ratio", ":enemy_strength", 100),
      (val_div, ":enemy_strength_ratio", ":friends_strength"),

      (assign, ":renown_val", ":enemy_strength"),
      (val_mul, ":renown_val", ":enemy_strength_ratio"),
      (val_div, ":renown_val", 100),

      (val_mul, ":renown_val", ":main_party_strength"),
      (val_div, ":renown_val",":friends_strength"),

      (store_div, "$battle_renown_value", ":renown_val", 5),
      (val_min, "$battle_renown_value", 2500),
      (convert_to_fixed_point, "$battle_renown_value"),
      (store_sqrt, "$battle_renown_value", "$battle_renown_value"),
      (convert_from_fixed_point, "$battle_renown_value"),
      (assign, reg8, "$battle_renown_value"),
      (display_message, "@Renown value for this battle is {reg8}.",0xFFFFFFFF),
  ]),

("get_max_skill_of_player_party",
    [(store_script_param, ":skill_no", 1),
     (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
     (store_skill_level, ":max_skill", ":skill_no", "trp_player"),
     (assign, ":skill_owner", "trp_player"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
       (troop_is_hero, ":stack_troop"),
       (neg|troop_is_wounded, ":stack_troop"),
       (store_skill_level, ":cur_skill", ":skill_no", ":stack_troop"),
       (gt, ":cur_skill", ":max_skill"),
       (assign, ":max_skill", ":cur_skill"),
       (assign, ":skill_owner", ":stack_troop"),
     (try_end),
     (party_get_skill_level, reg0, "p_main_party", ":skill_no"),
##     (assign, reg0, ":max_skill"),
     (assign, reg1, ":skill_owner"),
     ]),

("troop_add_gold",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":amount", 2),

      (troop_add_gold, ":troop_no", ":amount"),
      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (play_sound, "snd_money_received"),
      (try_end),
     ]),

("event_player_captured_as_prisoner",
    [
        (try_begin),
          (check_quest_active, "qst_raid_caravan_to_start_war"),
          (neg|check_quest_concluded, "qst_raid_caravan_to_start_war"),
          (quest_get_slot, ":quest_target_faction", "qst_raid_caravan_to_start_war", slot_quest_target_faction),
          (store_faction_of_party, ":capturer_faction", "$capturer_party"),
          (eq, ":quest_target_faction", ":capturer_faction"),
          (call_script, "script_fail_quest", "qst_raid_caravan_to_start_war"),
        (try_end),
        #Removing followers of the player
        (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
		  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
          (gt, ":party_no", 0),
          (party_is_active, ":party_no"),
          (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
          (party_slot_eq, ":party_no", slot_party_ai_object, "p_main_party"),
          (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
          (assign, "$g_recalculate_ais", 1),
        (try_end),
     ]),

("stay_captive_for_hours",
    [
      (store_script_param, ":num_hours", 1),
      (store_current_hours, ":cur_hours"),
      (val_add, ":cur_hours", ":num_hours"),
      (val_max, "$g_check_autos_at_hour", ":cur_hours"),
      (val_add, ":num_hours", 1),
      (rest_for_hours, ":num_hours", 0, 0),
    ]),

("remove_troop_from_prison",
    [
      (store_script_param, ":troop_no", 1),
      (troop_set_slot, ":troop_no", slot_troop_prisoner_of_party, -1),
      (troop_set_slot, ":troop_no", slot_troop_courtesan, -1),
      (try_begin),
        (eq, "$do_not_cancel_quest", 0),
        (check_quest_active, "qst_rescue_lord_by_replace"),
        (quest_slot_eq, "qst_rescue_lord_by_replace", slot_quest_target_troop, ":troop_no"),
        (call_script, "script_cancel_quest", "qst_rescue_lord_by_replace"),
      (try_end),
      (try_begin),
        (eq, "$do_not_cancel_quest", 0),
        (check_quest_active, "qst_rescue_prisoner"),
        (quest_slot_eq, "qst_rescue_prisoner", slot_quest_target_troop, ":troop_no"),
        (call_script, "script_cancel_quest", "qst_rescue_prisoner"),
        #SB : cancel companion missions
        (try_for_range, ":companions", companions_begin, companions_end),
          (troop_slot_eq, ":companions", slot_troop_current_mission, dplmc_npc_mission_rescue_prisoner),
          (troop_slot_eq, ":companions", slot_troop_mission_object, ":troop_no"),
          (troop_set_slot, ":companions", slot_troop_current_mission, npc_mission_rejoin_when_possible),
          (troop_set_slot, ":companions", slot_troop_days_on_mission, 1),
        (try_end),
        # also accrues debts
        (try_for_range, ":troop_no", heroes_begin, heroes_end),
          # (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (troop_get_slot, ":cur_debt", ":troop_no", slot_troop_player_debt),
          (gt, ":cur_debt", dplmc_ransom_debt_mask),
          (val_mod, ":cur_debt", dplmc_ransom_debt_mask),
          (troop_set_slot, ":troop_no", slot_troop_player_debt, ":cur_debt"),
        (try_end),
      (try_end),
      (try_begin),
        (check_quest_active, "qst_deliver_message_to_prisoner_lord"),
        (quest_slot_eq, "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop, ":troop_no"),
        (call_script, "script_cancel_quest", "qst_deliver_message_to_prisoner_lord"),
      (try_end),
      ]),

("age_troop_one_year",
    [
	(store_script_param, ":troop_no", 1),
    ##diplomacy start+ use gender script
	#(troop_get_type, ":is_female", ":troop_no"),
	(assign, ":save_reg0", reg0),
	(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
	(assign, ":is_female", reg0),
	(assign, reg0, ":save_reg0"),
	##diplomacy end+

	(troop_get_slot, ":age", ":troop_no", slot_troop_age),
	(troop_get_slot, ":appearance", ":troop_no", slot_troop_age_appearance),

	(val_add, ":age", 1),
	(store_random_in_range, ":addition", 1, 5),

	(try_begin),
		(eq, ":is_female", 1),
#		(val_add, ":addition", 2), #the women's age slider seems to produce less change than the male one - commented out: makes women look too old.
	(try_end),

	(val_add, ":appearance", ":addition"),
	(try_begin),
		(gt, ":age", 45),
		(store_attribute_level, ":strength", ":troop_no", ca_strength),
		(store_attribute_level, ":agility", ":troop_no", ca_agility),
		(store_random_in_range, ":random", 0, 50), #2% loss brings it down to about 36% by age 90, but of course can be counteracted by new level gain
		(try_begin),
			(lt, ":random", ":strength"),
			(troop_raise_attribute, ":troop_no", ca_strength, -1),
		(try_end),
		(try_begin),
			(lt, ":random", ":agility"),
			(troop_raise_attribute, ":troop_no", ca_agility, -1),
		(try_end),
	(try_end),

	(val_clamp, ":appearance", 1, 100),

	(troop_set_slot, ":troop_no", slot_troop_age, ":age"),
	(troop_set_slot, ":troop_no", slot_troop_age_appearance, ":appearance"),
	(troop_set_age, ":troop_no", ":appearance"),
	]),

("init_troop_age",
	[
	(store_script_param, ":troop_no", 1),
	(store_script_param, ":age", 2), #minimum 20

	(try_begin),
		(gt, ":age", 20),
		(troop_set_slot, ":troop_no", slot_troop_age, 20),
	(else_try),
		(troop_set_slot, ":troop_no", slot_troop_age, ":age"),
	(try_end),

	(store_sub, ":years_to_age", ":age", 20),
    (troop_set_age, ":troop_no", 0),

	(try_begin),
		(gt, ":years_to_age", 0),
		(try_for_range, ":unused", 0, ":years_to_age"),
			(call_script, "script_age_troop_one_year", ":troop_no"),
		(try_end),
	(try_end),

	]),

("troop_change_career", #empty now, but might want to add mid-game
	[
	]),

("start_courtyard_conversation",
	[
      (store_script_param, ":conversation_troop", 1),
      (store_script_param, ":center_no", 2),

      (party_get_slot, ":conversation_scene", ":center_no", slot_town_center), #castle's exterior
      (modify_visitors_at_site, ":conversation_scene"),
      (reset_visitors),
      (try_begin), #player vs troop, not much processing
        (neg|troop_is_hero, ":conversation_troop"),

      (else_try), #talking to lords, compare relative positions
        (assign, ":supplicant", "trp_player"),
        (store_faction_of_party, ":faction_no", ":center_no"),
        (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
        (assign, ":player_standing", reg0),
        (call_script, "script_dplmc_get_troop_standing_in_faction", ":conversation_troop", ":faction_no"),
        (assign, ":other_troop_standing", reg0),

        #23 : castle guard (adjacent), 2: lord's hall door
        (assign, ":entry_lower", 23),
        (assign, ":entry_upper", 2),
        #overwrite standing if center owned
        (try_begin),
          (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
          (assign, ":player_standing", 9999),
        (else_try),
          (party_slot_eq, ":center_no", slot_town_lord, ":conversation_troop"),
          (assign, ":other_troop_standing", 9999),
        (else_try), #strangers, use default street entry point (this may be outside in towns, 0 preferred)
          (this_or_next|eq, ":player_standing", DPLMC_FACTION_STANDING_UNAFFILIATED),
          (eq, ":other_troop_standing", DPLMC_FACTION_STANDING_UNAFFILIATED),
          (assign, ":entry_lower", 1),
        (try_end),

        (try_begin), #player is usually supplicant
          (gt, ":player_standing", ":other_troop_standing"),
          (assign, ":supplicant", ":conversation_troop"),
          (assign, ":conversation_troop", "trp_player"),
        (else_try),
          (is_between, ":center_no", towns_begin, towns_end),
          (eq, ":player_standing", ":other_troop_standing"),
          (assign, ":entry_upper", 27),
          (assign, ":entry_lower", 28),
        (try_end),
      (try_end),

      (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", ":entry_lower", af_override_horse|af_override_head|af_override_weapons),
      (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", ":entry_upper", af_override_horse|af_override_fullhelm),
      (set_visitor, ":entry_lower", ":supplicant"),
      (set_visitor, ":entry_upper", ":conversation_troop"),

      (set_jump_mission,"mt_conversation_encounter"),
      (jump_to_scene, ":conversation_scene"),
      (change_screen_map_conversation, ":conversation_troop"),
    ]),

("start_court_conversation",
    [
        (store_script_param, ":conversation_troop", 1),
        (store_script_param, ":center_no", 2),

        (party_get_slot, ":conversation_scene", ":center_no", slot_town_castle),
        (modify_visitors_at_site, ":conversation_scene"),
        (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", 0, af_override_horse),

        #clear flags for actual courtly conversations?
        (store_random_in_range, ":entry_no", 16, 32),
        (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", ":entry_no", af_override_horse),
        (try_begin),
          (troop_is_hero, ":conversation_troop"),
          (set_visitor, ":entry_no", ":conversation_troop"),
        (else_try),
          (store_script_param, ":troop_dna", 3),
          (set_visitor, ":entry_no", ":conversation_troop", ":troop_dna"),
        (try_end),
        (set_jump_mission,"mt_conversation_encounter"),
        (jump_to_scene, ":conversation_scene"),
        (change_screen_map_conversation, ":conversation_troop"),
    ]),

("companion_get_mission_string", [
        (store_script_param, ":companion", 1),
        (try_begin), #do not impose conditions here, do so from calling script
            # (this_or_next|main_party_has_troop, ":companion"),
            # (this_or_next|troop_slot_ge, ":companion", slot_troop_current_mission, 1),
                # (eq, "$g_player_minister", ":companion"),
            (str_store_troop_name, s4, ":companion"),
            (str_clear, s5),
            (str_clear, s8),
            (troop_get_slot, ":days_left", ":companion", slot_troop_days_on_mission),
            (troop_get_slot, ":mission", ":companion", slot_troop_current_mission),
            (try_begin),
                (le, ":days_left", 0),
                (str_store_string, s5, "str_whereabouts_unknown"),
            (else_try),
                (eq, ":days_left", 1),
                (str_store_string, s5, "str_expected_back_imminently"),
            (else_try),
                (assign, reg3, ":days_left"),
                (str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
            (try_end),


            (try_begin),
                (eq, ":mission", npc_mission_kingsupport),
                (str_store_string, s8, "str_gathering_support"),
            (else_try),
                (this_or_next|eq, ":mission", npc_mission_gather_intel),
                (eq, ":mission", dplmc_npc_mission_rescue_prisoner), #new mission
                (troop_get_slot, ":town_with_contacts", ":companion", slot_troop_town_with_contacts),
                (str_store_party_name, s9, ":town_with_contacts"),
                (try_begin),
                  (eq, ":mission", npc_mission_gather_intel),
                  (str_store_string, s8, "str_gathering_intelligence"),
                (else_try),
                  (eq, ":mission", dplmc_npc_mission_rescue_prisoner),
                  (str_store_string, s8, "str_preparing_prison_break"),
                (try_end),
            (else_try),
                (this_or_next|is_between, ":mission", npc_mission_peace_request, npc_mission_rejoin_when_possible),
                (is_between, ":mission", dplmc_npc_mission_war_request, dplmc_npc_mission_rescue_prisoner),

                (troop_get_slot, ":faction", ":companion", slot_troop_mission_object),
                (str_store_faction_name, s9, ":faction"),
                (str_store_string, s8, "str_diplomatic_embassy_to_s9"),
            # (else_try), #diplomacy missions

            (else_try),
                (eq, ":companion", "$g_player_minister"),
                (str_store_string, s8, "str_serving_as_minister"),
                (try_begin),
                  (is_between, "$g_player_court", centers_begin, centers_end),
                  (str_store_party_name, s9, "$g_player_court"),
                  (str_store_string, s5, "str_in_your_court_at_s9"),
                (else_try),
                  (str_store_string, s5, "str_awaiting_the_capture_of_a_fortress_which_can_serve_as_your_court"),
                (try_end),
            (else_try),
                (eq, ":mission", npc_mission_rejoin_when_possible),
                (str_store_string, s8, "str_attempting_to_rejoin_party"),
            (else_try),
                (main_party_has_troop, ":companion"),
                (str_store_string, s8, "str_under_arms"),
                (str_store_string, s5, "str_in_your_party"),
            (else_try),    #Companions who are in a center
                (troop_slot_ge, ":companion", slot_troop_cur_center, centers_begin),
                (str_store_string, s8, "str_separated_from_party"),
                (str_store_string, s5, "str_whereabouts_unknown"),
            (else_try),    #Companions who are (imprisoned) in a center
                (troop_slot_ge, ":companion", slot_troop_prisoner_of_party, centers_begin),
                (str_store_string, s8, "str_missing_after_battle"),
                (str_store_string, s5, "str_whereabouts_unknown"),
            (else_try),
                (try_begin),
                    (check_quest_active, "qst_lend_companion"),
                    (quest_slot_eq, "qst_lend_companion", slot_quest_target_troop, ":companion"),
                    (quest_get_slot, ":lord", "qst_lend_companion", slot_quest_giver_troop),
                    (str_store_troop_name, s5, ":lord"),
                    (str_store_string, s8, "str_accompanying_s5"),
                    (str_store_string, s5, "str_on_loan"),
                (else_try),
                    (check_quest_active, "qst_lend_surgeon"),
                    (quest_slot_eq, "qst_lend_surgeon", slot_quest_target_troop, ":companion"),
                    (quest_get_slot, ":lord", "qst_lend_surgeon", slot_quest_giver_troop),
                    (str_store_troop_name, s5, ":lord"),
                    (str_store_string, s8, "str_accompanying_s5"),
                    (str_store_string, s5, "str_on_loan"),
                (try_end),
            (try_end),

            (str_store_string, s0, "str_s4_s8_s5"),
        (try_end),
        ]
      ),

("get_disguise_string", [
      (store_script_param, ":cur_val", 1),
      (store_script_param, ":sreg", 2),
      (store_add, ":end_val", "str_pilgrim_disguise", num_disguises),
      (str_clear, ":sreg"),
      (try_for_range, ":string", "str_pilgrim_disguise", ":end_val"),
        (eq, ":cur_val", 1), #
        (assign, ":end_val", -1), #loop break
        (str_store_string, ":sreg", ":string"),
      (else_try),
        (val_div, ":cur_val", 2), #divide by 2, next iteration
      (try_end),
      ]),

("acquire_disguise", [
      (store_script_param, ":disguise", 1),
      (troop_get_slot, ":cur_disguise", "trp_player", slot_troop_player_disguise_sets),
      (val_or, ":cur_disguise", ":disguise"),
      (troop_set_slot, "trp_player", slot_troop_player_disguise_sets, ":cur_disguise"),
      (call_script, "script_get_disguise_string", ":disguise", 0),
      # (str_store_string, s0, reg0),
      (display_message, "@Acquired {s0}'s clothing", message_alert),
      ]),

("set_disguise_override_items", [
      (store_script_param, ":mission_template", 1),
      (store_script_param, ":entry_no", 2),
      (store_script_param, ":with_weapon", 3),

      (mission_tpl_entry_clear_override_items, ":mission_template", ":entry_no"),
      (try_begin),
        (eq, "$sneaked_into_town", disguise_pilgrim),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_pilgrim_disguise"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_pilgrim_hood"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_wrapping_boots"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_practice_staff"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_throwing_daggers"),
        (try_end),
      (else_try),
        (eq, "$sneaked_into_town", disguise_farmer),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_felt_hat"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_coarse_tunic"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_nomad_boots"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_battle_fork"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_cleaver"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_stones"),
        (try_end),
      (else_try),
        (eq, "$sneaked_into_town", disguise_hunter),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_black_hood"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_leather_gloves"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_light_leather"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_light_leather_boots"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_sword_khergit_1"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_hunting_bow"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_barbed_arrows"),
        (try_end),
      (else_try),
        (eq, "$sneaked_into_town", disguise_merchant),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_leather_jacket"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_woolen_hose"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_felt_steppe_cap"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_dagger"),
        (try_end),
      (else_try),
        (eq, "$sneaked_into_town", disguise_guard),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_footman_helmet"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_mail_mittens"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_mail_shirt"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_leather_jerkin"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_mail_chausses"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_fighting_pick"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_tab_shield_round_c"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_war_spear"),
        (try_end),
      (else_try),
        (eq, "$sneaked_into_town", disguise_bard),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_linen_tunic"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_leather_boots"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_winged_mace"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_lyre"),
        (try_end),
      (try_end),
   ]),

("simple_remove_disguise",
 [
	(try_begin),
		(gt, "$sneaked_into_town", disguise_none),
		(display_message, "@You retrieve your hidden items.", message_alert),
		(try_begin),
			(eq, "$g_dplmc_player_disguise", 1),
			(set_show_messages, 0),
		(try_for_range, ":i_slot", ek_item_0, ek_food + 1),
			(troop_get_inventory_slot, ":item", "trp_player", ":i_slot"),
			(neq, ":item", -1),
			(troop_get_inventory_slot_modifier, ":imod", "trp_player", ":i_slot"),
			(troop_add_item, "trp_random_town_sequence", ":item", ":imod"),
		(try_end),
			(call_script, "script_move_inventory_and_gold", "trp_player", "trp_random_town_sequence", 0),
			(call_script, "script_dplmc_copy_inventory", "trp_random_town_sequence", "trp_player"),
			(call_script, "script_troop_transfer_gold", "trp_random_town_sequence", "trp_player", 0),
			(set_show_messages, 1),
		(try_end),
		(assign, "$sneaked_into_town", disguise_none),
	(try_end),
]),
]