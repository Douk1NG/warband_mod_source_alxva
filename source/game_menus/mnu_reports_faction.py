# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

reports_faction_menu = [
("reports_faction",mnf_enable_hot_keys,
   "Select a report:",
   "none",
   [],
    [
      ("lord_relations",[],"View list of known lords by relation.",
       [
        (assign, "$g_jrider_pres_called_from_menu", 1),
        (assign, "$g_character_presentation_type", 1),
        (start_presentation, "prsnt_jrider_character_relation_report"),
        ]
       ),
      ("courtship_relations",[],"View courtship relations.",
       [
        (jump_to_menu, "mnu_courtship_relations"),
        ]
       ),
      ("view_affiliated_family_report",[
        (this_or_next|ge,"$cheat_mode",1),
        (is_between, "$g_player_affiliated_troop", kingdoms_begin, kingdoms_end),
        ], "View affiliated family member / spouse report.",
       [
        (jump_to_menu, "mnu_dplmc_affiliated_family_report"),
        ]
       ),
      ("view_faction_relations_report",[],"View faction relations report.",
       [
        (start_presentation, "prsnt_jrider_faction_relations_report"),
        ]
       ),
      ("view_cc_faction_relations_report",[],"View faction/lords relations report.",
       [
        (start_presentation, "prsnt_cc_relations_with_factions"),
       ]
       ),
      ("rtr_reports_faction",[],"Return.",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  )
]
