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

formation_end_scripts = [
("formation_end", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (try_begin),
        (store_add, ":slot", slot_team_d0_formation, ":fdivision"),
        (neg | team_slot_eq, ":fteam", ":slot", formation_none),
        (team_slot_ge, ":fteam", ":slot", formation_none),

        (try_begin),
          (eq, Native_Formations_Implementation, WFaS_Implementation),
          (team_set_slot, ":fteam", ":slot", formation_2_row),
        (else_try),
          (team_set_slot, ":fteam", ":slot", formation_none),
        (try_end),

        (team_get_leader, ":leader", ":fteam"),

        (try_for_agents, ":agent"),
          (agent_is_alive, ":agent"),
          (agent_is_human, ":agent"),
          (agent_get_group, ":team", ":agent"),
          (eq, ":team", ":fteam"),
          (neq, ":leader", ":agent"),
          (agent_get_division, ":bgdivision", ":agent"),
          (eq, ":bgdivision", ":fdivision"),
          (agent_clear_scripted_mode, ":agent"),
          (call_script, "script_switch_from_noswing_weapons", ":agent"),
          (agent_ai_set_always_attack_in_melee, ":agent", 0),
          (agent_set_speed_limit, ":agent", 100),
          (agent_set_slot, ":agent", slot_agent_formation_rank, 0),
          (agent_set_slot, ":agent", slot_agent_inside_formation, 0),
        (try_end),

        (try_begin),
          (eq, ":fteam", "$fplayer_team_no"),
          (store_add, ":slot", slot_team_d0_formation_space, ":fdivision"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),

          #adjust for differences between the systems of spreading out (Native spreads
          #out about twice as much)
          (try_begin),
            (eq, Native_Formations_Implementation, WFaS_Implementation),
            (assign, ":max_spacing", 3),
          (else_try),
            (assign, ":max_spacing", 2),
          (try_end),

          (store_mul, ":double_max", ":max_spacing", 2),

          (try_begin),
            (ge, ":div_spacing", ":double_max"),	#beyond Native max
            (assign, ":div_spacing", ":max_spacing"),
          (else_try),
            (gt, ":div_spacing", 0),
            (set_show_messages, 0),
            (team_give_order, "$fplayer_team_no", ":fdivision", mordr_stand_closer),
            (set_show_messages, 1),
            (val_div, ":div_spacing", 2),
          (try_end),

          (team_set_slot, "$fplayer_team_no", ":slot", ":div_spacing"),
        (try_end),
      (try_end),])
]
