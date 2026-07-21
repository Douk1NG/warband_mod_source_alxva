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

play_victorious_sound_scripts = [
# script_combat_music_set_situation_with_culture
# Input: none
# Output: none
("play_victorious_sound",
   [
     (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
#      (play_cue_track, "track_victorious_neutral_1"),
#      (play_track, "track_victorious_neutral_1", 1),
     ])
]
