# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

training_ground_training_result_menu = [
("training_ground_training_result",mnf_disable_all_keys,
   "{s7}{s2}",
   "none",
   [
     (store_skill_level, ":trainer_skill", "skl_trainer", "trp_player"),
     (store_add, ":trainer_skill_multiplier", 5, ":trainer_skill"),
     (call_script, "script_write_fit_party_members_to_stack_selection", "p_main_party", 1),
     (str_clear, s2),
     (troop_get_slot, ":num_fit", "trp_stack_selection_amounts", 1),
     (troop_get_slot, ":num_slots", "trp_stack_selection_amounts", 0),
     (try_begin),
       (gt, "$g_training_ground_training_success_ratio", 0),
       (store_mul, ":xp_ratio_to_add", "$g_training_ground_training_success_ratio", "$g_training_ground_training_success_ratio"),
       (try_begin),
         (eq, "$g_training_ground_training_success_ratio", 100),
         (val_mul, ":xp_ratio_to_add", 2), #2x when perfect
       (try_end),
       (try_begin),
         (eq, "$g_mt_mode", ctm_melee),
         (val_div, ":xp_ratio_to_add", 2),
       (try_end),
       (val_div, ":xp_ratio_to_add", 10), # value over 1000
       (try_begin),
         (gt, ":num_fit", 8),
         (val_mul, ":xp_ratio_to_add", 3),
         (assign, ":divisor", ":num_fit"),
         (convert_to_fixed_point, ":divisor"),
         (store_sqrt, ":divisor", ":divisor"),
         (convert_to_fixed_point, ":xp_ratio_to_add"),
         (val_div, ":xp_ratio_to_add", ":divisor"),
       (try_end),
##       (assign, reg0, ":xp_ratio_to_add"),
##       (display_message, "@xp earn ratio: {reg0}/1000"),
       (store_mul, ":xp_ratio_to_add_with_trainer_skill", ":xp_ratio_to_add", ":trainer_skill_multiplier"),
       (val_div, ":xp_ratio_to_add_with_trainer_skill", 10),
       (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
       (store_add, ":end_cond", ":num_slots", 2),
       (try_for_range, ":i_slot", 2, ":end_cond"),
         (troop_get_slot, ":amount", "trp_stack_selection_amounts", ":i_slot"),
         (troop_get_slot, ":troop_id", "trp_stack_selection_ids", ":i_slot"),
         (assign, ":end_cond_2", ":num_stacks"),
         (try_for_range, ":stack_no", 0, ":end_cond_2"),
           (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":stack_no"),
           (eq, ":stack_troop", ":troop_id"),
           (assign, ":end_cond_2", 0), #break
           (call_script, "script_cf_training_ground_sub_routine_for_training_result", ":troop_id", ":stack_no", ":amount", ":xp_ratio_to_add_with_trainer_skill"),
           (str_store_troop_name_by_count, s1, ":troop_id", ":amount"),
           #SB : hero name count
           (try_begin),
             (troop_is_hero, ":troop_id"),
             (assign, reg2, 1),
           (else_try),
             (assign, reg2, 0),
             (assign, reg1, ":amount"),
           (try_end),
           (str_store_string, s2, "@{s2}^{reg2?:{reg1} }{s1} earned {reg0} experience."),
         (try_end),
       (try_end),
       (try_begin),
         (eq, "$g_mt_mode", ctm_melee),
         (store_mul, ":special_xp_ratio_to_add", ":xp_ratio_to_add", 3),
         (val_div, ":special_xp_ratio_to_add", 2),
         (try_for_range, ":enemy_index", 0, "$g_training_ground_training_num_enemies"),
           (troop_get_slot, ":troop_id", "trp_temp_array_a", ":enemy_index"),
           (assign, ":end_cond_2", ":num_stacks"),
           (try_for_range, ":stack_no", 0, ":end_cond_2"),
             (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":stack_no"),
             (eq, ":stack_troop", ":troop_id"),
             (assign, ":end_cond_2", 0), #break
             (call_script, "script_cf_training_ground_sub_routine_for_training_result", ":troop_id", ":stack_no", 1, ":special_xp_ratio_to_add"),
             (str_store_troop_name, s1, ":troop_id"),
             (str_store_string, s2, "@{s2}^{s1} earned an additional {reg0} experience."),
           (try_end),
         (try_end),
       (try_end),
       (try_begin),
         (call_script, "script_cf_training_ground_sub_routine_for_training_result", "trp_player", -1, 1, ":xp_ratio_to_add"),
         (str_store_string, s2, "@^You earned {reg0} experience.{s2}"),
       (try_end),
     (try_end),
     (try_begin),
       (eq, "$g_training_ground_training_success_ratio", 0),
       (str_store_string, s7, "@The training didn't go well at all."),
     (else_try),
       (lt, "$g_training_ground_training_success_ratio", 25),
       (str_store_string, s7, "@The training didn't go well at all."),
     (else_try),
       (lt, "$g_training_ground_training_success_ratio", 50),
       (str_store_string, s7, "@The training didn't go very well."),
     (else_try),
       (lt, "$g_training_ground_training_success_ratio", 75),
       (str_store_string, s7, "@The training went quite well."),
     (else_try),
       (lt, "$g_training_ground_training_success_ratio", 99),
       (str_store_string, s7, "@The training went very well."),
     (else_try),
       (str_store_string, s7, "@The training went perfectly."),
     (try_end),

     ],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_training_ground"),
        ]
       ),
      ]
   )
]
