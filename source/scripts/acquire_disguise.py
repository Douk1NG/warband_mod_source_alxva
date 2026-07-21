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

acquire_disguise_scripts = [
("acquire_disguise", [
      (store_script_param, ":disguise", 1),
      (troop_get_slot, ":cur_disguise", "trp_player", slot_troop_player_disguise_sets),
      (val_or, ":cur_disguise", ":disguise"),
      (troop_set_slot, "trp_player", slot_troop_player_disguise_sets, ":cur_disguise"),
      (call_script, "script_get_disguise_string", ":disguise", 0),
      # (str_store_string, s0, reg0),
      (display_message, "@Acquired {s0}'s clothing", message_alert),
      ])
]
