# ======================================================================
# SHARED DEPENDENCY
# Entity: change_troop_renown (script)
# Called by menus in 12 domains: battle, captivity, castle, character_creation, cheats, dickplomacy, diplomacy, notifications, taxes, tournament, town, village
# ======================================================================

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

change_troop_renown_scripts = [
("change_troop_renown",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":renown_change"),

      (troop_get_slot, ":old_renown", ":troop_no", slot_troop_renown),

	  (try_begin),
		(gt, ":renown_change", 0),
		(assign, reg4, ":renown_change"),

		(store_div, ":subtraction", ":old_renown", 200),
	    (val_sub, ":renown_change", ":subtraction"),
	    (val_max, ":renown_change", 0),

	    (eq, ":troop_no", "trp_player"),
	    (assign, reg5, ":renown_change"),

		(eq, "$cheat_mode", 1),
	    (display_message, "str_renown_change_of_reg4_reduced_to_reg5_because_of_high_existing_renown"),
	  (try_end),

      (store_add, ":new_renown", ":old_renown", ":renown_change"),
      (val_max, ":new_renown", 0),
      (troop_set_slot, ":troop_no", slot_troop_renown, ":new_renown"),

      (try_begin),
        (eq, ":troop_no", "trp_player"),

		(try_begin),
		  (ge, ":new_renown", 50),

          (try_begin),
            (troop_get_type, ":is_female", "trp_player"),
            (eq, ":is_female", 1),
            (unlock_achievement, ACHIEVEMENT_TALK_OF_THE_TOWN),
          (try_end),
		(try_end),

        # (str_store_troop_name, s1, ":troop_no"),
        (assign, reg12, ":renown_change"),
        (val_abs, reg12),
        (try_begin),
         (gt, ":renown_change", 0),
         (display_message, "@You gained {reg12} renown.", message_positive),
        (else_try),
          (lt, ":renown_change", 0),
          (display_message, "@You lose {reg12} renown.", message_negative),
        (try_end),
      (try_end),
      (call_script, "script_update_troop_notes", ":troop_no"),
  ])
]
