# ======================================================================
# SHARED DEPENDENCY
# Entity: village_start_attack (menu)
# Called by menus in 2 domains: dickplomacy, village
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

village_start_attack_menu = [
( #SB : added fugitive related strings
    "village_start_attack",mnf_disable_all_keys|mnf_scale_picture,
    "Some of the angry villagers grab their tools and prepare to resist you.\
 It looks like you'll have a fight on your hands if you continue.{s1}",
    "none",
    [
       (set_background_mesh, "mesh_pic_villageriot"),
       (call_script, "script_party_count_members_with_full_health","p_main_party"),
       (assign, ":player_party_size", reg0),
       (call_script, "script_party_count_members_with_full_health","$current_town"),
       (assign, ":villagers_party_size", reg0),

       (try_begin), #SB : tweak fight avoidance parameters
         #also if we lost but reduced their numbers, don't allow this condition to be true
         (neq, "$g_battle_result", -1),
         (this_or_next|le, ":villagers_party_size", 30),
         (gt, ":player_party_size", ":villagers_party_size"),
         (jump_to_menu, "mnu_village_loot_no_resist"),
       (else_try),
         (this_or_next|eq, ":villagers_party_size", 0),
         (eq, "$g_battle_result", 1),
         (try_begin),
           (eq, "$g_battle_result", 1),
           (store_random_in_range, ":enmity", -30, -15),
           (call_script, "script_change_player_relation_with_center", "$current_town", ":enmity"),
           (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
           (gt, ":town_lord", 0),
           (call_script, "script_change_player_relation_with_troop", ":town_lord", -3),
         (try_end),
         (jump_to_menu, "mnu_village_loot_no_resist"),
       (else_try),
         (eq, "$g_battle_result", -1),
         (try_begin), #if we did not knock him out or kill him, he escapes
           (check_quest_active, "qst_hunt_down_fugitive"),
           (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
           (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
           (jump_to_menu, "mnu_village_hunt_down_fugitive_defeated"),
         (else_try),
           (jump_to_menu, "mnu_village_loot_defeat"),
         (try_end),
       (try_end),

       #SB : display string indicating fugitive is here
      (try_begin), #if we did not knock him out or kill him, he escapes
        (check_quest_active, "qst_hunt_down_fugitive"),
        (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
        (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
        (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
        (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
        (str_store_string, s1, "@ From your vantage point you see a man matching the description of {s50} arming himself with a sword during the commotion. If you do not press on the fugitive will slip away!"),
      (else_try),
        (str_clear, s1),
      (try_end),
    ],
    [
      ("village_raid_attack",[],"Charge them.",[
          (store_random_in_range, ":enmity", -10, -5),
          (call_script, "script_change_player_relation_with_center", "$current_town", ":enmity"),
          (try_begin),
            (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
            (gt, ":town_lord", 0),
            (call_script, "script_change_player_relation_with_troop", ":town_lord", -3),
          (try_end),
          #SB : add fugitive as defender here
          (try_begin),
            (check_quest_active, "qst_hunt_down_fugitive"),
            (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
            (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
            (neg|check_quest_failed, "qst_hunt_down_fugitive"),
            (quest_set_slot, "qst_hunt_down_fugitive", slot_quest_current_state, 1), #normally this is activated in dialogs
            (party_add_members, "$current_town", "trp_fugitive", 1),
          (try_end),
          (call_script, "script_calculate_battle_advantage"),
          (set_battle_advantage, reg0),
          (set_party_battle_mode),
          (assign, "$g_battle_result", 0),
          (assign, "$g_village_raid_evil", 1),
          (set_jump_mission,"mt_village_raid"),
          (party_get_slot, ":scene_to_use", "$current_town", slot_castle_exterior),
          (jump_to_scene, ":scene_to_use"),
          (assign, "$g_next_menu", "mnu_village_start_attack"),

          (call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$g_encountered_party"),
###NPC companion changes begin
          (call_script, "script_objectionable_action", tmt_humanitarian, "str_loot_village"),
#NPC companion changes end

          (jump_to_menu, "mnu_battle_debrief"),
          (change_screen_mission),
          ]),
      ("village_raid_leave",[],"Leave this village alone.",[(change_screen_return),
      #SB : fail fugitive quest if player backs away from demands
      (try_begin),
        (check_quest_active, "qst_hunt_down_fugitive"),
        (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
        (neg|check_quest_concluded, "qst_hunt_down_fugitive"),
        (call_script, "script_fail_quest", "qst_hunt_down_fugitive"),
      (try_end),

      ]),
    ],
  )
]
