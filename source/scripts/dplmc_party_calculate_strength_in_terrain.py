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

dplmc_party_calculate_strength_in_terrain_scripts = [
#script_dplmc_party_calculate_strength_in_terrain
# INPUT: arg1 = party_id
#        arg2 = terrain (from header_terrain_types.py)
#        arg3 = exclude leader (0 for do-not-exclude, 1 for exclude)
#        arg4 = cache policy (1 is use terrain, 2 is use non-terrain, 0 is do not use)
# OUTPUT: reg0 = strength with terrain
#         reg1 = strength ignoring terrain
("dplmc_party_calculate_strength_in_terrain",
    [
      (store_script_param, ":party", 1), #Party_id
      (store_script_param, ":terrain_type", 2),#a value from header_terrain_types.py
      (store_script_param, ":exclude_leader", 3),#(0 for do-not-exclude, 1 for exclude)
      (store_script_param, ":cache_policy", 4),#1 is use terrain, 2 is use non-terrain, 0 is do not use)

      (assign, ":total_strength_terrain", 0),
      (assign, ":total_strength_no_terrain", 0),

      (party_get_num_companion_stacks, ":num_stacks", ":party"),
      (assign, ":first_stack", 0),
      (try_begin),
        (neq, ":exclude_leader", 0),
        (assign, ":first_stack", 1),
      (try_end),
	  #Bonus for heroes on top of the rest
	  (assign, ":hero_percent", 110),
	  ##Moved setting the multipliers out of the loop...
	  (assign, ":guaranteed_horse_percent", 100),
	  (assign, ":guaranteed_ranged_percent", 100),
	  (assign, ":guaranteed_neither_percent", 100),
	  #First, test for some special codes:
	  (try_begin),
	     (eq, ":terrain_type", dplmc_terrain_code_none),#Apply no modifiers
		 (assign, ":hero_percent", 100),
	  (else_try),
	  	(eq, ":terrain_type", dplmc_terrain_code_village),#A dismounted fight at a village (apply hero modifier, nothing else)
      (else_try),
        (eq, ":terrain_type", dplmc_terrain_code_siege),#A siege battle, not including sorties.
        (assign, ":guaranteed_ranged_percent", 120),
	  #The rest are ordinary rt_* codes.
	  #I changed the balance of these to make the variations less extreme (e.g. 150% mounted strength on rt_steppe).
	  #I believe that the version from ArcherOS is trying to create certain map results, rather than solely
	  #make autocalc strength more accurate in terms of "what would happen if they fought the player".
	  (else_try),
        (eq, ":terrain_type", rt_steppe),
		#The 150% increase in the steppe strikes me as excessive.
		#Since the NPC cost increase for mounted troops is 20%, and the PC cost is 65%,
		#it isn't entirely implausible.
	    #(assign, ":guaranteed_horse_percent", 150),
		#Archer uses 150%, Custom Commander uses a flat 125%.
		(assign, ":guaranteed_horse_percent", 120),
	  (else_try),
		#I am unaware of any game mechanic in live battles that gives any disadvantage
		#to horses on snow or sand as opposed to a plain.
		(this_or_next|eq, ":terrain_type", rt_snow),
		(this_or_next|eq, ":terrain_type", rt_desert),
			(eq, ":terrain_type", rt_plain),
		(assign, ":guaranteed_horse_percent", 120),
     (else_try),
		#I suspect that the 120% mounted bonus for steppe forests is inaccurate,
		#but I haven't checked it out yet.
	    (eq, ":terrain_type", rt_steppe_forest),
        (assign, ":guaranteed_horse_percent", 120),
     (else_try),
        (this_or_next|eq, ":terrain_type", rt_forest),
        (this_or_next|eq, ":terrain_type", rt_mountain_forest),
		     (eq, ":terrain_type", rt_snow_forest),
        #(assign, ":guaranteed_neither_percent", 120),
		(assign, ":guaranteed_neither_percent", 110),
	 (try_end),

      (try_for_range, ":i_stack", ":first_stack", ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party", ":i_stack"),
        (store_character_level, ":stack_strength", ":stack_troop"),
        (val_add, ":stack_strength", 4), #new was 12 (patch 1.125)
        (val_mul, ":stack_strength", ":stack_strength"),
        (val_mul, ":stack_strength", 2), #new (patch 1.125)
        #move the next two lines to after terrain advantage
        #(val_div, ":stack_strength", 100),
        #(val_max, ":stack_strength", 1), #new (patch 1.125)
        (assign, ":terrain_free_strength", ":stack_strength"),
        ##use Arch3r's terrain advantage code (bug-fix changes 2011-04-13; other changes 2011-04-25)
        (try_begin),
           ##AotE terrain advantages
           (assign, ":hero_horse", 0),#added for heroes (any positive number = has a horse)
           (try_begin),
		      (this_or_next|eq, "trp_player", ":stack_troop"),
				(troop_is_hero, ":stack_troop"),
		      (gt, ":guaranteed_horse_percent", ":hero_percent"),#don't bother if we wouldn't use the result
              (neg|troop_is_guarantee_horse, ":stack_troop"),#don't bother if we already know the troop has a horse
			  (store_skill_level, reg0, "skl_riding", ":stack_troop"),
			  (ge, reg0, 2),#don't bother if the troop has no/minimal riding skill
			  #Just checking ek_horse may not work for non-companions, so check the inventory
			  (troop_get_inventory_capacity, ":inv_cap", ":stack_troop"),
			  (ge, ":inv_cap", 1),
			  (val_min, ":inv_cap", dplmc_ek_alt_items_begin + 8),#Don't check too much of the inventory
			  (try_for_range, ":inv_slot", 0, ":inv_cap"),
				(troop_inventory_slot_get_item_amount, reg1, ":stack_troop", ":inv_slot"),
				(ge, reg1, 1),#quantity must be greater than zero
				(troop_get_inventory_slot, reg0, ":stack_troop", ":inv_slot"),
				(ge, reg0, 1),#must be a valid item
				(item_get_type, reg1, reg0),#check if the item is a horse
				(eq, reg1, itp_type_horse),
				(assign, ":inv_cap", ":inv_slot"),#break loop
			  (try_end),
			  #If no horse found, set to zero
              (neg|is_between, ":hero_horse", horses_begin, horses_end),
              (assign, ":hero_horse", 0),
           (try_end),
		   (assign, ":stack_strength_multiplier", 100),#<-- percent multiplier
           (try_begin),#Mounted troops
			  (this_or_next|ge, ":hero_horse", 1),
              (troop_is_guarantee_horse, ":stack_troop"),
              (assign, ":stack_strength_multiplier", ":guaranteed_horse_percent"),
		   (else_try),#Ranged troops
              (troop_is_guarantee_ranged, ":stack_troop"),
              (assign, ":stack_strength_multiplier", ":guaranteed_ranged_percent"),
           (else_try),#Infantry
              (assign, ":stack_strength_multiplier", ":guaranteed_neither_percent"),
           (try_end),

		   #Use hero/player modifiers if a better one didn't apply
		   (try_begin),
		      (this_or_next|eq, ":stack_troop", "trp_player"),
			     (troop_is_hero, ":stack_troop"),
			  (val_max, ":stack_strength_multiplier", ":hero_percent"),#hero bonus
		   (try_end),

		   (val_mul, ":stack_strength", ":stack_strength_multiplier"),
		   (val_add, ":stack_strength", 50),#add this before division for correct rounding
           (val_div, ":stack_strength", 100),
           ##AotE terrain advantages
        (try_end),
        #moved the next two lines here from above
        (val_div, ":stack_strength", 100),#<- moved here from above
        (val_max, ":stack_strength", 1), #new (patch 1.125) #<- moved here from above
        (val_div, ":terrain_free_strength", 100),
        (val_max, ":terrain_free_strength", 1),
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":stack_size", ":num_wounded"),
          (val_mul, ":stack_strength", ":stack_size"),
          (val_mul, ":terrain_free_strength", ":stack_size"),
        (else_try),
          (troop_is_wounded, ":stack_troop"), #hero & wounded
          (assign, ":stack_strength", 0),
          (assign, ":terrain_free_strength", 0),
        (try_end),
        (val_add, ":total_strength_terrain", ":stack_strength"),
        (val_add, ":total_strength_no_terrain", ":terrain_free_strength"),
      (try_end),
	  #Load results into registers and cache if appropriate
	  (assign, reg0, ":total_strength_terrain"),
	  (assign, reg1, ":total_strength_no_terrain"),
      (try_begin),
         (eq, ":cache_policy", 1),
         (party_set_slot, ":party", slot_party_cached_strength, reg0),
      (else_try),
         (eq, ":cache_policy", 2),
         (party_set_slot, ":party", slot_party_cached_strength, reg1),
      (try_end),
  ])
]
