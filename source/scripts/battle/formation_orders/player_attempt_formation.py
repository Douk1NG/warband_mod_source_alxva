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

player_attempt_formation_scripts = [
("player_attempt_formation", [
      (store_script_param, ":fdivision", 1),
      (store_script_param, ":fformation", 2),
      (store_script_param, ":form_on_spot", 3),
      (set_fixed_point_multiplier, 100),
      (try_begin),
        (eq, ":fformation", formation_ranks),
        (str_store_string, s1, "@ranks"),
      (else_try),
        (eq, ":fformation", formation_shield),
        (str_store_string, s1, "@shield wall"),
      (else_try),
        (eq, ":fformation", formation_wedge),
        (str_store_string, s1, "@wedge"),
      (else_try),
        (eq, ":fformation", formation_square),
        (str_store_string, s1, "@square"),
      (else_try),
        (str_store_string, s1, "@up"),
      (try_end),
      (str_store_class_name, s2, ":fdivision"),

      (try_begin),
        (call_script, "script_cf_battlegroup_valid_formation", "$fplayer_team_no", ":fdivision", ":fformation"),
        (try_begin),	#new formation?
          (store_add, ":slot", slot_team_d0_formation, ":fdivision"),
          (neg | team_slot_eq, "$fplayer_team_no", ":slot", ":fformation"),
          (team_set_slot, "$fplayer_team_no", ":slot", ":fformation"),
          (store_add, reg1, ":fdivision", 1),
          (display_message, "@Division {reg1} {s2} forming {s1}."),
          (store_add, ":slot", slot_team_d0_fclock, ":fdivision"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_target_team, ":fdivision"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),

          (store_add, ":slot", slot_team_d0_formation_space, ":fdivision"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),

          #bring unformed divisions into sync with formations' minimum
          (set_show_messages, 0),
          (assign, reg0, ":div_spacing"),
          (try_for_range, reg1, reg0, formation_start_spread_out),	#spread out for ease of forming up
            (team_give_order, "$fplayer_team_no", ":fdivision", mordr_spread_out),
            (val_add, ":div_spacing", 1),
          (try_end),
          (set_show_messages, 1),

          (team_set_slot, "$fplayer_team_no", ":slot", ":div_spacing"),
        (try_end),

        #divisions must stop to order themselves
        (store_add, ":slot", slot_team_d0_move_order, ":fdivision"),
        (team_get_slot, ":div_order", "$fplayer_team_no", ":slot"),
        (try_begin),
          (this_or_next | eq, ":div_order", mordr_stand_ground),
          (this_or_next | eq, ":div_order", mordr_charge),
          (eq, ":div_order", mordr_retreat),
          (call_script, "script_battlegroup_get_position", pos1, "$fplayer_team_no", ":fdivision"),
          (team_give_order, "$fplayer_team_no", ":fdivision", mordr_hold),
          (call_script, "script_set_formation_destination", "$fplayer_team_no", ":fdivision", pos1),
        (try_end),

      (else_try),
        (assign, ":return_val", reg0),
        (call_script, "script_formation_end", "$fplayer_team_no", ":fdivision"),
        (gt, ":fformation", formation_none),
        (store_add, reg1, ":fdivision", 1),
        (try_begin),
          (gt, ":return_val", 0),
          (display_message, "@Not enough troops in division {reg1} {s2} to form {s1}."),
        (else_try),
          (store_add, ":slot", slot_team_d0_type, ":fdivision"),
          (team_get_slot, reg0, "$fplayer_team_no", ":slot"),
          (call_script, "script_str_store_division_type_name", s3, reg0),
          (display_message, "@Division {reg1} {s2} is an {s3} division and cannot form {s1}."),
        (try_end),
      (try_end),

      (try_begin),
        (eq, ":form_on_spot", 0),
        (call_script, "script_battlegroup_place_around_leader", "$fplayer_team_no", ":fdivision", "$fplayer_agent_no"),
      (else_try),
        (eq, ":form_on_spot", 2),
        (copy_position, pos1, Target_Pos),
        (call_script, "script_battlegroup_place_around_pos1", "$fplayer_team_no", ":fdivision", "$fplayer_agent_no"),
      (try_end),])
]
