# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dickplo_town_manage_menu = [
(
     "dickplo_town_manage",0,
     "The business district is full of opportunities to take advantage of.",
     "none",
     [
             (try_begin),
             (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
             (ge, ":center_lord", 0),
             (set_fixed_point_multiplier, 100),
             (position_set_x, pos1, 70),
             (position_set_y, pos1, 5),
             (position_set_z, pos1, 75),
             (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":center_lord", pos1),
             (try_end),

     ],
     [
 	#	Floris Bank Overhaul	//	Original Idea by Lazeras
 	("town_bank",
        [(party_slot_eq, "$current_town", slot_party_type, spt_town)],
        "Visit the landlords and moneylenders.",
        [
 			(assign, reg10, 0),
 			(start_presentation, "prsnt_bank"),
         ]),

#Troop hiring menu
       ("hire_troops",[],
        "Look to hire some mercenaries.",## You have added a new menu.
        [
            (jump_to_menu,"mnu_town_pre_hire_troops"),
         ]),

      ##diplomacy begin
      ("dplmc_guild_master_meeting",
       [
       (party_slot_eq,"$current_town",slot_party_type, spt_town),
	   ],
       "Meet the Guild Master.",
        [
          (try_begin),
            (call_script, "script_cf_enter_center_location_bandit_check"),
          (else_try), #SB : unified script call
            (call_script, "script_start_town_conversation", slot_town_elder, 11),
          (try_end),
     ]),
       ##diplomacy end


       ("back_to_town_menu",[],"Head back.",
        [
            (jump_to_menu,"mnu_town"),
         ]),
     ]
   )
]
