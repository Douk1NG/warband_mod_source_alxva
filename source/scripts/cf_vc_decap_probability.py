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

cf_vc_decap_probability_scripts = [
("cf_vc_decap_probability",
    [(store_script_param_1, ":inflicted_agent_id"),
      (store_script_param_2, ":attacker_agent_id"),
      (store_script_param, ":weapon_id",3),

      (agent_is_human, ":inflicted_agent_id"),
      (agent_is_human, ":attacker_agent_id"),
      (gt, ":weapon_id", 0),
	  (get_player_agent_no,":player"),
	  (agent_get_troop_id, ":player_troop", ":player"),

      ### Probability ###
      #BASE: 5
      #IF PLAYER
      #	BASE: +5
      #	IF MOUNTED +30
      #	IF STR>15 : +10
      #	IF PS>7 : +10
      #IF BOT
      #	IF MOUNTED +10
      #IF AXE +5
      #IF HAS HELMET -5
      #MIN CHANCE: 5
      (assign, ":base_chance", 5),

      (try_begin),

        # Mounted bot
        (agent_get_horse, ":horse_id", ":attacker_agent_id"),
        (try_begin),
          (agent_is_non_player, ":attacker_agent_id"),

          (try_begin),
            (neq, ":horse_id", -1),
            (val_add, ":base_chance", 10),
          (try_end),

          #Player bonus
        (else_try),
		  (eq,":attacker_agent_id",":player"),
		  (store_attribute_level, ":skill", ":player_troop", ca_strength),
          (val_add, ":base_chance", ":skill"),
          (try_begin),
            (neq, ":horse_id", -1),
            (val_add, ":base_chance", 30),
          (try_end),
        (try_end),


        # Helmet
        (try_begin),
          (agent_get_item_slot, ":head_gear", ":inflicted_agent_id", ek_head),
          (ge, ":head_gear", 1),
          (item_get_head_armor, ":armor", ":head_gear"),
          (gt, ":armor", 20),
          (val_sub, ":base_chance", 5),
        (try_end),

        (val_max, ":base_chance", 5),
      (try_end),

      (store_random_in_range, ":rand", 0, 101),

      #(val_div, ":base_chance", 2),#VC-3296
      # Debugging
      (ge, ":base_chance", ":rand"),])
]
