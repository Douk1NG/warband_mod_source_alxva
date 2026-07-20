# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

auto_trade_menu = [
(
    "auto_trade",0,
    "Trade goods will automatically be bought if their price is low enough or sold if their price is high enough. You can adjust the price thresholds, disable auto trading for certain goods, or set minimum and maximum quantities to avoid filling your inventory with one type of item or selling items you want to keep.",
    "none",
  [],
  [
    ("continue",[],"Continue...",
    [
      (call_script, "script_auto_trade_at_center", "$current_town"),
      (jump_to_menu, "$g_next_menu"),
    ]),
    ("change_settings",[],"Change settings.",[(start_presentation, "prsnt_auto_trade_options"),]),
    ("go_back",[],"Go back",[(jump_to_menu, "$g_next_menu")]),
  ]
  )
]
