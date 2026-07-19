# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

courtship_relations_menu = [
("courtship_relations",0,
   "{s1}",
   "none",
   [(str_store_string, s1, "str_courtships_in_progress_"),
    (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_slot_eq, ":lady", slot_troop_met, 2),
		(call_script, "script_troop_get_relation_with_troop", "trp_player", ":lady"),
		(gt, reg0, 0),
		(assign, reg3, reg0),

		(str_store_troop_name, s2, ":lady"),

		(store_current_hours, ":hours_since_last_visit"),
		(troop_get_slot, ":last_visit_hour", ":lady", slot_troop_last_talk_time),
		(val_sub, ":hours_since_last_visit", ":last_visit_hour"),
		(store_div, ":days_since_last_visit", ":hours_since_last_visit", 24),
		(assign, reg4, ":days_since_last_visit"),

		(str_store_string, s1, "str_s1_s2_relation_reg3_last_visit_reg4_days_ago"),
	(try_end),

	(str_store_string, s1, "str_s1__poems_known"),
	(try_begin),
		 (gt, "$allegoric_poem_recitations", 0),
		 (str_store_string, s1, "str_s1_storming_the_castle_of_love_allegoric"),
	(try_end),
	(try_begin),
		 (gt, "$tragic_poem_recitations", 0),
		 (str_store_string, s1, "str_s1_kais_and_layali_tragic"),
	(try_end),
	(try_begin),
		 (gt, "$comic_poem_recitations", 0),
		 (str_store_string, s1, "str_s1_a_conversation_in_the_garden_comic"),
	(try_end),
	(try_begin),
		 (gt, "$heroic_poem_recitations", 0),
		 (str_store_string, s1, "str_s1_helgered_and_kara_epic"),
	(try_end),
	(try_begin),
		 (gt, "$mystic_poem_recitations", 0),
		 (str_store_string, s1, "str_s1_a_hearts_desire_mystic"),
	(try_end),

    ],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  )
]
