# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

lady_visit_menu = [
(
    "lady_visit",0,
    "Whom do you wish to visit?",
    "none",
    [],
    [

	("visit_lady_1", [
	(gt, "$love_interest_in_town", 0),
	(str_store_troop_name, s12, "$love_interest_in_town"),
	],
	  "Visit {s12}",
       [
	    (assign, "$love_interest_in_town", "$love_interest_in_town"),
        (jump_to_menu, "mnu_garden"),
        ]),



	("visit_lady_2", [
	(gt, "$love_interest_in_town_2", 0),
	(str_store_troop_name, s12, "$love_interest_in_town_2"),
	],
	  "Visit {s12}",
       [
	    (assign, "$love_interest_in_town", "$love_interest_in_town_2"),
        (jump_to_menu, "mnu_garden"),
        ]),

	("visit_lady_3", [
	(gt, "$love_interest_in_town_3", 0),
	(str_store_troop_name, s12, "$love_interest_in_town_3"),
	],
	  "Visit {s12}",
       [
	    (assign, "$love_interest_in_town", "$love_interest_in_town_3"),
        (jump_to_menu, "mnu_garden")], "Door to the garden."),


	("visit_lady_4", [(gt, "$love_interest_in_town_4", 0),(str_store_troop_name, s12, "$love_interest_in_town_4"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_4"),(jump_to_menu, "mnu_garden"),]),

	("visit_lady_5", [(gt, "$love_interest_in_town_5", 0),(str_store_troop_name, s12, "$love_interest_in_town_5"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_5"),(jump_to_menu, "mnu_garden"),]),

	("visit_lady_6",[(gt, "$love_interest_in_town_6", 0),(str_store_troop_name, s12, "$love_interest_in_town_6"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_6"),(jump_to_menu, "mnu_garden"),]),

	("visit_lady_7",[(gt, "$love_interest_in_town_7", 0),(str_store_troop_name, s12, "$love_interest_in_town_7"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_7"),(jump_to_menu, "mnu_garden"),]),

	("visit_lady_8",[(gt, "$love_interest_in_town_8", 0),(str_store_troop_name, s12, "$love_interest_in_town_8"),],
	"Visit {s12}",[(assign, "$love_interest_in_town", "$love_interest_in_town_8"),(jump_to_menu, "mnu_garden"),]),


	("leave",[], "Leave",[(jump_to_menu, "mnu_town")]),

    ]
	)
]
