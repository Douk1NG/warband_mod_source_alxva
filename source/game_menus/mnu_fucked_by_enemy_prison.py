# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

fucked_by_enemy_prison_menu = [
(
    "fucked_by_enemy_prison",0,
    "The guards are infuriated by your refusal to pay the ransom.\
    They tell you that if you are not willing to pay, then there is no longer any reason to treat you humanely.\One of the guards then reaches for the keys to your cell, grins, and says that he is going to teach you a lesson.",
    "none",
    [
     ],
    [
      ("continue",[],"Continue...",
       [

            (assign, "$g_player_is_captive", 1),
            (store_random_in_range, reg(8), 16, 22),
            (call_script, "script_stay_captive_for_hours", reg8),
            (assign,"$auto_menu", "mnu_captivity_castle_check"),

		    (store_faction_of_party, ":capturer_faction", "$capturer_party"),

            (faction_get_slot, ":troop_prison_guard", ":capturer_faction", slot_faction_prison_guard_troop),
            (call_script, "script_change_troop_renown", "trp_player", -2),

            (try_begin),
                (eq, ":troop_prison_guard", -1),
                (assign, ":troop_prison_guard", "trp_hired_blade"),
            (try_end),

            (troop_set_slot, "trp_temp_array_a", 0, "trp_player"),
            (troop_set_slot, "trp_temp_array_a", 1, ":troop_prison_guard"),
            (troop_set_slot, "trp_temp_array_a", 2, -1),
            (troop_set_slot, "trp_temp_array_a", 3, ":troop_prison_guard"),
            (assign, "$g_sex_position", 2),
            (assign, "$f_cons1", -1), #Non-con
			(assign, "$f_cons2", 0), #Con
			(assign, "$f_cons3", 0), #Con
			(assign, "$f_cons4", 0), #Con
            (call_script, "script_start_fucking", 4, "scn_dungeon"),

         ]),
      ]
  )
]
