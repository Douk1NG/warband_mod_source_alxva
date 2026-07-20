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

get_enterprise_name_scripts = [
("get_enterprise_name",
    [
		(store_script_param_1, ":item_produced"),
		(assign, ":enterprise_name", "str_bread_site"),
		(try_begin),
			(eq, ":item_produced", "itm_bread"),
			(assign, ":enterprise_name", "str_bread_site"),
		(else_try),
			(eq, ":item_produced", "itm_ale"),
			(assign, ":enterprise_name", "str_ale_site"),
		(else_try),
			(eq, ":item_produced", "itm_oil"),
			(assign, ":enterprise_name", "str_oil_site"),
		(else_try),
			(eq, ":item_produced", "itm_wine"),
			(assign, ":enterprise_name", "str_wine_site"),
		(else_try),
			(eq, ":item_produced", "itm_leatherwork"),
			(assign, ":enterprise_name", "str_leather_site"),
		(else_try),
			(eq, ":item_produced", "itm_wool_cloth"),
			(assign, ":enterprise_name", "str_wool_cloth_site"),
		(else_try),
			(eq, ":item_produced", "itm_linen"),
			(assign, ":enterprise_name", "str_linen_site"),
		(else_try),
			(eq, ":item_produced", "itm_velvet"),
			(assign, ":enterprise_name", "str_velvet_site"),
		(else_try),
			(eq, ":item_produced", "itm_tools"),
			(assign, ":enterprise_name", "str_tool_site"),
		(try_end),
		(assign, reg0, ":enterprise_name"),
	])
]
