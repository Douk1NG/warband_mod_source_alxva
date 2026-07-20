# ======================================================================
# SHARED DEPENDENCY
# Entity: start_courtyard_conversation (script)
# Called by menus in 2 domains: castle, siege
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

start_courtyard_conversation_scripts = [
("start_courtyard_conversation",
	[
      (store_script_param, ":conversation_troop", 1),
      (store_script_param, ":center_no", 2),

      (party_get_slot, ":conversation_scene", ":center_no", slot_town_center), #castle's exterior
      (modify_visitors_at_site, ":conversation_scene"),
      (reset_visitors),
      (try_begin), #player vs troop, not much processing
        (neg|troop_is_hero, ":conversation_troop"),

      (else_try), #talking to lords, compare relative positions
        (assign, ":supplicant", "trp_player"),
        (store_faction_of_party, ":faction_no", ":center_no"),
        (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
        (assign, ":player_standing", reg0),
        (call_script, "script_dplmc_get_troop_standing_in_faction", ":conversation_troop", ":faction_no"),
        (assign, ":other_troop_standing", reg0),

        #23 : castle guard (adjacent), 2: lord's hall door
        (assign, ":entry_lower", 23),
        (assign, ":entry_upper", 2),
        #overwrite standing if center owned
        (try_begin),
          (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
          (assign, ":player_standing", 9999),
        (else_try),
          (party_slot_eq, ":center_no", slot_town_lord, ":conversation_troop"),
          (assign, ":other_troop_standing", 9999),
        (else_try), #strangers, use default street entry point (this may be outside in towns, 0 preferred)
          (this_or_next|eq, ":player_standing", DPLMC_FACTION_STANDING_UNAFFILIATED),
          (eq, ":other_troop_standing", DPLMC_FACTION_STANDING_UNAFFILIATED),
          (assign, ":entry_lower", 1),
        (try_end),

        (try_begin), #player is usually supplicant
          (gt, ":player_standing", ":other_troop_standing"),
          (assign, ":supplicant", ":conversation_troop"),
          (assign, ":conversation_troop", "trp_player"),
        (else_try),
          (is_between, ":center_no", towns_begin, towns_end),
          (eq, ":player_standing", ":other_troop_standing"),
          (assign, ":entry_upper", 27),
          (assign, ":entry_lower", 28),
        (try_end),
      (try_end),

      (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", ":entry_lower", af_override_horse|af_override_head|af_override_weapons),
      (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", ":entry_upper", af_override_horse|af_override_fullhelm),
      (set_visitor, ":entry_lower", ":supplicant"),
      (set_visitor, ":entry_upper", ":conversation_troop"),

      (set_jump_mission,"mt_conversation_encounter"),
      (jump_to_scene, ":conversation_scene"),
      (change_screen_map_conversation, ":conversation_troop"),
    ])
]
