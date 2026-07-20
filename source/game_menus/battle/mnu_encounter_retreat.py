# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

encounter_retreat_menu = [
(
    "encounter_retreat",0,
    "You tell {reg4} of your troops to hold the enemy while you retreat with the rest of your party.",
    "none",
    [
     ],
    [
      ("continue",[],"Continue...",
	  [
###Troop commentary changes begin
          (call_script, "script_objectionable_action", tmt_aristocratic, "str_flee_battle"),
          (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
          (try_for_range, ":stack_no", 0, ":num_stacks"),
              (party_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
              (is_between, ":stack_troop", active_npcs_begin, active_npcs_end),
              (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
              (store_troop_faction, ":victorious_faction", ":stack_troop"),
              (call_script, "script_add_log_entry", logent_player_retreated_from_lord_cowardly, "trp_player",  -1, ":stack_troop", ":victorious_faction"),
          (try_end),
###Troop commentary changes end
        (party_ignore_player, "$g_encountered_party", 1),
        (leave_encounter),
		(change_screen_return),
          ##diplomacy begin
          #(assign, "$g_move_fast", 1),
          ##diplomacy end
          ]),
    ]
  )
]
