# -*- coding: cp1254 -*-
# All Items — store presentation for all items.
# Reads the per-category item arrays that custom_troops builds at game start
# (script_cstm_setup_item_arrays); trp_temp_array_a/b/c/d are used for overlay
# tracking only.
# Depends on: shared.cstm_item_helpers.item_types (for cstm_item_type_strings),
# custom_troops_header_presentations (for the Presentation wrapper), and the
# custom_troops item-array machinery (cstm_items_arrays_begin, cstm_slot_array_*,
# script_cstm_get_item_from_array).

import collections

from header_common import *
from header_operations import *
from header_items import *
from module_constants import *
from custom_troops_header_presentations import *

# Import cstm_item_type_strings from shared helpers (modmerger adds shared/ to sys.path)
_item_types = __import__("shared.cstm_item_helpers.item_types", fromlist=["cstm_item_type_strings"])
cstm_item_type_strings = _item_types.cstm_item_type_strings

#######################################################################
# Presentation
#######################################################################

orig_presentations = []
exec(open("source/presentations/prsnt_all_items.py", "r").read())
orig_presentations.append(all_items)

presentations = collections.OrderedDict()
for presentation_tuple in orig_presentations:
    presentations[presentation_tuple[0]] = Presentation(*presentation_tuple)

presentations["all_items"].triggers[ti_on_presentation_load][0].extend([

    (presentation_set_duration, 999999),
    (set_fixed_point_multiplier, 1000),

    # Globals (first load only)
    (try_begin),
        (eq, "$all_items_items_array", 0),
        (assign, "$all_items_items_array", cstm_items_arrays_begin),
        (assign, "$all_items_item_modifier_selected", 0),
        (assign, "$all_items_page_no", 0),
    (try_end),
    (assign, "$all_items_item_details_overlay", -1),
    (assign, "$all_items_quality_selector", -1),
    (try_begin),
        (eq, "$g_all_items_qty", 0),
        (assign, "$g_all_items_qty", 1),
    (try_end),
    (try_begin),
        (gt, "$g_all_items_restart_item", 0),
        (assign, ":restart_item", "$g_all_items_restart_item"),
        (assign, "$g_last_sel_item", ":restart_item"),
    (else_try),
        (assign, "$g_last_sel_item", -1),
        (assign, ":restart_item", 0),
    (try_end),

    # Clear overlay tracking
    (try_for_range, ":i", 0, 9999),
        (troop_set_slot, "trp_temp_array_a", ":i", -1),
        (troop_set_slot, "trp_temp_array_b", ":i", 0),
        (troop_set_slot, "trp_temp_array_c", ":i", 0),
    (try_end),

    # Background
    (create_mesh_overlay, reg1, "mesh_note_window"),
    (position_set_x, pos1, 0),
    (position_set_y, pos1, 0),
    (overlay_set_position, reg1, pos1),

    ## === TOP BAR: Category selector + Page selector ===

    # Page selector combo_label @ (500, 670)
    (create_combo_label_overlay, "$all_items_page_selector"),
    (position_set_x, pos1, 500),
    (position_set_y, pos1, 670),
    (overlay_set_position, "$all_items_page_selector", pos1),
    # Count items in current category
    (troop_get_slot, ":num_items", "$all_items_items_array", cstm_slot_array_num_items),
    (store_add, ":num_pages", ":num_items", 55),
    (val_div, ":num_pages", 56),
    (try_for_range, ":page_no", 0, ":num_pages"),
        (store_add, reg0, ":page_no", 1),
        (assign, reg1, ":num_pages"),
        (str_store_string, s0, "@Page {reg0} / {reg1}"),
        (overlay_add_item, "$all_items_page_selector", s0),
    (try_end),
    (overlay_set_val, "$all_items_page_selector", "$all_items_page_no"),

    ## === LEFT SIDE: Item grid (8 cols, 80px slots) ===

    (str_clear, s0),
    (create_text_overlay, "$all_items_container", s0, tf_scrollable),
    (position_set_x, pos1, 20),
    (position_set_y, pos1, 100),
    (overlay_set_position, "$all_items_container", pos1),
    (position_set_x, pos1, 640),
    (position_set_y, pos1, 560),
    (overlay_set_area_size, "$all_items_container", pos1),
    (set_container_overlay, "$all_items_container"),

    # Count items on this page for grid height
    (assign, ":grid_count", 0),
    (try_for_range, ":i", 0, 56),
        (store_mul, ":offset", "$all_items_page_no", 56),
        (store_add, ":item_index", ":i", ":offset"),
        (call_script, "script_cstm_get_item_from_array", "$all_items_items_array", ":item_index"),
        (assign, ":item", reg0),
        (gt, ":item", 0),
        (val_add, ":grid_count", 1),
    (try_end),

    (store_div, ":num_rows", ":grid_count", 8),
    (store_mod, ":rem", ":grid_count", 8),
    (val_min, ":rem", 1),
    (val_add, ":num_rows", ":rem"),

    # Render grid
    (assign, ":slot_no", 1),
    (assign, ":first_item", 0),
    (store_mul, ":grid_height", ":num_rows", 80),
    (val_sub, ":grid_height", 80),
    (assign, ":pos_x", 0),
    (assign, ":pos_y", ":grid_height"),
    (try_for_range, ":i", 0, 56),
        (store_mul, ":offset", "$all_items_page_no", 56),
        (store_add, ":item_index", ":i", ":offset"),
        (call_script, "script_cstm_get_item_from_array", "$all_items_items_array", ":item_index"),
        (assign, ":item", reg0),
        (try_begin),
            (eq, ":first_item", 0),
            (assign, ":first_item", ":item"),
        (try_end),
        # Slot background
        (create_image_button_overlay, reg1, "mesh_mp_inventory_choose", "mesh_mp_inventory_choose"),
        (position_set_x, pos1, 640),
        (position_set_y, pos1, 640),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, ":pos_x"),
        (position_set_y, pos1, ":pos_y"),
        (overlay_set_position, reg1, pos1),
        (troop_set_slot, "trp_temp_array_a", ":slot_no", reg1),
        # Item icon
        (try_begin),
            (gt, ":item", 0),
            (create_mesh_overlay_with_item_id, reg1, ":item"),
            (position_set_x, pos1, 800),
            (position_set_y, pos1, 800),
            (overlay_set_size, reg1, pos1),
            (store_add, ":item_x", ":pos_x", 40),
            (store_add, ":item_y", ":pos_y", 40),
            (position_set_x, pos1, ":item_x"),
            (position_set_y, pos1, ":item_y"),
            (overlay_set_position, reg1, pos1),
        (try_end),
        (troop_set_slot, "trp_temp_array_b", ":slot_no", reg1),
        (troop_set_slot, "trp_temp_array_c", ":slot_no", ":item"),
        # Advance grid position
        (val_add, ":pos_x", 80),
        (val_add, ":slot_no", 1),
        (try_begin),
            (ge, ":pos_x", 640),
            (assign, ":pos_x", 0),
            (val_sub, ":pos_y", 80),
        (try_end),
    (try_end),

    (set_container_overlay, -1),

    # Category combo_button @ (160, 670)
    (create_combo_button_overlay, "$all_items_type_selector"),
    (position_set_x, pos1, 160),
    (position_set_y, pos1, 670),
    (overlay_set_position, "$all_items_type_selector", pos1),

    ## === RIGHT SIDE: Preview + Controls ===

    # "Preview:" label @ (720, 600)
    (create_text_overlay, reg1, "@Preview: ", tf_left_align),
    (position_set_x, pos1, 720),
    (position_set_y, pos1, 600),
    (overlay_set_position, reg1, pos1),

    # Preview frame @ (690, 305)
    (create_image_button_overlay, reg1, "mesh_mp_inventory_choose", "mesh_mp_inventory_choose"),
    (position_set_x, pos1, 2240),
    (position_set_y, pos1, 2240),
    (overlay_set_size, reg1, pos1),
    (position_set_x, pos1, 690),
    (position_set_y, pos1, 305),
    (overlay_set_position, reg1, pos1),

    # Preview item icon @ (830, 445), size (2800, 2800)
    (try_begin),
        (gt, ":restart_item", 0),
        (assign, ":preview_item", ":restart_item"),
    (else_try),
        (assign, ":preview_item", 0),
    (try_end),
    (create_mesh_overlay_with_item_id, reg1, ":preview_item"),
    (position_set_x, pos1, 2800),
    (position_set_y, pos1, 2800),
    (overlay_set_size, reg1, pos1),
    (position_set_x, pos1, 830),
    (position_set_y, pos1, 445),
    (overlay_set_position, reg1, pos1),
    (troop_set_slot, "trp_temp_array_a", 0, reg1),
    (troop_set_slot, "trp_temp_array_b", 0, reg1),
    (troop_set_slot, "trp_temp_array_c", 0, ":preview_item"),

    # Quality combo_button @ (830, 260)
    (create_combo_button_overlay, "$all_items_quality_selector"),
    (position_set_x, pos1, 830),
    (position_set_y, pos1, 260),
    (overlay_set_position, "$all_items_quality_selector", pos1),
    # Populate modifiers
    (overlay_add_item, "$all_items_quality_selector", "@Plain"),
    (troop_set_slot, "trp_temp_array_d", 0, imod_plain),
    (assign, ":m_idx", 1),
    (try_begin),
        (gt, ":restart_item", 0),
        (assign, ":combo_item", ":restart_item"),
    (else_try),
        (assign, ":combo_item", ":first_item"),
    (try_end),
    (try_for_range, ":imod", 1, 43),
        (gt, ":combo_item", 0),
        (call_script, "script_item_has_modifier", ":combo_item", ":imod"),
        (eq, reg0, 1),
        (store_add, ":modifier_string", modifier_strings_begin, ":imod"),
        (overlay_add_item, "$all_items_quality_selector", ":modifier_string"),
        (troop_set_slot, "trp_temp_array_d", ":m_idx", ":imod"),
        (val_add, ":m_idx", 1),
    (try_end),
    (assign, "$g_modifier_count", ":m_idx"),
    (assign, "$g_modifier_idx", 0),
    (assign, "$g_all_items_imod", imod_plain),
    (assign, "$g_all_items_restart_item", 0),

    # Quantity/get — only in cheat mode
    (try_begin),
        (eq, "$cheat_mode", 1),
        (create_text_overlay, reg1, "@Quantity:", tf_left_align),
        (position_set_x, pos1, 720),
        (position_set_y, pos1, 210),
        (overlay_set_position, reg1, pos1),
        (create_number_box_overlay, "$g_all_items_qty_input", 1, 99),
        (position_set_x, pos1, 830),
        (position_set_y, pos1, 210),
        (overlay_set_position, "$g_all_items_qty_input", pos1),
        (set_fixed_point_multiplier, 1000),
        (position_set_x, pos1, 200),
        (position_set_y, pos1, 50),
        (overlay_set_area_size, "$g_all_items_qty_input", pos1),
        (overlay_set_val, "$g_all_items_qty_input", 1),
        (create_game_button_overlay, "$g_all_items_get_button", "@Get"),
        (position_set_x, pos1, 830),
        (position_set_y, pos1, 140),
        (overlay_set_position, "$g_all_items_get_button", pos1),
    (try_end),

    # Done button @ (830, 80)
    (create_game_button_overlay, "$all_items_done_button", "@Done"),
    (position_set_x, pos1, 830),
    (position_set_y, pos1, 80),
    (overlay_set_position, "$all_items_done_button", pos1),
])

presentations["all_items"].triggers[ti_on_presentation_event_state_change][0].extend([
    (store_trigger_param_1, ":object"),
    (store_trigger_param_2, ":value"),
    (set_fixed_point_multiplier, 1000),

    (try_begin),
        ## TYPE SELECTOR CHANGED
        (eq, ":object", "$all_items_type_selector"),
        (store_add, "$all_items_items_array", cstm_items_arrays_begin, ":value"),
        (assign, "$all_items_item_modifier_selected", 0),
        (assign, "$all_items_page_no", 0),
        (start_presentation, "prsnt_all_items"),
    (else_try),
        ## PAGE SELECTOR CHANGED
        (eq, ":object", "$all_items_page_selector"),
        (assign, "$all_items_page_no", ":value"),
        (start_presentation, "prsnt_all_items"),
    (else_try),
        ## QUALITY SELECTOR CHANGED
        (eq, ":object", "$all_items_quality_selector"),
        (try_begin),
            (lt, ":value", "$g_modifier_count"),
            (troop_get_slot, "$g_all_items_imod", "trp_temp_array_d", ":value"),
            (assign, "$g_modifier_idx", ":value"),
        (try_end),
    (else_try),
        ## QUANTITY INPUT CHANGED
        (eq, ":object", "$g_all_items_qty_input"),
        (eq, "$cheat_mode", 1),
        (val_max, ":value", 1),
        (assign, "$g_all_items_qty", ":value"),
    (else_try),
        ## GET BUTTON
        (eq, ":object", "$g_all_items_get_button"),
        (eq, "$cheat_mode", 1),
        (gt, "$g_last_sel_item", 0),
        (try_for_range, ":i", 0, "$g_all_items_qty"),
            (troop_add_item, "trp_player", "$g_last_sel_item", "$g_all_items_imod"),
        (try_end),
        (assign, reg0, "$g_all_items_qty"),
        (str_store_item_name, s1, "$g_last_sel_item"),
        (display_message, "@Added {reg0}x {s1} to inventory"),
    (else_try),
        ## DONE BUTTON
        (eq, ":object", "$all_items_done_button"),
        (presentation_set_duration, 0),
    (else_try),
        ## ITEM CLICKED IN GRID
        (assign, ":found", 0),
        (try_for_range, ":sn", 1, 57),
            (troop_slot_eq, "trp_temp_array_a", ":sn", ":object"),
            (assign, ":found", ":sn"),
        (try_end),
        (gt, ":found", 0),
        (troop_get_slot, ":item", "trp_temp_array_c", ":found"),
        (gt, ":item", 0),
        (assign, "$g_last_sel_item", ":item"),
        (assign, "$g_all_items_restart_item", ":item"),
        (start_presentation, "prsnt_all_items"),
    (try_end),
])

presentations["all_items"].triggers[ti_on_presentation_mouse_enter_leave][0].extend([
    (store_trigger_param_1, ":object"),
    (store_trigger_param_2, ":enter_leave"),

    (try_begin),
        (eq, ":enter_leave", 0),
        ## MOUSE ENTER
        # Check preview icon (slot 0)
        (try_begin),
            (troop_slot_eq, "trp_temp_array_a", 0, ":object"),
            (troop_get_slot, ":item_no", "trp_temp_array_c", 0),
            (gt, ":item_no", 0),
            (close_item_details),
            (troop_get_slot, ":target_obj", "trp_temp_array_b", 0),
            (overlay_get_position, pos0, ":target_obj"),
            (show_item_details_with_modifier, ":item_no", "$g_all_items_imod", pos0, 100),
            (assign, "$all_items_item_details_overlay", 0),
        (try_end),
        # Check grid items (slots 1-56)
        (try_for_range, ":sn", 1, 57),
            (troop_slot_eq, "trp_temp_array_a", ":sn", ":object"),
            (troop_get_slot, ":item_no", "trp_temp_array_c", ":sn"),
            (neq, ":item_no", 0),
            (close_item_details),
            (troop_get_slot, ":target_obj", "trp_temp_array_b", ":sn"),
            (overlay_get_position, pos0, ":target_obj"),
            (show_item_details_with_modifier, ":item_no", "$g_all_items_imod", pos0, 100),
            (assign, "$all_items_item_details_overlay", ":sn"),
        (try_end),
    (else_try),
        ## MOUSE LEAVE
        (try_begin),
            (troop_slot_eq, "trp_temp_array_a", 0, ":object"),
            (eq, "$all_items_item_details_overlay", 0),
            (close_item_details),
        (try_end),
        (try_for_range, ":sn", 1, 57),
            (troop_slot_eq, "trp_temp_array_a", ":sn", ":object"),
            (try_begin),
                (eq, "$all_items_item_details_overlay", ":sn"),
                (close_item_details),
            (try_end),
        (try_end),
    (try_end),
])

# Populate type selector from shared cstm_item_type_strings
for item_type, string in cstm_item_type_strings.iteritems():
    presentations["all_items"].triggers[ti_on_presentation_load][0].extend([
        (str_store_string, s0, "@" + string),
        (overlay_add_item, "$all_items_type_selector", s0),
    ])
presentations["all_items"].triggers[ti_on_presentation_load][0].extend([
    (store_sub, reg0, "$all_items_items_array", cstm_items_arrays_begin),
    (overlay_set_val, "$all_items_type_selector", reg0),
])

del orig_presentations[:]
for presentation_id in presentations:
    orig_presentations.append(presentations[presentation_id].convert_to_tuple())

def modmerge(var_set):
    try:
        var_name_1 = "presentations"
        orig_presentations_var = var_set[var_name_1]

        index = -1
        for i, p in enumerate(orig_presentations_var):
            if p[0] == "all_items":
                index = i
                break
        if index == -1:
            orig_presentations_var.extend(orig_presentations)
        else:
            orig_presentations_var[index:index+1] = orig_presentations
    except KeyError:
        errstring = "Variable set does not contain expected variable."
        raise ValueError(errstring)
