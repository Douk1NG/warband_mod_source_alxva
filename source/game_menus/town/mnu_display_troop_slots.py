# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

display_troop_slots_menu = [
( #helper menu to show all troop slots
    "display_troop_slots", menu_text_color(0xFF009900),
    "{s1}^{s2}",
    "none",
    [
    # (set_background_mesh, "mesh_pic_cattle"),
    (assign, reg1, "$g_talk_troop"),
    (str_store_troop_name, s1, "$g_talk_troop"),
    (str_store_troop_name_plural, s2, "$g_talk_troop"),
    (store_troop_faction, ":faction_no", "$g_talk_troop"),
    (str_store_faction_name, s3, ":faction_no"),
    (troop_get_class, ":class", "$g_talk_troop"),
    (str_store_class_name, s4, ":class"),
    (store_character_level, reg2, "$g_talk_troop"),
    (str_store_string, s1, "@{reg1}: {s1}, {s2} classified as level {reg2} {s3} {s4}"),
    (try_begin), #upgrades
      (neg|troop_is_hero, "$g_talk_troop"),
      (try_begin),
        (troop_get_upgrade_troop, ":upgrade_0", "$g_talk_troop", 0),
        (gt, ":upgrade_0", 0),
        (str_store_troop_name_plural, s2, ":upgrade_0"),
        (str_store_string, s1, "@{s1}^becomes {s2}"),
        (troop_get_upgrade_troop, ":upgrade_1", "$g_talk_troop", 1),
        (gt, ":upgrade_1", 0),
        (str_store_troop_name_plural, s2, ":upgrade_1"),
        (str_store_string, s1, "@{s1} and {s2}"),
      (try_end),

      (call_script, "script_game_get_upgrade_xp", "$g_talk_troop"),
      (assign, reg10, reg0),
      (call_script, "script_game_get_upgrade_cost", "$g_talk_troop"),
      (assign, reg11, reg0),
      (str_store_string, s1, "@{s1}^costs {reg11} to upgrade with {reg10} xp"),

      (call_script, "script_game_get_troop_wage", "$g_talk_troop", -1),
      (assign, reg12, reg0),
      (call_script, "script_game_get_join_cost", "$g_talk_troop"),
      (assign, reg13, reg0),

      #this is because this script ties a global to the price
      (assign, ":troop_no", "$g_talk_troop"),
      (assign, "$g_talk_troop", ransom_brokers_begin),
      (call_script, "script_game_get_prisoner_price", ":troop_no"),
      (assign, reg14, reg0),
      (assign, "$g_talk_troop", ":troop_no"),

      (str_store_string, s1, "@{s1}^wage of {reg12}, buy costs {reg13} sell costs {reg14}"),
    (else_try),
      (troop_is_hero, "$g_talk_troop"),
      (str_store_string, s2, "@hero"),
      (call_script, "script_cf_troop_debug_range", "$g_talk_troop", s2, 0),
      (str_store_string, s1, "@{s1} is a {s2}"),
      (try_begin),
        (store_troop_gold, ":gold", "$g_talk_troop"),
        (gt, ":gold", 0),
        (assign, reg1, ":gold"),
        (str_store_string, s1, "@{s1} with {reg1} gold"),
      (try_end),
      # (try_begin),
        # (store_partner_quest, ":quest_no"),
        # (ge, ":quest_no", 0),
        # (str_store_quest_name, s2, ":quest_no"),
        # (str_store_string, s1, "@{s1} tasking you with {s2}"),
      # (try_end),
    (try_end),

    (str_clear, s2),
    (try_for_range, reg1, 0, 1000),
      (troop_get_slot, reg0, "$g_talk_troop", reg1),
      (neq, reg0, 0), #if there's a value in here
      (str_store_string, s2, "@{s2}^{reg1}: {reg0}"),
    (try_end),

    (set_fixed_point_multiplier, 100),
    (init_position, pos0),
    (try_begin),
      (str_is_empty, s2),
      (position_set_x, pos0, 17),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 100),
    (else_try),
      (position_set_x, pos0, 60),
      (position_set_y, pos0, 20),
      (position_set_z, pos0, 100),
    (try_end),
    (store_mul, ":troop_no", "$g_talk_troop", 2),
    (set_game_menu_tableau_mesh, "tableau_game_party_window", ":troop_no", pos0),
    ],
    [

    #So apparently this one needs to re-jump to the menu
      ("notes",
      [(is_between, "$g_talk_troop", heroes_begin, heroes_end),],
      "View Notes.",
      [
        (change_screen_notes, 1, "$g_talk_troop"),
      ]),

      ("prev_range",
      [
        (gt, "$g_talk_troop", "trp_player"),
        (call_script, "script_cf_troop_debug_range", "$g_talk_troop", s3, -1),
        (str_store_troop_name, s3, reg0),
      ],
      "Head ({s3}).",
      [
        (call_script, "script_cf_troop_debug_range", "$g_talk_troop", s0, -1),
        (assign, "$g_talk_troop", reg0),
        (jump_to_menu, "mnu_display_troop_slots"),
      ]),

      ("next_range",
      [
        (call_script, "script_cf_troop_debug_range", "$g_talk_troop", s3, 1),
        (str_store_troop_name, s3, reg0),
      ],
      "Tail ({s3}).",
      [
        (call_script, "script_cf_troop_debug_range", "$g_talk_troop", s0, 1),
        (assign, "$g_talk_troop", reg0),
        (jump_to_menu, "mnu_display_troop_slots"),
      ]),

      ("prev",
      [
        (gt, "$g_talk_troop", "trp_player"),
        (store_sub, ":troop_no", "$g_talk_troop", 1),
        (str_store_troop_name, s2, ":troop_no"),
      ],
      "Previous Troop ({s2}).",
      [
        (val_sub, "$g_talk_troop", 1),
        (jump_to_menu, "mnu_display_troop_slots"),
      ]),

      ("next",
      [
        (lt, "$g_talk_troop", "trp_dplmc_recruiter"), #last troop apparently
        (store_add, ":troop_no", "$g_talk_troop", 1),
        (str_store_troop_name, s2, ":troop_no"),
      ],
      "Next Troop ({s2}).",
      [
        (val_add, "$g_talk_troop", 1),
        (jump_to_menu, "mnu_display_troop_slots"),
      ]),

      ("rename",
      [],
      "Rename.",
      [
        (assign, "$g_player_troop", "$g_talk_troop"),
        (assign, "$g_presentation_state", rename_companion),
        (start_presentation, "prsnt_name_kingdom"),
      ]),

      ("change",
      [],
      "Modify slots.",
      [
        (assign, "$g_presentation_state", 0), #start off at first slot
        (assign, "$g_presentation_input", rename_companion),
        (start_presentation, "prsnt_modify_slots"),
      ]),

      ("inventory",
      [],
      "Modify inventory.",
      [
        (change_screen_loot, "$g_talk_troop"),
      ]),

      ("continue",
      [],
      "Continue.",
      [
        (change_screen_map),
      ]),
    ]
  )
]
