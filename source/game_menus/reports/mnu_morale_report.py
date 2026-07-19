# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

morale_report_menu = [
("morale_report",0,
   "{s1}",
   "none",
   [
     (call_script, "script_get_player_party_morale_values"),

     (assign, ":target_morale", reg0),
     (assign, reg1, "$g_player_party_morale_modifier_party_size"),
     (try_begin),
       (gt, reg1, 0),
       (str_store_string, s2, "@{!} -"),
     (else_try),
       (str_store_string, s2, "str_space"),
     (try_end),

     (assign, reg2, "$g_player_party_morale_modifier_leadership"),
     (try_begin),
       (gt, reg2, 0),
       (str_store_string, s3, "@{!} +"),
     (else_try),
       (str_store_string, s3, "str_space"),
     (try_end),

     (try_begin),
       (gt, "$g_player_party_morale_modifier_no_food", 0),
       (assign, reg7, "$g_player_party_morale_modifier_no_food"),
       (str_store_string, s5, "@^No food:  -{reg7}"),
     (else_try),
       (str_store_string, s5, "str_space"),
     (try_end),
     (assign, reg3, "$g_player_party_morale_modifier_food"),
     (try_begin),
       (gt, reg3, 0),
       (str_store_string, s4, "@{!} +"),
     (else_try),
       (str_store_string, s4, "str_space"),
     (try_end),

     (try_begin),
       (gt, "$g_player_party_morale_modifier_debt", 0),
       (assign, reg6, "$g_player_party_morale_modifier_debt"),
       (str_store_string, s6, "@^Wage debt:  -{reg6}"),
     (else_try),
       (str_store_string, s6, "str_space"),
     (try_end),

     (party_get_morale, reg5, "p_main_party"),
     (store_sub, reg4, reg5, ":target_morale"),
     (try_begin),
       (gt, reg4, 0),
       (str_store_string, s7, "@{!} +"),
     (else_try),
       (str_store_string, s7, "str_space"),
     (try_end),

     (assign, reg6, 50),

     (str_store_string, s1, "str_current_party_morale_is_reg5_current_party_morale_modifiers_are__base_morale__50_party_size_s2reg1_leadership_s3reg2_food_variety_s4reg3s5s6_recent_events_s7reg4_total__reg5___"),

     (try_for_range, ":kingdom_no", npc_kingdoms_begin, npc_kingdoms_end),
       (faction_get_slot, ":faction_morale", ":kingdom_no",  slot_faction_morale_of_player_troops),
       (val_div, ":faction_morale", 100),
       (neq, ":faction_morale", 0),
       (assign, reg6, ":faction_morale"),
       (str_store_faction_name, s9, ":kingdom_no"),
       (str_store_string, s1, "str_s1extra_morale_for_s9_troops__reg6_"),
     (try_end),
    ],
    [
      ("continue",[],"Continue...",
      [
        (jump_to_menu, "mnu_reports"),
      ]),
    ]
  )
]
