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

change_banners_and_chest_scripts = [
# Input: none
# Output: none
("change_banners_and_chest",
    [(party_get_slot, ":cur_leader", "$g_encountered_party", slot_town_lord),
     (try_begin),
       (ge, ":cur_leader", 0),
#normal_banner_begin
       (troop_get_slot, ":troop_banner_object", ":cur_leader", slot_troop_banner_scene_prop),
       (try_begin),
           (gt, ":troop_banner_object", 0),
           (replace_scene_props, banner_scene_props_begin, ":troop_banner_object"),
       (else_try),
           (eq, ":troop_banner_object", -1),
           (troop_get_slot, ":troop_custom_banner_object", ":cur_leader", slot_troop_custom_banner_flag_type),
           (ge, ":troop_custom_banner_object", 0),
           (val_add, ":troop_custom_banner_object", "spr_custom_banner_01"),
           (replace_scene_props, "spr_banner_a", ":troop_custom_banner_object"),
       (try_end),
     (else_try),
       (replace_scene_props, banner_scene_props_begin, "spr_empty"),
     (try_end),
     (try_begin),
       (neq, ":cur_leader", "trp_player"),
       (replace_scene_props, "spr_player_chest", "spr_locked_player_chest"),
     (try_end),
     ])
]
