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

check_and_finish_active_army_quests_for_faction_scripts = [
# script_decide_faction_ai
# Input: faction_no
# Output: none
("check_and_finish_active_army_quests_for_faction",
   [
     (store_script_param_1, ":faction_no"),
     (try_begin),
       (eq, "$players_kingdom", ":faction_no"),
       (try_begin),
         (check_quest_active, "qst_report_to_army"),
         (call_script, "script_cancel_quest", "qst_report_to_army"),
       (try_end),
       (assign, ":one_active", 0),
       (try_for_range, ":quest_no", army_quests_begin, army_quests_end),
         (check_quest_active, ":quest_no"),
         (call_script, "script_cancel_quest", ":quest_no"),
		 (troop_get_slot, ":army_quest_giver_troop", ":quest_no", slot_quest_giver_troop),
         (assign, ":one_active", 1),
       (try_end),
       (try_begin),
         (check_quest_active, "qst_follow_army"),
         (assign, ":one_active", 1),
		 (troop_get_slot, ":army_quest_giver_troop", "qst_follow_army", slot_quest_giver_troop),
         (call_script, "script_end_quest", "qst_follow_army"),
       (try_end),
       (eq, ":one_active", 1),
       (faction_get_slot, ":last_offensive_time", ":faction_no", slot_faction_last_offensive_concluded),
       (store_current_hours, ":cur_hours"),
       (store_sub, ":total_time_served", ":cur_hours", ":last_offensive_time"),
       (store_mul, ":xp_reward", ":total_time_served", 5),
       (val_div, ":xp_reward", 50),
       (val_mul, ":xp_reward", 50),
       (val_add, ":xp_reward", 50),
       (add_xp_as_reward, ":xp_reward"),
	   (call_script, "script_troop_change_relation_with_troop", "trp_player", ":army_quest_giver_troop", 2),
     (try_end),
    ])
]
