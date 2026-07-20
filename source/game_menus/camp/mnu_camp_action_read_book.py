# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

camp_action_read_book_menu = [
("camp_action_read_book",0,
   "Choose a book to read:",
   "none",
   [],
    [
      ("action_read_book_1",[(player_has_item, "itm_book_tactics"),
                             (item_slot_eq, "itm_book_tactics", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_tactics"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_tactics"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_2",[(player_has_item, "itm_book_persuasion"),
                             (item_slot_eq, "itm_book_persuasion", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_persuasion"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_persuasion"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_3",[(player_has_item, "itm_book_leadership"),
                             (item_slot_eq, "itm_book_leadership", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_leadership"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_leadership"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_4",[(player_has_item, "itm_book_intelligence"),
                             (item_slot_eq, "itm_book_intelligence", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_intelligence"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_intelligence"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_5",[(player_has_item, "itm_book_trade"),
                             (item_slot_eq, "itm_book_trade", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_trade"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_trade"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_6",[(player_has_item, "itm_book_weapon_mastery"),
                             (item_slot_eq, "itm_book_weapon_mastery", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_weapon_mastery"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_weapon_mastery"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_7",[(player_has_item, "itm_book_engineering"),
                             (item_slot_eq, "itm_book_engineering", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_engineering"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_engineering"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("camp_action_4",[],"Back to camp menu.",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  )
]
