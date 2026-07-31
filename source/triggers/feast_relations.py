# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *



  # 1175 feature: improve relations with attending lords while the player hosts a feast.
  

feast_relations_triggers = [
(1, 0, 0,
   [
      (faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_feast),
      (faction_slot_eq, "$players_kingdom", slot_faction_ai_object, "$g_encountered_party"),
      (check_quest_active, "qst_organize_feast"),
      (quest_slot_eq, "qst_organize_feast", slot_quest_target_center, "$g_encountered_party"),
      (neg|map_free),
    ],
   [
      (call_script, "script_internal_politics_rate_feast_to_s9", "trp_household_possessions", 120, "$players_kingdom", 0),
      (assign, ":quality_of_feast", reg0),
      (try_begin),
        (ge, ":quality_of_feast", 20),

        (store_current_hours, "$g_current_hours"),
        (quest_get_slot, ":feast_center", "qst_organize_feast", slot_quest_target_center),
        (party_clear, "p_temp_party"),
        (call_script, "script_get_heroes_attached_to_center_aux", ":feast_center", "p_temp_party"),
        (party_get_num_companion_stacks, ":num_stacks", "p_temp_party"),
        (try_for_range, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":i_stack"),
          (troop_get_slot, "$g_talk_troop_last_talk_time", ":stack_troop", slot_troop_last_talk_time),
          (store_sub, "$g_time_since_last_talk", "$g_current_hours", "$g_talk_troop_last_talk_time"),
          (ge, "$g_time_since_last_talk", 24),
          (troop_set_slot, ":stack_troop", slot_troop_last_talk_time, "$g_current_hours"),
          (call_script, "script_troop_change_relation_with_troop", ":stack_troop", "trp_player", 1),
        (try_end),
      (try_end),
    ]),
]
