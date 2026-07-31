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

auto_besiege_renown_simple_triggers = [
(1,
   [
      (gt,"$auto_besiege_town",0),
      (gt,"$g_player_besiege_town", 0),
      (ge, "$g_siege_method", 1),
      (store_current_hours, ":cur_hours"),
      (eq, "$g_siege_force_wait", 0),
      (ge, ":cur_hours", "$g_siege_method_finish_hours"),
      (neg|is_currently_night),
      #SB : add adjusted renown for ladder construction
      (try_begin), #we should have stored the original npc but composition is unlikely to change
        (call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
        (assign, ":troop_no", reg1),
        (neq, ":troop_no", "trp_player"),
        # (is_between, ":troop_no", companions_begin, companions_end),
        (store_mul, ":renown", "$g_siege_method", dplmc_companion_skill_renown + 1),
        (call_script, "script_change_troop_renown", ":troop_no", ":renown"),
      (try_end),
      (rest_for_hours, 0, 0, 0), #stop resting
    ]),
]
