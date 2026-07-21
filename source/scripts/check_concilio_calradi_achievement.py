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

check_concilio_calradi_achievement_scripts = [
("check_concilio_calradi_achievement",
  [
   (try_begin),
     (eq, "$players_kingdom", "fac_player_supporters_faction"),
     (faction_get_slot, ":player_faction_king", "fac_player_supporters_faction", slot_faction_leader),
     (eq, ":player_faction_king", "trp_player"),
     (assign, ":number_of_vassals", 0),
     (try_for_range, ":cur_troop", active_npcs_begin, active_npcs_end),
       (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
       (store_faction_of_troop, ":cur_faction", ":cur_troop"),
       (eq, ":cur_faction", "fac_player_supporters_faction"),
       (val_add, ":number_of_vassals", 1),
     (try_end),
     (ge, ":number_of_vassals", 3),
     (unlock_achievement, ACHIEVEMENT_CONCILIO_CALRADI),
   (try_end),
  ])
]
