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

npc_morale_scripts = [
("npc_morale",
[
        (store_script_param_1, ":npc"),

        (troop_get_slot, ":morality_grievances", ":npc", slot_troop_morality_penalties),
        (troop_get_slot, ":personality_grievances", ":npc", slot_troop_personalityclash_penalties),
        (party_get_morale, ":party_morale", "p_main_party"),

        (store_sub, ":troop_morale", ":party_morale", ":morality_grievances"),
        (val_sub, ":troop_morale", ":personality_grievances"),
        (val_add, ":troop_morale", 50), #SB : this should scale from actual relation

        (assign, reg8, ":troop_morale"),

        (val_mul, ":troop_morale", 3),
        (val_div, ":troop_morale", 4),
        (val_clamp, ":troop_morale", 0, 100),

        (assign, reg5, ":party_morale"),
        (assign, reg6, ":morality_grievances"),
        (assign, reg7, ":personality_grievances"),
        (assign, reg9, ":troop_morale"),

#        (str_store_troop_name, s11, ":npc"),
#        (display_message, "@{!}{s11}'s morale = PM{reg5} + 50 - MG{reg6} - PG{reg7} = {reg8} x 0.75 = {reg9}"),

        (try_begin),
            (lt, ":morality_grievances", 3),
            (str_store_string, 7, "str_happy"),
        (else_try),
            (lt, ":morality_grievances", 15),
            (str_store_string, 7, "str_content"),
        (else_try),
            (lt, ":morality_grievances", 30),
            (str_store_string, 7, "str_concerned"),
        (else_try),
            (lt, ":morality_grievances", 45),
            (str_store_string, 7, "str_not_happy"),
        (else_try),
            (str_store_string, 7, "str_miserable"),
        (try_end),


        (try_begin),
            (lt, ":personality_grievances", 3),
            (str_store_string, 6, "str_happy"),
        (else_try),
            (lt, ":personality_grievances", 15),
            (str_store_string, 6, "str_content"),
        (else_try),
            (lt, ":personality_grievances", 30),
            (str_store_string, 6, "str_concerned"),
        (else_try),
            (lt, ":personality_grievances", 45),
            (str_store_string, 6, "str_not_happy"),
        (else_try),
            (str_store_string, 6, "str_miserable"),
        (try_end),


        (try_begin),
            (gt, ":troop_morale", 80),
            (str_store_string, 8, "str_happy"),
            (str_store_string, 63, "str_bar_enthusiastic"),
        (else_try),
            (gt, ":troop_morale", 60),
            (str_store_string, 8, "str_content"),
            (str_store_string, 63, "str_bar_content"),
        (else_try),
            (gt, ":troop_morale", 40),
            (str_store_string, 8, "str_concerned"),
            (str_store_string, 63, "str_bar_weary"),
        (else_try),
            (gt, ":troop_morale", 20),
            (str_store_string, 8, "str_not_happy"),
            (str_store_string, 63, "str_bar_disgruntled"),
        (else_try),
            (str_store_string, 8, "str_miserable"),
            (str_store_string, 63, "str_bar_miserable"),
        (try_end),


        (str_store_string, 21, "str_npc_morale_report"),
        (assign, reg0, ":troop_morale"),

     ])
]
