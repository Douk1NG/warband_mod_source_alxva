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

from kingdom_custom_troop_tree_creator_simple_triggers import native_template_health_ops

dummy_empty_triggers_simple_triggers = [
(0, native_template_health_ops),
(24,
   []),
(24,
   []),
(24,
   []),
(24,
   []),
(24,
   []),
(24,
   []),
(24,
   []),
]
