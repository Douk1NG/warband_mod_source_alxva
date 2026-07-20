# ======================================================================
# SHARED DEPENDENCY
# Entity: cf_enter_center_location_bandit_check (script)
# Called by menus in 4 domains: cheats, diplomacy, town, village
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

cf_enter_center_location_bandit_check_scripts = [
# script_cf_enter_center_location_bandit_check
# Input: none
# Output: none
("cf_enter_center_location_bandit_check",
    [
      (neq, "$town_nighttime", 0),
      (party_slot_ge, "$current_town", slot_center_has_bandits, 1),
      (eq, "$g_defending_against_siege", 0),#Skip if the center is under siege (because of resting)
      (eq, "$sneaked_into_town", disguise_none),#Skip if sneaked
      (try_begin),
        (party_slot_eq, "$current_town", slot_party_type, spt_village),
        (party_get_slot, ":cur_scene", "$current_town", slot_castle_exterior),
      (else_try),
        (party_get_slot, ":cur_scene", "$current_town", slot_town_center),
      (try_end),
      (modify_visitors_at_site, ":cur_scene"),
      (reset_visitors),
      (party_get_slot, ":bandit_troop", "$current_town", slot_center_has_bandits),
      (store_character_level, ":level", "trp_player"),

      (set_jump_mission, "mt_bandits_at_night"),
      (try_begin),
        (party_slot_eq, "$current_town", slot_party_type, spt_village),
        (assign, ":spawn_amount", 2),
        (store_div, ":level_fac",  ":level", 10),
        (val_add, ":spawn_amount", ":level_fac"),
        (try_for_range, ":unused", 0, 3),
          (gt, ":level", 10),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":level"),
          (val_add, ":spawn_amount", 1),
        (try_end),
        (set_visitors, 4, ":bandit_troop", ":spawn_amount"),
        (assign, "$num_center_bandits", ":spawn_amount"),
        (set_jump_entry, 2),
      (else_try),
        (assign, ":spawn_amount", 1),
        (assign, "$num_center_bandits", 0),
        (try_begin),
          (gt, ":level", 15),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":level"),
          (assign, ":spawn_amount", 2),
        (try_end),
        (val_add, "$num_center_bandits",  ":spawn_amount"),
        (set_visitors, 11, ":bandit_troop", ":spawn_amount"),
        (assign, ":spawn_amount", 1),
        (try_begin),
          (gt, ":level", 20),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":level"),
          (assign, ":spawn_amount", 2),
        (try_end),
        (set_visitors, 27, ":bandit_troop", ":spawn_amount"),
        (val_add, "$num_center_bandits",  ":spawn_amount"),
        (try_begin),
          (gt, ":level", 9),
          (assign, ":spawn_amount", 1),
          (try_begin),
            (gt, ":level", 25),
            (store_random_in_range, ":random_no", 0, 100),
            (lt, ":random_no", ":level"),
            (assign, ":spawn_amount", 2),
          (try_end),
          (set_visitors, 28, ":bandit_troop", ":spawn_amount"),
          (val_add, "$num_center_bandits",  ":spawn_amount"),
        (try_end),
        (assign, "$town_entered", 1),
        (assign, "$all_doors_locked", 1),
      (try_end),

      (display_message, "@You have run into a trap!", message_negative),
      #SB : store actual bandit names
      (str_store_troop_name_plural, s1, ":bandit_troop"),
      (display_message, "@You are attacked by a group of {s1}!", message_negative),
      (play_sound, "snd_encounter_looters"), #more generic than bandit sounds
      (jump_to_scene, ":cur_scene"),
      (change_screen_mission),
      ])
]
