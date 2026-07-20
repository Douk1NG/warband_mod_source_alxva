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

dplmc_describe_prosperity_to_s4_scripts = [
##diplomacy begin
("dplmc_describe_prosperity_to_s4",
    [
      (store_script_param_1, ":center_no"),

      (str_store_party_name, s60,":center_no"),
      (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
      (str_store_string, s4, "str_empty_string"),
      (try_begin),
        (is_between, ":center_no", towns_begin, towns_end),
        (try_begin),
          (eq, ":prosperity", 0),
          (str_store_string, s4, "str_town_prosperity_0"),
        (else_try),
          (is_between, ":prosperity", 1, 11),
          (str_store_string, s4, "str_town_prosperity_10"),
        (else_try),
          (is_between, ":prosperity", 11, 21),
          (str_store_string, s4, "str_town_prosperity_20"),
        (else_try),
          (is_between, ":prosperity", 21, 31),
          (str_store_string, s4, "str_town_prosperity_30"),
        (else_try),
          (is_between, ":prosperity", 31, 41),
          (str_store_string, s4, "str_town_prosperity_40"),
        (else_try),
          (is_between, ":prosperity", 41, 51),
          (str_store_string, s4, "str_town_prosperity_50"),
        (else_try),
          (is_between, ":prosperity", 51, 61),
          (str_store_string, s4, "str_town_prosperity_60"),
        (else_try),
          (is_between, ":prosperity", 61, 71),
          (str_store_string, s4, "str_town_prosperity_70"),
        (else_try),
          (is_between, ":prosperity", 71, 81),
          (str_store_string, s4, "str_town_prosperity_80"),
        (else_try),
          (is_between, ":prosperity", 81, 91),
          (str_store_string, s4, "str_town_prosperity_90"),
        (else_try),
          (is_between, ":prosperity", 91, 101),
          (str_store_string, s4, "str_town_prosperity_100"),
        (try_end),
      (else_try),
        (is_between, ":center_no", villages_begin, villages_end),
        (try_begin),
          (eq, ":prosperity", 0),
          (str_store_string, s4, "str_village_prosperity_0"),
        (else_try),
          (is_between, ":prosperity", 1, 11),
          (str_store_string, s4, "str_village_prosperity_10"),
        (else_try),
          (is_between, ":prosperity", 11, 21),
          (str_store_string, s4, "str_village_prosperity_20"),
        (else_try),
          (is_between, ":prosperity", 21, 31),
          (str_store_string, s4, "str_village_prosperity_30"),
        (else_try),
          (is_between, ":prosperity", 31, 41),
          (str_store_string, s4, "str_village_prosperity_40"),
        (else_try),
          (is_between, ":prosperity", 41, 51),
          (str_store_string, s4, "str_village_prosperity_50"),
        (else_try),
          (is_between, ":prosperity", 51, 61),
          (str_store_string, s4, "str_village_prosperity_60"),
        (else_try),
          (is_between, ":prosperity", 61, 71),
          (str_store_string, s4, "str_village_prosperity_70"),
        (else_try),
          (is_between, ":prosperity", 71, 81),
          (str_store_string, s4, "str_village_prosperity_80"),
        (else_try),
          (is_between, ":prosperity", 81, 91),
          (str_store_string, s4, "str_village_prosperity_90"),
        (else_try),
          (is_between, ":prosperity", 91, 101),
          (str_store_string, s4, "str_village_prosperity_100"),
        (try_end),
      (try_end),
        ])
]
