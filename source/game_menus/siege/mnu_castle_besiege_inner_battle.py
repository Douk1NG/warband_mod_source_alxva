# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

castle_besiege_inner_battle_menu = [
(
    "castle_besiege_inner_battle",mnf_scale_picture,
    "{s1}",
    "none",
    [
		  # ##diplomacy start+ test gender with script
        # #(troop_get_type, ":is_female", "trp_player"),#<- replaced
        # (try_begin),
          # #(eq, ":is_female", 1),#<- replaced
		  # (eq, "$character_gender", tf_female),#<- added
          # (set_background_mesh, "mesh_pic_siege_sighted_fem"),
        # (else_try),
          # (set_background_mesh, "mesh_pic_siege_sighted"),
        # (try_end),
		  # ##diplomacy end+
        #SB : sally picture more appropriate
        (set_background_mesh, "mesh_pic_sally_out"),
        (assign, ":result", "$g_battle_result"),#will be reset at script_encounter_calculate_fit
        (call_script, "script_encounter_calculate_fit"),

# TODO: To use for the future:
        (try_begin),
          (this_or_next|neq, ":result", 1),
          (this_or_next|le, "$g_friend_fit_for_battle", 0),
          (le, "$g_enemy_fit_for_battle", 0),
          (jump_to_menu, "$g_siege_final_menu"),
        (else_try),
          (call_script, "script_encounter_calculate_fit"),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (try_begin),
            (eq, "$g_siege_battle_state", 0),
            (eq, ":result", 1),
            (assign, "$g_battle_result", 0),
            (jump_to_menu, "$g_siege_final_menu"),
          (else_try),
            (eq, "$g_siege_battle_state", 1),
            (eq, ":result", 1),
            (try_begin), #SB : siege strings
              (eq, "$g_ally_party", "$g_encountered_party"),
              (str_store_string, s1, "@You've been driven away from the walls.\
 Now the attackers are pouring into the streets. If you can defeat them, you can perhaps turn the tide and save the day."),
            (else_try),
              (str_store_string, s1, "@You've breached the town walls,\
 but the stubborn defenders continue to resist you in the streets!\
 You'll have to deal with them before you can attack the keep at the heart of the town."),
            (try_end),
          (else_try),
            (eq, "$g_siege_battle_state", 2),
            (eq, ":result", 1),
            (try_begin), #SB : siege strings
              (eq, "$g_ally_party", "$g_encountered_party"),
              (str_store_string, s1, "@As a last defensive effort, you retreat to the main hall of the keep.\
 You and your remaining soldiers will put up a desperate fight here. If you are defeated, there's no other place to fall back to."),
            (else_try),
              (str_store_string, s1, "@The town centre is yours,\
 but the remaining defenders have retreated to the castle.\
 It must fall before you can complete your victory."),
            (try_end),
          (else_try),
            (jump_to_menu, "$g_siege_final_menu"),
          (try_end),
        (else_try),
          (try_begin),
            (eq, "$g_siege_battle_state", 0),
            (eq, ":result", 1),
            (assign, "$g_battle_result", 0),
            (jump_to_menu, "$g_siege_final_menu"),
          (else_try),
            (eq, "$g_siege_battle_state", 1),
            (eq, ":result", 1),
            (str_store_string, s1, "@The remaining defenders have retreated to the castle as a last defense. You must go in and crush any remaining resistance."),
          (else_try),
            (jump_to_menu, "$g_siege_final_menu"),
          (try_end),
        (try_end),
    ],
    [
      ("continue",[],
       "Continue...",
       [
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (try_begin),
               (eq, "$g_siege_battle_state", 1),
               (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_center),
               (set_jump_mission, "mt_besiege_inner_battle_town_center"),
             (else_try),
               (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_castle),
               (set_jump_mission, "mt_besiege_inner_battle_castle"),
             (try_end),
           (else_try),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_castle),
             (set_jump_mission, "mt_besiege_inner_battle_castle"),
           (try_end),
##           (call_script, "script_calculate_battle_advantage"),
##           (set_battle_advantage, reg0),
           (set_party_battle_mode),
           (jump_to_scene, ":battle_scene"),
           (val_add, "$g_siege_battle_state", 1),
           (assign, "$g_next_menu", "mnu_castle_besiege_inner_battle"),
           (jump_to_menu, "mnu_battle_debrief"),
           (change_screen_mission),
       ]),
    ]
  )
]
