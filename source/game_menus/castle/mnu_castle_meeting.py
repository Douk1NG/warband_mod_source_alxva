# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

castle_meeting_menu = [
(
    "castle_meeting",mnf_scale_picture,
    "With whom do you want to meet?",
    "none",
    [   (party_clear, "p_temp_party"),
        (call_script, "script_set_town_picture"),
        (call_script, "script_get_heroes_attached_to_center_aux", "$g_encountered_party", "p_temp_party"),#recursive call
        (party_get_num_companion_stacks, "$num_castle_meeting_troops", "p_temp_party"),
        (assign, "$talk_context", tc_castle_gate), #SB : move this up here
    ],
    [ ("guard_meet_"+str(x),[
        (gt, "$num_castle_meeting_troops", x),#test this out
        (party_stack_get_troop_id, ":troop_no", "p_temp_party", x),
        (is_between, ":troop_no", active_npcs_begin, active_npcs_end),
        (str_store_troop_name, s5, ":troop_no")],
       "{s5}.",[(party_stack_get_troop_id, "$castle_meeting_selected_troop", "p_temp_party", x),
       # (party_stack_get_troop_dna, "$temp_2", "p_temp_party", x),
       (jump_to_menu,"mnu_castle_meeting_selected")])
       for x in range(0, 8)
      ]

    +[("forget_it",[], "Forget it.", [(jump_to_menu,"mnu_castle_guard")]),]
  )
]
