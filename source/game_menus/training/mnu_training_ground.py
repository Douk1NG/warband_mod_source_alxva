# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

training_ground_menu = [
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
  )
]
