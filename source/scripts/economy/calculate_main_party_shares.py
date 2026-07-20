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

calculate_main_party_shares_scripts = [
("calculate_main_party_shares",
    [
      (assign, ":num_player_party_shares", player_loot_share),
      # Add shares for player's party
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 1, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
          (val_add, ":num_player_party_shares", ":stack_size"),
        (else_try),
          (val_add, ":num_player_party_shares", hero_loot_share),
        (try_end),
      (try_end),

      (assign, reg0, ":num_player_party_shares"),
  ])
]
