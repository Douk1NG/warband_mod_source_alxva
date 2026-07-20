# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

arena_duel_conclusion_menu = [
("arena_duel_conclusion",0,
   "{!}{s11}",
   "none",
   [

    (try_begin),
		(eq, "$g_leave_encounter", 1),
		(change_screen_return),
	(try_end),

    (str_store_troop_name, s10, "$g_duel_troop"),
    #SB : change to loop
    (store_add, ":end", lady_quests_end, 2),
    (try_for_range, ":quest", "qst_duel_for_lady", ":end"),
      (try_begin),
        (eq, ":quest", lady_quests_end),
        (assign, ":quest", "qst_denounce_lord"),
      (try_end),
      (quest_slot_eq, ":quest", slot_quest_target_troop, "$g_duel_troop"),
      (try_begin),
        (check_quest_succeeded, ":quest"),
        (str_store_string, s11, "str_s10_lies_in_the_arenas_dust_for_several_minutes_then_staggers_to_his_feet_you_have_won_the_duel"),
        #(set_background_mesh, "mesh_pic_victory"),
      (else_try),
        (check_quest_failed, ":quest"),
        (str_store_string, s11, "str_you_lie_stunned_for_several_minutes_then_stagger_to_your_feet_to_find_your_s10_standing_over_you_you_have_lost_the_duel"),
        #(set_background_mesh, "mesh_pic_defeat"),
      (try_end),
    (try_end),
   ],
   [
     ("continue",[],"Continue...",
      [
        (assign, "$talk_context", tc_after_duel),
        (try_begin), #SB : use the appropriate script calls
          (is_between, "$g_encountered_party", centers_begin, centers_end),
          (call_script, "script_start_court_conversation", "$g_duel_troop", "$g_encountered_party"), #SB : script call
        (else_try),
          (call_script, "script_setup_troop_meeting", "$g_duel_troop", -1), #SB : script call
        (try_end),
        ]),
      ]
  )
]
