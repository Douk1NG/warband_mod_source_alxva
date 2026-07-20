# ======================================================================
# SHARED DEPENDENCY
# Entity: start_quest (script)
# Called by menus in 3 domains: kingdom_management, notifications, siege
# ======================================================================

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

start_quest_scripts = [
##  # script_event_center_captured
# INPUT: arg1 = quest_no, arg2 = giver_troop_no, s2 = description_text
# OUTPUT: none
("start_quest",
    [(store_script_param, ":quest_no", 1),
     (store_script_param, ":giver_troop_no", 2),

     (quest_set_slot, ":quest_no", slot_quest_giver_troop, ":giver_troop_no"),

     (try_begin),
       (eq, ":giver_troop_no", -1),
       (str_store_string, s63, "str_political_suggestion"),
     (else_try), #SB : extend range
       (is_between, ":giver_troop_no", active_npcs_begin, heroes_end),
       (str_store_troop_name_link, s62, ":giver_troop_no"),
       (str_store_string, s63, "@Given by: {s62}"),
     (else_try),
       (str_store_troop_name, s62, ":giver_troop_no"),
       (str_store_string, s63, "@Given by: {s62}"),
     (try_end),
     (store_current_hours, ":cur_hours"),
     (str_store_date, s60, ":cur_hours"),
     (str_store_string, s60, "@Given on: {s60}"),
     (add_quest_note_from_sreg, ":quest_no", 0, s60, 0),
     (add_quest_note_from_sreg, ":quest_no", 1, s63, 0),
     (add_quest_note_from_sreg, ":quest_no", 2, s2, 0),

     (try_begin),
       (quest_slot_ge, ":quest_no", slot_quest_expiration_days, 1),
       (quest_get_slot, reg0, ":quest_no", slot_quest_expiration_days),
       (add_quest_note_from_sreg, ":quest_no", 7, "@You have {reg0} days to finish this quest.", 0),
     (try_end),

     #Adding dont_give_again_for_days value
     (try_begin),
       (quest_slot_ge, ":quest_no", slot_quest_dont_give_again_period, 1),
       (quest_get_slot, ":dont_give_again_period", ":quest_no", slot_quest_dont_give_again_period),
       (quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days, ":dont_give_again_period"),
     (try_end),
     (start_quest, ":quest_no", ":giver_troop_no"),

     (try_begin),
       (eq, ":quest_no", "qst_report_to_army"),
       (assign, "$number_of_report_to_army_quest_notes", 8),
       (faction_get_slot, ":faction_ai_state", "$players_kingdom", slot_faction_ai_state),
       (call_script, "script_update_report_to_army_quest_note", "$players_kingdom", ":faction_ai_state", -1),
     (try_end),

     (display_message, "str_quest_log_updated"),
   ])
]
