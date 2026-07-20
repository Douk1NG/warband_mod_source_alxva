# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

add_lady_items_scripts = [
#Troop Commentaries begin
("add_lady_items",
	[
	(store_script_param, ":lady_no", 1),
	(troop_equip_items, ":lady_no"),

	(store_faction_of_troop, ":faction_no", ":lady_no"),

	(store_random_in_range, ":random", 0, 6),

	(try_begin), #assign clothes
		(this_or_next|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_adventurous),
			(troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_ambitious),

		(this_or_next|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_adventurous),
			(lt, ":random", 2),

		(neg|troop_slot_ge, ":lady_no", slot_troop_age, 40),
		(try_begin),
			(eq, ":faction_no", "fac_kingdom_2"),
			(lt, ":random", 4),
			(troop_add_item, ":lady_no", "itm_fur_coat", 0),
		(else_try),
			(eq, ":faction_no", "fac_kingdom_3"),
			(lt, ":random", 3),
			(troop_add_item, ":lady_no", "itm_nomad_robe", 0),
		(else_try),
			(troop_add_item, ":lady_no", "itm_nomad_vest", 0),
		(try_end),
	(else_try),
		(eq, ":faction_no", "fac_kingdom_1"),
		(try_begin),
			(lt, ":random", 2),
			(troop_add_item, ":lady_no", "itm_lady_dress_ruby", 0),
		(else_try),
			(lt, ":random", 4),
			(troop_add_item, ":lady_no", "itm_lady_dress_green", 0),
		(else_try),
			(troop_add_item, ":lady_no", "itm_lady_dress_blue", 0),
		(try_end),
	(else_try),
		(eq, ":faction_no", "fac_kingdom_2"),
		(try_begin),
			(eq, ":random", 0),
			(troop_add_item, ":lady_no", "itm_blue_dress", 0),
		(else_try),
			(eq, ":random", 1),
			(troop_add_item, ":lady_no", "itm_lady_dress_green", 0),
		(else_try),
			(eq, ":random", 2),
			(troop_add_item, ":lady_no", "itm_lady_dress_blue", 0),
		(else_try),
			(lt, ":random", 5),
			(neg|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_conventional),
			(neg|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_ambitious),
			(troop_add_item, ":lady_no", "itm_peasant_dress", 0),
		(else_try),
			(lt, ":random", 5),
			(troop_add_item, ":lady_no", "itm_lady_dress_ruby", 0),
		(else_try),
			(troop_add_item, ":lady_no", "itm_court_dress", 0),
		(try_end),

	(else_try),
		(eq, ":faction_no", "fac_kingdom_3"),
		(troop_add_item, ":lady_no", "itm_khergit_lady_dress", 0),

	(else_try),
		(eq, ":faction_no", "fac_kingdom_4"),

	(else_try),
		(eq, ":faction_no", "fac_kingdom_5"),


	(try_end),
	(troop_equip_items, ":lady_no"),

	#also available:
	#itm_blue_dress
	#itm_court_dress

	#to add for khergits -- salwar/shalvar?
	#western tang costume (p105, china's golden age)
	#kipchak woman from russia book

	(try_begin), #assign headguear matched to item
		(this_or_next|troop_has_item_equipped, ":lady_no", "itm_nomad_vest"),
		(this_or_next|troop_has_item_equipped, ":lady_no", "itm_fur_coat"),
			(troop_has_item_equipped, ":lady_no", "itm_nomad_robe"),

		#assign no headgear
	(else_try),
		(this_or_next|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_moralist),
		(this_or_next|troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_conventional),
			(lt, ":random", 2),


		(try_begin),
			(troop_has_item_equipped, ":lady_no", "itm_khergit_lady_dress"),
			(troop_add_item, ":lady_no", "itm_khergit_lady_hat", 0),

		(else_try),
			(troop_has_item_equipped, ":lady_no", "itm_lady_dress_ruby"),
			(troop_add_item, ":lady_no", "itm_turret_hat_ruby", 0),

			(str_store_troop_name, s4, ":lady_no"),
#			(display_message, "@Giving ruby turret hat to {s4}"),
		(else_try),
			(troop_has_item_equipped, ":lady_no", "itm_lady_dress_blue"),
			(troop_add_item, ":lady_no", "itm_turret_hat_blue", 0),

			(str_store_troop_name, s4, ":lady_no"),
#			(display_message, "@Giving blue turret hat to {s4}"),
		(else_try),
			(troop_has_item_equipped, ":lady_no", "itm_lady_dress_green"),
			(troop_add_item, ":lady_no", "itm_turret_hat_green", 0),

			(str_store_troop_name, s4, ":lady_no"),
#			(display_message, "@Giving green turret hat to {s4}"),
		(else_try),
			(troop_has_item_equipped, ":lady_no", "itm_green_dress"),
			(troop_add_item, ":lady_no", "itm_wimple_with_veil", 0),

			(str_store_troop_name, s4, ":lady_no"),
#			(display_message, "@Giving green-lined wimple to {s4}"),
		(else_try),
			(neq, ":faction_no", "fac_kingdom_3"),
			(neq, ":faction_no", "fac_kingdom_6"),
			(troop_add_item, ":lady_no", "itm_wimple_a", 0),

			(str_store_troop_name, s4, ":lady_no"),
#			(display_message, "@Giving red-lined wimple to {s4}"),
		(else_try),
			(eq, ":faction_no", "fac_kingdom_6"),
			(try_begin),
				(troop_has_item_equipped, ":lady_no", "itm_sarranid_lady_dress"),
				(troop_add_item, ":lady_no", "itm_sarranid_head_cloth", 0),
			(else_try),
				(troop_add_item, ":lady_no", "itm_sarranid_head_cloth_b", 0),
			(try_end),
		(try_end),
	(try_end),
	(troop_equip_items, ":lady_no"),
	##diplomacy start+
	##Save personal items of kingdom ladies
	(call_script, "script_dplmc_save_civilian_clothing", ":lady_no"),
	##diplomacy end+
	]
	)
]
