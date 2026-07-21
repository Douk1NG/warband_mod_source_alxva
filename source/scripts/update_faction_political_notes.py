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

update_faction_political_notes_scripts = [
("update_faction_political_notes",
    [(store_script_param, ":faction_no", 1),

	(call_script, "script_evaluate_realm_stability", ":faction_no"),
    (add_faction_note_from_sreg, ":faction_no", 2, "str_instability_reg0_of_lords_are_disgruntled_reg1_are_restless", 0),
	])
]
