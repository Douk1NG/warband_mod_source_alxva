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

battlegroup_place_around_pos1_scripts = [
("battlegroup_place_around_pos1", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),

      (assign, ":store_fpm", 1),
      (convert_to_fixed_point, ":store_fpm"),
      (set_fixed_point_multiplier, 100),

      (store_sub, ":player_division", "$FormAI_player_in_division", 1),
      (try_begin),
        (eq, ":player_division", ":fdivision"),
        (assign, ":first_member_is_player", 1),
      (else_try),
        (assign, ":first_member_is_player", 0),
      (try_end),

      (try_begin),
        (eq, "$FormAI_autorotate", 1),
        (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, ":fteam", grc_everyone),
        (neq, reg0, 0),	#more than 0 enemies still alive?
        (call_script, "script_point_y_toward_position", pos1, Enemy_Team_Pos),
      (try_end),

      (store_add, ":slot", slot_team_d0_type, ":fdivision"),
      (team_get_slot, ":sd_type", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_size, ":fdivision"),
      (team_get_slot, ":num_troops", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation, ":fdivision"),
      (team_get_slot, ":fformation", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation_space, ":fdivision"),
      (team_get_slot, ":formation_extra_spacing", ":fteam", ":slot"),

      #handle memorized placement
      (try_begin),
        (eq, ":first_member_is_player", 0),
        (store_add, ":slot", slot_faction_d0_mem_relative_x_flag, ":fdivision"),
        (faction_get_slot, ":value", "fac_player_faction", ":slot"),	#only used for player now
        (neq, ":value", 0),

        (position_move_x, pos1, ":value", 0),
        (store_add, ":slot", slot_faction_d0_mem_relative_y, ":fdivision"),
        (faction_get_slot, ":value", "fac_player_faction", ":slot"),	#only used for player now
        (position_move_y, pos1, ":value", 0),
        (copy_position, pos61, pos1),
        (try_begin),
          (gt, ":fformation", formation_none),
          (try_begin),
            (this_or_next | eq, ":sd_type", sdt_cavalry),
            (eq, ":sd_type", sdt_harcher),
            (call_script, "script_form_cavalry", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", 0),
          (else_try),
            (eq, ":sd_type", sdt_archer),
            (call_script, "script_get_centering_amount", formation_default, ":num_troops", ":formation_extra_spacing"),
            (val_mul, reg0, -1),
            (position_move_x, pos1, reg0, 0),
            (call_script, "script_form_archers", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", 0, ":fformation"),
          (else_try),
            (call_script, "script_get_centering_amount", ":fformation", ":num_troops", ":formation_extra_spacing"),
            (position_move_x, pos1, reg0, 0),
            (call_script, "script_form_infantry", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", 0, ":fformation"),
          (try_end),
        (try_end),

      #default placement per division type
      (else_try),
        (this_or_next | eq, ":sd_type", sdt_cavalry),
        (eq, ":sd_type", sdt_harcher),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_x, pos1, "$next_cavalry_place", 0),
        (try_end),

        (try_begin),
          (gt, ":fformation", formation_none),
          (store_mul, ":troop_space", ":formation_extra_spacing", 50),
          (val_add, ":troop_space", formation_minimum_spacing_horse_width),
          (convert_to_fixed_point, ":num_troops"),
          (store_sqrt, ":formation_width", ":num_troops"),
          (val_mul, ":formation_width", ":troop_space"),
          (convert_from_fixed_point, ":formation_width"),
          (val_sub, ":formation_width", ":troop_space"),
          (store_div, reg0, ":formation_width", 2),
          (position_move_x, pos1, reg0, 0),	#cavalry set up RIGHT of leader
          (copy_position, pos61, pos1),
          (call_script, "script_form_cavalry", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player"),

        #handle Native's way of doing things
        (else_try),
          (store_mul, ":troop_space", ":formation_extra_spacing", 133),	#cm added by each Spread Out
          (val_add, ":troop_space", 150),	#minimum spacing

          #WFaS multi-ranks
          (try_begin),
            (eq, ":fformation", formation_2_row),
            (val_div, ":num_troops", 2),
          (else_try),
            (eq, ":fformation", formation_3_row),
            (val_div, ":num_troops", 3),
          (else_try),
            (eq, ":fformation", formation_4_row),
            (val_div, ":num_troops", 4),
          (else_try),
            (eq, ":fformation", formation_5_row),
            (val_div, ":num_troops", 5),

          (else_try),	#WB multi-ranks
            (lt, ":formation_extra_spacing", 0),
            (assign, ":troop_space", 200),
            (val_mul, ":formation_extra_spacing", -1),
            (val_add, ":formation_extra_spacing", 1),
            (val_div, ":num_troops", ":formation_extra_spacing"),
          (try_end),

          (store_mul, ":formation_width", ":num_troops", ":troop_space"),
          (store_div, reg0, ":formation_width", 2),
          (position_move_x, pos1, reg0, 0),	#cavalry set up RIGHT of leader
          (copy_position, pos61, pos1),
        (try_end),

        (try_begin),
          (eq, ":first_member_is_player", 0),
          (val_add, "$next_cavalry_place", ":formation_width"),
          (val_add, "$next_cavalry_place", formation_minimum_spacing_horse_width),
        (try_end),

      (else_try),
        (eq, ":sd_type", sdt_archer),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_y, pos1, "$next_archer_place"),	#archers set up FRONT of leader
          (val_add, "$next_archer_place", 500),	#next archers 5m FRONT of these
        (try_end),
        (copy_position, pos61, pos1),
        (try_begin),
          (gt, ":fformation", formation_none),
          (call_script, "script_get_centering_amount", formation_default, ":num_troops", ":formation_extra_spacing"),
          (val_mul, reg0, -1),
          (position_move_x, pos1, reg0, 0),
          (call_script, "script_form_archers", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player", ":fformation"),
        (try_end),

      (else_try),
        (eq, ":sd_type", sdt_skirmisher),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_y, pos1, "$next_archer_place"),	#skirmishers set up FRONT of leader
          (val_add, "$next_archer_place", 500),	#next archers 5m FRONT of these
        (try_end),
        (copy_position, pos61, pos1),
        (try_begin),
          (gt, ":fformation", formation_none),
          (call_script, "script_get_centering_amount", ":fformation", ":num_troops", ":formation_extra_spacing"),
          (position_move_x, pos1, reg0, 0),
          (call_script, "script_form_infantry", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player", ":fformation"),
        (try_end),

      (else_try),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_x, pos1, "$next_infantry_place", 0),
        (try_end),
        (copy_position, pos61, pos1),

        (try_begin),
          (gt, ":fformation", formation_none),
          (call_script, "script_form_infantry", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player", ":fformation"),
          (call_script, "script_get_centering_amount", ":fformation", ":num_troops", ":formation_extra_spacing"),
          (store_mul, ":formation_width", 2, reg0),
          (store_mul, ":troop_space", ":formation_extra_spacing", 50),
          (val_add, ":troop_space", formation_minimum_spacing),
          (val_add, ":formation_width", ":troop_space"),
          (val_mul, reg0, -1),	#infantry set up LEFT of leader
          (position_move_x, pos61, reg0, 0),

        #handle Native's way of doing things
        (else_try),
          (store_mul, ":troop_space", ":formation_extra_spacing", 75),	#Native minimum spacing not consistent but less than this
          (val_add, ":troop_space", 100),	#minimum spacing

          #WFaS multi-ranks
          (try_begin),
            (eq, ":fformation", formation_2_row),
            (val_div, ":num_troops", 2),
          (else_try),
            (eq, ":fformation", formation_3_row),
            (val_div, ":num_troops", 3),
          (else_try),
            (eq, ":fformation", formation_4_row),
            (val_div, ":num_troops", 4),
          (else_try),
            (eq, ":fformation", formation_5_row),
            (val_div, ":num_troops", 5),

          (else_try),	#WB multi-ranks
            (lt, ":formation_extra_spacing", 0),
            (assign, ":troop_space", 150),
            (val_mul, ":formation_extra_spacing", -1),
            (val_add, ":formation_extra_spacing", 1),
            (val_div, ":num_troops", ":formation_extra_spacing"),
          (try_end),

          (store_mul, ":formation_width", ":num_troops", ":troop_space"),
          (store_div, reg0, ":formation_width", 2),
          (val_mul, reg0, -1),	#infantry set up LEFT of leader
          (position_move_x, pos61, reg0, 0),
        (try_end),

        (try_begin),
          (eq, ":first_member_is_player", 0),
          (val_sub, "$next_infantry_place", ":formation_width"),	#next infantry 1m LEFT of these
          (val_sub, "$next_infantry_place", 100),
        (try_end),
      (try_end),

      (store_add, ":slot", slot_team_d0_move_order, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", mordr_hold),
      (set_show_messages, 0),
      (team_get_movement_order, reg0, ":fteam", ":fdivision"),
      (try_begin),
        (neq, reg0, mordr_hold),
        (team_give_order, ":fteam", ":fdivision", mordr_hold),
      (try_end),
      (call_script, "script_set_formation_destination", ":fteam", ":fdivision", pos61),
      (set_show_messages, 1),
      (set_fixed_point_multiplier, ":store_fpm"),])
]
