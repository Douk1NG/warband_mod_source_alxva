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

update_troop_location_notes_prisoned_scripts = [
("update_troop_location_notes_prisoned",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":capturer_faction_no", 2),
      ##diplomacy start+ use gender script
      #(troop_get_type, reg1, ":troop_no"),
	  (call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
      (assign, reg1, reg0),
	  ##diplomacy end+
      (str_store_faction_name_link, s1, ":capturer_faction_no"),

      (add_troop_note_from_sreg, ":troop_no", 2, "str_reg1shehe_is_prisoner_of_s1", 1),
    ])
]
