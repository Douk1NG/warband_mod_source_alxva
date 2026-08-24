# -*- coding: cp1254 -*-
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from header_items import *
from header_skills import *
from header_troops import *
from module_constants import *

from custom_troops_constants import *
from kingdom_custom_troop_tree_creator_constants import *

from kingdom_custom_troop_tree_creator.kct_presentations.layout import *

# --- Customisation store for the tree creator (ported from the custom_troops
# prsnt_cstm_customise_troop). Self-contained: only calls script_kct_* and core
# operations. Exit returns to the creation viewer (prsnt_cstm_create_troop_tree).

kct_customise_core = (
	("kct_customise_troop", 0, mesh_load_window,
	[
		(ti_on_presentation_load,
		[
			(assign, "$cstm_item_details_overlay", -1),
			(assign, "$cstm_customise_troop_save", -1),
			(assign, "$cstm_customise_troop_reset", -1),
			(assign, "$cstm_customise_troop_exit", -1),
			(assign, "$cstm_class_selector", -1),
			(troop_get_slot, "$cstm_item_type_selected", "$cstm_items_array", cstm_slot_array_item_type),
			(try_for_range, ":overlay_id", 0, 9999),
				(troop_set_slot, "trp_cstm_overlay_items", ":overlay_id", -1),
				(troop_set_slot, "trp_cstm_overlay_is_store_item", ":overlay_id", 0),
				(troop_set_slot, "trp_cstm_overlay_is_attribute_box", ":overlay_id", 0),
				(troop_set_slot, "trp_cstm_overlay_is_proficiency_box", ":overlay_id", 0),
				(troop_set_slot, "trp_cstm_overlay_is_skill_box", ":overlay_id", 0),
				(troop_set_slot, "trp_cstm_overlay_attribute", ":overlay_id", -1),
				(troop_set_slot, "trp_cstm_overlay_proficiency", ":overlay_id", -1),
				(troop_set_slot, "trp_cstm_overlay_skill", ":overlay_id", -1),
			(try_end),
			
			(troop_get_slot, ":dummy", "$cstm_troop_being_customised", cstm_slot_troop_dummy),
			
			# Design lock: a troop is frozen (stat boxes read-only) once its first
			# child has been saved; only equipment and name remain editable.
			(troop_get_slot, "$cstm_troop_design_locked", "$cstm_troop_being_customised", cstm_slot_troop_design_lock),
			
			# Baseline re-derivation (spec §7, snapshot model): every FRESH entry
			# into an unconfigured child (its parent configured, itself not yet
			# configured) rebuilds its starting stats from the base unit data plus
			# the parent's CURRENT attribute/skill/proficiency levels, and rolls
			# the parent's unspent proficiency points into its own pool. Keyed off
			# $g_kct_recalc_baseline (set by the tree viewer on node click), NOT
			# the inherited marker, so a parent re-customised after the child's
			# first open never leaves a stale distribution behind. Internal store
			# reloads (box edits, Reset) leave the flag clear and skip this.
			(troop_get_slot, ":parent", "$cstm_troop_being_customised", cstm_slot_troop_base_troop),
			(troop_get_slot, ":configured", "$cstm_troop_being_customised", cstm_slot_troop_configured),
			(try_begin,),
				(gt, ":parent", 0),
				(eq, ":configured", 0),
				(eq, "$g_kct_recalc_baseline", 1),
				
				# Base unit data first...
				(call_script, "script_kct_troop_set_stats_to_default", ":dummy"),
				# ...then raise attrs/skills up to the parent's current levels.
				(call_script, "script_kct_troop_copy_stats_if_higher", ":dummy", ":parent"),
				
				(try_for_range, ":proficiency", proficiencies_begin, proficiencies_end),
					(store_proficiency_level, ":parent_level", ":parent", ":proficiency"),
					(call_script, "script_kct_dummy_set_proficiency", ":dummy", ":proficiency", ":parent_level"),
				(try_end,),
				
				# The child inherits the parent's CURRENT build for free (spec §7):
				# its starting stats are the base unit data plus the parent's
				# levels, and it keeps its own pool minus what the inherited stats
				# cost - so a fully-spent level-26 parent hands its level-34 child
				# exactly the level-gap points (34-26 = 8). No refund: the child
				# only gains what its higher level grants. The kct_get_*_points_
				# available floors at 0 are the backstop against negatives from any
				# other path (stale saves, auto-distribution).
				
				# Proficiency rollover (deliberately generous - full cost refund):
				# the parent's unspent points (clamped at 0 so a stale over-budget
				# parent can't hand down a debt) PLUS the entire cost of the
				# inherited levels, so the child always has enough to cover its
				# inherited proficiencies and then some.
				(call_script, "script_kct_get_proficiency_points_available", ":parent"),
				(assign, ":inherited_bonus", reg0),
				(val_max, ":inherited_bonus", 0),
				(call_script, "script_kct_get_proficiency_points_spent", ":dummy"),
				(val_add, ":inherited_bonus", reg0),
				(troop_set_slot, "$cstm_troop_being_customised", cstm_slot_troop_proficiency_bonus, ":inherited_bonus"),
				(troop_set_slot, ":dummy", cstm_slot_troop_proficiency_bonus, ":inherited_bonus"),
			(try_end,),
			
			# Auto-distribute attributes to meet the tree minimums (spec §7
			# non-decreasing invariant): a node inherited from a configured parent
			# must never open below the floor - raise it from the dummy's points.
			(try_for_range, ":attribute", attributes_begin, attributes_end),
				(store_attribute_level, ":curr_val", ":dummy", ":attribute"),
				(call_script, "script_kct_troop_get_attribute_min_from_tree", "$cstm_troop_being_customised", "$cstm_troop_being_customised", ":attribute"),
				(try_begin,),
					(gt, reg0, ":curr_val"),
					(store_sub, ":difference", reg0, ":curr_val"),
					(troop_raise_attribute, ":dummy", ":attribute", ":difference"),
				(try_end,),
			(try_end,),
			
			# Baseline bake (snapshot model): on the same fresh entries above, fold
			# the re-derived stats into the REAL troop so the store's "anything
			# changed?" check starts at zero; Save/Reset then appear only for
			# genuine user edits. This OVERWRITES the previous baked baseline each
			# fresh entry while the child stays unconfigured.
			(try_begin,),
				(gt, ":parent", 0),
				(eq, ":configured", 0),
				(eq, "$g_kct_recalc_baseline", 1),
				(call_script, "script_kct_troop_copy_stats", "$cstm_troop_being_customised", ":dummy"),
				(troop_set_slot, "$cstm_troop_being_customised", cstm_slot_troop_inherited, 1),
				(troop_set_slot, ":dummy", cstm_slot_troop_inherited, 1),
			(try_end,),
			
			# Capture the persisted class override once per FRESH entry (the
			# $g_kct_recalc_baseline flag is still 1 here) so Reset can revert the
			# Class selector to what was saved. Internal reloads (box edits, Reset)
			# leave the flag clear and never overwrite it.
			(try_begin),
				(eq, "$g_kct_recalc_baseline", 1),
				(troop_get_slot, "$cstm_class_override_original", "$cstm_troop_being_customised", cstm_slot_troop_class_override),
				(assign, "$cstm_class_changed", 0),
				(troop_get_slot, "$cstm_gender_original", "$cstm_troop_being_customised", cstm_slot_troop_gender),
				(assign, "$cstm_gender_changed", 0),
			(try_end),

			# Consume the fresh-entry flag on every store load (configured units
			# included) so internal reloads never re-derive mid-edit. The flag is
			# captured first: the funds block below uses it to freeze the budget
			# at the session's first open.
			(assign, ":fresh_entry", "$g_kct_recalc_baseline"),
			(assign, "$g_kct_recalc_baseline", 0),
			
			(store_character_level, ":troop_level", "$cstm_troop_being_customised"),
			
			# Per-tree equipment budget (cstm_slot_tree_budget_begin +
			# $cstm_selected_tree on the shared prefix troop): Balanced (0) /
			# Boosted (1) / Cheater (2) are three tables stored contiguously in
			# trp_cstm_inventory_values (EQUIPMENT_FUNDS_TABLE_SIZE entries
			# each); read the tree's budget's table at the troop's level. Auto
			# (3) derives the funds from the troop's gear cost at entry, so ANY
			# imported template - whatever budget model it was authored under -
			# opens editable with remaining exactly 0 (no free denars). The gear
			# value is always the floor for the explicit tiers (snapshot): a tree
			# authored on a higher budget (or the budget lowered after saving)
			# costs more than the tier allows and would otherwise open negative;
			# max() covers the gap exactly so remaining = 0 and a raised budget
			# never hands out free denars.
			# Funds are computed ONLY on the session's fresh entry. Internal
			# reloads (add/remove item, class, boxes, Reset) must NOT re-derive
			# them from the evolving dummy gear: Auto would shrink the budget
			# when gear is removed (remaining stuck at 0, the removed item
			# unrecoverable) and grow it when gear is added (no real limit).
			# Frozen at entry, removing gear frees budget (remaining goes
			# positive and is spendable) and adding beyond it shows negative
			# (red) until balanced - the Save gate enforces remaining >= 0.
			(try_begin,),
				(eq, ":fresh_entry", 1),
				(call_script, "script_kct_troop_get_inventory_value", ":dummy"),
				(assign, ":gear_value", reg0),
				(store_add, ":budget_slot", cstm_slot_tree_budget_begin, "$cstm_selected_tree"),
				(troop_get_slot, ":budget", cstm_troop_tree_prefix, ":budget_slot"),
				(try_begin,),
					(eq, ":budget", 3),
					(assign, "$cstm_total_funds", ":gear_value"),
				(else_try,),
					(store_mul, ":funds_slot", ":budget", EQUIPMENT_FUNDS_TABLE_SIZE),
					(val_add, ":funds_slot", ":troop_level"),
					(troop_get_slot, ":funds", "trp_cstm_inventory_values", ":funds_slot"),
					(val_max, ":funds", ":gear_value"),
					(assign, "$cstm_total_funds", ":funds"),
				(try_end,),
			(try_end,),
			
			(call_script, "script_kct_troop_copy_inventory", "$cstm_presentation_troop", ":dummy"),
			(troop_sort_inventory, "$cstm_presentation_troop"),
			(troop_equip_items, "$cstm_presentation_troop"),
			(call_script, "script_kct_create_troop_image", "$cstm_presentation_troop", -25, 350, 1250),
			(assign, "$cstm_troop_image", reg1),
			
			(call_script, "script_kct_create_scrollable_container", KCT_INV_POS_X, KCT_INV_POS_Y, KCT_INV_SLOT_SIZE * KCT_INV_CONT_WIDTH, KCT_INV_SLOT_SIZE * KCT_INV_CONT_HEIGHT),
			(assign, "$cstm_troop_inventory_container", reg1),
			
			(set_container_overlay, "$cstm_troop_inventory_container"),
			
			(try_for_range, ":item_slot", 0, num_equipment_kinds),
				(troop_get_inventory_slot, ":item", ":dummy", ":item_slot"),
				(troop_get_inventory_slot_modifier, ":imod", ":dummy", ":item_slot"),
				(gt, ":item", 0),
				
				(troop_add_item, ":dummy", ":item", ":imod"),
				(troop_set_inventory_slot, ":dummy", ":item_slot", -1),
			(try_end),
			
			(troop_get_inventory_capacity, ":capacity", ":dummy"),
			(val_sub, ":capacity", num_equipment_kinds),
			(try_for_range, ":item_index", 0, ":capacity"),
				(store_add, ":item_slot", ":item_index", num_equipment_kinds),
				(troop_get_inventory_slot, ":item", ":dummy", ":item_slot"),
				
				
				
				(call_script, "script_kct_get_grid_position", ":item_index", ":capacity", KCT_INV_CONT_WIDTH, KCT_INV_SLOT_SIZE, KCT_INV_SLOT_SIZE),
				(assign, ":pos_x", reg0),
				(assign, ":pos_y", reg1),
				
				
				(call_script, "script_kct_create_mesh_overlay", "mesh_inv_slot", ":pos_x", ":pos_y", KCT_INV_SLOT_SIZE * 10, KCT_INV_SLOT_SIZE * 10),
				(gt, ":item", 0),
				
				(troop_set_slot, "trp_cstm_overlay_items", reg1, ":item_slot"),
				
				(store_add, ":item_x", ":pos_x", KCT_INV_SLOT_SIZE / 2),
				(store_add, ":item_y", ":pos_y", KCT_INV_SLOT_SIZE / 2),
				(call_script, "script_kct_create_item_overlay", ":item", ":item_x", ":item_y", KCT_INV_SLOT_SIZE * 10),
			(try_end),
			
			(set_container_overlay, -1),
			
			(str_store_string, s0, "@Right-click to remove"),
      (call_script, "script_kct_create_text_overlay", "str_s0", KCT_INV_POS_X, KCT_INV_POS_Y - 28, 1000, KCT_INV_SLOT_SIZE * KCT_INV_CONT_WIDTH, 20, tf_left_align),
			(assign, "$cstm_remove_from_inventory_message", reg1),
			(overlay_set_display, "$cstm_remove_from_inventory_message", 0),
			
			
			(call_script, "script_kct_create_combo_button_overlay", KCT_STORE_POS_X + KCT_STORE_SLOT_SIZE * KCT_STORE_CONT_WIDTH + 135, KCT_STORE_POS_Y + KCT_STORE_SLOT_SIZE * KCT_STORE_CONT_HEIGHT + 20),
			(assign, "$cstm_store_item_type_selector", reg1),
			(position_set_x, pos1, 750),
			(position_set_y, pos1, 750),
			(overlay_set_size, "$cstm_store_item_type_selector", pos1),
			
			(call_script, "script_kct_create_combo_button_overlay", KCT_STORE_POS_X + KCT_STORE_SLOT_SIZE * KCT_STORE_CONT_WIDTH + 345, KCT_STORE_POS_Y + KCT_STORE_SLOT_SIZE * KCT_STORE_CONT_HEIGHT + 20),
			(assign, "$cstm_store_item_modifier_selector", reg1),
			(position_set_x, pos1, 750),
			(position_set_y, pos1, 750),
			(overlay_set_size, "$cstm_store_item_modifier_selector", pos1),
			
			(assign, ":count", 0),
			(try_for_range, ":imod", imod_plain, imod_large_bag+1),
				(store_add, ":modifier_string", modifier_strings_begin, ":imod"),
				(call_script, "script_kct_cf_cci_imod_appropriate_for_item", "$cstm_item_type_selected", ":imod"),
				
				(overlay_add_item, "$cstm_store_item_modifier_selector", ":modifier_string"),
				
				(try_begin),
					(eq, ":imod", "$cstm_item_modifier_selected"),
					
					(overlay_set_val, "$cstm_store_item_modifier_selector", ":count"),
				(try_end),
				
				(val_add, ":count", 1),
			(try_end),
			
			(call_script, "script_kct_create_combo_label_overlay", KCT_STORE_POS_X + (KCT_STORE_SLOT_SIZE * (KCT_STORE_CONT_WIDTH + 1)) / 2, KCT_STORE_POS_Y + KCT_STORE_SLOT_SIZE * KCT_STORE_CONT_HEIGHT + 15),
			(assign, "$cstm_item_page_selector", reg1),
			(position_set_x, pos1, 750),
			(position_set_y, pos1, 1000),
			(overlay_set_size, "$cstm_item_page_selector", pos1),
			
			(troop_get_slot, ":num_items", "$cstm_items_array", cstm_slot_array_num_items),
			(store_add, ":num_pages", ":num_items", KCT_STORE_CONT_WIDTH * KCT_STORE_CONT_HEIGHT - 1),
			(val_div, ":num_pages", KCT_STORE_CONT_WIDTH * KCT_STORE_CONT_HEIGHT),
			
			(try_for_range, ":page_no", 0, ":num_pages"),
				(store_add, reg0, ":page_no", 1),
				(assign, reg1, ":num_pages"),
				(str_store_string, s0, "@Items page {reg0} / {reg1}"),
				(overlay_add_item, "$cstm_item_page_selector", s0),
			(try_end),
			(overlay_set_val, "$cstm_item_page_selector", "$cstm_item_page_no"),
			
			(call_script, "script_kct_create_scrollable_container", KCT_STORE_POS_X, KCT_STORE_POS_Y, KCT_STORE_SLOT_SIZE * KCT_STORE_CONT_WIDTH, KCT_STORE_SLOT_SIZE * KCT_STORE_CONT_HEIGHT),
			(assign, "$cstm_store_container", reg1),
			
			(set_container_overlay, "$cstm_store_container"),
			
			(try_for_range, ":slot_no", 0, KCT_STORE_CONT_WIDTH * KCT_STORE_CONT_HEIGHT),
				(store_mul, ":offset", "$cstm_item_page_no", KCT_STORE_CONT_WIDTH * KCT_STORE_CONT_HEIGHT),
				(store_add, ":item_index", ":slot_no", ":offset"),
				(call_script, "script_kct_get_item_from_array", "$cstm_items_array", ":item_index"),
				(assign, ":item", reg0),
				
				
				
				(call_script, "script_kct_get_grid_position", ":slot_no", KCT_STORE_CONT_WIDTH * KCT_STORE_CONT_HEIGHT, KCT_STORE_CONT_WIDTH, KCT_STORE_SLOT_SIZE, KCT_STORE_SLOT_SIZE),
				(assign, ":pos_x", reg0),
				(assign, ":pos_y", reg1),
				
				
				(call_script, "script_kct_create_mesh_overlay", "mesh_inv_slot", ":pos_x", ":pos_y", KCT_STORE_SLOT_SIZE * 10, KCT_STORE_SLOT_SIZE * 10),
				(troop_set_slot, "trp_cstm_overlay_items", reg1, ":item"),
				(troop_set_slot, "trp_cstm_overlay_is_store_item", reg1, 1),
				
				(gt, ":item", 0),
				
				(store_add, ":item_x", ":pos_x", KCT_STORE_SLOT_SIZE / 2),
				(store_add, ":item_y", ":pos_y", KCT_STORE_SLOT_SIZE / 2),
				(call_script, "script_kct_create_item_overlay", ":item", ":item_x", ":item_y", KCT_STORE_SLOT_SIZE * 10),
			(try_end),
			
			(set_container_overlay, -1),
			
			(str_store_string, s0, "@Remaining funds:"),
      (call_script, "script_kct_create_text_overlay", "str_s0", KCT_STORE_POS_X - 3, KCT_STORE_POS_Y - 28, 1000, KCT_STORE_SLOT_SIZE * KCT_STORE_CONT_WIDTH, 20, tf_left_align),
			
			(call_script, "script_kct_troop_get_inventory_value", ":dummy"),
			(store_sub, ":remaining_funds", "$cstm_total_funds", reg0),
			(assign, reg0, ":remaining_funds"),
			(str_store_string, s0, "@{reg0} denars"),
      (call_script, "script_kct_create_text_overlay", "str_s0", KCT_STORE_POS_X + KCT_STORE_SLOT_SIZE * KCT_STORE_CONT_WIDTH, KCT_STORE_POS_Y - 28, 1000, 200, 20, tf_right_align),
			(try_begin),
				(ge, ":remaining_funds", 0),
				
				(overlay_set_color, reg1, 0xffff00),
			(else_try),
				(overlay_set_color, reg1, 0xbb0000),
			(try_end),
			
			(call_script, "script_kct_create_scrollable_container", KCT_STATS_POS_X, KCT_STATS_POS_Y, KCT_STATS_SIZE_X, KCT_STATS_SIZE_Y),
			(assign, "$cstm_stats_container", reg1),
			
			(set_container_overlay, "$cstm_stats_container"),
			
			(store_character_level, reg0, "$cstm_troop_being_customised"),
			(store_troop_health, reg1, "$cstm_troop_being_customised", 1),
			(str_store_string, s0, "@Level {reg0}    HP {reg1}"),
			(call_script, "script_kct_create_text_overlay", "str_s0", 0, KCT_STATS_GAP_Y * 3 + KCT_STATS_ATTR_SECTION_HEIGHT + KCT_STATS_SKL_SECTION_HEIGHT + KCT_STATS_PROF_SECTION_HEIGHT + KCT_CLASS_SECTION_HEIGHT, KCT_STATS_SKL_TEXT_SIZE, KCT_STATS_SIZE_X, 50, tf_left_align),

			## CLASS SELECTOR INNER - label separate + select below Level/HP
			(str_store_string, s0, "@Class:"),
			(call_script, "script_kct_create_text_overlay", "str_s0", KCT_CLASS_LABEL[0], KCT_CLASS_LABEL[1], 900, 60, 25, tf_left_align),
			(call_script, "script_kct_create_combo_button_overlay", KCT_CLASS_SELECT[0], KCT_CLASS_SELECT[1]),
			(assign, "$cstm_class_selector", reg1),
			(str_store_string, s0, "@Auto"),
			(overlay_add_item, "$cstm_class_selector", s0),
			(str_store_string, s0, "@Infantry"),
			(overlay_add_item, "$cstm_class_selector", s0),
			(str_store_string, s0, "@Cavalry"),
			(overlay_add_item, "$cstm_class_selector", s0),
			(str_store_string, s0, "@Archers"),
			(overlay_add_item, "$cstm_class_selector", s0),
			(troop_get_slot, ":class_override", "$cstm_troop_being_customised", cstm_slot_troop_class_override),
			(overlay_set_val, "$cstm_class_selector", ":class_override"),
			(position_set_x, pos1, 750),
			(position_set_y, pos1, 750),
			(overlay_set_size, "$cstm_class_selector", pos1),
			
			(try_for_range, ":attribute", attributes_begin, ca_intelligence + 1),
			(call_script, "script_kct_get_grid_position", ":attribute", 3, KCT_STATS_ATTR_CONT_WIDTH, KCT_STATS_ATTR_COL_WIDTH, KCT_STATS_ATTR_ROW_HEIGHT),
			(assign, ":pos_x", reg0),
			(store_add, ":pos_y", reg1, KCT_STATS_PROF_SECTION_HEIGHT + KCT_STATS_SKL_SECTION_HEIGHT + KCT_STATS_GAP_Y * 2 + KCT_CLASS_SECTION_HEIGHT),
				
				(store_add, ":attribute_string", cstm_attribute_strings_begin, ":attribute"),
				(str_store_string, s0, ":attribute_string"),
				(call_script, "script_kct_create_text_overlay", "str_s0", ":pos_x", ":pos_y", KCT_STATS_ATTR_TEXT_SIZE, KCT_STATS_ATTR_COL_WIDTH, KCT_STATS_ATTR_ROW_HEIGHT, tf_left_align),
				(store_add, ":attribute_tooltip", kct_attribute_tooltips_begin, ":attribute"),
				(overlay_set_tooltip, reg1, ":attribute_tooltip"),
				
				(val_add, ":pos_x", KCT_STATS_ATTR_COL_WIDTH - 75),
				
				(store_attribute_level, ":curr_val", ":dummy", ":attribute"),
				
				(call_script, "script_kct_troop_get_attribute_min_from_points", "$cstm_troop_being_customised", ":attribute"),
				(assign, ":min", reg0),
				(call_script, "script_kct_troop_get_attribute_min_from_tree", "$cstm_troop_being_customised", "$cstm_troop_being_customised", ":attribute"),
				(val_max, ":min", reg0),
				
				(store_attribute_level, ":max", ":dummy", ":attribute"),
				(call_script, "script_kct_get_attribute_points_available", ":dummy", ":attribute"),
				(val_add, ":max", reg0),
				(val_add, ":max", 1),

				(try_begin),
					(lt, ":curr_val", ":min"),
					
					(str_store_string, s0, ":attribute_string"),
					(assign, reg0, ":min"),
					(assign, reg1, ":curr_val"),
					(display_message, "@{s0} minimum was being set to {reg0}, but current value is {reg1}"),
					(assign, ":min", ":curr_val"),
				(try_end),

				(try_begin),
					(ge, ":curr_val", ":max"),
					
					(str_store_string, s0, ":attribute_string"),
					(assign, reg0, ":max"),
					(assign, reg1, ":curr_val"),
					(display_message, "@{s0} maximum was being set to {reg0}, but current value is {reg1}"),
					(store_add, ":max", ":curr_val", 1),
				(try_end),
				
				
				(call_script, "script_kct_create_number_box_overlay", ":pos_x", ":pos_y", ":min", ":max"),
				(troop_set_slot, "trp_cstm_overlay_is_attribute_box", reg1, 1),
				(troop_set_slot, "trp_cstm_overlay_attribute", reg1, ":attribute"),
				(overlay_set_val, reg1, ":curr_val"),
			(try_end),
			
			# Attribute points (glued to the attributes section above)
			(call_script, "script_kct_get_attribute_points_available", ":dummy"),
			(str_store_string, s0, "@Attribute points: {reg0}"),
			(call_script, "script_kct_create_text_overlay", "str_s0", 0, KCT_STATS_PROF_SECTION_HEIGHT + KCT_STATS_SKL_SECTION_HEIGHT + KCT_STATS_GAP_Y * 2 + KCT_STATS_ATTR_ROW_HEIGHT + KCT_CLASS_SECTION_HEIGHT, KCT_STATS_POINTS_TEXT_SIZE, KCT_STATS_POINTS_COL_WIDTH, KCT_STATS_POINTS_ROW_HEIGHT, tf_left_align),
			
			# Proficiency section: "Proficiency points: {reg0}" label on top,
			# then one number box per weapon type in a 2-column grid below. The
			# boxes are bounded by the points budget (original custom_troops
			# behaviour): min can't go below the starting level, max is the
			# highest level affordable with the available points, capped at
			# CSTM_WP_CAP_LEVELS_PER_WM*WM + CSTM_WP_CAP_ADDITIONAL.
			(call_script, "script_kct_get_proficiency_points_available", ":dummy"),
			(str_store_string, s0, "@Proficiency points: {reg0}"),
			(call_script, "script_kct_create_text_overlay", "str_s0", 0, KCT_STATS_PROF_SECTION_HEIGHT - KCT_STATS_PROF_POINTS_ROW_HEIGHT + KCT_CLASS_SECTION_HEIGHT, KCT_STATS_POINTS_TEXT_SIZE, KCT_STATS_POINTS_COL_WIDTH * 2, KCT_STATS_PROF_POINTS_ROW_HEIGHT, tf_left_align),
			
			(try_for_range, ":proficiency", proficiencies_begin, proficiencies_end),
				(call_script, "script_kct_get_grid_position", ":proficiency", proficiencies_end, KCT_STATS_PROF_CONT_WIDTH, KCT_STATS_PROF_COL_WIDTH, KCT_STATS_PROF_ROW_HEIGHT),
				(assign, ":pos_x", reg0),
				(store_add, ":pos_y", reg1, KCT_CLASS_SECTION_HEIGHT),
				
				(store_add, ":proficiency_string", cstm_proficiency_strings_begin, ":proficiency"),
				(str_store_string, s0, ":proficiency_string"),
				(call_script, "script_kct_create_text_overlay", "str_s0", ":pos_x", ":pos_y", KCT_STATS_PROF_TEXT_SIZE, KCT_STATS_PROF_COL_WIDTH, KCT_STATS_PROF_ROW_HEIGHT, tf_left_align),
				
				(val_add, ":pos_x", KCT_STATS_PROF_COL_WIDTH - 75),
				
				(store_proficiency_level, ":curr_val", ":dummy", ":proficiency"),
				
				(call_script, "script_kct_troop_get_proficiency_min_from_points", "$cstm_troop_being_customised", ":proficiency"),
				(assign, ":min", reg0),
				(call_script, "script_kct_troop_get_proficiency_min_from_tree", "$cstm_troop_being_customised", ":proficiency"),
				(val_max, ":min", reg0),
				
				(try_begin),
					(lt, ":curr_val", ":min"),
					
					(str_store_string, s0, ":proficiency_string"),
					(assign, reg0, ":min"),
					(assign, reg1, ":curr_val"),
					(display_message, "@{s0} minimum was being set to {reg0}, but current value is {reg1}"),
					(assign, ":min", ":curr_val"),
				(try_end),
				
				(call_script, "script_kct_troop_get_proficiency_max_from_points", ":dummy", ":proficiency"),
				(assign, ":max", reg0),
				
				# Apply cap from weapon master
				(store_skill_level, ":weapon_master", skl_weapon_master, ":dummy"),
				(store_mul, ":cap", CSTM_WP_CAP_LEVELS_PER_WM, ":weapon_master"),
				(val_add, ":cap", CSTM_WP_CAP_ADDITIONAL),
				(val_min, ":max", ":cap"),
				(val_add, ":max", 1),
				
				(try_begin),
					(ge, ":curr_val", ":max"),
					
					(str_store_string, s0, ":proficiency_string"),
					(assign, reg0, ":max"),
					(assign, reg1, ":curr_val"),
					(display_message, "@{s0} maximum was being set to {reg0}, but current value is {reg1}"),
					(store_add, ":max", ":curr_val", 1),
				(try_end),
				
				(call_script, "script_kct_create_number_box_overlay", ":pos_x", ":pos_y", ":min", ":max"),
				(troop_set_slot, "trp_cstm_overlay_is_proficiency_box", reg1, 1),
				(troop_set_slot, "trp_cstm_overlay_proficiency", reg1, ":proficiency"),
				(overlay_set_val, reg1, ":curr_val"),
			(try_end),
			
			(set_container_overlay, -1),
			
			(str_store_string, s0, "@Name (singular): "),
      (call_script, "script_kct_create_text_overlay", "str_s0", KCT_NAME_POS_X + KCT_NAME_LABEL_WIDTH, KCT_NAME_POS_Y, 1000, KCT_NAME_LABEL_WIDTH, 50, tf_right_align),
      
      (str_store_troop_name, s0, ":dummy"),
      (call_script, "script_kct_create_text_box_overlay", "str_s0", KCT_NAME_POS_X + KCT_NAME_LABEL_WIDTH, KCT_NAME_POS_Y),
      (assign, "$cstm_set_name", reg1),
      
      (str_store_string, s0, "@Name (plural): "),
      (call_script, "script_kct_create_text_overlay", "str_s0", KCT_NAME_POS_X + KCT_NAME_LABEL_WIDTH + KCT_NAME_GAP, KCT_NAME_POS_Y, 1000, KCT_NAME_LABEL_WIDTH, 50, tf_right_align),
      
      (str_store_troop_name_plural, s0, ":dummy"),
      (call_script, "script_kct_create_text_box_overlay", "str_s0", KCT_NAME_POS_X + KCT_NAME_LABEL_WIDTH + KCT_NAME_GAP, KCT_NAME_POS_Y),
      (assign, "$cstm_set_name_plural", reg1),
			
			## CLASS SELECTOR - MOVED INSIDE STATS (hidden outside, see inner block below Level/HP)
			(assign, "$cstm_class_selector", -1),

			## GENDER SELECTOR (branch-gender hierarchy: flipping a node flips its entire subtree)
			# SELECT (combo button dropdown) - proven store pattern 750x750, not label.
			(call_script, "script_kct_create_combo_button_overlay", KCT_GENDER_POS[0], KCT_GENDER_POS[1]),
			(assign, "$cstm_gender_selector", reg1),
			(str_store_string, s0, "@Male"),
			(overlay_add_item, "$cstm_gender_selector", s0),
			(str_store_string, s0, "@Female"),
			(overlay_add_item, "$cstm_gender_selector", s0),
			(troop_get_slot, ":gender_flipped", "$cstm_troop_being_customised", cstm_slot_troop_gender),
			(try_begin),
				(eq, ":gender_flipped", 1),
				(try_begin),
					(eq, "$cstm_selected_gender", 0),
					(assign, ":gender_display", 1),
				(else_try),
					(assign, ":gender_display", 0),
				(try_end),
			(else_try),
				(assign, ":gender_display", "$cstm_selected_gender"),
			(try_end),
			(overlay_set_val, "$cstm_gender_selector", ":gender_display"),
			(position_set_x, pos1, 750),
			(position_set_y, pos1, 750),
			(overlay_set_size, "$cstm_gender_selector", pos1),
			
			(assign, ":changes_made", "$cstm_name_changed"),
			(val_add, ":changes_made", "$cstm_class_changed"),
			(val_add, ":changes_made", "$cstm_gender_changed"),
			(try_begin),
				(call_script, "script_kct_cf_troop_stats_are_different", "$cstm_troop_being_customised", ":dummy"),
				
				(assign, ":changes_made", 1),
			(else_try),
				(call_script, "script_kct_cf_troop_equipments_are_different", "$cstm_troop_being_customised", ":dummy"),
				
				(assign, ":changes_made", 1),
			(try_end),
			
			(try_begin),
				(eq, ":changes_made", 1),
				(ge, ":remaining_funds", 0),
				
				(str_store_string, s0, "@Save"),
				(call_script, "script_kct_create_game_button_overlay", "str_s0", KCT_BUTTONS_POS_X, KCT_BUTTONS_POS_Y),
				(assign, "$cstm_customise_troop_save", reg1),
				(position_set_x, pos1, KCT_BUTTONS_SIZE_X),
				(position_set_y, pos1, KCT_BUTTONS_SIZE_Y),
				(overlay_set_size, "$cstm_customise_troop_save", pos1),
			(end_try),
			
			(try_begin),
				(eq, ":changes_made", 1),
				
				(str_store_string, s0, "@Reset"),
				(call_script, "script_kct_create_game_button_overlay", "str_s0", KCT_BUTTONS_POS_X + KCT_BUTTONS_SIZE_X + KCT_BUTTONS_GAP, KCT_BUTTONS_POS_Y),
				(assign, "$cstm_customise_troop_reset", reg1),
				(position_set_x, pos1, KCT_BUTTONS_SIZE_X),
				(position_set_y, pos1, KCT_BUTTONS_SIZE_Y),
				(overlay_set_size, "$cstm_customise_troop_reset", pos1),
			(try_end),
			
			(try_begin),
				(neq, ":changes_made", 1),
				
				(str_store_string, s0, "@Exit"),
				(call_script, "script_kct_create_game_button_overlay", "str_s0", KCT_BUTTONS_POS_X + KCT_BUTTONS_SIZE_X + KCT_BUTTONS_GAP, KCT_BUTTONS_POS_Y),
				(assign, "$cstm_customise_troop_exit", reg1),
				(position_set_x, pos1, KCT_BUTTONS_SIZE_X),
				(position_set_y, pos1, KCT_BUTTONS_SIZE_Y),
				(overlay_set_size, "$cstm_customise_troop_exit", pos1),
			(try_end),
			
			(presentation_set_duration, 999999),
		]),
		
		(ti_on_presentation_mouse_enter_leave,
		[
			(store_trigger_param_1, ":overlay"),
			(store_trigger_param_2, ":mouse_left"),
			
			(try_begin),
				(troop_slot_ge, "trp_cstm_overlay_items", ":overlay", 1),
				
				(try_begin),
					(eq, ":mouse_left", 1),
					
					(try_begin),
						(eq, "$cstm_item_details_overlay", ":overlay"),
						
						(close_item_details),
						(assign, "$cstm_item_details_overlay", -1),
						(overlay_set_display, "$cstm_remove_from_inventory_message", 0),
					(try_end),
				(else_try),
					(try_begin),
						(gt, "$cstm_item_details_overlay", 0),
						
						(close_item_details),
					(try_end),
					
					(troop_get_slot, ":dummy", "$cstm_troop_being_customised", cstm_slot_troop_dummy),
					(try_begin),
						(troop_slot_eq, "trp_cstm_overlay_is_store_item", ":overlay", 1),
						
						(troop_get_slot, ":item", "trp_cstm_overlay_items", ":overlay"),
						(assign, ":imod", "$cstm_item_modifier_selected"),
					(else_try),
						(troop_get_slot, ":inventory_slot", "trp_cstm_overlay_items", ":overlay"),
						
						(troop_get_inventory_slot, ":item", ":dummy", ":inventory_slot"),
						(troop_get_inventory_slot_modifier, ":imod", ":dummy", ":inventory_slot"),
					(try_end),
					
					(overlay_get_position, pos1, ":overlay"),
					(call_script, "script_kct_item_get_price_with_modifier", ":item", ":imod"),
					(show_item_details_with_modifier, ":item", ":imod", pos1, reg1),
					(assign, "$cstm_item_details_overlay", ":overlay"),
					
					(neg|troop_slot_eq, "trp_cstm_overlay_is_store_item", ":overlay", 1),
					
					(overlay_set_display, "$cstm_remove_from_inventory_message", 1),
				(try_end),
			(try_end),
		]),
		
		(ti_on_presentation_mouse_press,
		[
			(store_trigger_param_1, ":overlay"),
			(store_trigger_param_2, ":mouse_button"),
			
			(troop_get_slot, ":dummy", "$cstm_troop_being_customised", cstm_slot_troop_dummy),
			
			(try_begin),
				(eq, ":mouse_button", 0),	# Left-click
				(troop_slot_ge, "trp_cstm_overlay_items", ":overlay", 1),
				(troop_slot_eq, "trp_cstm_overlay_is_store_item", ":overlay", 1),
				
				(try_begin),
					(store_free_inventory_capacity, ":free_capacity", ":dummy"),
					(eq, ":free_capacity", 0),
					
					(display_message, "@{s1} has no room left in inventory", 0xff0000),
				(else_try),
					(troop_get_slot, ":item", "trp_cstm_overlay_items", ":overlay"),
					
					(assign, ":meets_requirement", 1),
					(try_begin),
						(call_script, "script_kct_cf_troop_can_use_item_with_modifier", ":dummy", ":item", "$cstm_item_modifier_selected"),
					(else_try),
						(assign, ":meets_requirement", 0),
					(try_end),
					
					(eq, ":meets_requirement", 0),
					
					(str_store_troop_name, s1, ":dummy"),
					(str_store_item_name, s2, ":item"),
					(try_begin),
						(gt, "$cstm_item_modifier_selected", 0),
						
						(store_add, ":modifier_string", modifier_strings_begin, "$cstm_item_modifier_selected"),
						(str_store_string, s0, ":modifier_string"),
						(str_store_string, s2, "@{s0} {s2}"),
					(try_end),
					(call_script, "script_kct_store_item_requirement_stat_to_s0", ":item"),
					(display_message, "@{reg1} {s0} is required to equip {s2}, {s1} has {reg0}", 0xff0000),
				(else_try),
					(troop_add_item, ":dummy", ":item", "$cstm_item_modifier_selected"),
					(start_presentation, "prsnt_kct_customise_troop"),
				(try_end),
			(else_try),
				(eq, ":mouse_button", 1),	# Right-click
				
				(troop_get_slot, ":inventory_slot", "trp_cstm_overlay_items", ":overlay"),
				(gt, ":inventory_slot", 0),
				
				(troop_slot_eq, "trp_cstm_overlay_is_store_item", ":overlay", 0),
				
				(troop_set_inventory_slot, ":dummy", ":inventory_slot", -1),
				(start_presentation, "prsnt_kct_customise_troop"),
			(try_end),
		]),
		
		(ti_on_presentation_run,
		[
			(try_begin),
				(key_clicked, key_escape),
				
				(try_begin),
					(eq, "$cstm_class_changed", 1),
					
					(troop_set_slot, "$cstm_troop_being_customised", cstm_slot_troop_class_override, "$cstm_class_override_original"),
					(troop_get_slot, ":dummy", "$cstm_troop_being_customised", cstm_slot_troop_dummy),
					(call_script, "script_kct_apply_troop_class", "$cstm_troop_being_customised", ":dummy", "$cstm_class_override_original"),
				(try_end),
				(try_begin),
					(eq, "$cstm_gender_changed", 1),
					(call_script, "script_kct_flip_subtree", "$cstm_troop_being_customised", "$cstm_gender_original"),
				(try_end),
				
				(presentation_set_duration, 0),
			(try_end),
		]),
		
		(ti_on_presentation_event_state_change,
		[
			(store_trigger_param_1, ":object"),
			(store_trigger_param_2, ":value"),
			
			
			(troop_get_slot, ":dummy", "$cstm_troop_being_customised", cstm_slot_troop_dummy),
			(try_begin),
				(eq, ":object", "$cstm_set_name"),
				
				(troop_set_name, ":dummy", s0),
				(str_store_string, s1, "@{s0}s"),
				(troop_set_plural_name, ":dummy", s1),
				(assign, "$cstm_name_changed", 1),
				(start_presentation, "prsnt_kct_customise_troop"),
			(else_try),
				(eq, ":object", "$cstm_set_name_plural"),
				
				(troop_set_plural_name, ":dummy", s0),
				(assign, "$cstm_name_changed", 1),
				(start_presentation, "prsnt_kct_customise_troop"),
			(else_try),
				(eq, ":object", "$cstm_store_item_type_selector"),
        
        (store_add, "$cstm_items_array", cstm_items_arrays_begin, ":value"),
				(assign, "$cstm_item_modifier_selected", 0),
				(assign, "$cstm_item_page_no", 0),
				(start_presentation, "prsnt_kct_customise_troop"),
			(else_try),
				(eq, ":object", "$cstm_store_item_modifier_selector"),
				
				(assign, ":count", 0),
				(assign, ":end_cond", imod_large_bag + 1),
				(try_for_range, ":imod", imod_plain, ":end_cond"),
					(call_script, "script_kct_cf_cci_imod_appropriate_for_item", "$cstm_item_type_selected", ":imod"),
					
					(try_begin),
						(eq, ":count", ":value"),
						
						(assign, "$cstm_item_modifier_selected", ":imod"),
						(assign, ":end_cond", 0),
					(try_end),
					
					(val_add, ":count", 1),
				(try_end),
				
				(start_presentation, "prsnt_kct_customise_troop"),
			(else_try),
				(eq, ":object", "$cstm_item_page_selector"),
				
				(assign, "$cstm_item_page_no", ":value"),
				(start_presentation, "prsnt_kct_customise_troop"),
			(else_try),
				## CLASS SELECTOR CHANGED - persist the override on the real troop
				## and immediately apply the class to the dummy so the portrait
				## and Save logic both see it. 0 = Auto (derived on Save).
				(eq, ":object", "$cstm_class_selector"),
				
				(troop_set_slot, "$cstm_troop_being_customised", cstm_slot_troop_class_override, ":value"),
				(call_script, "script_kct_apply_troop_class", "$cstm_troop_being_customised", ":dummy", ":value"),
				(assign, "$cstm_class_changed", 1),
				
				(start_presentation, "prsnt_kct_customise_troop"),
			(else_try),
				(eq, ":object", "$cstm_gender_selector"),
				(try_begin),
					(eq, ":value", "$cstm_selected_gender"),
					(assign, ":flipped", 0),
				(else_try),
					(assign, ":flipped", 1),
				(try_end),
				(call_script, "script_kct_flip_subtree", "$cstm_troop_being_customised", ":flipped"),
				(assign, "$cstm_gender_changed", 1),
				(start_presentation, "prsnt_kct_customise_troop"),
			(else_try),
				(troop_slot_eq, "trp_cstm_overlay_is_attribute_box", ":object", 1),
				(eq, "$cstm_troop_design_locked", 0),
				
				(troop_get_slot, ":attribute", "trp_cstm_overlay_attribute", ":object"),
				(call_script, "script_kct_dummy_set_attribute", ":dummy", ":attribute", ":value"),
				(start_presentation, "prsnt_kct_customise_troop"),
			(else_try),
				# PROFICIENCY CHANGED
				(troop_slot_eq, "trp_cstm_overlay_is_proficiency_box", ":object", 1),
				(eq, "$cstm_troop_design_locked", 0),
				
				(troop_get_slot, ":proficiency", "trp_cstm_overlay_proficiency", ":object"),
				(call_script, "script_kct_dummy_set_proficiency", ":dummy", ":proficiency", ":value"),
				(start_presentation, "prsnt_kct_customise_troop"),
			(else_try),
				(troop_slot_eq, "trp_cstm_overlay_is_skill_box", ":object", 1),
				(eq, "$cstm_troop_design_locked", 0),
				
				(troop_get_slot, ":skill", "trp_cstm_overlay_skill", ":object"),
				(call_script, "script_kct_dummy_set_skill", ":dummy", ":skill", ":value"),
				(start_presentation, "prsnt_kct_customise_troop"),
			(else_try),
				(eq, ":object", "$cstm_customise_troop_save"),
				
				# Mark this node as configured so its children unlock (spec §7).
				(troop_set_slot, "$cstm_troop_being_customised", cstm_slot_troop_configured, 1),
				
				# Saving a child locks the parent: its stat boxes freeze so the
				# inherited baseline can never be lowered (spec §7). Equipment and
				# name stay editable.
				(troop_get_slot, ":parent", "$cstm_troop_being_customised", cstm_slot_troop_base_troop),
				(try_begin),
					(gt, ":parent", 0),
					
					(troop_set_slot, ":parent", cstm_slot_troop_design_lock, 1),
				(try_end),
				
				(try_begin),
					(call_script, "script_kct_cf_troop_equipments_are_different", "$cstm_troop_being_customised", ":dummy"),
					
					(troop_set_slot, "$cstm_troop_being_customised", cstm_slot_troop_equipment_modified, 1),
				(try_end),
				
				## CLASS: honour the store's Class selector override when set
				## (1 = infantry, 2 = cavalry, 3 = archers); otherwise derive from
				## equipment as before (horse -> cavalry, bow/crossbow -> archers,
				## else infantry).
				(troop_get_slot, ":class_override", "$cstm_troop_being_customised", cstm_slot_troop_class_override),
				(call_script, "script_kct_apply_troop_class", "$cstm_troop_being_customised", ":dummy", ":class_override"),
				(assign, "$cstm_class_changed", 0),
				(assign, "$cstm_gender_changed", 0),
				
				(troop_sort_inventory, "$cstm_troop_being_customised"),
				(troop_equip_items, "$cstm_troop_being_customised"),				
				
				(call_script, "script_kct_replace_custom_troop_with_dummy", "$cstm_troop_being_customised"),
				(troop_get_slot, ":dummy", "$cstm_troop_being_customised", cstm_slot_troop_dummy),
				
				(troop_get_upgrade_troop, ":upgrade", "$cstm_troop_being_customised", 0),
				(try_begin),
					(gt, ":upgrade", 0),
					
				(call_script, "script_kct_troop_tree_copy_inventory_if_unmodified", ":upgrade", ":dummy"),
					
					(troop_get_upgrade_troop, ":upgrade", "$cstm_troop_being_customised", 1),
					(gt, ":upgrade", 0),
					
				(call_script, "script_kct_troop_tree_copy_inventory_if_unmodified", ":upgrade", ":dummy"),
			(try_end),
			
			(str_store_troop_name, s0, ":dummy"),
				(troop_set_name, "$cstm_presentation_troop", s0),
				(str_store_troop_name_plural, s0, ":dummy"),
				(troop_set_plural_name, "$cstm_presentation_troop", s0),
				
				(display_message, "@Changes saved"),
				(assign, "$cstm_name_changed", 0),
				
				(start_presentation, "prsnt_cstm_create_troop_tree"),
			(else_try),
				(eq, ":object", "$cstm_customise_troop_reset"),
				
				(display_message, "@Changes discarded"),
				(assign, "$cstm_name_changed", 0),
				(assign, "$cstm_class_changed", 0),
				(assign, "$cstm_gender_changed", 0),
				(call_script, "script_kct_flip_subtree", "$cstm_troop_being_customised", "$cstm_gender_original"),
				(troop_set_slot, "$cstm_troop_being_customised", cstm_slot_troop_class_override, "$cstm_class_override_original"),
				(call_script, "script_kct_copy_custom_troop_to_dummy", "$cstm_troop_being_customised"),
				(troop_get_slot, ":dummy", "$cstm_troop_being_customised", cstm_slot_troop_dummy),
				(call_script, "script_kct_apply_troop_class", "$cstm_troop_being_customised", ":dummy", "$cstm_class_override_original"),
				
				(str_store_troop_name, s0, "$cstm_presentation_troop"),
				(troop_set_name, ":dummy", s0),
				(str_store_troop_name_plural, s0, "$cstm_presentation_troop"),
				(troop_set_plural_name, ":dummy", s0),
				
				(start_presentation, "prsnt_kct_customise_troop"),
			(else_try),
				(eq, ":object", "$cstm_customise_troop_exit"),
				
				(try_begin),
					(eq, "$cstm_class_changed", 1),
					
					(troop_set_slot, "$cstm_troop_being_customised", cstm_slot_troop_class_override, "$cstm_class_override_original"),
					(troop_get_slot, ":dummy", "$cstm_troop_being_customised", cstm_slot_troop_dummy),
					(call_script, "script_kct_apply_troop_class", "$cstm_troop_being_customised", ":dummy", "$cstm_class_override_original"),
				(try_end),
				(try_begin),
					(eq, "$cstm_gender_changed", 1),
					(call_script, "script_kct_flip_subtree", "$cstm_troop_being_customised", "$cstm_gender_original"),
				(try_end),
				
				(assign, "$cstm_item_modifier_selected", 0),
				(assign, "$cstm_item_page_no", 0),
				(start_presentation, "prsnt_cstm_create_troop_tree"),
			(else_try),
				(eq, ":object", "$cstm_troop_image"),
				(eq, "$cheat_mode", 1),
				
				(assign, ":num_troops", 1),
				(try_begin),
					(this_or_next|key_is_down, key_left_shift),
					(key_is_down, key_right_shift),
					
					(assign, ":num_troops", 10),
				(try_end),
				
				(party_add_members, "p_main_party", "$cstm_troop_being_customised", ":num_troops"),
				(str_store_troop_name_by_count, s0, "$cstm_troop_being_customised", reg0),
				(display_message, "@{reg0} {s0} added to party"),
			(try_end),
		]),
	])
)

# Store-specific load-trigger additions (ported from the custom_troops modmerge):
# item-type combo entries, the active-fighting-skill grid and the points rows.
_kct_customise_load = kct_customise_core[3][0][1]

for item_type, string in cstm_item_type_strings.iteritems():
	_kct_customise_load.append((str_store_string, s0, "@" + string))
	_kct_customise_load.append((overlay_add_item, "$cstm_store_item_type_selector", s0))
_kct_customise_load.extend([
	(store_sub, ":array_offset", "$cstm_items_array", cstm_items_arrays_begin),
	(overlay_set_val, "$cstm_store_item_type_selector", ":array_offset"),
])

_kct_customise_load.append((set_container_overlay, "$cstm_stats_container"))
skill_index = 0
for skill in ACTIVE_FIGHTING_SKILLS[::-1]:
	skill_ref = "skl_" + skill[0]
	base_attribute = skill[2] & 0xf
	_kct_customise_load.extend([
		(call_script, "script_kct_get_grid_position", skill_index, len(ACTIVE_FIGHTING_SKILLS), KCT_STATS_SKL_CONT_WIDTH, KCT_STATS_SKL_COL_WIDTH, KCT_STATS_SKL_ROW_HEIGHT),
		(assign, ":pos_x", reg0),
		(store_add, ":pos_y", reg1, KCT_STATS_GAP_Y + KCT_STATS_PROF_SECTION_HEIGHT + KCT_CLASS_SECTION_HEIGHT),
		
		(call_script, "script_kct_print_skill_to_s0", skill_ref),
		(call_script, "script_kct_create_text_overlay", "str_s0", ":pos_x", ":pos_y", KCT_STATS_SKL_TEXT_SIZE, KCT_STATS_SKL_COL_WIDTH, KCT_STATS_SKL_ROW_HEIGHT, tf_left_align),
		(overlay_set_tooltip, reg1, "str_kct_tip_" + skill[0]),
		
		(val_add, ":pos_x", KCT_STATS_SKL_COL_WIDTH - 75),
		
		(store_skill_level, ":curr_val", skill_ref, ":dummy"),
		
		(call_script, "script_kct_troop_get_skill_min_from_points", "$cstm_troop_being_customised", skill_ref),
		(assign, ":min", reg0),
		(call_script, "script_kct_troop_get_skill_min_from_tree", "$cstm_troop_being_customised", "$cstm_troop_being_customised", skill_ref),
		(val_max, ":min", reg0),
		
		(call_script, "script_kct_get_skill_points_available", ":dummy", skill_ref),
		(store_add, ":max", ":curr_val", reg0),
		(val_add, ":max", 1),
		
		(store_attribute_level, ":attribute_cap", ":dummy", base_attribute),
		(val_div, ":attribute_cap", 3),
		(val_add, ":attribute_cap", 1),
		(val_min, ":max", ":attribute_cap"),
		
		(try_begin,),
			(ge, ":curr_val", ":attribute_cap"),
			
			(store_sub, ":difference", ":attribute_cap", ":curr_val"),
			(val_sub, ":difference", 1),
			(troop_raise_skill, ":dummy", skill_ref, ":difference"),
			(store_skill_level, ":curr_val", skill_ref, ":dummy"),
			(assign, reg0, ":curr_val"),
			(display_message, "@{s0} reduced to {reg0}"),
		(try_end,),
		
		(try_begin,),
			(lt, ":curr_val", ":min"),
			
			(call_script, "script_kct_print_skill_to_s0", skill_ref),
			(assign, reg0, ":min"),
			(assign, reg1, ":curr_val"),
			(display_message, "@{s0} minimum was being set to {reg0}, but current value is {reg1}"),
			(assign, ":min", ":curr_val"),
		(try_end,),
		
		(try_begin,),
			(ge, ":curr_val", ":max"),
			
			(call_script, "script_kct_print_skill_to_s0", skill_ref),
			(assign, reg0, ":max"),
			(assign, reg1, ":curr_val"),
			(display_message, "@{s0} maximum was being set to {reg0}, but current value is {reg1}"),
			(store_add, ":max", ":curr_val", 1),
		(try_end,),
		
		(call_script, "script_kct_create_number_box_overlay", ":pos_x", ":pos_y", ":min", ":max"),
		(troop_set_slot, "trp_cstm_overlay_is_skill_box", reg1, 1),
		(troop_set_slot, "trp_cstm_overlay_skill", reg1, skill_ref),
		(overlay_set_val, reg1, ":curr_val"),
	])
	skill_index += 1

_kct_customise_load.extend([
	(call_script, "script_kct_get_skill_points_available", ":dummy"),
	(str_store_string, s0, "@Skill points: {reg0}"),
	(call_script, "script_kct_create_text_overlay", "str_s0", 0, KCT_STATS_GAP_Y + KCT_STATS_PROF_SECTION_HEIGHT + KCT_STATS_SKL_GRID_HEIGHT + KCT_CLASS_SECTION_HEIGHT, KCT_STATS_POINTS_TEXT_SIZE, KCT_STATS_POINTS_COL_WIDTH, KCT_STATS_POINTS_ROW_HEIGHT, tf_left_align),
	
	(set_container_overlay, -1),
])

new_customise_presentation = kct_customise_core
