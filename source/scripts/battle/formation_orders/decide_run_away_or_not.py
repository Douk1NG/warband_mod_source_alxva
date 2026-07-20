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

decide_run_away_or_not_scripts = [
# script_update_map_bar
("decide_run_away_or_not",
    [
      (store_script_param, ":cur_agent", 1),
      (store_script_param, ":mission_time", 2),



      (assign, ":force_retreat", 0),
      (agent_get_team, ":agent_team", ":cur_agent"),
      (agent_get_division, ":agent_division", ":cur_agent"),
      (try_begin),
        (lt, ":agent_division", 9), #static classes
        (team_get_movement_order, ":agent_movement_order", ":agent_team", ":agent_division"),
        (eq, ":agent_movement_order", mordr_retreat),
        (assign, ":force_retreat", 1),
      (try_end),

      (agent_get_slot, ":is_cur_agent_running_away", ":cur_agent", slot_agent_is_running_away),
      (try_begin),
		#(neg|agent_slot_eq, ":cur_agent", slot_agent_courage_score_bonus, -1),
        (eq, ":is_cur_agent_running_away", 0),
        (try_begin),
          (eq, ":force_retreat", 1),
          (agent_clear_scripted_mode, ":cur_agent"),	#handle scripted mode troops - motomataru
          (agent_start_running_away, ":cur_agent"),
		  #(call_script, "script_agent_remove_from_square", ":cur_agent"), #jacobhinds infantry square script (remove if you don't have the infantry square script)
          (agent_set_slot, ":cur_agent",  slot_agent_is_running_away, 1),
		  #(agent_set_speed_limit, ":cur_agent", 60),
        (else_try),
          (ge, ":mission_time", 4), #first 4 seconds anyone does not run away whatever happens.
          (agent_get_slot, ":agent_courage_score", ":cur_agent",  slot_agent_courage_score),
          (store_agent_hit_points, ":agent_hit_points", ":cur_agent"),
          (val_mul, ":agent_hit_points", 10), #was 4
         # (try_begin),
          #  (agent_is_ally, ":cur_agent"),
           # (val_sub, ":agent_hit_points", 100), #ally agents will be more tend to run away, to make game more funnier/harder
         # (try_end),

#	IGNORE THIS, just rambling from several workarounds ago BEGIN

#	ratio
#	assume major battle 100(enemy) vs 100(ally)
#	20/100 = 0.2 = nigh unbreakable (for now give no negative effects)
#	100/20 = 5	= rout
#	battle ratio * 100
#	potential swing from 0-1000 courage score malus before rout
#	perhaps link to battle ai....? or unbalanced?

#	IGNORE THIS, just rambling from several workarounds ago END

		  (try_begin),
			(call_script, "script_cf_agent_can_rout", ":cur_agent"),
			(agent_is_ally, ":cur_agent"),
			(val_add, ":agent_hit_points", "$battle_ratio"),
		  (else_try),
			(call_script, "script_cf_agent_can_rout", ":cur_agent"),
			(val_sub, ":agent_hit_points", "$battle_ratio"),
		  (try_end),

          #(val_mul, ":agent_hit_points", 10),
          (store_sub, ":start_running_away_courage_score_limit", 1500, ":agent_hit_points"), #was 3500
          #(assign, reg11, ":agent_courage_score"),
          #(assign, reg12, ":start_running_away_courage_score_limit"),
          #(display_message, "@courage: {reg11}, limit: {reg12}"),
          (lt, ":agent_courage_score", ":start_running_away_courage_score_limit"), #if (courage score < 3500 - (agent hit points * 40)) and (agent is not running away) then start running away, average hit points : 50, average running away limit = 1500

          (agent_get_troop_id, ":troop_id", ":cur_agent"), #for now do not let heroes to run away from battle
          (neg|troop_is_hero, ":troop_id"),

		  # (try_begin), #this block is optional, delete if you don't have diplomacy or if you don't want retreating voices.
			  # (call_script, "script_dplmc_store_troop_is_female", ":troop_id"), #shout "retreat" if male
			  # (neq, reg0, 1),
			  # #(agent_play_sound, ":cur_agent", "snd_man_retreat"), #uncomment if you want retreating voices
		  # (try_end),

          (agent_clear_scripted_mode, ":cur_agent"),	#handle scripted mode troops - motomataru
          (agent_start_running_away, ":cur_agent"),
		  #(call_script, "script_agent_remove_from_square", ":cur_agent"), #jacobhinds infantry square script (remove if you don't have the infantry square script)
		  #(agent_set_speed_limit, ":cur_agent", 60),
          (agent_set_slot, ":cur_agent",  slot_agent_is_running_away, 1),
          #(display_message, "@AGENT HAS STARTED RUNNING"),
        (try_end),


      (else_try),
		#(neg|agent_slot_eq, ":cur_agent", slot_agent_courage_score_bonus, -1),
        (neq, ":force_retreat", 1),
        (agent_get_slot, ":agent_courage_score", ":cur_agent",  slot_agent_courage_score),
        (store_agent_hit_points, ":agent_hit_points", ":cur_agent"),
        (val_mul, ":agent_hit_points", 10), #was 4
   #     (try_begin),
    #      (agent_is_ally, ":cur_agent"),
     #     (val_sub, ":agent_hit_points", 100), #ally agents will be more tend to run away, to make game more funnier/harder
      #  (try_end),

		  (try_begin),
			(call_script, "script_cf_agent_can_rout", ":cur_agent"),
			(agent_is_ally, ":cur_agent"),
			(val_add, ":agent_hit_points", "$battle_ratio"),
		  (else_try),
			(call_script, "script_cf_agent_can_rout", ":cur_agent"),
			(val_sub, ":agent_hit_points", "$battle_ratio"),
		  (try_end),

        #(val_mul, ":agent_hit_points", 10),
        (store_sub, ":stop_running_away_courage_score_limit", 1800, ":agent_hit_points"),#what

        #(assign, reg11, ":agent_courage_score"),
        #(assign, reg12, ":start_running_away_courage_score_limit"),
        #(display_message, "@courage: {reg11}, limit: {reg12}"),

        (ge, ":agent_courage_score", ":stop_running_away_courage_score_limit"), #if (courage score > 3700 - agent hit points) and (agent is running away) then stop running away, average hit points : 50, average running away limit = 1700
        (agent_stop_running_away, ":cur_agent"),
        (agent_set_slot, ":cur_agent",  slot_agent_is_running_away, 0),
        #(display_message, "@AGENT HAS STOPPED RUNNING"),
      (try_end),
  ])
]
