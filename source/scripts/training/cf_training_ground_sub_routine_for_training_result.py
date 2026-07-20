# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

cf_training_ground_sub_routine_for_training_result_scripts = [
#script_cf_training_ground_sub_routine_for_training_result
# INPUT:
# arg1: troop_id, arg2: stack_no, arg3: troop_count, arg4: xp_ratio_to_add
#OUTPUT:
# none
("cf_training_ground_sub_routine_for_training_result",
   [
     (store_script_param, ":troop_id", 1),
     (store_script_param, ":stack_no", 2),
     (store_script_param, ":amount", 3),
     (store_script_param, ":xp_ratio_to_add", 4),

     (store_character_level, ":level", ":troop_id"),
     (store_add, ":level_added", ":level", 5),
     (store_mul, ":min_hardness", ":level_added", 3),
     (val_min, ":min_hardness", 100),
     (store_sub, ":hardness_dif", ":min_hardness", "$g_training_ground_training_hardness"),
     (val_max, ":hardness_dif", 0),
     (store_sub, ":hardness_dif", 100, ":hardness_dif"),
     (val_mul, ":hardness_dif", ":hardness_dif"),
     (val_div, ":hardness_dif", 10), # value over 1000
##     (assign, reg0, ":hardness_dif"),
##     (display_message, "@Hardness difference: {reg0}/1000"),
     (store_mul, ":xp_ratio_to_add_for_stack", ":xp_ratio_to_add", ":hardness_dif"),
     (val_div, ":xp_ratio_to_add_for_stack", 1000),
     (try_begin),
       (eq, ":troop_id", "trp_player"),
       (val_mul, ":xp_ratio_to_add_for_stack", 1),
     (else_try),
       (try_begin),
         (eq, "$g_mt_mode", ctm_melee),
         (try_begin),
           (this_or_next|troop_is_guarantee_ranged, ":troop_id"),
           (troop_is_guarantee_horse, ":troop_id"),
           (val_div, ":xp_ratio_to_add_for_stack", 4),
         (try_end),
       (else_try),
         (eq, "$g_mt_mode", ctm_mounted),
         (try_begin),
           (neg|troop_is_guarantee_horse, ":troop_id"),
           (assign, ":xp_ratio_to_add_for_stack", 0),
         (try_end),
       (else_try),
         (neg|troop_is_guarantee_ranged, ":troop_id"),
         (assign, ":xp_ratio_to_add_for_stack", 0),
       (try_end),
     (try_end),
     (val_add,  ":level", 1),
     (store_mul, ":xp_to_add", 100, ":level"),
     (val_mul, ":xp_to_add", ":amount"),
     (val_div, ":xp_to_add", 20),
     (val_mul, ":xp_to_add", ":xp_ratio_to_add_for_stack"),
     (val_div, ":xp_to_add", 1000),
     (store_mul, ":max_xp_to_add", ":xp_to_add", 3),
     (val_div, ":max_xp_to_add", 2),
     (store_div, ":min_xp_to_add", ":xp_to_add", 2),
     (store_random_in_range, ":random_xp_to_add", ":min_xp_to_add", ":max_xp_to_add"),
     (gt, ":random_xp_to_add", 0),
     (try_begin),
       (troop_is_hero, ":troop_id"),
       (add_xp_to_troop, ":random_xp_to_add", ":troop_id"),
       (store_div, ":proficiency_to_add", ":random_xp_to_add", 50),
       (try_begin),
         (gt, ":proficiency_to_add", 0),
         (troop_raise_proficiency, ":troop_id", "$g_training_ground_used_weapon_proficiency", ":proficiency_to_add"),
       (try_end),
     (else_try),
       (party_add_xp_to_stack, "p_main_party", ":stack_no", ":random_xp_to_add"),
     (try_end),
     (assign, reg0, ":random_xp_to_add"),
     ])
]
