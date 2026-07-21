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

combat_music_set_situation_with_culture_scripts = [
# script_set_items_for_tournament
("combat_music_set_situation_with_culture",
    [
      (assign, ":situation", mtf_sit_fight),
      (assign, ":num_allies", 0),
      (assign, ":num_enemies", 0),
      (try_for_agents, ":agent_no"),
        (agent_is_alive, ":agent_no"),
        (agent_is_human, ":agent_no"),
        (agent_get_troop_id, ":agent_troop_id", ":agent_no"),
        (store_character_level, ":troop_level", ":agent_troop_id"),
        (val_add,  ":troop_level", 10),
        (val_mul, ":troop_level", ":troop_level"),
        (try_begin),
          (agent_is_ally, ":agent_no"),
          (val_add, ":num_allies", ":troop_level"),
        (else_try),
          (val_add, ":num_enemies", ":troop_level"),
        (try_end),
      (try_end),
      (val_mul, ":num_allies", 4), #play ambushed music if we are 2 times outnumbered.
      (val_div, ":num_allies", 3),
      (try_begin),
        (lt, ":num_allies", ":num_enemies"),
        (assign, ":situation", mtf_sit_ambushed),
      (try_end),
      (call_script, "script_music_set_situation_with_culture", ":situation"),
     ])
]
