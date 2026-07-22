# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

camp_cheat_party_menu = [
("camp_cheat_party",0,
   "Party cheats:",
   "none",
   [
     (try_begin),
       (neq, "$g_player_icon_state", pis_ship),
     (assign, "$g_player_icon_state", pis_normal),
        (party_get_slot, ":player_party", "$marshalship"),
        (ge, ":player_party", 0),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos1, 70),
        (position_set_y, pos1, 5),
        (position_set_z, pos1, 75),
        (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":player_party", pos1),
        (try_end),
    ],
    [
      ("camp_cheat_heal",[],"Heal party.",
       [
         (heal_party, "p_main_party"),
        ]
       ),

      ("camp_cheat_xp",[],"Add xp to party.",
       [
         (set_show_messages, 0),
         (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
         (try_for_range, ":stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":id", "p_main_party", ":stack"),
            (try_begin),
                (party_stack_get_size, ":size", "p_main_party", ":stack"),
                (call_script, "script_game_get_upgrade_xp", ":id"),
                (store_mul, ":xp", reg0, ":size"),
                (try_begin),
                  (troop_is_hero, ":id"),
                  (store_character_level, ":level", ":id"),
                  (assign, ":end", 100),
                  (try_begin),
                    (le, ":level", 10),
                    (assign, ":xp", 100),
                  (else_try),
                    (le, ":level", 25),
                    (assign, ":xp", 1000),
                  (else_try),
                    (le, ":level", 35),
                    (assign, ":xp", 10000),
                  (else_try),
                    (le, ":level", 50),
                    (assign, ":xp", 30000),
                  (else_try),
                    (le, ":level", 60),
                    (assign, ":xp", 1000000),
                  (else_try),
                    (assign, ":xp", 10000000),
                  (try_end),
                  (try_for_range, ":unused", 0, ":end"),
                    (party_add_xp_to_stack, "p_main_party", ":stack", ":xp"),
                    (add_xp_to_troop, 1, ":id"),
                    (store_character_level, ":cur_level", ":id"),
                    (lt, ":level", ":cur_level"),
                    (assign, ":end", 0),
                  (try_end),
                (else_try),
                  (party_add_xp_to_stack, "p_main_party", ":stack", ":xp"),
                (try_end),
            (try_end),
         (try_end),
         (set_show_messages, 1),
        ]
       ),

      ("camp_cheat_prisoner",[
          (party_get_num_prisoner_stacks, ":stack", "p_main_party"),
          (gt, ":stack", 0),
          (try_for_range, ":i_stack", 0, ":stack"),
            (party_prisoner_stack_get_troop_id, ":troop", "p_main_party", ":i_stack"),
            (neg|troop_is_hero, ":troop"),
            (assign, ":stack", 0),
          (try_end),
          (eq, ":stack", 0),
      ],"Recruit all prisoners.",
       [
         (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
         (try_for_range_backwards, ":stack", 0, ":num_stacks"),
            (party_prisoner_stack_get_troop_id, ":troop", "p_main_party", ":stack"),
            (neg|troop_is_hero, ":troop"),
            (gt, ":troop", 0),
            (party_prisoner_stack_get_size, ":amount", "p_main_party", ":stack"),
            (party_remove_prisoners, "p_main_party", ":troop", ":amount"),
            (party_add_members, "p_main_party", ":troop", ":amount"),
         (try_end),
        ]
       ),

      ("camp_cheat_party_back",[],"Back to cheat menu.",
       [(jump_to_menu, "mnu_camp_cheat"),]
       ),
      ]
  )
]
