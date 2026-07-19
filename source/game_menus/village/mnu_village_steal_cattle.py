# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

village_steal_cattle_menu = [
(
    "village_steal_cattle",mnf_disable_all_keys,
    "{s1}",
    "none",
    [
      (call_script, "script_calculate_amount_of_cattle_can_be_stolen", "$current_town"),
      (assign, ":max_value", reg0),
      (val_add, ":max_value", 1),
      (store_random_in_range, ":random_value", 0, ":max_value"),
      (party_set_slot, "$current_town", slot_village_player_can_not_steal_cattle, 1),
      (party_get_slot, ":lord", "$current_town", slot_town_lord),
      (try_begin),
        (le, ":random_value", 0),
        (call_script, "script_change_player_relation_with_center", "$current_town", -3),
        (str_store_string, s1, "@You fail to steal any cattle."),
      (else_try),
        (assign, reg17, ":random_value"),
        (store_sub, reg12, ":random_value", 1),
        (try_begin),
          (gt, ":lord", 0),
          (call_script, "script_change_player_relation_with_troop", ":lord", -3),
          (call_script, "script_add_log_entry", logent_player_stole_cattles_from_village, "trp_player",  "$current_town", ":lord", "$g_encountered_party_faction"),
        (try_end),
        (call_script, "script_change_player_relation_with_center", "$current_town", -5),
        (str_store_string, s1, "@You drive away {reg17} {reg12?heads:head} of cattle from the village's herd."),

        (try_begin),
          (eq, ":random_value", 3),
          (unlock_achievement, ACHIEVEMENT_GOT_MILK),
        (try_end),

        (call_script, "script_create_cattle_herd", "$current_town", ":random_value"),
        (party_get_slot, ":num_cattle", "$current_town", slot_village_number_of_cattle),
        (val_sub, ":num_cattle", ":random_value"),
        (party_set_slot, "$current_town", slot_village_number_of_cattle, ":num_cattle"),

        #SB : add lesser renown bonus
        (try_begin),
          (call_script, "script_get_max_skill_of_player_party", "skl_looting"),
          (neq, reg1, "trp_player"),
          (call_script, "script_change_troop_renown", reg1, dplmc_companion_skill_renown / 2),
        (try_end),
      (try_end),
    ],
    [
      ("continue",[],"Continue...",
       [
         (change_screen_return),
         ]),
    ],
  )
]
