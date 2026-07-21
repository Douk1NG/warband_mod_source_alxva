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

loot_player_items_scripts = [
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
      ])
]
