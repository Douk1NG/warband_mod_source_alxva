# ======================================================================
# SHARED DEPENDENCY
# Entity: update_all_notes (script)
# Called by menus in 2 domains: castle, notifications
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

update_all_notes_scripts = [
("update_all_notes",
    [
      (call_script, "script_update_troop_notes", "trp_player"),
      (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
	    (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	    (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive_pretender),
        (call_script, "script_update_troop_notes", ":troop_no"),
      (try_end),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (call_script, "script_update_center_notes", ":center_no"),
      (try_end),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (call_script, "script_update_faction_notes", ":faction_no"),
      (try_end),
    ])
]
