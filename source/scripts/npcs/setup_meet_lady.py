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

setup_meet_lady_scripts = [
# script_setup_random_scene
("setup_meet_lady",
    [
      (store_script_param_1, ":lady_no"),
      (store_script_param_2, ":center_no"),

      #(mission_tpl_entry_set_override_flags, "mt_visit_town_castle", 0, af_override_horse),
      (troop_set_slot, ":lady_no", slot_lady_last_suitor, "trp_player"),

      (set_jump_mission,"mt_visit_town_castle"),
      (party_get_slot, ":castle_scene", ":center_no", slot_town_castle),
      (modify_visitors_at_site,":castle_scene"),
      (reset_visitors),

	  (troop_set_age, "trp_nurse_for_lady", 100),
      (set_visitor, 7, "trp_nurse_for_lady"),

      (assign, ":cur_pos", 16),
	  (set_visitor, ":cur_pos", ":lady_no"),

      (assign, "$talk_context", tc_garden),

      (jump_to_scene,":castle_scene"),
      (scene_set_slot, ":castle_scene", slot_scene_visited, 1),
      (change_screen_mission),
	])
]
