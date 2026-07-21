# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

train_peasants_against_bandits_attack_menu = [
(
    "train_peasants_against_bandits_attack",0,
    "As you get ready to continue the training, a sentry from the village runs up to you, shouting alarums.\
 The bandits have been spotted on the horizon, riding hard for {s3}.\
 The elder begs that you organize your newly-trained militia and face them.",
    "none",
    [
    (str_store_party_name, s3, "$current_town"),
     ],
    [
      ("peasants_against_bandits_attack_resist", [], "Prepare for a fight!",
       [ ## SB : use new bandit script
        # (store_random_in_range, ":random_no", 0, 3),
        # (try_begin),
          # (eq, ":random_no", 0),
          # (assign, ":bandit_troop", "trp_bandit"),
        # (else_try),
          # (eq, ":random_no", 1),
          # (assign, ":bandit_troop", "trp_mountain_bandit"),
        # (else_try),
          # (assign, ":bandit_troop", "trp_forest_bandit"),
        # (try_end),
        (call_script, "script_center_get_bandits", "$current_town", 0),
        (assign, ":bandit_troop", reg0),
        (party_get_slot, ":scene_to_use", "$g_encountered_party", slot_castle_exterior),
        (modify_visitors_at_site, ":scene_to_use"),
        (reset_visitors),
        (store_character_level, ":level", "trp_player"),
        (val_div, ":level", 2),
        (store_add, ":min_bandits", ":level", 16),
        (store_add, ":max_bandits", ":min_bandits", 6),
        (store_random_in_range, ":random_no", ":min_bandits", ":max_bandits"),
        (set_visitors, 0, ":bandit_troop", ":random_no"),
        # (assign, ":num_villagers", ":max_bandits"),
        #SB : more accurate count
        (party_count_members_of_type, ":num_villagers", "$current_town", "trp_farmer"), #disallow peasant woman
        (val_min, ":num_villagers", ":max_bandits"), #dckplmc
        (set_visitors, 2, "trp_trainee_peasant", ":num_villagers"),
        (set_party_battle_mode),
        (set_battle_advantage, 0),
        (assign, "$g_battle_result", 0),
        (set_jump_mission,"mt_village_attack_bandits"),
        (jump_to_scene, ":scene_to_use"),
        (assign, "$g_next_menu", "mnu_train_peasants_against_bandits_attack_result"),
        (jump_to_menu, "mnu_battle_debrief"),
        (assign, "$g_mt_mode", vba_after_training),
        (change_screen_mission),
        ]),
      ]
    )
]
