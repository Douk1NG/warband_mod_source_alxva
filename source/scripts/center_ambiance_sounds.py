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

center_ambiance_sounds_scripts = [
# script_center_ambiance_sounds
# Input: none
# Output: none
# to be called every two seconds
("center_ambiance_sounds",
    [
        (assign, ":sound_1", -1),
        (assign, ":sound_2", -1),
        (assign, ":sound_3", -1),
        (assign, ":sound_4", -1),
        (assign, ":sound_5", -1),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
          (try_begin),
            (neg|is_currently_night),
            (assign, ":sound_3", "snd_distant_dog_bark"),
            (assign, ":sound_3", "snd_distant_chicken"),
          (else_try),
            (assign, ":sound_1", "snd_distant_dog_bark"),
            (assign, ":sound_2", "snd_distant_owl"),
          (try_end),
        (else_try),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (try_begin),
            (neg|is_currently_night),
            (assign, ":sound_1", "snd_distant_carpenter"),
            (assign, ":sound_2", "snd_distant_blacksmith"),
            (assign, ":sound_3", "snd_distant_dog_bark"),
          (else_try),
            (assign, ":sound_1", "snd_distant_dog_bark"),
          (try_end),
        (try_end),
        (try_begin),
          (store_random_in_range, ":r", 0, 7),
          (try_begin),
            (eq, ":r", 1),
            (ge, ":sound_1", 0),
            (play_sound, ":sound_1"),
          (else_try),
            (eq, ":r", 2),
            (ge, ":sound_2", 0),
            (play_sound, ":sound_2"),
          (else_try),
            (eq, ":r", 3),
            (ge, ":sound_3", 0),
            (play_sound, ":sound_3"),
          (else_try),
            (eq, ":r", 4),
            (ge, ":sound_4", 0),
            (play_sound, ":sound_4"),
          (else_try),
            (eq, ":r", 5),
            (ge, ":sound_5", 0),
            (play_sound, ":sound_5"),
          (try_end),
        (try_end),
  ])
]
