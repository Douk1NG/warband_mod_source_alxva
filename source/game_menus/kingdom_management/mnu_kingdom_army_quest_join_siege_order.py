# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

kingdom_army_quest_join_siege_order_menu = [
(
    "kingdom_army_quest_join_siege_order",mnf_scale_picture,
    "{s8} sends word that you are to join the siege of {s9} in preparation for a full assault.\
 Your troops are to take {s9} at all costs.",
    "none",
    [
		(set_background_mesh, "mesh_pic_messenger"),
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (quest_get_slot, ":quest_target_center", "qst_join_siege_with_army", slot_quest_target_center),
        (str_store_troop_name, s8, ":faction_marshall"),
        (str_store_party_name, s9, ":quest_target_center"),
      ],
    [
      ("continue",[],"Continue...",
       [
           (call_script, "script_end_quest", "qst_follow_army"),
           (quest_get_slot, ":quest_target_center", "qst_join_siege_with_army", slot_quest_target_center),
           (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
           (str_store_troop_name_link, s13, ":faction_marshall"),
           (str_store_party_name_link, s14, ":quest_target_center"),
           (setup_quest_text, "qst_join_siege_with_army"),
           (str_store_string, s2, "@{s13} ordered you to join the assault against {s14}."),
           (call_script, "script_start_quest", "qst_join_siege_with_army", ":faction_marshall"),
           (change_screen_return),
        ]),
     ]
  )
]
