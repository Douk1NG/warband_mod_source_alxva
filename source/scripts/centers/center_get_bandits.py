# ======================================================================
# SHARED DEPENDENCY
# Entity: center_get_bandits (script)
# Called by menus in 2 domains: cheats, village
# ======================================================================

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

center_get_bandits_scripts = [
("center_get_bandits",[

    (store_script_param_1, ":village_no"),
    (store_script_param_2, ":mode"),
    (assign, ":bandit_troop", "trp_looter"),

    (try_begin), #native mode
      (eq, ":mode", -1),
      (store_random_in_range, ":random_no", 0, 3),
      (try_begin),
        (eq, ":random_no", 0),
        (assign, ":bandit_troop", "trp_bandit"),
      (else_try),
        (eq, ":random_no", 1),
        (assign, ":bandit_troop", "trp_mountain_bandit"),
      (else_try),
        (assign, ":bandit_troop", "trp_forest_bandit"),
      (try_end),
    (else_try), #faction mode
      (eq, ":mode", 0),

      (assign, ":bandit_troop", "trp_looter"),
      # (store_faction_of_party, ":faction", ":village_no"),
      (party_get_slot, ":faction", ":village_no", slot_center_original_faction),
      (store_random_in_range, ":random_no", 0, 10),
      (try_begin), #deserter troops, 10% chance
        (eq, ":random_no", 0),
        (faction_get_slot, ":bandit_troop", ":faction", slot_faction_deserter_troop),
      (else_try),
        (lt, ":random_no", 6),  #regular bandits (looter to brigand), 50%
        (val_div, ":random_no", 2),
        (store_add, ":bandit_troop","trp_looter",":random_no"),
      (else_try), #regional bandits, 40% (should be terrain based though)
        (try_begin),
          (eq, ":faction", "fac_kingdom_6"),
          (assign, ":bandit_troop", "trp_desert_bandit"),
        (else_try),
          (eq, ":faction", "fac_kingdom_5"),
          (assign, ":bandit_troop", "trp_mountain_bandit"),
        (else_try),
          (eq, ":faction", "fac_kingdom_4"),
          (assign, ":bandit_troop", "trp_sea_raider"),
        (else_try),
          (eq, ":faction", "fac_kingdom_3"),
		  (try_begin),
			(lt, ":random_no", 3),
			(assign, ":bandit_troop", "trp_black_khergit_horseman"), # dckplmc - 20% chance of black khergits
		  (else_try),
			(assign, ":bandit_troop", "trp_steppe_bandit"),
		  (try_end),
        (else_try),
          (eq, ":faction", "fac_kingdom_2"),
          (assign, ":bandit_troop", "trp_taiga_bandit"),
        (else_try),
          (eq, ":faction", "fac_kingdom_1"),
          (assign, ":bandit_troop", "trp_forest_bandit"),
        (try_end),
      (try_end),
    (else_try), #terrain mode
      (eq, ":mode", 1),
      #base type first
      (party_get_current_terrain, ":terrain_type", ":village_no"),
      (try_begin),
        (this_or_next|eq, ":terrain_type", rt_steppe),
        (eq, ":terrain_type", rt_steppe_forest),
		(store_random_in_range, ":random_no", 0, 10),
	    (try_begin),
		  (lt, ":random_no", 3),
		  (assign, ":bandit_troop", "trp_black_khergit_horseman"), # dckplmc - 20% chance of black khergits
	    (else_try),
		  (assign, ":bandit_troop", "trp_steppe_bandit"),
	    (try_end),
      # (else_try),
        # (eq, ":terrain_type", rt_plain),
        # (assign, ":bandit_troop", "trp_bandit"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_snow),
        (eq, ":terrain_type", rt_snow_forest),
        (assign, ":bandit_troop", "trp_taiga_bandit"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_desert),
        (eq, ":terrain_type", rt_desert_forest),
        (assign, ":bandit_troop", "trp_desert_bandit"),
      # (else_try),
        # (eq, ":terrain_type", rt_forest),
        # (assign, ":bandit_troop", "trp_forest_bandit"),
      (try_end),
      (try_begin),
        (eq, ":bandit_troop", "trp_looter"), #still not picked
        #proximity to features (forest, mountain, ocean),
        (party_get_position, pos1, ":village_no"),
        (try_begin), #cf operation to see if it's near water
          (map_get_water_position_around_position, pos2, pos1, 5),
          # after finding water limit range of spawning (so sea raiders don't appear upriver)
          (store_add, ":limit", "p_sea_raider_spawn_point_1", num_sea_raider_spawn_points),
          (try_for_range, ":spawn_point", "p_sea_raider_spawn_point_1", ":limit"),
            (store_distance_to_party_from_party, ":distance", ":village_no", ":spawn_point"),
            (lt, ":distance", 50), # 200% bandit spawning radius
            (assign, ":limit", -1),
          (try_end),
          (eq, ":limit", -1), #within boundaries
          (assign, ":bandit_troop", "trp_sea_raider"),
        (else_try), #sample random points until we find forest/mountain (coast)
          (assign, ":forest_count", 0),
          (assign, ":mountain_count", 0),
          (assign, ":other_count", 0),
          (try_for_range, ":unused", 0, 100),
            (map_get_land_position_around_position, pos2, pos1, 5),
            (party_set_position, "p_temp_party", pos2),
            (party_get_current_terrain, ":terrain_type", "p_temp_party"),
            (try_begin),
              (eq, ":terrain_type", rt_forest),
              (val_add, ":forest_count", 1),
            (else_try),
              (eq, ":terrain_type", rt_mountain),
              (val_add, ":mountain_count", 1),
            (else_try),
              (val_add, ":other_count", 1),
            (try_end),
          (try_end),
          (try_begin), # not enough features
            (gt, ":other_count", 75), #pass through to faction calls
            (call_script, "script_center_get_bandits", ":village_no", 0),
            (assign, ":bandit_troop", reg0),
          (else_try),
            (gt, ":forest_count", ":mountain_count"),
            (gt, ":forest_count", 15),
            (assign, ":bandit_troop", "trp_forest_bandit"),
          (else_try),
            (gt, ":mountain_count", ":forest_count"),
            (gt, ":mountain_count", 15),
            (assign, ":bandit_troop", "trp_mountain_bandit"),
          (try_end),
        (try_end),
      (try_end),
    (try_end),
    (assign, reg0, ":bandit_troop"),
  ])
]
