# ======================================================================
# SHARED DEPENDENCY
# Entity: cf_reinforce_party (script)
# Called by menus in 2 domains: castle, cheats
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

cf_reinforce_party_scripts = [
("cf_reinforce_party",
    [
      (store_script_param_1, ":party_no"),

      (store_faction_of_party, ":party_faction", ":party_no"),
	  ##diplomacy start+ The party faction may be changed for culture, but we still need the original
	  (assign, ":real_party_faction", ":party_faction"),
	  ##diplomacy end+
      (party_get_slot, ":party_type",":party_no", slot_party_type),

#Rebellion changes begin:
      (try_begin),
        (eq, ":party_type", spt_kingdom_hero_party),
        (party_stack_get_troop_id, ":leader", ":party_no"),
        (troop_get_slot, ":party_faction",  ":leader", slot_troop_original_faction),
		##diplomacy start+ Use player culture for companions and spouse (and any hypothetical non-hero mercenaries)
		(eq, ":real_party_faction", "fac_player_supporters_faction"),
		(is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
		(this_or_next|is_between, ":leader", companions_begin, companions_end),
		(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":leader"),
		   (neg|is_between, ":leader", heroes_begin, heroes_end),
		(assign, ":party_faction", "$g_player_culture"),
		##diplomacy end+
      (try_end),
#Rebellion changes end

      (try_begin),
      #SB : this block checks for town lords, which is invalid for kingdom parties
        (is_between, ":party_type", spt_castle, spt_village),
        (eq, ":party_faction", "fac_player_supporters_faction"),
        (party_get_slot, ":town_lord", ":party_no", slot_town_lord),
        (try_begin),
        ##diplomacy begin
          (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
          (assign, ":party_faction", "$g_player_culture"),

          # (try_begin), #debug
            # (eq, "$cheat_mode", 1),
            # (str_store_party_name, s11, ":party_no"),
            # (display_message, "@pt in {s11}"),
          # (try_end),

        (else_try),
        ##diplomacy end
          (gt, ":town_lord", 0),
          (troop_get_slot, ":party_faction", ":town_lord", slot_troop_original_faction),
          (gt, ":party_faction", 0), ## CC
        (else_try),
          (party_get_slot, ":party_faction", ":party_no", slot_center_original_faction),
        (try_end),
      (try_end),
	  ##diplomacy start+ Player culture cleanup (do this once here, instead of separately for each type)
	  (try_begin),
	     (gt, ":real_party_faction", "fac_commoners"),
	     (this_or_next|eq, ":real_party_faction", "fac_player_faction"),
	     (this_or_next|eq, ":real_party_faction", "fac_player_supporters_faction"),
		 (eq, ":real_party_faction", "$players_kingdom"),
		 (neg|is_between, ":party_faction", npc_kingdoms_begin, npc_kingdoms_end),
		 (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
		 (assign, ":party_faction", "$g_player_culture"),
	  (try_end),
	  ##diplomacy end+

      (faction_get_slot, ":party_template_a", ":party_faction", slot_faction_reinforcements_a),
      (faction_get_slot, ":party_template_b", ":party_faction", slot_faction_reinforcements_b),
      (faction_get_slot, ":party_template_c", ":party_faction", slot_faction_reinforcements_c),

      (assign, ":party_template", 0),
      (store_random_in_range, ":rand", 0, 100),
  	  ##diplomacy start+
	  #Implement "quality vs. quantity" in a way that is visible in player battles
	  #(previously, quantity increased party size, but quality only had an effect
	  #in autocalc battles)
	  (try_begin),
		(is_between, ":real_party_faction", kingdoms_begin, kingdoms_end),
		(faction_get_slot, ":dplmc_quality", ":real_party_faction", dplmc_slot_faction_quality),
		(val_clamp, ":dplmc_quality", -3, 4),
		(val_add, ":rand", ":dplmc_quality"),
		(val_clamp, ":rand", 0, 101),
	  (try_end),
	  ##diplomacy end+
      (try_begin),
        (this_or_next|eq, ":party_type", spt_town),
        (eq, ":party_type", spt_castle),  #CASTLE OR TOWN
        (try_begin),
          (lt, ":rand", 65),
          (assign, ":party_template", ":party_template_a"),
        (else_try),
          (assign, ":party_template", ":party_template_b"),
        (try_end),
      (else_try),
        (eq, ":party_type", spt_kingdom_hero_party),
        (try_begin),
          (lt, ":rand", 50),
          (assign, ":party_template", ":party_template_a"),
        (else_try),
          (lt, ":rand", 75),
          (assign, ":party_template", ":party_template_b"),
        (else_try),
          (assign, ":party_template", ":party_template_c"),
        (try_end),
      (else_try),
	  ##diplomacy start+ Reinforcements for patrols
	    (this_or_next|eq, ":party_type", spt_patrol),
	    (eq, ":party_type", spt_reinforcement), #SB : add more reinf if necessary
		(try_begin),
		   (lt, ":rand", 65),
		   (assign, ":party_template", ":party_template_a"),
		(else_try),
		   (assign, ":party_template", ":party_template_b"),
		(try_end),
	  ##diplomacy end+
      (try_end),

      (try_begin),
        (gt, ":party_template", 0),
        (party_add_template, ":party_no", ":party_template"),
      (try_end),
  ])
]
