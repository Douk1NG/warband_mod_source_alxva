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

change_player_controversy_scripts = [
("change_player_controversy",
    [
      (store_script_param_1, ":controversy_dif"),
	  (troop_set_slot, "trp_player", slot_troop_controversy, ":controversy_dif"),
      (try_begin),
        (lt, ":controversy_dif", 0),
        (display_message, "@Things cool down.", message_positive),
      (else_try),
        (gt, ":controversy_dif", 0),
        (display_message, "@Rumors will certianly spread over this.", message_negative),
      (try_end),
  ])
]
