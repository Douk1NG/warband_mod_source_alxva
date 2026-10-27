# ======================================================================
# Bridge menu: Camp Hub Walk -> camp scene
# Hub presentations cannot reliably change_screen_mission directly
# (menu stays open behind the presentation), so Walk jumps here and
# this menu init performs the mission jump (same ops as the old
# mnu_camp camp_walk option).
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

camp_hub_walk_menu = [
 ("camp_hub_walk", 0,
    "Walking around the campsite...",
    "none",
    [
      # Guard: jump to scene only when requested from Hub. Leaving the
      # scene returns here - then go to camp (auto-opens Hub), no re-jump.
      (try_begin),
        (eq, "$g_camp_hub_walk_jump", 1),
        (assign, "$g_camp_hub_walk_jump", 0),
        (set_jump_mission, "mt_camp"),
        (call_script, "script_setup_camp_scene"),
        (change_screen_mission),
      (else_try),
        (jump_to_menu, "mnu_camp"),
      (try_end),
    ],
    [
      ("camp_hub_walk_return", [], "Return.",
        [
          (change_screen_return),
        ]
      ),
    ]
  )
]
