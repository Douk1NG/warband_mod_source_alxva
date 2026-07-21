# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

camp_recruit_prisoners_menu = [
("camp_recruit_prisoners",0,
   "You offer your prisoners freedom if they agree to join you as soldiers. {s18}",
   "none",
   [(assign, ":num_regular_prisoner_slots", 0),
    (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
    (try_for_range, ":cur_stack", 0, ":num_stacks"),
      (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":cur_stack"),
      # (neg|troop_is_hero, ":cur_troop_id"),
      #SB : use script check
      (call_script, "script_game_check_prisoner_can_be_sold", ":cur_troop_id"),
      (eq, reg0, 1),
      (val_add, ":num_regular_prisoner_slots", 1),
    (try_end),
    (try_begin),
      (eq, ":num_regular_prisoner_slots", 0),
      (jump_to_menu, "mnu_camp_no_prisoners"),
    (else_try),
      (eq, "$g_prisoner_recruit_troop_id", 0),
      (store_current_hours, "$g_prisoner_recruit_last_time"),
      (store_random_in_range, ":rand", 0, 100),
      (store_skill_level, ":persuasion_level", "skl_persuasion", "trp_player"),
      (store_sub, ":reject_chance", 15, ":persuasion_level"),
      (val_mul, ":reject_chance", 4),
      (try_begin),
        (lt, ":rand", ":reject_chance"),
        (assign, "$g_prisoner_recruit_troop_id", -7),
      (else_try),
        # (assign, ":num_regular_prisoner_slots", 0),
        # (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
        # (try_for_range, ":cur_stack", 0, ":num_stacks"),
          # (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":cur_stack"),
          # (neg|troop_is_hero, ":cur_troop_id"),
          # (val_add, ":num_regular_prisoner_slots", 1),
        # (try_end),
        (store_random_in_range, ":random_prisoner_slot", 0, ":num_regular_prisoner_slots"),
        (try_for_range, ":cur_stack", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":cur_stack"),
          (call_script, "script_game_check_prisoner_can_be_sold", ":cur_troop_id"),
          (eq, reg0, 1), #SB : use script call to prevent quest troops from being recruited
          (val_sub, ":random_prisoner_slot", 1),
          (lt, ":random_prisoner_slot", 0),
          (assign, ":num_stacks", 0),
          (assign, "$g_prisoner_recruit_troop_id", ":cur_troop_id"),
          (party_prisoner_stack_get_size, "$g_prisoner_recruit_size", "p_main_party", ":cur_stack"),
        (try_end),
      (try_end),

      (try_begin),
        (gt, "$g_prisoner_recruit_troop_id", 0),
        (party_get_free_companions_capacity, ":capacity", "p_main_party"),
        (val_min, "$g_prisoner_recruit_size", ":capacity"),
        (assign, reg1, "$g_prisoner_recruit_size"),
        (gt, "$g_prisoner_recruit_size", 0),
        (try_begin),
          (gt, "$g_prisoner_recruit_size", 1),
          (assign, reg2, 1),
        (else_try),
          (assign, reg2, 0),
        (try_end),
        (str_store_troop_name_by_count, s1, "$g_prisoner_recruit_troop_id", "$g_prisoner_recruit_size"),
        (str_store_string, s18, "@{reg1} {s1} {reg2?accept:accepts} the offer."),
      (else_try),
        (str_store_string, s18, "@No one accepts the offer."),
      (try_end),
    (try_end),
    ],
    [
      ("camp_recruit_prisoners_accept",[(gt, "$g_prisoner_recruit_troop_id", 0)],"Take them.",
       [(remove_troops_from_prisoners, "$g_prisoner_recruit_troop_id", "$g_prisoner_recruit_size"),
        (party_add_members, "p_main_party", "$g_prisoner_recruit_troop_id", "$g_prisoner_recruit_size"),
        #SB : change base morale reduction by difficulty
        (game_get_reduce_campaign_ai, ":reduce"), #0 to 2
        (val_sub, ":reduce", 4), #-4 to -2
        (store_mul, ":morale_change", ":reduce", "$g_prisoner_recruit_size"),
        (store_troop_faction, ":troop_faction", "$g_prisoner_recruit_troop_id"),
        (store_character_level, ":troop_level", "$g_prisoner_recruit_troop_id"),

        (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
          (faction_set_slot, ":faction", slot_faction_temp_slot, 0),
        (try_end),
        (try_begin), #give extra penalty to faction morale if we recruit high-level enemy troops
          (this_or_next|eq, ":troop_faction", "fac_outlaws"),
          (eq, ":troop_faction", "fac_deserters"),
          (call_script, "script_objectionable_action", tmt_aristocratic, "str_hire_deserters"),
        (else_try),
          (is_between, ":troop_faction", npc_kingdoms_begin, npc_kingdoms_end),
          # (store_character_level, ":relation", "$g_prisoner_recruit_troop_id"),
          (try_begin), #check culture
            (eq, "$players_kingdom", "fac_player_supporters_faction"),
            (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
            (eq, "$g_player_culture", ":troop_faction"),
            (assign, ":troop_faction", "$players_kingdom"),
          (try_end),
          (try_begin), #no penalty for same faction
            (eq, ":troop_faction", "$players_kingdom"),
            # (val_sub, ":relation", ":morale_change"), #bonus
            (assign, ":morale_change", 0),
            (assign, "$g_prisoner_recruit_troop_id", 0),
            (assign, "$g_prisoner_recruit_size", 0),
          (else_try), #one point per offended party
            (party_get_num_companion_stacks, ":cap", "p_main_party"),
            (try_for_range, ":stack", 1, ":cap"),
              (party_stack_get_troop_id, ":troop", "p_main_party", ":stack"),
              # (neg|troop_is_hero, ":troop"),
              # (neq, ":troop", "$g_prisoner_recruit_troop_id"), #not just recruited
              (store_faction_of_troop, ":stack_faction", ":troop"),
              # (neq, ":stack_faction", ":troop_faction"),
              (store_relation, ":faction_relation", ":troop_faction", ":stack_faction"),
              (lt, ":faction_relation", 0),
              (faction_get_slot, ":amount", ":stack_faction", slot_faction_temp_slot),
              (party_stack_get_size, ":reduce", "p_main_party", ":stack"),
              (val_sub, ":amount", ":reduce"),
              (faction_set_slot, ":stack_faction", slot_faction_temp_slot, ":amount"),
            (try_end),
          (try_end),
        (try_end),
        (call_script, "script_change_player_party_morale", ":morale_change"),
        (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
          (faction_get_slot, ":relation", ":faction", slot_faction_temp_slot),
          (neq, ":relation", 0),
          (val_sub, ":relation", ":troop_level"),
          (call_script, "script_change_faction_troop_morale", ":faction", ":relation", 1),
        (try_end),
        (jump_to_menu, "mnu_camp"),
        ]
       ),
      ("camp_recruit_prisoners_reject",[(gt, "$g_prisoner_recruit_troop_id", 0)],"Reject them.",
       [(jump_to_menu, "mnu_camp"),
        (assign, "$g_prisoner_recruit_troop_id", 0),
        (assign, "$g_prisoner_recruit_size", 0),
        ]
       ),
      ("continue",[(le, "$g_prisoner_recruit_troop_id", 0)],"Go back.",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  )
]
