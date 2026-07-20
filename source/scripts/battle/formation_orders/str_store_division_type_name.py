# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

str_store_division_type_name_scripts = [
("str_store_division_type_name", [
      (store_script_param, ":str_reg", 1),
      (store_script_param, ":division_type", 2),
      (try_begin),
        (eq, ":division_type", sdt_infantry),
        (str_store_string, ":str_reg", "@infantry"),
      (else_try),
        (eq, ":division_type", sdt_archer),
        (str_store_string, ":str_reg", "@archer"),
      (else_try),
        (eq, ":division_type", sdt_cavalry),
        (str_store_string, ":str_reg", "@cavalry"),
      (else_try),
        (eq, ":division_type", sdt_polearm),
        (str_store_string, ":str_reg", "@polearm"),
      (else_try),
        (eq, ":division_type", sdt_skirmisher),
        (str_store_string, ":str_reg", "@skirmisher"),
      (else_try),
        (eq, ":division_type", sdt_harcher),
        (str_store_string, ":str_reg", "@mounted archer"),
      (else_try),
        (eq, ":division_type", sdt_support),
        (str_store_string, ":str_reg", "@support"),
      (else_try),
        (eq, ":division_type", sdt_bodyguard),
        (str_store_string, ":str_reg", "@bodyguard"),
      (else_try),
        (str_store_string, ":str_reg", "@undetermined type of"),
      (try_end),])
]
