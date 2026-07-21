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

calculate_player_faction_wage_scripts = [
# script_give_center_to_lord
# Input: arg1 = party_no
# Output: reg0 = weekly wage
("calculate_player_faction_wage",
    [(assign, ":nongarrison_wages", 0),
     (assign, ":garrison_wages", 0),
     (try_for_parties, ":party_no"),
       (assign, ":garrison_troop", 0),
       (try_begin),
         (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_town),
         (party_slot_eq, ":party_no", slot_party_type, spt_castle),
         (party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
         (assign, ":garrison_troop", 1),
       (try_end),
       (this_or_next|eq, ":party_no", "p_main_party"),
       (eq, ":garrison_troop", 1),
       (party_get_num_companion_stacks, ":num_stacks",":party_no"),
       (try_for_range, ":i_stack", 0, ":num_stacks"),
         (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
         (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
         (call_script, "script_game_get_troop_wage", ":stack_troop", ":party_no"),
         (assign, ":cur_wage", reg0),
         (val_mul, ":cur_wage", ":stack_size"),
         (try_begin),
           (eq, ":garrison_troop", 1),
           (val_add, ":garrison_wages", ":cur_wage"),
         (else_try),
           (val_add, ":nongarrison_wages", ":cur_wage"),
         (try_end),
       (try_end),
     (try_end),
     (val_div, ":garrison_wages", 2),#Half payment for garrisons
     (store_sub, ":total_payment", 14, "$g_cur_week_half_daily_wage_payments"), #between 0 and 7
     (val_mul, ":nongarrison_wages", ":total_payment"),
     (val_div, ":nongarrison_wages", 14),
     ##diplomacy start+ centralization affects this in the player's kingdom
###xxx TODO: This appears to be missing.
     ##diplomacy end+
     (store_add, reg0, ":nongarrison_wages", ":garrison_wages"),
    ])
]
