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

default_division_placements_scripts = [
("default_division_placements", [
      (try_for_range, ":division", 0, 9),
        (class_is_listening_order, "$fplayer_team_no", ":division"),
        (store_add, ":slot", slot_faction_d0_mem_relative_x_flag, ":division"),	#use as flag
        (faction_set_slot, "fac_player_faction", ":slot", 0),

        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_ge, "$fplayer_team_no", ":slot", 1),
        (store_add, ":slot", slot_team_d0_type, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (call_script, "script_str_store_division_type_name", s1, ":value"),
        (store_add, reg0, ":division", 1),
        (display_message, "@The placement of {s1} division {reg0} set to default."),
      (try_end),])
]
