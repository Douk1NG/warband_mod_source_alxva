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


   #SB : deprecate these triggers, set party order directly
# Escort merchant caravan:
  

escort_merchant_caravan_mode1_triggers = [
(1, 0.0, ti_once, [
                   # (check_quest_active, "qst_escort_merchant_caravan"),
                   # (eq, "$escort_merchant_caravan_mode", 1)
                   ],
                  [
                   # (quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                   # (try_begin),
                     # (party_is_active, ":quest_target_party"),
                     # (party_set_ai_behavior, ":quest_target_party", ai_bhvr_hold),
                     # (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
                   # (try_end),
                   ]),
]
