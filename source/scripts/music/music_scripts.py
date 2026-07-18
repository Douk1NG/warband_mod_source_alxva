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

####################################################################################################################
# MUSIC & SOUND SCRIPTS
# 
# This file contains scripts for managing the dynamic music system and sound effects. 
# It sets the appropriate combat or atmospheric music tracks based on the current situation, 
# culture, and battle outcome.
####################################################################################################################

music_scripts = [
  # Input: arg1 = music_situation
  # Output: none
  ("music_set_situation_with_culture",
    [
      (store_script_param, ":situation", 1),
      (assign, ":culture", 0), #no culture
      (try_begin),
        (this_or_next|eq, ":situation", mtf_sit_town),
        (this_or_next|eq, ":situation", mtf_sit_day),
        (this_or_next|eq, ":situation", mtf_sit_night),
        (this_or_next|eq, ":situation", mtf_sit_town_infiltrate),
        (eq, ":situation", mtf_sit_encounter_hostile),
        (call_script, "script_get_culture_with_party_faction_for_music", "$g_encountered_party"),
        (val_or, ":culture", reg0),
      (else_try),
        (this_or_next|eq, ":situation", mtf_sit_ambushed),
        (eq, ":situation", mtf_sit_fight),
        (call_script, "script_get_culture_with_party_faction_for_music", "$g_encountered_party"),
        (val_or, ":culture", reg0),
        (call_script, "script_get_culture_with_party_faction_for_music", "p_main_party"),
        (val_or, ":culture", reg0),
        (call_script, "script_get_closest_center", "p_main_party"),
        (call_script, "script_get_culture_with_party_faction_for_music", reg0),
        (val_or, ":culture", reg0),
      (else_try),
        (eq, ":situation", mtf_sit_multiplayer_fight),
        (call_script, "script_get_culture_with_faction_for_music", "$g_multiplayer_team_1_faction"),
        (val_or, ":culture", reg0),
        (call_script, "script_get_culture_with_faction_for_music", "$g_multiplayer_team_2_faction"),
        (val_or, ":culture", reg0),
      (else_try),
        (eq, ":situation", mtf_sit_travel),
        (call_script, "script_get_culture_with_party_faction_for_music", "p_main_party"),
        (val_or, ":culture", reg0),
        (call_script, "script_get_closest_center", "p_main_party"),
        (call_script, "script_get_culture_with_party_faction_for_music", reg0),
        (val_or, ":culture", reg0),
      (else_try),
        (eq, ":situation", mtf_sit_victorious),
        (call_script, "script_get_culture_with_party_faction_for_music", "p_main_party"),
        (val_or, ":culture", reg0),
      (else_try),
        (eq, ":situation", mtf_sit_killed),
        (call_script, "script_get_culture_with_party_faction_for_music", "$g_encountered_party"),
        (val_or, ":culture", reg0),
      (try_end),
      (try_begin),
        (this_or_next|eq, ":situation", mtf_sit_town),
        (eq, ":situation", mtf_sit_day),
        (try_begin),
          (is_currently_night),
          (assign, ":situation", mtf_sit_night),
        (try_end),
      (try_end),
      (music_set_situation, ":situation"),
      (music_set_culture, ":culture"),
     ]),


  # script_combat_music_set_situation_with_culture
  # Input: none
  # Output: none
  ("play_victorious_sound",
   [
     (call_script, "script_music_set_situation_with_culture", mtf_sit_victorious),
#      (play_cue_track, "track_victorious_neutral_1"),
#      (play_track, "track_victorious_neutral_1", 1),
     ]),

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
     ]),
]
