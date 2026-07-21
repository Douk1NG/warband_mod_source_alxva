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

player_formation_end_scripts = [
("player_formation_end", [
      (store_script_param, ":fdivision", 1),

      (call_script, "script_formation_end", "$fplayer_team_no", ":fdivision"),

      (store_add, ":slot", slot_team_d0_type, ":fdivision"),
      (str_store_class_name, s1, ":fdivision"),
      (try_begin),
        (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_infantry),
        (team_slot_eq, "$fplayer_team_no", ":slot", sdt_polearm),
        (display_message, "@{s1}: infantry formation disassembled."),
      (else_try),
        (team_slot_eq, "$fplayer_team_no", ":slot", sdt_archer),
        (display_message, "@{s1}: archer formation disassembled."),
      (else_try),
        (team_slot_eq, "$fplayer_team_no", ":slot", sdt_skirmisher),
        (display_message, "@{s1}: skirmisher formation disassembled."),
      (else_try),
        (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
        (team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
        (display_message, "@{s1}: cavalry formation disassembled."),
      (else_try),
        (display_message, "@{s1}: formation disassembled."),
      (try_end),])
]
