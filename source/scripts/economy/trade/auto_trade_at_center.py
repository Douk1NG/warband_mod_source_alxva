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

auto_trade_at_center_scripts = [
("auto_trade_at_center", [
    (store_script_param, ":center_no", 1),
    (try_begin),
      #For Towns:
      (is_between, ":center_no", towns_begin, towns_end),
      (try_begin),
        #Sell to non-trade good merchants first so player has plenty of cash and inventory space when dealing with goods merchant
        (party_get_slot, ":merchant_troop", ":center_no", slot_town_weaponsmith),
        (ge, ":merchant_troop", 1),
        (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
      (try_end),
      (try_begin),
        (party_get_slot, ":merchant_troop", ":center_no", slot_town_armorer),
        (ge, ":merchant_troop", 1),
        (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
      (try_end),
      (try_begin),
        (party_get_slot, ":merchant_troop", ":center_no", slot_town_horse_merchant),
        (ge, ":merchant_troop", 1),
        (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
      (try_end),
      (try_begin),
        (party_get_slot, ":merchant_troop", ":center_no", slot_town_merchant),
        (ge, ":merchant_troop", 1),
        #Player should be in a good position to buy after selling to other merchants
        (call_script, "script_auto_trade_buy_from_merchant", ":merchant_troop"),
        (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
      (try_end),
    (else_try),
      #For Villages:
      (is_between, ":center_no", villages_begin, villages_end),
      (party_get_slot, ":merchant_troop", ":center_no", slot_town_elder),
      (ge, ":merchant_troop", 1),
      #Villages tend to not have much coin, so we buy first to make sure they can afford the player's goods
      (call_script, "script_auto_trade_buy_from_merchant", ":merchant_troop"),
      (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
    (try_end),
  ])
]
