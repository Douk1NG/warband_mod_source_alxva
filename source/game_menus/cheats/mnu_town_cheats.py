# ======================================================================
# SHARED DEPENDENCY
# Entity: town_cheats (menu)
# Called by menus in 4 domains: castle, cheats, town, village
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

town_cheats_menu = [
(
    "town_cheats",0,
    "Select an option to interact with troops here",
    "none",[(call_script, "script_set_town_picture"),],
    [
      ("page",
      [],
      "Next Page.",
      [
        (jump_to_menu, "mnu_town_cheats_2"),
      ]),

      ("debug",
      [],
      "Party Cheats.",
      [
        (jump_to_menu, "mnu_party_cheat"),
      ]),
      ("host_tournament",
      [(party_slot_eq, "$current_town", slot_party_type, spt_town),],
      "Host a tournament",
      [
           (call_script, "script_fill_tournament_participants_troop", "$current_town", 1),
           (assign, "$g_tournament_cur_tier", 0),
           (assign, "$g_tournament_player_team_won", -1),
           (assign, "$g_tournament_bet_placed", 0),
           (assign, "$g_tournament_bet_win_amount", 0),
           (assign, "$g_tournament_last_bet_tier", -1),
           (assign, "$g_tournament_next_num_teams", 0),
           (assign, "$g_tournament_next_team_size", 0),
           (jump_to_menu, "mnu_town_tournament"),
      ]),

      ("camp_cheat_gather",[(party_slot_eq, "$current_town", slot_party_type, spt_town),],"Gather all inactive NPCs.",
       [ (assign, "$npc_to_rejoin_party", -1),
         (try_for_range, ":troop_no", companions_begin, companions_end),
           (neg|main_party_has_troop, ":troop_no"),
           (troop_slot_eq, ":troop_no", slot_troop_days_on_mission, 0),
           (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),
            # (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
           (troop_set_slot, ":troop_no", slot_troop_cur_center, "$current_town"),
           (troop_set_slot, ":troop_no", slot_troop_turned_down_twice, 0),
         (try_end),
         # (jump_to_menu, "mnu_camp_cheat"),
        ]
        ),

      # ("camp_cheat_gather",[(party_slot_eq, "$current_town", slot_party_type, spt_town),],"Gather all NPCs not in main party (cancel missions).",
       # [ (assign, "$npc_to_rejoin_party", -1),
         # (try_for_range, ":troop_no", companions_begin, companions_end),
            # (neg|main_party_has_troop, ":troop_no"),
            # (call_script, "script_remove_troop_from_prison", ":troop_no"),
            # (try_for_range, ":slots", slot_troop_days_on_mission, slot_troop_recruit_price),
              # (troop_set_slot, ":troop_no", ":slots", 0),
            # (try_end),
            # (troop_set_slot, ":troop_no", slot_troop_cur_center, "$current_town"),
         # (try_end),
        # ]
        # ),

      ("summon_drunk",
      [(party_slot_eq, "$current_town", slot_party_type, spt_town),
       # (troop_get_slot, ":town", "trp_belligerent_drunk", slot_troop_cur_center),
       (try_begin),
         # (is_between, ":town", towns_begin, towns_end),
         (troop_slot_eq, "trp_belligerent_drunk", slot_troop_cur_center, "$current_town"),
         (assign, reg10, 1),
       (else_try),
         (assign, reg10, 0),
       (try_end),
       ],
      "{reg10?Dismiss:Get} a drunkard.",
      [
        (try_begin),
          (eq, reg10, 1),
          (troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, -1),
        (else_try),
          (troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, "$current_town"),
        (try_end),
      ]),


      ("summon_ass",
      [(party_slot_eq, "$current_town", slot_party_type, spt_town),
       (try_begin),
         # (is_between, ":town", towns_begin, towns_end),
         (troop_slot_eq, "trp_hired_assassin", slot_troop_cur_center, "$current_town"),
         (assign, reg11, 1),
       (else_try),
         (assign, reg11, 0),
       (try_end),
      ],
      "{reg11?Scare away:Hire} an assassin.",
      [
        (try_begin),
          (eq, reg11, 1),
          (troop_set_slot, "trp_hired_assassin", slot_troop_cur_center, -1),
        (else_try),
          (troop_set_slot, "trp_hired_assassin", slot_troop_cur_center, "$current_town"),
        (try_end),
      ]),

      ("summon_bandit",
      [
       (neg|party_slot_eq, "$current_town", slot_party_type, spt_castle),
       (party_get_slot, reg12, "$current_town", slot_center_has_bandits),
       # (try_begin),
         # (party_slot_ge, "$current_town", slot_center_has_bandits, 1),
         # (assign, reg12, 1),
       # (else_try),
         # (assign, reg12, 0),
       # (try_end).
       (try_begin), #none present
         (eq, reg12, 0),
         (str_store_string, s12, "str_bandits"),
       (else_try),
         (str_store_troop_name_plural, s12, reg12),
       (try_end),
      ],
      "{reg12?Kick out:Get ambushed by} some {s12}.",
      [
       (try_begin), #cleanse
         (party_slot_ge, "$current_town", slot_center_has_bandits, 1),
         (party_set_slot, "$current_town", slot_center_has_bandits, 0),
       (else_try), #ambush
         (store_random_in_range, ":bandit", bandits_begin, bandits_end),
         (party_set_slot, "$current_town", slot_center_has_bandits, ":bandit"),
         (assign, "$town_nighttime", 1),
         (assign, "$sneaked_into_town", 0),
         (assign, "$g_defending_against_siege", 0),
         (call_script, "script_cf_enter_center_location_bandit_check"),
         # (assign, "$town_nighttime", 1),
       (try_end),
      ]),

      ("summon_village_bandit",
      [
       (party_slot_eq, "$current_town", slot_party_type, spt_village),
       (party_get_slot, reg13, "$current_town", slot_village_infested_by_bandits),
       (try_begin),
         (le, reg13, 0),
         (str_store_troop_name_plural, s13, "trp_bandit"),
       (else_try),
         (str_store_troop_name_plural, s13, reg13),
       (try_end),
      ],
      "{reg13?Cleanse:Infest} the village {reg13?of:with} {s13}.",
      [
        (try_begin), #cleanse
          (party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
          (party_set_slot, "$current_town", slot_village_infested_by_bandits, 0),
        (else_try), #infest
          (call_script, "script_center_get_bandits", "$current_town", 0),
          (party_set_slot, "$current_town", slot_village_infested_by_bandits, reg0),
          (jump_to_menu, "mnu_village"),
        (try_end),
      ]),

      ("summon_insurgent",
      [ (party_slot_eq, "$current_town", slot_village_infested_by_bandits, 0),
      ],
      "Spearhead a peasant revolution.",
      [
        (party_set_slot, "$current_town", slot_village_infested_by_bandits, "trp_peasant_woman"),

        #add additional troops
        (store_character_level, ":player_level", "trp_player"),
        (store_div, ":player_leveld2", ":player_level", 2),
        (store_mul, ":player_levelx2", ":player_level", 2),
        (try_begin),
          (is_between, "$current_town", villages_begin, villages_end),
          (store_random_in_range, ":random",0, ":player_level"),
          (party_add_members, "$current_town", "trp_mercenary_swordsman", ":random"),
          (store_random_in_range, ":random", 0, ":player_leveld2"),
          (party_add_members, "$current_town", "trp_hired_blade", ":random"),
        (else_try),
          (party_set_banner_icon, "$current_town", 0),
          (party_get_num_companion_stacks, ":num_stacks","$current_town"),
          (try_for_range, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_size, ":stack_size","$current_town",":i_stack"),
            (val_div, ":stack_size", 2),
            (party_stack_get_troop_id, ":troop_id", "$current_town", ":i_stack"),
            (party_remove_members, "$current_town", ":troop_id", ":stack_size"),
          (try_end),
          (store_random_in_range, ":random",":player_leveld2", ":player_levelx2"),
          (party_add_members, "$current_town", "trp_townsman", ":random"),
          (store_random_in_range, ":random",0, ":player_level"),
          (party_add_members, "$current_town", "trp_watchman", ":random"),
        (try_end),
      ]),

      ("center_refresh",
      [(party_slot_eq, "$current_town", slot_party_type, spt_town),],
      "Refresh merchants (global).",
      [
        # (party_get_slot, g.selected_troop,"$current_town", slot_town_weaponsmith),
        (call_script, "script_refresh_center_weaponsmiths"),
        # (party_get_slot, g.selected_troop,"$current_town", slot_town_armorer),
        (call_script, "script_refresh_center_armories"),
        # (party_get_slot, g.selected_troop,"$current_town", slot_town_horse_merchant),
        (call_script, "script_refresh_center_stables"),
        # (party_get_slot, g.selected_troop,"$current_town", slot_town_merchant),
        (call_script, "script_refresh_center_inventories"),
        # (assign, g.selected_troop, -1),
      ]),

      ("village_refresh",
      [(party_slot_eq, "$current_town", slot_party_type, spt_village),],
      "Refresh village goods.",
      [
        (call_script, "script_refresh_village_merchant_inventory", "$current_town"),
      ]),

      ("village_recruits",
      [(party_slot_eq, "$current_town", slot_party_type, spt_village),],
      "Refresh recruits.",
      [
        (call_script, "script_update_volunteer_troops_in_village", "$current_town"),
      ]),
      ("center_recruits",
      [(party_slot_eq, "$current_town", slot_party_type, spt_town),],
      "Refresh mercenaries.",
      [
        (store_random_in_range, ":troop_no", mercenary_troops_begin, mercenary_troops_end),
        (party_set_slot, "$current_town", slot_center_mercenary_troop_type, ":troop_no"),
        (store_random_in_range, ":amount", 3, 8),
        (try_begin),
          (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
          (store_character_level, ":level", "trp_player"), #increase limits a little bit as the game progresses.
          (store_add, ":level_factor", 80, ":level"),
          (val_mul, ":amount", ":level_factor"),
          (val_div, ":amount", 80),
        (try_end),
        (party_set_slot, "$current_town", slot_center_mercenary_troop_amount, ":amount"),
      ]),

      ("go_back",
      [(neg|party_slot_eq,"$current_town",slot_party_type, spt_village),],
      "Go Back.",
      [
        (jump_to_menu,"mnu_town"),
      ]),

      ("continue",
      [(party_slot_eq,"$current_town",slot_party_type, spt_village),],
      "Continue.",
      [
        (jump_to_menu,"mnu_village"),
      ]),
    ])
]
