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

update_other_taverngoers_scripts = [
("update_other_taverngoers",
  [
	(store_random_in_range, ":fight_promoter_tavern", towns_begin, towns_end),
	(troop_set_slot, "trp_fight_promoter", slot_troop_cur_center, ":fight_promoter_tavern"),

	(store_random_in_range, ":belligerent_drunk_tavern", towns_begin, towns_end),
	(troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, ":belligerent_drunk_tavern"),
	])
]
