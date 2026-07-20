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

select_battle_tactic_aux_scripts = [
# script_select_battle_tactic_aux
# Input: team_no
# Output: battle_tactic
("select_battle_tactic_aux",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":defense_not_an_option", 2),
      (assign, ":battle_tactic", 0),
      (get_player_agent_no, ":player_agent"),
      (agent_get_team, ":player_team", ":player_agent"),
      (try_begin),
        (eq, "$cant_leave_encounter", 1),
        (teams_are_enemies, ":team_no", ":player_team"),
        (assign, ":defense_not_an_option", 1),
      (try_end),
      (call_script, "script_team_get_class_percentages", ":team_no", 0),
      #      (assign, ":ai_perc_infantry", reg0),
      (assign, ":ai_perc_archers",  reg1),
      (assign, ":ai_perc_cavalry",  reg2),
      (call_script, "script_team_get_class_percentages", ":team_no", 1),#enemies of the ai_team
      #      (assign, ":enemy_perc_infantry", reg0),
      #      (assign, ":enemy_perc_archers",  reg1),
      #      (assign, ":enemy_perc_cavalry",  reg2),

      (store_random_in_range, ":rand", 0, 100),
      (try_begin),
        (assign, ":continue", 0),
        (try_begin),
          (teams_are_enemies, ":team_no", ":player_team"),
          (party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_hero_party),
          (assign, ":continue", 1),
        (else_try),
          (neg|teams_are_enemies, ":team_no", ":player_team"),
          (gt, "$g_ally_party", 0),
          (party_slot_eq, "$g_ally_party", slot_party_type, spt_kingdom_hero_party),
          (assign, ":continue", 1),
        (try_end),
        #(this_or_next|lt, ":rand", 20),
        (eq, ":continue", 1),
		(store_faction_of_party, ":enemy_faction_no", "$g_enemy_party"),
		(neq, ":enemy_faction_no", "fac_kingdom_3"), #don't let khergits use battle tactics
        (try_begin),
          (eq, ":defense_not_an_option", 0),
          (gt, ":ai_perc_archers", 50),
          (lt, ":ai_perc_cavalry", 35),
          (assign, ":battle_tactic", btactic_hold),
        (else_try),
          (lt, ":rand", 80),
          (assign, ":battle_tactic", btactic_follow_leader),
        (try_end),
      (try_end),
      (assign, reg0, ":battle_tactic"),
  ])
]
