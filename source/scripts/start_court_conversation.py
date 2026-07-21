# ======================================================================
# SHARED DEPENDENCY
# Entity: start_court_conversation (script)
# Called by menus in 2 domains: battle, town
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

start_court_conversation_scripts = [
("start_court_conversation",
    [
        (store_script_param, ":conversation_troop", 1),
        (store_script_param, ":center_no", 2),

        (party_get_slot, ":conversation_scene", ":center_no", slot_town_castle),
        (modify_visitors_at_site, ":conversation_scene"),
        (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", 0, af_override_horse),

        #clear flags for actual courtly conversations?
        (store_random_in_range, ":entry_no", 16, 32),
        (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", ":entry_no", af_override_horse),
        (try_begin),
          (troop_is_hero, ":conversation_troop"),
          (set_visitor, ":entry_no", ":conversation_troop"),
        (else_try),
          (store_script_param, ":troop_dna", 3),
          (set_visitor, ":entry_no", ":conversation_troop", ":troop_dna"),
        (try_end),
        (set_jump_mission,"mt_conversation_encounter"),
        (jump_to_scene, ":conversation_scene"),
        (change_screen_map_conversation, ":conversation_troop"),
    ])
]
