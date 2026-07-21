# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

notification_player_faction_political_issue_resolved_menu = [
(
    "notification_player_faction_political_issue_resolved",0,
    "After consulting with the peers of the realm, {s10} has decided to confer {s11} on {s12}.",
    "none",
    [
    (assign, ":faction_issue_resolved", "$g_notification_menu_var1"),
    (assign, ":faction_decision", "$g_notification_menu_var2"),
    (faction_get_slot, ":leader", "$players_kingdom", slot_faction_leader),
    (str_store_troop_name, s10, ":leader"),
    (try_begin),
        (eq, ":faction_issue_resolved", 1),
        (str_store_string, s11, "str_the_marshalship"),
    (else_try),
        (str_store_party_name, s11, ":faction_issue_resolved"),
    (try_end),
    (str_store_troop_name, s12, ":faction_decision"),

    ],
    [
       ("continue",
       [],"Continue...",
       [
        (change_screen_return),
        ]),


    ]
  )
]
