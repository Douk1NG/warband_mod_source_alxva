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

spawn_diagnostics = ("spawn_diagnostics", 0, mesh_load_window,
    [(ti_on_presentation_load,
      [
       (presentation_set_duration, 999999),
       (set_fixed_point_multiplier, 1000),

       (create_mesh_overlay, reg1, "mesh_pic_payment"),
       (position_set_x, pos1, 800),
       (position_set_y, pos1, 800),
       (overlay_set_size, reg1, pos1),
       (position_set_x, pos1, 170),
       (position_set_y, pos1, 0),
       (overlay_set_position, reg1, pos1),

       (create_text_overlay, reg1, "@Spawn / World-AI Diagnostics (update 010)", tf_center_justify),
       (position_set_x, pos1, 1500),
       (position_set_y, pos1, 1500),
       (overlay_set_size, reg1, pos1),
       (position_set_x, pos1, 260),
       (position_set_y, pos1, 660),
       (overlay_set_position, reg1, pos1),

       (create_text_overlay, reg1, "@active/cap  -  next = hours until next party spawns  -  lair = lair active (1/0)", tf_single_line),
       (position_set_x, pos1, 10),
       (position_set_y, pos1, 622),
       (overlay_set_position, reg1, pos1),

       (str_clear, s0),
       (create_text_overlay, "$g_presentation_obj_spawn_diag_container", s0, tf_scrollable_style_2),
       (position_set_x, pos1, 0),
       (position_set_y, pos1, 100),
       (overlay_set_position, "$g_presentation_obj_spawn_diag_container", pos1),
       (position_set_x, pos1, 505),
       (position_set_y, pos1, 500),
       (overlay_set_area_size, "$g_presentation_obj_spawn_diag_container", pos1),
       (set_container_overlay, "$g_presentation_obj_spawn_diag_container"),

       (assign, ":cur_y", 25),

       (create_text_overlay, reg1, "@-- Land bandits (lair-linked, cap 18) --", 0),
       (position_set_x, pos1, 25),
       (position_set_y, pos1, ":cur_y"),
       (overlay_set_position, reg1, pos1),
       (val_add, ":cur_y", 22),

       (str_store_string, s1, "@Mountain Bandits"),
       (call_script, "script_get_spawn_report_line", "pt_mountain_bandits", 18, 1),
       (str_store_string, s2, "@{s1}: {s0}"),
       (create_text_overlay, reg1, s2, 0),
       (position_set_x, pos1, 25),
       (position_set_y, pos1, ":cur_y"),
       (overlay_set_position, reg1, pos1),
       (val_add, ":cur_y", 22),

       (str_store_string, s1, "@Forest Bandits"),
       (call_script, "script_get_spawn_report_line", "pt_forest_bandits", 18, 1),
       (str_store_string, s2, "@{s1}: {s0}"),
       (create_text_overlay, reg1, s2, 0),
       (position_set_x, pos1, 25),
       (position_set_y, pos1, ":cur_y"),
       (overlay_set_position, reg1, pos1),
       (val_add, ":cur_y", 22),

       (str_store_string, s1, "@Sea Raiders (land)"),
       (call_script, "script_get_spawn_report_line", "pt_sea_raiders", 18, 1),
       (str_store_string, s2, "@{s1}: {s0}"),
       (create_text_overlay, reg1, s2, 0),
       (position_set_x, pos1, 25),
       (position_set_y, pos1, ":cur_y"),
       (overlay_set_position, reg1, pos1),
       (val_add, ":cur_y", 22),

       (str_store_string, s1, "@Steppe Bandits"),
       (call_script, "script_get_spawn_report_line", "pt_steppe_bandits", 18, 1),
       (str_store_string, s2, "@{s1}: {s0}"),
       (create_text_overlay, reg1, s2, 0),
       (position_set_x, pos1, 25),
       (position_set_y, pos1, ":cur_y"),
       (overlay_set_position, reg1, pos1),
       (val_add, ":cur_y", 22),

       (str_store_string, s1, "@Taiga Bandits"),
       (call_script, "script_get_spawn_report_line", "pt_taiga_bandits", 18, 1),
       (str_store_string, s2, "@{s1}: {s0}"),
       (create_text_overlay, reg1, s2, 0),
       (position_set_x, pos1, 25),
       (position_set_y, pos1, ":cur_y"),
       (overlay_set_position, reg1, pos1),
       (val_add, ":cur_y", 22),

       (str_store_string, s1, "@Desert Bandits"),
       (call_script, "script_get_spawn_report_line", "pt_desert_bandits", 18, 1),
       (str_store_string, s2, "@{s1}: {s0}"),
       (create_text_overlay, reg1, s2, 0),
       (position_set_x, pos1, 25),
       (position_set_y, pos1, ":cur_y"),
       (overlay_set_position, reg1, pos1),
       (val_add, ":cur_y", 22),

       (create_text_overlay, reg1, "@-- Looters (cap 42) --", 0),
       (position_set_x, pos1, 25),
       (position_set_y, pos1, ":cur_y"),
       (overlay_set_position, reg1, pos1),
       (val_add, ":cur_y", 22),

       (str_store_string, s1, "@Looters"),
       (call_script, "script_get_spawn_report_line", "pt_looters", 18, 0),
       (str_store_string, s2, "@{s1}: {s0}"),
       (create_text_overlay, reg1, s2, 0),
       (position_set_x, pos1, 25),
       (position_set_y, pos1, ":cur_y"),
       (overlay_set_position, reg1, pos1),
       (val_add, ":cur_y", 22),

        (create_text_overlay, reg1, "@-- Pirate ships (one type: total cap 5, size <=15) --", 0),
        (position_set_x, pos1, 25),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (val_add, ":cur_y", 22),

        (store_num_parties_of_template, ":ns1", "pt_sea_raiders_ship"),
        (store_num_parties_of_template, ":ns2", "pt_corsair_ship"),
        (store_num_parties_of_template, ":ns3", "pt_pirate_ship"),
        (store_add, ":ns_total", ":ns1", ":ns2"),
        (val_add, ":ns_total", ":ns3"),
        (assign, reg1, ":ns_total"),
        (assign, reg2, num_max_pirate_ships),
        (assign, reg3, ":ns1"),
        (assign, reg4, ":ns2"),
        (assign, reg5, ":ns3"),
        (str_store_string, s0, "@Pirate ships total: {reg1}/{reg2}   (raiders {reg3} / corsair {reg4} / pirate {reg5})"),
        (create_text_overlay, reg1, s0, 0),
        (position_set_x, pos1, 25),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg1, pos1),
        (val_add, ":cur_y", 22),


        (store_num_parties_of_template, ":num_mh", "pt_manhunters"),
        (assign, ":num_bandits", 0),
        (try_for_range, ":bt", bandit_party_templates_begin, bandit_party_templates_end),
          (store_num_parties_of_template, ":n", ":bt"),
          (val_add, ":num_bandits", ":n"),
        (try_end),
        (store_div, ":mh_cap", ":num_bandits", manhunter_bandits_per_manhunter),
        (val_max, ":mh_cap", 4),
        (val_min, ":mh_cap", num_max_manhunters),
        (create_text_overlay, reg1, "@-- Manhunters (~2:1 with land bandits) --", 0),
       (position_set_x, pos1, 25),
       (position_set_y, pos1, ":cur_y"),
       (overlay_set_position, reg1, pos1),
       (val_add, ":cur_y", 22),
       (assign, reg1, ":num_mh"),
       (assign, reg2, ":mh_cap"),
       (assign, reg3, ":num_bandits"),
       (str_store_string, s0, "@Manhunters: {reg1}/{reg2}   (active bandits = {reg3})"),
       (create_text_overlay, reg1, s0, 0),
       (position_set_x, pos1, 25),
       (position_set_y, pos1, ":cur_y"),
       (overlay_set_position, reg1, pos1),
       (val_add, ":cur_y", 22),

       (store_num_parties_of_template, ":num_des", "pt_deserters"),
       (assign, reg1, ":num_des"),
       (str_store_string, s0, "@Deserters active: {reg1}  (party size capped at 20)"),
       (create_text_overlay, reg1, s0, 0),
       (position_set_x, pos1, 25),
       (position_set_y, pos1, ":cur_y"),
       (overlay_set_position, reg1, pos1),
       (val_add, ":cur_y", 22),

       (set_container_overlay, -1),

       (create_button_overlay, "$g_presentation_obj_spawn_diag_close", "@Close"),
       (position_set_x, pos1, 225),
       (position_set_y, pos1, 60),
       (overlay_set_position, "$g_presentation_obj_spawn_diag_close", pos1),
      ]),
     (ti_on_presentation_event_state_change,
      [(store_trigger_param_1, ":object"),
       (try_begin),
         (eq, ":object", "$g_presentation_obj_spawn_diag_close"),
         (presentation_set_duration, 0),
       (try_end),
       ]),
     ])
