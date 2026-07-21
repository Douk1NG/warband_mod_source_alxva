# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

castle_meeting_selected_menu = [
(
    "castle_meeting_selected",0,
    "Your request for a meeting is relayed inside, and finally {s6} appears in the courtyard to speak with you.",
    "none",
    [
    (try_begin),
		(eq, "$g_leave_encounter", 1),
		(change_screen_return),
	(try_end),

    (str_store_troop_name, s6, "$castle_meeting_selected_troop")],
    [
      ("continue",[],
       "Continue...",
       [(jump_to_menu, "mnu_castle_outside"),
        #do not set context here in case we need to use another one, set tc_castle_gate from parent menu
        (call_script, "script_start_courtyard_conversation", "$castle_meeting_selected_troop", "$current_town"),
        ]),
    ]
  )
]
