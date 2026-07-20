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

mini_map = ("mini_map", prsntf_read_only, 0, [
    (ti_on_presentation_load,
     [
      (set_fixed_point_multiplier, 1000),

      (create_mesh_overlay, reg0, "mesh_white_plane"),
      (position_set_x, pos1, 1200),
      (position_set_y, pos1, 800),
      (overlay_set_position, reg0, pos1),

      (try_begin),
        (ge, "$g_minimap_style", 1), # old style
        (try_for_agents, ":agent_no"),
          (agent_set_slot, ":agent_no", slot_agent_map_overlay_id, 0),
        (try_end),

        (get_scene_boundaries, pos2, pos3),
        (position_transform_position_to_local, pos4, pos2, pos3),
        (set_fixed_point_multiplier, 1000),
        (position_get_x, ":map_width", pos4),
        (position_get_y, ":map_height", pos4),
        (set_fixed_point_multiplier, 1000),
        (store_div, ":map_ratio", ":map_height", 100),
        (store_div, ":map_ratio", ":map_width", ":map_ratio"),
        (assign, ":minimap_ratio", 100),
        (try_begin),
          (eq, "$g_minimap_style", 1),
          (assign, ":minimap_ratio", 60),
        (else_try),
          (eq, "$g_minimap_style", 2),
          (assign, ":minimap_ratio", 80),
        (try_end),
        (try_begin),
          (gt, ":map_ratio", 100),
          (store_mul, "$g_battle_map_width", ":minimap_ratio", 3),
          (store_div, "$g_battle_map_scale", ":map_width", "$g_battle_map_width"),
          (store_div, "$g_battle_map_height", ":map_height", "$g_battle_map_scale"),
        (else_try),
          (store_mul, "$g_battle_map_height", ":minimap_ratio", 3),
          (store_div, "$g_battle_map_scale", ":map_height", "$g_battle_map_height"),
          (store_div, "$g_battle_map_width", ":map_width", "$g_battle_map_scale"),
        (try_end),

        (create_mesh_overlay, "$g_battle_map_plane", "mesh_white_plane"),
        (overlay_set_color, "$g_battle_map_plane", 0),
        (store_add, ":map_bordered_width", "$g_battle_map_width", 20),
        (store_add, ":map_bordered_height", "$g_battle_map_height", 20),
        (store_mul, ":map_scale_x", ":map_bordered_width", 50),
        (store_mul, ":map_scale_y", ":map_bordered_height", 50),
        (position_set_x, pos1, ":map_scale_x"),
        (position_set_y, pos1, ":map_scale_y"),
        (overlay_set_size, "$g_battle_map_plane", pos1),
        (store_sub, ":map_pos_x", 990, ":map_bordered_width"),
        (store_sub, ":map_pos_y", 740, ":map_bordered_height"),
        (position_set_x, pos1, ":map_pos_x"),
        (position_set_y, pos1, ":map_pos_y"),
        (overlay_set_position, "$g_battle_map_plane", pos1),
        (overlay_set_alpha, "$g_battle_map_plane", 0x22),

        ## show player chest
        (try_begin),
          (scene_prop_get_instance, ":player_chest", "spr_inventory", 0),
          (ge, ":player_chest", 0),
          (create_mesh_overlay, "$g_player_chest_overlay", "mesh_white_plane"),
          (overlay_set_color, "$g_player_chest_overlay", 0xFF00FF),
          (position_set_x, pos1, 250),
          (position_set_y, pos1, 250),
          (overlay_set_size, "$g_player_chest_overlay", pos1),
        (try_end),
      (try_end),

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

      # update
      (call_script, "script_update_order_panel_map"),

      ## hp bar
      (try_for_agents, ":agent_no"),
        (agent_set_slot, ":agent_no", slot_agent_hp_bar_overlay_id, 0),
        (agent_set_slot, ":agent_no", slot_agent_hp_bar_bg_overlay_id, 0),
        #(agent_set_slot, ":agent_no", slot_agent_name_overlay_id, 0),
      (try_end),
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
     ]),
    (ti_on_presentation_run,
     [
      #(set_fixed_point_multiplier, 1000)
      #Troop Ratio Bar
      #End Troop Ratio Bar
      (set_fixed_point_multiplier, 1000),
      #Troop Ratio Bar
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
      (try_begin),
        (game_key_clicked, gk_view_orders),
        (presentation_set_duration, 0),
        (start_presentation, "prsnt_battle"),
      (try_end),
     ]),
  ])
