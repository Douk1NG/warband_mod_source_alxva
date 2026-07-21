# ======================================================================
# SHARED DEPENDENCY
# Entity: encounter_init_variables (script)
# Called by menus in 3 domains: battle, castle, siege
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

encounter_init_variables_scripts = [
# script_encounter_init_variables
# Input: arg1 = troop_no
# Output: none
("encounter_init_variables",
    [
      (assign, "$capture_screen_shown", 0),
      (assign, "$loot_screen_shown", 0),
      (assign, "$thanked_by_ally_leader", 0),
      (assign, "$g_battle_result", 0),
      (assign, "$cant_leave_encounter", 0),
      (assign, "$cant_talk_to_enemy", 0),
      (assign, "$last_defeated_hero", 0),
      (assign, "$last_freed_hero", 0),

      (call_script, "script_encounter_calculate_fit"),
      (call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
	  ##diplomacy start+
	  #If terrain advantage is enabled, use it to initialize the variables.
	  (assign, ":terrain_code", -1),
	  (try_begin),
	     (eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
		 (lt, "$g_encounter_is_in_village", 1),#Do not apply to village encounters
	     (try_begin),
	        (encountered_party_is_attacker),
		    (call_script, "script_dplmc_get_terrain_code_for_battle", "$g_encountered_party", "p_main_party"),
	     (else_try),
	        (call_script, "script_dplmc_get_terrain_code_for_battle", "p_main_party", "$g_encountered_party"),
		 (try_end),
		 (assign, ":terrain_code", reg0),
		 #calculate party strength with terrain
		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_main_party", ":terrain_code", 0, 1),
		 (assign, "$g_starting_strength_main_party", reg0),
		 (try_begin),
			#Print debug Message
		    (ge, "$cheat_mode", 1),
		    (assign, reg2, ":terrain_code"),
			(display_message, "@{!}DEBUG - Main party raw strength {reg1}, terrain code {reg2}, modified strength {reg0}"),
		 (try_end),
		 #calculate enemy strength with terrain
		 (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"),
		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_enemy", ":terrain_code", 0, 1),
		 (assign, "$g_starting_strength_enemy_party", reg0),
		 (assign, "$g_strength_contribution_of_player", 100),
		 (try_begin),
		    (ge, "$cheat_mode", 1),#debug
		    (assign, reg2, ":terrain_code"),
			(display_message, "@{!} DEBUG - Enemy party raw strength {reg1}, terrain code {reg2}, modified strength {reg0}"),
		 (try_end),
		 #calculate friends strength with terrain
		 (call_script, "script_party_copy", "p_collective_friends_backup", "p_collective_friends"),
		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_friends", ":terrain_code", 0, 1),
		 (assign, "$g_starting_strength_friends", reg0),
	  (else_try),
	     ##Calculate all party strengths without terrain:
	     #calculate main party strength
         (call_script, "script_party_calculate_strength", "p_main_party", 0),
         (assign, "$g_starting_strength_main_party", reg0),
		 #calculate enemy strength
         (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"),
         (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
         (assign, "$g_starting_strength_enemy_party", reg0),
         (assign, "$g_strength_contribution_of_player", 100),
		 #calculate friends strength
         (call_script, "script_party_copy", "p_collective_friends_backup", "p_collective_friends"),
         (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
         (assign, "$g_starting_strength_friends", reg0),
	  (try_end),
	  ##diplomacy end+

      (store_mul, "$g_strength_contribution_of_player","$g_starting_strength_main_party", 100), # reduce contribution if we are helping someone.

	  (try_begin),
		(gt, "$g_starting_strength_friends", 0), #this new to prevent occasional div by zero error
		(val_div, "$g_strength_contribution_of_player","$g_starting_strength_friends"),
	  (else_try),
		(assign, "$g_strength_contribution_of_player", 100), #Or zero, maybe
	  (try_end),

      (party_clear, "p_routed_enemies"), #new
      (assign, "$num_routed_us", 0),#newtoday
      (assign, "$num_routed_allies", 0),#newtoday
      (assign, "$num_routed_enemies", 0),#newtoday
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop_id", "p_main_party", ":i_stack"),
        (try_begin),
          (troop_set_slot, ":stack_troop_id", slot_troop_player_routed_agents, 0),
          #(troop_set_slot, ":stack_troop_id", slot_troop_enemy_routed_agents, 0),
          #(troop_set_slot, ":stack_troop_id", slot_troop_ally_routed_agents, 0),
        (try_end),
      (try_end),

      (party_get_num_companion_stacks, ":num_stacks", "p_collective_friends"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop_id", "p_collective_friends", ":i_stack"),
        (try_begin),
          #(troop_set_slot, ":stack_troop_id", slot_troop_player_routed_agents, 0),
          #(troop_set_slot, ":stack_troop_id", slot_troop_enemy_routed_agents, 0),
          (troop_set_slot, ":stack_troop_id", slot_troop_ally_routed_agents, 0),
        (try_end),
      (try_end),

      (party_get_num_companion_stacks, ":num_stacks", "p_collective_enemy"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop_id", "p_collective_enemy", ":i_stack"),
        (try_begin),
          #(troop_set_slot, ":stack_troop_id", slot_troop_player_routed_agents, 0),
          (troop_set_slot, ":stack_troop_id", slot_troop_enemy_routed_agents, 0),
          #(troop_set_slot, ":stack_troop_id", slot_troop_ally_routed_agents, 0),
        (try_end),
      (try_end),

      (try_for_range, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end),
        (faction_set_slot, ":cur_faction", slot_faction_num_routed_agents, 0),
      (try_end),

      (assign, "$routed_party_added", 0), #new
      (party_clear, "p_total_enemy_casualties"), #new

      ###(((add wounded troops of enemy to p_total_enemy_casualties
      (party_get_num_companion_stacks, ":num_stacks", "p_collective_enemy"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_collective_enemy", ":stack_no"),
        (party_stack_get_num_wounded, ":stack_wounded_size", "p_collective_enemy", ":stack_no"),
        (gt, ":stack_wounded_size", 0),
        (party_add_members, "p_total_enemy_casualties", ":stack_troop", ":stack_wounded_size"),
        (party_wound_members, "p_total_enemy_casualties", ":stack_troop", ":stack_wounded_size"),
      (try_end),
      ###)))

#      (try_begin),
#        (gt, "$g_ally_party", 0),
#        (call_script, "script_party_copy", "p_ally_party_backup", "p_collective_ally"),
#        (call_script, "script_party_calculate_strength", "p_collective_ally"),
#        (assign, "$g_starting_strength_ally_party", reg0),
#        (store_add, ":starting_strength_factor_combined","$g_starting_strength_ally_party","$g_starting_strength_main_party"),
#         (store_mul, "$g_strength_contribution_of_player","$g_starting_strength_main_party", 80), #reduce contribution if we are helping someone.
#        (val_div, "$g_strength_contribution_of_player",":starting_strength_factor_combined"),
#      (try_end),
  ])
]
