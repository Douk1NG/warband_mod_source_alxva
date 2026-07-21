# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

center_improve_menu = [
(
    "center_improve",0,
    "{s19} As the party member with the highest engineer skill ({reg2}), {reg3?you reckon:{s3} reckons} that building the {s4} will cost you\
 {reg5} denars and will take {reg6} days.",
    "none",
    [#SB : town pictures
     (call_script, "script_set_town_picture"),
     (call_script, "script_get_improvement_details", "$g_improvement_type"),
     (assign, ":improvement_cost", reg0),
     (str_store_string, s4, s0),
     (str_store_string, s19, s1),
     (call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),
     (assign, reg2, ":max_skill"),

     (store_sub, ":multiplier", 20, ":max_skill"),
     (val_mul, ":improvement_cost", ":multiplier"),
     (val_div, ":improvement_cost", 20),

     (store_div, ":improvement_time", ":improvement_cost", 100),
     (val_add, ":improvement_time", 3),

     (assign, reg5, ":improvement_cost"),
     (assign, reg6, ":improvement_time"),

     #SB : tableau at bottom
     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s3, ":max_skill_owner"),
     (try_end),

    #SB : assign globals to be safe
    (assign, "$diplomacy_var", ":improvement_cost"),
    (assign, "$diplomacy_var2", ":improvement_time"),
    (assign, "$lord_selected", ":max_skill_owner"),
    (set_fixed_point_multiplier, 100),
    (position_set_x, pos0, 70),
    (position_set_y, pos0, 5),
    (position_set_z, pos0, 75),
    (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":max_skill_owner", pos0),
    ],
    [
      ##diplomacy begin
      ("dplmc_improve_cont",
      [
        (gt, "$g_player_chamberlain", 0),
        (store_troop_gold, ":cur_gold", "trp_household_possessions"),
        (ge, ":cur_gold", "$diplomacy_var"),
      ], "Go on. (Pay from treasury)",
        [
          (call_script, "script_dplmc_withdraw_from_treasury", "$diplomacy_var"),
          # (call_script, "script_get_max_skill_of_player_party", "skl_engineer"), #SB : re-fetch skill
          (call_script, "script_improve_center", "$g_encountered_party", "$lord_selected", "$diplomacy_var2"),
          (jump_to_menu,"mnu_center_manage"),
         ]
      ),
      ("improve_not_enough_gold",[(gt, "$g_player_chamberlain", 0),
                                  (store_troop_gold, ":cur_gold", "trp_household_possessions"),
                                  (lt, ":cur_gold", "$diplomacy_var"),
                                  #SB : disable_menu_option
                                  (disable_menu_option)],
       "Insufficient fund in the treasury.", []),
      ##diplomacy end

      ("improve_cont",[(store_troop_gold, ":cur_gold", "trp_player"),
                       (ge, ":cur_gold", "$diplomacy_var")],
       "Go on.", [
                  (try_begin), #fast build
                    (ge, "$cheat_mode", 1),
                    (assign, "$diplomacy_var2", 0),
                  (else_try),
                    (troop_remove_gold, "trp_player", "$diplomacy_var"),
                  (try_end),
                  (call_script, "script_improve_center", "$g_encountered_party", "$lord_selected", "$diplomacy_var2"),
                  (jump_to_menu,"mnu_center_manage"),
                  ]),
      ("improve_not_enough_gold",[(store_troop_gold, ":cur_gold", "trp_player"),
                                  (lt, ":cur_gold", "$diplomacy_var"),
                                  #SB : disable_menu_option
                                  (disable_menu_option)],
       "I don't have enough money for that.", []),
      ("forget_it",[], "Forget it.", [(jump_to_menu,"mnu_center_manage")]),

    ],
  )
]
