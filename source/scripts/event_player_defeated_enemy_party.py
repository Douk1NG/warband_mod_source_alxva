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

event_player_defeated_enemy_party_scripts = [
("event_player_defeated_enemy_party",
    [(try_begin),
       (check_quest_active, "qst_raid_caravan_to_start_war"),
       (neg|check_quest_concluded, "qst_raid_caravan_to_start_war"),
       (party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_caravan),
       (store_faction_of_party, ":enemy_faction", "$g_enemy_party"),
       (quest_slot_eq, "qst_raid_caravan_to_start_war", slot_quest_target_faction, ":enemy_faction"),
       (quest_get_slot, ":cur_state", "qst_raid_caravan_to_start_war", slot_quest_current_state),
       (quest_get_slot, ":quest_target_amount", "qst_raid_caravan_to_start_war", slot_quest_target_amount),
       (val_add, ":cur_state", 1),
       (quest_set_slot, "qst_raid_caravan_to_start_war", slot_quest_current_state, ":cur_state"),
       (try_begin),
         (ge, ":cur_state", ":quest_target_amount"),
         (quest_get_slot, ":quest_target_faction", "qst_raid_caravan_to_start_war", slot_quest_target_faction),
         (quest_get_slot, ":quest_giver_troop", "qst_raid_caravan_to_start_war", slot_quest_giver_troop),
         (store_troop_faction, ":quest_giver_faction", ":quest_giver_troop"),
         (call_script, "script_diplomacy_start_war_between_kingdoms", ":quest_target_faction", ":quest_giver_faction", 1),
         (call_script, "script_succeed_quest", "qst_raid_caravan_to_start_war"),
       (try_end),
     (try_end),

     ])
]
