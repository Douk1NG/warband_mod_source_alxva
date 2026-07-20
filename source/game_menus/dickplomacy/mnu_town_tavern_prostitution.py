# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

town_tavern_prostitution_menu = [
(
    "town_tavern_prostitution",0,
    "{s15}",
    "none",
    [#Auto-exectued
	(try_begin),
		(party_slot_eq, "$current_town", slot_town_has_brothel, 1),
		(str_store_string,s15,"@Your room is luxuriant, comfortable from the linen sheets to the smoothed flooring. The rose-stained glass window illuminates the bed, casting a soft pink glow about the chamber which itself radiates with a mood of pleasure and relaxation."),
	(else_try),
		(str_store_string,s15,"@Your room is nice, if old and worn down. The window holds a dissapointing, but convienent view of a stone wall from the neighboring building. A dim candle lights the otherwise mellow room to provide a somewhat romantic atmosphere."),
	(try_end),
	(set_background_mesh, "mesh_pic_custom_01"),
	(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
	(try_begin),
		(gt, "$g_currently_soliciting", 0),
		(str_store_string,s15,"@The hours drag on as you practice your craft..."), # Everything else has the stupid pluralities, this should too at some point.
		(set_background_mesh, "mesh_pic_custom_02"),
		(assign, ":fems", 0),
		(try_for_range, ":i_stack", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":troop_id", "p_main_party", ":i_stack"),
			(troop_is_hero, ":troop_id"),
			(call_script, "script_cf_dplmc_troop_is_female", ":troop_id"),
			(val_add, ":fems", 1),
		(try_end),
		(store_random_in_range, ":ff", 0, ":fems"),
		(try_begin),
			(try_for_range, ":i_stack", 0, ":num_stacks"),
				(party_stack_get_troop_id, ":troop_id", "p_main_party", ":i_stack"),
				(troop_is_hero, ":troop_id"),
				(call_script, "script_cf_dplmc_troop_is_female", ":troop_id"),
				(try_begin),
					(gt, ":ff", 0),
					(val_sub, ":ff", 1),
				(else_try),
					(eq, ":ff", 0),
					(val_sub, ":ff", 1),
					(assign, "$f_temp_var", ":troop_id"),
					(str_store_troop_name,s4,":troop_id"),
				(try_end),
			(try_end),
		(try_end),
	(try_end),
	],
	[
	 ("solicit_clients",
	 [(le, "$g_currently_soliciting", 0),],
	 "Solicit customers.",
		[
		(assign, "$g_currently_soliciting", "$current_town"),
		(try_begin),
			(party_slot_eq, "$current_town", slot_town_has_brothel, 1),
			(rest_for_hours, 24, 6, 0),
		(else_try),
			(rest_for_hours, 24, 3, 0),
		(try_end),
		(change_screen_return),
		],
	 ),

	 ("just_do_it",[(gt, "$g_currently_soliciting", 0),],"Watch {s4} with her customer.",
		[
		(assign, "$g_currently_soliciting", 0),
		(assign, ":workgirl", "$f_temp_var"),

		(party_get_slot, ":center_faction", "$current_town", slot_center_original_faction),
		(faction_get_slot, ":center_culture", ":center_faction", slot_faction_culture),
		(assign, ":customer1", 0),
		(assign, ":dna1", 0),
		(assign, ":customer2", 0),
		(assign, ":dna2", 0),

		(try_for_range,":entry",0,2), #generate 2 townspeople
			(faction_get_slot, ":town_walker", ":center_culture", slot_faction_town_walker_male_troop),
			(store_random_in_range,":rand",0,9), #dckplmc - randomly male or female
			(try_begin),
				(eq, ":rand", 1),
				(store_add, ":town_walker", 1, ":town_walker"),
			(try_end),
			(store_random_in_range,":dna",0,1000),
			(try_begin),
				(eq, ":customer1", 0),
				(assign, ":customer1", ":town_walker"),
				(assign, ":dna1", ":dna"),
			(else_try),
				(assign, ":customer2", ":town_walker"),
				(assign, ":dna2", ":dna"),
			(try_end),
		(try_end),

		(troop_set_slot, "trp_temp_array_a", 0, ":workgirl"),
		(troop_set_slot, "trp_temp_array_b", 0, -1), #Will always be a hero, so no dna needed
		(troop_set_slot, "trp_temp_array_a", 1, ":customer1"),
		(troop_set_slot, "trp_temp_array_b", 1, ":dna1"),
		(troop_set_slot, "trp_temp_array_a", 2, -1), #observer
		(troop_set_slot, "trp_temp_array_b", 2, -1),
		(troop_set_slot, "trp_temp_array_a", 3, ":customer2"),
		(troop_set_slot, "trp_temp_array_b", 3, ":dna2"),

		(assign, "$f_cons1", 0), #Con
		(assign, "$f_cons2", 0), #Con
		(assign, "$f_cons3", 0), #Con
		(assign, "$f_cons4", 0), #Con

		(assign, "$f_encountertype", 2),

		(store_random_in_range,"$g_sex_position",0,3), #Random position type
		(try_begin),
			(eq, "$g_sex_position", 2),
			(assign, ":pos", 4),
		(else_try),
			(assign, ":pos", 2),
		(try_end),

		(assign, ":scene", "scn_tavern"),
		(call_script, "script_start_fucking", ":pos", ":scene"),
		],
	 ),

	 ("back_to_town",
	 [
	 	(try_begin),
			(party_slot_eq, "$current_town", slot_town_has_brothel, 1),
			(str_store_string,s16,"@Leave your brothel."),
		(else_try),
			(str_store_string,s16,"@Leave the tavern."),
		(try_end),
	 ]
	 ,"{s16}",
		[
		(jump_to_menu, "mnu_town"),
		],
	 ),
	],
  )
]
