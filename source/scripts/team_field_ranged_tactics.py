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

team_field_ranged_tactics_scripts = [
("team_field_ranged_tactics", [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":rel_army_size", 2),
      (store_script_param, ":battle_presence", 3),
      (assign, ":division", grc_archers), #Pre-Many Divisions
      (assign, ":bg_pos", Archers_Pos), #Pre-Many Divisions

      (try_begin),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_eq, ":team_no", ":slot", 0),
        (try_begin),	#undo reversion to BP_Jockey (see below)
          (lt, "$battle_phase", BP_Fight),
          (call_script, "script_cf_any_fighting"),
          (call_script, "script_cf_count_casualties"),
          (assign, "$battle_phase", BP_Fight),
        (try_end),

      (else_try),
        (call_script, "script_battlegroup_get_position", ":bg_pos", ":team_no", ":division"),
        (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, ":team_no", grc_everyone),
        (call_script, "script_point_y_toward_position", ":bg_pos", Enemy_Team_Pos),

        (store_add, ":slot", slot_team_d0_closest_enemy_special_dist, ":division"),	#distance to nearest enemy infantry agent
        (team_get_slot, ":distance_to_enemy", ":team_no", ":slot"),
        (try_begin),
          (eq, ":distance_to_enemy", 0),
          (call_script, "script_get_nearest_enemy_battlegroup_location", Nearest_Enemy_Battlegroup_Pos, ":team_no", ":bg_pos"),
          (assign, ":distance_to_enemy", reg0),
        (try_end),

        (try_begin),	#avoid being provoked from defensive position
          (ge, "$battle_phase", BP_Fight),
          (try_begin),
            (call_script, "script_cf_any_fighting"),
          (else_try),
            (assign, "$battle_phase", BP_Jockey),
            (assign, "$clock_reset", 0),
          (try_end),
        (try_end),

        (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
        (team_get_slot, ":is_firing", ":team_no", ":slot"),
        (store_add, ":slot", slot_team_d0_size, grc_infantry),
        (team_get_slot, ":num_infantry", ":team_no", ":slot"),

        (call_script, "script_calculate_decision_numbers", ":team_no", ":battle_presence"),
        (assign, ":decision_index", reg0),
        (assign, ":level_bump", reg1),

        (try_begin),
          (gt, ":decision_index", 86),	#outpower enemies more than 6:1?
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_charge),
            (team_give_order, ":team_no", ":division", mordr_charge),
          (try_end),

        (else_try),
          (lt, ":decision_index", 14),	#outpowered more than 6:1?
          (eq, ":num_infantry", 0),	#no infantry to delay enemy?
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_retreat),
            (team_give_order, ":team_no", ":division", mordr_retreat),
          (try_end),

        (else_try),
          (ge, "$battle_phase", BP_Jockey),
          (store_add, ":slot", slot_team_d0_low_ammo, ":division"),
          (team_slot_ge, ":team_no", ":slot", 1),	#running out of ammo?
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_charge),
            (team_give_order, ":team_no", ":division", mordr_charge),
          (try_end),

        (else_try),
          (ge, "$battle_phase", BP_Fight),
          (eq, ":is_firing", 0),
          (gt, ":decision_index", Advance_More_Point),
          (le, ":distance_to_enemy", AI_long_range),	#closer than reposition?
          (team_give_order, ":team_no", ":division", mordr_advance),

        #hold somewhere
        (else_try),
          (store_add, ":decision_index", ":rel_army_size", ":level_bump"),	#decision w.r.t. largest enemy team
          (assign, ":move_archers", 0),

          (init_position, Team_Starting_Point),
          (team_get_slot, reg0, ":team_no", slot_team_starting_x),
          (position_set_x, Team_Starting_Point, reg0),
          (team_get_slot, reg0, ":team_no", slot_team_starting_y),
          (position_set_y, Team_Starting_Point, reg0),
          (position_set_z_to_ground_level, Team_Starting_Point),

          (try_begin),
            (eq, "$battle_phase", BP_Setup),
            (assign, ":move_archers", 1),
          (else_try),
            (ge, "$battle_phase", BP_Fight),
            (try_begin),
              (neg | is_between, ":distance_to_enemy", AI_charge_distance, AI_long_range),
              (assign, ":move_archers", 1),
            (else_try),
              (lt, ":decision_index", Hold_Point),	#probably coming from a defensive position (see below)
              (eq, "$FormAI_AI_no_defense", 0),	#player hasn't set disallow defense option?
              (eq, ":is_firing", 0),	#probably because player team has retreated
              (assign, ":move_archers", 1),
            (try_end),
          (else_try),	#jockey phase
            (this_or_next | gt, "$FormAI_AI_no_defense", 0),	#player has set disallow defense option OR
            (ge, ":decision_index", Hold_Point),	#not starting in a defensive position (see below)
            (try_begin),
              (gt, ":distance_to_enemy", AI_long_range),	#enemy very far off
              (assign, ":move_archers", 1),
            (else_try),
              (call_script, "script_point_y_toward_position", Team_Starting_Point, ":bg_pos"),
              (position_get_rotation_around_z, reg0, Team_Starting_Point),
              (position_get_rotation_around_z, reg1, ":bg_pos"),
              (val_sub, reg0, reg1),
              (this_or_next | is_between, reg0, -45, 45),	#only move if within "cone of advancement" to prevent constant adjusting at
              #border OR
              (eq, ":is_firing", 0),	#if not firing for some reason (hill in way?)

              (try_begin),
                (eq, ":num_infantry", 0),	#no infantry to wait for
                (assign, ":move_archers", 1),
              (else_try),
                (call_script, "script_battlegroup_get_position", Infantry_Pos, ":team_no", grc_infantry),
                (get_distance_between_positions, ":infantry_to_enemy", Infantry_Pos, Enemy_Team_Pos),
                (get_distance_between_positions, ":archers_to_enemy", ":bg_pos", Enemy_Team_Pos),
                (val_sub, ":infantry_to_enemy", ":archers_to_enemy"),
                (le, ":infantry_to_enemy", 1500),	#don't outstrip infantry when closing
                (assign, ":move_archers", 1),
              (try_end),
            (try_end),
          (try_end),

          (try_begin),
            (gt, ":move_archers", 0),
            (try_begin),
              (lt, ":decision_index", Hold_Point),	#outnumbered?
              (eq, "$FormAI_AI_no_defense", 0),	#player hasn't set disallow defense option?
              (lt, "$battle_phase", BP_Fight),
              (neq, ":team_no", 1),	#not attacker?
              (neq, ":team_no", 3),	#not ally of attacker?
              (store_div, ":distance_to_move", ":distance_to_enemy", 6),	#middle of rear third of battlefield
              (assign, ":hill_search_radius", ":distance_to_move"),

            (else_try),
              (try_begin),
                (ge, "$battle_phase", BP_Fight),
                (copy_position, ":bg_pos", Team_Starting_Point),
                (call_script, "script_point_y_toward_position", ":bg_pos", Enemy_Team_Pos),
                (try_begin),
                  (gt, ":num_infantry", 0),
                  (store_add, ":slot", slot_team_d0_closest_enemy, grc_infantry),
                  (team_get_slot, ":enemy_agent_nearest_infantry", ":team_no", ":slot"),
                  (le, ":enemy_agent_nearest_infantry", 0),
                  (agent_get_team, ":target_team", ":enemy_agent_nearest_infantry"),
                  (agent_get_division, ":target_division", ":enemy_agent_nearest_infantry"),
                  (call_script, "script_battlegroup_get_position", Nearest_Enemy_Battlegroup_Pos, ":target_team", ":target_division"),
                  (get_distance_between_positions, ":distance_to_enemy", ":bg_pos", Nearest_Enemy_Battlegroup_Pos),
                (else_try),
                  (call_script, "script_get_nearest_enemy_battlegroup_location", Nearest_Enemy_Battlegroup_Pos, ":team_no", ":bg_pos"),
                  (assign, ":distance_to_enemy", reg0),
                (try_end),
              (try_end),

              (try_begin),
                (eq, "$battle_phase", BP_Setup),
                (assign, ":shot_distance", AI_long_range),
              (else_try),
                (assign, ":shot_distance", AI_firing_distance),
                (store_sub, reg1, AI_firing_distance, AI_charge_distance),
                (val_sub, reg1, 200),	#subtract two meters to prevent automatically provoking melee from forward
                #enemy infantry
                (store_add, ":slot", slot_team_d0_percent_throwers, ":division"),
                (team_get_slot, reg0, ":team_no", ":slot"),
                (val_mul, reg1, reg0),
                (val_div, reg1, 100),
                (val_sub, ":shot_distance", reg1),
              (try_end),

              (store_sub, ":distance_to_move", ":distance_to_enemy", ":shot_distance"),
              (store_div, ":hill_search_radius", ":shot_distance", 3),	#limit so as not to run into enemy
              (try_begin),
                (lt, "$battle_phase", BP_Fight),
                (try_begin),
                  (this_or_next | eq, "$battle_phase", BP_Setup),
                  (lt, ":battle_presence", Advance_More_Point),	#expect to meet halfway?
                  (val_div, ":distance_to_move", 2),
                (try_end),
              (try_end),
            (try_end),

            (position_move_y, ":bg_pos", ":distance_to_move", 0),
            (try_begin),
              (lt, "$battle_phase", BP_Fight),
              (copy_position, pos1, ":bg_pos"),
              (store_div, reg0, ":hill_search_radius", 100),
              (call_script, "script_find_high_ground_around_pos1_corrected", ":bg_pos", reg0),
            (try_end),
          (try_end),

          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_hold),
            (team_give_order, ":team_no", ":division", mordr_hold),
          (try_end),
          (call_script, "script_set_formation_destination", ":team_no", ":division", ":bg_pos"),
        (try_end),
      (try_end)])
]
