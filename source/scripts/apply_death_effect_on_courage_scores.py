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

apply_death_effect_on_courage_scores_scripts = [
#ozan
#jacobhinds Morale Code BEGIN
# script_apply_death_effect_on_courage_scores
# Input: dead agent id, killer agent id
# Output: none
("apply_death_effect_on_courage_scores",
    [
      (store_script_param, ":dead_agent_no", 1),
      (store_script_param, ":killer_agent_no", 2),



      (try_begin),
        (agent_is_human, ":dead_agent_no"),

        (try_begin),
          (agent_is_ally, ":dead_agent_no"),
          (assign, ":is_dead_agent_ally", 1),
        (else_try),
          (assign, ":is_dead_agent_ally", 0),
        (try_end),

        #(agent_get_position, pos0, ":dead_agent_no"),
        #(assign, ":number_of_near_allies_to_dead_agent", 0),

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
            # (val_add, ":number_of_near_allies_to_dead_agent", 1), #was 1
																	# # (number_of_near_allies_to_dead_agent) is counted because if there are
          # (try_end),                                              # many allies of dead agent around him, negative courage effect become less.

			# # jacobhinds edit: wait a second, this doesn't really make sense.
			# # If a soldier in a blob of soldiers gets slaughtered, nobody routs,
			# # but if they're outside, they cause more routing. Halve this effect:
			# # distance should play the biggest role.
          # (val_div, ":number_of_near_allies_to_dead_agent", 2),

        # (try_end),

        (try_for_agents, ":agent_no"),
          (agent_is_human, ":agent_no"),
          (agent_is_alive, ":agent_no"),

          (try_begin),
            (agent_is_ally, ":agent_no"),
            (assign, ":is_agent_ally", 1),
          (else_try),
            (assign, ":is_agent_ally", 0),
          (try_end),

          (try_begin), # each agent is effected by a killed agent positively if he is rival or negatively if he is ally.
            (neq, ":is_dead_agent_ally", ":is_agent_ally"),
            (assign, ":agent_delta_courage_score", 3),  # if killed agent is agent of rival side, add points to fear score #was 10 #after that, was 1
          (else_try),
            (assign, ":agent_delta_courage_score", -5), # if killed agent is agent of our side, decrease points from fear score #jacobhinds was -15, was -4 before battle_ratio overhaul, FEAR SCORE
            #(val_add, ":agent_delta_courage_score", ":number_of_near_allies_to_dead_agent"), # ":number_of_near_allies_to_dead_agent" is added because if there are many # allies of dead agent around him, negative courage effect become less.
            # (try_begin),
              # (lt, ":agent_delta_courage_score", -4), #was -5 #was -2 before battle_ratio overhaul #was gt
              # (assign, ":agent_delta_courage_score", -4), #was -5
            # (try_end),

            (agent_get_slot, ":dead_agent_was_running_away_or_not", ":dead_agent_no",  slot_agent_is_running_away), #look dead agent was running away or not.
            (try_begin),
              (eq, ":dead_agent_was_running_away_or_not", 1),
              (val_div, ":agent_delta_courage_score", 3), #was 3 # if killed agent was running away his negative effect on ally courage scores become very less. This added because
            (try_end),                                     # running away agents are easily killed and courage scores become very in a running away group after a time, and
          (try_end),                                       # they do not stop running away although they pass near a new powerful ally party.
          (agent_get_position, pos1, ":agent_no"),
          (get_distance_between_positions, ":dist", pos0, pos1),

          (try_begin), #if agent is the killer, give him x20 more courage than usual
            (eq, ":killer_agent_no", ":agent_no"),
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 20),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (try_end),

			#jacobhinds edit: prevent morale from getting too high
          (try_begin),
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
			(ge, ":agent_courage_score", max_morale),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, max_morale),
          (try_end),

          (try_begin),
            (lt, ":dist", 100), #0-1 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 120), #was 150
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 200), #2 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 110), #was 120
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 300), #3 meter
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 100),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 400), #4 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 90),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 600), #5-6 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 80),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 800), #7-8 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 70),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 1000), #9-10 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 60),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 1500), #11-15 meter
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 50),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 2500), #16-25 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 40),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 4000), #26-40 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 30),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 6500), #41-65 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 20),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 10000), #61-100 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 10),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (try_end),
        (try_end),
      (try_end),

			#housekeeping
			# (store_random_in_range, ":rand", 0, 10),
			# (try_begin),
				# (eq, ":rand", 1),
				# (assign, reg4, ":agent_delta_courage_score"),
				# (display_message, "@{reg4}"),
			# (try_end),
			#housekeeping

      ])
]
