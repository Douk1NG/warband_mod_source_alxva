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

upgrade_hero_party_scripts = [
# script_complete_family_relations
# INPUT: arg1 = party_id, arg2 = xp_amount
("upgrade_hero_party",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":xp_amount", 2),
      ##diplomacy start+
      #Take into account faction quality/quantity settings.  Do not apply this
      #to the player party or to special parties.
      (try_begin),
        (ge, ":party_no", spawn_points_begin),
        (store_faction_of_party, ":var1", ":party_no"),
        (faction_get_slot, ":var1", ":var1", dplmc_slot_faction_quality),
        (val_add, ":var1", 100),
        (val_clamp, ":var1", 97, 104),#100 plus or minus three percent
        (val_mul, ":xp_amount", ":var1"),
        (val_div, ":xp_amount", 100),
      (try_end),
       ##diplomacy end+
      (party_upgrade_with_xp, ":party_no", ":xp_amount", 0),
    ])
]
