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

game_missile_dives_into_water_scripts = [
("game_missile_dives_into_water", [
	# (store_script_param, ":launcher_item_modifier", 4),
	# (store_script_param, ":shooter_agent_no", 5),
	# (store_script_param, ":missile_no", 6),

    (play_sound_at_position, "snd_jump_end_water", pos1),
    (particle_system_burst, "psys_game_water_splash_2", pos1, 40),

])
]
