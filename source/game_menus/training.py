# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

training_menus = [
  (
    "training_ground",0,
    "You approach a training field where you can practice your martial skills. What kind of training do you want to do?",
    "none",
    [
      (try_begin), #SB : track slot
        (party_get_slot, ":scene_no", slot_grounds_track, "$g_encountered_party"),
        (le, ":scene_no", 0),
        (store_add, ":scene_no", "scn_training_ground_horse_track_1", "$g_encountered_party"),
        (val_sub, ":scene_no", training_grounds_begin),
        (party_set_slot, "$g_encountered_party", slot_grounds_track, ":scene_no"),
      (try_end),
      (try_begin), #SB : melee/ranged slot
        (party_get_slot, ":scene_no", slot_grounds_melee, "$g_encountered_party"),
        (le, ":scene_no", 0),
        (store_add, ":scene_no", "scn_training_ground_ranged_melee_1", "$g_encountered_party"),
        (val_sub, ":scene_no", training_grounds_begin),
        (party_set_slot, "$g_encountered_party", slot_grounds_melee, ":scene_no"),
      (try_end),
      (assign, "$g_training_ground_melee_training_scene", ":scene_no"),


      #SB : modify this interval
      (party_get_skill_level, ":training", "p_main_party", "skl_trainer"), #from 0 to 10
      (try_begin), #grab trainer troop if it isn't linked
        (party_get_slot, ":trainer_troop", "$g_encountered_party", slot_grounds_trainer),
        (try_begin),
          (le, ":trainer_troop", 0),
          (store_sub, ":trainer_troop", "$g_encountered_party", training_grounds_begin),
          (val_add, ":trainer_troop", training_ground_trainers_begin),
          (party_set_slot, "$g_encountered_party", slot_grounds_trainer, ":trainer_troop"),
        (try_end),
        (troop_get_slot, ":difficulty", ":trainer_troop", slot_troop_trainer_training_difficulty), #from 0 to 4
        (val_add, ":training", ":difficulty"), #0 to 14
      (try_end),
      (val_div, ":training", 2), #0 to 7
      (val_max, ":training", 3),
      (try_begin), #was $g_training_ground_training_count
        (party_slot_ge, "$g_encountered_party", slot_grounds_count, ":training"),
        (party_set_slot, "$g_encountered_party", slot_grounds_count, 0),
        # (assign, "$g_training_ground_training_count", 0),
        (rest_for_hours, 1, 5, 0), #rest while not attackable
        (assign, "$auto_enter_town", "$g_encountered_party"),
        (change_screen_return),
      (try_end),
      #SB : set background mesh, player troop
      (assign, "$g_player_troop", "trp_player"),
      (set_background_mesh, "mesh_pic_mb_warrior_1"),
      ],
    [
      ("camp_trainer",
       [], "Speak with the trainer.",
       [
         (set_jump_mission, "mt_training_ground_trainer_talk"),
         # no need to reset visitors, trainer is always there
         # (modify_visitors_at_site, "$g_training_ground_melee_training_scene"),
         # (reset_visitors),
         (set_jump_entry, 5),
         (jump_to_scene, "$g_training_ground_melee_training_scene"),
         (change_screen_mission),
         (music_set_situation, 0),
         ]),
      ("camp_train_melee",
       [
         (neg|troop_is_wounded, "trp_player"),
         (call_script, "script_party_count_fit_for_battle", "p_main_party"),
         (gt, reg0, 1),
         ], "Sparring practice.",
       [
         (assign, "$g_mt_mode", ctm_melee),
         (jump_to_menu, "mnu_training_ground_selection_details_melee_1"),
         (music_set_situation, 0),
         ]),
      ("camp_train_archery",[], "Ranged weapon practice.",
       [
         (jump_to_menu, "mnu_training_ground_selection_details_ranged_1"),
         (music_set_situation, 0),
         ]),
      ("camp_train_mounted",[], "Horseback practice.",
       [
         (assign, "$g_mt_mode", ctm_mounted),
         (jump_to_menu, "mnu_training_ground_selection_details_mounted"),
         (music_set_situation, 0),
         ]),

      ("go_to_track",[(eq, "$cheat_mode", 1)],"{!}Cheat: Go to track.",
       [
         (set_jump_mission, "mt_ai_training"),
         (try_begin), #SB : slots
           (party_get_slot, ":scene_no", slot_grounds_track, "$g_encountered_party"),
           (le, ":scene_no", 0),
           (store_add, ":scene_no", "scn_training_ground_horse_track_1", "$g_encountered_party"),
           (val_sub, ":scene_no", training_grounds_begin),
         (try_end),
         (jump_to_scene, ":scene_no"),
         (change_screen_mission),
        ]
       ),
      ("go_to_range",[(eq, "$cheat_mode", 1)],"{!}Cheat: Go to range.",
       [
         (set_jump_mission, "mt_ai_training"),
         (jump_to_scene, "$g_training_ground_melee_training_scene"),
         (change_screen_mission),
        ]
       ),
      ("leave",[],"Leave.",
       [(change_screen_return),
        ]),
    ]
  ),
  ("training_ground_selection_details_melee_1",0,
   "How many opponents will you go against?",
   "none",
   [
     (call_script, "script_write_fit_party_members_to_stack_selection", "p_main_party", 1),
     (troop_get_slot, "$temp", "trp_stack_selection_amounts", 1), #number of men fit
     (assign, "$temp_2", 1),
     ],
    [
      ("camp_train_melee_num_men_1",[(ge, "$temp", 1)], "One.",
       [
         (assign, "$temp", 1),
         (jump_to_menu, "mnu_training_ground_selection_details_melee_2"),
         ]),
      ("camp_train_melee_num_men_2",[(ge, "$temp", 2)], "Two.",
       [
         (assign, "$temp", 2),
         (jump_to_menu, "mnu_training_ground_selection_details_melee_2"),
         ]),
      ("camp_train_melee_num_men_3",[(ge, "$temp", 3)], "Three.",
       [
         (assign, "$temp", 3),
         (jump_to_menu, "mnu_training_ground_selection_details_melee_2"),
         ]),
      ("camp_train_melee_num_men_4",[(ge, "$temp", 4)], "Four.",
       [
         (assign, "$temp", 4),
         (jump_to_menu, "mnu_training_ground_selection_details_melee_2"),
         ]),
      ("go_back_dot",[],"Cancel.",
       [
         (jump_to_menu, "mnu_training_ground"),
        ]),
      ]
  ),
  ("training_ground_selection_details_melee_2",0,
   "Choose your opponent:^{s1}^{reg1}:",
   "none",
    [
      (assign, reg1, "$temp_2"),
      (troop_get_slot, "$temp_3", "trp_stack_selection_amounts", 0), #number of slots

      #SB : show current list
      (str_clear, s1),
      (store_sub, ":end", "$temp_2", 1),
      (try_for_range, ":slot_index", 0, ":end"),
        (store_add, reg0, ":slot_index", 1),
        (troop_get_slot, ":troop_id", "trp_temp_array_a", ":slot_index"),
        (gt, ":troop_id", 0),
        (str_store_troop_name, s2, ":troop_id"),
        (str_store_string, s1, "@{s1}^{reg0}: {s2}"),
      # (else_try),
        # (str_store_string, s1, "@{s1}^{reg0}:"),
      (try_end),
    ],
    [
      ("training_ground_selection_details_melee_random", [], "Choose randomly.",
       [(call_script, "script_training_ground_sub_routine_2_for_melee_details", -1),]),
      ("go_back_dot",[],"Go back.",
       [(jump_to_menu, "mnu_training_ground"),]
       ), #SB : stack built from loop
      ]+
      [("stack"+str(x), [(call_script, "script_cf_training_ground_sub_routine_1_for_melee_details", x),], "{s0}",
       [(call_script, "script_training_ground_sub_routine_2_for_melee_details", x),])
       for x in range(1, 20)]
  ),
  ("training_ground_selection_details_mounted",0,
   "What kind of weapon do you want to train with?",
   "none",
   [
   #SB : background mesh
   (set_background_mesh, "mesh_pic_mb_warrior_2"),
   ],
    [
      ("camp_train_mounted_details_1",[], "One handed weapon.",
       [
         (call_script, "script_start_training_at_training_ground", itp_type_one_handed_wpn, 0),
         ]),
      ("camp_train_mounted_details_2",[], "Polearm.",
       [
         (call_script, "script_start_training_at_training_ground", itp_type_polearm, 0),
         ]),
      ("camp_train_mounted_details_3",[], "Bow.",
       [
         (call_script, "script_start_training_at_training_ground", itp_type_bow, 0),
         ]),
      ("camp_train_mounted_details_4",[], "Thrown weapon.",
       [
         (call_script, "script_start_training_at_training_ground", itp_type_thrown, 0),
         ]),
      ("go_back_dot",[],"Go back.",
       [(jump_to_menu, "mnu_training_ground"),
        ]
       ),
      ]
  ),
  ("training_ground_selection_details_ranged_1",0,
   "What kind of ranged weapon do you want to train with?",
   "none",
   [
   (set_background_mesh, "mesh_pic_mb_warrior_4"), #SB : background mesh
   ],
    [
      ("camp_train_ranged_weapon_bow",[], "Bow and arrows.",
       [
         (assign, "$g_mt_mode", ctm_ranged),
         (assign, "$temp", itp_type_bow),
         (jump_to_menu, "mnu_training_ground_selection_details_ranged_2"),
         ]),
      ("camp_train_ranged_weapon_crossbow",[], "Crossbow.",
       [
         (assign, "$g_mt_mode", ctm_ranged),
         (assign, "$temp", itp_type_crossbow),
         (jump_to_menu, "mnu_training_ground_selection_details_ranged_2"),
         ]),
      ("camp_train_ranged_weapon_thrown",[], "Throwing Knives.",
       [
         (assign, "$g_mt_mode", ctm_ranged),
         (assign, "$temp", itp_type_thrown),
         (jump_to_menu, "mnu_training_ground_selection_details_ranged_2"),
         ]),
      ("go_back_dot",[],"Go back.",
       [(jump_to_menu, "mnu_training_ground"),
        ]
       ),
      ]
  ),
  ("training_ground_selection_details_ranged_2",0,
   "What range do you want to practice at?",
   "none",
   [
   (set_background_mesh, "mesh_pic_mb_warrior_4"), #SB : background mesh
   ],
    [
      ("camp_train_ranged_details_1",[], "10 yards.",
       [
         (call_script, "script_start_training_at_training_ground", "$temp", 10),
         ]),
      ("camp_train_ranged_details_2",[], "20 yards.",
       [
         (call_script, "script_start_training_at_training_ground", "$temp", 20),
         ]),
      ("camp_train_ranged_details_3",[], "30 yards.",
       [
         (call_script, "script_start_training_at_training_ground", "$temp", 30),
         ]),
      ("camp_train_ranged_details_4",[], "40 yards.",
       [
         (call_script, "script_start_training_at_training_ground", "$temp", 40),
         ]),
      ("camp_train_ranged_details_5",[(eq, "$g_mt_mode", ctm_ranged),], "50 yards.",
       [
         (call_script, "script_start_training_at_training_ground", "$temp", 50),
         ]),
      ("camp_train_ranged_details_6",[(eq, "$g_mt_mode", ctm_ranged),], "60 yards.",
       [
         (call_script, "script_start_training_at_training_ground", "$temp", 60),
         ]),
      ("camp_train_ranged_details_7",[(eq, "$g_mt_mode", ctm_ranged),], "70 yards.",
       [
         (call_script, "script_start_training_at_training_ground", "$temp", 70),
         ]),
      ("go_back_dot",[],"Go back.",
       [(jump_to_menu, "mnu_training_ground"),
        ]
       ),
      ]
  ),
  ("training_ground_description",0,
   "{s0}",
   "none",
   [
   #Sb : format string here instead of script_start_training_at_training_ground
   (store_sub, reg0, "$g_training_ground_training_num_enemies", 1),
   (store_sub, ":string", "$g_mt_mode", 1),
   (val_add, ":string", "str_ctm_melee"),
   (str_store_string, s0, ":string"),

   ],
    [
      ("continue", [], "Continue...",
       [
         (jump_to_scene, "$g_training_ground_training_scene"),
         (change_screen_mission),
        ]
       ),
      ]
  ),
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
   ),
]
