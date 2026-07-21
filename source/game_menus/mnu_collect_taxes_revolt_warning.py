# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

collect_taxes_revolt_warning_menu = [
(
    "collect_taxes_revolt_warning",0,
    "The people of {s3} are outraged at your demands and decry it as nothing more than extortion.\
 They're getting very restless, and they may react badly if you keep pressing them.",
    "none",
    [(str_store_party_name, s3, "$current_town"),
     ],
    [
      ("continue_collecting_taxes", [], "Ignore them and continue.",
       [ #SB : objectionable action
       (call_script, "script_objectionable_action", tmt_egalitarian, "str_repress_farmers"),
       (change_screen_return),]),
      ("halve_taxes", [(quest_get_slot, ":quest_giver_troop", "qst_collect_taxes", slot_quest_giver_troop),
                       (str_store_troop_name, s1, ":quest_giver_troop"),],
       "Agree to reduce your collection by half. ({s1} may be upset)",
       [(assign, "$qst_collect_taxes_halve_taxes", 1),
        (change_screen_return),
        ]),
    ]
  )
]
