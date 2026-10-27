# -*- coding: cp1254 -*-
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *

# Main Settings (XGM mod_option) shared UI - hub-aware
# Hub uses inner scrollable container 20,20,610,520 inside camp_hub's 300,0,650,1600 -> 2 bars as requested keep both
from xgm_mod_options import mod_options, ModOptionWrapper, mod_options_get_total_height
from xgm_mod_options_header import *
from util_wrappers import OpBlockWrapper

def _generate_hub_mod_options_load():
    total_height = mod_options_get_total_height()
    if total_height < 520 - xgm_mod_options_property_height/2:
        total_height = 520 - xgm_mod_options_property_height/2
    cur_posy = total_height
    cur_overlay_index = 1
    opblock = OpBlockWrapper([])
    # no inner - outer 650×1600 handles scroll, single outer bar at ~950
    for x in mod_options:
        aModOption = ModOptionWrapper(x)
        if aModOption.GetType() == xgm_ov_line:
            opblock.Append([
                (assign, ":size_x", xgm_mod_options_line_width),
                (assign, ":size_y", xgm_mod_options_line_height),
                (assign, ":pos_x", xgm_mod_options_line_posx),
                (assign, ":pos_y", cur_posy + xgm_mod_options_line_offsety),
                (create_mesh_overlay, reg1, "mesh_white_plane"),
                (val_mul, ":size_x", 50),
                (val_mul, ":size_y", 50),
                (position_set_x, pos1, ":size_x"),
                (position_set_y, pos1, ":size_y"),
                (overlay_set_size, reg1, pos1),
                (position_set_x, pos1, ":pos_x"),
                (position_set_y, pos1, ":pos_y"),
                (overlay_set_position, reg1, pos1),
                (overlay_set_color, reg1, 0x000000),
            ])
        elif aModOption.GetType() in [xgm_ov_checkbox, xgm_ov_numberbox, xgm_ov_combolabel, xgm_ov_combobutton, xgm_ov_slider]:
            labeltext = aModOption.GetTextLabel()
            if labeltext and labeltext != "":
                textflags = tf_vertical_align_center | aModOption.GetTextLabelFlags()
                opblock.Append([
                    (position_set_x, pos1, xgm_mod_options_property_label_posx),
                    (create_text_overlay, reg0, "@%s" % aModOption.GetTextLabel(), tf_vertical_align_center),
                    (position_set_y, pos1, cur_posy),
                    (overlay_set_position, reg0, pos1),
                ])
            if aModOption.GetType() == xgm_ov_numberbox:
                overlay_var = "$g_presentation_obj_%s" % cur_overlay_index
                opblock.Append([
                    (assign, overlay_var, 0),
                    (position_set_x, pos1, xgm_mod_options_property_value_posx + xgm_ov_numberbox_offsetx),
                    (create_number_box_overlay, overlay_var, aModOption.GetParameter(0), aModOption.GetParameter(1)),
                    (position_set_y, pos1, cur_posy + xgm_ov_numberbox_offsety),
                    (overlay_set_position, overlay_var, pos1),
                    (position_set_x, pos1, xgm_ov_numberbox_scalex),
                    (position_set_y, pos1, xgm_ov_numberbox_scaley),
                    (overlay_set_size, overlay_var, pos1),
                ])
                opblock.Append(aModOption.GetInitializeBlock())
                opblock.Append([(overlay_set_val, overlay_var, reg1)])
                cur_overlay_index += 1
            elif aModOption.GetType() == xgm_ov_slider:
                overlay_var = "$g_presentation_obj_%s" % cur_overlay_index
                opblock.Append([
                    (assign, overlay_var, 0),
                    (position_set_x, pos1, xgm_mod_options_property_value_posx + xgm_ov_slider_offsetx),
                    (create_slider_overlay, overlay_var, aModOption.GetParameter(0), aModOption.GetParameter(1)),
                    (position_set_y, pos1, cur_posy + xgm_ov_slider_offsety),
                    (overlay_set_position, overlay_var, pos1),
                    (position_set_x, pos1, xgm_ov_slider_scalex),
                    (position_set_y, pos1, xgm_ov_slider_scaley),
                    (overlay_set_size, overlay_var, pos1),
                ])
                opblock.Append(aModOption.GetInitializeBlock())
                opblock.Append([(overlay_set_val, overlay_var, reg1)])
                cur_overlay_index += 1
            elif aModOption.GetType() == xgm_ov_checkbox:
                overlay_var = "$g_presentation_obj_%s" % cur_overlay_index
                opblock.Append([
                    (assign, overlay_var, 0),
                    (position_set_x, pos1, xgm_mod_options_property_value_posx + xgm_ov_checkbox_offsetx),
                    (create_check_box_overlay, overlay_var, "mesh_checkbox_off", "mesh_checkbox_on"),
                    (position_set_y, pos1, cur_posy + xgm_ov_checkbox_offsety),
                    (overlay_set_position, overlay_var, pos1),
                ])
                opblock.Append(aModOption.GetInitializeBlock())
                opblock.Append([
                    (overlay_set_val, overlay_var, reg1),
                    (position_set_x, pos1, xgm_ov_checkbox_scalex),
                    (position_set_y, pos1, xgm_ov_checkbox_scaley),
                    (overlay_set_size, overlay_var, pos1),
                ])
                cur_overlay_index += 1
            elif aModOption.GetType() == xgm_ov_combolabel:
                overlay_var = "$g_presentation_obj_%s" % cur_overlay_index
                opblock.Append([
                    (assign, overlay_var, 0),
                    (position_set_x, pos1, xgm_mod_options_property_value_posx + xgm_ov_combolabel_offsetx),
                    (create_combo_label_overlay, overlay_var),
                    (position_set_y, pos1, cur_posy + xgm_ov_combolabel_offsety),
                    (overlay_set_position, overlay_var, pos1),
                    (position_set_x, pos1, xgm_ov_combolabel_scalex),
                    (position_set_y, pos1, xgm_ov_combolabel_scaley),
                    (overlay_set_size, overlay_var, pos1),
                ])
                for aComboItem in aModOption.GetParameters():
                    opblock.Append([(overlay_add_item, overlay_var, "@%s" % aComboItem)])
                opblock.Append(aModOption.GetInitializeBlock())
                opblock.Append([(overlay_set_val, overlay_var, reg1)])
                cur_overlay_index += 1
            elif aModOption.GetType() == xgm_ov_combobutton:
                overlay_var = "$g_presentation_obj_%s" % cur_overlay_index
                opblock.Append([
                    (assign, overlay_var, 0),
                    (position_set_x, pos1, xgm_mod_options_property_value_posx + xgm_ov_combobutton_offsetx),
                    (create_combo_button_overlay, overlay_var),
                    (position_set_y, pos1, cur_posy + xgm_ov_combobutton_offsety),
                    (overlay_set_position, overlay_var, pos1),
                    (position_set_x, pos1, xgm_ov_combobutton_scalex),
                    (position_set_y, pos1, xgm_ov_combobutton_scaley),
                    (overlay_set_size, overlay_var, pos1),
                ])
                for aComboItem in aModOption.GetParameters():
                    opblock.Append([(overlay_add_item, overlay_var, "@%s" % aComboItem)])
                opblock.Append(aModOption.GetInitializeBlock())
                opblock.Append([(overlay_set_val, overlay_var, reg1)])
                cur_overlay_index += 1
            cur_posy -= xgm_mod_options_property_height
    # no inner close - outer remains open
    return opblock.Unwrap()

def _generate_hub_mod_options_event():
    from util_wrappers import OpBlockWrapper
    opblock = OpBlockWrapper([])
    opblock2 = OpBlockWrapper([])
    cur_overlay_index = 1
    opblock.Append([
        (store_script_param, ":object", 1),
        (store_script_param, ":value", 2),
        (try_begin), (neq, 1, 1)])
    for x in mod_options:
        aModOption = ModOptionWrapper(x)
        if aModOption.GetType() in [xgm_ov_checkbox, xgm_ov_numberbox, xgm_ov_combolabel, xgm_ov_combobutton, xgm_ov_slider]:
            if aModOption.GetType() in [xgm_ov_numberbox, xgm_ov_checkbox, xgm_ov_combolabel, xgm_ov_combobutton, xgm_ov_slider]:
                overlay_var = "$g_presentation_obj_%s" % cur_overlay_index
                opblock.Append([(else_try), (eq, ":object", overlay_var), (assign, reg1, ":value")])
                opblock.Append(aModOption.GetUpdateBlock())
                opblock2.Append(aModOption.GetInitializeBlock())
                opblock2.Append([(overlay_set_val, overlay_var, reg1)])
                cur_overlay_index += 1
    opblock.Append([(try_end)])
    return opblock.Unwrap() + opblock2.Unwrap()

main_settings_shared_ui_scripts = [
  ("main_settings_create_ui", [
      (store_script_param, ":is_hub", 1),
      (try_begin),
        (eq, ":is_hub", 1),
      (else_try),
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
      (try_end),
  ] + _generate_hub_mod_options_load()
  ),
  ("main_settings_handle_event", _generate_hub_mod_options_event()),
]
