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

calculate_troop_score_for_center_scripts = [
# script_consume_food
# Input: arg1 = troop_no, arg2 = center_no
# Output: reg0 = score
("calculate_troop_score_for_center",
   [(store_script_param, ":troop_no", 1),
    (store_script_param, ":center_no", 2),
    (assign, ":num_center_points", 1),
    (try_for_range, ":cur_center", centers_begin, centers_end),
      (assign, ":center_owned", 0),
      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (party_slot_eq, ":cur_center", slot_town_lord, stl_reserved_for_player),
        (assign, ":center_owned", 1),
      (try_end),
      (this_or_next|party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
      (eq, ":center_owned", 1),
      (try_begin),
        (party_slot_eq, ":cur_center", slot_party_type, spt_town),
        (val_add, ":num_center_points", 4),
      (else_try),
        (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
        (val_add, ":num_center_points", 2),
      (else_try),
        (val_add, ":num_center_points", 1),
      (try_end),
    (try_end),
    (troop_get_slot, ":troop_renown", ":troop_no", slot_troop_renown),
    (store_add, ":score", 500, ":troop_renown"),
    (val_div, ":score", ":num_center_points"),
    (store_random_in_range, ":random", 50, 100),
    (val_mul, ":score", ":random"),
    (try_begin),
      (party_slot_eq, ":center_no", slot_center_last_taken_by_troop, ":troop_no"),
      (val_mul, ":score", 3),
      (val_div, ":score", 2),
  	##diplomacy start+
	#Take into account original/most-recent lord and home slots.
	#Fief allocations during rebellions are an example of when this would apply.
	(else_try),
	#Bonus for original owner
 		(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		(party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
		(party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":troop_no"),
		(val_mul, ":score", 3),
		(val_div, ":score", 2),
	(else_try),
	#Bonus for previous owner
 		(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		(party_slot_ge, ":center_no", dplmc_slot_center_ex_lord, 1),
		(party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":troop_no"),
		(val_mul, ":score", 3),
		(val_div, ":score", 2),
	(else_try),
	#Bonus for lord claiming the center as home
 		(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		(troop_slot_eq, ":troop_no", slot_troop_home, ":center_no"),
		(val_mul, ":score", 3),
		(val_div, ":score", 2),
	##diplomacy end+
    (try_end),
    (try_begin),
      (eq, ":troop_no", "trp_player"),
       ##diplomacy start+ xxx Replaced next line (slot 0 is not the faction leader slot):
      #(faction_get_slot, ":faction_leader", "$players_kingdom"),
      (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
      ##diplomacy end+
      (call_script, "script_troop_get_player_relation", ":faction_leader"),
      (assign, ":leader_relation", reg0),
      #(troop_get_slot, ":leader_relation", ":faction_leader", slot_troop_player_relation),
      (val_mul, ":leader_relation", 2),
      (val_add, ":score", ":leader_relation"),
    (try_end),
    (assign, reg0, ":score"),
    ])
]
