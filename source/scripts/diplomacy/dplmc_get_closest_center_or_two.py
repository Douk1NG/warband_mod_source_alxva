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

dplmc_get_closest_center_or_two_scripts = [
#script_npc_decision_checklist_troop_follow_or_not
# Input: arg1 = party_no
# Output: reg0 = center_no (closest)
#         reg1 = center_no2 (another close center or -1)
#
# If reg1 is non-negative, it should make some sense to say "<party_no> is
# between <reg0> and <reg1>".
#
# The way I do this is:
#   1.  Find the closest center to the party.
#   2.  Excluding the center from (1), find the closest center to the
#       party which is not closer to the center from (1) than it is to
#       the party.  (There might not be any centers matching this
#       description.)
#
# If the party is much closer to center_1 than center_2, I discard
# the second center.  (The rationale is that if I'm standing on my
# doorstep, it is be helpful to say "I am between my house and the
# grocery store".  It is less misleading to just say "I am near my
# house.")
("dplmc_get_closest_center_or_two",
    [
      (store_script_param_1, ":party_no"),
      (call_script, "script_get_closest_center", ":party_no"),#writes closest center to reg0
      (store_distance_to_party_from_party, ":distance_to_beat", ":party_no", reg0),
      (val_mul, ":distance_to_beat", 2),
      (val_add, ":distance_to_beat", 1),

      (assign, reg1, -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (neq, ":center_no", reg0),
        (store_distance_to_party_from_party, ":party_to_center_distance", ":party_no", ":center_no"),
        (lt, ":party_to_center_distance", ":distance_to_beat"),
        (store_distance_to_party_from_party, ":center_to_center_distance", reg0, ":center_no"),
        (gt, ":center_to_center_distance", ":party_to_center_distance"),
        (assign, ":distance_to_beat", ":party_to_center_distance"),
        (assign, reg1, ":center_no"),
      (try_end),
  ])
]
