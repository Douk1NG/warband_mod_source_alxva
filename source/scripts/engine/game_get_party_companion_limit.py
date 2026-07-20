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

game_get_party_companion_limit_scripts = [
# This script is called from the game engine when the companion limit is needed for a party.
# INPUT: arg1 = none
# OUTPUT: reg0 = companion_limit
("game_get_party_companion_limit",
    [
      (assign, ":troop_no", "trp_player"),

      (assign, ":limit", 30),
      (store_skill_level, ":skill", "skl_leadership", ":troop_no"),
      (store_attribute_level, ":charisma", ":troop_no", ca_charisma),
      (val_mul, ":skill", 5),
      (val_add, ":limit", ":skill"),
      (val_add, ":limit", ":charisma"),

      #SB : possibly inherit half of spouse's renown
      (troop_get_slot, ":troop_renown", ":troop_no", slot_troop_renown),
      (store_div, ":renown_bonus", ":troop_renown", 25),
      (val_add, ":limit", ":renown_bonus"),

      #SB : add non-standard size modifiers here
      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
        (try_begin),
          (faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
          (store_mul, ":king_bonus", "$player_right_to_rule", 5),
          (val_clamp, ":king_bonus", dplmc_marshal_party_bonus, dplmc_monarch_party_bonus + 1), #to match marshal amount
          (val_add, ":limit", ":king_bonus"),
        (try_end),
        (try_begin),
          (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
          (val_add, ":limit", dplmc_marshal_party_bonus),
        (try_end),
        #party takes additional 20 limit per each castle its party leader owns
        (try_for_range, ":cur_center", castles_begin, castles_end),
          (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
          (val_add, ":limit", dplmc_castle_party_bonus),
        (try_end),

        ##diplomacy begin
        (assign, ":percent", 100),
        (assign, ":policy_min", -3),
        (assign, ":policy_max", 4),

        (try_begin),
            (this_or_next|eq, "$players_kingdom", "fac_player_supporters_faction"),
                (faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
            (faction_get_slot, ":policy_max", "$players_kingdom", slot_faction_num_towns),
            (faction_get_slot, reg0, "$players_kingdom", slot_faction_num_castles),
            (val_add, ":policy_max", reg0),
            (val_clamp, ":policy_max", 0, 4),#0, 1, 2, 3
            (store_mul, ":policy_min", ":policy_max", -1),
            (val_add, ":policy_max", 1),#one greater than the maximum
        (try_end),
        ##diplomacy end+

        (try_begin),
          (faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
          # (val_add, ":limit", "$player_right_to_rule"),
          (try_begin),
            (faction_get_slot, ":centralization", "$players_kingdom", dplmc_slot_faction_centralization),
            (neq, ":centralization", 0),
            (val_clamp, ":centralization", ":policy_min", ":policy_max"),
            (val_mul, ":centralization", 10),
            (val_add, ":percent", ":centralization"),
          (try_end),

        (else_try),
          (try_begin),
            (faction_get_slot, ":centralization", "$players_kingdom", dplmc_slot_faction_centralization),
            (neq, ":centralization", 0),
            (val_clamp, ":centralization", ":policy_min", ":policy_max"),
            (val_mul, ":centralization", -3),
            (val_add, ":percent", ":centralization"),
          (try_end),
          (try_begin),
            (faction_get_slot, ":aristocracy", "$players_kingdom", dplmc_slot_faction_aristocracy),
            (neq, ":aristocracy", 0),
            (val_clamp, ":aristocracy", ":policy_min", ":policy_max"),
            (val_mul, ":aristocracy", 3),
            (val_add, ":percent", ":aristocracy"),
          (try_end),
          (try_begin),
            (faction_get_slot, ":quality", "$players_kingdom", dplmc_slot_faction_quality),
            (neq, ":quality", 0),
            (val_clamp, ":quality", ":policy_min", ":policy_max"),
            (val_mul, ":quality", -4),
            (val_add, ":percent", ":quality"),
          (try_end),
        (try_end),

        (try_begin),
          (faction_get_slot, ":serfdom", "$players_kingdom", dplmc_slot_faction_serfdom),
          (neq, ":serfdom", 0),
          (val_clamp, ":serfdom", ":policy_min", ":policy_max"),
          (val_mul, ":serfdom", 2),
          (val_add, ":percent", ":serfdom"),
        (try_end),

        (val_mul, ":limit", ":percent"),
        ##nested diplomacy start+ Round correctly
        (val_add, ":limit", 50),
        ##nested diplomacy end+
        (val_div, ":limit", 100),
        ##diplomacy end
      (try_end),

      (assign, reg0, ":limit"),
      (set_trigger_result, reg0),
    ])
]
