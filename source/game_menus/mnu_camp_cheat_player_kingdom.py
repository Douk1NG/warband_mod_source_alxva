# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

camp_cheat_player_kingdom_menu = [
("camp_cheat_player_kingdom",0,
   "Player & Kingdom cheats:",
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
      ("camp_cheat_7",[(troop_slot_ge, "trp_player", slot_troop_spouse, 1),],"{!}Divorce player spouse",
       [
  	 (troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
		 (troop_set_slot, ":spouse", slot_troop_spouse, -1),
 	     (troop_set_slot, "trp_player", slot_troop_spouse, -1),

		 (call_script, "script_change_player_relation_with_troop", ":spouse", -40),
		(try_for_range, ":family_member", heroes_begin, heroes_end),
		    (neq, ":family_member", ":spouse"),
			(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":spouse", ":family_member"),
			(gt, reg0, 0),
			(val_mul, reg0, -2),
			(val_div, reg0, 3),
			(val_min, reg0, -1),
			(call_script, "script_change_player_relation_with_troop", ":family_member", reg0),
		(try_end),
        ]
       ),

      ("action_modify_banner",[(eq, "$cheat_mode", 1)],"{!} Modify your banner.",
       [
           (assign, "$g_edit_banner_troop", "trp_player"),
           (jump_to_menu, "mnu_choose_banner"),
        ]
       ),

      ("action_change_policies",
       [
           (gt, "$cheat_mode", 0),
           (store_and, ":name_set", "$players_kingdom_name_set", rename_kingdom),
           (eq, ":name_set", rename_kingdom),
           (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
           (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
       ],"{!} Change kingdom policies",
       [(start_presentation, "prsnt_dplmc_policy_management"),
       ]
       ),

      ("camp_cheat_player_back",[],"Back to cheat menu.",
       [(jump_to_menu, "mnu_camp_cheat"),]
       ),
      ]
  )
]
