# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

captivity_end_propose_ransom_menu = [
(
    "captivity_end_propose_ransom",0,
    "You spend long hours in the sunless dank of the dungeon, more than you can count.\
 Suddenly one of your captors enters your cell with an offer;\
 he proposes to free you in return for {reg5} denars of your hidden wealth. You decide to...",
    "none",
    [
      (assign, reg5, "$player_ransom_amount"),
    ],
    [
      ("captivity_end_ransom_accept",
      [
        (store_troop_gold,":player_gold", "trp_player"),
        (ge, ":player_gold","$player_ransom_amount")
      ],"Accept the offer.",
      [
        (play_cue_track, "track_escape"),
        (assign, "$g_player_is_captive", 0),
        (troop_remove_gold, "trp_player", "$player_ransom_amount"),
        (try_begin),
          (party_is_active, "$capturer_party"),
          (party_relocate_near_party, "p_main_party", "$capturer_party", 1),
        (try_end),
        (call_script, "script_set_parties_around_player_ignore_player", 8, 12), #it was radius:2 and hours:6, but players make lots of complains about consequent battle losses after releases from captivity then I changed this.
        (assign, "$g_player_icon_state", pis_normal),
        (set_camera_follow_party, "p_main_party"),
        (rest_for_hours, 0, 0, 0), #stop resting
        (change_screen_return),
      ]),
      ("captivity_end_ransom_accept_2",
      [
        (store_troop_gold,":player_gold", "trp_player"),
        (lt, ":player_gold","$player_ransom_amount"),

        (try_begin),
          (store_troop_gold, ":player_gold", "trp_player"),
          (assign, reg6, ":player_gold"),
        (try_end),
      ],"Pay him {reg6} denars, promising to pay the rest when you are free.",
      [
        (play_cue_track, "track_escape"),
        (assign, "$g_player_is_captive", 0),

        (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
        (party_get_slot, ":guild_master_troop", "$current_town",slot_town_elder),

        (store_troop_gold,":player_gold", "trp_player"),
        (troop_remove_gold, "trp_player", ":player_gold"),
        (store_sub, ":new_debts", "$player_ransom_amount", ":player_gold"),
        (try_begin),
            (gt, ":town_lord", -1),
            (call_script, "script_change_debt_to_troop", ":town_lord", ":new_debts"),
        (else_try),
            (gt, ":guild_master_troop", -1),
            (call_script, "script_change_debt_to_troop", ":guild_master_troop", ":new_debts"),
        (try_end),

        (val_max, ":new_debts", 1),
        (val_div, ":new_debts", 200),
        (try_begin),
            (gt, ":new_debts", 0),
            (val_mul, ":new_debts", -1),
            (call_script, "script_change_troop_renown", "trp_player", ":new_debts"),
        (try_end),

        (try_begin),
          (party_is_active, "$capturer_party"),
          (party_relocate_near_party, "p_main_party", "$capturer_party", 1),
        (try_end),
        (call_script, "script_set_parties_around_player_ignore_player", 8, 12), #it was radius:2 and hours:6, but players make lots of complains about consequent battle losses after releases from captivity then I changed this.
        (assign, "$g_player_icon_state", pis_normal),
        (set_camera_follow_party, "p_main_party"),
        (rest_for_hours, 0, 0, 0), #stop resting
		(call_script, "script_simple_remove_disguise"),
        (change_screen_return),
      ]),
      ("captivity_end_ransom_deny",
      [
      ],"Refuse him, wait for something better.",
      [
        (try_begin),
            (eq, "$g_sexual_content", 2),
	        (this_or_next|eq, "$character_gender", 1),(eq, "$g_nohomo", 0),
            (jump_to_menu, "mnu_fucked_by_enemy_prison"),
        (else_try),
            (assign, "$g_player_is_captive", 1),
            (store_random_in_range, reg(8), 16, 22),
            (call_script, "script_stay_captive_for_hours", reg8),
            (assign,"$auto_menu", "mnu_captivity_castle_check"),
            (change_screen_return),
        (try_end),
      ]),
    ]
  )
]
