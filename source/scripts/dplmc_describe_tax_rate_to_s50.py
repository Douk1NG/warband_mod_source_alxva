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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_describe_tax_rate_to_s50_scripts = [
("dplmc_describe_tax_rate_to_s50",
    [
      (store_script_param_1, ":tax_rate"),
      (val_div, ":tax_rate", 25),
      (store_add, ":str_id","str_dplmc_tax_normal", ":tax_rate"),
      (str_store_string, s50, ":str_id"),
  ])
]
