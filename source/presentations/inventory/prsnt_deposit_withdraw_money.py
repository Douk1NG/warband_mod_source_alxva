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

deposit_withdraw_money = ("deposit_withdraw_money", 0, 0, [
    (ti_on_presentation_load,
      [ (set_show_messages, 0),
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
        # (call_script, "script_get_chest_troop", "$current_town"),
        # (assign, ":chest_troop", reg0),
        (store_troop_gold, ":account_money", "$pool_troop"),
        (store_troop_gold, ":player_money", "trp_player"),

        (create_mesh_overlay, reg0, "mesh_message_window"),
        (position_set_x, pos1, 224),
        (position_set_y, pos1, 230),
        (overlay_set_position, reg0, pos1),

        #string qualifiers
        (try_begin),
          (eq, "$pool_troop", "trp_household_possessions"),
          (assign, reg5, 1),
        (else_try),
          (assign, reg5, 0),
        (try_end),
        (assign, reg6, ":account_money"),
        (create_text_overlay, reg0, "@{reg6}^money in the {reg5?treasury:chest}", tf_center_justify|tf_vertical_align_center),
        (position_set_x, pos1, 370),
        (position_set_y, pos1, 320),
        (overlay_set_position, reg0, pos1),

        (assign, reg4, ":player_money"),
        (create_text_overlay, reg0, "@{reg4}^money in your inventory", tf_center_justify|tf_vertical_align_center),
        (position_set_x, pos1, 630),
        (position_set_y, pos1, 320),
        (overlay_set_position, reg0, pos1),

        (create_combo_button_overlay, "$g_presentation_obj_1"),
        (position_set_x, pos1, 480),
        (position_set_y, pos1, 380),
        (overlay_set_position, "$g_presentation_obj_1", pos1),
        (position_set_x, pos1, 800),
        (position_set_y, pos1, 800),
        (overlay_set_size, "$g_presentation_obj_1", pos1),
        (overlay_add_item, "$g_presentation_obj_1", "@Withdraw"),
        (overlay_add_item, "$g_presentation_obj_1", "@Deposit"),
        (overlay_set_val, "$g_presentation_obj_1", 1),

        (position_set_x, pos1, 600),
        (position_set_y, pos1, 380),
        (val_add, ":player_money", 1),
        (create_number_box_overlay, "$g_presentation_obj_2", 0, ":player_money"),
        (overlay_set_position, "$g_presentation_obj_2", pos1),
        (overlay_set_val, "$g_presentation_obj_2", 0),
        (overlay_set_display, "$g_presentation_obj_2", 1),
        (val_add, ":account_money", 1),
        (create_number_box_overlay, "$g_presentation_obj_3", 0, ":account_money"),
        (overlay_set_position, "$g_presentation_obj_3", pos1),
        (overlay_set_val, "$g_presentation_obj_3", 0),
        (overlay_set_display, "$g_presentation_obj_3", 0),

        (create_game_button_overlay, "$g_presentation_obj_5", "str_done"),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 250),
        (overlay_set_position, "$g_presentation_obj_5", pos1),
      ]),

   #crashes when you access inventory, see if we can skip out
   (ti_on_presentation_run,
    [
        (try_begin),
          (this_or_next|game_key_clicked, gk_inventory_window),
          (this_or_next|game_key_clicked, gk_character_window),
          (game_key_clicked, gk_action),
          (presentation_set_duration, 0),
        (try_end),
   ]),
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_1"),
          (try_begin),
            (eq, ":value", 1),
            (overlay_set_display, "$g_presentation_obj_2", 1),
            (overlay_set_display, "$g_presentation_obj_3", 0),
          (else_try),
            (overlay_set_display, "$g_presentation_obj_2", 0),
            (overlay_set_display, "$g_presentation_obj_3", 1),
          (try_end),
        (else_try),
          (this_or_next|eq, ":object", "$g_presentation_obj_2"),
          (eq, ":object", "$g_presentation_obj_3"),
          (gt, ":value", 0),
          # (call_script, "script_get_chest_troop", "$current_town"),
          # (assign, ":chest_troop", reg0),
          (try_begin),
            (eq, ":object", "$g_presentation_obj_2"),
            (troop_remove_gold, "trp_player",":value"),
            (troop_add_gold, "$pool_troop", ":value"),
          (else_try),
            (eq, ":object", "$g_presentation_obj_3"),
            (troop_remove_gold, "$pool_troop",":value"),
            (troop_add_gold, "trp_player", ":value"),
          (try_end),
          (start_presentation, "prsnt_deposit_withdraw_money"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_5"),
          (set_show_messages, 1),
          (presentation_set_duration, 0),
        (try_end),
    ]),
  ])
