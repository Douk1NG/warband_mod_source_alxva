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

store_battlegroup_data_scripts = [
("store_battlegroup_data", [
      (assign, ":team0_leader", 0),
      (assign, ":team0_x_leader", 0),
      (assign, ":team0_y_leader", 0),
      (assign, ":team0_zrot_leader", 0),
      (assign, ":team0_level_leader", 0),
      (assign, ":team1_leader", 0),
      (assign, ":team1_x_leader", 0),
      (assign, ":team1_y_leader", 0),
      (assign, ":team1_zrot_leader", 0),
      (assign, ":team1_level_leader", 0),
      (assign, ":team2_leader", 0),
      (assign, ":team2_x_leader", 0),
      (assign, ":team2_y_leader", 0),
      (assign, ":team2_zrot_leader", 0),
      (assign, ":team2_level_leader", 0),
      (assign, ":team3_leader", 0),
      (assign, ":team3_x_leader", 0),
      (assign, ":team3_y_leader", 0),
      (assign, ":team3_zrot_leader", 0),
      (assign, ":team3_level_leader", 0),

      #save some info
      (try_for_range, ":division", 0, 9),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (try_begin),
          (team_slot_ge, "$fplayer_team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_exists, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),

        (else_try),
          (store_add, ":slot", slot_team_d0_exists, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 0),
        (try_end),
      (try_end),

      #Team Slots reset every mission, like agent slots, but just to be sure for
      #when it gets called during the mission
      (try_for_range, ":slot", reset_team_stats_begin, reset_team_stats_end), #Those within the "RESET GROUP" in formations_constants
        (try_for_range, ":team", 0, 4),
          (team_set_slot, ":team", ":slot", 0),
        (try_end),
      (try_end),

      (try_for_agents, ":cur_agent"),
        (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, -1),

        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_slot_eq, ":cur_agent", slot_agent_is_running_away, 0),

        (agent_get_group, ":bgteam", ":cur_agent"),
        (agent_get_division, ":bgdivision", ":cur_agent"),
        (agent_get_class, ":agent_class", ":cur_agent"),
        (agent_get_position, pos1, ":cur_agent"),

        (try_begin),
          (agent_is_non_player, ":cur_agent"),

          (store_add, ":slot", slot_team_d0_type, ":bgdivision"),
          (team_get_slot, ":bgtype", ":bgteam", ":slot"),
          (this_or_next | eq, ":bgtype", sdt_cavalry),	#assigned to horsed division
          (eq, ":bgtype", sdt_harcher),

          (team_get_riding_order, reg0, ":bgteam", ":bgdivision"),
          (neq, reg0, rordr_dismount),

          (team_get_order_position, pos0, ":bgteam", ":bgdivision"),
          (get_distance_between_positions, ":old_distance", pos0, pos1),
          (gt, ":old_distance", AI_charge_distance),	#agent is out of formation?

          (assign, ":target_type", ":bgtype"),

          (try_begin),
            (eq, ":agent_class", grc_infantry),	#Native has transferred this agent to infantry
            (assign, ":target_type", sdt_infantry),

            (try_for_range, ":item_slot", ek_item_0, ek_head),
              (eq, ":bgteam", "$fplayer_team_no"),	#AI doesn't use extended right now
              (agent_get_item_slot, ":item", ":cur_agent", ":item_slot"),
              (call_script, "script_cf_is_thrusting_weapon", ":item"),
              (item_get_type, reg0, ":item"),
              (eq, reg0, itp_type_polearm),
              (assign, ":target_type", sdt_polearm),
            (try_end),

          (else_try),
            (eq, ":agent_class", grc_archers),	#Native has transferred this agent to archers
            (assign, ":target_type", sdt_archer),

            (try_for_range, ":item_slot", ek_item_0, ek_head),
              (eq, ":bgteam", "$fplayer_team_no"),	#AI doesn't use extended right now
              (agent_get_item_slot, ":item", ":cur_agent", ":item_slot"),
              (call_script, "script_cf_is_weapon_ranged", ":item", 1),
              (agent_get_ammo, reg1, ":cur_agent", 0),
              (ge, reg1, minimum_ranged_ammo),  #more than two to throw on a charge?
              (item_get_type, reg0, ":item"),
              (eq, reg0, itp_type_thrown),
              (assign, ":target_type", sdt_skirmisher),
            (try_end),
          (try_end),

          (neq, ":target_type", ":bgtype"),
          (assign, ":bgdivision", ":target_type"),

          (try_for_range_backwards, ":new_division", 0, 9),
            (store_add, ":slot", slot_team_d0_size, ":new_division"),
            (team_get_slot, reg0, ":bgteam", ":slot"),
            (gt, reg0, 0),

            (store_add, ":slot", slot_team_d0_type, ":new_division"),
            (team_get_slot, reg0, ":bgteam", ":slot"),
            (eq, reg0, ":target_type"),

            (assign, ":bgdivision", ":new_division"),
          (try_end),

          (try_begin),
            (store_add, ":slot", slot_team_d0_exists, ":bgdivision"),
            (team_slot_eq, "$fplayer_team_no", ":slot", 0),	#division does not yet exist?
            (agent_is_alive, "$fplayer_agent_no"),
            (store_add, ":slot", slot_team_d0_move_order, ":bgdivision"),
            (neg | team_slot_eq, "$fplayer_team_no", ":slot", mordr_follow),
            (team_set_slot, "$fplayer_team_no", ":slot", mordr_follow),
            (set_show_messages, 0),
            (team_give_order, "$fplayer_team_no", ":bgdivision", mordr_follow),
            (set_show_messages, 1),
          (try_end),

          (agent_set_slot, ":cur_agent", slot_agent_new_division, ":bgdivision"),	#reassign
          (agent_set_division, ":cur_agent", ":bgdivision"),

        (else_try),	#Maintain any changed divisions (apparently agents get switched back)
          (agent_is_non_player, ":cur_agent"),
          (agent_slot_ge, ":cur_agent", slot_agent_new_division, 0),
          (neg | agent_slot_eq, ":cur_agent", slot_agent_new_division, ":bgdivision"),
          (agent_get_slot, ":bgdivision", ":cur_agent", slot_agent_new_division),
          (agent_set_division, ":cur_agent", ":bgdivision"),
        (try_end),
        (agent_get_troop_id, ":cur_troop", ":cur_agent"),
        (try_begin),
          (game_in_multiplayer_mode),
          (try_begin),
            (is_between, ":cur_troop", multiplayer_troops_begin, multiplayer_troops_end),	#it's a player
            (assign, ":bgdivision", -1),
          (try_end),
        (else_try),
          (team_get_leader, ":leader", ":bgteam"),
          (eq, ":leader", ":cur_agent"),
          (assign, ":bgdivision", -1),
        (try_end),
        (store_character_level, ":cur_level", ":cur_troop"),
        (agent_get_ammo, ":cur_ammo", ":cur_agent", 0),

        #get weapon characteristics
        (assign, ":cur_weapon_type", 0),
        (assign, ":cur_weapon_length", 0),
        (assign, ":cur_swung_weapon_length", 0),
        (agent_get_wielded_item, ":cur_weapon", ":cur_agent", 0),
        (try_begin),
          (is_between, ":cur_weapon", weapons_begin, weapons_end),
          # (neg | is_between, ":cur_weapon", estandartes_begin, estandartes_end),	#put exceptions here, such as standards, that will otherwise force a lot of
          #extra spacing for nothing
          (item_get_weapon_length, ":cur_weapon_length", ":cur_weapon"),

          (try_begin),
            (call_script, "script_cf_is_thrusting_weapon", ":cur_weapon"),
          (else_try),
            (assign, ":cur_swung_weapon_length", ":cur_weapon_length"),
          (try_end),
        (try_end),

        #add up armor
        (assign, ":cur_avg_armor", 0),
        (try_for_range, ":item_slot", ek_head, ek_horse),
          (agent_get_item_slot, ":armor", ":cur_agent", ":item_slot"),
          (gt, ":armor", itm_no_item),
          (item_get_head_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
          (item_get_body_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
          (item_get_leg_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
        (try_end),
        (agent_get_wielded_item, ":armor", ":cur_agent", 1),	#include shield
        (try_begin),
          (gt, ":armor", itm_no_item),
          (item_get_type, ":item_type", ":armor"),
          (eq, ":item_type", itp_type_shield),
          (item_get_body_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
        (try_end),
        (val_div, ":cur_avg_armor", 3),	#average the zones (head, body, leg)

        #average with horse armor for mounted agents
        (agent_get_horse, ":cur_horse", ":cur_agent"),
        (try_begin),
          (gt, ":cur_horse", -1),
          (agent_get_item_id, ":itm_horse", ":cur_horse"),
          (gt, ":itm_horse", itm_no_item),
          (item_get_body_armor, reg0, ":itm_horse"),
          (val_add, ":cur_avg_armor", reg0),
          (val_div, ":cur_avg_armor", 2),
        (try_end),

        (position_get_x, ":x_value", pos1),
        (position_get_y, ":y_value", pos1),
        (position_get_rotation_around_z, ":zrot_value", pos1),
        (try_begin),
          (eq, ":bgdivision", -1), #Leaders
          (try_begin),
            (eq, ":bgteam", 0),
            (assign, ":team0_leader", 1),
            (assign, ":team0_x_leader", ":x_value"),
            (assign, ":team0_y_leader", ":y_value"),
            (assign, ":team0_zrot_leader", ":zrot_value"),
            (assign, ":team0_level_leader", ":cur_level"),
          (else_try),
            (eq, ":bgteam", 1),
            (assign, ":team1_leader", 1),
            (assign, ":team1_x_leader", ":x_value"),
            (assign, ":team1_y_leader", ":y_value"),
            (assign, ":team1_zrot_leader", ":zrot_value"),
            (assign, ":team1_level_leader", ":cur_level"),
          (else_try),
            (eq, ":bgteam", 2),
            (assign, ":team2_leader", 1),
            (assign, ":team2_x_leader", ":x_value"),
            (assign, ":team2_y_leader", ":y_value"),
            (assign, ":team2_zrot_leader", ":zrot_value"),
            (assign, ":team2_level_leader", ":cur_level"),
          (else_try),
            (eq, ":bgteam", 3),
            (assign, ":team3_leader", 1),
            (assign, ":team3_x_leader", ":x_value"),
            (assign, ":team3_y_leader", ":y_value"),
            (assign, ":team3_zrot_leader", ":zrot_value"),
            (assign, ":team3_level_leader", ":cur_level"),
          (try_end),
        (else_try),
          # (agent_get_ammo, reg0, ":cur_agent", 1), #Division in Melee
          (try_begin),
            # (le, reg0, 0), #not wielding ranged weapon?
            (agent_get_attack_action, reg0, ":cur_agent"),
            (gt, reg0, 0),
            (store_add, ":slot", slot_team_d0_is_fighting, ":bgdivision"),
            (team_get_slot, reg0, ":bgteam", ":slot"),
            (val_add, reg0, 1),
            (team_set_slot, ":bgteam", ":slot", reg0),
          (try_end),

          (store_add, ":slot", slot_team_d0_size, ":bgdivision"), #Division Count
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (try_begin),
            (ge, ":cur_ammo", minimum_ranged_ammo),
            (store_add, ":slot", slot_team_d0_percent_ranged, ":bgdivision"), #Division Percentage are Archers
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (val_add, ":value", 1),
            (team_set_slot, ":bgteam", ":slot", ":value"),
          (else_try),
            (store_add, ":slot", slot_team_d0_low_ammo, ":bgdivision"), #Division Running out of Ammo Flag
            (team_set_slot, ":bgteam", ":slot", 1),
          (try_end),

          (try_begin),
            (eq, ":cur_weapon_type", itp_type_thrown),
            (store_add, ":slot", slot_team_d0_percent_throwers, ":bgdivision"), #Division Percentage are Throwers
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (val_add, ":value", 1),
            (team_set_slot, ":bgteam", ":slot", ":value"),
          (try_end),

          (store_add, ":slot", slot_team_d0_level, ":bgdivision"), #Division Level
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":cur_level"),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_weapon_length, ":bgdivision"), #Division Weapon Length
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":cur_weapon_length"),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_swung_weapon_length, ":bgdivision"), #Division Swung Weapon Length
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (try_begin),
            (lt, ":value", ":cur_swung_weapon_length"),
            (team_set_slot, ":bgteam", ":slot", ":cur_swung_weapon_length"),
          (try_end),

          (store_add, ":slot", slot_team_d0_armor, ":bgdivision"), #Division Armor
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":cur_avg_armor"),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (try_begin),	#Division First Rank Shortest Weapon Length
            (agent_slot_eq, ":cur_agent", slot_agent_formation_rank, 1),
            (store_add, ":slot", slot_team_d0_front_weapon_length, ":bgdivision"),
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (this_or_next | eq, ":value", 0),
            (gt, ":value", ":cur_weapon_length"),
            (team_set_slot, ":bgteam", ":slot", ":cur_weapon_length"),
          (try_end),

          (store_add, ":slot", slot_team_d0_avg_x, ":bgdivision"), #Position X
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":x_value"),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_avg_y, ":bgdivision"), #Position Y
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":y_value"),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_avg_zrot, ":bgdivision"), #Rotation
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":zrot_value"),
          (team_set_slot, ":bgteam", ":slot", ":value"),
        (try_end), #Leader vs Regular

        (try_begin),
          (eq, ":agent_class", grc_archers),
          (team_get_slot, ":value", ":bgteam", slot_team_num_archers),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", slot_team_num_archers, ":value"),

        (else_try),
          (eq, ":agent_class", grc_cavalry),
          (team_get_slot, ":value", ":bgteam", slot_team_num_cavalry),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", slot_team_num_cavalry, ":value"),

        (else_try),
          (eq, ":agent_class", grc_infantry),
          (team_get_slot, ":value", ":bgteam", slot_team_num_infantry),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", slot_team_num_infantry, ":value"),
        (try_end),

        #find nearest enemy agent
        (assign, ":nearest_runner", -1),
        (agent_ai_get_num_cached_enemies, ":num_nearby_agents", ":cur_agent"),
        (try_for_range, reg0, 0, ":num_nearby_agents"),
          (agent_ai_get_cached_enemy, ":enemy_agent", ":cur_agent", reg0),
          (agent_is_alive, ":enemy_agent"),

          (try_begin),
            (eq, ":nearest_runner", -1),
            (assign, ":nearest_runner", ":enemy_agent"),

          (else_try),
            (agent_get_position, pos0, ":enemy_agent"),
            (get_distance_between_positions, ":new_distance", pos0, pos1),
            (agent_get_position, pos0, ":nearest_runner"),
            (get_distance_between_positions, ":old_distance", pos0, pos1),
            (lt, ":new_distance", ":old_distance"),
            (assign, ":nearest_runner", ":enemy_agent"),
          (try_end),

          (agent_slot_eq, ":enemy_agent", slot_agent_is_running_away, 0),

          (try_begin),
            (agent_get_slot, ":closest_enemy", ":cur_agent", slot_agent_nearest_enemy_agent),
            (eq, ":closest_enemy", -1),
            (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, ":enemy_agent"),

          (else_try),
            (agent_get_position, pos0, ":enemy_agent"),
            (get_distance_between_positions, ":new_distance", pos0, pos1),
            (agent_get_position, pos0, ":closest_enemy"),
            (get_distance_between_positions, ":old_distance", pos0, pos1),
            (lt, ":new_distance", ":old_distance"),
            (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, ":enemy_agent"),
          (try_end),
        (try_end),
        (try_begin),
          (agent_slot_eq, ":cur_agent", slot_agent_nearest_enemy_agent, -1),
          (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, ":nearest_runner"),
        (try_end),

        #exploit closest agent data
        (try_begin),
          (agent_get_slot, ":closest_enemy", ":cur_agent", slot_agent_nearest_enemy_agent),
          (neq, ":closest_enemy", -1),
          (agent_get_position, pos0, ":closest_enemy"),
          (get_distance_between_positions, ":closest_distance", pos0, pos1),

          #check target of AI agent behavior
          (try_begin),
            (agent_is_non_player, ":cur_agent"),

            (agent_ai_get_behavior_target, ":cur_targeted_agent", ":cur_agent"),
            (neq, ":closest_enemy", ":cur_targeted_agent"),

            (this_or_next | neg | agent_is_non_player, ":closest_enemy"),	#AI can always sense player behind them (balancing factor, dedicated to
            #Idibil)
            (neg | position_is_behind_position, pos0, pos1),

            (lt, ":closest_distance", 2000),	#Assuming rethink is expensive, don't bother beyond 20m

            (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (this_or_next | eq, formation_rethink_for_formations_only, 0),
            (gt, ":value", formation_none),

            (agent_force_rethink, ":cur_agent"),
          (try_end),

          #update division information
          (try_begin),
            (ge, ":bgdivision", 0),	#not leaders

            (try_begin),
              (lt, ":closest_distance", 350),
              (agent_get_division, reg0, ":closest_enemy"),
              (store_add, ":slot", slot_team_d0_enemy_supporting_melee, reg0),
              (agent_get_group, reg0, ":closest_enemy"),
              (team_get_slot, ":value", reg0, ":slot"),
              (val_add, ":value", 1),
              (team_set_slot, reg0, ":slot", ":value"),
            (try_end),

            (store_add, ":slot", slot_team_d0_closest_enemy_dist, ":bgdivision"),
            (team_get_slot, ":old_distance", ":bgteam", ":slot"),
            (try_begin),
              (this_or_next | eq, ":old_distance", 0),
              (lt, ":closest_distance", ":old_distance"),
              (team_set_slot, ":bgteam", ":slot", ":closest_distance"),
              (store_add, ":slot", slot_team_d0_closest_enemy, ":bgdivision"),
              (team_set_slot, ":bgteam", ":slot", ":closest_enemy"),
            (try_end),

            (assign, ":doit", 0),
            (agent_get_class, ":enemy_agent_class", ":closest_enemy"),
            (store_add, ":slot", slot_team_d0_type, ":bgdivision"),
            (team_get_slot, ":value", ":bgteam", ":slot"),

            #AI infantry division tracks non-infantry to preferably chase
            (try_begin),
              (this_or_next | eq, ":value", sdt_polearm),
              (eq, ":value", sdt_infantry),
              (neq, ":enemy_agent_class", grc_cavalry),
              (assign, ":doit", 1),

              #AI archer division tracks infantry to avoid
            (else_try),
              (this_or_next | eq, ":value", sdt_archer),
              (eq, ":value", sdt_skirmisher),
              (eq, ":enemy_agent_class", grc_infantry),
              (assign, ":doit", 1),
            (try_end),

            (eq, ":doit", 1),
            (store_add, ":slot", slot_team_d0_closest_enemy_special_dist, ":bgdivision"),
            (team_get_slot, ":old_distance", ":bgteam", ":slot"),
            (try_begin),
              (this_or_next | eq, ":old_distance", 0),
              (lt, ":closest_distance", ":old_distance"),
              (team_set_slot, ":bgteam", ":slot", ":closest_distance"),
              (store_add, ":slot", slot_team_d0_closest_enemy_special, ":bgdivision"),
              (team_set_slot, ":bgteam", ":slot", ":closest_enemy"),
            (try_end),
          (try_end),	#update division info
        (try_end),	#exploit closest agent data
      (try_end), #Agent Loop

      #calculate team sizes, sum positions; within calculate battle group averages
      (try_for_range, ":team", 0, 4),
        (assign, ":team_size", 0),
        (assign, ":team_level", 0),
        (assign, ":team_x", 0),
        (assign, ":team_y", 0),
        (assign, ":team_zrot", 0),

        (try_for_range, ":division", 0, 9),
          #sum for team averages
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_get_slot, ":division_size", ":team", ":slot"),
          (gt, ":division_size", 0),
          (val_add, ":team_size", ":division_size"),

          (store_add, ":slot", slot_team_d0_level, ":division"),
          (team_get_slot, ":division_level", ":team", ":slot"),
          (val_add, ":team_level", ":division_level"),

          (store_add, ":slot", slot_team_d0_avg_x, ":division"),
          (team_get_slot, ":division_x", ":team", ":slot"),
          (val_add, ":team_x", ":division_x"),

          (store_add, ":slot", slot_team_d0_avg_y, ":division"),
          (team_get_slot, ":division_y", ":team", ":slot"),
          (val_add, ":team_y", ":division_y"),

          (store_add, ":slot", slot_team_d0_avg_zrot, ":division"),
          (team_get_slot, ":division_zrot", ":team", ":slot"),
          (val_add, ":team_zrot", ":division_zrot"),

          #calculate battle group averages
          (store_add, ":slot", slot_team_d0_level, ":division"),
          (val_div, ":division_level", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_level"),

          (store_add, ":slot", slot_team_d0_percent_ranged, ":division"),
          (team_get_slot, ":value", ":team", ":slot"),
          (val_mul, ":value", 100),
          (val_div, ":value", ":division_size"),
          (team_set_slot, ":team", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_percent_throwers, ":division"),
          (team_get_slot, ":value", ":team", ":slot"),
          (val_mul, ":value", 100),
          (val_div, ":value", ":division_size"),
          (team_set_slot, ":team", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_weapon_length, ":division"),
          (team_get_slot, ":value", ":team", ":slot"),
          (val_div, ":value", ":division_size"),
          (team_set_slot, ":team", ":slot", ":value"),

          # (store_add, ":slot", slot_team_d0_swung_weapon_length, ":division"), MOTO
          # systematic testing shows best to use max swung weapon length as basis for
          # formation spacing
          # (team_get_slot, ":value", ":team", ":slot"),
          # (val_div, ":value", ":division_size"),
          # (team_set_slot, ":team", ":slot", ":value"),

          # (store_add, ":slot", slot_team_d0_front_agents, ":division"), MOTO front
          # rank should be within shortest weapon distance, not average
          # (team_get_slot, reg0, ":team", ":slot"),
          # (try_begin),
          # (gt, reg0, 0),
          # (store_add, ":slot", slot_team_d0_front_weapon_length, ":division"),
          # (team_get_slot, ":value", ":team", ":slot"),
          # (val_div, ":value", reg0),
          # (team_set_slot, ":team", ":slot", ":value"),
          # (try_end),

          (store_add, ":slot", slot_team_d0_avg_x, ":division"),
          (val_div, ":division_x", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_x"),

          (store_add, ":slot", slot_team_d0_avg_y, ":division"),
          (val_div, ":division_y", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_y"),

          (store_add, ":slot", slot_team_d0_avg_zrot, ":division"),
          (val_div, ":division_zrot", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_zrot"),

          (store_add, ":slot", slot_team_d0_type, ":division"),
          (team_get_slot, reg0, ":team", ":slot"),
          (try_begin),
            (neg | is_between, reg0, 0, 8),	#TODO reset on reinforcements
            (call_script, "script_store_battlegroup_type", ":team", ":division"),
          (try_end),
        (try_end), #Division Loop

        #Team Leader Additions
        (try_begin),
          (eq, ":team", 0),
          (val_add, ":team_size", ":team0_leader"),
          (val_add, ":team_level", ":team0_level_leader"),
          (val_add, ":team_x", ":team0_x_leader"),
          (val_add, ":team_y", ":team0_y_leader"),
          (val_add, ":team_zrot", ":team0_zrot_leader"),
        (else_try),
          (eq, ":team", 1),
          (val_add, ":team_size", ":team1_leader"),
          (val_add, ":team_level", ":team1_level_leader"),
          (val_add, ":team_x", ":team1_x_leader"),
          (val_add, ":team_y", ":team1_y_leader"),
          (val_add, ":team_zrot", ":team1_zrot_leader"),
        (else_try),
          (eq, ":team", 2),
          (val_add, ":team_size", ":team2_leader"),
          (val_add, ":team_level", ":team2_level_leader"),
          (val_add, ":team_x", ":team2_x_leader"),
          (val_add, ":team_y", ":team2_y_leader"),
          (val_add, ":team_zrot", ":team2_zrot_leader"),
        (else_try),
          (eq, ":team", 3),
          (val_add, ":team_size", ":team3_leader"),
          (val_add, ":team_level", ":team3_level_leader"),
          (val_add, ":team_x", ":team3_x_leader"),
          (val_add, ":team_y", ":team3_y_leader"),
          (val_add, ":team_zrot", ":team3_zrot_leader"),
        (try_end),

        #calculate team averages
        (gt, ":team_size", 0),
        (team_set_slot, ":team", slot_team_size, ":team_size"),
        (val_div, ":team_level", ":team_size"),
        (team_set_slot, ":team", slot_team_level, ":team_level"),

        (val_div, ":team_x", ":team_size"),
        (team_set_slot, ":team", slot_team_avg_x, ":team_x"),
        (val_div, ":team_y", ":team_size"),
        (team_set_slot, ":team", slot_team_avg_y, ":team_y"),
        (val_div, ":team_zrot", ":team_size"),
        (team_set_slot, ":team", slot_team_avg_zrot, ":team_zrot"),
      (try_end), #Team Loop
  ])
]
