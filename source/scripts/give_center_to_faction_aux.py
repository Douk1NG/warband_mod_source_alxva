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

give_center_to_faction_aux_scripts = [
# script_give_center_to_faction_aux
# Input: arg1 = center_no, arg2 = faction
("give_center_to_faction_aux",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":faction_no"),

      (store_faction_of_party, ":old_faction", ":center_no"),
      (party_set_faction, ":center_no", ":faction_no"),

      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (try_begin),
          (party_get_slot, ":farmer_party", ":center_no", slot_village_farmer_party),
          (gt, ":farmer_party", 0),
          (party_is_active, ":farmer_party"),
          (party_set_faction, ":farmer_party", ":faction_no"),
        (try_end),
        #SB : reinforcements becomes deserters
        (try_begin),
          (party_get_slot, ":reinf_party", ":center_no", slot_village_reinforcement_party),
          (gt, ":reinf_party", 0),
          (party_is_active, ":reinf_party"),
          (set_spawn_radius, 0),
          (spawn_around_party, ":reinf_party", "pt_deserters"),
          (assign, ":new_party", reg0),
          #apply move_members_with_ratio, party_inflict_attrition, party_inflict_casualties, etc based on center relations/prosperity
          (call_script, "script_party_add_party", ":new_party", ":reinf_party"),
          (party_set_slot, ":center_no", slot_village_reinforcement_party, -1),
          (party_set_ai_behavior, ":new_party", ai_bhvr_patrol_party),
          (party_set_ai_object, ":new_party", ":center_no"), #or its market town
          (party_set_ai_patrol_radius, ":new_party", 25),
          (remove_party, ":reinf_party"),
        (try_end),
      (try_end),

      (try_begin),
	    #This bit of seemingly redundant code (the neq condition) is designed to prevent a bug that occurs when a player first conquers a center -- apparently this script is called again AFTER it is handed to a lord
		#Without this line, then the player's dialog selection does not have any affect, because town_lord is set again to stl_unassigned after the player makes his or her choice
	    (neq, ":faction_no", ":old_faction"),
		##diplomacy start+
		(party_get_slot, ":old_ex_faction", ":center_no", slot_center_ex_faction),
		##diplomacy end+
        (party_set_slot, ":center_no", slot_center_ex_faction, ":old_faction"),
        (party_get_slot, ":old_town_lord", ":center_no", slot_town_lord),
		##diplomacy start+
		(store_current_hours, ":hours"),
		(party_get_slot, ":old_ex_lord", ":center_no", dplmc_slot_center_ex_lord),
		#(party_get_slot, ":old_last_transfer", ":center_no", dplmc_slot_center_last_transfer_time),
		(try_begin),
			#When a faction regains a lost fief, if the ex-lord is a member of that faction,
			#don't erase that information.
			(this_or_next|party_slot_eq, ":center_no", slot_center_original_faction, ":faction_no"),#Handle several rapid sequential transfers
				(eq, ":old_ex_faction", ":faction_no"),
			(is_between, ":old_ex_lord", heroes_begin, heroes_end),
			(store_faction_of_troop, ":old_ex_lord_faction", ":old_ex_lord"),
			(eq, ":old_ex_lord_faction", ":faction_no"),
		(else_try),
			#Otherwise, if the center had a lord before this transfer, set the
			#ex-lord to the lord losing this.
			(neq, ":old_town_lord", stl_unassigned),
			(ge, ":old_town_lord", 0),
			(this_or_next|ge, ":old_town_lord", 1),#Don't apply to the player at the start of the game
				(gt, ":hours", 0),

			#Don't apply to fiefs lost by the faction leader, except for his "home",
			#and any fiefs with him marked as the original lord.
			(call_script, "script_dplmc_get_troop_standing_in_faction", ":old_town_lord", ":old_faction"),
			(this_or_next|lt, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(this_or_next|troop_slot_eq, ":old_faction", slot_troop_home, ":center_no"),
				(party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":old_town_lord"),

			(party_set_slot, ":center_no", dplmc_slot_center_ex_lord, ":old_town_lord"),
		(try_end),
        (party_set_slot, ":center_no", dplmc_slot_center_last_transfer_time, ":hours"),
        (party_set_slot, ":center_no", slot_town_lord, stl_unassigned),
        (party_set_banner_icon, ":center_no", 0),#Removing banner
        (call_script, "script_update_faction_notes", ":old_faction"),
        #Invalidate old lord's cached center points
        (gt, ":old_town_lord", -1),
        (troop_set_slot, ":old_town_lord", dplmc_slot_troop_center_points_plus_one, 0),
      (try_end),

      (call_script, "script_update_faction_notes", ":faction_no"),
      (call_script, "script_update_center_notes", ":center_no"),

      (try_begin),
        (ge, ":old_town_lord", 0),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (call_script, "script_update_troop_notes", ":old_town_lord"),
      (try_end),

      (try_for_range, ":other_center", centers_begin, centers_end),
        (party_slot_eq, ":other_center", slot_village_bound_center, ":center_no"),
        ##diplomacy start+ Avoid infinite recursion even if some foolish modder (such as myself)
        #has set up bizarre cyclic dependencies
        (store_faction_of_party, ":other_center_faction", ":other_center"),
        ##The "this or next" is so that any weird uses of this function
        ##in Native (to change something to its own faction) will be
        ##replicated.  The reason this works is that all villages have
        ##higher ID numbers than castles or towns.
        (this_or_next|gt, ":other_center", ":center_no"),
        (neq, ":other_center_faction", ":old_faction"),
        ##diplomacy end+
        (call_script, "script_give_center_to_faction_aux", ":other_center", ":faction_no"),
      (try_end),
  ])
]
