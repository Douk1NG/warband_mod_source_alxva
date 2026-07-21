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

inflict_casualties_to_party_scripts = [
("inflict_casualties_to_party",
    [
      (party_clear, "p_temp_casualties"),
      (store_script_param_1, ":party"), #Party_id
      (call_script, "script_party_count_fit_regulars", ":party"),
      (assign, ":num_fit", reg(0)), #reg(47) = number of fit regulars.
      (store_script_param_2, ":num_attack_rounds"), #number of attacks
      (try_for_range, ":unused", 0, ":num_attack_rounds"),
        (gt, ":num_fit", 0),
        (store_random_in_range, ":attacked_troop_rank", 0 , ":num_fit"), #attack troop with rank reg(46)
        (assign, reg1, ":attacked_troop_rank"),
        (call_script, "script_get_stack_with_rank", ":party", ":attacked_troop_rank"),
        (assign, ":attacked_stack", reg(0)), #reg(53) = stack no to attack.
        (party_stack_get_troop_id,     ":attacked_troop",":party",":attacked_stack"),
        (store_character_level, ":troop_toughness", ":attacked_troop"),
        (val_add, ":troop_toughness", 5),  #troop-toughness = level + 5
        (assign, ":casualty_chance", 10000),
        (val_div, ":casualty_chance", ":troop_toughness"), #dying chance
        (try_begin),
          (store_random_in_range, ":rand_num", 0 ,10000),
          (lt, ":rand_num", ":casualty_chance"), #check chance to be a casualty
          (store_random_in_range, ":rand_num2", 0, 2), #check if this troop will be wounded or killed
          (try_begin),
            (troop_is_hero,":attacked_troop"), #currently troop can't be a hero, but no harm in keeping this.
            (store_troop_health, ":troop_hp",":attacked_troop"),
            (val_sub, ":troop_hp", 45),
            (val_max, ":troop_hp", 1),
            (troop_set_health, ":attacked_troop", ":troop_hp"),
          (else_try),
            (lt, ":rand_num2", 1), #wounded
            (party_add_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_wound_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_wound_members, ":party", ":attacked_troop", 1),
          (else_try), #killed
            (party_add_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_remove_members, ":party", ":attacked_troop", 1),
          (try_end),
          (val_sub, ":num_fit", 1), #adjust number of fit regulars.
        (try_end),
      (try_end),
  ])
]
