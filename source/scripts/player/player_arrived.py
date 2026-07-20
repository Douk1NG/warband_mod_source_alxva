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

player_arrived_scripts = [
("player_arrived",
   [
      # (assign, ":player_faction_culture", "fac_culture_1"),
      #SB : align start faction culture
      (party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
      (party_get_slot, ":player_faction_culture", "$g_starting_town", slot_center_culture),
      (faction_set_slot, "fac_player_supporters_faction",  slot_faction_culture, ":player_faction_culture"),
      (faction_set_slot, "fac_player_faction",  slot_faction_culture, ":player_faction_culture"),
      (party_set_morale, "p_main_party", 100),
    ])
]
