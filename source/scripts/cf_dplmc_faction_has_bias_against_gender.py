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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

cf_dplmc_faction_has_bias_against_gender_scripts = [
##"script_dplmc_troop_get_family_relation_to_troop"
("cf_dplmc_faction_has_bias_against_gender", [
	(store_script_param_1, ":faction_no"),
	(store_script_param_2, ":test_gender"),#Special: 1 is female

    (assign, reg0, 0),
	(lt, "$g_disable_condescending_comments", 2),#If bias is disabled, do not continue
	(is_between, ":test_gender", 0, 2),#valid genders are 0 and 1

	(try_begin),
		(eq, ":faction_no", "fac_player_supporters_faction"),
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(assign, ":faction_no", "$players_kingdom"),
	(try_end),

	(try_begin),
		#For a-typical factions, nothing by default.
		(neg|is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
	(else_try),
		#If the leader has that gender, no prejudice.
		(faction_get_slot, ":active_npc", ":faction_no", slot_faction_leader),
		(gt, ":active_npc", -1),
		(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
		(eq, reg0, ":test_gender"),
		(assign, reg0, 0),
	(else_try),
		#Traditional gender prejudice if both are true:
		#1.  The faction has no original members of the specified gender.
		#2.  The faction has original members with non-accepting lord personalities.

		(assign, ":num_closeminded", 0),
		(assign, ":end_cond", active_npcs_end),

		(try_for_range, ":active_npc", active_npcs_begin, ":end_cond"),#Deliberately do not include kingdom ladies
			#Also deliberately exclude companions and pretenders
			#(Pretenders are marginalized at the start of the game, and
			#companions don't necessarily start in positions of power either)
			(this_or_next|is_between, ":active_npc", kings_begin, kings_end),
				(is_between, ":active_npc", lords_begin, lords_end),
			(troop_slot_eq, ":active_npc", slot_troop_original_faction, ":faction_no"),

			(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
			(try_begin),
				(eq, reg0, ":test_gender"),
				(assign, ":num_closeminded", -1000),
				(assign, ":end_cond", ":active_npc"),
			(else_try),
				(troop_get_slot, reg0, ":active_npc", slot_lord_reputation_type),
				(is_between, reg0, lrep_none + 1, lrep_roguish),#Lord (non-commoner, non-liege, non-lady) personality type
				(neq, reg0, lrep_cunning),
				(neq, reg0, lrep_goodnatured),
				(val_add, ":num_closeminded", 1),
			(try_end),
		(try_end),

		(store_sub, reg0, ":num_closeminded", 1),#Needs at least one
		(val_clamp, reg0, 0, 2),
	(try_end),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(assign, ":end_cond", reg1),#just save reg1 and reg2 (ignore the normal meaning of the variable names)
		(assign, ":active_npc", reg2),
		(assign, reg1, ":faction_no"),
		(assign, reg2, ":test_gender"),
		(display_message, "@{!} Checked if faction {reg1} is prejudiced against {reg2?women:men}: {reg0?true:false}"),
		(assign, reg1, ":end_cond"),#revert reg1 and reg2 (ignore the normal meaning of the variable names)
		(assign, reg2, ":active_npc"),
	(try_end),
	(gt, reg0, 0),
])
]
