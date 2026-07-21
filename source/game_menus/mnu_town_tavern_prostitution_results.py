# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

town_tavern_prostitution_results_menu = [
(
    "town_tavern_prostitution_results",0,
    "{s10}",
    "none",
    [
		(set_background_mesh, "mesh_pic_custom_01"),
		(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
		(assign, ":fems", 0),
		(try_for_range, ":i_stack", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":troop_id", "p_main_party", ":i_stack"),
			(troop_is_hero, ":troop_id"),
			(call_script, "script_cf_dplmc_troop_is_female", ":troop_id"),
			(val_add, ":fems", 1),
			(str_store_troop_name,s5,":troop_id"),
		(try_end),

		(try_begin),
		(gt, ":fems", 2),
		(str_store_string, s10, "@After a hard night's work, everyone returns to your room and pools the earnings..."),
		(else_try),
		(eq, ":fems", 2),
		(str_store_string, s10, "@After a hard night's work, {s5} meets you in your room to pool the earnings..."),
		(else_try),
		(str_store_string, s10, "@After a hard night's work, you retire to your room to go over the earnings..."),
		(try_end),
    ],
	[
		(
			"continue_to_room",
			[],
			"Collect payment and clean yourself up.",
			[
			(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
			(assign, ":cash", 0),
			(try_for_range, ":i_stack", 0, ":num_stacks"),
				(party_stack_get_troop_id, ":troop_id", "p_main_party", ":i_stack"),
				(troop_is_hero, ":troop_id"),
				(call_script, "script_cf_dplmc_troop_is_female", ":troop_id"),

				(try_begin),
					(neq, "$f_temp_var", ":troop_id"),
					(troop_get_slot, ":encounters", ":troop_id", slot_troop_encounters),
					(val_add, ":encounters", 1),
					(troop_set_slot, ":troop_id", slot_troop_encounters, ":encounters"),
				(try_end),

				(store_attribute_level, ":cha", ":troop_id", ca_charisma),
				(val_mul, ":cha", 5), # This is really a dumb thing to do but I'm not sure this command takes floats
				(val_div, ":cha", 4), # Ends up being 1.25 multiplier, +/- however rounding works.
				(store_random_in_range, ":rand", -3, 6),
				(val_add, ":cha", ":rand"),
				(val_clamp, ":cha", 1, 1000),
				(val_add, ":cash", ":cha"),
				(assign, reg5, ":cha"),
				(str_store_troop_name,s4,":troop_id"),

				(display_message, "@{s4}'s customer paid her {reg5} denars.",0xFFFFD800),
			(try_end),
			(try_begin), # Now the tavernkeepers actually do take a third.
				(neg|party_slot_eq, "$current_town", slot_town_has_brothel, 1),
				(store_div, ":fee", ":cash", 3),
				(assign, reg5, ":fee"),
				(display_message, "@The tavernkeep's fee is {reg5} denars.", message_negative),
				(val_sub, ":cash", ":fee"),
				(val_clamp, ":cash", 1, 1000),
			(try_end),

			(assign, "$f_temp_var", 0),
			(play_sound, "snd_money_received"),
			(troop_add_gold, "trp_player", ":cash"),
			(jump_to_menu, "mnu_town_tavern_prostitution"),
			],
		),
	],
  )
]
