# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

notification_player_faction_political_issue_resolved_for_player_menu = [
(
    "notification_player_faction_political_issue_resolved_for_player",0,
    "After consulting with the peers of the realm, {s10} has decided to confer {s11} on you. You may decline the honor, but it will probably mean that you will not receive other awards for a little while.{s12}",
    "none",
    [
    (faction_get_slot, ":leader", "$players_kingdom", slot_faction_leader),
    (str_store_troop_name, s10, ":leader"),
    (faction_get_slot, ":issue", "$players_kingdom", slot_faction_political_issue),
    (try_begin),
        (eq, ":issue", 1),
        (str_store_string, s11, "str_the_marshalship"),
        (str_store_string, s12, "@^^Note that so long as you remain marshal, the lords of the realm will be expecting you to lead them on campaign. So, if you are awaiting a feast, either for a wedding or for other purposes, you may wish to resign the marshalship by speaking to your liege."),
    (else_try),
        (str_clear, s12),
        (str_store_party_name, s11, ":issue"),
    (try_end),
    ],
    [
       ("accept",
       [],"Accept the honor",
       [
        (faction_get_slot, ":issue", "$players_kingdom", slot_faction_political_issue),

        (try_begin),
            (eq, ":issue", 1),
            (call_script, "script_check_and_finish_active_army_quests_for_faction", "$players_kingdom"),
            (call_script, "script_appoint_faction_marshall", "$players_kingdom", "trp_player"),
            (unlock_achievement, ACHIEVEMENT_AUTONOMOUS_COLLECTIVE),
        (else_try),
            (call_script, "script_give_center_to_lord", ":issue", "trp_player", 0), #Zero means don't add garrison
        (try_end),

        (faction_set_slot, "$players_kingdom", slot_faction_political_issue, 0),
        (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
            (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
            (eq, ":active_npc_faction", "$players_kingdom"),
            (troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
        (try_end),
        (change_screen_return),
        ]),

       ("decline",
       [],"Decline the honor",
       [
        (faction_get_slot, ":issue", "$players_kingdom", slot_faction_political_issue),
        (try_begin),
            (is_between, ":issue", centers_begin, centers_end),
            (assign, "$g_dont_give_fief_to_player_days", 30),
        (else_try),
            (assign, "$g_dont_give_marshalship_to_player_days", 30),
        (try_end),

        (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
            (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
            (eq, ":active_npc_faction", "$players_kingdom"),
            (troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
        (try_end),
        (change_screen_return),
        ]),
    ]
  )
]
