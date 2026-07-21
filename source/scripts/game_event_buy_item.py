# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

game_event_buy_item_scripts = [
# script_get_trade_penalty
# This script is called from the game engine when player buys an item.
# INPUT:
# param1: item_kind_id
("game_event_buy_item",
    [
      (store_script_param_1, ":item_kind_id"),
      (store_script_param_2, ":reclaim_mode"),
      (try_begin),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":multiplier", "$g_encountered_party", ":item_slot_no"),
        (try_begin),
          (eq, ":reclaim_mode", 0),
          (val_add, ":multiplier", 20),
        (else_try),
          (val_add, ":multiplier", 30),
        (try_end),

        (store_item_value, ":item_value", ":item_kind_id"),
        (try_begin),
          (ge, ":item_value", 100),
          (store_sub, ":item_value_sub_100", ":item_value", 100),
          (store_div, ":item_value_sub_100_div_8", ":item_value_sub_100", 8),
          (val_add, ":multiplier", ":item_value_sub_100_div_8"),
        (try_end),
        (val_min, ":multiplier", maximum_price_factor),

        (party_set_slot, "$g_encountered_party", ":item_slot_no", ":multiplier"),
      (try_end),
  ])
]
