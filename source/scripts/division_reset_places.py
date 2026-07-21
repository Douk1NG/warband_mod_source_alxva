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

division_reset_places_scripts = [
("division_reset_places", [
      (assign, "$next_cavalry_place", formation_minimum_spacing_horse_width),	#first spot RIGHT of the player
      (assign, "$next_archer_place", 1000),	#first spot 10m FRONT of the player
      (assign, "$next_infantry_place", -1 * formation_minimum_spacing_horse_width),	#first spot LEFT of the player
  ])
]
