# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

display_party_slots_menu = [
( #helper menu to show all slots
    "display_party_slots", menu_text_color(0xFF990000),
    "{s1}",
    "none",
    [
    (set_background_mesh, "mesh_pic_messenger"),
    (str_store_party_name, s1, "$g_encountered_party"),
    (assign, reg1, "$g_encountered_party"),
    (assign, "$pout_party", 0),
    (try_for_parties, ":party_no"),
      # (assign, "$pout_party", ":party_no"),
      (party_is_active, ":party_no"),
      (gt, ":party_no", "$pout_party"),
      (assign, "$pout_party", ":party_no"),
    (try_end),
    (assign, reg2, "$pout_party"),
    (str_store_string, s1, "@{reg1}/{reg2}: {s1}"),
    #There's probably too many slots (and conflicting ones) to actually output the slot names to string
    (try_for_range, reg1, 0, 1000), #slot_town_trade_good_productions_begin
      (party_get_slot, reg0, "$g_encountered_party", reg1),
      (neq, reg0, 0), #if there's a value in here
      (str_store_string, s1, "@{s1}^{reg1}: {reg0}"),
    (try_end),

    # Process the prev and next parties
    # (assign, "$diplomacy_var",  "$g_encountered_party"),
    # (assign, "$diplomacy_var2", "$g_encountered_party"),
    # (try_for_parties, ":party_no"),
      # (party_is_active, ":party_no"),
      # (eq, "$diplomacy_var2", "$g_encountered_party"),
      # (try_begin), #find last party before current one
        # (lt, ":party_no", "$g_encountered_party"),
        # (assign, "$diplomacy_var", ":party_no"),
      # (else_try), #find first party after current one
        # (gt, ":party_no", "$g_encountered_party"),
        # (assign, "$diplomacy_var2", ":party_no"),
      # (try_end),
    # (try_end),
    (store_sub, "$diplomacy_var",  "$g_encountered_party", 1),
    (store_add, "$diplomacy_var2", "$g_encountered_party", 1),
    (try_begin), #find first
      (neg|party_is_active, "$diplomacy_var"),
      (assign, "$diplomacy_var", 0),
      (assign, ":end", "$g_encountered_party"),
      (try_for_range_backwards, ":party_no", 0, ":end"),
        (party_is_active, ":party_no"),
        (lt, ":party_no", "$g_encountered_party"),
        (gt, ":party_no", "$diplomacy_var"),
        (assign, "$diplomacy_var", ":party_no"),
        (assign, ":end", 0),
      (try_end),
    (try_end),
    # (val_max, "$diplomacy_var", "p_main_party"), #lock as first party

    (try_begin), #look for next
      (neg|party_is_active, "$diplomacy_var2"),
      (assign, "$diplomacy_var2", "$pout_party"), #this was previous checked as highest party
      (assign, ":end", "$pout_party"),
      (try_for_range, ":party_no", "$g_encountered_party", ":end"),
        (party_is_active, ":party_no"),
        (gt, ":party_no", "$g_encountered_party"),
        (le, ":party_no", "$diplomacy_var2"),
        (assign, "$diplomacy_var2", ":party_no"),
        (assign, ":end", "$g_encountered_party"),
      (try_end),
    (try_end),

    ],
    [

      ("notes",
      [(is_between, "$g_encountered_party", centers_begin, centers_end),],
      "View Notes.",
      [
        (change_screen_notes, 3, "$g_encountered_party"),
      ]),
      ("previous",
      [
        (ge, "$diplomacy_var", "p_main_party"),
        (lt, "$diplomacy_var", "$g_encountered_party"),
        (party_is_active, "$diplomacy_var"),
        (str_store_party_name, s2, "$diplomacy_var"),
      ],
      "Previous Party ({s2}).",
      [
        # (jump_to_menu, "mnu_party_cheat"),
        (assign, "$g_encountered_party", "$diplomacy_var"),
      ]),

      ("next",
      [
        (le, "$diplomacy_var2", "$pout_party"),
        (gt, "$diplomacy_var2", "$g_encountered_party"),
        (party_is_active, "$diplomacy_var2"),
        (str_store_party_name, s2, "$diplomacy_var2"),
      ],
      "Next Party ({s2}).",
      [
        (assign, "$g_encountered_party", "$diplomacy_var2"),
      ]),


      ("change",
      [],
      "Modify slots.",
      [
        (assign, "$g_presentation_state", 0), #start off at first slot
        (assign, "$g_presentation_input", rename_center),
        (start_presentation, "prsnt_modify_slots"),
      ]),

      ("continue",
      [],
      "Continue.",
      [
        # (jump_to_menu, "mnu_party_cheat"),
        (assign, "$new_encounter", 2),
        (set_encountered_party, "$g_encountered_party"),
        (call_script, "script_game_event_party_encounter", "$g_encountered_party", -1),
        # (change_screen_map),
        # (start_encounter, "$g_encountered_party"),
      ]),
    ]
  )
]
