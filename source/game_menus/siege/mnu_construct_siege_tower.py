# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

construct_siege_tower_menu = [
(
    "construct_siege_tower",0,
    "As the party member with the highest Engineer skill ({reg2}), {reg3?you estimate:{s3} estimates} that building a siege tower will take\
 {reg4} hours.",
    "none",
    [(call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),
     (assign, reg2, ":max_skill"),

     (store_sub, reg4, 15, ":max_skill"),
     (val_mul, reg4, 6),

     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s3, ":max_skill_owner"),
     (try_end),

    #SB : add tableau
    (set_fixed_point_multiplier, 100),
    (position_set_x, pos0, 70),
    (position_set_y, pos0, 5),
    (position_set_z, pos0, 75),
    (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":max_skill_owner", pos0),
    ],
    [
      ("build_siege_tower_cont",[],
       "Start building.", [
           (assign, "$g_siege_method", 2),
           (store_current_hours, ":cur_hours"),
           (call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
           (store_sub, ":hours_takes", 15, reg0),
           (val_mul, ":hours_takes", 6),
           (store_add, "$g_siege_method_finish_hours",":cur_hours", ":hours_takes"),
           (assign,"$auto_besiege_town","$current_town"),
           (rest_for_hours_interactive, 240, 5, 1), #rest while attackable. A trigger will divert control when attack is ready.
           (change_screen_return),
           ]),
      ("go_back",[],
       "Go back.", [(jump_to_menu,"mnu_castle_besiege")]),
        ],
  )
]
