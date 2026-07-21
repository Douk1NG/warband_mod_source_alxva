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

troop_describes_quarrel_with_troop_to_s14_scripts = [
("troop_describes_quarrel_with_troop_to_s14",
  #perhaps replace this with get_relevant_comment at a later date
    [
	(store_script_param, ":troop", 1),
	(store_script_param, ":troop_2", 2),

	(str_store_troop_name, s15, ":troop"),
	(str_store_troop_name, s16, ":troop_2"),

	(str_store_string, s14, "str_stop_gap__s15_is_the_rival_of_s16"),

	(try_begin),
		(eq, ":troop", "$g_talk_troop"),
		(call_script, "script_cf_test_lord_incompatibility_to_s17", ":troop", ":troop_2"),
		(str_store_string, s14, s17),
	(else_try),
		(eq, ":troop_2", "$g_talk_troop"),
		(call_script, "script_cf_test_lord_incompatibility_to_s17", ":troop_2", ":troop"),
		(str_store_string, s14, s17),
	(else_try),
		(str_store_string, s14, "str_general_quarrel"),
	(try_end),

])
]
