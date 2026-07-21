# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

marshall_selection_candidate_ask_menu = [
("marshall_selection_candidate_ask",0,
   "{s15} will soon select a new marshall for {s23}. Some of the lords have suggested your name as a likely candidate.",
   "none",
   [
     (try_begin),
       (eq, "$g_presentation_marshall_selection_ended", 1),
       (change_screen_return),
     (try_end),
     (faction_get_slot, ":king", "$players_kingdom", slot_faction_leader),
     (str_store_troop_name, s15, ":king"),
     (str_store_faction_name, s23, "$players_kingdom"),
     ],
    [
      ("marshall_candidate_accept", [], "Let {s15} learn that you are willing to serve as marshall.",
       [
         (start_presentation, "prsnt_marshall_selection"),
        ]
       ),
      ("marshall_candidate_reject", [], "Tell everyone that you are too busy these days.",
       [
         (try_begin),
           (eq, "$g_presentation_marshall_selection_max_renown_2_troop", "trp_player"),
           (assign, "$g_presentation_marshall_selection_max_renown_2", "$g_presentation_marshall_selection_max_renown_3"),
           (assign, "$g_presentation_marshall_selection_max_renown_2_troop", "$g_presentation_marshall_selection_max_renown_3_troop"),
         (else_try),
           (assign, "$g_presentation_marshall_selection_max_renown_1", "$g_presentation_marshall_selection_max_renown_2"),
           (assign, "$g_presentation_marshall_selection_max_renown_1_troop", "$g_presentation_marshall_selection_max_renown_2_troop"),
           (assign, "$g_presentation_marshall_selection_max_renown_2", "$g_presentation_marshall_selection_max_renown_3"),
           (assign, "$g_presentation_marshall_selection_max_renown_2_troop", "$g_presentation_marshall_selection_max_renown_3_troop"),
         (try_end),
         (start_presentation, "prsnt_marshall_selection"),
        ]
       ),
      ]
  )
]
