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

process_player_division_positioning_scripts = [
("process_player_division_positioning", [
      (call_script, "script_division_reset_places"),

      #implement HOLD OVER THERE when player lets go of key
      (try_begin),
        (ge, "$gk_order_hold_over_there", HOT_F1_held),
        (neg | game_key_is_down, gk_order_1),
        (assign, "$gk_order_hold_over_there", HOT_no_order),
        (call_script, "script_process_place_divisions"),
      (try_end),	#HOLD OVER THERE

      #periodic functions
      (assign, ":save_autorotate", "$FormAI_autorotate"),
      (assign, "$FormAI_autorotate", 0),
      (try_for_range, ":division", 0, 9),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
        (gt, ":troop_count", 0),

        (store_add, ":slot", slot_team_d0_target_team, ":division"),
        (team_get_slot, ":target_team", "$fplayer_team_no", ":slot"),
        (store_add, ":slot", slot_team_d0_target_division, ":division"),
        (team_get_slot, ":target_division", "$fplayer_team_no", ":slot"),
        (try_begin),
          (ge, ":target_team", 0),	#enemy battlegroup targeted?
          (store_add, ":slot", slot_team_d0_size, ":target_division"),
          (team_get_slot, reg0, ":target_team", ":slot"),

          (le, reg0, 0),	#target destroyed?
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),

          (store_add, ":slot", slot_team_d0_type, ":target_division"),
          (team_get_slot, reg0, ":target_team", ":slot"),
          (call_script, "script_str_store_division_type_name", s1, reg0),

          (str_store_class_name, s2, ":division"),
          (display_message, "@{s2}: returning after destroying enemy {s1} division."),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", mordr_follow),
        (try_end),

        (store_add, ":slot", slot_team_d0_fclock, ":division"),
        (team_get_slot, ":fclock", "$fplayer_team_no", ":slot"),
        (store_mod, ":time_slice", ":fclock", Reform_Trigger_Modulus),
        (val_add, ":fclock", 1),
        (team_set_slot, "$fplayer_team_no", ":slot", ":fclock"),

        (try_begin),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_slot_eq, "$fplayer_team_no", ":slot", mordr_follow),
          (call_script, "script_battlegroup_place_around_leader", "$fplayer_team_no", ":division", "$fplayer_agent_no"),
          (team_set_slot, "$fplayer_team_no", ":slot", mordr_follow),	#override script_battlegroup_place_around_leader

        #periodically reform
        (else_try),
          (eq, ":time_slice", 0),
          (team_get_movement_order, reg0, "$fplayer_team_no", ":division"),
          (neq, reg0, mordr_stand_ground),

          (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, "$fplayer_team_no", grc_everyone),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":fformation", "$fplayer_team_no", ":slot"),
          (try_begin),
            (gt, ":fformation", formation_none),
            (store_add, ":slot", slot_team_d0_formation_space, ":division"),
            (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
            (store_add, ":slot", slot_team_d0_type, ":division"),
            (team_get_slot, ":sd_type", "$fplayer_team_no", ":slot"),

            (try_begin),
              (store_add, ":slot", slot_team_d0_first_member, ":division"),
              (team_slot_eq, "$fplayer_team_no", ":slot", "$fplayer_agent_no"),
              (assign, ":first_member_is_player", 1),
            (else_try),
              (assign, ":first_member_is_player", 0),
            (try_end),

            (try_begin),
              (ge, ":target_team", 0),	#enemy battlegroup targeted?
              (try_begin),
                (this_or_next | eq, ":sd_type", sdt_archer),
                (this_or_next | eq, ":sd_type", sdt_harcher),
                (eq, ":sd_type", sdt_skirmisher),
                (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
                (team_slot_ge, "$fplayer_team_no", ":slot", 1),	#ranged are firing?
                (call_script, "script_formation_current_position", pos1, "$fplayer_team_no", ":division"),	#stop advancing
              (else_try),
                (call_script, "script_battlegroup_get_attack_destination", pos1, "$fplayer_team_no", ":division", ":target_team", ":target_division"),
              (try_end),

            (else_try),
              (call_script, "script_get_formation_destination", pos1, "$fplayer_team_no", ":division"),
              (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
              (team_get_slot, ":is_fighting", "$fplayer_team_no", ":slot"),
              (try_begin),
                (neq, ":sd_type", sdt_cavalry),
                (neq, ":sd_type", sdt_harcher),
                (neq, ":is_fighting", 0),
                (eq, ":first_member_is_player", 0),
                (position_move_y, pos1, -2000),
              (try_end),
              (call_script, "script_point_y_toward_position", pos1, Enemy_Team_Pos),
              (try_begin),
                (neq, ":sd_type", sdt_cavalry),
                (neq, ":sd_type", sdt_harcher),
                (neq, ":is_fighting", 0),
                (eq, ":first_member_is_player", 0),
                (position_move_y, pos1, 2000),
              (try_end),
            (try_end),

            (call_script, "script_set_formation_destination", "$fplayer_team_no", ":division", pos1),

            (try_begin),
              (eq, ":sd_type", sdt_archer),
              (call_script, "script_get_centering_amount", formation_default, ":troop_count", ":div_spacing"),
              (val_mul, reg0, -1),
              (position_move_x, pos1, reg0),
            (else_try),
              (neq, ":sd_type", sdt_cavalry),
              (neq, ":sd_type", sdt_harcher),
              (call_script, "script_get_centering_amount", ":fformation", ":troop_count", ":div_spacing"),
              (position_move_x, pos1, reg0),
            (try_end),

            (try_begin),
              (eq, ":sd_type", sdt_archer),
              (call_script, "script_form_archers", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":fformation"),
            (else_try),
              (this_or_next | eq, ":sd_type", sdt_cavalry),
              (eq, ":sd_type", sdt_harcher),
              (try_begin),
                (ge, ":target_team", 0),	#enemy battlegroup targeted?
                (call_script, "script_formation_current_position", pos29, "$fplayer_team_no", ":division"),
                (call_script, "script_battlegroup_get_position", Enemy_Team_Pos, ":target_team", ":target_division"),
                (get_distance_between_positions, ":distance_to_enemy", pos29, Enemy_Team_Pos),

                (call_script, "script_battlegroup_get_action_radius", "$fplayer_team_no", ":division"),
                (assign, ":combined_radius", reg0),
                (call_script, "script_battlegroup_get_action_radius", ":target_team", ":target_division"),
                (val_add, ":combined_radius", reg0),

                (le, ":distance_to_enemy", ":combined_radius"),
                (call_script, "script_formation_end", "$fplayer_team_no", ":division"),
                (str_store_class_name, s1, ":division"),
                (display_message, "@{s1}: cavalry formation disassembled."),
                (set_show_messages, 0),
                (team_give_order, "$fplayer_team_no", ":division", mordr_charge),
                (set_show_messages, 1),
              (else_try),
                (call_script, "script_form_cavalry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player"),
              (try_end),
            (else_try),
              (call_script, "script_form_infantry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":fformation"),
            (try_end),

          (else_try),	#divisions not in formation
            (ge, ":target_team", 0),	#enemy battlegroup targeted?
            (store_add, ":slot", slot_team_d0_target_division, ":division"),
            (team_get_slot, ":target_division", "$fplayer_team_no", ":slot"),
            (try_begin),
              (this_or_next | eq, ":sd_type", sdt_archer),
              (this_or_next | eq, ":sd_type", sdt_harcher),
              (eq, ":sd_type", sdt_skirmisher),
              (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
              (team_slot_ge, "$fplayer_team_no", ":slot", 1),	#ranged are firing?
              (call_script, "script_battlegroup_get_position", pos1, "$fplayer_team_no", ":division"),	#stop advancing
            (else_try),
              (call_script, "script_battlegroup_get_attack_destination", pos1, "$fplayer_team_no", ":division", ":target_team", ":target_division"),
            (try_end),
            (call_script, "script_set_formation_destination", "$fplayer_team_no", ":division", pos1),
            (team_get_movement_order, ":existing_order", "$fplayer_team_no", ":division"),
            (try_begin),
              (ge, ":target_team", 0),	#enemy battlegroup targeted?
              (call_script, "script_battlegroup_get_position", pos29, "$fplayer_team_no", ":division"),
              (call_script, "script_battlegroup_get_position", Enemy_Team_Pos, ":target_team", ":target_division"),
              (get_distance_between_positions, ":distance_to_enemy", pos29, Enemy_Team_Pos),

              (call_script, "script_battlegroup_get_action_radius", "$fplayer_team_no", ":division"),
              (assign, ":combined_radius", reg0),
              (call_script, "script_battlegroup_get_action_radius", ":target_team", ":target_division"),
              (val_add, ":combined_radius", reg0),

              (le, ":distance_to_enemy", ":combined_radius"),
              (try_begin),
                (neq, ":existing_order", mordr_charge),
                (set_show_messages, 0),
                (team_give_order, "$fplayer_team_no", ":division", mordr_charge),
                (set_show_messages, 1),
              (try_end),
            (else_try),
              (neq, ":existing_order", mordr_hold),
              (set_show_messages, 0),
              (team_give_order, "$fplayer_team_no", ":division", mordr_hold),
              (set_show_messages, 1),
            (try_end),
          (try_end),
        (try_end),	#Periodic Reform
      (try_end),	#Division Loop

      (assign, "$FormAI_autorotate", ":save_autorotate"),])
]
