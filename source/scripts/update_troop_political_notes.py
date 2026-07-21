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

update_troop_political_notes_scripts = [
#script_update_troop_notes
("update_troop_political_notes",
      [
		(store_script_param, ":troop_no", 1),
		(try_begin),
		    (str_clear, s47),

			(store_faction_of_troop, ":troop_faction", ":troop_no"),

		    (faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),

		    (str_clear, s40),
		    (assign, ":logged_a_rivalry", 0),
		    (try_for_range, ":kingdom_hero", active_npcs_begin, active_npcs_end),
				(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":kingdom_hero"),
				(lt, reg0, -10),

		   		(str_store_troop_name_link, s39, ":kingdom_hero"),
				(try_begin),
					(eq, ":logged_a_rivalry", 0),
					(str_store_string, s40, "str_s39_rival"),
					(assign, ":logged_a_rivalry", 1),
				(else_try),
					(str_store_string, s41, "str_s40"),
					(str_store_string, s40, "str_s41_s39_rival"),
				(try_end),

		    (try_end),

		    (str_clear, s46),
		    (try_begin),
				(ge, "$cheat_mode", 1),
				(try_begin),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
					(str_store_string, s46, "str_reputation_cheat_mode_only_martial_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
					(str_store_string, s46, "str_reputation_cheat_mode_only_debauched_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
					(str_store_string, s46, "str_reputation_cheat_mode_only_pitiless_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
					(str_store_string, s46, "str_reputation_cheat_mode_only_calculating_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
					(str_store_string, s46, "str_reputation_cheat_mode_only_quarrelsome_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
					(str_store_string, s46, "str_reputation_cheat_mode_only_goodnatured_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
					(str_store_string, s46, "str_reputation_cheat_mode_only_upstanding_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_conventional),
					(str_store_string, s46, "str_reputation_cheat_mode_only_conventional_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_adventurous),
					(str_store_string, s46, "str_reputation_cheat_mode_only_adventurous_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_otherworldly),
					(str_store_string, s46, "str_reputation_cheat_mode_only_romantic_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_moralist),
					(str_store_string, s46, "str_reputation_cheat_mode_only_moralist_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_ambitious),
					(str_store_string, s46, "str_reputation_cheat_mode_only_ambitious_"),
				(else_try),
					(troop_get_slot, reg11, ":troop_no", slot_lord_reputation_type),
					(str_store_string, s46, "str_reputation_cheat_mode_only_reg11_"),
				(try_end),

				(try_begin),
					(eq, "$cheat_mode", 1),
					(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
						(troop_get_slot, ":love_interest", ":troop_no", ":love_interest_slot"),
						(is_between, ":love_interest", kingdom_ladies_begin, kingdom_ladies_end),
						(str_store_troop_name_link, s39, ":love_interest"),
						(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":love_interest"),
						(str_store_string, s2, "str_love_interest"),
						(try_begin),
							(troop_slot_eq, ":troop_no", slot_troop_betrothed, ":love_interest"),
							(str_store_string, s2, "str_betrothed"),
						(try_end),
						(str_store_string, s40, "str_s40_s39_s2_reg0"),
					(try_end),
				(try_end),

		    (try_end),

		    (str_store_string, s45, "str_other_relations_s40_"),

		    (str_clear, s44),
		    (try_begin),
				(neq, ":troop_no", ":faction_leader"),
				(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
				(str_store_string, s44, "str_relation_with_liege_reg0_"),
		    (try_end),

			(str_clear, s48),

		    (try_begin),
				(eq, "$cheat_mode", 1),
				(store_current_hours, ":hours"),
				(gt, ":hours", 0),
#				(display_message, "@{!}Updating political factors"),
				(call_script, "script_calculate_troop_political_factors_for_liege", ":troop_no", ":faction_leader"),
				(str_store_string, s48, "str_sense_of_security_military_reg1_court_position_reg3_"),
			(try_end),
			(str_store_string, s47, "str_s46s45s44s48"),

			(add_troop_note_from_sreg, ":troop_no", 3, "str_political_details_s47_", 1),

		(try_end),
    ])
]
