# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

notification_player_kingdom_holds_feast_menu = [
(
    "notification_player_kingdom_holds_feast",mnf_scale_picture,
    "{s11}",
    "none",
    [
		(set_background_mesh, "mesh_pic_messenger"),

		(str_store_troop_name, s8, "$g_notification_menu_var1"),
		(store_faction_of_troop, ":host_faction", "$g_notification_menu_var1"),
		(str_store_faction_name, s9, ":host_faction"),

#		(str_store_faction_name, s9, "$players_kingdom"),
		(str_store_party_name, s10, "$g_notification_menu_var2"),

		(str_clear, s12),
		(try_begin),
			(check_quest_active, "qst_wed_betrothed"),
			(quest_get_slot, ":giver_troop", "qst_wed_betrothed", slot_quest_giver_troop),
			(store_faction_of_troop, ":giver_troop_faction", ":giver_troop"),
			(eq, ":giver_troop_faction", "$players_kingdom"),
			(str_store_string, s12, "str_feast_wedding_opportunity"),
		(try_end),



		(str_store_string, s11, "str_s8_wishes_to_inform_you_that_the_lords_of_s9_will_be_gathering_for_a_feast_at_his_great_hall_in_s10_and_invites_you_to_be_part_of_this_august_assembly"),
		(try_begin),
			(eq, "$g_notification_menu_var1", 0),
			(str_store_string, s11, "str_the_great_lords_of_your_kingdom_plan_to_gather_at_your_hall_in_s10_for_a_feast"),
		(try_end),
		(str_store_string, s11, "@{!}{s11}{s12}"),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(store_current_hours, ":hours_since_last_feast"),
			(faction_get_slot, ":last_feast_start_time", "$players_kingdom", slot_faction_last_feast_start_time),
			(val_sub, ":hours_since_last_feast", ":last_feast_start_time"),
			(assign, reg4, ":hours_since_last_feast"),
			(display_message, "@{!}DEBUG -- Hours since last feast started: {reg4}"),
		(try_end),

      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  )
]
