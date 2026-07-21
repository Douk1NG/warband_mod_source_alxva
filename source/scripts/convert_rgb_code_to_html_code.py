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

convert_rgb_code_to_html_code_scripts = [
("convert_rgb_code_to_html_code",
    [
      (store_script_param, ":red", 1),
      (store_script_param, ":green", 2),
      (store_script_param, ":blue", 3),

      # (str_store_string, s0, "@#"),

      (store_div, reg11, ":red", 0x10),
      #(store_add, ":dest_string", "str_key_0", reg11"),
      #(str_store_string, s1, ":dest_string"),
      #(str_store_string, s0, "@{s0}{s1}"),

      (store_mod, reg12, ":red", 0x10),
      #(store_add, ":dest_string", "str_key_0", ":r_2"),
      #(str_store_string, s1, ":dest_string"),
      #(str_store_string, s0, "@{s0}{s1}"),

      (store_div, reg13, ":green", 0x10),
      #(store_add, ":dest_string", "str_key_0", ":g_1"),
      #(str_store_string, s1, ":dest_string"),
      #(str_store_string, s0, "@{s0}{s1}"),

      (store_mod, reg14, ":green", 0x10),
      #(store_add, ":dest_string", "str_key_0", ":g_2"),
      #(str_store_string, s1, ":dest_string"),
      #(str_store_string, s0, "@{s0}{s1}"),

      (store_div, reg15, ":blue", 0x10),
      #(store_add, ":dest_string", "str_key_0", ":b_1"),
      #(str_store_string, s1, ":dest_string"),
      #(str_store_string, s0, "@{s0}{s1}"),

      (store_mod, reg16, ":blue", 0x10),
      #(store_add, ":dest_string", "str_key_0", ":b_2"),
      #(str_store_string, s1, ":dest_string"),
      #(str_store_string, s0, "@{s0}{s1}"),
      (str_store_string, s0, "str_html_color"),
    ])
]
