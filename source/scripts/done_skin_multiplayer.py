# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

done_skin_multiplayer_scripts = [
# script_party_get_ideal_size @used for NPC parties.
("done_skin_multiplayer",
	[
		(store_script_param, ":agent_no", 1),
		(try_begin),
			(agent_is_active, ":agent_no"),
			(agent_is_alive, ":agent_no"),
			(agent_is_human, ":agent_no"),
			(agent_get_item_slot, ":body_armor", ":agent_no", ek_body),
			(eq, ":body_armor", -1),
			(agent_equip_item, ":agent_no", "itm_loincloth"), # man also equip - troop_type always 0 - "is_female" not working
		(try_end),
	]
  )
]
