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

cf_calculate_battle_ratio_scripts = [
("cf_calculate_battle_ratio",
		[
			#bugfix; prevents earlier scripts from enforcing
			#fixed_point_* operations
			#(set_fixed_point_multiplier, 1),

			(assign, "$battle_ratio", 0),

			(assign, "$j_num_us_ready", 0),
			(assign, "$j_num_us_wounded", 0),
			(assign, "$j_num_us_routed", 0),
			(assign, "$j_num_us_dead", 0),

			(assign, "$j_num_allies_ready", 0),
			(assign, "$j_num_allies_wounded", 0),
			(assign, "$j_num_allies_routed", 0),
			(assign, "$j_num_allies_dead", 0),

			(assign, "$j_num_enemies_ready", 0),
			(assign, "$j_num_enemies_wounded", 0),
			(assign, "$j_num_enemies_routed", 0),
			(assign, "$j_num_enemies_dead", 0),

			#count and categorize agents (me, ally, enemy/wounded, dead, routed, alive)
			(try_for_agents, ":cur_agent"),
			  (agent_is_human, ":cur_agent"),
			  (agent_get_party_id, ":agent_party", ":cur_agent"),
			  (try_begin),
				(eq, ":agent_party", "p_main_party"),
				(try_begin),
				  (agent_is_alive, ":cur_agent"),
				  (val_add, "$j_num_us_ready", 1),
				(else_try),
				  (agent_is_wounded, ":cur_agent"),
				  (val_add, "$j_num_us_wounded", 1),
				(else_try),
				  (agent_is_routed, ":cur_agent"),
				  (val_add, "$j_num_us_routed", 1),
				(else_try),
				  (val_add, "$j_num_us_dead", 1),
				(try_end),
			  (else_try),
				(agent_is_ally, ":cur_agent"),
				(try_begin),
				  (agent_is_alive, ":cur_agent"),
				  (val_add, "$j_num_allies_ready", 1),
				(else_try),
				  (agent_is_wounded, ":cur_agent"),
				  (val_add, "$j_num_allies_wounded", 1),
				(else_try),
				  (agent_is_routed, ":cur_agent"),
				  (val_add, "$j_num_allies_routed", 1),
				(else_try),
				  (val_add, "$j_num_allies_dead", 1),
				(try_end),
			  (else_try),
				(try_begin),
				  (agent_is_alive, ":cur_agent"),
				  (val_add, "$j_num_enemies_ready", 1),
				(else_try),
				  (agent_is_wounded, ":cur_agent"),
				  (val_add, "$j_num_enemies_wounded", 1),
				(else_try),
				  (agent_is_routed, ":cur_agent"),
				  (val_add, "$j_num_enemies_routed", 1),
				(else_try),
				  (val_add, "$j_num_enemies_dead", 1),
				(try_end),
			  (try_end),
			(try_end),

			#don't think I need these
			# (assign, ":ratio", 0),
			# (assign, ":ratio_3", 0),
			# (assign, ":difference", 0),
			# (assign, ":enemy_sqrt", 0),
			# (assign, ":ally_sqrt", 0),

			# ALLY STRENGTH
			(assign, ":ally_strength", 1),
			(val_add, ":ally_strength", "$j_num_enemies_routed"),
			(val_add, ":ally_strength", "$j_num_enemies_dead"),
			(val_add, ":ally_strength", "$j_num_enemies_wounded"),
			#ready is counted three times
			(val_add, ":ally_strength", "$j_num_us_ready"),
			(val_add, ":ally_strength", "$j_num_us_ready"),
			(val_add, ":ally_strength", "$j_num_us_ready"),
			(val_add, ":ally_strength", "$j_num_allies_ready"),
			(val_add, ":ally_strength", "$j_num_allies_ready"),
			(val_add, ":ally_strength", "$j_num_allies_ready"),

			# ENEMY STRENGTH
			(assign, ":enemy_strength", 1),
			(val_add, ":enemy_strength", "$j_num_us_dead"),
			(val_add, ":enemy_strength", "$j_num_us_wounded"),
			(val_add, ":enemy_strength", "$j_num_us_routed"),
			(val_add, ":enemy_strength", "$j_num_allies_dead"),
			(val_add, ":enemy_strength", "$j_num_allies_wounded"),
			(val_add, ":enemy_strength", "$j_num_allies_routed"),
			#ready is counted three times
			(val_add, ":enemy_strength", "$j_num_enemies_ready"),
			(val_add, ":enemy_strength", "$j_num_enemies_ready"),
			(val_add, ":enemy_strength", "$j_num_enemies_ready"),

			#(A*10/E)
			#10/1 ratio = 10,000 morale penalty
			(store_mul, ":enemy_value", ":enemy_strength", battle_ratio_multiple),
			(val_div, ":enemy_value", ":ally_strength"),

			#(E*10/A)
			(store_mul, ":ally_value", ":ally_strength", battle_ratio_multiple),
			(val_div, ":ally_value", ":enemy_strength"),

			#if enemy value is greater, use negative of that.
			(try_begin),
				(gt, ":enemy_value", ":ally_value"),
				(val_sub, ":enemy_value", battle_ratio_multiple),
				(store_sub, ":enemy_value", 0, ":enemy_value"),
				(assign, "$battle_ratio", ":enemy_value"),
			(else_try),
				(val_sub, ":ally_value", battle_ratio_multiple),
				(assign, "$battle_ratio", ":ally_value"),
			(try_end),

			#(val_clamp, "$battle_ratio", -max_ratio, max_ratio),

			# (assign, reg2, ":enemy_value"),
			# (assign, reg1, ":ally_value"),

			#(assign, reg0, "$battle_ratio"),
			#(display_message, "@Battle Ratio:{reg0}"),


			#(sqrt A - sqrt E)^3 + (A-E) (unused)

				#(sqrt A - sqrt E)^3
				# (store_sqrt, ":enemy_sqrt", ":enemy_strength"),
				# (store_sqrt, ":ally_sqrt", ":ally_strength"),
				# (store_sub, ":ratio", ":ally_sqrt", ":enemy_sqrt"),
				# #I get the feeling store_pow doesn't work or is deprecated in some way; keep getting weird results
				# #perhaps use cumbersome approach instead:
				# (store_pow, ":ratio_3", ":ratio", 3),
				# # (store_mul, ":ratio_3", ":ratio", ":ratio"), #squared
				# # (val_mul, ":ratio_3", ":ratio"), #cubed

				# #(A-E)
				# (store_sub, ":difference", ":ally_strength", ":enemy_strength"),

			# (store_add, "$battle_ratio", ":difference", ":ratio_3"),
			# (val_mul, "$battle_ratio", 10),
			# (val_mul, "$battle_ratio", 10),

		#housekeeping BEGIN
			# (assign, reg2, "$battle_ratio"),
			# (assign, reg3, ":ally_strength"),
			# (assign, reg4, ":enemy_strength"),
			# (display_message, "@{reg3}/{reg4}={reg2}"),

			#find average morale for each side
			# (assign, ":enemy_morale", 1),
			# (assign, ":ally_morale", 1),
			# (assign, ":ally_amount", 1),

			#store morale for all troops
			# (try_for_agents,":cur_agent"),
				# (agent_is_human, ":cur_agent"),
				# (agent_is_alive, ":cur_agent"),
				# (agent_get_slot, ":agent_courage_score", ":cur_agent", slot_agent_courage_score),
				# (try_begin),
					# (agent_is_ally, ":cur_agent"),
					# (val_add, ":ally_morale", ":agent_courage_score"),
				# (else_try),
					# (val_add, ":enemy_morale", ":agent_courage_score"),
				# (try_end),
			# (try_end),

			# (store_add, ":ally_amount", "$j_num_us_ready", "$j_num_allies_ready"),

			# (store_div, reg6, ":ally_morale", ":ally_amount"),
			# (store_div, reg7, ":enemy_morale", "$j_num_enemies_ready"),
			# (display_message, "@Morale: {reg6}/{reg7}"),

			#check that fixed_point_whatever or something else isn't screwing me over
			#answer: it is, and tends to fluctuate
			# (store_sqrt, ":four", 16),
			# (assign, reg5, ":four"),
			# (display_message, "@the square root of sixteen is {reg5}"),
		#housekeeping END

			#100-10	= ~400
			#100-30	= ~150
			#100-50	= ~75

			#50-10	= ~100
			#50-30	= ~25
			#50-40	= ~10
		]
	)
]
