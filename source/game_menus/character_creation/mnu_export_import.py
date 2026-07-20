# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

export_import_menu = [
( #export/import from prsnt_companion_overview
    "export_import", mnf_enable_hot_keys,
    "Press C to access {s1}'s character screen and then the statistics button on the bottom left.",
    "none",
    [
    (set_background_mesh, "mesh_pic_mb_warrior_1"),
    # # (set_player_troop, "trp_player"),
    # (change_screen_view_character),
    # # (change_screen_return),
    # (assign, "$talk_context", tc_town_talk),
    # (start_map_conversation, "$g_player_troop"),
    (set_player_troop, "$g_player_troop"),
    (str_store_troop_name_plural, s1, "$g_player_troop"),
    ],
    [
      ("rename",
      [],
      "I never liked the name {s1}...",
      [
        (assign, "$g_presentation_state", rename_companion),
        (start_presentation, "prsnt_name_kingdom"),
      ]),

      ("display_slots",
      [(ge, "$cheat_mode", 1)], "Show me all your secrets...",
      [
        (assign, "$g_talk_troop", "$g_player_troop"),
        (jump_to_menu, "mnu_display_troop_slots"),
      ]),
      ("continue",
      [],
      "Continue...",
      [
        (set_player_troop, "trp_player"),
        (jump_to_menu, "$g_next_menu"),
      ]),
    ]
  )
]
