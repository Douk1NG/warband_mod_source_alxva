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

process_place_divisions_scripts = [
("process_place_divisions", [
      (assign, ":num_bgroups", 0),
      (try_for_range, ":division", 0, 9),
        (class_is_listening_order, "$fplayer_team_no", ":division"),
        (store_add, ":slot", slot_team_d0_target_team, ":division"),
        (team_set_slot, "$fplayer_team_no", ":slot", -1),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_ge, "$fplayer_team_no", ":slot", 1),
        (store_add, ":slot", slot_team_d0_fclock, ":division"),
        (team_set_slot, "$fplayer_team_no", ":slot", 1),
        (team_get_order_position, pos1, "$fplayer_team_no", ":division"),
        (val_add, ":num_bgroups", 1),
      (try_end),

      (try_begin),
        (gt, ":num_bgroups", 0),
        (copy_position, Target_Pos, pos1),	#kludge around team_get_order_position rotation problems

        (try_begin),
          (eq, "$battle_phase", BP_Deploy),

          (try_begin),
            (eq, "$g_is_quick_battle", 1),
            (assign, reg0, 5),
          (else_try),
            (party_get_skill_level, reg0, "p_main_party", "skl_tactics"),
          (try_end),
          (store_mul, ":range_limit", reg0, 1000),

          (agent_get_position, Temp_Pos, "$fplayer_agent_no"),
          (get_distance_between_positions, reg0, Target_Pos, Temp_Pos),
          (lt, ":range_limit", reg0),
          (display_message, "@Your party's tactical skill limits how far away you can deploy your troops!"),
          (call_script, "script_point_y_toward_position", Temp_Pos, Target_Pos),
          (copy_position, Target_Pos, Temp_Pos),
          (position_move_y, Target_Pos, ":range_limit"),
        (try_end),

        #player designating target battlegroup?
        (assign, ":distance_to_enemy", Far_Away),
        (try_for_range, ":team", 0, 4),
          (teams_are_enemies, ":team", "$fplayer_team_no"),
          (team_slot_ge, ":team", slot_team_size, 1),
          (try_for_range, ":division", 0, 9),
            (store_add, ":slot", slot_team_d0_size, ":division"),
            (team_slot_ge, ":team", ":slot", 1),
            (call_script, "script_battlegroup_get_position", Temp_Pos, ":team", ":division"),
            (get_distance_between_positions, reg0, Target_Pos, Temp_Pos),
            (gt, ":distance_to_enemy", reg0),
            (assign, ":distance_to_enemy", reg0),
            (assign, ":closest_enemy_team", ":team"),
            (assign, ":closest_enemy_division", ":division"),
          (try_end),
        (try_end),

        (call_script, "script_battlegroup_get_action_radius", ":closest_enemy_team", ":closest_enemy_division"),
        (assign, ":radius_enemy_battlegroup", reg0),

        (try_begin),
          (le, ":distance_to_enemy", ":radius_enemy_battlegroup"),	#target position within radius of an enemy battlegroup?
          (le, ":distance_to_enemy", AI_charge_distance),	#limit so player can place divisions near large enemy battlegroups without
          #selecting them
          (call_script, "script_battlegroup_get_position", Target_Pos, ":closest_enemy_team", ":closest_enemy_division"),
          (gt, ":num_bgroups", 1),
          (store_add, ":slot", slot_team_d0_type, ":closest_enemy_division"),
          (team_get_slot, reg0, ":closest_enemy_team", ":slot"),
          (call_script, "script_str_store_division_type_name", s1, reg0),
          (display_message, "@...and attack enemy {s1} division!"),
        (try_end),

        (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, "$fplayer_team_no", grc_everyone),
        (call_script, "script_point_y_toward_position", Target_Pos, Enemy_Team_Pos),

        #place player divisions
        (agent_get_position, pos49, "$fplayer_agent_no"),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
          (gt, ":troop_count", 0),

          (try_begin),
            (le, ":distance_to_enemy", ":radius_enemy_battlegroup"),	#target position within radius of an enemy battlegroup?
            (le, ":distance_to_enemy", AI_charge_distance),	#limit so player can place divisions near large enemy battlegroups without
            #selecting them
            (store_add, ":slot", slot_team_d0_target_team, ":division"),
            (team_set_slot, "$fplayer_team_no", ":slot", ":closest_enemy_team"),
            (store_add, ":slot", slot_team_d0_target_division, ":division"),
            (team_set_slot, "$fplayer_team_no", ":slot", ":closest_enemy_division"),
          (try_end),

          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":fformation", "$fplayer_team_no", ":slot"),

          (try_begin),
            (gt, ":num_bgroups", 1),
            (agent_set_position, "$fplayer_agent_no", Target_Pos),	#fake out script_battlegroup_place_around_leader
            (call_script, "script_player_attempt_formation", ":division", ":fformation", 0),
          (else_try),
            (try_begin),
              (le, ":distance_to_enemy", ":radius_enemy_battlegroup"),	#target position within radius of an enemy battlegroup?
              (le, ":distance_to_enemy", AI_charge_distance),	#limit so player can place divisions near large enemy battlegroups without
              #selecting them
              (call_script, "script_battlegroup_get_attack_destination", Target_Pos, "$fplayer_team_no", ":division", ":closest_enemy_team", ":closest_enemy_division"),
              (store_add, ":slot", slot_team_d0_type, ":closest_enemy_division"),
              (team_get_slot, reg0, ":closest_enemy_team", ":slot"),
              (call_script, "script_str_store_division_type_name", s1, reg0),
              (display_message, "@...and attack enemy {s1} division!"),
            (try_end),

            (call_script, "script_set_formation_destination", "$fplayer_team_no", ":division", Target_Pos),

            (gt, ":fformation", formation_none),
            (store_add, ":slot", slot_team_d0_formation_space, ":division"),
            (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
            (try_begin),
              (store_add, ":slot", slot_team_d0_type, ":division"),
              (team_get_slot, ":sd_type", "$fplayer_team_no", ":slot"),
              (neq, ":sd_type", sdt_cavalry),
              (neq, ":sd_type", sdt_harcher),
              (try_begin),
                (eq, ":sd_type", sdt_archer),
                (call_script, "script_get_centering_amount", formation_default, ":troop_count", ":div_spacing"),
                (val_mul, reg0, -1),
                (assign, ":script", "script_form_archers"),
              (else_try),
                (call_script, "script_get_centering_amount", ":fformation", ":troop_count", ":div_spacing"),
                (assign, ":script", "script_form_infantry"),
              (try_end),
              (position_move_x, Target_Pos, reg0),
            (else_try),
              (assign, ":script", "script_form_cavalry"),
            (try_end),
            (copy_position, pos1, Target_Pos),
            (call_script, ":script", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0, ":fformation"),
          (try_end),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", mordr_hold),
        (try_end), #division loop
        (agent_set_position, "$fplayer_agent_no", pos49),
      (try_end),	#num_bgroups > 0
  ])
]
