# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_village_riot_result_menu = [
(
    "dplmc_village_riot_result",mnf_scale_picture,
    "{s9}",
    "none",
    [(try_begin),
       (eq, "$g_battle_result", 1),
       (jump_to_menu, "mnu_dplmc_village_riot_removed"),
     (else_try),
       (set_background_mesh, "mesh_pic_villageriot"),
       (str_store_string, s9, "@Try as you might, you could not defeat the rebelling village."),
     (try_end),
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [(call_script, "script_change_player_relation_with_center", "$g_encountered_party", -3),
        (call_script, "script_change_troop_renown", "trp_player", -5), #SB : renown loss highest here
        (jump_to_menu, "mnu_village"),]),
    ],
  )
]
