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

auto_upgrade_troops_simple_triggers = [
(1,
[
    (store_time_of_day, ":cur_hour"),
    (eq, ":cur_hour", 0),
    (call_script, "script_auto_upgrade_troops"),
]),
]
