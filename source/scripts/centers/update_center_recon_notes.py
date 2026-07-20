# ======================================================================
# SHARED DEPENDENCY
# Entity: update_center_recon_notes (script)
# Called by menus in 3 domains: diplomacy, town, village
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

update_center_recon_notes_scripts = [
#script_update_center_recon_notes
# INPUT: center_no
# OUTPUT: none
("update_center_recon_notes",
    [(store_script_param, ":center_no", 1),
     (try_begin),
       (this_or_next|is_between, ":center_no", towns_begin, towns_end),
       (is_between, ":center_no", castles_begin, castles_end),
       (party_get_slot, ":center_food_store", ":center_no", slot_party_food_store),
       (call_script, "script_center_get_food_consumption", ":center_no"),
       (assign, ":food_consumption", reg0),
       (store_div, reg6, ":center_food_store", ":food_consumption"),
       (party_collect_attachments_to_party, ":center_no", "p_collective_ally"),
       (party_get_num_companions, reg5, "p_collective_ally"),
       (add_party_note_from_sreg, ":center_no", 1, "@Current garrison consists of {reg5} men.^Has food stock for {reg6} days.", 1),
     (try_end),
     ])
]
