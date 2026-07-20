# ======================================================================
# SHARED DEPENDENCY
# Entity: setup_camp_scene (script)
# Called by menus in 2 domains: camp, siege
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

setup_camp_scene_scripts = [
("setup_camp_scene",
    [
      (party_get_current_terrain, ":terrain_type", "p_main_party"),
      (assign, ":scene_to_use", "scn_camp_scene_plain"),
      (try_begin),
        (this_or_next|eq, ":terrain_type", rt_steppe),
        (eq, ":terrain_type", rt_steppe_forest),
        (assign, ":scene_to_use", "scn_camp_scene_steppe"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_plain),
        (eq, ":terrain_type", rt_forest),
        (assign, ":scene_to_use", "scn_camp_scene_plain"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_snow),
        (eq, ":terrain_type", rt_snow_forest),
        (assign, ":scene_to_use", "scn_camp_scene_snow"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_desert),
        (eq, ":terrain_type", rt_desert_forest),
        (assign, ":scene_to_use", "scn_camp_scene_desert"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_river),
        (eq, ":terrain_type", rt_water), #figure this out later
        (assign, ":scene_to_use", "scn_sea_1"),

        (party_get_slot, ":ship_type", "p_main_party", slot_party_ship_type),
        (try_begin),
          (eq, ":ship_type", 1),
          (assign, ":scene_to_use", "scn_sea_1"),
        (else_try),
          (eq, ":ship_type", 2),
          (assign, ":scene_to_use", "scn_sea_2"),
        (else_try),
          (eq, ":ship_type", 3),
          (assign, ":scene_to_use", "scn_sea_3"),
        (else_try),
          (eq, ":ship_type", 4),
          (assign, ":scene_to_use", "scn_sea_4"),
        (try_end),

       (try_for_range, ":entry_no", 33, 40),
         (mission_tpl_entry_set_override_flags, "mt_camp", ":entry_no", af_override_horse),
       (try_end),

      (else_try),
        (eq, ":terrain_type", rt_bridge),
		(try_for_parties, ":party_no"),
			(is_between, ":party_no", "p_bridge_1", "p_looter_spawn_point"),
			(store_distance_to_party_from_party, ":distance", ":party_no", "p_main_party"),
			(lt, ":distance", 2),
			(party_get_icon, ":icon", ":party_no"),
			(try_begin),
				(eq, ":icon", "icon_bridge_snow_a"),
				(assign, ":scene_to_use", "scn_camp_scene_snow"),
			(else_try),
				(assign, ":scene_to_use", "scn_camp_scene_plain"),
			(try_end),
		(try_end),
      (try_end),
	  (modify_visitors_at_site, ":scene_to_use"),
	  (reset_visitors),
	# (set_visitor,1,"trp_follower_woman"),

	(assign, ":cur_entry", 2),

    (assign, ":entry_1_assigned", 0),

    (troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),

   (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
   (try_for_range, ":troop_iterator", 0, ":num_stacks"), #1st pass: grab all heroes
	 (party_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":troop_iterator"),
	 (troop_is_hero, ":cur_troop_id"),
	 (neq, ":cur_troop_id", "trp_player"),
	 (try_begin),
		(ge, ":cur_entry", 40),
		(assign, ":num_stacks", -1), #break the loop
	 (else_try),
         (eq, ":cur_troop_id", ":spouse"),
		 (set_visitor, 1, ":cur_troop_id"), #is spouse
         (assign, ":entry_1_assigned", 1),
	 (else_try),
		 (set_visitor, ":cur_entry", ":cur_troop_id"),
		 (val_add, ":cur_entry", 1),
	 (try_end),
   (try_end),

   #2nd pass: get anyone else
   (try_for_range, ":troop_iterator", 0, ":num_stacks"),
	 (party_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":troop_iterator"),
	 (neq, ":cur_troop_id", "trp_player"),
	 (neg|troop_is_hero, ":cur_troop_id"),
	 (try_begin),
		(ge, ":cur_entry", 40),
		(assign, ":num_stacks", -1), #break the loop
	 (else_try),
		 (party_stack_get_size, ":stack_size","p_main_party",":troop_iterator"),
		 (party_stack_get_num_wounded, ":num_wounded","p_main_party",":troop_iterator"),
		 (val_sub, ":stack_size", ":num_wounded"),
		 (gt, ":stack_size", 0),
		 (try_for_range, ":stack_iterator", 0, ":stack_size"), #nested loop ayy lmao
			 (try_begin),
				(ge, ":cur_entry", 40),
				(assign, ":stack_size", -1), #break the loop
             (else_try),
                 (neq, ":entry_1_assigned", 1),
                 (this_or_next|eq, ":cur_troop_id", "trp_prostitute"),
                 (eq, ":cur_troop_id", "trp_courtesan"),
                 (set_visitor, 1, ":cur_troop_id"),
                 (assign, ":entry_1_assigned", 1),
			 (else_try),
				 (store_random_in_range,":troop_dna",0,1000),
				 (set_visitor, ":cur_entry", ":cur_troop_id", ":troop_dna"),
                 (troop_set_slot, "trp_temp_array_c", ":cur_entry", ":troop_dna"),
				 (val_add, ":cur_entry", 1),
			 (try_end),
		 (try_end),
	  (try_end),
   (try_end),

	#prisoners
	(assign, ":cur_entry", 40),
	(party_get_num_prisoner_stacks, ":prisoner_stacks","p_main_party"),
    (try_for_range, ":troop_iterator", 0, ":prisoner_stacks"), #1st pass: grab all heroes
	 (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":troop_iterator"),
	 (troop_is_hero, ":cur_troop_id"),
	 (neq, ":cur_troop_id", "trp_player"),
	 (try_begin),
		(ge, ":cur_entry", 48),
		(assign, ":troop_iterator", ":prisoner_stacks"), #break the loop
	 (else_try),
		 (set_visitor, ":cur_entry", ":cur_troop_id"),
		 (store_add, ":cur_entry", ":cur_entry", 1),
	 (try_end),
   (try_end),

   #2nd pass: get anyone else
   (party_get_num_prisoner_stacks, ":prisoner_stacks","p_main_party"),
   (try_for_range, ":troop_iterator", 0, ":prisoner_stacks"),
	 (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":troop_iterator"),
	 (neg|troop_is_hero, ":cur_troop_id"),
	 (try_begin),
		(ge, ":cur_entry", 48),
		(assign, ":troop_iterator", ":num_stacks"), #break the loop
	 (else_try),
		 (party_prisoner_stack_get_size, ":stack_size","p_main_party",":troop_iterator"),
		 (gt, ":stack_size", 0),
		 (try_for_range, ":stack_iterator", 0, ":stack_size"), #nested loop ayy lmao
			 (try_begin),
				(ge, ":cur_entry", 48),
				(assign, ":stack_size", -1), #break the loop
			 (else_try),
				 (store_random_in_range,":troop_dna",0,1000),
				 (set_visitor, ":cur_entry", ":cur_troop_id", ":troop_dna"),
                 (troop_set_slot, "trp_temp_array_c", ":cur_entry", ":troop_dna"),
				 (val_add, ":cur_entry", 1),
			 (try_end),
		 (try_end),
	  (try_end),
   (try_end),

	(mission_tpl_entry_clear_override_items,"mt_camp",1),
	(store_random_in_range,":r",0,2),
	(try_begin),
		(eq,":r",0),
		(mission_tpl_entry_add_override_item,"mt_camp",1,"itm_lute"),
	(else_try),
		(mission_tpl_entry_add_override_item,"mt_camp",1,"itm_lyre"),
	(try_end),

	  (assign, "$talk_context", tc_camp_talk),
      (jump_to_scene,":scene_to_use"),
  ])
]
