# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

captivity_castle_check_menu = [
(
    "captivity_castle_check",0,
    "stub",
    "none",
    [
        (store_random_in_range, reg(7), 0, 100),
        (try_begin),
		  (party_is_active, "$capturer_party"),
		  (store_faction_of_party, ":capturer_faction", "$capturer_party"),
		  (is_between, ":capturer_faction", kingdoms_begin, kingdoms_end),
		  (store_relation, ":relation_w_player_faction", ":capturer_faction", "fac_player_faction"),
		  (ge, ":relation_w_player_faction", 0),
          #SB : this doesn't make much sense when the player is unaffiliated
          (jump_to_menu,"mnu_captivity_end_exchanged_with_prisoner"),
		(else_try),
          (lt, reg(7), 40),
          (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
          (val_mul, ":player_renown", 2),
          (store_character_level, ":player_level", "trp_player"),
          (store_mul, "$player_ransom_amount", ":player_level", 50),
          (val_add, "$player_ransom_amount", 100),
          (val_add, "$player_ransom_amount", ":player_renown"),
          (store_troop_gold, reg3, "trp_player"),
          (store_div, ":player_gold_div_20", reg3, 20),
          (val_add, "$player_ransom_amount", ":player_gold_div_20"),

          #(gt, reg3, "$player_ransom_amount"),
          (jump_to_menu,"mnu_captivity_end_propose_ransom"),
        (else_try),
          (lt, reg(7), 45), #4% chance to be set free
          (jump_to_menu,"mnu_captivity_end_exchanged_with_prisoner"),
        (else_try),
          (jump_to_menu,"mnu_captivity_castle_remain"),
        (try_end),
    ],
    []
  )
]
