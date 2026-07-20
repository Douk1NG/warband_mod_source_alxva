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

troop_write_owned_centers_to_s2_scripts = [
# script_troop_write_owned_centers_to_s2
# Input: arg1 = troop_no
# Output: none
("troop_write_owned_centers_to_s2",
    [
      (store_script_param_1, ":troop_no"),

      (call_script, "script_get_number_of_hero_centers", ":troop_no"),
      (assign, ":no_centers", reg0),

      (str_store_troop_name, s5, ":troop_no"),

      (try_begin),
        (gt, ":no_centers", 1),
        (try_for_range, ":i_center", 1, ":no_centers"),
          (call_script, "script_troop_get_leaded_center_with_index", ":troop_no", ":i_center"),
          (str_store_party_name_link, s50, reg0),
          (try_begin),
            (eq, ":i_center", 1),
            (call_script, "script_troop_get_leaded_center_with_index", ":troop_no", 0),
            (str_store_party_name_link, s51, reg0),
            (str_store_string, s51, "str_s50_and_s51"),
          (else_try),
            (str_store_string, s51, "str_s50_comma_s51"),
          (try_end),
        (try_end),
        (str_store_string, s2, "str_s5_is_the_ruler_of_s51"),
      (else_try),
        (eq, ":no_centers", 1),
        (call_script, "script_troop_get_leaded_center_with_index", ":troop_no", 0),
        (str_store_party_name_link, s51, reg0),
        (str_store_string, s2, "str_s5_is_the_ruler_of_s51"),
      (else_try),
        (store_troop_faction, ":faction_no", ":troop_no"),
        (str_store_faction_name_link, s6, ":faction_no"),
        ##diplomacy start+ make gender-correct
        #(troop_get_type, reg4, ":troop_no"),
        (assign, ":save_reg4", reg4),
        (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 4),
        (str_store_string, s2, "str_s5_is_a_nobleman_of_s6"),
        (assign, reg4, ":save_reg4"),
        ##diplomacy end+
      (try_end),
  ])
]
