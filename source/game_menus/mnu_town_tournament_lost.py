# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

town_tournament_lost_menu = [
(
    "town_tournament_lost",0,
    "You have been eliminated from the tournament.{s8}",
    "none",
    [
	(str_clear, s8),
	(try_begin),
		(this_or_next|neq, "$players_kingdom", "$g_encountered_party_faction"),
			(neg|troop_slot_ge, "trp_player", slot_troop_renown, 50),
		(neg|troop_slot_ge, "trp_player", slot_troop_renown, 125),
		(gt, "$g_player_tournament_placement", 4),
		(faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_state, sfai_feast),
		(faction_slot_eq, "$g_encountered_party_faction", slot_faction_ai_object, "$g_encountered_party"),
		(str_store_string, s8, "str__however_you_have_sufficiently_distinguished_yourself_to_be_invited_to_attend_the_ongoing_feast_in_the_lords_castle"),
	(try_end),

        ],
    [
      ("continue", [], "Continue...",
       [(jump_to_menu, "mnu_town_tournament_won_by_another"),
        ]),
    ]
  )
]
