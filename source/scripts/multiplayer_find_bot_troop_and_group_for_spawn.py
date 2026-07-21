# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

multiplayer_find_bot_troop_and_group_for_spawn_scripts = [
# script_multiplayer_find_bot_troop_and_group_for_spawn
# Input: arg1 = team_no
# Output: reg0 = troop_id, reg1 = group_id
("multiplayer_find_bot_troop_and_group_for_spawn",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":look_only_actives", 2),

      (call_script, "script_multiplayer_find_player_leader_for_bot", ":team_no", ":look_only_actives"),
      (assign, ":leader_player", reg0),

      (assign, ":available_troops_in_faction", 0),
      (assign, ":available_troops_to_spawn", 0),
      (team_get_faction, ":team_faction_no", ":team_no"),

      (try_for_range, ":troop_no", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
        (store_troop_faction, ":troop_faction", ":troop_no"),
        (eq, ":troop_faction", ":team_faction_no"),
        (store_add, ":wanted_slot", slot_player_bot_type_1_wanted, ":available_troops_in_faction"),
        (val_add, ":available_troops_in_faction", 1),
        (try_begin),
          (this_or_next|lt, ":leader_player", 0),
          (player_slot_ge, ":leader_player", ":wanted_slot", 1),
          (val_add, ":available_troops_to_spawn", 1),
        (try_end),
      (try_end),

      (assign, ":available_troops_in_faction", 0),

      (store_random_in_range, ":random_troop_index", 0, ":available_troops_to_spawn"),
      (assign, ":end_cond", multiplayer_ai_troops_end),
      (try_for_range, ":troop_no", multiplayer_ai_troops_begin, ":end_cond"),
        (store_troop_faction, ":troop_faction", ":troop_no"),
        (eq, ":troop_faction", ":team_faction_no"),
        (store_add, ":wanted_slot", slot_player_bot_type_1_wanted, ":available_troops_in_faction"),
        (val_add, ":available_troops_in_faction", 1),
        (this_or_next|lt, ":leader_player", 0),
        (player_slot_ge, ":leader_player", ":wanted_slot", 1),
        (val_sub, ":random_troop_index", 1),
        (lt, ":random_troop_index", 0),
        (assign, ":end_cond", 0),
        (assign, ":selected_troop", ":troop_no"),
      (try_end),
      (assign, reg0, ":selected_troop"),
      (assign, reg1, ":leader_player"),
      ])
]
