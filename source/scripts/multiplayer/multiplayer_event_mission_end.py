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

multiplayer_event_mission_end_scripts = [
#script_multiplayer_event_mission_end
# Input: none
# Output: none
("multiplayer_event_mission_end",
   [
     #EVERY_BREATH_YOU_TAKE achievement
     (try_begin),
       (multiplayer_get_my_player, ":my_player_no"),
       (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
       (player_get_kill_count, ":kill_count", ":my_player_no"),
       (player_get_death_count, ":death_count", ":my_player_no"),
       (gt, ":kill_count", ":death_count"),
       (unlock_achievement, ACHIEVEMENT_EVERY_BREATH_YOU_TAKE),
     (try_end),
     #EVERY_BREATH_YOU_TAKE achievement end
     ])
]
