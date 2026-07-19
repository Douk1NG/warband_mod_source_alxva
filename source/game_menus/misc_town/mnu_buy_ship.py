# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

buy_ship_menu = [
(
    "buy_ship",0,
    "{s22}",
    "none",
    [  # I'd like to make this a full scene, or at least a dialogue with more to it than a simple menu.
	(try_begin), # For now I settle with not breaking the disguise feature.
		(gt, "$sneaked_into_town", disguise_none),
		(str_store_string, s22, "@After further consideration, a large purchace such as commisioning an entire ship will certianly attract too much attention..."),
	(else_try),
		(str_store_string, s22, "@Which ship do you want to buy?"),
	(try_end),
	],
    [
      ("ship_a",[(le, "$sneaked_into_town", disguise_none),],"Longship (5000 denars)",[
        (try_begin),
          (store_troop_gold, ":gold", "trp_player"),
          (ge, ":gold", 5000),
          (assign, "$g_player_icon_state", pis_ship),
          (party_set_flags, "p_main_party", pf_is_ship, 1),
          #
          (party_get_slot, ":port", "$current_town", slot_town_port),
          (party_get_position, pos2, ":port"),
          (party_set_position, "p_main_party", pos2),
          # (party_get_position, pos1, "p_main_party"),
          # (map_get_water_position_around_position, pos2, pos1, 8),
          # (party_set_position, "p_main_party", pos2),
          (assign, "$g_main_ship_party", -1),
          (party_set_slot, "p_main_party", slot_party_ship_type, 1),
          (troop_remove_gold, "trp_player", 5000),
          (change_screen_return),
        (else_try),
          (display_message, "@Not enough money to buy that."),
        (try_end),
      ]),
      ("ship_b",[(le, "$sneaked_into_town", disguise_none),],"Galley (7,000 denars)",[
        (try_begin),
          (store_troop_gold, ":gold", "trp_player"),
          (ge, ":gold", 7000),
          (assign, "$g_player_icon_state", pis_ship),
          (party_set_flags, "p_main_party", pf_is_ship, 1),
          #
          (party_get_slot, ":port", "$current_town", slot_town_port),
          (party_get_position, pos2, ":port"),
          (party_set_position, "p_main_party", pos2),
          # (party_get_position, pos1, "p_main_party"),
          # (map_get_water_position_around_position, pos2, pos1, 8),
          # (party_set_position, "p_main_party", pos2),
          (assign, "$g_main_ship_party", -1),
          (party_set_slot, "p_main_party", slot_party_ship_type, 2),
          (troop_remove_gold, "trp_player", 7000),
          (change_screen_return),
        (else_try),
          (display_message, "@Not enough money to buy that."),
        (try_end),
      ]),
      ("ship_c",[(le, "$sneaked_into_town", disguise_none),],"Cog (10,000 denars)",[
        (try_begin),
          (store_troop_gold, ":gold", "trp_player"),
          (ge, ":gold", 10000),
          (assign, "$g_player_icon_state", pis_ship),
          (party_set_flags, "p_main_party", pf_is_ship, 1),
          #
          (party_get_slot, ":port", "$current_town", slot_town_port),
          (party_get_position, pos2, ":port"),
          (party_set_position, "p_main_party", pos2),
          # (party_get_position, pos1, "p_main_party"),
          # (map_get_water_position_around_position, pos2, pos1, 8),
          # (party_set_position, "p_main_party", pos2),
          (assign, "$g_main_ship_party", -1),
          (party_set_slot, "p_main_party", slot_party_ship_type, 3),
          (troop_remove_gold, "trp_player", 10000),
          (change_screen_return),
        (else_try),
          (display_message, "@Not enough money to buy that."),
        (try_end),
      ]),
      ("ship_d",[(le, "$sneaked_into_town", disguise_none),],"Dhow (8,000 denars)",[
        (try_begin),
          (store_troop_gold, ":gold", "trp_player"),
          (ge, ":gold", 8000),
          (assign, "$g_player_icon_state", pis_ship),
          (party_set_flags, "p_main_party", pf_is_ship, 1),
          #
          (party_get_slot, ":port", "$current_town", slot_town_port),
          (party_get_position, pos2, ":port"),
          (party_set_position, "p_main_party", pos2),
          # (party_get_position, pos1, "p_main_party"),
          # (map_get_water_position_around_position, pos2, pos1, 8),
          # (party_set_position, "p_main_party", pos2),
          (assign, "$g_main_ship_party", -1),
          (party_set_slot, "p_main_party", slot_party_ship_type, 4),
          (troop_remove_gold, "trp_player", 8000),
          (change_screen_return),
        (else_try),
          (display_message, "@Not enough money to buy that."),
        (try_end),
      ]),
      ("leave",[],"Leave the shipyard.",[(jump_to_menu, "mnu_town")]),
    ]
  )
]
