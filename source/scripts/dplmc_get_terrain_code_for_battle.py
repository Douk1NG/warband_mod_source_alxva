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

dplmc_get_terrain_code_for_battle_scripts = [
#script_dplmc_center_point_calc
#
# Gets the terrain code for a battle between two parties, which
# is usually a value like rt_desert, but can instead be two
# special values: -1 for
#
# INPUT: arg1 = attacker_party
#        arg2 = defender_party
# OUTPUT: reg0 = terrain code (-1 for invalid, -2 for siege)
("dplmc_get_terrain_code_for_battle",
   [
      (store_script_param, ":attacker_party", 1),
      (store_script_param, ":defender_party", 2),

      (assign, reg0, dplmc_terrain_code_unknown), #Terrain code, defined in header_terrain_types.py

	  (try_begin),
		#Check for village missions
         (this_or_next|eq, ":attacker_party", "p_main_party"),
			(eq, ":defender_party", "p_main_party"),
		 (ge, "$g_encounter_is_in_village", 1),
		 (assign, reg0, dplmc_terrain_code_village),#defined in header_terrain_types.py
      (else_try),
		#If the attacker party is a town, a castle, a village, a bandit lair, or a ship,
		#set the terrain code to "none" since we don't have any specific ideas for modifying
		#the unit-type performance in scenarios of that type (whatever they are).
         (ge, ":attacker_party", 0),
         (this_or_next|party_slot_eq, ":attacker_party", slot_party_type, spt_town),#no modifier for being attacked by garrisoned troops
         (this_or_next|party_slot_eq, ":attacker_party", slot_party_type, spt_castle),
         (this_or_next|party_slot_eq, ":attacker_party", slot_party_type, spt_village),
         (this_or_next|party_slot_eq, ":attacker_party", slot_party_type, spt_bandit_lair),
			(party_slot_eq, ":attacker_party", slot_party_type, spt_ship),#no modifier for being attacked by a ship
         (assign, reg0, dplmc_terrain_code_unknown),#no terrain options, defined in header_terrain_types.py
	  (else_try),
		#If the attacker party is *attached* to a town/castle/village, a bandit lair, or a ship,
		#set the terrain code to "none" since we don't have any specific ideas for modifying
		#the unit-type performance in scenarios of that type (whatever they are).
	     (ge, ":attacker_party", 0),
	     (party_get_attached_to, ":attachment", ":attacker_party"),
		 (ge, ":attachment", 0),
		 (party_is_active, ":attachment"),
		 (this_or_next|party_slot_eq, ":attachment", slot_party_type, spt_town),#no modifier for being attacked by garrisoned troops
         (this_or_next|party_slot_eq, ":attachment", slot_party_type, spt_castle),
         (this_or_next|party_slot_eq, ":attachment", slot_party_type, spt_village),
         (this_or_next|party_slot_eq, ":attachment", slot_party_type, spt_bandit_lair),
			(party_slot_eq, ":attachment", slot_party_type, spt_ship),#no modifier for being attacked by a ship
         (assign, reg0, dplmc_terrain_code_unknown),#no terrain modifiers
      (else_try),
		#If the attacker party isn't a weird type, the terrain is entirely based on the
		#defender (unless the defender is invalid).
         (ge, ":defender_party", 0),
         (try_begin),
			#If the defender is a walled center, use siege mode.
            (this_or_next|party_slot_eq, ":defender_party", slot_party_type, spt_town),
            (party_slot_eq, ":defender_party", slot_party_type, spt_castle),
            (assign, reg0, dplmc_terrain_code_siege),#siege mode, defined in header_terrain_types.py
		 (else_try),
			#If the defender is a village
			(party_slot_eq, ":defender_party", slot_party_type, spt_village),
			(assign, reg0, dplmc_terrain_code_village),
         (else_try),
			#If the defender is a bandit lair or a ship, use no terrain modifier.
            (this_or_next|party_slot_eq, ":defender_party", slot_party_type, spt_bandit_lair),
				(party_slot_eq, ":defender_party", slot_party_type, spt_ship),
            (assign, reg0, dplmc_terrain_code_unknown),#no terrain modifiers
 		 (else_try),
			#If the defender is attached, do the same checks but for the attachment.
		    (party_get_attached_to, ":attachment", ":defender_party"),
			(ge, ":attachment", 0),
			(party_is_active, ":attachment"),
			(assign, ":attachment_value", -100),
			(try_begin),
				#Walled centers use siege modifiers
			   (this_or_next|party_slot_eq, ":attachment", slot_party_type, spt_town),
			      (party_slot_eq, ":attachment", slot_party_type, spt_castle),
			   (assign, ":attachment_value", dplmc_terrain_code_siege),
			(else_try),
				#Villages
			   (party_slot_eq, ":attachment", slot_party_type, spt_village),
			   (assign, ":attachment_value", dplmc_terrain_code_village),
			(else_try),
				#bandit-lairs and ships have no modifiers currently
			   (this_or_next|party_slot_eq, ":attachment", slot_party_type, spt_bandit_lair),
				(party_slot_eq, ":attachment", slot_party_type, spt_ship),
			   (assign, ":attachment_value", dplmc_terrain_code_unknown),#no terrain modifiers
			(try_end),
			#If neither of the above apply, fall through to the next condition.
			(neq, ":attachment_value", -100),
			(assign, reg0, ":attachment_value"),
         (else_try),
			#Use the terrain under the defender.
			#In the future I might want to change this so there's a tactics contest
			#between the attacker and defender to choose the more favorable ground
			#from their immediate surroundings.  I would also have to change the actual
			#terrain-type code.
            (party_get_current_terrain, reg0, ":defender_party"),
		 (try_end),
      (else_try),
		 #If we get here, it means the defender was invalid, so use the terrain under
		 #the attacker.
         (ge, ":attacker_party", 0),
         (party_get_current_terrain, reg0, ":attacker_party"),#terrain under attacker
      (try_end),
   ])
]
