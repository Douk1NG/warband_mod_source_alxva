# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

misc_menus = [
  ("cattle_herd",mnf_scale_picture,
   "You encounter a herd of cattle.",
   "none",
   [(play_sound, "snd_cow_moo"),
    (set_background_mesh, "mesh_pic_cattle"),
   ],
    [
      ("cattle_drive_away",[],"Drive the cattle onward.",
       [
        (party_set_slot, "$g_encountered_party", slot_cattle_driven_by_player, 1),
        (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_driven_by_party),
        (party_set_ai_object,"$g_encountered_party", "p_main_party"),
        (party_set_extra_text, "$g_encountered_party", "str_ai_bhvr_driven_by_party"),
        (change_screen_return),
        ]
       ),

       #SB : cattle tweaks
      ("cattle_drag_with",[
       # (call_script, "script_party_count_members_with_full_health", "p_main_party"),
       # (assign, ":size", reg0),
       # (party_stack_get_size, ":num_cattle", "$g_encountered_party", 0),
       # (gt, ":size", ":num_cattle"),
      ],"Drag the cattle with you.",
       [
        (party_set_slot, "$g_encountered_party", slot_cattle_driven_by_player, 1),
        (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_escort_party),
        (party_set_ai_object,"$g_encountered_party", "p_main_party"),
        (party_set_extra_text, "$g_encountered_party", "str_ai_bhvr_escort_party"),
        (change_screen_return),
        ]
       ),

      ("cattle_stop",[],"Bring the herd to a stop.",
       [
        (party_set_slot, "$g_encountered_party", slot_cattle_driven_by_player, 0),
        (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_hold),
        (party_set_extra_text, "$g_encountered_party", "@Grazing"),
        (change_screen_return),
        ]
       ),
      ("cattle_kill",[(assign, ":continue", 1),
                      (try_begin),
                        (check_quest_active, "qst_move_cattle_herd"),
                        (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, "$g_encountered_party"),
                        (assign, ":continue", 0),
                      (try_end),
                      (eq, ":continue", 1)],"Slaughter some of the animals.",
       [(jump_to_menu, "mnu_cattle_herd_kill"),
        ]
       ),
      ("leave",[],"Leave.",
       [(change_screen_return),
        ]
       ),
      ]
  ),
  ("cattle_herd_kill",0,
   "How many animals do you want to slaughter?",
   "none",
   [(party_get_num_companions, reg5, "$g_encountered_party")],
    [
      ("cattle_kill_1",[(ge, reg5, 1),],"One.",
       [(call_script, "script_kill_cattle_from_herd", "$g_encountered_party", 1),
        (jump_to_menu, "mnu_cattle_herd_kill_end"),
        (change_screen_loot, "trp_temp_troop"),
        (play_sound, "snd_cow_slaughter"),
        ]
       ),
      ("cattle_kill_2",[(ge, reg5, 2),],"Two.",
       [(call_script, "script_kill_cattle_from_herd", "$g_encountered_party", 2),
        (jump_to_menu, "mnu_cattle_herd_kill_end"),
        (change_screen_loot, "trp_temp_troop"),
        (play_sound, "snd_cow_slaughter"),
        ]
       ),
      ("cattle_kill_3",[(ge, reg5, 3),],"Three.",
       [(call_script, "script_kill_cattle_from_herd", "$g_encountered_party", 3),
        (jump_to_menu, "mnu_cattle_herd_kill_end"),
        (change_screen_loot, "trp_temp_troop"),
        (play_sound, "snd_cow_slaughter"),
        ]
       ),
      ("cattle_kill_4",[(ge, reg5, 4),],"Four.",
       [(call_script, "script_kill_cattle_from_herd", "$g_encountered_party", 4),
        (jump_to_menu, "mnu_cattle_herd_kill_end"),
        (change_screen_loot, "trp_temp_troop"),
        (play_sound, "snd_cow_slaughter"),
        ]
       ),
      ("cattle_kill_5",[(ge, reg5, 5),],"Five.",
       [(call_script, "script_kill_cattle_from_herd", "$g_encountered_party", 5),
        (jump_to_menu, "mnu_cattle_herd_kill_end"),
        (change_screen_loot, "trp_temp_troop"),
        (play_sound, "snd_cow_slaughter"),
        ]
       ),
      ("go_back_dot",[],"Go back.",
       [(jump_to_menu, "mnu_cattle_herd"),
        ]
       ),
      ]
  ),
  ("cattle_herd_kill_end",0,
   "{!}You shouldn't be reading this.",
   "none",
   [(change_screen_return)],
    [
      ]
  ),
  ("arena_duel_fight",0,
   "You and your opponent prepare to duel.",
   "none",
   [
      (troop_get_slot, ":leader_troop_faction", "$g_duel_troop", slot_troop_original_faction),
      (try_begin),
        (eq, ":leader_troop_faction", fac_kingdom_1),
        (set_background_mesh, "mesh_pic_swad"),
      (else_try),
        (eq, ":leader_troop_faction", fac_kingdom_2),
        (set_background_mesh, "mesh_pic_vaegir"),
      (else_try),
        (eq, ":leader_troop_faction", fac_kingdom_3),
        (set_background_mesh, "mesh_pic_khergit"),
      (else_try),
        (eq, ":leader_troop_faction", fac_kingdom_4),
        (set_background_mesh, "mesh_pic_nord"),
      (else_try),
        (eq, ":leader_troop_faction", fac_kingdom_5),
        (set_background_mesh, "mesh_pic_rhodock"),
      (else_try),
        (eq, ":leader_troop_faction", fac_kingdom_6),
        (set_background_mesh, "mesh_pic_sarranid_encounter"),
      (try_end),
   ],
   [
     ("continue",[],"Continue...",
      [
        (assign, "$g_leave_encounter", 0),
        (assign, ":closest_town", "$g_encountered_party"),

        #restructure this to take into account $g_start_arena_fight_at_nearest_town
        (try_begin), #check if the parameter is necessary
          (neg|is_between, ":closest_town", walled_centers_begin, walled_centers_end),
          (is_between, "$g_start_arena_fight_at_nearest_town", walled_centers_begin, walled_centers_end),
          (assign, ":closest_town", "$g_start_arena_fight_at_nearest_town"),
          (assign, "$g_start_arena_fight_at_nearest_town", 0),
        (try_end),

        (try_begin),
          (is_between, ":closest_town", towns_begin, towns_end),
          (party_get_slot, ":duel_scene", ":closest_town", slot_town_arena),
        (else_try), #SB : duels at castle arena
          (is_between, ":closest_town", castles_begin, castles_end),
          (party_get_slot, ":duel_scene", ":closest_town", slot_castle_exterior),
        (else_try),
          (party_get_current_terrain, ":terrain", "p_main_party"),
          (eq, ":terrain", rt_snow),
          (assign, ":duel_scene", "scn_training_ground_ranged_melee_3"),
        (else_try),
          (this_or_next|eq, ":terrain", rt_desert),
          (eq, ":terrain", rt_steppe), #this is the actual steppe scene
          (assign, ":duel_scene", "scn_training_ground_ranged_melee_4"),
        (else_try),
          (assign, ":duel_scene", "scn_training_ground_ranged_melee_1"),
        (try_end),
        (modify_visitors_at_site, ":duel_scene"),
        (reset_visitors),
        # (set_visitor, 0, "trp_player"),
        # (set_visitor, 1, "$g_duel_troop"),
        (troop_set_slot, "trp_tournament_participants", 0, "trp_player"),
        (troop_set_slot, "trp_tournament_participants", 1, "$g_duel_troop"),
        (set_jump_mission, "mt_duel_with_lord"),
        #SB : check relative standing, 0 = (higher renown)
        (try_begin),
          (troop_is_hero, "$g_duel_troop"),
          (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
          (troop_slot_ge, "$g_duel_troop", slot_troop_renown, ":player_renown"),
          #swap positions
          (troop_set_slot, "trp_tournament_participants", 1, "trp_player"),
          (troop_set_slot, "trp_tournament_participants", 0, "$g_duel_troop"),
        (try_end),
        #SB : set up additional equipment, do not always use sword_medieval_a
        (troop_get_slot, ":faction", "$g_duel_troop", slot_troop_original_faction),
        (try_begin),
          (this_or_next|eq, ":faction", "fac_kingdom_1"),
          (eq, ":faction", "fac_kingdom_5"),
          (store_random_in_range, ":weapon", "itm_sword_medieval_a", "itm_sword_viking_1"),
        (else_try),
          (eq, ":faction", "fac_kingdom_3"),
          (assign, ":weapon", "itm_sword_khergit_1"),
        (else_try),
          (this_or_next|eq, ":faction", "fac_kingdom_2"),
          (eq, ":faction", "fac_kingdom_4"),
          (store_random_in_range, ":weapon", "itm_sword_viking_1", "itm_sword_viking_3_small"),
        # (else_try),
          # (eq, ":faction", "fac_kingdom_5"), #no requirement
          # (assign, ":weapon", "itm_military_cleaver_b"),
        (else_try),
          (eq, ":faction", "fac_kingdom_6"),
          (assign, ":weapon", "itm_scimitar"),
        (else_try),
          (assign, ":weapon", "itm_arena_sword"),
        (try_end),

        (try_for_range, ":cur_entry_point", 0, 2),
          (troop_get_slot, ":cur_troop", "trp_tournament_participants", ":cur_entry_point"),
          (try_begin), #within the courtyard, 23/24 is guard entry
            (is_between, ":closest_town", castles_begin, castles_end),
            (val_add, ":cur_entry_point", 2), #to use the new mission template entries 3 & 4
          (try_end),

          (mission_tpl_entry_clear_override_items, "mt_duel_with_lord", ":cur_entry_point"),
          #weapon, make sure they have no difficulty requirement
          (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", ":weapon"),
          # (item_get_type, ":type", ":weapon"),
          # (try_begin),
            # (is_between, ":type", itp_type_pistol, itp_type_bullets),
            # (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", "itm_cartridges2"),
            # (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", "itm_dagger"),#backup
          # (else_try),
            # (eq, ":type", itp_type_crossbow),
            # (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", "itm_practice_bolts_9_amount"),
            # (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", "itm_estoc"),#backup
          # (else_try),
            # (eq, ":type", itp_type_bow),
            # (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", "itm_practice_arrows_10_amount"),
            # (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", ":backup"),#backup
          # (try_end),

          #armor, they're statistically almost the same
          # (troop_get_slot, ":renown", ":cur_troop", slot_troop_renown),
          # (val_min, ":renown", 2000),
          # (store_div, ":armor", ":renown", 500),#0 to 3
          # (val_add, ":armor", "itm_heraldic_mail_with_surcoat"),
          # (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", ":armor"),

          (set_visitor, ":cur_entry_point", ":cur_troop"),
        (try_end),

        (jump_to_scene, ":duel_scene"),
        (jump_to_menu, "mnu_arena_duel_conclusion"),
        (change_screen_mission),
      ]),
    ]
  ),
  ("arena_duel_conclusion",0,
   "{!}{s11}",
   "none",
   [

    (try_begin),
		(eq, "$g_leave_encounter", 1),
		(change_screen_return),
	(try_end),

    (str_store_troop_name, s10, "$g_duel_troop"),
    #SB : change to loop
    (store_add, ":end", lady_quests_end, 2),
    (try_for_range, ":quest", "qst_duel_for_lady", ":end"),
      (try_begin),
        (eq, ":quest", lady_quests_end),
        (assign, ":quest", "qst_denounce_lord"),
      (try_end),
      (quest_slot_eq, ":quest", slot_quest_target_troop, "$g_duel_troop"),
      (try_begin),
        (check_quest_succeeded, ":quest"),
        (str_store_string, s11, "str_s10_lies_in_the_arenas_dust_for_several_minutes_then_staggers_to_his_feet_you_have_won_the_duel"),
        #(set_background_mesh, "mesh_pic_victory"),
      (else_try),
        (check_quest_failed, ":quest"),
        (str_store_string, s11, "str_you_lie_stunned_for_several_minutes_then_stagger_to_your_feet_to_find_your_s10_standing_over_you_you_have_lost_the_duel"),
        #(set_background_mesh, "mesh_pic_defeat"),
      (try_end),
    (try_end),
   ],
   [
     ("continue",[],"Continue...",
      [
        (assign, "$talk_context", tc_after_duel),
        (try_begin), #SB : use the appropriate script calls
          (is_between, "$g_encountered_party", centers_begin, centers_end),
          (call_script, "script_start_court_conversation", "$g_duel_troop", "$g_encountered_party"), #SB : script call
        (else_try),
          (call_script, "script_setup_troop_meeting", "$g_duel_troop", -1), #SB : script call
        (try_end),
        ]),
      ]
  ),
  ("lost_tavern_duel",mnf_disable_all_keys,
    "{s11}{s12}",
    "none",
    [
    (str_clear, s11),
    (str_clear, s12),
    #use s11 as primary indicator string
	(try_begin),
		(agent_get_troop_id, ":type", "$g_main_attacker_agent"),
		(eq, ":type", "trp_belligerent_drunk"),
		(try_begin),
			(eq, "$g_sexual_content", 2),
			(this_or_next|eq, "$character_gender", 1),(eq, "$g_nohomo", 0),
			(agent_get_entry_no, ":entry_no", "$g_main_attacker_agent"),
			(troop_get_slot, ":dna", "trp_temp_array_c", ":entry_no"), #I really don't know why this won't work.
			(troop_set_slot, "trp_temp_array_a", 0, "trp_player"),
			(troop_set_slot, "trp_temp_array_b", 0, -1),
			(troop_set_slot, "trp_temp_array_a", 1, ":type"),
			(troop_set_slot, "trp_temp_array_b", 1, ":dna"),
			(assign, "$g_sex_position", 1),
			(assign, "$f_encountertype", 1),
			(assign, "$f_cons1", -1), #Non-con
			(assign, "$f_cons2", 0), #Con
			(str_store_string, s11, "@You slump to the floor, stunned by the drunk's last blow. Your attacker's rage seems unending. He flails about and flips a table as the other tavern-goers beat a hasty retreat. Suddenly, he grabs you by the leg and drags you up to the rooms..."),
		(else_try),
			(str_store_string, s11, "str_lost_tavern_duel_ordinary"),
		(try_end),
	(else_try),
		(agent_get_troop_id, ":type", "$g_main_attacker_agent"),
		(eq, ":type", "trp_hired_assassin"),
		(str_store_string, s11, "str_lost_tavern_duel_assassin"),
	(try_end),
	(troop_set_slot, "trp_hired_assassin", slot_troop_cur_center, -1),
	(troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, -1), #remove him for now

    #use s12 for additional info like lost purse, etc
    #SB : penalty for fighting while disguised
    (try_begin),
      (gt, "$sneaked_into_town", disguise_none),
      (store_random_in_range, ":random_no", -100, 200),
      # (ge, ":random_no", "$g_player_luck"),
      (ge, ":random_no", 0),
      (str_store_string, s12, "@ Unfortunately, when the guards inquired about the tavern brawl, your description was recognized and you were in no condition to fight them off."),
    (try_end),
    ],
    [
      ("continue",[(eq, "$sneaked_into_town", disguise_none),],"Continue...",
       [
		(try_begin), # Drunk barfight loss scene
			(eq, "$g_sexual_content", 2),
			(this_or_next|eq, "$character_gender", 1),(eq, "$g_nohomo", 0),
			(call_script, "script_change_troop_renown", "trp_player", -5),
			(call_script, "script_start_fucking", 2, "scn_tavern"),
		(else_try),
        (jump_to_menu, "mnu_town"),
        (troop_set_health, "trp_player", 25),
        #SB : renown loss, less than losing to bandits
        (call_script, "script_change_troop_renown", "trp_player", -1),
		(try_end),
       ]),

      ("surrender",[(gt, "$sneaked_into_town", disguise_none),],"Surrender...",
       [
         (jump_to_menu, "mnu_captivity_castle_taken_prisoner"),
       ]),
    ]
  ),
  ("establish_court",mnf_disable_all_keys,
    "To establish {s4} as your court will require a small refurbishment. In particular, you will need a set of tools and a bolt of velvet. it may also take a short while for some of your followers to relocate here. Do you wish to proceed?",
    "none",
    [
	(str_store_party_name, s4, "$g_encountered_party"),
	],

    [
      ("establish",[
	  (player_has_item, "itm_tools"),
	  (player_has_item, "itm_velvet"),
	  ],"Establish {s4} as your court",
       [
		(assign, "$g_player_court", "$current_town"),
	    (troop_remove_item, "trp_player", "itm_tools"),
	    (troop_remove_item, "trp_player", "itm_velvet"),
        (jump_to_menu, "mnu_center_manage"),
       ]),

    ("capital_exists",
      [
        (store_and, ":name_set", "$players_kingdom_name_set", rename_center),
        (ge, ":name_set", rename_center),
        (str_store_party_name, s1, "$g_player_court"),
        (disable_menu_option),
      ],
       "You cannot move the court as your capital is at {s1}.",
       [
     ]),


      ("continue",[],"Hold off...",
       [
         (jump_to_menu, "mnu_center_manage"),
       ]),
    ]
  ),
  (
    "fuck",0,
    "Select a scene.",
    "none",
    [
	],
    [
      ("snow",[],"snow",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_camp_scene_snow"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Snow."),
      ("desert",[],"desert",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_camp_scene_desert"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Desert."),
      ("steppe",[],"steppe",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_camp_scene_steppe"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Steppe."),
      ("plain",[],"plain",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_camp_scene_plain"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Plain."),
      ("manor",[],"Manor",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_manor"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Manor."),
      ("tavern",[],"Tavern",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_tavern"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Tavern."),
      ("dungeon",[],"Dungeon",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_dungeon"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Dungeon."),
      ("ship_a",[],"Ship a",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_sea_1"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Ship a."),
      ("ship_b",[],"Ship b",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_sea_2"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Ship b."),
      ("ship_c",[],"Ship c",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_sea_3"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Ship c."),
      ("ship_d",[],"Ship d",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_sea_4"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Ship d."),
      # ("aa",[],"a a",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_a_a"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"a a."),
      # ("ab",[],"a b",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_a_b"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"a b."),
      # ("ac",[],"a c",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_a_c"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"a c."),
      # ("ad",[],"a d",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_a_d"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"a d."),
      # ("bb",[],"b b",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_b_b"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"b b."),
      # ("bc",[],"b c",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_b_c"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"b c."),
      # ("bd",[],"b d",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_b_d"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"b d."),
      # ("cc",[],"c c",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_c_c"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"c c."),
      # ("cd",[],"c d",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_c_d"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"c d."),
      # ("dd",[],"d d",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_d_d"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"d d."),
      ("leave",[],"back",[(jump_to_menu, "mnu_camp")]),
    ]
  ),
  (
    "fuck_2",0,
    "Pick a position",
    "none",
    [(assign, "$g_sex_position", 0),
	 (assign, "$temp", 3),
	 (assign, "$temp_2", 1),
	 (call_script, "script_write_fit_party_members_to_stack_selection", "p_main_party", 1),
	],
    [
      ("op_1",[],"Riding",[
		  (assign, "$g_sex_position", 0),
		  (jump_to_menu,"mnu_fuck_3"),
	  ],"Riding"),
      ("op_2",[],"Fucking from behind",[
		  (assign, "$g_sex_position", 1),
		  (jump_to_menu,"mnu_fuck_3"),
	  ]),
      ("op_3",[],"Fucking both ends",[
		  (assign, "$g_sex_position", 2),
		  (assign, "$temp", 4),
		  (jump_to_menu,"mnu_fuck_3"),
	  ]),
      ("leave",[],"Go back.",[(jump_to_menu, "mnu_camp")]),
	]
  ),
  ("fuck_3",0,
   "Who will be {s4}?^{s1}^{reg1}:",
   "none",
    [
      (assign, reg1, "$temp_2"),
      (troop_get_slot, "$temp_3", "trp_stack_selection_amounts", 0), #number of slots

	  (str_clear, s4),
	  (try_begin),
		  (eq, "$temp_2", 1),
		  (str_store_string, s4, "@getting fucked"),
	  (else_try),
		  (eq, "$temp_2", 4),
		  (str_store_string, s4, "@fucking the mouth"),
	  (else_try),
		  (eq, "$temp_2", 3),
		  (str_store_string, s4, "@watching"),
	  (else_try),
		  (str_store_string, s4, "@fucking"),
	  (try_end),

      #SB : show current list
      (str_clear, s1),
      (store_sub, ":end", "$temp_2", 1),
      (try_for_range, ":slot_index", 0, ":end"),
        (store_add, reg0, ":slot_index", 1),
        (troop_get_slot, ":troop_id", "trp_temp_array_a", ":slot_index"),
		(try_begin),
			(ge, ":troop_id", 0),
			(str_store_troop_name, s2, ":troop_id"),
			(str_store_string, s1, "@{s1}^{reg0}: {s2}"),
        (else_try),
			(str_store_string, s1, "@{s1}^{reg0}: No one"),
		(try_end),
      (try_end),
    ],
    [
      ("training_ground_selection_details_melee_random", [], "Choose randomly.",
       [(call_script, "script_training_ground_sub_routine_2_for_melee_details_fuck", -1),]),
      ("go_back_dot",[],"Go back.",
       [(jump_to_menu, "mnu_camp"),]
       ), #SB : stack built from loop
	  ("nobody", [], "No one.",
       [(call_script, "script_training_ground_sub_routine_2_for_melee_details_fuck", -2),]
	  ),
      ]+
      [("stack"+str(x), [(call_script, "script_cf_training_ground_sub_routine_1_for_melee_details", x),], "{s0}",
       [(call_script, "script_training_ground_sub_routine_2_for_melee_details_fuck", x),])
       for x in range(0, 20)]
  ),
  (
    "fucked_by_enemy",0,
    "{s10}",
    "none",
    [
		 (set_background_mesh, "mesh_pic_custom_03"),
         (set_camera_follow_party, "$capturer_party"),
         (assign, "$g_player_is_captive", 1),
         (store_random_in_range, ":random_hours", 18, 30),
         (call_script, "script_event_player_captured_as_prisoner"),
         (call_script, "script_stay_captive_for_hours", ":random_hours"),
         (assign,"$auto_menu","mnu_captivity_wilderness_check"),

        (call_script, "script_change_troop_renown", "trp_player", -10),

        (troop_get_slot, ":dna", "trp_temp_array_c", 17),
        (troop_set_slot, "trp_temp_array_b", 0, -1),

		(try_begin),
		(this_or_next|eq, "$character_gender", 1),(eq, "$g_nohomo", 0),
        (troop_set_slot, "trp_temp_array_a", 0, "trp_player"),
		(try_end),


		(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
		(try_begin),
			(assign, ":fems", 0),
			(try_for_range, ":i_stack", 0, ":num_stacks"),
				(party_stack_get_troop_id, ":troop_id", "p_main_party", ":i_stack"),
				(troop_is_hero, ":troop_id"),
				(this_or_next|eq, "$g_nohomo", 0),
				(call_script, "script_cf_dplmc_troop_is_female", ":troop_id"),
				(val_add, ":fems", 1),
			(try_end),
			(store_random_in_range, ":ff", 0, ":fems"),
			(try_begin),
				(try_for_range, ":i_stack", 0, ":num_stacks"),
					(party_stack_get_troop_id, ":troop_id", "p_main_party", ":i_stack"),
					(troop_is_hero, ":troop_id"),
					(this_or_next|eq, "$g_nohomo", 0),
					(call_script, "script_cf_dplmc_troop_is_female", ":troop_id"),
					(try_begin),
						(gt, ":ff", 0),
						(val_sub, ":ff", 1),
					(else_try),
						(eq, ":ff", 0),
						(val_sub, ":ff", 1),
						(troop_set_slot, "trp_temp_array_a", 0, ":troop_id"),
						(troop_set_slot, "trp_temp_array_b", 0, -1),
						(try_begin),
							(neq, ":troop_id", "trp_player"),
							(troop_set_slot, "trp_temp_array_a", 2, "trp_player"),
							(troop_set_slot, "trp_temp_array_b", 2, -1),
							(else_try),
							(troop_set_slot, "trp_temp_array_a", 2, -1),
							(troop_set_slot, "trp_temp_array_b", 2, -1),
						(try_end),
					(try_end),
				(try_end),
			(try_end),
		(try_end),

        (troop_set_slot, "trp_temp_array_a", 1, "$g_talk_troop"),
        (troop_set_slot, "trp_temp_array_b", 1, ":dna"),
        (store_random_in_range, ":r", 0, 2),
        (assign, "$g_sex_position", ":r"),

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
            (party_get_slot, ":ship_type", "$capturer_party", slot_party_ship_type),
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

		(assign, "$f_temp_var", ":scene_to_use"),
		(troop_get_slot, ":girl", "trp_temp_array_a", 0),
		(str_store_troop_name,s4,":girl"),
		(try_begin),
			(eq, ":girl", 0),
			(str_store_string, s10, "@Your enemies take you prisoner, and drag you back to their camp. ^^After a few hungry glances, their leader snatches your hair and roughly pulls you into his tent where he tears your clothes away."),
			(else_try),
			(str_store_string, s10, "@Your enemies take you and your companions prisoner, leading all of you back to their camp. ^^After a few hungry glances, their leader grabs you by the arm and snatches {s4}'s hair. He roughly pulls you both into his tent and tears both your clothes away."),
		(try_end),
     ],
    [
      ("continue",[],"Continue...",
       [
	   	(try_begin),
		(troop_get_slot, ":target_char", "trp_temp_array_a", 2),
		(neq, ":target_char", "trp_player"),
		(assign, ":pos", 2),
		(else_try),
		(assign, ":pos", 3),
		(try_end),
		(call_script, "script_start_fucking", ":pos", "$f_temp_var"),
		(assign, "$f_temp_var", 0),
         ]),
      ]
  ),
  (
    "fucked_by_enemy_prison",0,
    "The guards are infuriated by your refusal to pay the ransom.\
    They tell you that if you are not willing to pay, then there is no longer any reason to treat you humanely.\One of the guards then reaches for the keys to your cell, grins, and says that he is going to teach you a lesson.",
    "none",
    [
     ],
    [
      ("continue",[],"Continue...",
       [

            (assign, "$g_player_is_captive", 1),
            (store_random_in_range, reg(8), 16, 22),
            (call_script, "script_stay_captive_for_hours", reg8),
            (assign,"$auto_menu", "mnu_captivity_castle_check"),

		    (store_faction_of_party, ":capturer_faction", "$capturer_party"),

            (faction_get_slot, ":troop_prison_guard", ":capturer_faction", slot_faction_prison_guard_troop),
            (call_script, "script_change_troop_renown", "trp_player", -2),

            (try_begin),
                (eq, ":troop_prison_guard", -1),
                (assign, ":troop_prison_guard", "trp_hired_blade"),
            (try_end),

            (troop_set_slot, "trp_temp_array_a", 0, "trp_player"),
            (troop_set_slot, "trp_temp_array_a", 1, ":troop_prison_guard"),
            (troop_set_slot, "trp_temp_array_a", 2, -1),
            (troop_set_slot, "trp_temp_array_a", 3, ":troop_prison_guard"),
            (assign, "$g_sex_position", 2),
            (assign, "$f_cons1", -1), #Non-con
			(assign, "$f_cons2", 0), #Con
			(assign, "$f_cons3", 0), #Con
			(assign, "$f_cons4", 0), #Con
            (call_script, "script_start_fucking", 4, "scn_dungeon"),

         ]),
      ]
  ),
  (
    "choose_banner",0,
    "Members of the nobility are each granted the right to carry their own banner. {s1} can either choose between the preset banners or design a custom banner.",
    "none",
    [
        (try_begin),
            (neq, "$g_edit_banner_troop", "trp_player"),
            (str_store_troop_name, s1, "$g_edit_banner_troop"),
        (else_try),
            (str_store_string, s1, "@You"),
        (try_end),
     ],
    [
      ("select_preset_banner",[],"Choose from preset banners.",
       [
           (jump_to_menu, "mnu_auto_return"),
           (start_presentation, "prsnt_banner_selection"),
        ]
       ),
      ("select_custom_banner",[],"Create a custom banner.",
       [
           (jump_to_menu, "mnu_auto_return"),
           (start_presentation, "prsnt_custom_banner"),
        ]
       ),
      ]
  ),
  ("content_options",0,
   "Diplomacy Content Options",
   "none",
   [     (set_background_mesh, "mesh_pic_camp"), ],
    [
      ("camp_fuck_setting",[
        #(eq,0,1),
        (try_begin),
            (eq, "$g_sexual_content", 2),
            (str_store_string, s0, "@Consensual and non-consensual sex are enabled"),
        (else_try),
            (eq, "$g_sexual_content", 1),
            (str_store_string, s0, "@Consensual sex is enabled"),
        (else_try),
            (str_store_string, s0, "@Sexual content is disabled"),
        (try_end),
      ],"{s0}",
       [
       (try_begin),
            (ge, "$g_sexual_content", 2),
            (assign, "$g_sexual_content", 0),
       (else_try),
            (store_add, "$g_sexual_content", 1, "$g_sexual_content"),
       (try_end),
        ]
       ),

      ("camp_dark_hunters",[(assign, reg0, "$g_dark_hunters_enabled"),],"{reg0?Dis:En}able Dark Hunter's and Black Khergit Raider's spawning script",
       [
           (val_clamp, "$g_dark_hunters_enabled", 0, 2), #in case of other values
           (store_sub, "$g_dark_hunters_enabled", 1, "$g_dark_hunters_enabled"),
        ]
       ),
      ("camp_remove_dark_hunters",[(eq, "$g_dark_hunters_enabled", 0),],"Remove all Dark Hunters and Black Khergit Raider parties from the map",
       [
           (assign, ":removed", 0),
           (try_for_parties, ":party_no"),
                (party_get_template_id, ":ptid", ":party_no"),
                (this_or_next|eq, ":ptid", "pt_dark_hunters"),
                (eq, ":ptid", "pt_black_khergit_raiders"),
                (remove_party, ":party_no"),
                (val_add, ":removed", 1),
           (try_end),
           (assign, reg0, ":removed"),
           (display_message, "@{reg0} parties removed from the map."),
        ]
       ),
      ("camp_realistic_wounding",[(assign, reg0, "$g_realistic_wounding"),],"{reg0?Dis:En}able realistic casualties",
       [
           (val_clamp, "$g_realistic_wounding", 0, 2), #in case of other values
           (store_sub, "$g_realistic_wounding", 1, "$g_realistic_wounding"),
        ]
       ),
      ("camp_same_sex_on",[(neq, "$g_disable_condescending_comments", 2)],"Enable same sex marriage",
       [
           (assign,"$g_disable_condescending_comments", 2),
        ]
       ),
      ("camp_same_sex_off", [(neq, "$g_disable_condescending_comments", 0)],
        "Disable same sex marriage",
        [(assign, "$g_disable_condescending_comments", 0),
        ]
       ),
      ("camp_polygamy",[(assign, reg0, "$g_polygamy"),],"{reg0?Dis:En}able polygamy",
       [
           (val_clamp, "$g_polygamy", 0, 2), #in case of other values
           (store_sub, "$g_polygamy", 1, "$g_polygamy"),
        ]
       ),
      ("camp_nohomobro",[(assign, reg0, "$g_nohomo"),],"{reg0?Dis:En}able gay scenes",
       [
           (val_clamp, "$g_nohomo", 0, 2), #in case of other values
           (store_sub, "$g_nohomo", 1, "$g_nohomo"),
        ]
       ),
       ("back",[],"Back",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
  (
    "fuck_encounter",0,
    "Continue",
    "none",
    [
        # (troop_set_slot, "trp_temp_array_a", 0, "trp_player"),
        # (troop_set_slot, "trp_temp_array_b", 0, -1),
        # (troop_set_slot, "trp_temp_array_a", 1, "$g_talk_troop"),
        # (troop_set_slot, "trp_temp_array_b", 1, ":dna"),
        # (store_random_in_range, ":r", 0, 2),
        # (assign, "$g_sex_position", ":r"),

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

		(assign, "$f_temp_var", ":scene_to_use"),

		(assign, "$f_cons1", -1), #Non-con
		(assign, "$f_cons2", 0), #Con
     ],
    [
      ("continue",[],"Continue...",
       [
        (call_script, "script_start_fucking", 2, "$f_temp_var"),
		(assign, "$f_temp_var", 0),
       ]),
      ]
  ),
  (
    "startgame_mod_options",0,
    "Now decide how the world will behave.^Nearly everything may be changed later through the camp menu, but the content option will make some irreversable changes to the game world.",
    "none",
    [],
    [
	  # XGM Mod Menu, contains most basic settings
      ("camp_mod_opition",[],"Change Settings", [(start_presentation, "prsnt_mod_option"),(assign, "$f_temp_var", 1),]),
      ("options_back",[],"Continue",
       [
			(try_begin),
				(eq, "$f_temp_var", 0),
				(display_message, "@You haven't checked the options yet. Are you sure?"),
				(assign, "$f_temp_var", 2),
			(else_try),
				(eq, "$f_temp_var", 2),
				(display_message, "@Absolutely sure?"),
				(assign, "$f_temp_var", 3),
			(else_try),
				(eq, "$f_temp_var", 3),
				(assign, "$f_temp_var", 0),
				(display_message, "@Ok, fine."),
				(jump_to_menu, "mnu_c3_finalize"),
			(else_try),
				(assign, "$f_temp_var", 0),
				(jump_to_menu, "mnu_c3_finalize"),
			(try_end),
        ]),
     ]
  ),

  #Autotrade begin,
  (
    "auto_trade",0,
    "Trade goods will automatically be bought if their price is low enough or sold if their price is high enough. You can adjust the price thresholds, disable auto trading for certain goods, or set minimum and maximum quantities to avoid filling your inventory with one type of item or selling items you want to keep.",
    "none",
  [],
  [
    ("continue",[],"Continue...",
    [
      (call_script, "script_auto_trade_at_center", "$current_town"),
      (jump_to_menu, "$g_next_menu"),
    ]),
    ("change_settings",[],"Change settings.",[(start_presentation, "prsnt_auto_trade_options"),]),
    ("go_back",[],"Go back",[(jump_to_menu, "$g_next_menu")]),
  ]
  ),
  #Autotrade end,
]
