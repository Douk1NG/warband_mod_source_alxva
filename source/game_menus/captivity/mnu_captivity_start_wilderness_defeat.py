# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

captivity_start_wilderness_defeat_menu = [
(
    "captivity_start_wilderness_defeat",0,
    "Your enemies take you prisoner.",
    "none",
    [
       (assign, "$g_player_is_captive", 1),
       (assign,"$auto_menu",-1),
       (assign, "$capturer_party", "$g_encountered_party"),

       (try_begin),
         (party_stack_get_troop_id, ":party_leader", "$g_encountered_party", 0),
         (is_between, ":party_leader", active_npcs_begin, active_npcs_end),
         (troop_slot_eq, ":party_leader", slot_troop_occupation, slto_kingdom_hero),
         (store_sub, ":kingdom_hero_id", ":party_leader", active_npcs_begin),
         (set_achievement_stat, ACHIEVEMENT_BARON_GOT_BACK, ":kingdom_hero_id", 1),
       (try_end),

       (jump_to_menu, "mnu_captivity_wilderness_taken_prisoner"),
    ],
    []
  )
]
