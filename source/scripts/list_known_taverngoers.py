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

list_known_taverngoers_scripts = [
#script_list_known_taverngoers
#input: starting/ending troop range, also party slot if necessary as error check
#output: location of known tavern npcs to s11
("list_known_taverngoers",
  [
      (store_script_param, ":begin", 1),
      (store_script_param, ":end", 2),
      (store_script_param, ":slot_no", 3),

      (assign, ":num_towns", 0),
      (try_for_range, ":troop_no", ":begin", ":end"),
        (this_or_next|troop_slot_ge, ":troop_no", slot_troop_met, 1),
        (troop_slot_eq, ":troop_no", slot_troop_cur_center, "$current_town"),
        (troop_get_slot, ":town_no", ":troop_no", slot_troop_cur_center),
        (is_between, ":town_no", walled_centers_begin, walled_centers_end),
        # (neg|party_slot_eq, ":town_no", slot_center_ransom_broker, 0),
        (party_slot_eq, ":town_no", ":slot_no", ":troop_no"),
        (val_add, ":num_towns", 1),
        (str_store_party_name_link, s50, ":town_no"),
        (try_begin),
          (eq, ":num_towns", 1),
          (str_store_string, s51, s50),
        (else_try),
          (eq, ":num_towns", 2),
          (str_store_string, s51, "str_s50_and_s51"),
        (else_try),
          (str_store_string, s51, "str_s50_comma_s51"),
        (try_end),

        (try_begin), #list false tavern npcs
          (call_script, "script_cf_find_alternative_town_for_taverngoers", ":town_no", -9),
          (assign, ":alternative_town", reg0),
          (neg|party_slot_ge, ":alternative_town", ":slot_no", ":begin"),
          (val_add, ":num_towns", 1),
          (str_store_party_name_link, s52, ":alternative_town"),
          (try_begin), #this is at least the second town in the string
            (eq, ":num_towns", 2),
            (str_store_string, s51, "str_s52_and_s51"),
          (else_try),
            (str_store_string, s51, "str_s52_comma_s51"),
          (try_end),
        (try_end),
        # (display_message, "@{s51}"),
      (try_end),
      (str_store_troop_name_plural, s10, ":begin"), #default titles "book_merchant" "ransom_broker" etc
      (str_store_string_reg, s11, s51),
      (display_message, "@You can find {s10}s at {s11}."),
  ])
]
