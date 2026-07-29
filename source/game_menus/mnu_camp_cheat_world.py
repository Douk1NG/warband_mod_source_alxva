# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

camp_cheat_world_menu = [
("camp_cheat_world",0,
   "World cheats:",
   "none",
   [
     (try_begin),
       (neq, "$g_player_icon_state", pis_ship),
     (assign, "$g_player_icon_state", pis_normal),
        (party_get_slot, ":player_party", "$marshalship"),
        (ge, ":player_party", 0),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos1, 70),
        (position_set_y, pos1, 5),
        (position_set_z, pos1, 75),
        (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":player_party", pos1),
        (try_end),
    ],
    [
      ("camp_cheat_5",[],"Scramble taverngoers.",
       [
        (try_for_range, ":slots", slot_center_ransom_broker, slot_center_tavern_minstrel + 1),
          (neq, ":slots", slot_center_traveler_info_faction),
          (try_for_range, ":towns", towns_begin, towns_end),
            (party_set_slot, ":towns", ":slots", -1),
          (try_end),

          (try_begin),
            (eq, ":slots", slot_center_ransom_broker),
            (assign, ":start", ransom_brokers_begin),
            (assign, ":end", ransom_brokers_end),
          (else_try),
            (eq, ":slots", slot_center_tavern_traveler),
            (assign, ":start", tavern_travelers_begin),
            (assign, ":end", tavern_travelers_end),
          (else_try),
            (eq, ":slots", slot_center_tavern_minstrel),
            (assign, ":start", tavern_minstrels_begin),
            (assign, ":end", tavern_minstrels_end),
          (else_try),
            (eq, ":slots", slot_center_tavern_bookseller),
            (assign, ":start", tavern_booksellers_begin),
            (assign, ":end", tavern_booksellers_end),
          (try_end),

          (assign, ":num_towns", 0),
          (str_store_string, s51, "@nowhere in particular"),
          (try_for_range, ":troop_no", ":start", ":end"),
            (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
            (store_random_in_range, ":town_no", towns_begin, towns_end),

            (try_begin),
              (party_slot_ge, ":town_no", ":slots", ":start"),
            (else_try),
              (val_add, ":num_towns", 1),
              (str_store_party_name_link, s50, ":town_no"),
              (party_set_slot, ":town_no", ":slots", ":troop_no"),
              (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"),
              (try_begin),
                (eq, ":num_towns", 1),
                (str_store_string, s51, s50),
              (else_try),
                (str_store_string, s51, "str_s50_comma_s51"),
              (try_end),
            (try_end),
          (try_end),
          (str_store_troop_name_plural, s10, ":start"),
          (str_store_string_reg, s11, s51),
          (display_message, "@You can find {s10}s at {s11}."),
        (try_end),
        (call_script, "script_update_mercenary_units_of_towns"),
        ]
       ),

      ("camp_cheat_6",[],"Infinite camp",
       [
         (assign,"$g_camp_mode", 1),
         (assign, "$g_infinite_camping", 1),
         (assign, "$g_player_icon_state", pis_camping),
         (rest_for_hours_interactive, 10 * 24 * 365, 20),
         (change_screen_return),
        ]
       ),

      ("camp_cheat_weather",[],"Change weather...",
       [(jump_to_menu, "mnu_cheat_change_weather"),]
       ),

      ("camp_cheat_force_spawn_bandits",[],"Force trigger daily bandit spawn.",
       [
         (call_script, "script_spawn_bandits"),
         (display_message, "@Bandit spawn script triggered.", 0x00FF0000),
        ]
       ),

      ("camp_cheat_clear_bandits",[],"Clear all roaming bandits.",
       [
         (try_for_range, ":bandit_template", bandit_party_templates_begin, bandit_party_templates_end),
           (party_template_set_slot, ":bandit_template", slot_party_template_respawn_cooldown, 0),
         (try_end),
         (try_for_parties, ":cur_party"),
           (party_get_template_id, ":template", ":cur_party"),
           (assign, ":is_bandit", 0),
           (try_begin),
             (is_between, ":template", bandit_party_templates_begin, bandit_party_templates_end),
             (assign, ":is_bandit", 1),
           (else_try),
             (eq, ":template", "pt_looters"),
             (assign, ":is_bandit", 1),
           (else_try),
             (eq, ":template", "pt_deserters"),
             (assign, ":is_bandit", 1),
           (try_end),
           (eq, ":is_bandit", 1),
           (remove_party, ":cur_party"),
         (try_end),
         (display_message, "@All roaming bandits cleared and cooldowns reset.", 0x00FF0000),
        ]
       ),

      ("camp_cheat_clear_lairs",[],"Clear all bandit lairs.",
       [
         # 1. Clear the slots in the templates so they can respawn
         (try_for_range, ":bandit_template", bandit_party_templates_begin, bandit_party_templates_end),
           (party_template_set_slot, ":bandit_template", slot_party_template_lair_party, 0),
           (party_template_set_slot, ":bandit_template", slot_party_template_lair_next_spawn, 0),
           (party_template_set_slot, ":bandit_template", slot_party_template_respawn_cooldown, 0),
         (try_end),
         # 2. Remove all lair parties on the map
         (try_for_parties, ":cur_party"),
           (party_is_active, ":cur_party"),
           (party_get_template_id, ":template", ":cur_party"),
           (this_or_next|eq, ":template", "pt_looter_lair"),
           (is_between, ":template", "pt_steppe_bandit_lair", "pt_bandit_lair_templates_end"),
           (remove_party, ":cur_party"),
         (try_end),
         (display_message, "@All bandit lairs cleared and slots reset.", 0x00FF0000),
        ]
       ),

      ("remove_ships",[],"Remove all ships.",
       [
         (try_for_parties, ":cur_party"),
           (party_slot_eq, ":cur_party", slot_party_type, spt_ship),
           (disable_party, ":cur_party"),
         (try_end),
         (display_message, "@All ships removed.", 0x00FF0000),
        ]
       ),

      ("camp_cheat_world_back",[],"Back to cheat menu.",
       [(jump_to_menu, "mnu_camp_cheat"),]
       ),
      ]
  )
]
