# ======================================================================
# SHARED DEPENDENCY
# Entity: change_player_relation_with_faction (script)
# Called by menus in 5 domains: battle, dickplomacy, diplomacy, kingdom_management, village
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

change_player_relation_with_faction_scripts = [
# script_get_center_faction_relation_including_player
# Input: arg1 = faction_no, arg2 = relation difference
# Output: none
("change_player_relation_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":difference"),

      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (assign, reg1, ":player_relation"),
      (val_add, ":player_relation", ":difference"),
      (assign, reg2, ":player_relation"),
      (set_relation, ":faction_no", "fac_player_faction", ":player_relation"),
      (set_relation, ":faction_no", "fac_player_supporters_faction", ":player_relation"),

      (try_begin),
        (le, ":player_relation", -50),
        (unlock_achievement, ACHIEVEMENT_OLD_DIRTY_SCOUNDREL),
      (try_end),


      (str_store_faction_name_link, s1, ":faction_no"),
      #SB : colorize message, although faction color might be better
      (try_begin),
        (gt, ":difference", 0),
        (display_message, "str_faction_relation_increased", message_positive),
      (else_try),
        (lt, ":difference", 0),
        (display_message, "str_faction_relation_detoriated", message_negative),
      (try_end),
      (call_script, "script_update_all_notes"),
      ])
]
