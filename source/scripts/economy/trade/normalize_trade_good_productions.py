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

normalize_trade_good_productions_scripts = [
#script_normalize_trade_good_productions
#Adjusts productions according to the amount of the item produced
# INPUT: none
# This currently deprecated, as I was going to try to fine-tune productions
("normalize_trade_good_productions",
    [
      (store_sub, ":item_to_slot", slot_town_trade_good_productions_begin, trade_goods_begin),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (assign, ":total_production", 0),
        (assign, ":num_centers", 0),
        (store_add, ":cur_good_slot", ":cur_good", ":item_to_slot"),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (val_add, ":num_centers", 1),
          (try_begin),
            (is_between, ":center_no", towns_begin, towns_end), #each town is weighted as 5 villages...
            (val_add, ":num_centers", 4),
          (try_end),
          (party_get_slot, ":center_production", ":center_no", ":cur_good_slot"),
          (val_add, ":total_production", ":center_production"),
        (try_end),
        (store_div, ":new_production_difference", ":total_production", ":num_centers"),
        (neq, ":new_production_difference", 0),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (this_or_next|is_between, ":center_no", towns_begin, towns_end),
          (is_between, ":center_no", villages_begin, villages_end),
          (party_get_slot, ":center_production", ":center_no", ":cur_good_slot"),
          (val_sub, ":center_production", ":new_production_difference"),
          (party_set_slot, ":center_no", ":cur_good_slot", ":center_production"),
        (try_end),
      (try_end),
  ])
]
