# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

camp_cheat_adv_menu = [
("camp_cheat_adv",0,       # New menu for less used cheats, because old one ran out of space.
   "Select advanced cheat:", # Fancy name so they feel classy and elite, when in reality they're just never used.
   "none",
   [],
    [

      ("camp_cheat_weather",[], "Change weather..",
       [(jump_to_menu, "mnu_cheat_change_weather"),]
       ),

      ("camp_cheat_3",[],"{!}Update political notes.",
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

      ("camp_cheat_4",[],"{!}Update troop notes.",
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
	  "{!}Cheat: Set Debug messages to All.",
       [(assign,"$cheat_mode",1),
         (jump_to_menu, "mnu_camp_cheat_adv"),
        ]
       ),
      ("cheat_faction_orders",[
	  (ge, "$cheat_mode", 1),
	  (neq,"$cheat_mode",3)],"{!}Cheat: Set Debug messages to Econ Only.",
       [(assign,"$cheat_mode",3),
         (jump_to_menu, "mnu_camp_cheat_adv"),
        ]
       ),
      ("cheat_faction_orders",[
	  (ge, "$cheat_mode", 1),
	  (neq,"$cheat_mode",4)],"{!}Cheat: Set Debug messages to Political Only.",
       [(assign,"$cheat_mode",4),
         (jump_to_menu, "mnu_camp_cheat_adv"),
        ]
       ),

      ("to_simple_cheats",[],"{!}Simple Cheats",
		[
         (jump_to_menu, "mnu_camp_cheat"),
		]
       ),
      ("back_to_camp_menu",[],"{!}Back to camp menu.",
       [
         (jump_to_menu, "mnu_camp"),
        ]
       ),
    ]
  )
]
