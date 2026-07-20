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

apply_effect_of_other_people_on_courage_scores_scripts = [
#script_print_casualties_to_s0:
# script_apply_effect_of_other_people_on_courage_scores
# Input: none
# Output: none
("apply_effect_of_other_people_on_courage_scores",
    [
      (get_player_agent_no, ":player_agent"),

      (try_for_agents, ":centered_agent_no"),
        (agent_is_human, ":centered_agent_no"),
        (agent_is_alive, ":centered_agent_no"),
        (neq, ":centered_agent_no", ":player_agent"),
        ###(((courage_scores NEW FIX
        (agent_slot_eq, ":centered_agent_no", slot_agent_is_running_away, 1), 
        ###)))
        (agent_get_position, pos0, ":centered_agent_no"),
        (try_begin),
          (agent_is_ally, ":centered_agent_no"),
          (assign, ":is_centered_agent_ally", 1),
        (else_try),
          (assign, ":is_centered_agent_ally", 0),
        (try_end),

        (try_for_agents, ":agent_no"),
          (agent_is_human, ":agent_no"),
          (agent_is_alive, ":agent_no"),
          (neq, ":centered_agent_no", ":agent_no"),

          (try_begin),
            (agent_is_ally, ":agent_no"),
            (assign, ":is_agent_ally", 1),
          (else_try),
            (assign, ":is_agent_ally", 0),
          (try_end),

          (eq, ":is_centered_agent_ally", ":is_agent_ally"), #if centered agent and other agent is at same team then continue.
          (agent_get_slot, ":agent_is_running_away_or_not", ":agent_no", slot_agent_is_running_away),

          (try_begin),
            (eq, ":agent_no", ":player_agent"),
            (assign, ":agent_delta_courage_score", 6),
          (else_try),
            (agent_get_troop_id, ":troop_id", ":agent_no"),
            (troop_is_hero, ":troop_id"),

            #Hero Agent : if near agent (hero, agent_no) is not running away his positive effect on centered agent (centered_agent_no) fighting at his side is effected by his hit points.
            (try_begin),
              (neq, ":agent_is_running_away_or_not", 1), #if agent is not running away
              (store_agent_hit_points, ":agent_hit_points", ":agent_no"),
              (try_begin),
                (eq, ":agent_hit_points", 100),
                (assign, ":agent_delta_courage_score", 6),
              (else_try),
                (ge, ":agent_hit_points", 75),
                (assign, ":agent_delta_courage_score", 5),
              (else_try),
                (ge, ":agent_hit_points", 60),
                (assign, ":agent_delta_courage_score", 4),
              (else_try),
                (ge, ":agent_hit_points", 45),
                (assign, ":agent_delta_courage_score", 3),
              (else_try),
                (ge, ":agent_hit_points", 30),
                (assign, ":agent_delta_courage_score", 2),
              (else_try),
                (ge, ":agent_hit_points", 15),
                (assign, ":agent_delta_courage_score", 1),
              (end_try),
            (else_try),
              (assign, ":agent_delta_courage_score", 4),
            (end_try),
          (else_try),
            #Normal Agent : if near agent (agent_no) is not running away his positive effect on centered agent (centered_agent_no) fighting at his side is effected by his hit points.
            (try_begin),
              (neq, ":agent_is_running_away_or_not", 1), # if agent is not running away
              (store_agent_hit_points, ":agent_hit_points", ":agent_no"),
              (try_begin),
                (eq, ":agent_hit_points", 100),
                (assign, ":agent_delta_courage_score", 4),
              (else_try),
                (ge, ":agent_hit_points", 75),
                (assign, ":agent_delta_courage_score", 3),
              (else_try),
                (ge, ":agent_hit_points", 50),
                (assign, ":agent_delta_courage_score", 2),
              (else_try),
                (ge, ":agent_hit_points", 25),
                (assign, ":agent_delta_courage_score", 1),
              (try_end),
              (try_begin), # to make our warrior run away easier we decrease one, because they have player_agent (+6) advantage.
                (agent_is_ally, ":agent_no"),
                (val_sub, ":agent_delta_courage_score", 1),
              (try_end),
            (else_try),
              (assign, ":agent_delta_courage_score", 2),
            (end_try),
          (try_end),

          ###(((courage_scores NEW FIX
          (try_begin),
            (agent_get_troop_id, ":centered_troop_id", ":centered_agent_no"),
            (troop_is_hero, ":centered_troop_id"),
            (assign, ":agent_delta_courage_score_2", 4),
          (else_try),
            (assign, ":agent_delta_courage_score_2", 2),
          (try_end),

          (agent_get_position, pos1, ":agent_no"),
          (get_distance_between_positions, ":dist", pos0, pos1),

          (assign, ":pos_effect", 0),
          (try_begin),
            (lt, ":dist", 2000), #0-20 meter
            (assign, ":pos_effect", 50),
          (else_try),
            (lt, ":dist", 4000), #21-40 meter
            (assign, ":pos_effect", 40),
          (else_try),
            (lt, ":dist", 7000), #41-70 meter
            (assign, ":pos_effect", 30),
          (else_try),
            (lt, ":dist", 11000), #71-110 meter
            (assign, ":pos_effect", 20),
          (else_try),      
            (lt, ":dist", 16000), # 111-160 meter, assumed that eye can see agents friendly at most 160 meters far while fighting. 
                                  # this is more than below limit (108 meters) because we hear that allies come from further.
            (assign, ":pos_effect", 10),
          (try_end),

          (assign, ":neg_effect", 0),                             # negative effect of running agent on other ally agents are lower then positive effects above, to avoid starting  
          (try_begin),                                            # run away of all agents at a moment. I want to see agents running away one by one during battle, not all together.
            (lt, ":dist", 200), #1-2 meter,                       # this would create better game play.
            (assign, ":neg_effect", 15),
          (else_try),
            (lt, ":dist", 400), #3-4 meter, 
            (assign, ":neg_effect", 13),
          (else_try),
            (lt, ":dist", 600), #5-6 meter
            (assign, ":neg_effect", 11),
          (else_try),
            (lt, ":dist", 800), #7-8 meter
            (assign, ":neg_effect", 9),
          (else_try),
            (lt, ":dist", 1200), #9-12 meters
            (assign, ":neg_effect", 7),
          (else_try),
            (lt, ":dist", 2400), #13-24 meters
            (assign, ":neg_effect", 5),
          (else_try),
            (lt, ":dist", 4800), #25-48 meters
            (assign, ":neg_effect", 3),
          (else_try),
            (lt, ":dist", 9600), #49-98 meters, assumed that eye can see agents running away at most 98 meters far while fighting.
            (assign, ":neg_effect", 1),
          (try_end),   

          (try_begin),
            (neq, ":agent_is_running_away_or_not", 1),
            (val_mul, ":agent_delta_courage_score", 1),
            (val_mul, ":agent_delta_courage_score", ":pos_effect"),

            (val_mul, ":agent_delta_courage_score_2", -2),
            (val_mul, ":agent_delta_courage_score_2", ":neg_effect"),
            (neq, ":agent_delta_courage_score_2", 0),
            (agent_get_slot, ":agent_courage_score_2", ":agent_no", slot_agent_courage_score),
            (val_add, ":agent_courage_score_2", ":agent_delta_courage_score_2"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score_2"),

          (else_try),
            (val_mul, ":agent_delta_courage_score", -1),
            (val_mul, ":agent_delta_courage_score", ":neg_effect"),
          (try_end),
          (neq, ":agent_delta_courage_score", 0),
          (agent_get_slot, ":agent_courage_score", ":centered_agent_no", slot_agent_courage_score),
          (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
          (agent_set_slot, ":centered_agent_no", slot_agent_courage_score, ":agent_courage_score"),
          ###)))
        (try_end),
      (try_end),
  ])
]
