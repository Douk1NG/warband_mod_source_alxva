# ======================================================================
# SHARED DEPENDENCY
# Entity: setup_troop_meeting (script)
# Called by menus in 4 domains: battle, captivity, castle, town
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

setup_troop_meeting_scripts = [
("setup_troop_meeting",
    [
      (store_script_param_1, ":meeting_troop"),
      (store_script_param_2, ":troop_dna"),
      (call_script, "script_get_meeting_scene"),
      (assign, ":meeting_scene", reg0),
      (modify_visitors_at_site,":meeting_scene"),
      (reset_visitors),
      (set_visitor,0,"trp_player"),
	  (try_begin),
		(gt, ":troop_dna", -1),
        (troop_set_slot, "trp_temp_array_c", 17, ":troop_dna"),
        (set_visitor,17,":meeting_troop",":troop_dna"),
	  (else_try),
        (set_visitor,17,":meeting_troop"),
	  (try_end),
      (set_jump_mission,"mt_conversation_encounter"),
      (jump_to_scene,":meeting_scene"),
      (change_screen_map_conversation, ":meeting_troop"),
  ])
]
