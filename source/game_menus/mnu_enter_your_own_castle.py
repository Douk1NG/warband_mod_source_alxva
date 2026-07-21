# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

enter_your_own_castle_menu = [
(
    "enter_your_own_castle",0,
    "{s10}",
    "none",
    [
      (try_begin),
	  ##diplomacy start+ Add support for the player as co-ruler of an NPC faction
	    (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
		(neg|is_between, "$supported_pretender", pretenders_begin, pretenders_end), #SB : exception for honorific
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(try_begin),
			(eq, "$character_gender", tf_female),
			(call_script, "script_dplmc_print_cultural_word_to_sreg", "trp_player", DPLMC_CULTURAL_TERM_KING_FEMALE, s10),
		(else_try),
			(call_script, "script_dplmc_print_cultural_word_to_sreg", "trp_player", DPLMC_CULTURAL_TERM_KING, s10),
		(try_end),
		(str_store_string, s10, "@As you approach, you are spotted by the castle guards, who welcome you and open the gates for their {s10}."),
	  (else_try),
	  ##diplomacy end+
        (neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
        (faction_get_slot, ":faction_leader", "fac_player_supporters_faction", slot_faction_leader),
        (eq, ":faction_leader", "trp_player"),
        (str_store_string, s10, "@As you approach, you are spotted by the castle guards, who welcome you and open the gates for their {king/queen}."),
      (else_try),
        (str_store_string, s10, "@As you approach, you are spotted by the castle guards, who welcome you and open the gates for their {lord/lady}."),
      (try_end),

      (str_store_party_name, s2, "$current_town"),
    ],
    [
      ("continue",[],"Continue...",
       [ (jump_to_menu,"mnu_town"),
        ]),
    ],
  )
]
