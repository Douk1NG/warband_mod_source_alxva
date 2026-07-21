# ======================================================================
# SHARED DEPENDENCY
# Entity: lift_siege (script)
# Called by menus in 2 domains: castle, siege
# ======================================================================

# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

lift_siege_scripts = [
# script_lift_siege
# Input: arg1 = center_no, arg2 = display_message
# Output: none
#called from triggers
("lift_siege",
    [
      (store_script_param, ":center_no", 1),
      (store_script_param, ":display_message", 2),
      (party_set_slot, ":center_no", slot_center_is_besieged_by, -1), #clear siege
      (call_script, "script_village_set_state",  ":center_no", 0), #clear siege flag
      (try_begin),
        (eq, ":center_no", "$g_player_besiege_town"),
        (assign, "$g_siege_method", 0), #remove siege progress
      (try_end),
      (try_begin),
        (eq, ":display_message", 1),
        (str_store_party_name_link, s3, ":center_no"),
        (display_message, "@{s3} is no longer under siege."),
      (try_end),

      #SB : ideally we deal with post-conquest here but this is also called for cancelled sieges
      ])
]
