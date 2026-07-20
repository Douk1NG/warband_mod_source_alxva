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

update_troop_location_notes_scripts = [
("update_troop_location_notes",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":see_or_hear", 2),
      (try_begin),
        (call_script, "script_get_information_about_troops_position", ":troop_no", 1),
        (neq, reg0, 0),

        (call_script, "script_search_troop_prisoner_of_party", ":troop_no"),
        (eq, reg0, -1),
        ##diplomacy start+ use gender script
	    #(troop_get_type, reg1, ":troop_no"),
		(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
		(assign, reg1, reg0),
		##diplomacy end+
        (try_begin),
          (eq, ":see_or_hear", 0),
          (add_troop_note_from_sreg, ":troop_no", 2, "@The last time you saw {reg1?her:him}, {s1}", 1),
        (else_try),
          (add_troop_note_from_sreg, ":troop_no", 2, "@The last time you heard about {reg1?her:him}, {s1}", 1),
        (try_end),
      (try_end),
     ])
]
