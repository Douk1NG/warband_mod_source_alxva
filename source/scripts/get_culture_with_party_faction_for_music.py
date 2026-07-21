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

get_culture_with_party_faction_for_music_scripts = [
#script_update_center_notes
# script_get_culture_with_party_faction_for_music
# Input: arg1 = party_no
# Output: reg0 = culture
("get_culture_with_party_faction_for_music",
    [
      (store_script_param, ":party_no", 1),
      (store_faction_of_party, ":faction_no", ":party_no"),
      (try_begin),
        (this_or_next|eq, ":faction_no", "fac_player_faction"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (assign, ":faction_no", "$players_kingdom"),
      (try_end),
      (try_begin),
        (is_between, ":party_no", centers_begin, centers_end),
        (this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
        (neg|is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        (party_get_slot, ":faction_no", ":party_no", slot_center_original_faction),
      (try_end),
      (call_script, "script_get_culture_with_faction_for_music", ":faction_no"),
     ])
]
