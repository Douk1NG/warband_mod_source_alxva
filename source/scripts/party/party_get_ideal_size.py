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

party_get_ideal_size_scripts = [
("party_get_ideal_size",
    [
      (store_script_param_1, ":party_no"),

      #default limit is 30 for any party
      (assign, ":limit", 30),

      (try_begin),
        (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
        (party_stack_get_troop_id, ":party_leader", ":party_no", 0),
        (store_faction_of_party, ":faction_id", ":party_no"),

        #default limit is 10 for kingdom lords
        (assign, ":limit", 10),

        #each (leadership level) gives 5 to limit
        (store_skill_level, ":skill", "skl_leadership", ":party_leader"),
        (store_attribute_level, ":charisma", ":party_leader", ca_charisma),
        (val_mul, ":skill", 5),
        (val_add, ":limit", ":skill"),

        #each (charisma level) gives 1 to limit
        (val_add, ":limit", ":charisma"),

        #each (25 renown) gives 1 to limit
        (troop_get_slot, ":troop_renown", ":party_leader", slot_troop_renown),
        (store_div, ":renown_bonus", ":troop_renown", 25),
        (val_add, ":limit", ":renown_bonus"),

        ##diplomacy begin
        (assign, ":percent", 100),
        ##diplomacy end

		##diplomacy start+
		#Limit effects of policies for nascent kingdoms.
		(assign, ":policy_min", -3),
		(assign, ":policy_max", 4),#one greater than the maximum

		(try_begin),
			(this_or_next|eq, ":faction_id", "fac_player_supporters_faction"),
				(faction_slot_eq, ":faction_id", slot_faction_leader, "trp_player"),
			(faction_get_slot, ":policy_max", ":faction_id", slot_faction_num_towns),
			(faction_get_slot, reg0, ":faction_id", slot_faction_num_castles),
			(val_add, ":policy_max", reg0),
			(val_clamp, ":policy_max", 0, 4),#0, 1, 2, 3
			(store_mul, ":policy_min", ":policy_max", -1),
			(val_add, ":policy_max", 1),#one greater than the maximum
		(try_end),
		##diplomacy end+

        (try_begin),
          (faction_slot_eq, ":faction_id", slot_faction_leader, ":party_leader"),
          (val_add, ":limit", dplmc_monarch_party_bonus),
          ##diplomacy begin
          (try_begin),
            (faction_get_slot, ":centralization", ":faction_id", dplmc_slot_faction_centralization),
            (neq, ":centralization", 0),
			##diplomacy start+ Apply constraint
			(val_clamp, ":centralization", ":policy_min", ":policy_max"),
			##diplomacy end+
            (val_mul, ":centralization", 10),
            (val_add, ":percent", ":centralization"),
          (try_end),

        (else_try),
          (try_begin),
            (faction_get_slot, ":centralization", ":faction_id", dplmc_slot_faction_centralization),
            (neq, ":centralization", 0),
			##diplomacy start+ Apply constraint
			(val_clamp, ":centralization", ":policy_min", ":policy_max"),
			##diplomacy end+
            (val_mul, ":centralization", -3),
            (val_add, ":percent", ":centralization"),
          (try_end),
          (try_begin),
            (faction_get_slot, ":aristocraty", ":faction_id", dplmc_slot_faction_aristocracy),
            (neq, ":aristocraty", 0),
			##diplomacy start+ Apply constraint
			(val_clamp, ":aristocraty", ":policy_min", ":policy_max"),
			##diplomacy end+
            (val_mul, ":aristocraty", 3),
            (val_add, ":percent", ":aristocraty"),
          (try_end),
          (try_begin),
            (faction_get_slot, ":quality", ":faction_id", dplmc_slot_faction_quality),
            (neq, ":quality", 0),
			##diplomacy start+ Apply constraint
			(val_clamp, ":quality", ":policy_min", ":policy_max"),
			##diplomacy end+
            (val_mul, ":quality", -4),
            (val_add, ":percent", ":quality"),
          (try_end),
          ##diplomacy end
        (try_end),

        ##diplomacy begin
        (try_begin),
          (faction_get_slot, ":serfdom", ":faction_id", dplmc_slot_faction_serfdom),
          (neq, ":serfdom", 0),
		  ##diplomacy start+ Apply constraint
		  (val_clamp, ":serfdom", ":policy_min", ":policy_max"),
		  ##diplomacy end+
          (val_mul, ":serfdom", 2), #SB : description says 1, this used to be 3
          (val_add, ":percent", ":serfdom"),
        (try_end),

        (val_mul, ":limit", ":percent"),
        ##nested diplomacy start+ Round correctly
        (val_add, ":limit", 50),
        ##nested diplomacy end+
        (val_div, ":limit", 100),
        ##diplomacy end

        (try_begin),
          (faction_slot_eq, ":faction_id", slot_faction_marshall, ":party_leader"),
          (val_add, ":limit", dplmc_marshal_party_bonus),
        (try_end),

        #party takes additional 20 limit per each castle its party leader owns
        (try_for_range, ":cur_center", castles_begin, castles_end),
          (party_slot_eq, ":cur_center", slot_town_lord, ":party_leader"),
          (val_add, ":limit", dplmc_castle_party_bonus),
        (try_end),
      ##diplomacy start+
      ##Extend this script so it will also work with garrisons
      (else_try),
         (party_slot_eq, ":party_no", slot_party_type, spt_town),
         (assign, ":limit", 380),#average starting town garrison size
      (else_try),
         (this_or_next|is_between, ":party_no", walled_centers_begin, walled_centers_end),
         (party_slot_eq, ":party_no", slot_party_type, spt_castle),
         (assign, ":limit", 142),#average starting castle garrison size
         #(store_faction_of_party, ":faction_id", ":party_no"),
      ##diplomacy end+
      (try_end),

      #if player has level of 0 then ideal limit will be exactly same, if player has level of 80 then ideal limit will be multiplied by 2 ((80 + 80) / 80)
      #below code will increase limits a little as the game progresses and player gains level
      (store_character_level, ":level", "trp_player"),
      (val_min, ":level", 80),
      (store_add, ":level_factor", 80, ":level"),
      (val_mul, ":limit", ":level_factor"),
      (val_div, ":limit", 80),
      (assign, reg0, ":limit"),
  ])
]
