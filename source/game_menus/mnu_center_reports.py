# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

center_reports_menu = [
(
    "center_reports",0,
    "Town Name: {s1}^Rent Income: {reg1} denars^Tariff Income: {reg2} denars^Food Stock: for {reg3} days",
    "none",
    [(party_get_slot, ":town_food_store", "$g_encountered_party", slot_party_food_store),
     (call_script, "script_center_get_food_consumption", "$g_encountered_party"),
     (assign, ":food_consumption", reg0),
     (try_begin),
       (gt, ":food_consumption", 0),
       (store_div, reg3, ":town_food_store", ":food_consumption"),
     (else_try),
       (assign, reg3, 9999),
     (try_end),
     (str_store_party_name, s1, "$g_encountered_party"),
     (party_get_slot, reg1, "$g_encountered_party", slot_center_accumulated_rents),
     (party_get_slot, reg2, "$g_encountered_party", slot_center_accumulated_tariffs),
     ],
    [
      ("to_price_and_productions", [], "Show prices and productions.",
       [(jump_to_menu, "mnu_price_and_production"),
        ]),

      ("go_back_dot",[],"Go back.",
       [(try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
          (jump_to_menu, "mnu_village"),
        (else_try),
          (jump_to_menu, "mnu_town"),
        (try_end),
        ]),
    ]
  )
]
