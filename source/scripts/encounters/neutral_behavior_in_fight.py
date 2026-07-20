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

neutral_behavior_in_fight_scripts = [
("neutral_behavior_in_fight",
	[
      (get_player_agent_no, ":player_agent"),
      (agent_get_position, pos3, ":player_agent"),
      (agent_get_team, ":player_team", ":player_agent"),

      (try_begin),
        (gt, "$g_main_attacker_agent", 0),
        (agent_get_team, ":attacker_team_no", "$g_main_attacker_agent"),
        (agent_get_position, pos5, "$g_main_attacker_agent"),
      (else_try),
        (eq, ":attacker_team_no", -1),
        (agent_get_position, pos5, ":player_agent"),
      (try_end),

      (set_fixed_point_multiplier, 100),

      (try_for_agents, ":agent"),
        (agent_get_team, ":other_team", ":agent"),
        (neq, ":other_team", ":attacker_team_no"),
        (neq, ":other_team", ":player_team"),

        (agent_get_troop_id, ":troop_id", ":agent"),
        #SB : better range checks
        (this_or_next|eq, ":troop_id", "trp_farmer"), #farmers are "neutral"
        (neg|is_between, ":troop_id", soldiers_begin, soldiers_end), #but lie within this range
        (troop_slot_eq, ":troop_id", slot_troop_mission_participation, mp_unaware), #neutral prisoners?

        (agent_get_position, pos4, ":agent"),

        (assign, ":best_position_score", 0),
        (assign, ":best_position", -1),

        (try_begin),
          (neg|agent_slot_eq, ":agent", slot_agent_is_running_away, 0), #if agent is running away
          (agent_get_slot, ":target_entry_point_plus_one",  ":agent", slot_agent_is_running_away),
          (store_sub, ":target_entry_point", ":target_entry_point_plus_one", 1),
          (entry_point_get_position, pos6, ":target_entry_point"),
          (get_distance_between_positions, ":agent_distance_to_target", pos6, pos4),
          (lt, ":agent_distance_to_target", 100),
          (agent_set_slot, ":agent", slot_agent_is_running_away, 0),
        (try_end),

        (agent_slot_eq, ":agent", slot_agent_is_running_away, 0), #if agent is not already running away

        (try_begin), #stand in place
          (get_distance_between_positions, ":distance", pos4, pos5),
          (get_distance_between_positions, ":distance_to_player", pos4, pos3),

          (val_min, ":distance", ":distance_to_player"),

          (this_or_next|gt, ":distance", 700), #7 meters away from main belligerents
          (main_hero_fallen),

          (agent_set_scripted_destination, ":agent", pos4),
        (else_try), #get out of the way
          (try_for_range, ":target_entry_point", 0, 64),
            (neg|entry_point_is_auto_generated, ":target_entry_point"),
            (entry_point_get_position, pos6, ":target_entry_point"),
            (get_distance_between_positions, ":agent_distance_to_target", pos6, pos4),
            (get_distance_between_positions, ":player_distance_to_target", pos6, pos3),
            (store_sub, ":position_score", ":player_distance_to_target", ":agent_distance_to_target"),
            (ge, ":position_score", 0),
            (try_begin),
              (ge, ":agent_distance_to_target", 2000),
              (store_sub, ":extra_distance", ":agent_distance_to_target", 2000),
              (val_min, ":extra_distance", 1000),
              (val_min, ":agent_distance_to_target", 2000), #if more than 10 meters assume it is 10 meters far while calculating best run away target
              (val_sub, ":agent_distance_to_target", ":extra_distance"),
            (try_end),
            (val_mul, ":position_score", ":agent_distance_to_target"),
            (try_begin),
              (ge, ":position_score", ":best_position_score"),
              (assign, ":best_position_score", ":position_score"),
              (assign, ":best_position", ":target_entry_point"),
            (try_end),
          (try_end),

          (try_begin),
            (ge, ":best_position", 0),
            (entry_point_get_position, pos6, ":best_position"),
            (agent_set_speed_limit, ":agent", 10),
            (agent_set_scripted_destination, ":agent", pos6),
            (store_add, ":best_position_plus_one", ":best_position", 1),
            (agent_set_slot, ":agent", slot_agent_is_running_away, ":best_position_plus_one"),
          (try_end),
        (try_end),
	  (try_end),
	])
]
