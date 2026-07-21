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

multiplayer_find_player_leader_for_bot_scripts = [
# script_multiplayer_find_player_leader_for_bot
# Input: arg1 = team_no
# Output: reg0 = player_no
("multiplayer_find_player_leader_for_bot",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":look_only_actives", 2),

      (team_get_faction, ":team_faction", ":team_no"),
      (assign, ":num_ai_troops", 0),
      (try_for_range, ":cur_ai_troop", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
        (store_troop_faction, ":ai_troop_faction", ":cur_ai_troop"),
        (eq, ":ai_troop_faction", ":team_faction"),
        (val_add, ":num_ai_troops", 1),
      (try_end),

      (call_script, "script_multiplayer_count_players_bots"),

      (assign, ":team_player_count", 0),

      (get_max_players, ":num_players"),
      (try_for_range, ":cur_player", 0, ":num_players"),
        (assign, ":continue", 0),
        (player_is_active, ":cur_player"),
        (try_begin),
          (eq, ":look_only_actives", 0),
          (assign, ":continue", 1),
        (else_try),
          (neq, ":look_only_actives", 0),
          (player_get_agent_id, ":cur_agent", ":cur_player"),
          (ge, ":cur_agent", 0),
          (agent_is_alive, ":cur_agent"),
          (assign, ":continue", 1),
        (try_end),

        (eq, ":continue", 1),

        (player_get_team_no, ":player_team", ":cur_player"),
        (eq, ":team_no", ":player_team"),
        (val_add, ":team_player_count", 1),
      (try_end),
      (assign, ":result_leader", -1),
      (try_begin),
        (gt, ":team_player_count", 0),
        (assign, ":total_bot_count", "$g_multiplayer_num_bots_team_1"),
        (try_begin),
          (eq, ":team_no", 1),
          (assign, ":total_bot_count", "$g_multiplayer_num_bots_team_2"),
        (try_end),
        (store_div, ":num_bots_for_each_player", ":total_bot_count", ":team_player_count"),
        (store_mul, ":check_remainder", ":num_bots_for_each_player", ":team_player_count"),
        (try_begin),
          (lt, ":check_remainder", ":total_bot_count"),
          (val_add, ":num_bots_for_each_player", 1),
        (try_end),

        (assign, ":total_bot_req", 0),
        (try_for_range, ":cur_player", 0, ":num_players"),
          (player_is_active, ":cur_player"),

          (player_get_agent_id, ":cur_agent", ":cur_player"),
          (ge, ":cur_agent", 0),
          (agent_is_alive, ":cur_agent"),

          (player_get_team_no, ":player_team", ":cur_player"),
          (eq, ":team_no", ":player_team"),
          (assign, ":ai_wanted", 0),
          (store_add, ":end_cond", slot_player_bot_type_1_wanted, ":num_ai_troops"),
          (try_for_range, ":bot_type_wanted_slot", slot_player_bot_type_1_wanted, ":end_cond"),
            (player_slot_ge, ":cur_player", ":bot_type_wanted_slot", 1),
            (assign, ":ai_wanted", 1),
            (assign, ":end_cond", 0), #break
          (try_end),
          (eq, ":ai_wanted", 1),
          (player_get_slot, ":player_bot_count", ":cur_player", slot_player_last_bot_count),
          (lt, ":player_bot_count", ":num_bots_for_each_player"),
          (val_add, ":total_bot_req", ":num_bots_for_each_player"),
          (val_sub, ":total_bot_req", ":player_bot_count"),
        (try_end),
        (gt, ":total_bot_req", 0),

        (store_random_in_range, ":random_bot", 0, ":total_bot_req"),
        (try_for_range, ":cur_player", 0, ":num_players"),
          (player_is_active, ":cur_player"),

          (player_get_agent_id, ":cur_agent", ":cur_player"),
          (ge, ":cur_agent", 0),
          (agent_is_alive, ":cur_agent"),

          (player_get_team_no, ":player_team", ":cur_player"),
          (eq, ":team_no", ":player_team"),
          (assign, ":ai_wanted", 0),
          (store_add, ":end_cond", slot_player_bot_type_1_wanted, ":num_ai_troops"),
          (try_for_range, ":bot_type_wanted_slot", slot_player_bot_type_1_wanted, ":end_cond"),
            (player_slot_ge, ":cur_player", ":bot_type_wanted_slot", 1),
            (assign, ":ai_wanted", 1),
            (assign, ":end_cond", 0), #break
          (try_end),
          (eq, ":ai_wanted", 1),
          (player_get_slot, ":player_bot_count", ":cur_player", slot_player_last_bot_count),
          (lt, ":player_bot_count", ":num_bots_for_each_player"),
          (val_sub, ":random_bot", ":num_bots_for_each_player"),
          (val_add, ":random_bot", ":player_bot_count"),
          (lt, ":random_bot", 0),
          (assign, ":result_leader", ":cur_player"),
          (assign, ":num_players", 0), #break
        (try_end),
      (try_end),
      (assign, reg0, ":result_leader"),
      ])
]
