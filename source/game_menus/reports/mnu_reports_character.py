# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

reports_character_menu = [
("reports_character",mnf_enable_hot_keys,
   "Select a report:",
   "none",
   [],
    [
      ("view_character_report",[],"View character report.",
       [(jump_to_menu, "mnu_character_report"),
        ]
       ),
      ("view_party_size_report",[],"View party size report.",
       [(jump_to_menu, "mnu_party_size_report"),
        ]
       ),
      ("view_npc_mission_report",[],"View companion mission report.",
       [(jump_to_menu, "mnu_companion_report"),
        (assign, "$g_player_troop", "trp_player"),
        ]
       ),
      ("view_morale_report",[],"View party morale report.",
       [(jump_to_menu, "mnu_morale_report"),
        ]
       ),
      ("rtr_reports_character",[],"Return.",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  )
]
