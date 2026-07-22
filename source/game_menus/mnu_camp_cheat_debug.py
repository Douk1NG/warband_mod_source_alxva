# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

camp_cheat_debug_menu = [
("camp_cheat_debug",0,
   "Debug tools:",
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
      ("camp_cheat_update_notes",[],"{!}Update political notes.",
       [
         (try_for_range, ":hero", active_npcs_begin, active_npcs_end),
           (troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_hero),
           (call_script, "script_update_troop_political_notes", ":hero"),
         (try_end),

         (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
           (call_script, "script_update_faction_political_notes", ":kingdom"),
         (try_end),
        ]
       ),

      ("camp_cheat_update_troop_notes",[],"{!}Update troop notes.",
       [
         (try_for_range, ":hero", active_npcs_begin, active_npcs_end),
           (troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_hero),
           (call_script, "script_update_troop_notes", ":hero"),
         (try_end),

         (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
           (call_script, "script_update_troop_notes", ":lady"),
           (call_script, "script_update_troop_political_notes", ":lady"),
           (call_script, "script_update_troop_location_notes", ":lady", 0),
         (try_end),
        ]
       ),

      ("cheat_faction_orders",[(ge,"$cheat_mode",1)],
	  "{!}Set Debug messages to All.",
       [(assign,"$cheat_mode",1),
         (jump_to_menu, "mnu_camp_cheat"),
        ]
       ),
      ("cheat_faction_orders_econ",[
	  (ge, "$cheat_mode", 1),
	  (neq,"$cheat_mode",3)],"{!}Set Debug messages to Econ Only.",
       [(assign,"$cheat_mode",3),
         (jump_to_menu, "mnu_camp_cheat"),
        ]
       ),
      ("cheat_faction_orders_political",[
	  (ge, "$cheat_mode", 1),
	  (neq,"$cheat_mode",4)],"{!}Set Debug messages to Political Only.",
       [(assign,"$cheat_mode",4),
         (jump_to_menu, "mnu_camp_cheat"),
        ]
       ),

      ("camp_cheat_debug_back",[],"Back to cheat menu.",
       [(jump_to_menu, "mnu_camp_cheat"),]
       ),
      ]
  )
]
