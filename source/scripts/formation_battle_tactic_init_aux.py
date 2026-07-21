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

formation_battle_tactic_init_aux_scripts = [
#script_troop_debug_range
# script_formation_battle_tactic_init_aux
# Input: team_no, battle_tactic
# Output: none
("formation_battle_tactic_init_aux",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_tactic", 2),
      (team_get_leader, ":ai_leader", ":team_no"),
      (try_begin),
        (eq, ":battle_tactic", btactic_hold),
        (agent_get_position, pos1, ":ai_leader"),
        (call_script, "script_find_high_ground_around_pos1", ":team_no", 30),
        (copy_position, pos1, pos52),
        (call_script, "script_find_high_ground_around_pos1", ":team_no", 30), # call again just in case we are not at peak point.
        (copy_position, pos1, pos52),
        (call_script, "script_find_high_ground_around_pos1", ":team_no", 30), # call again just in case we are not at peak point.
        (team_give_order, ":team_no", grc_everyone, mordr_hold),
        (team_set_order_position, ":team_no", grc_everyone, pos52),
        (team_give_order, ":team_no", grc_archers, mordr_advance),
        (team_give_order, ":team_no", grc_archers, mordr_advance),
      (else_try),
        (eq, ":battle_tactic", btactic_follow_leader),
        (team_get_leader, ":ai_leader", ":team_no"),
        (ge, ":ai_leader", 0),
        (agent_set_speed_limit, ":ai_leader", 8),
        (agent_get_position, pos60, ":ai_leader"),
        (team_give_order, ":team_no", grc_everyone, mordr_hold),
        (team_set_order_position, ":team_no", grc_everyone, pos60),
      (try_end),
# formations additions
	  (call_script, "script_division_reset_places"),
	  (call_script, "script_get_default_formation", ":team_no"),
	  (assign, ":fformation", reg0),

	  (try_begin),
		(call_script, "script_cf_battlegroup_valid_formation", ":team_no", grc_infantry, ":fformation"),
		(store_add, ":slot", slot_team_d0_formation, grc_infantry),
		(team_set_slot, ":team_no", ":slot", ":fformation"),
		(store_add, ":slot", slot_team_d0_formation_space, grc_infantry),
		(team_set_slot, ":team_no", ":slot", 0),
	  (else_try),
		(call_script, "script_formation_end", ":team_no", grc_infantry),
	  (try_end),
	  (call_script, "script_battlegroup_place_around_leader", ":team_no", grc_infantry),

	  (try_begin),
		(call_script, "script_cf_battlegroup_valid_formation", ":team_no", grc_archers, formation_default),
		(store_add, ":slot", slot_team_d0_formation, grc_archers),
		(team_set_slot, ":team_no", ":slot", formation_default),
		(store_add, ":slot", slot_team_d0_formation_space, grc_archers),
		(team_set_slot, ":team_no", ":slot", 2),
	  (else_try),
		(call_script, "script_formation_end", ":team_no", grc_archers),
	  (try_end),
	  (call_script, "script_battlegroup_place_around_leader", ":team_no", grc_archers),

	  (try_begin),
		(call_script, "script_cf_battlegroup_valid_formation", ":team_no", grc_cavalry, formation_wedge),
		(store_add, ":slot", slot_team_d0_formation, grc_cavalry),
		(team_set_slot, ":team_no", ":slot", formation_wedge),
		(store_add, ":slot", slot_team_d0_formation_space, grc_cavalry),
		(team_set_slot, ":team_no", ":slot", 0),
	  (else_try),
		(call_script, "script_formation_end", ":team_no", grc_cavalry),
	  (try_end),
	  (call_script, "script_battlegroup_place_around_leader", ":team_no", grc_cavalry),

	  (team_give_order, ":team_no", grc_archers, mordr_spread_out),
	  (team_give_order, ":team_no", grc_archers, mordr_spread_out),
# end formations additions
  ])
]
