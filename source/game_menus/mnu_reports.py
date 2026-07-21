# ======================================================================
# SHARED DEPENDENCY
# Entity: reports (menu)
# Called by menus in 4 domains: cheats, diplomacy, kingdom_management, reports
# ======================================================================

# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

reports_menu = [
("reports",mnf_scale_picture|mnf_enable_hot_keys,
   "Character Renown: {reg5}^Honor Rating: {reg6}^Party Morale: {reg8}^Party Size Limit: {reg7}^",
   "none",
   [(call_script, "script_game_get_party_companion_limit"),
    (assign, ":party_size_limit", reg0),
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (assign, reg5, ":renown"),
    (assign, reg6, "$player_honor"),
    (assign, reg7, ":party_size_limit"),
    #(call_script, "script_get_player_party_morale_values"),
    #(party_set_morale, "p_main_party", reg0),
    (party_get_morale, reg8, "p_main_party"),

    ##diplomacy begin
    (str_clear, s1),
    (try_begin),
	    (gt, "$g_next_pay_time", 0),
      (str_store_date, s1, "$g_next_pay_time"),
      (str_store_string, s1, "@ Next pay day: {s1}"),
    (try_end),

    (try_begin),
      (is_between, "$g_player_affiliated_troop", lords_begin, kingdom_ladies_end),
      (str_store_troop_name, s5, "$g_player_affiliated_troop"),
      (str_store_string, s1, "@{s1}^^Affiliated to {s5}"),
    (try_end),
    ##diplomacy end
   ],
    [
      ("reports_cheat",[(ge,"$cheat_mode",1)],"{!}Cheat Reports.",
       [(jump_to_menu, "mnu_cheat_reports"),
        ]
       ),



      ###(((reports_character
      ("reports_character",[],"View character/party reports.",
       [(jump_to_menu, "mnu_reports_character"),
        ]
       ),
      ###)))

      ###(((reports_faction
      ("reports_faction",[],"View faction/relations reports.",
       [(jump_to_menu, "mnu_reports_faction"),
        ]
       ),
      ###)))

      ###(((reports_economy
      ("reports_economy",[],"View economic reports.",
       [(jump_to_menu, "mnu_reports_economy"),
        ]
       ),
      ###)))

      ###(((all_items
      ("all_items",[],"View all items.",
        [
          (assign, "$temp", 0),
          (start_presentation, "prsnt_all_items"),
        ]),
      ###)))

      ("resume_travelling",[],"Resume travelling.",
       [(change_screen_return),
        ]
       ),
      ]
  )
]
