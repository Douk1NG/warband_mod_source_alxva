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

add_rumor_string_to_troop_notes_scripts = [
("add_rumor_string_to_troop_notes", #parameters from dialog
	[
      (store_script_param, ":object_1", 1),
      (store_script_param, ":object_2", 2),
      (store_script_param, ":string", 3),

      (str_store_troop_name, s10, "$g_talk_troop"),
      (str_store_string_reg, s11, ":string"),

      (store_current_hours, ":hours"),
      (call_script, "script_game_get_date_text", 0, ":hours"),

      (str_store_string, s5, "str_s10_said_on_s1_s11__"),

      (try_begin),
        (is_between, ":object_1", active_npcs_begin, kingdom_ladies_end),
        (troop_get_slot, ":current_rumor_note", ":object_1", slot_troop_current_rumor),
        (val_add, ":current_rumor_note", 1),
        (try_begin),
        # Lav modifications start (custom lord notes)
                  (neg|is_between, ":current_rumor_note", 3, 15), # Was 16 in original Native, thus using notes slot #15 as well. Now it will leave notes slot #15 for custom notes.
        # Lav modifications end (custom lord notes)
          (assign, ":current_rumor_note", 3),
        (try_end),
        (troop_set_slot, ":object_1", slot_troop_current_rumor, ":current_rumor_note"),

        (add_troop_note_from_sreg, ":object_1", ":current_rumor_note", s5, 0), #troop, note slot, string, show

        (try_begin),
          (eq, "$cheat_mode", 1),
          (str_store_troop_name, s3, ":object_1"),
          (assign, reg4, ":current_rumor_note"),
          (display_message, "str_rumor_note_to_s3s_slot_reg4_s5"),
        (try_end),
      (try_end),

      (try_begin),
        (is_between, ":object_2", active_npcs_begin, kingdom_ladies_end),
        (troop_get_slot, ":current_rumor_note", ":object_2", slot_troop_current_rumor),
        (val_add, ":current_rumor_note", 1),
        (try_begin),
# Lav modifications start (custom lord notes)
          (neg|is_between, ":current_rumor_note", 3, 15), # Was 16 in original Native, thus using notes slot #15 as well. Now it will leave notes slot #15 for custom notes.
# Lav modifications end (custom lord notes)
          (assign, ":current_rumor_note", 3),
        (try_end),
        (troop_set_slot, ":object_2", slot_troop_current_rumor, ":current_rumor_note"),

        (add_troop_note_from_sreg, ":object_2", ":current_rumor_note", s5, 0), #troop, note slot, string, show

        (try_begin),
          (eq, "$cheat_mode", 1),
          (str_store_troop_name, s3, ":object_2"),
          (assign, reg4, ":current_rumor_note"),
          (display_message, "str_rumor_note_to_s3s_slot_reg4_s5"),
        (try_end),
      (try_end),
	])
]
