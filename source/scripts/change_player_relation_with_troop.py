# ======================================================================
# SHARED DEPENDENCY
# Entity: change_player_relation_with_troop (script)
# Called by menus in 7 domains: battle, castle, cheats, kingdom_management, reports, town, village
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

change_player_relation_with_troop_scripts = [
("change_player_relation_with_troop",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":difference"),

      (try_begin),
        (neq, ":troop_no", "trp_player"),
        (neg|is_between, ":troop_no", soldiers_begin, soldiers_end),
        ##diplomacy start+
		  (neq, ":troop_no", "trp_kingdom_heroes_including_player_begin"),
		  #(neq, ":troop_no", -1),#OLD
		  (ge, ":troop_no", 1),#NEW
        ##diplomacy end+
        (neq, ":difference", 0),
        (call_script, "script_troop_get_player_relation", ":troop_no"),
        (assign, ":old_effective_relation", reg0),
        (troop_get_slot, ":player_relation", ":troop_no", slot_troop_player_relation),
        (val_add, ":player_relation", ":difference"),
        (val_clamp, ":player_relation", -100, 101),
        (try_begin),
          (troop_set_slot, ":troop_no", slot_troop_player_relation, ":player_relation"),

          (try_begin),
            (le, ":player_relation", -50),
            (unlock_achievement, ACHIEVEMENT_OLD_DIRTY_SCOUNDREL),
          (try_end),

          (str_store_troop_name_link, s1, ":troop_no"),
          (call_script, "script_troop_get_player_relation", ":troop_no"),
          (assign, ":new_effective_relation", reg0),
          (neq, ":old_effective_relation", ":new_effective_relation"),
          (assign, reg1, ":old_effective_relation"),
          (assign, reg2, ":new_effective_relation"),
          (try_begin),
			##diplomacy start+ Suppress this message for dead people except in cheat mode
            (lt, "$cheat_mode", 1),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_dead),
			(neq, ":troop_no", "$g_talk_troop"),
		  (else_try),
		  ##diplomacy end+
            (gt, ":difference", 0),
            (display_message, "str_troop_relation_increased", message_positive),
          (else_try),
            (lt, ":difference", 0),
            (display_message, "str_troop_relation_detoriated", message_negative),
          (try_end),
          (try_begin),
            (eq, ":troop_no", "$g_talk_troop"),
            (assign, "$g_talk_troop_relation", ":new_effective_relation"),
            (call_script, "script_setup_talk_info"),
          (try_end),
          (call_script, "script_update_troop_notes", ":troop_no"),
        (try_end),
      (try_end),
  ])
]
