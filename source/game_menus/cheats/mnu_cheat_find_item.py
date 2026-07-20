# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

cheat_find_item_menu = [
("cheat_find_item",0,
   "{!}Current item range: {reg5} to {reg6}",
   "none",
   [
     (assign, reg5, "$cheat_find_item_range_begin"),
     (store_add, reg6, "$cheat_find_item_range_begin", max_inventory_items),
     (val_min, reg6, "itm_items_end"),
     (val_sub, reg6, 1),
     ],
    [

    #SB : easier debug
      ("cheat_find_item_prev_range",[], "{!}Move to previous range.",
       [
        (val_sub, "$cheat_find_item_range_begin", max_inventory_items),
        (try_begin),
          (lt, "$cheat_find_item_range_begin", 0),
          (assign, "$cheat_find_item_range_begin", itm_items_end-max_inventory_items),
        (try_end),
        (jump_to_menu, "mnu_cheat_find_item"),
       ]
       ),

      ("cheat_find_item_next_range",[], "{!}Move to next item range.",
       [
        (val_add, "$cheat_find_item_range_begin", max_inventory_items),
        (try_begin),
          (ge, "$cheat_find_item_range_begin", "itm_items_end"),
          (assign, "$cheat_find_item_range_begin", 0),
        (try_end),
        (jump_to_menu, "mnu_cheat_find_item"),
       ]
       ),

       ("cheat_find_item_choose_this",[], "{!}Choose from this range.",
       [
        (troop_clear_inventory, "trp_find_item_cheat"),
        (store_add, ":max_item", "$cheat_find_item_range_begin", max_inventory_items),
        (val_min, ":max_item", "itm_items_end"),
        (store_sub, ":num_items_to_add", ":max_item", "$cheat_find_item_range_begin"),
        (try_begin), #SB : even more super-cheats
          (this_or_next|key_is_down, key_left_shift),
          (key_is_down, key_right_shift),
          (try_for_range, ":i_slot", 0, ":num_items_to_add"),
            (store_add, ":item_id", "$cheat_find_item_range_begin", ":i_slot"),
            (item_get_type, ":i_type", ":item_id"),
            (try_begin),
              (eq, ":i_type", itp_type_horse),
              (troop_add_item, "trp_find_item_cheat", ":item_id", imod_champion),
            (else_try),
              (this_or_next|eq, ":i_type", itp_type_shield),
              (is_between, ":i_type", itp_type_head_armor, itp_type_pistol),
              (troop_add_item, "trp_find_item_cheat", ":item_id", imod_lordly),
            (else_try),
              (this_or_next|is_between, ":i_type", itp_type_one_handed_wpn, itp_type_goods),
              (is_between, ":i_type", itp_type_pistol, itp_type_animal),
              (troop_add_item, "trp_find_item_cheat", ":item_id", imod_masterwork),
            (else_try),
              (troop_add_item, "trp_find_item_cheat", ":item_id", imod_plain),
            (try_end),
          (try_end),
          (change_screen_loot, "trp_find_item_cheat"),
        (else_try), #Native behaviour
          (try_for_range, ":i_slot", 0, ":num_items_to_add"),
            (store_add, ":item_id", "$cheat_find_item_range_begin", ":i_slot"),
            (troop_add_items, "trp_find_item_cheat", ":item_id", 1),
          (try_end),
          (change_screen_trade, "trp_find_item_cheat"),
        (try_end),
       ]
       ),

      ("camp_action_4",[],"{!}Back to camp menu.",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  )
]
