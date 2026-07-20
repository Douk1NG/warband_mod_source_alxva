# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_trade_auto_sell_begin (menu)
# Called by menus in 2 domains: town, village
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

dplmc_trade_auto_sell_begin_menu = [
(
    "dplmc_trade_auto_sell_begin",0,
    "Items in your inventory whose type is marked as sellable and whose prices \
are below {reg1} denars will be sold to the {reg2?appropriate merchants:elder} \
in the current {reg2?town:village} automatically.  Specifically food, trade \
goods, and books will never be sold. ^^You can change some settings here freely.",
    "none",
  [
	##dplmc+ added section begin
    (this_or_next|is_between, "$current_town", towns_begin, towns_end),
	    (is_between, "$current_town", villages_begin, villages_end),
	(call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
	##dplmc+ added section end
    (assign, reg1, "$g_dplmc_auto_sell_price_limit"),
	 (assign, reg2, 0),
    (try_begin),
      (is_between, "$current_town", towns_begin, towns_end),
      (assign, reg2, 1),
    (try_end),
  ],
  [
    ("continue",[],"Continue...",
    [
      #(call_script, "script_auto_sell_all"),
	  (call_script, "script_dplmc_player_auto_sell_at_center", "$current_town"),
      (jump_to_menu, "$g_next_menu"),
      ]),
    ("change_settings",[],"Change settings.",[(start_presentation, "prsnt_dplmc_auto_sell_options"),]),
    ("go_back",[],"Go back",[(jump_to_menu, "$g_next_menu")]),
  ]
  )
]
