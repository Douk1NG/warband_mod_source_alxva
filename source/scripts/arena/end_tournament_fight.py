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

end_tournament_fight_scripts = [
# script_end_tournament_fight
# Input: arg1 = player_team_won (1 or 0)
# Output: none
("end_tournament_fight",
    [
      (store_script_param, ":player_team_won", 1),
      (call_script, "script_get_num_tournament_participants"),
      (assign, ":num_participants", reg0),
      (store_div, ":needed_to_remove_randomly", ":num_participants", 2),
      #Must remove other participants randomly earlier than adding the winners back to participants
      (call_script, "script_remove_tournament_participants_randomly", ":needed_to_remove_randomly"),

      #SB : because we've added relationship losses, we'll also add this here
      (store_div, ":relation", "$g_tournament_cur_tier", 2),
      (assign, ":num_needed", "$g_tournament_num_participants_for_fight"),
      (val_div, ":num_needed", 2),
      (get_player_agent_no, ":player_agent"),
      (agent_get_team, ":player_team", ":player_agent"),
      (try_for_agents, ":agent_no"),
        (agent_is_human, ":agent_no"),
        (agent_get_troop_id, ":troop_id", ":agent_no"),
        (neg|is_between, ":troop_id", arena_masters_begin, arena_masters_end),#omit tournament master
        (agent_get_team, ":agent_team", ":agent_no"),
        (assign, ":cur_point", 0),
        (try_begin),
          (eq, ":player_team_won", 1),
          (eq, ":agent_team", ":player_team"),
          (val_add, ":cur_point", 5000000),#Make sure that team members are chosen
          #SB : apply relationship bonus here
          (agent_is_alive, ":agent_no"),
          (troop_is_hero, ":troop_id"),
          (try_begin), #player's companions, change their morale penalty
            (troop_slot_eq, ":troop_id", slot_troop_occupation, slto_player_companion),
            (troop_get_slot, ":grievance", ":troop_id", slot_troop_personalityclash_penalties),
            (val_sub, ":grievance", "$g_tournament_cur_tier"),
            (troop_set_slot, ":troop_id", slot_troop_personalityclash_penalties, ":grievance"),
          (else_try), #friendly lords, less will have this bonus as the tiers increase
            (call_script, "script_change_player_relation_with_troop", ":troop_id", ":relation"),
          (try_end),
        (try_end),
        (agent_get_kill_count, ":kill_count", ":agent_no", 1), #everyone is knocked unconscious
        (store_mul, ":kill_point", ":kill_count", 160000),#Make sure that kill count is the second most important variable
        (val_add, ":cur_point", ":kill_point"),
        (call_script, "script_get_troop_priority_point_for_tournament", ":troop_id"),
        (val_add, ":cur_point", reg0),
        (try_begin),#reset player's point if kill count is one after the first 2 rounds, or if it is zero
         (eq, ":agent_no", ":player_agent"),
         (eq, ":player_team_won", 0),
         (assign, ":not_passed", 1),
         (try_begin),
           (ge, ":kill_count", 2),
           (assign, ":not_passed", 0),
         (else_try),
           (eq, ":kill_count", 1),
           (le, "$g_tournament_cur_tier", 1),
           (assign, ":not_passed", 0),
         (try_end),
         (eq, ":not_passed", 1),
         (assign, ":cur_point", 0),
       (try_end),
       (agent_set_slot, ":agent_no", slot_agent_tournament_point, ":cur_point"),
     (try_end),
     (try_for_range, ":unused", 0, ":num_needed"),
       (assign, ":best_point", 0),
       (assign, ":best_agent_no", -1),
       (try_for_agents, ":agent_no"),
         (agent_is_human, ":agent_no"),
         (agent_get_slot, ":point", ":agent_no", slot_agent_tournament_point),
         (gt, ":point", ":best_point"),
         (assign, ":best_agent_no", ":agent_no"),
         (assign, ":best_point", ":point"),
       (try_end),
       (agent_set_slot, ":best_agent_no", slot_agent_tournament_point, 0),#Do not select the same agent again
       (agent_get_troop_id, ":troop_id", ":best_agent_no"),
       (call_script, "script_add_tournament_participant", ":troop_id"),
     (try_end),
     (assign, "$g_tournament_player_team_won", ":player_team_won"),
     (jump_to_menu, "mnu_town_tournament"),
     ])
]
