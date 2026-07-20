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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

game_get_total_wage_scripts = [
# script_game_get_total_wage
# This script is called from the game engine for calculating total wage of the player party which is shown at the party window.
# Input: none
# Output: reg0: weekly wage
("game_get_total_wage",
    [
      (assign, ":total_wage", 0),
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
        (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
        (call_script, "script_game_get_troop_wage", ":stack_troop", 0),
        (val_mul, reg0, ":stack_size"),
        (val_add, ":total_wage", reg0),
      (try_end),
	  ##diplomacy start+
	  #If the player leads a kingdom, take into account centralization.
	  (faction_get_slot, ":centralization", "$players_kingdom", dplmc_slot_faction_centralization),
	  (try_begin),
		  (neq, ":centralization", 0),

		  (assign, reg0, 0),
	     (try_begin),
		     (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
		     (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
		     (ge, ":faction_leader", 0),
		     (this_or_next|eq, ":faction_leader", "trp_player"),
		     (this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
              (troop_slot_eq, "trp_player", slot_troop_spouse, reg0),
           (assign, reg0, 1),
        (try_end),

		  (this_or_next|eq, reg0, 1),
		     (eq, "$players_kingdom", "fac_player_supporters_faction"),
		  (faction_slot_eq, "$players_kingdom", slot_faction_state, sfs_active),

		  #Apply centralization, but limit it for nascent kingdoms
        (val_clamp, ":centralization", -3, 4),
	     (faction_get_slot, ":policy_limit", "$players_kingdom", slot_faction_num_towns),
	     (faction_get_slot, reg0, "$players_kingdom", slot_faction_num_castles),
	     (val_add, ":policy_limit", reg0),

	     (val_max, ":policy_limit", 0),
	     (val_min, ":centralization", ":policy_limit"),
	     (val_mul, ":policy_limit", -1),
	     (val_max, ":centralization", ":policy_limit"),

		  #Now reg0 is going to be the result again
		  (store_mul, reg0, ":centralization", -5),
		  (val_add, reg0, 100),
		  (val_mul, reg0, ":total_wage"),
		  (val_add, reg0, 50),#rounding
		  (val_div, reg0, 100),
	  (try_end),
    ##diplomacy end+
      (assign, reg0, ":total_wage"),
      (set_trigger_result, reg0),
  ])
]
