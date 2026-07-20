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

get_manhunt_information_to_s15_scripts = [
("get_manhunt_information_to_s15",
    [
     (store_script_param, ":quest", 1),

	(str_store_string, s15, "str_the_roads_are_full_of_brigands_friend_but_that_name_in_particular_does_not_sound_familiar_good_hunting_to_you_nonetheless"),
    (quest_get_slot, ":quarry", ":quest", slot_quest_target_party),
	(try_begin),
		(is_between, "$g_talk_troop", active_npcs_begin, active_npcs_end),
		(troop_get_slot, ":talk_party", "$g_talk_troop", slot_troop_leaded_party),
	(else_try),
		(gt, "$g_encountered_party", "p_spawn_points_end"),
		(assign, ":talk_party", "$g_encountered_party"),
	(else_try),
		(assign, ":talk_party", -1),
	(try_end),

    (try_for_range, ":log_entry", 0, "$num_log_entries"),
		(gt, ":talk_party", -1),
		(troop_get_slot, ":party", "trp_log_array_actor", ":log_entry"),
		(eq, ":party", ":talk_party"),
		(troop_get_slot, ":bandit_party", "trp_log_array_troop_object", ":log_entry"),
		(eq, ":bandit_party", ":quarry"),
		(store_current_hours, ":hours_ago"),
		(troop_get_slot, ":sighting_time", "trp_log_array_entry_time",  ":log_entry"),
		(val_sub, ":hours_ago", ":sighting_time"),
		(try_begin),
			(le, ":hours_ago", 1),
			(str_store_string, s16, "str_less_than_an_hour_ago"),
		(else_try),
			(le, ":hours_ago", 48),
			(assign, reg3, ":hours_ago"),
			(str_store_string, s16, "str_maybe_reg3_hours_ago"),
		(else_try),
			(val_div, ":hours_ago", 24),
			(assign, reg3, ":hours_ago"),
			(str_store_string, s16, "str_reg3_days_ago"),
		(try_end),

		(troop_get_slot, ":center", "trp_log_array_center_object", ":log_entry"),
		(str_store_party_name, s17, ":center"),
		(troop_get_slot, ":entry_type", "trp_log_array_entry_type", ":log_entry"),
		(eq, ":entry_type", logent_party_spots_wanted_bandits),
		(str_store_string, s15, "str_youre_in_luck_we_sighted_those_bastards_s16_near_s17_hurry_and_you_might_be_able_to_pick_up_their_trail_while_its_still_hot"),

#		(try_begin),
#			(eq, ":entry_type", logent_party_chases_wanted_bandits),
#			(str_store_string, s15, "@You're in luck. We gave chase to those bastards {s16} near {s17}. They have eluded us so far -- but perhaps you will do better..."),
#		(else_try),
#			(eq, ":entry_type", logent_party_runs_from_wanted_bandits),
#			(str_store_string, s15, "@As it happens, they tried to run us down near {s17} {s16}. By the heavens, I hope you teach them a lesson."),
#		(try_end),
	(try_end),
	])
]
