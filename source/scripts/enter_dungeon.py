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

enter_dungeon_scripts = [
# script_change_player_relation_with_faction
# Input: arg1 = center_no, arg2 = mission_template_no
# Output: none
("enter_dungeon",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":mission_template_no"),

      (set_jump_mission,":mission_template_no"),
      #new added...
      (mission_tpl_entry_set_override_flags, ":mission_template_no", 0, af_override_horse),
      (try_begin),
        (gt, "$sneaked_into_town", disguise_none),
        (mission_tpl_entry_set_override_flags, ":mission_template_no", 0, af_override_everything), #boots + gloves
        # (mission_tpl_entry_clear_override_items, ":mission_template_no", 0),
        #SB : different disguises
        (call_script, "script_set_disguise_override_items", ":mission_template_no", 0, 0), #no weapons
        # (mission_tpl_entry_add_override_item, ":mission_template_no", 0, "itm_pilgrim_hood"),
        # (mission_tpl_entry_add_override_item, ":mission_template_no", 0, "itm_wrapping_boots"), #SB add boots
        # (mission_tpl_entry_add_override_item, ":mission_template_no", 0, "itm_pilgrim_disguise"),
        # (mission_tpl_entry_add_override_item, ":mission_template_no", 0, "itm_practice_staff"),
        # (mission_tpl_entry_add_override_item, ":mission_template_no", 0, "itm_throwing_daggers"),
      (try_end),
      #new added end

      (party_get_slot, ":dungeon_scene", ":center_no", slot_town_prison),

      (modify_visitors_at_site,":dungeon_scene"),
      (reset_visitors),
      (assign, ":cur_pos", 16),


      (call_script, "script_get_heroes_attached_to_center_as_prisoner", ":center_no", "p_temp_party"),
      (party_get_num_companion_stacks, ":num_stacks","p_temp_party"),
      ##diplomacy start+ Allow some variation in which prisoners appear,
      #when there are too many to all fit in the jail at once.
      (try_begin),
         	(gt, ":num_stacks", 15),
            (store_random_in_range, ":offset", 0, ":num_stacks"),
      (else_try),
           	(assign, ":offset", 0),
      (try_end),
      ##diplomacy end+
      (try_for_range, ":i_stack", 0, ":num_stacks"),
      ##diplomacy start+
        (val_add, ":i_stack", ":offset"),
        (try_begin),
           (ge, ":i_stack", ":num_stacks"),
           (val_sub, ":i_stack", ":num_stacks"),
        (try_end),
      ##diplomacy end+
        (party_stack_get_troop_id, ":stack_troop","p_temp_party",":i_stack"),

		(assign, ":prisoner_offered_parole", 0),
		(try_begin),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
		(else_try),
			(call_script, "script_cf_prisoner_offered_parole", ":stack_troop"),
			(assign, ":prisoner_offered_parole", 1),
		(else_try),
			(assign, ":prisoner_offered_parole", 0),
		(try_end),
		(eq, ":prisoner_offered_parole", 0),

        (lt, ":cur_pos", 32), # spawn up to entry point 32
        (set_visitor, ":cur_pos", ":stack_troop"),
        (val_add,":cur_pos", 1),
      (try_end),

#	  (set_visitor, ":cur_pos", "trp_npc3"),
#	  (troop_set_slot, "trp_npc3", slot_troop_prisoner_of_party, "$g_encountered_party"),

      (set_jump_entry, 0),
      (jump_to_scene,":dungeon_scene"),
      (scene_set_slot, ":dungeon_scene", slot_scene_visited, 1),
      (change_screen_mission),
  ])
]
