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

prepare_alley_to_fight_scripts = [
(
   "prepare_alley_to_fight",
   [
     (party_get_slot, ":scene_no", "$current_town", slot_town_alley),

     #(store_faction_of_party, ":faction_no", "$current_town"),

     (modify_visitors_at_site, ":scene_no"),

     (reset_visitors),
     (set_visitor, 0, "trp_player"),

     #(set_visitor, 3, ":bandit_troop"),
     (set_visitor, 3, "trp_bandit"),

     (assign, "$talked_with_merchant", 0),
     (set_jump_mission, "mt_alley_fight"),
     (jump_to_scene, ":scene_no"),
     (change_screen_mission),
   ])
]
