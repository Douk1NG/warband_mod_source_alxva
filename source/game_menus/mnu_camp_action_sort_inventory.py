# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

camp_action_sort_inventory_menu = [
("camp_action_sort_inventory",0,
     "Choose what to sort by.",
     "none",
     [
          (try_begin),
            (neq, "$g_player_icon_state", pis_ship),
          (assign, "$g_player_icon_state", pis_normal),
             (party_get_slot, ":player_party", "$marshalship"),
             (ge, ":player_party", 0),
             (set_fixed_point_multiplier, 100),
             (position_set_x, pos1, 70),
             (position_set_y, pos1, 5),
             (position_set_z, pos1, 75),
             (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":player_party", pos1),
             (try_end),
         ],
      [
        ("camp_sort_by_cost",
         [], "Sort inventory by cost.",
         [
         (call_script, "script_rearrange_inventory","trp_player", 1),
         (display_message, "@Your inventory is now sorted by cost."),
         ],
         ),

        ("camp_sort_by_type",
         [], "Sort inventory by type.",
         [
        (call_script, "script_rearrange_inventory","trp_player", 2),
        (display_message, "@Your inventory is now sorted by type."),
        ]
       ),
       ("camp_sort_leave_to_menu",[],"Back to camp menu.",
        [(jump_to_menu, "mnu_camp"),
        ]
       ),
     ]
  )
]
