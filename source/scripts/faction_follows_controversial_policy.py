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

faction_follows_controversial_policy_scripts = [
("faction_follows_controversial_policy",
	[
	(store_script_param, ":faction_no", 1),
	(store_script_param, ":policy_type", 2),

	(faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(str_store_faction_name, s3, ":faction_no"),
		(display_message, "str_calculating_effect_for_policy_for_s3"),

		(val_add, "$number_of_controversial_policy_decisions", 1),
	(try_end),

	(try_begin),
		(eq, ":policy_type", logent_policy_ruler_attacks_without_provocation),
		(assign, ":hawk_relation_effect", 0),
		(assign, ":honorable_relation_effect", -2),
		(assign, ":honor_change", -1),

	(else_try),
		(eq, ":policy_type", logent_policy_ruler_ignores_provocation),
		(assign, ":hawk_relation_effect", -3),
		(assign, ":honorable_relation_effect", 0),
		(assign, ":honor_change", 0),

	(else_try),
		(eq, ":policy_type", logent_policy_ruler_declares_war_with_justification),
		(assign, ":hawk_relation_effect", 3),
		(assign, ":honorable_relation_effect", 1),
		(assign, ":honor_change", 0),

	(else_try),
		(eq, ":policy_type", logent_policy_ruler_breaks_truce),
		(assign, ":hawk_relation_effect", 0),
		(assign, ":honorable_relation_effect", -3),
		(assign, ":honor_change", -5),

	(else_try),
		(eq, ":policy_type", logent_policy_ruler_makes_peace_too_soon),
		(assign, ":hawk_relation_effect", -5),
		(assign, ":honorable_relation_effect", 0),
		(assign, ":honor_change", 0),

	##diplomacy start+ If none of the preceeding match, don't use random memory
	(else_try),
		(assign, ":hawk_relation_effect", 0),
		(assign, ":honorable_relation_effect", 0),
		(assign, ":honor_change", 0),
	##diplomacy end+
	(try_end),

	(try_begin),
		(eq, ":faction_leader", "trp_player"),
		(call_script, "script_change_player_honor", ":honor_change"),
	(try_end),

   ##diplomacy start+ add support for promoted kingdom ladies
	#(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
	(try_for_range, ":lord", heroes_begin, heroes_end),
	##diplomacy end+
		(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
		(store_faction_of_troop, ":lord_faction", ":lord"),
		(eq, ":lord_faction", ":faction_no"),
		(neq, ":lord", ":faction_leader"),

		(try_begin),
		   ##diplomacy start+ Add support for lady personality type
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_adventurous),
			##diplomacy end+
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_martial),
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_quarrelsome),
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_selfrighteous),
				(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_debauched),
			(call_script, "script_troop_change_relation_with_troop", ":faction_leader", ":lord", ":hawk_relation_effect"),
			(val_add, "$total_policy_dispute_changes", ":hawk_relation_effect"),
		(try_end),

		(try_begin),
		   ##diplomacy start+ Add support for lady personality type
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_moralist),
			##diplomacy end+
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_martial),
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_goodnatured),
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_selfrighteous),
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_benefactor), #new for enfiefed commoners
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_custodian), #new for enfiefed commoners
				(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_upstanding),
			(call_script, "script_troop_change_relation_with_troop", ":faction_leader", ":lord", ":honorable_relation_effect"),
			(val_add, "$total_policy_dispute_changes", ":honorable_relation_effect"),

		(try_end),

	(try_end),

	])
]
