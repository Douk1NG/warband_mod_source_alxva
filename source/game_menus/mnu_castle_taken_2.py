# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

castle_taken_2_menu = [
(
    "castle_taken_2",mnf_disable_all_keys,
    "{s3} has fallen to your troops, and you now have full control of the castle.\
 It is time to send word to {s9} about your victory. {s5}",
    "none",
    [
        (str_store_party_name, s3, "$g_encountered_party"),
        (str_clear, s5),
        (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
        (str_store_troop_name, s9, ":faction_leader"),
        (try_begin),
          (eq, "$player_has_homage", 0),
          (assign, reg8, 0),
          (try_begin),
		    ##diplomacy start+ FIX: Inserted missing argument
            #(party_slot_eq, "$g_encountered_party", spt_town),
			(party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
			##diplomacy end+
            (assign, reg8, 1),
          (try_end),
          ##diplomacy start+ fix gender of pronoun
          (call_script, "script_dplmc_store_troop_is_female", ":faction_leader"),
          (str_store_string, s5, "@However, since you are not a sworn {man/follower} of {s9}, there is no chance {reg0?she:he} would recognize you as the {lord/lady} of this {reg8?town:castle}."),
          ##diplomacy end+
        (try_end),
    ],
    [
        ("castle_taken_claim",[(eq, "$player_has_homage", 1)],
		"Request that {s3} be awarded to you.",
        [
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, "trp_player"),
        (assign, "$g_castle_requested_by_player", "$current_town"),
		(assign, "$g_castle_requested_for_troop", "trp_player"),
        (assign, "$auto_enter_town", "$g_encountered_party"),
        (change_screen_return),
        ]),

		("castle_taken_claim_2",[
		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
		(is_between, ":spouse", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, ":spouse", slot_troop_occupation, slto_kingdom_hero),
		(store_faction_of_troop, ":spouse_faction", ":spouse"),
		(eq, ":spouse_faction", "$players_kingdom"),
		],
		"Request that {s3} be awarded to your {wife/husband}.",
        [
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, "trp_player"),
        (assign, "$g_castle_requested_by_player", "$current_town"),
		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
		(assign, "$g_castle_requested_for_troop", ":spouse"),
        (assign, "$auto_enter_town", "$g_encountered_party"),
        (change_screen_return),
        ]),



      ("castle_taken_no_claim",[],"Ask no rewards.",
       [
        (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, -1),
        (assign, "$auto_enter_town", "$g_encountered_party"),
        (change_screen_return),
#        (jump_to_menu, "mnu_town"),
        ]),
    ],
  )
]
