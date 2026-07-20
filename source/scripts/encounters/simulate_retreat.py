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

simulate_retreat_scripts = [
##  # script_siege_defender_tactic_apply
# Input: arg1 = players_side_damage, arg2 = enemy_side_damage, arg3 = continue_battle s5 = title_string
# Output: none
("simulate_retreat",
    [
      (call_script, "script_music_set_situation_with_culture", mtf_sit_killed),
      (set_show_messages, 0),
      (store_script_param, ":players_side_damage", 1),
      (store_script_param, ":enemy_side_damage", 2),
      (store_script_param, ":continue_battle", 3),

      (assign, ":players_side_strength", 0),
      (assign, ":enemy_side_strength", 0),

      (assign, ":do_calculate", 1),
      (try_begin),
        (try_for_agents, ":cur_agent"),
          (agent_is_human, ":cur_agent"),
          (agent_is_alive, ":cur_agent"),
          (agent_set_slot, ":cur_agent", slot_agent_is_alive_before_retreat, 1),#needed for simulation

          (agent_get_troop_id, ":cur_troop", ":cur_agent"),
          (store_character_level, ":cur_level", ":cur_troop"),
          (val_add, ":cur_level", 5),
          (try_begin),
            (troop_is_hero, ":cur_troop"),
            (val_add, ":cur_level", 5),
          (try_end),
          (try_begin),
            (agent_is_ally, ":cur_agent"),
            (val_add, ":players_side_strength", ":cur_level"),
          (else_try),
            (val_add, ":enemy_side_strength", ":cur_level"),
          (try_end),
        (try_end),
        (eq, "$pin_player_fallen", 0),
        (lt, ":enemy_side_strength", ":players_side_strength"),
        (eq, ":continue_battle", 1),
        (assign, ":do_calculate", 0),
      (try_end),

      (try_begin),
        (eq, ":do_calculate", 1),

        (assign, "$g_last_mission_player_damage", 0),
        (party_clear, "p_temp_party"),
        (party_clear, "p_temp_party_2"),
        (call_script, "script_simulate_battle_with_agents_aux", 0, ":players_side_damage"),
        (call_script, "script_simulate_battle_with_agents_aux", 1, ":enemy_side_damage"),

        (assign, ":display_casualties", 0),

        (try_begin),
          (gt, "$g_last_mission_player_damage", 0),
          (assign, ":display_casualties", 1),
          (assign, reg1, "$g_last_mission_player_damage"),
          (str_store_string, s12, "str_casualty_display_hp"),
        (else_try),
          (str_clear, s12),
        (try_end),

        (call_script, "script_print_casualties_to_s0", "p_temp_party", 1),
        (try_begin),
          (party_get_num_companion_stacks, ":num_stacks", "p_temp_party"),
          (gt, ":num_stacks", 0),
          (assign, ":display_casualties", 1),
        (try_end),
        (str_store_string_reg, s10, s0),

        (call_script, "script_print_casualties_to_s0", "p_temp_party_2", 1),
        (try_begin),
          (party_get_num_companion_stacks, ":num_stacks", "p_temp_party_2"),
          (gt, ":num_stacks", 0),
          (assign, ":display_casualties", 1),
        (try_end),
        (str_store_string_reg, s11, s0),
        (try_begin),
          (eq, ":display_casualties", 1),
          (dialog_box,"str_casualty_display", s5),
        (try_end),
      (try_end),
      (set_show_messages, 1),

      #Calculating morale penalty (can be between 0-30)
      (assign, ":ally_casualties", 0),
      (assign, ":enemy_casualties", 0),
      (assign, ":total_allies", 0),

      (try_for_agents, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (try_begin),
          (agent_is_ally, ":cur_agent"),
          (val_add, ":total_allies", 1),
          (try_begin),
            (neg|agent_is_alive, ":cur_agent"),
            (val_add, ":ally_casualties", 1),
          (try_end),
        (else_try),
          (neg|agent_is_alive, ":cur_agent"),
          (val_add, ":enemy_casualties", 1),
        (try_end),
      (try_end),
      (store_add, ":total_casualties", ":ally_casualties", ":enemy_casualties"),
      (try_begin),
        (gt, ":total_casualties", 0),
        (store_mul, ":morale_adder", ":ally_casualties", 100),
        (val_div, ":morale_adder", ":total_casualties"),
        (val_mul, ":morale_adder", ":ally_casualties"),
        (val_div, ":morale_adder", ":total_allies"),
        (val_mul, ":morale_adder", -30),
        (val_div, ":morale_adder", 100),
        (call_script, "script_change_player_party_morale", ":morale_adder"),
      (try_end),
  ])
]
