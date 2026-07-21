# ======================================================================
# SHARED DEPENDENCY
# Entity: start_town_conversation (script)
# Called by menus in 2 domains: diplomacy, town
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

start_town_conversation_scripts = [
#script_calculate_ransom_contribution
#input: center's slot no, entry points
#used to talk to various center merchant npcs including guildmaster
("start_town_conversation",
	[
	  (store_script_param, ":troop_slot_no", 1),
	  (store_script_param, ":entry_no", 2),

      (assign, "$talk_context", tc_town_talk),
	  (try_begin),
		(eq, ":troop_slot_no", slot_town_merchant),
		(assign, ":scene_slot_no", slot_town_store),
	  (else_try),
		(eq, ":troop_slot_no", slot_town_tavernkeeper),
		(assign, ":scene_slot_no", slot_town_tavern),
        (assign, "$talk_context", tc_tavern_talk),
	  (else_try),
		(assign, ":scene_slot_no", slot_town_center),
	  (try_end),

	  (party_get_slot, ":conversation_scene", "$current_town", ":scene_slot_no"),
	  (modify_visitors_at_site, ":conversation_scene"),
	  (reset_visitors),
	  (set_visitor, 0, "trp_player"),

	  (try_begin),
		(gt, "$sneaked_into_town", disguise_none),
		(mission_tpl_entry_set_override_flags, "mt_conversation_encounter", 0, af_override_all),
        #SB : use script call
        (call_script, "script_set_disguise_override_items", "mt_conversation_encounter", 0, 0),
	  (else_try),
		(mission_tpl_entry_set_override_flags, "mt_conversation_encounter", 0, af_override_horse),
		(mission_tpl_entry_clear_override_items, "mt_conversation_encounter", 0),
	  (try_end),
	  (party_get_slot, ":conversation_troop", "$current_town", ":troop_slot_no"),
	  (set_visitor, ":entry_no", ":conversation_troop"),
	  (set_jump_mission,"mt_conversation_encounter"),
	  (jump_to_scene, ":conversation_scene"),
	  (change_screen_map_conversation, ":conversation_troop"),
	])
]
