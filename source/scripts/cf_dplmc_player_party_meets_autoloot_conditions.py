# ======================================================================
# SHARED DEPENDENCY
# Entity: cf_dplmc_player_party_meets_autoloot_conditions (script)
# Called by menus in 3 domains: battle, camp, siege
# ======================================================================

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

cf_dplmc_player_party_meets_autoloot_conditions_scripts = [
#"script_dplmc_translate_inactive_player_supporter_faction_2"
##
#
#INPUT:
#   None
#OUTPUT:
#   reg0   -1 means there are no companions and skill is too low
#           0 means there are companions and skill is too low
#           1 means skill is high enough but there are no companions
#           2 means skill is high enough and there are companions
#
# Will fail if it does not set reg0 to 2.
##
("cf_dplmc_player_party_meets_autoloot_conditions",
[
	  (store_skill_level, ":best_loot_skill", "skl_looting", "trp_player"),
	  (store_skill_level, ":player_inv_skill", "skl_inventory_management", "trp_player"),
	  (assign, ":best_inv_skill", ":player_inv_skill"),
	  (assign, ":num_companions", 0),
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
         (party_stack_get_troop_id,   ":stack_troop", "p_main_party", ":stack_no"),
		 (ge, ":stack_troop", 0),
		 #Check skill
		 (is_between, ":stack_troop", heroes_begin, heroes_end),
		 (store_skill_level, ":hero_skill", "skl_inventory_management", ":stack_troop"),
		 (val_max, ":best_inv_skill", ":hero_skill"),

		 (store_skill_level, ":hero_skill", "skl_looting", ":stack_troop"),
		 (val_max, ":best_loot_skill", ":hero_skill"),
		 #Check is companion
         (is_between, ":stack_troop", companions_begin, companions_end),
         (val_add, ":num_companions", 1),
      (try_end),

	  (try_begin),
	    (lt, ":player_inv_skill", 2),
		(lt, ":best_inv_skill", 3),
		(lt, ":best_loot_skill", 2),
		(assign, reg0, 0),
		(try_begin),
			(lt, ":num_companions", 1),#change 2011-06-07
			(assign, reg0, -1),
		(try_end),
	  (else_try),
		(assign, reg0, 1),
		(gt, ":num_companions", 0),
		(assign, reg0, 2),
	  (try_end),

	  (eq, reg0, 2),
])
]
