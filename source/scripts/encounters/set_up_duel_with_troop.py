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

set_up_duel_with_troop_scripts = [
("set_up_duel_with_troop", #now the setup is handled through the menu
	[
	  (store_script_param, "$g_duel_troop", 1),
      #SB : change by parameter instead of always one
	  (store_script_param, "$g_start_arena_fight_at_nearest_town", 2),
	  (store_faction_of_troop, ":troop_faction", "$g_duel_troop"),
	  (try_begin),
	    (eq, "$g_start_arena_fight_at_nearest_town", 1),
        # (assign, ":closest_town", -1),
        (assign, ":minimum_dist", 500),
        (try_for_range, ":cur_town", walled_centers_begin, walled_centers_end),
          (store_distance_to_party_from_party, ":dist", ":cur_town", "$g_encountered_party"),
          (lt, ":dist", ":minimum_dist"),
          #make sure it's at least neutral, so we don't fight in an enemy town's arena
          (store_faction_of_party, ":center_faction", ":cur_town"),
          (store_relation, ":relation", ":troop_faction", ":center_faction"),
          (ge, ":relation", 0),
          (assign, ":minimum_dist", ":dist"),
          (assign, "$g_start_arena_fight_at_nearest_town", ":cur_town"),
        (try_end),
	  (try_end),
	  (unlock_achievement, ACHIEVEMENT_PUGNACIOUS_D),
      (jump_to_menu, "mnu_arena_duel_fight"),
	  (finish_mission),

	])
]
