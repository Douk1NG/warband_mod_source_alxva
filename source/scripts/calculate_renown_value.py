# ======================================================================
# SHARED DEPENDENCY
# Entity: calculate_renown_value (script)
# Called by menus in 2 domains: battle, siege
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

calculate_renown_value_scripts = [
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
  ])
]
