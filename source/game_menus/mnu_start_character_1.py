# ======================================================================
# SHARED DEPENDENCY
# Entity: start_character_1 (menu)
# Called by menus in 2 domains: character_creation, diplomacy
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

start_character_1_menu = [
(
    "start_character_1",mnf_disable_all_keys,
    "You were born years ago, in a land far away. Your father was...",
    "none",
    [
    (str_clear,s10),
    (str_clear,s11),
    (str_clear,s12),
    (str_clear,s13),
    (str_clear,s14),
    (str_clear,s15),
    (assign, reg11, "$character_gender"), #SB : every string now uses reg11 for daughter/son boy/girl etc
    ],
    [
    ("start_noble",[],"An impoverished noble.",[
        (assign,"$background_type",cb_noble),
        (str_store_string,s10,"str_story_parent_noble"),
        (jump_to_menu,"mnu_start_character_2"),
    ]),
    ("start_merchant",[],"A travelling merchant.",[
        (assign,"$background_type",cb_merchant),
        (str_store_string,s10,"str_story_parent_merchant"),
        (jump_to_menu,"mnu_start_character_2"),
    ]),
    ("start_guard",[],"A veteran warrior.",[
        (assign,"$background_type",cb_guard),
        (str_store_string,s10,"str_story_parent_guard"),
        (jump_to_menu,"mnu_start_character_2"),
    ]),
    ("start_forester",[],"A hunter.",[
        (assign,"$background_type",cb_forester),
        (str_store_string,s10,"str_story_parent_forester"),
        (jump_to_menu,"mnu_start_character_2"),
    ]),
    ("start_nomad",[],"A steppe nomad.",[
        (assign,"$background_type",cb_nomad),
        (str_store_string,s10,"str_story_parent_nomad"),
        (jump_to_menu,"mnu_start_character_2"),
    ]),
    ("start_thief",[],"A thief.",[
        (assign,"$background_type",cb_thief),
        (str_store_string,s10,"str_story_parent_thief"),
        (jump_to_menu,"mnu_start_character_2"),
    ]),
    #SB: could say "Your father was... The Church" instead of "A Priest/s"
    ("start_priest",[],"A fleeting memory.",[
        (assign,"$background_type",cb_priest),
        (str_store_string,s10,"str_story_parent_priest"),
        (jump_to_menu,"mnu_start_character_2"),
    ]),
    ("go_back",[],"Go back",
     [(jump_to_menu,"mnu_start_game_1"),
    ]),
    ]
  )
]
