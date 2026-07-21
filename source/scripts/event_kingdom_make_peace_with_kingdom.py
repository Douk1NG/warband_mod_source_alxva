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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

event_kingdom_make_peace_with_kingdom_scripts = [
("event_kingdom_make_peace_with_kingdom",
    [
      (store_script_param_1, ":source_kingdom"),
      (store_script_param_2, ":target_kingdom"),
      (try_begin),
        (check_quest_active, "qst_capture_prisoners"),
        (try_begin),
          (eq, "$players_kingdom", ":source_kingdom"),
          (quest_slot_eq, "qst_capture_prisoners", slot_quest_target_faction, ":target_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_prisoners"),
        (else_try),
          (eq, "$players_kingdom", ":target_kingdom"),
          (quest_slot_eq, "qst_capture_prisoners", slot_quest_target_faction, ":source_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_prisoners"),
        (try_end),
      (try_end),

      (try_begin),
        (check_quest_active, "qst_capture_enemy_hero"),
        (try_begin),
          (eq, "$players_kingdom", ":source_kingdom"),
          (quest_slot_eq, "qst_capture_enemy_hero", slot_quest_target_faction, ":target_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_enemy_hero"),
        (else_try),
          (eq, "$players_kingdom", ":target_kingdom"),
          (quest_slot_eq, "qst_capture_enemy_hero", slot_quest_target_faction, ":source_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_enemy_hero"),
        (try_end),
      (try_end),



      (try_begin),
        (check_quest_active, "qst_persuade_lords_to_make_peace"),
        (quest_get_slot, ":lord_1", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
        (quest_get_slot, ":lord_2", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),

        (try_begin),
            (lt, ":lord_1", 0),
            (val_mul, ":lord_1", -1),
        (try_end),
        (try_begin),
            (lt, ":lord_2", 0),
            (val_mul, ":lord_2", -1),
        (try_end),


        (store_faction_of_troop, ":lord_1_faction", ":lord_1"),
        (store_faction_of_troop, ":lord_2_faction", ":lord_2"),

        (this_or_next|eq, ":lord_1_faction", ":source_kingdom"),
            (eq, ":lord_2_faction", ":source_kingdom"),

        (this_or_next|eq, ":lord_1_faction", ":target_kingdom"),
            (eq, ":lord_2_faction", ":target_kingdom"),

        (call_script, "script_cancel_quest", "qst_persuade_lords_to_make_peace"),

      (try_end),

      #Rescue prisoners cancelled in simple_triggers

      (try_begin),
        #SB : better checking, also adds rtr for co-ruler
        (this_or_next|eq, "$players_kingdom", ":source_kingdom"),
        (eq, "$players_kingdom", ":target_kingdom"),
        (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
        (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
        (call_script, "script_change_player_right_to_rule", 3),
      (try_end),

  ])
]
