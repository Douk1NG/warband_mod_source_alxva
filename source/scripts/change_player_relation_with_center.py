# ======================================================================
# SHARED DEPENDENCY
# Entity: change_player_relation_with_center (script)
# Called by menus in 8 domains: captivity, center_management, cheats, dickplomacy, diplomacy, taxes, tournament, village
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

change_player_relation_with_center_scripts = [
#script_update_report_to_army_quest_note
# Input: arg1 = party_no, arg2 = relation difference
# Output: none
("change_player_relation_with_center",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":difference"),

      (party_get_slot, ":player_relation", ":center_no", slot_center_player_relation),
      (assign, reg1, ":player_relation"),
      (val_add, ":player_relation", ":difference"),
      (val_clamp, ":player_relation", -100, 100),
      (assign, reg2, ":player_relation"),
      (party_set_slot, ":center_no", slot_center_player_relation, ":player_relation"),

      (try_begin),
        (le, ":player_relation", -50),
        (unlock_achievement, ACHIEVEMENT_OLD_DIRTY_SCOUNDREL),
      (try_end),


      (str_store_party_name_link, s1, ":center_no"),
      (try_begin),
        (gt, ":difference", 0),
        (display_message, "@Your relation with {s1} has improved.", message_positive),
      (else_try),
        (lt, ":difference", 0),
        (display_message, "@Your relation with {s1} has deteriorated.", message_negative),
      (try_end),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (call_script, "script_update_volunteer_troops_in_village", ":center_no"),
      (try_end),

      (try_begin),
        (this_or_next|is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
        (is_between, "$g_talk_troop", mayors_begin, mayors_end),
        ##diplomacy start+
		  #Fix potential bug: don't adjust relations except with *that* center's
		  #mayor.
		  (party_slot_eq, ":center_no", slot_town_elder, "$g_talk_troop"),
	    ##diplomacy end+
        (assign, "$g_talk_troop_relation", ":player_relation"),
        (call_script, "script_setup_talk_info"),
      (try_end),
  ])
]
