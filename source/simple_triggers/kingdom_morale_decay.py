# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *

kingdom_morale_decay_simple_triggers = [
(24,
[
    (try_for_range, ":kingdom_no", npc_kingdoms_begin, npc_kingdoms_end),
      (faction_get_slot, ":faction_morale", ":kingdom_no",  slot_faction_morale_of_player_troops),

	  (store_sub, ":divisor", 140, "$player_right_to_rule"),
	  (val_div, ":divisor", 14),
	  (val_max, ":divisor", 1),

      (store_div, ":faction_morale_div_10", ":faction_morale", ":divisor"), #10 is the base, down to 2 for 100 rtr
      (val_sub, ":faction_morale", ":faction_morale_div_10"),

      (faction_set_slot, ":kingdom_no",  slot_faction_morale_of_player_troops, ":faction_morale"),
    (try_end),
]),
]
