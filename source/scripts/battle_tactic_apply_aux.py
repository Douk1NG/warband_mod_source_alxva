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

battle_tactic_apply_aux_scripts = [
# Replacement script for battle_tactic_init_aux to switch between using
# M&B Standard AI with changes for formations and original based on
# NOTE: original script "battle_tactic_apply_aux" should be renamed to "orig_battle_tactic_apply_aux"
# constant formation_native_ai_use_formation ( 0: original, 1: use formation )
# script_battle_tactic_apply_aux
# Input: team_no, battle_tactic
# Output: battle_tactic
("battle_tactic_apply_aux",
	[
	  (store_script_param, ":team_no", 1),
	  (store_script_param, ":battle_tactic", 2),
	  (try_begin),
		(eq, formation_native_ai_use_formation, 1),
		(call_script, "script_formation_battle_tactic_apply_aux", ":team_no", ":battle_tactic"),
	  (else_try),
		(call_script, "script_orig_battle_tactic_apply_aux", ":team_no", ":battle_tactic"),
	  (try_end),
  ])
]
