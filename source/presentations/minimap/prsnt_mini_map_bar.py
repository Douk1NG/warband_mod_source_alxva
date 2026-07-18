# -*- coding: cp1254 -*-
import string
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
#SB: import skills from ID_skills import *
from module_constants import *
##diplomacy start+ Import for use with terrain advantage
from header_terrain_types import *
from module_items import *
#SB : import colors
from module_factions import *
from header_items import *
##diplomacy end
from compiler import *

mini_map_bar = ("mini_map_bar", prsntf_read_only, 0, [
    (ti_on_presentation_load,
     [
      (set_fixed_point_multiplier, 1000),

      (create_mesh_overlay, reg1, "mesh_white_plane"),
      (position_set_x, pos1, 1200),
      (position_set_y, pos1, 800),
      (overlay_set_position, reg1, pos1),

      (create_mesh_overlay, reg1, "mesh_battle_map_bar"),
      (position_set_x, pos1, 500),
      (position_set_y, pos1, 700),
      (overlay_set_position, reg1, pos1),
      (overlay_set_alpha, reg1, 0xFF),

      ## init map dot and hp bar
      (try_for_agents, ":agent_no"),
        (agent_set_slot, ":agent_no", slot_agent_map_overlay_id, 0),
        (agent_set_slot, ":agent_no", slot_agent_hp_bar_overlay_id, 0),
        (agent_set_slot, ":agent_no", slot_agent_hp_bar_bg_overlay_id, 0),
        #(agent_set_slot, ":agent_no", slot_agent_name_overlay_id, 0),
      (try_end),

      ## player chest
      (create_mesh_overlay, "$g_player_chest_overlay", "mesh_white_plane"),
      (position_set_x, pos1, 500),
      (position_set_y, pos1, 500),
      (overlay_set_size, "$g_player_chest_overlay", pos1),
      (overlay_set_color, "$g_player_chest_overlay", 0xFF00FF),
      (overlay_set_alpha, "$g_player_chest_overlay", 0),

      ## horse stamina
      (create_text_overlay, "$g_horse_stamina_overlay", "@0", tf_center_justify),
      (position_set_x, pos1, 925),
      (position_set_y, pos1, 40),
      (overlay_set_position, "$g_horse_stamina_overlay", pos1),
      (position_set_x, pos1, 600),
      (position_set_y, pos1, 600),
      (overlay_set_size, "$g_horse_stamina_overlay", pos1),
      (overlay_set_color, "$g_horse_stamina_overlay", 0xFFFFFF),
      (overlay_set_alpha, "$g_horse_stamina_overlay", 0),

      ## enemies-allies-us
      # position
      (assign, ":pos_x", 380),
      (assign, ":pos_y", 725),
      (create_text_overlay, "$g_battle_enemies_ready", s7, tf_center_justify),
      (position_set_x, pos1, ":pos_x"),
      (position_set_y, pos1, ":pos_y"),
      (overlay_set_position, "$g_battle_enemies_ready", pos1),
      (val_sub, ":pos_y", 10),
      (create_text_overlay, "$g_battle_allies_ready", s7, tf_center_justify),
      (position_set_x, pos1, ":pos_x"),
      (position_set_y, pos1, ":pos_y"),
      (overlay_set_position, "$g_battle_allies_ready", pos1),
      (val_sub, ":pos_y", 10),
      (create_text_overlay, "$g_battle_us_ready", s7, tf_center_justify),
      (position_set_x, pos1, ":pos_x"),
      (position_set_y, pos1, ":pos_y"),
      (overlay_set_position, "$g_battle_us_ready", pos1),

      # size
      (position_set_x, pos1, 600),
      (position_set_y, pos1, 600),
      (overlay_set_size, "$g_battle_enemies_ready", pos1),
      (overlay_set_size, "$g_battle_allies_ready", pos1),
      (overlay_set_size, "$g_battle_us_ready", pos1),
      # color
      (overlay_set_color, "$g_battle_enemies_ready", 0xFFFFFF),
      (overlay_set_color, "$g_battle_allies_ready", 0xFFFFFF),
      (overlay_set_color, "$g_battle_us_ready", 0xFFFFFF),

      ## update map dot and hp bar
      (call_script, "script_update_map_bar"),
      (call_script, "script_update_agent_hp_bar"),

      #Troop Ratio Bar
      (try_begin),
      (ge, "$g_troop_ratio_bar", 1),
      (assign, "$presentation_troop_ratio_bar_active", 1),
      (set_fixed_point_multiplier, 1000),
      (create_mesh_overlay, "$g_presentation_obj_1", "mesh_status_troop_ratio_bar"),
      (position_set_x, pos1, 30),
      (position_set_y, pos1, 700),
      (overlay_set_position, "$g_presentation_obj_1", pos1),
      (position_set_x, pos1, 35),
      (position_set_y, pos1, 713),
      (create_mesh_overlay, "$g_presentation_obj_2", "mesh_white_plane"),
      (overlay_set_color, "$g_presentation_obj_2", 11149087),
      (overlay_set_position, "$g_presentation_obj_2", pos1),
      (create_mesh_overlay, "$g_presentation_obj_3", "mesh_white_plane"),
      (overlay_set_color, "$g_presentation_obj_3", 2039722),
      (overlay_set_position, "$g_presentation_obj_3", pos1),
      (create_mesh_overlay, "$g_presentation_obj_4", "mesh_white_plane"),
      (overlay_set_color, "$g_presentation_obj_4", 2075167),
      (overlay_set_position, "$g_presentation_obj_4", pos1),
      (create_mesh_overlay, "$g_presentation_obj_5", "mesh_status_troop_ratio_bar_button"),
      (position_set_x, pos1, 35),
      (position_set_y, pos1, 700),
      (overlay_set_position, "$g_presentation_obj_5", pos1),
      (create_mesh_overlay, "$g_presentation_obj_6", "mesh_status_troop_ratio_bar_button"),
      (position_set_x, pos1, 275),
      (position_set_y, pos1, 700),
      (overlay_set_position, "$g_presentation_obj_6", pos1),
      (create_mesh_overlay, "$g_presentation_obj_7", "mesh_status_troop_ratio_bar_button"),
      (create_mesh_overlay, "$g_presentation_obj_8", "mesh_status_troop_ratio_bar_button"),
      (try_end),
      #End Troop Ratio Bar
      (presentation_set_duration, 999999),
      # ####### mouse fix pos system #######
      # (call_script, "script_mouse_fix_pos_ready"),
      # ####### mouse fix pos system #######
     ]),
    (ti_on_presentation_run,
     [
          #Troop Ratio Bar
           #End Troop Ratio Bar
      (set_fixed_point_multiplier, 1000),
            (try_begin),
            (ge, "$g_troop_ratio_bar", 1),
       (assign, ":var1", 0),
       (assign, ":var2", 0),
       (assign, ":var3", 0),
       (assign, ":var4", 0),
       (try_for_agents, ":var5"),
         (agent_is_human, ":var5"),
         (agent_is_alive, ":var5"),
         (agent_get_party_id, ":var6", ":var5"),
         (try_begin),
           (eq, ":var6", "p_main_party"),
           (val_add, ":var1", 1),
         (else_try),
           (agent_is_ally, ":var5"),
           (val_add, ":var2", 1),
         (else_try),
           (val_add, ":var3", 1),
         (end_try),
       (end_try),
       (val_add, ":var4", ":var1"),
       (val_add, ":var4", ":var2"),
       (val_add, ":var4", ":var3"),
       (position_set_x, pos1, 12000),
       (position_set_y, pos1, 300),
       (overlay_set_size, "$g_presentation_obj_2", pos1),
       (store_add, ":var7", ":var1", ":var2"),
       (val_mul, ":var7", 12000),
       (val_div, ":var7", ":var4"),
       (position_set_x, pos1, ":var7"),
       (position_set_y, pos1, 300),
       (overlay_set_size, "$g_presentation_obj_3", pos1),
       (store_mul, ":var8", ":var1", 12000),
       (val_div, ":var8", ":var4"),
       (position_set_x, pos1, ":var8"),
       (position_set_y, pos1, 300),
       (overlay_set_size, "$g_presentation_obj_4", pos1),
       (store_add, ":var9", ":var1", ":var2"),
       (val_mul, ":var9", 240),
       (val_div, ":var9", ":var4"),
       (val_add, ":var9", 35),
       (position_set_x, pos1, ":var9"),
       (position_set_y, pos1, 700),
       (overlay_set_position, "$g_presentation_obj_7", pos1),
       (store_mul, ":var10", ":var1", 240),
       (val_div, ":var10", ":var4"),
       (val_add, ":var10", 35),
       (position_set_x, pos1, ":var10"),
       (position_set_y, pos1, 700),
       (overlay_set_position, "$g_presentation_obj_8", pos1),
       (try_end),
       #End Troop Ratio Bar
      # ####### mouse fix pos system #######
      # (call_script, "script_mouse_fix_pos_run"),
      # ####### mouse fix pos system #######
      (try_begin),
        (game_key_clicked, gk_view_orders),
        (presentation_set_duration, 0),
        (start_presentation, "prsnt_battle"),
      (try_end),
     ]),
  ])
