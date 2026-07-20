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

battle_tactic_apply_scripts = [
# script_calculate_team_powers
#jacobhinds Morale Code END
#(Native version)
# script_apply_death_effect_on_courage_scores
# Input: dead agent id, killer agent id
# Output: none
# ("apply_death_effect_on_courage_scores",
# [
# (store_script_param, ":dead_agent_no", 1),
# (store_script_param, ":killer_agent_no", 2),
# (try_begin),
# (agent_is_human, ":dead_agent_no"),
# (try_begin),
# (agent_is_ally, ":dead_agent_no"),
# (assign, ":is_dead_agent_ally", 1),
# (else_try),
# (assign, ":is_dead_agent_ally", 0),
# (try_end),
# (agent_get_position, pos0, ":dead_agent_no"),
# (assign, ":number_of_near_allies_to_dead_agent", 0),
# (try_for_agents, ":agent_no"),
# (agent_is_human, ":agent_no"),
# (agent_is_alive, ":agent_no"),
# (agent_get_position, pos1, ":agent_no"),
# (get_distance_between_positions, ":dist", pos0, pos1),
# (le, ":dist", 1300), # to count number of allies within 13 meters to dead agent.
# (try_begin),
# (agent_is_ally, ":agent_no"),
# (assign, ":is_agent_ally", 1),
# (else_try),
# (assign, ":is_agent_ally", 0),
# (try_end),
# (try_begin),
# (eq, ":is_dead_agent_ally", ":is_agent_ally"),
# (val_add, ":number_of_near_allies_to_dead_agent", 1), # (number_of_near_allies_to_dead_agent) is counted because if there are
# (try_end),                                              # many allies of dead agent around him, negative courage effect become less.
# (try_end),
# (try_for_agents, ":agent_no"),
# (agent_is_human, ":agent_no"),
# (agent_is_alive, ":agent_no"),
# (try_begin),
# (agent_is_ally, ":agent_no"),
# (assign, ":is_agent_ally", 1),
# (else_try),
# (assign, ":is_agent_ally", 0),
# (try_end),
# (try_begin), # each agent is effected by a killed agent positively if he is rival or negatively if he is ally.
# (neq, ":is_dead_agent_ally", ":is_agent_ally"),
# (assign, ":agent_delta_courage_score", 10),  # if killed agent is agent of rival side, add points to fear score
# (else_try),
# (assign, ":agent_delta_courage_score", -15), # if killed agent is agent of our side, decrease points from fear score
# (val_add, ":agent_delta_courage_score", ":number_of_near_allies_to_dead_agent"), # ":number_of_near_allies_to_dead_agent" is added because if there are many
# (try_begin),                                                                     # allies of dead agent around him, negative courage effect become less.
# (gt, ":agent_delta_courage_score", -5),
# (assign, ":agent_delta_courage_score", -5),
# (try_end),
# (agent_get_slot, ":dead_agent_was_running_away_or_not", ":dead_agent_no",  slot_agent_is_running_away), #look dead agent was running away or not.
# (try_begin),
# (eq, ":dead_agent_was_running_away_or_not", 1),
# (val_div, ":agent_delta_courage_score", 3),  # if killed agent was running away his negative effect on ally courage scores become very less. This added because
# (try_end),                                     # running away agents are easily killed and courage scores become very in a running away group after a time, and
# (try_end),                                       # they do not stop running away althought they pass near a new powerfull ally party.
# (agent_get_position, pos1, ":agent_no"),
# (get_distance_between_positions, ":dist", pos0, pos1),
# (try_begin),
# (eq, ":killer_agent_no", ":agent_no"),
# (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
# (val_mul, ":agent_delta_courage_score", 20),
# (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
# (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
# (try_end),
# (try_begin),
# (lt, ":dist", 100), #0-1 meters
# (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
# (val_mul, ":agent_delta_courage_score", 150),
# (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
# (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
# (else_try),
# (lt, ":dist", 200), #2 meters
# (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
# (val_mul, ":agent_delta_courage_score", 120),
# (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
# (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
# (else_try),
# (lt, ":dist", 300), #3 meter
# (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
# (val_mul, ":agent_delta_courage_score", 100),
# (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
# (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
# (else_try),
# (lt, ":dist", 400), #4 meters
# (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
# (val_mul, ":agent_delta_courage_score", 90),
# (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
# (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
# (else_try),
# (lt, ":dist", 600), #5-6 meters
# (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
# (val_mul, ":agent_delta_courage_score", 80),
# (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
# (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
# (else_try),
# (lt, ":dist", 800), #7-8 meters
# (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
# (val_mul, ":agent_delta_courage_score", 70),
# (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
# (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
# (else_try),
# (lt, ":dist", 1000), #9-10 meters
# (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
# (val_mul, ":agent_delta_courage_score", 60),
# (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
# (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
# (else_try),
# (lt, ":dist", 1500), #11-15 meter
# (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
# (val_mul, ":agent_delta_courage_score", 50),
# (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
# (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
# (else_try),
# (lt, ":dist", 2500), #16-25 meters
# (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
# (val_mul, ":agent_delta_courage_score", 40),
# (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
# (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
# (else_try),
# (lt, ":dist", 4000), #26-40 meters
# (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
# (val_mul, ":agent_delta_courage_score", 30),
# (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
# (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
# (else_try),
# (lt, ":dist", 6500), #41-65 meters
# (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
# (val_mul, ":agent_delta_courage_score", 20),
# (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
# (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
# (else_try),
# (lt, ":dist", 10000), #61-100 meters
# (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
# (val_mul, ":agent_delta_courage_score", 10),
# (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
# (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
# (try_end),
# (try_end),
# (try_end),
# ]), #ozan
# # script_decide_run_away_or_not
# # Input: none
# # Output: none
# ("decide_run_away_or_not",
# [
# (store_script_param, ":cur_agent", 1),
# (store_script_param, ":mission_time", 2),
# (assign, ":force_retreat", 0),
# (agent_get_team, ":agent_team", ":cur_agent"),
# (agent_get_division, ":agent_division", ":cur_agent"),
# (try_begin),
# (lt, ":agent_division", 9), #static classes
# (team_get_movement_order, ":agent_movement_order", ":agent_team", ":agent_division"),
# (eq, ":agent_movement_order", mordr_retreat),
# (assign, ":force_retreat", 1),
# (try_end),
# (agent_get_slot, ":is_cur_agent_running_away", ":cur_agent", slot_agent_is_running_away),
# (try_begin),
# (eq, ":is_cur_agent_running_away", 0),
# (try_begin),
# (eq, ":force_retreat", 1),
# (agent_start_running_away, ":cur_agent"),
# (agent_set_slot, ":cur_agent",  slot_agent_is_running_away, 1),
# (else_try),
# (ge, ":mission_time", 4), #first 45 seconds anyone does not run away whatever happens.
# (agent_get_slot, ":agent_courage_score", ":cur_agent",  slot_agent_courage_score),
# (store_agent_hit_points, ":agent_hit_points", ":cur_agent"),
# (val_mul, ":agent_hit_points", 4),
# (try_begin),
# (agent_is_ally, ":cur_agent"),
# (val_sub, ":agent_hit_points", 100), #ally agents will be more tend to run away, to make game more funnier/harder
# (try_end),
# (val_mul, ":agent_hit_points", 10),
# (store_sub, ":start_running_away_courage_score_limit", 3500, ":agent_hit_points"),
# (lt, ":agent_courage_score", ":start_running_away_courage_score_limit"), #if (courage score < 3500 - (agent hit points * 40)) and (agent is not running away) then start running away, average hit points : 50, average running away limit = 1500
# (agent_get_troop_id, ":troop_id", ":cur_agent"), #for now do not let heroes to run away from battle
# (neg|troop_is_hero, ":troop_id"),
# (agent_start_running_away, ":cur_agent"),
# (agent_set_slot, ":cur_agent",  slot_agent_is_running_away, 1),
# (try_end),
# (else_try),
# (neq, ":force_retreat", 1),
# (agent_get_slot, ":agent_courage_score", ":cur_agent",  slot_agent_courage_score),
# (store_agent_hit_points, ":agent_hit_points", ":cur_agent"),
# (val_mul, ":agent_hit_points", 4),
# (try_begin),
# (agent_is_ally, ":cur_agent"),
# (val_sub, ":agent_hit_points", 100), #ally agents will be more tend to run away, to make game more funnier/harder
# (try_end),
# (val_mul, ":agent_hit_points", 10),
# (store_sub, ":stop_running_away_courage_score_limit", 3700, ":agent_hit_points"),
# (ge, ":agent_courage_score", ":stop_running_away_courage_score_limit"), #if (courage score > 3700 - agent hit points) and (agent is running away) then stop running away, average hit points : 50, average running away limit = 1700
# (agent_stop_running_away, ":cur_agent"),
# (agent_set_slot, ":cur_agent",  slot_agent_is_running_away, 0),
# (try_end),
# ]), #ozan
# script_battle_tactic_apply
# Input: none
# Output: none
("battle_tactic_apply",
    [
      (call_script, "script_battle_tactic_apply_aux", "$ai_team_1", "$ai_team_1_battle_tactic"),
      (assign, "$ai_team_1_battle_tactic", reg0),
      (try_begin),
        (ge, "$ai_team_2", 0),
        (call_script, "script_battle_tactic_apply_aux", "$ai_team_2", "$ai_team_2_battle_tactic"),
        (assign, "$ai_team_2_battle_tactic", reg0),
      (try_end),
  ])
]
