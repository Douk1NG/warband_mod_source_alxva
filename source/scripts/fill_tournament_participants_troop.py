# ======================================================================
# SHARED DEPENDENCY
# Entity: fill_tournament_participants_troop (script)
# Called by menus in 2 domains: cheats, town
# ======================================================================

# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

fill_tournament_participants_troop_scripts = [
# Input: arg1 = center_no, arg2 = player_at_center
# Output: none (fills trp_tournament_participants)
("fill_tournament_participants_troop",
   [
    (store_script_param, ":center_no", 1),
    (store_script_param, ":player_at_center", 2),
    (assign, ":cur_slot", 0),

      (try_begin),
        (eq, ":player_at_center", 1),
        (troop_set_slot, "trp_tournament_participants", 0, "trp_player"), #we add the player
        (val_add, ":cur_slot", 1),
        (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
        (try_begin), #add adventuring spouse
          (troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
          (ge, ":spouse", active_npcs_begin),
          (main_party_has_troop, ":spouse"),
          (neg|troop_is_wounded, ":spouse"),
          (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":spouse"),
          (val_add, ":cur_slot", 1),
        (try_end),
        #SB : add in companions
        (try_for_range, ":companion_candidate", companions_begin, companions_end),

          (assign, ":continue", 0),
          (try_begin), #player pays entrance fee
            (main_party_has_troop, ":companion_candidate"),
            (assign, ":continue", 1),
          (else_try), #same conditions as below
            (troop_slot_eq, ":companion_candidate", slot_troop_cur_center, ":center_no"),
            (troop_slot_ge, ":companion_candidate", slot_troop_renown, 100),
            (assign, ":continue", 1),
          (try_end),

          (try_begin), #disqualify from health/imprisonment
            (this_or_next|troop_is_wounded, ":companion_candidate"),
            (troop_slot_ge, ":companion_candidate", slot_troop_prisoner_of_party, centers_begin),
            (assign, ":continue", 0),
          (try_end),
          (eq, ":continue", 1),

          (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":companion_candidate"),
          # (call_script, "script_join_tournament", ":companion_candidate"),
          (val_add, ":cur_slot", 1),
        (try_end),

       # (try_for_range, ":stack_no", 0, ":num_stacks"),
         # (party_stack_get_troop_id, ":cur_troop", "p_main_party", ":stack_no"),
         # (troop_is_hero, ":cur_troop"),
         # (neq, ":cur_troop", "trp_kidnapped_girl"),
         # (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":cur_troop"),
         # (val_add, ":cur_slot", 1),
       # (try_end),
      (else_try), #noble companions with starting renown > 100 can participate
        (eq, ":player_at_center", 0),
        (try_for_range, ":companion_candidate", companions_begin, companions_end),
          #this is handled by having their parties be in town
          (neg|troop_slot_eq, ":companion_candidate", slot_troop_occupation, slto_kingdom_hero),
          (troop_slot_eq, ":companion_candidate", slot_troop_cur_center, ":center_no"),
          (troop_slot_ge, ":companion_candidate", slot_troop_renown, 100), #rofl, alayen, etc
          (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":companion_candidate"),
          (val_add, ":cur_slot", 1),
        (try_end),

      (try_end),

     #SB : add in pretender who would want renown bonus
    (try_begin),
      (is_between, "$supported_pretender", pretenders_begin, pretenders_end),
      (eq, ":player_at_center", 1),
      (main_party_has_troop, "$supported_pretender"),
      (troop_set_slot, "trp_tournament_participants", ":cur_slot", "$supported_pretender"),
      (val_add, ":cur_slot", 1),
    (try_end),
    (try_for_range, ":pretender", pretenders_begin, pretenders_end),
      # (neq, ":pretender", "$supported_pretender"),
      # (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
      (troop_slot_eq, ":pretender", slot_troop_cur_center, ":center_no"),
      (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":pretender"),
      (val_add, ":cur_slot", 1),
    (try_end),
    (party_collect_attachments_to_party, ":center_no", "p_temp_party"),
    (party_get_num_companion_stacks, ":num_stacks", "p_temp_party"),
    (try_for_range, ":stack_no", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":cur_troop", "p_temp_party", ":stack_no"),
      (troop_is_hero, ":cur_troop"),
      (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":cur_troop"),
      (val_add, ":cur_slot", 1),
    (try_end),

     # (try_begin),
       # (store_random_in_range, ":random_no", 0, 100),
       # (lt, ":random_no", 50),
       # (troop_set_slot, "trp_tournament_participants", ":cur_slot", "trp_xerina"),
       # (val_add, ":cur_slot", 1),
     # (try_end),
     # (try_begin),
       # (store_random_in_range, ":random_no", 0, 100),
       # (lt, ":random_no", 50),
       # (troop_set_slot, "trp_tournament_participants", ":cur_slot", "trp_dranton"),
       # (val_add, ":cur_slot", 1),
     # (try_end),
     # (try_begin),
       # (store_random_in_range, ":random_no", 0, 100),
       # (lt, ":random_no", 50),
       # (troop_set_slot, "trp_tournament_participants", ":cur_slot", "trp_kradus"),
       # (val_add, ":cur_slot", 1),
     # (try_end),
    #SB : recalculate chances
    (store_add, ":heroes_limit", ":cur_slot", 5),
    (val_min, ":heroes_limit", 64),
    (try_for_range, ":hero", tournament_champions_begin, tournament_champions_end),
        # (neg|troop_is_wounded, ":hero"),
        (store_troop_health, ":health", ":hero", 0),
        (gt, ":health", 10),
        (store_random_in_range, ":random_no", 0, 6),
        (troop_set_slot, ":hero", slot_troop_cur_center, -1),
        (troop_set_slot, ":hero", slot_lady_used_tournament, -1),

        (try_begin),
            (lt, ":random_no", 2),
            (lt, ":cur_slot", ":heroes_limit"),
            (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":hero"),
            # (try_begin),
                # (is_between, ":hero", quick_battle_troops_original_begin, quick_battle_troops_tournament_end),
                # (troop_set_slot, ":hero", slot_troop_cur_center, ":center_no"),
            # (try_end),
            (val_add, ":cur_slot", 1),
            #add some health too
            (val_mul, ":random_no", 10),
            (val_add, ":health", ":random_no"),
            (troop_set_health, ":hero", ":health"),
        (try_end),
    (try_end),
    ##SB : random quick-battle heroes (20% each x 11) at full health, capped to 5 per tourney to not saturate
    (try_for_range, ":hero", quick_battle_troops_begin, quick_battle_troops_end),
        (lt, ":cur_slot", ":heroes_limit"),
        (store_random_in_range, ":random_no", 0, 5),
        (try_begin),
            (eq, ":random_no", 0),
            (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":hero"),
            (troop_set_health, ":hero", ":health"),
            (val_add, ":cur_slot", 1),
        (try_end),
    (try_end),
    (assign, ":begin_slot", ":cur_slot"),

    #SB : set up flavour troops (town mercenary, sword sister alternatives)
    (party_get_slot, ":town_merc", ":center_no", slot_center_mercenary_troop_type),
    (party_get_slot, ":merc_amount", ":center_no", slot_center_mercenary_troop_amount),
    (val_mul, ":merc_amount", 2),
    (val_div, ":merc_amount", 3),

    (store_faction_of_party, ":town_faction", ":center_no"),
    #alternatively check if other female heroes are present and allow sword sisters?

    #might need to test for male prejudice against hired blades?
    (try_begin),
      (call_script, "script_cf_dplmc_faction_has_bias_against_gender", ":town_faction", tf_female),
      (assign, ":sword_sister", -1),
    (else_try),
      (assign, ":sword_sister", "trp_sword_sister"),
    (try_end),
    (try_for_range, ":cur_slot", ":begin_slot", 64), #dckplmc - use faction troops unless none applicable
      (store_random_in_range, ":random_no", 0, 6),
      (store_random_in_range, ":random_no2", 0, 3), #1/3 chance of tournament fighters
      (try_begin),
        (eq, ":random_no", 0),
        (try_begin),
          (lt, ":random_no2", 2),
          (faction_get_slot, ":troop_no", ":town_faction", slot_faction_tier_3_troop),
          (gt, ":troop_no", 0),
          (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":troop_no"),
        (else_try),
          (troop_set_slot, "trp_tournament_participants", ":cur_slot", "trp_regular_fighter"),
        (try_end),
      (else_try),
        (eq, ":random_no", 1),
        (try_begin),
          (lt, ":random_no2", 2),
          (faction_get_slot, ":troop_no", ":town_faction", slot_faction_tier_4_troop),
          (gt, ":troop_no", 0),
          (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":troop_no"),
        (else_try),
          (troop_set_slot, "trp_tournament_participants", ":cur_slot", "trp_veteran_fighter"),
        (try_end),
      (else_try),
        (eq, ":random_no", 2),
        (try_begin),
          (lt, ":random_no2", 2),
          (faction_get_slot, ":troop_no", ":town_faction", slot_faction_tier_5_troop),
          (gt, ":troop_no", 0),
          (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":troop_no"),
        (else_try),
          (troop_set_slot, "trp_tournament_participants", ":cur_slot", "trp_champion_fighter"),
        (try_end),
      (else_try),
        (eq, ":random_no", 3),
        (try_begin),
          (eq, ":sword_sister", "trp_sword_sister"),
          (eq, ":random_no2", 2),
          (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":sword_sister"),
        (else_try),
          (lt, ":random_no2", 2),
          (faction_get_slot, ":troop_no", ":town_faction", slot_faction_tier_5_troop),
          (gt, ":troop_no", 0),
          (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":troop_no"),
        (else_try),
          (troop_set_slot, "trp_tournament_participants", ":cur_slot", "trp_mercenary_swordsman"),
        (try_end),
      (else_try),
        (eq, ":random_no", 4),
        (try_begin),
          (lt, ":random_no2", 2),
          (faction_get_slot, ":troop_no", ":town_faction", slot_faction_tier_5_troop),
          (gt, ":troop_no", 0),
          (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":troop_no"),
        (else_try),
          (troop_set_slot, "trp_tournament_participants", ":cur_slot", "trp_hired_blade"),
        (try_end),
        #(troop_set_slot, "trp_tournament_participants", ":cur_slot", "trp_hired_blade"),
      (else_try), #SB : use current town mercenary (if any remaining)
        (eq, ":random_no2", 5),
        (gt, ":merc_amount", 0),
        (val_sub, ":merc_amount", 1),
        (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":town_merc"),
      (else_try), #otherwise fallback to random mercenary participant
        (store_random_in_range, ":merc", mercenary_troops_begin, mercenary_troops_end),
        (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":merc"),
      (try_end),
    (try_end),
  ])
]
