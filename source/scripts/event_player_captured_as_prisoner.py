# ======================================================================
# SHARED DEPENDENCY
# Entity: event_player_captured_as_prisoner (script)
# Called by menus in 2 domains: captivity, dickplomacy
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

event_player_captured_as_prisoner_scripts = [
("event_player_captured_as_prisoner",
    [
        (try_begin),
          (check_quest_active, "qst_raid_caravan_to_start_war"),
          (neg|check_quest_concluded, "qst_raid_caravan_to_start_war"),
          (quest_get_slot, ":quest_target_faction", "qst_raid_caravan_to_start_war", slot_quest_target_faction),
          (store_faction_of_party, ":capturer_faction", "$capturer_party"),
          (eq, ":quest_target_faction", ":capturer_faction"),
          (call_script, "script_fail_quest", "qst_raid_caravan_to_start_war"),
        (try_end),
        #Removing followers of the player
        (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
		  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
          (gt, ":party_no", 0),
          (party_is_active, ":party_no"),
          (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
          (party_slot_eq, ":party_no", slot_party_ai_object, "p_main_party"),
          (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
          (assign, "$g_recalculate_ais", 1),
        (try_end),
     ])
]
