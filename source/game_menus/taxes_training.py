# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

taxes_training_menus = [
  (
    "collect_taxes",mnf_disable_all_keys,
    "As the party member with the highest trade skill ({reg2}), {reg3?you expect:{s1} expects} that collecting taxes from here will take {reg4} days...",
    "none",
    [(call_script, "script_get_max_skill_of_player_party", "skl_trade"),
     (assign, ":max_skill", reg0),
     (assign, reg2, reg0),
     (assign, ":max_skill_owner", reg1),
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s1, ":max_skill_owner"),
     (try_end),
     (assign, ":tax_quest_expected_revenue", 3000),
     (try_begin),
       (party_slot_eq, "$current_town", slot_party_type, spt_town),
       (assign, ":tax_quest_expected_revenue", 6000),
     (try_end),

     (try_begin),
       (quest_slot_eq, "qst_collect_taxes", slot_quest_current_state, 0),
       (store_add, ":max_skill_plus_thirty", ":max_skill", 30),
       (try_begin),
         (party_slot_eq, "$current_town", slot_party_type, spt_town),
         (store_div, "$qst_collect_taxes_total_hours", 24* 7 * 30, ":max_skill_plus_thirty"),
       (else_try),
         #Village
         (store_div, "$qst_collect_taxes_total_hours", 24 * 3 * 30, ":max_skill_plus_thirty"),
       (try_end),

       (call_script, "script_party_count_fit_for_battle", "p_main_party"),
       (val_add, reg0, 20),
       (val_mul, "$qst_collect_taxes_total_hours", 20),
       (val_div, "$qst_collect_taxes_total_hours", reg0),


       (quest_set_slot, "qst_collect_taxes", slot_quest_target_amount, "$qst_collect_taxes_total_hours"),
       (store_div, ":menu_begin_time", "$qst_collect_taxes_total_hours", 20),#between %5-%25
       (store_div, ":menu_end_time", "$qst_collect_taxes_total_hours", 4),
       (assign, ":unrest_begin_time", ":menu_end_time"),#between %25-%75
       (store_mul, ":unrest_end_time", "$qst_collect_taxes_total_hours", 3),
       (val_div, ":unrest_end_time", 4),

       (val_mul, ":tax_quest_expected_revenue", 2),
       (store_div, "$qst_collect_taxes_hourly_income", ":tax_quest_expected_revenue", "$qst_collect_taxes_total_hours"),

       (store_random_in_range, "$qst_collect_taxes_menu_counter", ":menu_begin_time", ":menu_end_time"),
       (store_random_in_range, "$qst_collect_taxes_unrest_counter", ":unrest_begin_time", ":unrest_end_time"),
       (assign, "$qst_collect_taxes_halve_taxes", 0),
     (try_end),
     (quest_get_slot, ":target_hours", "qst_collect_taxes", slot_quest_target_amount),
     (store_div, ":target_days", ":target_hours", 24),
     (val_mul, ":target_days", 24),
     (try_begin),
       (lt, ":target_days", ":target_hours"),
       (val_add, ":target_days", 24),
     (try_end),
     (val_div, ":target_days", 24),
     (assign, reg4, ":target_days"),
     ],
    [
      ("start_collecting", [], "Start collecting.",
       [(assign, "$qst_collect_taxes_currently_collecting", 1),
        (try_begin),
          (quest_slot_eq, "qst_collect_taxes", slot_quest_current_state, 0),
          (quest_set_slot, "qst_collect_taxes", slot_quest_current_state, 1),
        (try_end),
        (rest_for_hours_interactive, 1000, 5, 0), #rest while not attackable
        (assign,"$auto_enter_town","$current_town"),
        (assign, "$g_town_visit_after_rest", 1),
        (change_screen_return),
        ]),
      ("collect_later", [], "Put it off until later.",
       [(try_begin),
          (party_slot_eq, "$current_town", slot_party_type, spt_town),
          (jump_to_menu, "mnu_town"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
        ]),
    ]
  ),
  (
    "collect_taxes_complete",mnf_disable_all_keys,
    ##diplomacy start+
    ##Replace "him" with "{reg4?her:him}"
    "You've collected {reg3} denars in taxes from {s3}. {s19} will be expecting you to take the money to {reg4?her:him}.",
    ##diplomacy end+
    "none",
    [(str_store_party_name, s3, "$current_town"),
     (quest_get_slot, ":quest_giver", "qst_collect_taxes", slot_quest_giver_troop),
     (str_store_troop_name, s19, ":quest_giver"),
     ##diplomacy start+

     (try_begin),
       (eq, "$qst_collect_taxes_halve_taxes", 0),
       (call_script, "script_change_player_relation_with_center", "$current_town", -2),
     (try_end),
     (call_script, "script_succeed_quest", "qst_collect_taxes"),

     #SB : add renown to tax collector
     (try_begin),
       (call_script, "script_get_max_skill_of_player_party", "skl_trade"),
       (neq, reg1, "trp_player"),
       (call_script, "script_change_troop_renown", reg1, dplmc_companion_skill_renown),
     (try_end),

     (quest_get_slot, reg3, "qst_collect_taxes", slot_quest_gold_reward),
     ##Store quest giver gender to reg4
     (call_script, "script_dplmc_store_troop_is_female_reg", ":quest_giver", 4), #SB : use other script
     ##diplomacy end+
     ],
    [
      ("continue", [], "Continue...",
       [(change_screen_return),
        ]),
    ]
  ),
  (
    "collect_taxes_rebels_killed",0,
    "Your quick action and strong arm have successfully put down the revolt.\
 Surely, anyone with a mind to rebel against you will think better of it after this.",
    "none",
    [
    ],
    [
      ("continue", [], "Continue...",
       [(change_screen_map),
        ]),
    ]
  ),
  (
    "collect_taxes_failed",mnf_disable_all_keys,
##diplomacy start+ fix gender of pronoun
    "You could collect only {reg3} denars as tax from {s3} before the revolt broke out.\
 {s1} won't be happy, but some silver will placate {reg4?her:him} better than nothing at all...",
##diplomacy end+
    "none",
    [#SB : set up picture
     (try_begin),
       (eq, "$character_gender", tf_male),
       (set_background_mesh, "mesh_pic_escape_1"),
     (else_try),
       (eq, "$character_gender", tf_male),
       (set_background_mesh, "mesh_pic_escape_1_fem"),
     (try_end),
     (str_store_party_name, s3, "$current_town"),
     (quest_get_slot, ":quest_giver", "qst_collect_taxes", slot_quest_giver_troop),
     ##diplomacy start+ store gender of quest giver in reg4
     (call_script, "script_dplmc_store_troop_is_female", ":quest_giver"),
     (assign, reg4, reg0),
     ##diplomacy end+
     (str_store_troop_name, s1, ":quest_giver"),
     (quest_get_slot, reg3, "qst_collect_taxes", slot_quest_gold_reward),
     (call_script, "script_fail_quest", "qst_collect_taxes"),
     (quest_set_slot, "qst_collect_taxes", slot_quest_current_state, 4),
     (rest_for_hours, 0, 0, 0), #stop resting
     ],
    [
      ("continue", [], "Continue...",
        [#SB : lose renown
          (call_script, "script_change_troop_renown", "trp_player", -2),
          (change_screen_map),
        ]),
    ]
  ),
  (
    "collect_taxes_revolt_warning",0,
    "The people of {s3} are outraged at your demands and decry it as nothing more than extortion.\
 They're getting very restless, and they may react badly if you keep pressing them.",
    "none",
    [(str_store_party_name, s3, "$current_town"),
     ],
    [
      ("continue_collecting_taxes", [], "Ignore them and continue.",
       [ #SB : objectionable action
       (call_script, "script_objectionable_action", tmt_egalitarian, "str_repress_farmers"),
       (change_screen_return),]),
      ("halve_taxes", [(quest_get_slot, ":quest_giver_troop", "qst_collect_taxes", slot_quest_giver_troop),
                       (str_store_troop_name, s1, ":quest_giver_troop"),],
       "Agree to reduce your collection by half. ({s1} may be upset)",
       [(assign, "$qst_collect_taxes_halve_taxes", 1),
        (change_screen_return),
        ]),
    ]
  ),
  (
    "collect_taxes_revolt",0,
    "You are interrupted while collecting the taxes at {s3}. A large band of angry {reg9?peasants:townsmen} is marching nearer,\
 shouting about the exorbitant taxes and waving torches and weapons. It looks like they aim to fight you!",
    "none",
    [(str_store_party_name, s3, "$current_town"),
     #SB : town pictures
     (try_begin),
       (party_slot_eq, "$current_town", slot_party_type, spt_village),
       (assign, reg9, 1),
       (set_background_mesh, "mesh_pic_villageriot"),
     (else_try),
       (set_background_mesh, "mesh_pic_townriot"),
       (assign, reg9, 0),
     (try_end),
     ],
    [
      ("continue", [], "Continue...",
       [(set_jump_mission,"mt_back_alley_revolt"),
        (quest_get_slot, ":target_center", "qst_collect_taxes", slot_quest_target_center),
        (try_begin),
          (party_slot_eq, ":target_center", slot_party_type, spt_town),
          (party_get_slot, ":town_alley", ":target_center", slot_town_alley),
        (else_try),
          (party_get_slot, ":town_alley", ":target_center", slot_castle_exterior),
        (try_end),
        (modify_visitors_at_site,":town_alley"),
        (reset_visitors),
        (assign, ":num_rebels", 6),
        (store_character_level, ":level", "trp_player"),
        (val_div, ":level", 5),
        (val_add, ":num_rebels", ":level"),
        (set_visitors, 1, "trp_tax_rebel", ":num_rebels"),
        (jump_to_scene,":town_alley"),
        (change_screen_mission),
        ]),
    ]
  ),

# They must learn field discipline and the steadiness to follow orders in combat before they can be thought to use arms.",
  (
    "train_peasants_against_bandits",0,
    "As the party member with the highest training skill ({reg2}), {reg3?you expect:{s1} expects} that getting some peasants ready for practice will take {reg4} hours.",
    "none",
    [(call_script, "script_get_max_skill_of_player_party", "skl_trainer"),
     (assign, ":max_skill", reg0),
     (assign, reg2, reg0),
     (assign, ":max_skill_owner", reg1),
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s1, ":max_skill_owner"),
     (try_end),
     (store_sub, ":needed_hours", 20, ":max_skill"),
     (val_mul, ":needed_hours", 3),
     (val_div, ":needed_hours", 5),
     (store_sub, reg4, ":needed_hours", "$qst_train_peasants_against_bandits_num_hours_trained"),
     ],
    [
      ("make_preparation", [], "Train them.",
       [
         (assign, "$qst_train_peasants_against_bandits_currently_training", 1),
         (rest_for_hours_interactive, 1000, 5, 0), #rest while not attackable
         (assign, "$auto_enter_town", "$current_town"),
         (assign, "$g_town_visit_after_rest", 1),
         (change_screen_return),
         ]),
      ("train_later", [], "Put it off until later.",
       [
         (jump_to_menu, "mnu_village"),
        ]),
    ]
  ),
  (
    "train_peasants_against_bandits_ready",0,
    "You put the peasants through the basics of soldiering, discipline and obedience.\
 You think {reg0} of them {reg1?have:has} fully grasped the training and {reg1?are:is} ready for some practice.",
    "none",
    [
      (store_character_level, ":level", "trp_player"),
      (val_div, ":level", 10),
      (val_add, ":level", 1),
      (quest_get_slot, ":quest_target_amount", "qst_train_peasants_against_bandits", slot_quest_target_amount),
      (quest_get_slot, ":quest_current_state", "qst_train_peasants_against_bandits", slot_quest_current_state),
      (val_sub, ":quest_target_amount", ":quest_current_state"),
      (assign, ":max_random", ":level"),
      (val_min, ":max_random", ":quest_target_amount"),
      (val_add, ":max_random", 1),
      (store_random_in_range, ":random_number", 1, ":max_random"),
      (assign, "$g_train_peasants_against_bandits_num_peasants", ":random_number"),
      (assign, reg0, ":random_number"),
      (store_sub, reg1, ":random_number", 1),
      (str_store_troop_name_by_count, s0, "trp_trainee_peasant", ":random_number"),
     ],
    [
      ("peasant_start_practice", [], "Start the practice fight.",
       [
         (set_jump_mission,"mt_village_training"),
         (quest_get_slot, ":target_center", "qst_train_peasants_against_bandits", slot_quest_target_center),
         (party_get_slot, ":village_scene", ":target_center", slot_castle_exterior),
         (modify_visitors_at_site, ":village_scene"),
         (reset_visitors),
         (set_visitor, 0, "trp_player"),
         (set_visitors, 1, "trp_trainee_peasant", "$g_train_peasants_against_bandits_num_peasants"),
         (set_jump_entry, 11),
         (jump_to_scene, ":village_scene"),
         (jump_to_menu, "mnu_train_peasants_against_bandits_training_result"),
         (music_set_situation, 0),
         (change_screen_mission),
         ]),
      ]
    ),
  (
    "train_peasants_against_bandits_training_result",mnf_disable_all_keys,
    "{s0}",
    "none",
    [
      (assign, reg5, "$g_train_peasants_against_bandits_num_peasants"),
      (str_store_troop_name_by_count, s0, "trp_trainee_peasant", "$g_train_peasants_against_bandits_num_peasants"),
      (try_begin),
        (eq, "$g_train_peasants_against_bandits_training_succeeded", 0),
        (str_store_string, s0, "@You were beaten. The peasants are heartened by their success, but the lesson you wanted to teach them probably didn't get through..."),
      (else_try),
        (str_store_string, s0, "@After beating your last opponent, you explain to the peasants how to better defend themselves against such an attack. Hopefully they'll take the experience on board and will be prepared next time."),
        (quest_get_slot, ":quest_current_state", "qst_train_peasants_against_bandits", slot_quest_current_state),
        (val_add, ":quest_current_state", "$g_train_peasants_against_bandits_num_peasants"),
        (quest_set_slot, "qst_train_peasants_against_bandits", slot_quest_current_state, ":quest_current_state"),
      (try_end),
     ],
    [
      ("continue", [], "Continue...",
       [
         (try_begin),
           (quest_get_slot, ":quest_current_state", "qst_train_peasants_against_bandits", slot_quest_current_state),
           (quest_slot_eq, "qst_train_peasants_against_bandits", slot_quest_target_amount, ":quest_current_state"),
           (jump_to_menu, "mnu_train_peasants_against_bandits_attack"),
         (else_try),
           (change_screen_map),
         (try_end),
         ]),
      ]
    ),
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
    ),
  (
    "train_peasants_against_bandits_attack_result",mnf_scale_picture|mnf_disable_all_keys,
    "{s9}",
    "none",
    [
      (try_begin),
        (eq, "$g_battle_result", 1),
        (str_store_string, s9, "@The bandits are broken!\
 Those few who remain alive and conscious run off with their tails between their legs,\
 terrified of the peasants and their new champion."),
        (call_script, "script_succeed_quest", "qst_train_peasants_against_bandits"),
        (jump_to_menu, "mnu_train_peasants_against_bandits_success"),
      (else_try),
        (call_script, "script_fail_quest", "qst_train_peasants_against_bandits"),
        (str_store_string, s9, "@Try as you might, you could not defeat the bandits.\
 Infuriated, they raze the village to the ground to punish the peasants,\
 and then leave the burning wasteland behind to find greener pastures to plunder."),
        (set_background_mesh, "mesh_pic_looted_village"),
      (try_end),
     ],
    [
      ("continue", [], "Continue...",
       [(try_begin),
          (call_script, "script_village_set_state",  "$current_town", svs_looted),
          (party_set_slot, "$current_town", slot_village_raid_progress, 0),
          (party_set_slot, "$current_town", slot_village_recover_progress, 0),
          (call_script, "script_change_player_relation_with_center", "$g_encountered_party", -3),
          (call_script, "script_end_quest", "qst_train_peasants_against_bandits"),
        (try_end),
        (change_screen_map),
    ]),
      ]
    ),

   (
    "train_peasants_against_bandits_success",mnf_disable_all_keys,
    "The bandits are broken!\
 Those few who remain run off with their tails between their legs,\
 terrified of the peasants and their new champion.\
 The villagers have little left in the way of wealth after their ordeal,\
 but they offer you all they can find to show their gratitude.",
    "none",
    [(party_clear, "p_temp_party"),
     #SB : probably apply casualties before adding new troops?
     (quest_get_slot, ":amount_trained", "qst_train_peasants_against_bandits", slot_quest_target_amount),
     (store_faction_of_party, ":village_faction", "$current_town"), #assuming player trains them with local weapons
     (faction_get_slot, ":recruit_troop", ":village_faction", slot_faction_tier_1_troop),
     (party_add_members, "$current_town", ":recruit_troop", ":amount_trained"),
     (party_remove_members, "$current_town", "trp_farmer", ":amount_trained"),

     (call_script, "script_end_quest", "qst_train_peasants_against_bandits"),
     (call_script, "script_change_player_relation_with_center", "$current_town", 4),

     (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
     (try_for_range, ":slot_no", num_equipment_kinds ,max_inventory_items + num_equipment_kinds),
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", 50),
        (troop_set_inventory_slot, ":merchant_troop", ":slot_no", -1),
     (try_end),
     (call_script, "script_add_log_entry", logent_helped_peasants, "trp_player",  "$current_town", -1, -1),
     #(set_background_mesh, "mesh_pic_mb_warrior_3"), #SB : background mesh
    ],
    [
      ("village_bandits_defeated_accept",[],"Take it as your just due.",[(jump_to_menu, "mnu_auto_return_to_map"),
                                                                         (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
                                                                         (troop_sort_inventory, ":merchant_troop"),
                                                                         (change_screen_loot, ":merchant_troop"),
                                                                       ]),
      ("village_bandits_defeated_cont",[],  "Refuse, stating that they need these items more than you do.",[
      (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 3),
      (call_script, "script_change_player_honor", 1),
      (change_screen_map)]),
    ],
  ),
]
