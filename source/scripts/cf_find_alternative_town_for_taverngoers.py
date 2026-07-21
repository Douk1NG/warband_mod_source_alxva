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

cf_find_alternative_town_for_taverngoers_scripts = [
#native functionality to increase tavern diversity
("cf_find_alternative_town_for_taverngoers",
  [
      (store_script_param_1, ":town_no"),
      (store_script_param_2, ":adder"),
      (store_add, ":alternative_town", ":town_no", ":adder"), #should really randomize this

      # (store_sub, ":num_towns", towns_end, towns_begin),
      (try_begin),
        (ge, ":alternative_town", towns_end),
        (val_sub, ":alternative_town", towns_end),
        (val_add, ":alternative_town", towns_begin),
      (else_try),
        (lt, ":alternative_town", towns_begin),
        (val_add, ":alternative_town", towns_end),
      (try_end),
      ##diplomacy start+
      #The above code makes assumptions about the number of towns that might not be true on other maps.
      #Changing it to support variable sizes would not be hard, but I'm not convinced that it is so
      #desirable in the first place.
      (is_between, ":alternative_town", towns_begin, towns_end),
      # (party_slot_eq, ":alternative_town", slot_party_type, spt_town),
      (assign, reg0, ":alternative_town"),
  ])
]
