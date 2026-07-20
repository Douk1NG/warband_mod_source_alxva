# ======================================================================
# SHARED DEPENDENCY
# Entity: battle_debrief (menu)
# Called by menus in 3 domains: battle, siege, village
# ======================================================================

# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

battle_debrief_menu = [
(
    "battle_debrief",mnf_scale_picture|mnf_disable_all_keys,
    "{s11}^^Your Casualties:{s8}{s10}^^Enemy Casualties:{s9}",
    "none",
    [
     (try_begin),
       (eq, "$g_battle_result", 1),
       (call_script, "script_change_troop_renown", "trp_player", "$battle_renown_value"),
       #SB : also distribute amount to companions, maybe pretender/spouse in party as well
       (assign, ":amount", 0),
       (try_for_range, ":companions", companions_begin, companions_end),
         (main_party_has_troop, ":companions"),
         (val_add, ":amount", 1),
       (try_end),
       (try_begin),
         (gt, ":amount", 0),
         (store_div, ":amount", "$battle_renown_value", ":amount"),
         (val_max, ":amount", dplmc_companion_battle_renown),
         (try_for_range, ":companions", companions_begin, companions_end),
           (main_party_has_troop, ":companions"),
           # (neg|troop_is_wounded, ":companions"), #survived, or stayed at the back
           (call_script, "script_change_troop_renown", ":companions", ":amount"),
         (try_end),
       (try_end),

       (try_begin),
         (ge, "$g_encountered_party", 0),
         (party_is_active, "$g_encountered_party"),
         (party_get_template_id, ":encountered_party_template", "$g_encountered_party"),
         (eq, ":encountered_party_template", "pt_kingdom_caravan_party"),

         (get_achievement_stat, ":number_of_village_raids", ACHIEVEMENT_THE_BANDIT, 0),
         (get_achievement_stat, ":number_of_caravan_raids", ACHIEVEMENT_THE_BANDIT, 1),
         (val_add, ":number_of_caravan_raids", 1),
         (set_achievement_stat, ACHIEVEMENT_THE_BANDIT, 1, ":number_of_caravan_raids"),

         (try_begin),
           (ge, ":number_of_village_raids", 3),
           (ge, ":number_of_caravan_raids", 3),
           (unlock_achievement, ACHIEVEMENT_THE_BANDIT),
         (try_end),
       (try_end),

       (try_begin),
         (party_get_current_terrain, ":cur_terrain", "p_main_party"),
         (eq, ":cur_terrain", rt_snow),
         (get_achievement_stat, ":number_of_victories_at_snowy_lands", ACHIEVEMENT_BEST_SERVED_COLD, 0),
         (val_add, ":number_of_victories_at_snowy_lands", 1),
         (set_achievement_stat, ACHIEVEMENT_BEST_SERVED_COLD, 0, ":number_of_victories_at_snowy_lands"),

         (try_begin),
           (eq, ":number_of_victories_at_snowy_lands", 10),
           (unlock_achievement, ACHIEVEMENT_BEST_SERVED_COLD),
         (try_end),
       (try_end),

       (try_begin),
         (ge, "$g_enemy_party", 0),
         (party_is_active, "$g_enemy_party"),
         (party_stack_get_troop_id, ":stack_troop", "$g_enemy_party", 0),
         (eq, ":stack_troop", "trp_mountain_bandit"),

         (get_achievement_stat, ":number_of_victories_aganist_mountain_bandits", ACHIEVEMENT_MOUNTAIN_BLADE, 0),
         (val_add, ":number_of_victories_aganist_mountain_bandits", 1),
         (set_achievement_stat, ACHIEVEMENT_MOUNTAIN_BLADE, 0, ":number_of_victories_aganist_mountain_bandits"),

         (try_begin),
           (eq, ":number_of_victories_aganist_mountain_bandits", 10),
           (unlock_achievement, ACHIEVEMENT_MOUNTAIN_BLADE),
         (try_end),
       (try_end),

       (try_begin),
         (is_between, "$g_ally_party", walled_centers_begin, walled_centers_end),
         (unlock_achievement, ACHIEVEMENT_NONE_SHALL_PASS),
       (try_end),

       (try_begin),
         (eq, "$g_joined_battle_to_help", 1),
         (unlock_achievement, ACHIEVEMENT_GOOD_SAMARITAN),
       (try_end),
     (try_end),

     (assign, "$g_joined_battle_to_help", 0),
     (call_script, "script_count_casualties_and_adjust_morale"),#new
     (call_script, "script_encounter_calculate_fit"),

     (call_script, "script_party_count_fit_regulars", "p_main_party"),
     (assign, "$playerparty_postbattle_regulars", reg0),

     (try_begin),
       (eq, "$g_battle_result", 1),
       (eq, "$g_enemy_fit_for_battle", 0),
       (str_store_string, s11, "@You were victorious!"),
#       (play_track, "track_bogus"), #clear current track.
#       (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
       (try_begin),
         (gt, "$g_friend_fit_for_battle", 1),
         (set_background_mesh, "mesh_pic_victory"),
       (try_end),
     (else_try),
       (eq, "$g_battle_result", -1),
       (ge, "$g_enemy_fit_for_battle",1),
       (this_or_next|le, "$g_friend_fit_for_battle",0),
       (le, "$playerparty_postbattle_regulars", 0),
       (str_store_string, s11, "@The battle was lost. Your forces were utterly crushed."), #SB : "The battle"
       (set_background_mesh, "mesh_pic_defeat"),
     (else_try),
       (eq, "$g_battle_result", -1),
       (str_store_string, s11, "@Your companions carry you away from the fighting."),
		 ##diplomacy start+ Test gender with script
       #(troop_get_type, ":is_female", "trp_player"),#<- replaced
       (try_begin),
         #(eq, ":is_female", 1),#<- replaced
         (eq, tf_female, "$character_gender"),#<- added
         (set_background_mesh, "mesh_pic_wounded_fem"),
       (else_try),
         (set_background_mesh, "mesh_pic_wounded"),
       (try_end),
		 ##diplomacy end+
     (else_try),
       (eq, "$g_battle_result", 1),
       (str_store_string, s11, "@You have defeated the enemy."),
       (try_begin),
         (gt, "$g_friend_fit_for_battle", 1),
         (set_background_mesh, "mesh_pic_victory"),
       (try_end),
     (else_try),
       (eq, "$g_battle_result", 0),
       (str_store_string, s11, "@You have retreated from the fight."),
     (try_end),
#NPC companion changes begin
##check for excessive casualties, more forgiving if battle result is good
     (try_begin),
        (gt, "$playerparty_prebattle_regulars", 9),
        (store_add, ":divisor", 3, "$g_battle_result"),
        (store_div, ":half_of_prebattle_regulars", "$playerparty_prebattle_regulars", ":divisor"),
        (lt, "$playerparty_postbattle_regulars", ":half_of_prebattle_regulars"),
        (call_script, "script_objectionable_action", tmt_egalitarian, "str_excessive_casualties"),
     (try_end),
#NPC companion changes end

     (call_script, "script_print_casualties_to_s0", "p_player_casualties", 0),
     (str_store_string_reg, s8, s0),
     (call_script, "script_print_casualties_to_s0", "p_enemy_casualties", 0),
     (str_store_string_reg, s9, s0),
     (str_clear, s10),
     (try_begin),
       (eq, "$any_allies_at_the_last_battle", 1),
       (call_script, "script_print_casualties_to_s0", "p_ally_casualties", 0),
       (str_store_string, s10, "@^^Ally Casualties:{s0}"),
     (try_end),
     ],
    [
      ("continue",[],"Continue...",[(jump_to_menu, "$g_next_menu"),]),
    ]
  )
]
