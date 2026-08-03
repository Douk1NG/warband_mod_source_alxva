# -*- coding: cp1254 -*-
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from header_items import *
from module_constants import *

from kingdom_custom_troop_tree_creator_troops import PRESET_4_UNITS


class P4LabelDragTool:
	"""Drag tool for tuning the preset-4 label positions in-game.

	Self-contained copy of the drag tool logic, specialised for the name labels:
	a left press on a registered label starts a drag that moves it with the mouse
	and records the delta vs its base position; the Snapshot button prints
	paste-ready "P4L <node>: (dx,dy)," lines for P4_LABEL_MANUAL.

	Each instance owns an exclusive offset (slot_base) into the shared temp
	arrays trp_temp_array_a/b/c/d and its own globals (prefixed $<name>_*), so
	multiple tools can coexist in one presentation.

	Slot layout (item-based, so every slot index is a compile-time constant;
	offsets are relative to slot_base):
	  A[base + item]     = overlay id
	  B[base + item]     = base x
	  C[base + item]     = base y
	  D[base + 2*item]   = current dx
	  D[base + 2*item+1] = current dy
	"""

	def __init__(self, name, slot_base, num_items):
		self.name = name
		self.base = slot_base
		self.num_items = num_items
		self.dragging = "$%s_dragging" % name
		self.drag_overlay = "$%s_drag_overlay" % name
		self.drag_item = "$%s_drag_item" % name
		self.drag_base_x = "$%s_drag_base_x" % name
		self.drag_base_y = "$%s_drag_base_y" % name
		self.snapshot_button = "$%s_snapshot_button" % name
		self.readout = "$%s_readout" % name

	def register(self, item, overlay, base_x, base_y, dx, dy):
		"""Ops to register a freshly created overlay (id in `overlay`) as a
		draggable item with the given base position and initial delta."""
		base = self.base
		return [
			(troop_set_slot, "trp_temp_array_a", base + item, overlay),
			(troop_set_slot, "trp_temp_array_b", base + item, base_x),
			(troop_set_slot, "trp_temp_array_c", base + item, base_y),
			(troop_set_slot, "trp_temp_array_d", base + 2 * item, dx),
			(troop_set_slot, "trp_temp_array_d", base + 2 * item + 1, dy),
		]

	def reset(self):
		"""Ops to clear the tool's slots and globals on presentation load."""
		base = self.base
		ops = []
		for item in range(self.num_items):
			ops.append((troop_set_slot, "trp_temp_array_a", base + item, -1))
			ops.append((troop_set_slot, "trp_temp_array_b", base + item, 0))
			ops.append((troop_set_slot, "trp_temp_array_c", base + item, 0))
			ops.append((troop_set_slot, "trp_temp_array_d", base + 2 * item, 0))
			ops.append((troop_set_slot, "trp_temp_array_d", base + 2 * item + 1, 0))
		ops.append((assign, self.dragging, 0))
		return ops

	def create_readout(self, text, pos, size, width, height=50):
		"""Ops to create the live drag readout text overlay."""
		return [
			(str_store_string, s0, "@" + text),
			(call_script, "script_kct_create_text_overlay", "str_s0", pos[0], pos[1], size, width, height, tf_left_align),
			(assign, self.readout, reg1),
		]

	def create_snapshot_button(self, pos, size_x=200, size_y=50):
		"""Ops to create the Snapshot button with an explicit clickable size."""
		return [
			(str_store_string, s0, "@Snapshot"),
			(call_script, "script_kct_create_game_button_overlay", "str_s0", pos[0], pos[1]),
			(assign, self.snapshot_button, reg1),
			(position_set_x, pos1, size_x),
			(position_set_y, pos1, size_y),
			(overlay_set_size, self.snapshot_button, pos1),
		]

	def mouse_press_ops(self):
		"""Ops for the presentation mouse_press trigger: a left press on any
		registered overlay starts a drag."""
		return [
			(try_begin,),
			(eq, ":mouse_state", 0),
			(try_for_range, ":item", 0, self.num_items),
			(store_add, reg4, self.base, ":item"),
			(troop_get_slot, ":ov", "trp_temp_array_a", reg4),
			(eq, ":ov", ":object"),
			(assign, self.drag_overlay, ":object"),
			(assign, self.drag_item, ":item"),
			(troop_get_slot, self.drag_base_x, "trp_temp_array_b", reg4),
			(troop_get_slot, self.drag_base_y, "trp_temp_array_c", reg4),
			(assign, self.dragging, 1),
			(try_end,),
			(try_end,),
		]

	def run_ops(self):
		"""Ops for the presentation run trigger: while the left button is held
		the pressed overlay follows the mouse and its delta vs base is recorded;
		on release the drag stops."""
		return [
			(try_begin,),
			(eq, self.dragging, 1),
			(key_is_down, key_left_mouse_button),
			(mouse_get_position, pos0),
			(overlay_set_position, self.drag_overlay, pos0),
			(position_get_x, reg0, pos0),
			(position_get_y, reg1, pos0),
			(store_sub, reg2, reg0, self.drag_base_x),
			(store_sub, reg3, reg1, self.drag_base_y),
			(assign, reg4, self.drag_item),
			(store_mul, ":slot", self.drag_item, 2),
			(val_add, ":slot", self.base),
			(troop_set_slot, "trp_temp_array_d", ":slot", reg2),
			(val_add, ":slot", 1),
			(troop_set_slot, "trp_temp_array_d", ":slot", reg3),
			(str_store_string, s0, "@P4L n{reg4}: d=({reg2},{reg3})  x{reg0} y{reg1}"),
			(overlay_set_text, self.readout, "str_s0"),
			(else_try,),
			(eq, self.dragging, 1),
			(assign, self.dragging, 0),
			(try_end,),
		]

	def snapshot_event_ops(self, header):
		"""Ops for the presentation event trigger: the Snapshot button prints
		one paste-ready "P4L <node>: (dx,dy)," line per item, then confirms on
		the readout."""
		ops = [
			(eq, ":object", self.snapshot_button),
			(str_store_string, s0, "@" + header),
			(display_message, s0),
		]
		for item in range(self.num_items):
			ops.append((troop_get_slot, reg0, "trp_temp_array_d", self.base + 2 * item))
			ops.append((troop_get_slot, reg1, "trp_temp_array_d", self.base + 2 * item + 1))
			ops.append((str_store_string, s0, "@P4L %d: ({reg0},{reg1})," % item))
			ops.append((display_message, s0))
		ops.append((str_store_string, s0, "@Snapshot: %d lines in message feed" % self.num_items))
		ops.append((overlay_set_text, self.readout, "str_s0"))
		return ops


# Slot base 10000 stays clear of the low slots used by other presentations and
# of the dummy tool's base 20000; slot numbers go up to 2^20 so this is safe.
p4_label_tool = P4LabelDragTool("p4_labels", 10000, len(PRESET_4_UNITS))
