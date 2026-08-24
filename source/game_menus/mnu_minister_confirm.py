# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

minister_confirm_menu = [
(
    "minister_confirm",0,
    "{s9}can be found at your court in {s12}. You should consult {reg4?her:him} periodically, to avoid the accumulation of unresolved issues that may sap your authority...",
    "none",
    [
    (try_begin),
        (store_and, ":name_set", "$players_kingdom_name_set", rename_kingdom),
        (eq, ":name_set", rename_kingdom),
        (try_begin),
            (eq, "$cstm_open_troop_tree_view", 1),
            (assign, "$cstm_open_troop_tree_view", 0),
            (assign, "$cstm_selected_troop", -1),
            (start_presentation, "prsnt_cstm_choose_troop_tree"),
        (else_try),
            (change_screen_return),
        (try_end),
    (try_end),

	(try_begin),
		(eq, "$g_player_minister", "trp_temporary_minister"),
		(str_store_string, s9, "str_your_new_minister_"),
	(else_try),
		(str_store_troop_name, s10, "$g_player_minister"),
		(str_store_string, s9, "str_s10_is_your_new_minister_and_"),
	(try_end),

	(try_begin),
		(main_party_has_troop, "$g_player_minister"),
		(remove_member_from_party, "$g_player_minister", "p_main_party"),
	(try_end),

    #SB : tableau notes
    (set_fixed_point_multiplier, 100),
    (position_set_x, pos0, 70),
    (position_set_y, pos0, 5),
    (position_set_z, pos0, 75),
    (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", "$g_player_minister", pos0),
    #also gender string
    (call_script, "script_dplmc_store_troop_is_female_reg", "$g_player_minister", 4),
	],
    [
      ("continue",[],"Continue...",
       [
         #SB : explicitly state kingdom
         (assign, "$g_presentation_state", rename_kingdom),
         (start_presentation, "prsnt_name_kingdom"),
        ]),
     ]
  )
]
