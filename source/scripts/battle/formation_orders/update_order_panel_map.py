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

update_order_panel_map_scripts = [
# script_update_order_panel_statistics_and_map
# Input: none
# Output: none
("update_order_panel_map",
   [
    (set_fixed_point_multiplier, 1000),

    (get_scene_boundaries, pos2, pos3),
    (try_begin),
      (ge, "$g_minimap_style", 1), # old style
      (try_for_agents,":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_slot, ":agent_overlay", ":cur_agent", slot_agent_map_overlay_id),
        (try_begin),
          (agent_is_alive, ":cur_agent"),
          (call_script, "script_update_agent_position_on_map", ":cur_agent"),
        (else_try),
          (overlay_set_alpha, ":agent_overlay", 0),
        (try_end),
      (try_end),
      # player_chest
      (try_begin),
        (scene_prop_get_instance, ":player_chest", "spr_inventory", 0),
        (ge, ":player_chest", 0),
        (prop_instance_get_position, pos1, ":player_chest"),
        (call_script, "script_convert_3d_pos_to_map_pos"),
        (overlay_set_position, "$g_player_chest_overlay", pos0),
        (overlay_set_alpha, "$g_player_chest_overlay", 0xFF),
      (else_try),
        (overlay_set_alpha, "$g_player_chest_overlay", 0),
      (try_end),
    (try_end),

    # Horse Stamina
    #(get_player_agent_no, ":player_agent"),
    #(agent_get_horse, ":horse_agent", ":player_agent"),
    #(try_begin),
    #  (eq, "$g_horse_charging_for_player", 1),
    #  (ge, ":horse_agent", 0),
    #  (agent_get_slot, ":horse_stamina", ":player_agent", slot_agent_horse_stamina),
    #  (store_agent_hit_points, ":horse_hp", ":horse_agent"),
    #  (assign, reg1, ":horse_stamina"),
    #  (assign, reg2, ":horse_hp"),
    #  (overlay_set_text, "$g_horse_stamina_overlay", "@Horse Stamina: {reg1}/{reg2}"),
    #  (overlay_set_alpha, "$g_horse_stamina_overlay", 0xFF),
    #(else_try),
    #  (overlay_set_alpha, "$g_horse_stamina_overlay", 0),
    #(try_end),
  ])
]
