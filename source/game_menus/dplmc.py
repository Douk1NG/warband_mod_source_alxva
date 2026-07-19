# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_menus = [
  (
    "dplmc_notification_alliance_declared",0,
    "Alliance Agreement^^{s1} and {s2} have formed an alliance!^{s57}",
    "none",
    [

	  (str_clear, s57),

	  (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (store_sub, ":faction_1", "$g_notification_menu_var1", kingdoms_begin),
      (store_sub, ":faction_2", "$g_notification_menu_var2", kingdoms_begin),
      (val_mul, ":faction_1", 128),
      (val_add, ":faction_1", ":faction_2"),
      (set_game_menu_tableau_mesh, "tableau_2_factions_mesh", ":faction_1", pos0),
      ],
    [
      ("dplmc_continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_defensive_declared",0,
    "Defensive Pact^^{s1} and {s2} have agreed to a defensive pact!^{s57}",
    "none",
    [

	  (str_clear, s57),

	  (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (store_sub, ":faction_1", "$g_notification_menu_var1", kingdoms_begin),
      (store_sub, ":faction_2", "$g_notification_menu_var2", kingdoms_begin),
      (val_mul, ":faction_1", 128),
      (val_add, ":faction_1", ":faction_2"),
      (set_game_menu_tableau_mesh, "tableau_2_factions_mesh", ":faction_1", pos0),
      ],
    [
      ("dplmc_continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_trade_declared",0,
    "Trade Agreement^^{s1} and {s2} have signed a trade agreement!^{s57}",
    "none",
    [

	  (str_clear, s57),

	  (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (store_sub, ":faction_1", "$g_notification_menu_var1", kingdoms_begin),
      (store_sub, ":faction_2", "$g_notification_menu_var2", kingdoms_begin),
      (val_mul, ":faction_1", 128),
      (val_add, ":faction_1", ":faction_2"),
      (set_game_menu_tableau_mesh, "tableau_2_factions_mesh", ":faction_1", pos0),
      ],
    [
      ("dplmc_continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_nonaggression_declared",0,
    "Non-aggression Treaty^^{s1} and {s2} have concluded a non-aggression treaty!^{s57}",
    "none",
    [
	  (str_clear, s57),

	  (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (store_sub, ":faction_1", "$g_notification_menu_var1", kingdoms_begin),
      (store_sub, ":faction_2", "$g_notification_menu_var2", kingdoms_begin),
      (val_mul, ":faction_1", 128),
      (val_add, ":faction_1", ":faction_2"),
      (set_game_menu_tableau_mesh, "tableau_2_factions_mesh", ":faction_1", pos0),
      ],
    [
      ("dplmc_continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_question_alliance_offer",0,
    "You Receive an Alliance Offer^^The {s1} wants to form an alliance with you. What is your answer?",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("dplmc_alliance_offer_accept",[],"Accept",
       [
         (call_script, "script_dplmc_start_alliance_between_kingdoms", "fac_player_supporters_faction", "$g_notification_menu_var1", 1),
         (change_screen_return),
        ]),
      ("dplmc_alliance_offer_reject",[],"Reject",
       [
         (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -2),
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_question_defensive_offer",0,
    "You Receive a Pact Offer^^The {s1} offers you a defensive pact. What is your answer?",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("dplmc_defensive_offer_accept",[],"Accept",
       [
         (call_script, "script_dplmc_start_defensive_between_kingdoms", "fac_player_supporters_faction", "$g_notification_menu_var1", 1),
         (change_screen_return),
        ]),
      ("dplmc_defensive_offer_reject",[],"Reject",
       [
         (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -2),
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_question_trade_offer",0,
    "You Receive a Pact Offer^^The {s1} offers you a trade pact. What is your answer?",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("dplmc_trade_offer_accept",[],"Accept",
       [
         (call_script, "script_dplmc_start_trade_between_kingdoms", "fac_player_supporters_faction", "$g_notification_menu_var1", 1),
         (change_screen_return),
        ]),
      ("dplmc_trade_offer_reject",[],"Reject",
       [
         (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -2),
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_question_nonaggression_offer",0,
    "You Receive a Pact Offer^^The {s1} offers you a non-aggression treaty. What is your answer?",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("dplmc_nonaggression_offer_accept",[],"Accept",
       [
         (call_script, "script_dplmc_start_nonaggression_between_kingdoms", "fac_player_supporters_faction", "$g_notification_menu_var1", 1),
         (change_screen_return),
        ]),
      ("dplmc_nonaggression_offer_reject",[],"Reject",
       [
         (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -2),
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_alliance_expired",0,
    "Alliance Has Expired^^The alliance between {s1} and {s2} has expired and was degraded to a defensive pact.",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),

      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("dplmc_continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_defensive_expired",0,
    "Defensive Pact Has Expired^^The defensive pact between {s1} and {s2} has expired and was degraded to a trade agreement.",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),

      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("dplmc_continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_trade_expired",0,
    "Trade Agreement Has Expired^^The trade agreement between {s1} and {s2} has expired and was degraded to a non-aggression treaty.",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),

      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("dplmc_continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
  ),
  ("dplmc_dictate_terms",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "Dictate your peace terms.",
    "none",
    [(set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),],
    [
      ("dplmc_demand_4000",[(gt, "$g_player_chamberlain", 0),],"Demand 4000 denars",
      [
        (call_script, "script_npc_decision_checklist_peace_or_war", "$g_notification_menu_var1", "fac_player_supporters_faction", -1),
        (assign, ":goodwill", reg0),
        (store_random_in_range, ":random", 0, 4),

        (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -3),
        (try_begin),
          (le, ":random", ":goodwill"),
          (call_script, "script_dplmc_pay_into_treasury", 4000),
          (call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_notification_menu_var1", "fac_player_supporters_faction", 1),
          (change_screen_return),
        (else_try),
          (jump_to_menu,"mnu_dplmc_deny_terms"),
        (try_end),
      ]),
      ("dplmc_demand_8000",[(gt, "$g_player_chamberlain", 0),],"Demand 8000 denars",
       [
         (call_script, "script_npc_decision_checklist_peace_or_war", "$g_notification_menu_var1", "fac_player_supporters_faction", -1),
         (assign, ":goodwill", reg0),
         (val_mul, ":goodwill", 2),
				 (store_random_in_range, ":random", 0, 10),

         (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -5),
				 (try_begin),
				   (le, ":random", ":goodwill"),
           (call_script, "script_dplmc_pay_into_treasury", 8000),
           (call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_notification_menu_var1", "fac_player_supporters_faction", 1),
           (change_screen_return),
         (else_try),
             (jump_to_menu,"mnu_dplmc_deny_terms"),
         (try_end),
       ]),
      ("dplmc_demand_castle",[
        (assign, ":distance", 100),
        (assign, "$demanded_castle", -1),
		##diplomacy start+ Handle player is co-ruler of NPC kingdom
		(assign, ":alt_faction", "fac_player_supporters_faction"),
		(try_begin),
			(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":alt_faction", "$players_kingdom"),
		(try_end),
		##diplomacy end+
        (try_for_range, ":castle", castles_begin, castles_end),
          (store_faction_of_party, ":castle_faction", ":castle"),
          (eq, ":castle_faction", "$g_notification_menu_var1"),
          (try_for_range, ":center", centers_begin, centers_end),
            (store_faction_of_party, ":center_faction", ":center"),
			##diplomacy start+
			(this_or_next|eq, ":alt_faction", ":center_faction"),
			##diplomacy end+
            (eq, ":center_faction", "fac_player_supporters_faction"),
            (store_distance_to_party_from_party, ":tmp_distance", ":center", ":castle"),

            (lt, ":tmp_distance", ":distance"),
            (assign, ":distance", ":tmp_distance"),
            (assign, "$demanded_castle", ":castle"),
            (str_store_party_name, s2, ":castle"),
          (try_end),
        (try_end),
        (is_between, "$demanded_castle", castles_begin,castles_end),
      ],"Demand {s2}.",
       [
        (call_script, "script_npc_decision_checklist_peace_or_war", "$g_notification_menu_var1", "fac_player_supporters_faction", -1),
        (assign, ":goodwill", reg0),
        (val_mul, ":goodwill", 2),
        (store_random_in_range, ":random", 0, 12),

        (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -6),
        (try_begin),
          (le, ":random", ":goodwill"),
			 ##diplomacy start+
			 #Chance of veto based on ownership and difficulty setting.
			 (assign, ":did_veto", 0),
			 (try_begin),
					 (party_get_slot, ":castle_lord", "$demanded_castle", slot_town_lord),
					 (ge, ":castle_lord", 1),
					 (neg|troop_slot_ge, ":castle_lord", slot_troop_prisoner_of_party, 0),
					 (try_begin),
								(this_or_next|troop_slot_eq, ":castle_lord", slot_troop_home, "$demanded_castle"),
								(party_slot_eq, "$demanded_castle", dplmc_slot_center_original_lord, ":castle_lord"),
								(store_random_in_range, ":random", 0, 24),
								(assign, ":did_veto", 1),
								(le, ":random", ":goodwill"),
								(assign, ":did_veto", 0),
 					 (else_try),
								(troop_get_slot, ":castle_lord_original_faction", ":castle_lord", slot_troop_original_faction),
								(party_slot_eq, "$demanded_castle", slot_center_original_faction, ":castle_lord_original_faction"),
								(store_random_in_range, ":random", 0, 12),
								(assign, ":did_veto", 1),
								(le, ":random", ":goodwill"),
								(assign, ":did_veto", 0),
					 (try_end),
			 (try_end),
			 (eq, ":did_veto", 0),
		  ##Handle player is co-ruler of NPC kingdom
          ##OLD:
          #(call_script, "script_give_center_to_faction", "$demanded_castle", "fac_player_supporters_faction"),
          #(call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_notification_menu_var1", "fac_player_supporters_faction", 1),
		  ##NEW:
		  (assign, ":player_kingdom", "fac_player_supporters_faction"),
		  (try_begin),
		        (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
				(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
				(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
				(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
				(assign, ":player_kingdom", "$players_kingdom"),
		  (try_end),
		  (call_script, "script_give_center_to_faction", "$demanded_castle", ":player_kingdom"),
          (call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_notification_menu_var1", ":player_kingdom", 1),
		  ##diplomacy end+
          (change_screen_return),
        (else_try),
          (jump_to_menu,"mnu_dplmc_deny_terms"),
        (try_end),        ]
       ),
	  ("dplmc_go_back",[],"Go back",
       [
	     (jump_to_menu,"mnu_question_peace_offer"),
       ]),
    ]
  ),
  ("dplmc_deny_terms",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "The {s1} refuses your terms and is breaking off of negotiations.",
    "none",
    [(set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),],
    [
	  ("dplmc_continue",[],"Continue",
       [
       (change_screen_return),
       ]),
    ]
  ),
  (
    "dplmc_village_riot_result",mnf_scale_picture,
    "{s9}",
    "none",
    [(try_begin),
       (eq, "$g_battle_result", 1),
       (jump_to_menu, "mnu_dplmc_village_riot_removed"),
     (else_try),
       (set_background_mesh, "mesh_pic_villageriot"),
       (str_store_string, s9, "@Try as you might, you could not defeat the rebelling village."),
     (try_end),
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [(call_script, "script_change_player_relation_with_center", "$g_encountered_party", -3),
        (call_script, "script_change_troop_renown", "trp_player", -5), #SB : renown loss highest here
        (jump_to_menu, "mnu_village"),]),
    ],
  ),
  (
    "dplmc_village_riot_removed",mnf_disable_all_keys,
    "In bloody battle you and your men slaughter the rebels and regain control over the village. But there is not much left you can control.",
    "none",
    [
     (set_background_mesh, "mesh_pic_looted_village"),
     (party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
     (call_script, "script_village_set_state",  "$current_town", svs_looted),
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (jump_to_menu, "mnu_village"),
       ]),
    ],
  ),
  (
    "dplmc_town_riot_removed",mnf_disable_all_keys,
    "In bloody battle you and your men slaughter the rebels and regain control over the town.",
    "none",
    [],
    [
      ("dplmc_continue",[],"Continue...",
       [
        (party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
        (assign, "$new_encounter", 1),
        (try_begin),
          (party_get_slot, ":town_lord","$g_encountered_party", slot_town_lord),
          (troop_get_slot, ":cur_banner", ":town_lord", slot_troop_banner_scene_prop),
          (try_begin),
              (gt, ":cur_banner", 0),
              (val_sub, ":cur_banner", banner_scene_props_begin),
              (val_add, ":cur_banner", banner_map_icons_begin),
              (party_set_banner_icon, "$g_encountered_party", ":cur_banner"),
          (else_try),
              (eq, ":cur_banner", -1),
              (troop_get_slot, ":flag_icon", ":town_lord", slot_troop_custom_banner_map_flag_type),
              (try_begin),
                (ge, ":flag_icon", 0),
                (val_add, ":flag_icon", custom_banner_map_icons_begin),
                (party_set_banner_icon, "$g_encountered_party", ":flag_icon"),
              (try_end),
          (try_end), #custom_banner_begin
        (try_end),
        (jump_to_menu, "mnu_castle_outside"),
       ]),
    ],
  ),
  (
    "dplmc_riot_negotiate",mnf_disable_all_keys,
    "You approach the angry crowd and begin negotiations. The leader of the riot demands {reg0} denars. He agrees to lay down arms if you are willing to pay.",
    "none",
    [
      (party_get_slot, ":center_relation", "$g_encountered_party", slot_center_player_relation),
      (val_min, ":center_relation", 0),
      (try_begin),
        (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
        (val_sub, ":center_relation", 75),
        (set_background_mesh, "mesh_pic_townriot"),
      (else_try),
        (val_sub, ":center_relation", 50),
        (set_background_mesh, "mesh_pic_villageriot"),
      (try_end),

      (store_skill_level, ":persuasion_level", "skl_persuasion", "trp_player"),
      (val_add, ":center_relation", ":persuasion_level"),
      (val_mul, ":center_relation", ":center_relation"),
      (assign, reg0, ":center_relation"),
    ],
    [
      ("dplmc_pay_riot_treasury",
      [
        (gt, "$g_player_chamberlain", 0),
        (store_troop_gold, ":gold", "trp_household_possessions"),
        (ge, ":gold", reg0),
      ],"Induce your chamberlain to pay the money from the treasury.",
       [
        (call_script, "script_dplmc_withdraw_from_treasury", reg0),
        (party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (jump_to_menu, "mnu_castle_outside"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),

       ]),
       ("dplmc_pay_riot_cash",
      [
        (store_troop_gold, ":gold", "trp_player"),
        (ge, ":gold", reg0),
      ],"Pay cash.",
       [
        (troop_remove_gold, "trp_player", reg0),
        (party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (jump_to_menu, "mnu_castle_outside"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),

       ]),

      ("dplmc_back",[],"Back...",
       [
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (jump_to_menu, "mnu_castle_outside"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
       ]),
    ],
  ),
  (
    "dplmc_notification_riot",0,
    "The peasants of {s1} launched a riot against you! In a surprise attack, men loyal to you have been slain. The remainder joined the angry crowd.",
    "none",
    [
      (str_store_party_name, s1, "$g_notification_menu_var1"),
      (try_begin),
        (party_slot_eq, "$g_notification_menu_var1", slot_party_type, spt_town),
        (set_background_mesh, "mesh_pic_townriot"),
      (else_try),
        (set_background_mesh, "mesh_pic_villageriot"),
      (try_end),
      ],
    [
      ("dplmc_continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_appoint_chamberlain",0,
    "As a lord of a fief you can now appoint a chamberlain who resides at you court for a weekly salary of 15 denars. He will handle all financial affairs like collecting and determining taxes, paying wages and managing your estate. In addition he supervises money transfers between kingdoms giving you more diplomatic options.",
    "none",
    [],
    [

      ("dplmc_appoint_default",[],"Appoint a prominent nobleman from the area.",
       [
        (call_script, "script_dplmc_appoint_chamberlain"),
        (jump_to_menu, "mnu_dplmc_chamberlain_confirm"),
        ]),
      ("dplmc_continue",[],"Proceed without chamberlain.",
       [
         (assign, "$g_player_chamberlain", -1), #denied
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_chamberlain_confirm",0,
    "Your chamberlain can be found at your court. You should consult him if you want to give him any financial advice or you need greater amounts of money. You should always make sure that there is enough money in the treasury to pay for political affairs.",
    "none",
    [],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_appoint_constable",0,
    "As a lord of a fief you can now appoint a constable who resides at you court for a weekly salary of 15 denars. He will recruit new troops and provide information about your army.",
    "none",
    [],
    [

      ("dplmc_appoint_default",[],"Appoint a prominent nobleman from the area.",
       [
        (call_script, "script_dplmc_appoint_constable"),
        (jump_to_menu, "mnu_dplmc_constable_confirm"),
        ]),
      ("dplmc_continue",[],"Proceed without constable.",
       [
         (assign, "$g_player_constable", -1), #denied
         (assign, "$g_constable_training_center", -1),
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_constable_confirm",0,
    "Your constable can be found at your court. You should consult him if you want to recruit new troops or get detailed information about your standing army.",
    "none",
    [],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_notification_appoint_chancellor",0,
    "As a lord of a fief you can now appoint a chancellor who resides at you court for a weekly salary of 20 denars. He will be the keeper of your seal and conduct the correspondence between you and other important persons.",
    "none",
    [],
    [

      ("dplmc_appoint_default",[],"Appoint a prominent nobleman from the area.",
       [
        (call_script, "script_dplmc_appoint_chancellor"),
        (jump_to_menu, "mnu_dplmc_chancellor_confirm"),
        ]),
      ("dplmc_continue",[],"Proceed without chancellor.",
       [
         (assign, "$g_player_chancellor", -1), #denied
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_chancellor_confirm",0,
    "Your chancellor can be found at your court. You should consult him if you want to send messages or gifts.",
    "none",
    [],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_deserters",0,
    "Some of your men don't believe that you will pay their wages and desert. Overall you lose: {s11} men.",
    "none",
    [
      (set_background_mesh, "mesh_pic_deserters"),
      (store_random_in_range, ":random", 1,  "$g_notification_menu_var1"),
      (call_script, "script_dplmc_player_troops_leave", ":random"),
      (str_store_string, s11, "@{reg0}"),
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_negotiate_besieger",0,
    "You appear with a white flag at the top of the wall. After a while a negotiator of {s11} approaches you. He demands {s6} and all associated villages as well as {reg0} denars for safe conduct.",
    "none",
    [
      (party_get_slot, ":besieger", "$current_town", slot_center_is_besieged_by),
      (party_stack_get_troop_id, ":enemy_party_leader", ":besieger", 0),
      (str_store_troop_name, s11, ":enemy_party_leader"),
      (store_faction_of_troop, ":besieger_faction", ":enemy_party_leader"),

      ##diplomacy start+
	  #1) Support promoted kingdom ladies, mercenary parties, etc.
	  #2) Fix mistake with potentially not counting besieger party in the size calculation!
	  ##OLD:
	  #(assign, ":besieger_size", 0),
      #(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
      #  (store_faction_of_troop, ":lord_faction", ":lord"),
      #  (eq, ":lord_faction", ":besieger_faction"),
      #  (troop_get_slot, ":led_party", ":lord", slot_troop_leaded_party),
      ##NEW:
      (party_get_num_companions, ":besieger_size", ":besieger"),

	  (try_for_parties, ":led_party"),
        (ge, ":led_party", spawn_points_end),
        (neq, ":led_party", ":besieger"),#don't double count
        (store_faction_of_party, ":party_faction", ":led_party"),
        (eq, ":party_faction", ":besieger_faction"),
	  ##diplomacy end+
        (party_is_active, ":led_party"),

        (party_slot_eq, ":led_party", slot_party_ai_state, spai_accompanying_army),
        (party_slot_eq, ":led_party", slot_party_ai_object, ":besieger"),

        (party_is_active, ":besieger"),
        (store_distance_to_party_from_party, ":distance_to_marshal", ":led_party", ":besieger"),
        (lt, ":distance_to_marshal", 25),
        (party_get_num_companions, ":party_size", ":led_party"),
        (val_add, ":besieger_size", ":party_size"),
      (try_end),

      (assign, ":garrison_size", 0),
      (party_get_num_companion_stacks, ":num_stacks", "$current_town"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_size, ":stack_size", "$current_town", ":i_stack"),
        (val_add, ":garrison_size", ":stack_size"),
      (try_end),
      (val_sub, ":besieger_size", ":garrison_size"),

      (store_skill_level, ":player_persuasion_skill", "skl_persuasion", "trp_player"),
      (val_mul, ":player_persuasion_skill", 10),
      (store_sub, "$diplomacy_var", ":besieger_size", ":player_persuasion_skill"),
      (val_mul, "$diplomacy_var", 4),
      ##diplomacy start+ : include ransom cost in calculation
      (call_script, "script_calculate_ransom_amount_for_troop", "trp_player"),
      (val_add, "$diplomacy_var", reg0),
      ##diplomacy end+
      (val_max,"$diplomacy_var",500),
      (val_div, "$diplomacy_var", 100),
      (val_mul, "$diplomacy_var", 100),
      (assign, reg0, "$diplomacy_var"),

      (str_store_party_name, s6, "$current_town"),

    ],
      [
      ("dplmc_comply_treasury",
      [
        (store_troop_gold, ":gold", "trp_household_possessions"),
        (ge, ":gold", "$diplomacy_var"),
      ],"Comply and induce your chamberlain to pay the money from the treasury.",
      [
        (call_script, "script_dplmc_withdraw_from_treasury", "$diplomacy_var"),
		##diplomacy start+ when the player pays, give the gold to the lord
		(party_get_slot, ":besieger", "$current_town", slot_center_is_besieged_by),
		(party_stack_get_troop_id, ":enemy_party_leader", ":besieger", 0),
		(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", "$diplomacy_var", ":enemy_party_leader"),
		##diplomacy end+
        (call_script, "script_dplmc_player_center_surrender", "$current_town"),
        (change_screen_return),
      ]),

      ("dplmc_comply",
      [
        (store_troop_gold, ":gold", "trp_player"),
        (ge, ":gold", "$diplomacy_var"),
      ],"Comply and pay the gold.",
      [
        (troop_remove_gold, "trp_player", "$diplomacy_var"),
		##diplomacy start+ when the player pays, give the gold to the lord
		(party_get_slot, ":besieger", "$current_town", slot_center_is_besieged_by),
		(party_stack_get_troop_id, ":enemy_party_leader", ":besieger", 0),
		(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", "$diplomacy_var", ":enemy_party_leader"),
		##diplomacy end+
        (call_script, "script_dplmc_player_center_surrender", "$current_town"),
        (change_screen_return),
      ]),

      ("dplmc_break_off",[],"Break off negotiations.",
       [
          (jump_to_menu, "mnu_town"),
        ]),
     ]
  ),
  (
    "dplmc_messenger",0,
##nested diplomacy start+ "His" to "{reg4?Her:His}"
    "Sire, I found {s10} and delivered your message. {reg4?Her:His} answer was {s11}.",
##nested diplomacy end+
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (str_store_troop_name, s10, "$g_notification_menu_var1"),
        (try_begin),
          (eq, "$g_notification_menu_var2", 1),
          (str_store_string, s11, "@positive"),
        (else_try),
          (str_store_string, s11, "@negative"),
        (try_end),
        ##nested diplomacy start+
        (try_begin),
           (call_script, "script_cf_dplmc_troop_is_female", "$g_notification_menu_var1"),
           (assign, reg4, 1),
        (else_try),
           (assign, reg4, 0),
        (try_end),
        ##nested diplomacy end+
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_scout",0,
    "Your spy returned from {s10}^^{s11}{s12}",
    "none",
    [
    (set_background_mesh, "mesh_pic_messenger"),
    (str_store_party_name, s10, "$g_notification_menu_var1"),

    (call_script, "script_game_get_center_note", "$g_notification_menu_var1", 0),
    (str_store_string, s11, "@{!}{s0}"),
    (try_begin),
      (this_or_next|is_between, "$g_notification_menu_var1", towns_begin, towns_end),
      (is_between, "$g_notification_menu_var1", castles_begin, castles_end),
      (party_get_slot, ":center_food_store", "$g_notification_menu_var1", slot_party_food_store),
      (call_script, "script_center_get_food_consumption", "$g_notification_menu_var1"),
      (assign, ":food_consumption", reg0),
      (store_div, reg6, ":center_food_store", ":food_consumption"),
      (store_party_size, reg5, "$g_notification_menu_var1"),
      (str_store_string, s11, "@{s11}^^ The current garrison consists of {reg5} men.^The food stock lasts for {reg6} days."),
    (try_end),

    (str_clear, s12),
    (party_get_num_attached_parties, ":num_attached_parties", "$g_notification_menu_var1"),
    (try_begin),#<- dplmc+ unclosed try_begin!
      (gt, ":num_attached_parties", 0),
      (str_store_string, s12, "@^^Additional the following parties are currently inside:^"),
    (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
      (party_get_attached_party_with_rank, ":attached_party", "$g_notification_menu_var1", ":attached_party_rank"),
      (str_store_party_name, s3, ":attached_party"),
      (store_party_size, reg1, ":attached_party"),
      (str_store_string, s12, "@{s12} {s3} with {reg1} troops.^"),
    (try_end),
	##diplomacy start+
	#Add missing try-end for (gt, ":num_attached_parties", 0),
	(try_end),
	##diplomacy end+

    (call_script, "script_update_center_recon_notes", "$g_notification_menu_var1"),
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_domestic_policy",0,
    "You can now shape the domestic policy of your kingdom. Do you want to change your policy now?",
    "none",
    [
      (try_begin),
          (eq, "$g_players_policy_set", 1),
          (change_screen_return),
      (try_end),

      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "fac_player_supporters_faction", pos0),
    ],
    [
      ("dplmc_yes",[],"Yes, I want to change the domestic policy.",
       [
         (start_presentation, "prsnt_dplmc_policy_management"),
        ]),
      ("dplmc_no",[],"No, I don't want to change the domestic policy.",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_affiliate_end",0,
    "{!}{s11}",
    "none",
    [
      (set_background_mesh, "mesh_pic_messenger"),

      (str_store_troop_name, s9, "$g_notification_menu_var1"),
      (try_begin),
        ##nested diplomacy start+ (1) Fix a bug from the Diplomacy 3.3.2 version of this menu by getting your ex-affiliate
	    #from "$g_notification_menu_var2" instead of "$g_player_affiliated_troop".
        ##OLD: #(eq, "$g_player_affiliated_troop", "$g_notification_menu_var1"),
        (eq, "$g_notification_menu_var2", "$g_notification_menu_var1"),
        ##nested diplomacy end+
        (str_store_string, s11, "@{playername}, ^^I always knew you were a bad egg, since the day you have pledged allegiance to my clan. ^Did you really think you could set my family against me? You've dropped your mask, you snake! You are an infliction, and I will not bear it anymore. ^Hereby, I disown and ban you from my house. I have urged my family to fight you, and I will warn Calradia lords about your infamy. ^Tremble with fear, you have a deadly enemy! ^^{s9}."),
      (else_try),
        ##nested diplomacy start+ (2) Fix a bug from the Diplomacy 3.3.2 version of this menu by getting your ex-affiliate
	    #from "$g_notification_menu_var2" instead of "$g_player_affiliated_troop".
        ##OLD:
		#(is_between, "$g_player_affiliated_troop", lords_begin, kingdom_ladies_end),
        #(str_store_troop_name, s10, "$g_player_affiliated_troop"),
		##NEW:
		(ge, "$g_notification_menu_var2", walkers_end),
        (troop_is_hero, "$g_notification_menu_var2"),
		(str_store_troop_name, s10, "$g_notification_menu_var2"),
        ##### (3) Make the next line use correct pronouns, and correct term for king/queen.  TODO: Change some of the funny wording.
		##OLD:
        #(str_store_string, s11, "@{playername},^^ I've received a letter from {s9}, telling me about your disgracefull jiggery-pokery. In the present circumstances, {s9} could not provide evidence. But unlike you, {he/she} is a distinguished member of my family; and since all these years, I never had any reason to distrust {him/her}. I take {his/her} charges for granted. ^Hopefully, you failed to breakup my family unit. Hereby I reject your pledge : you are no longer related to my house. Each membership will retaliate against you in all conscience... ^I would be ashamed to confess how you maliciously fooled me, so I will not challenge you, to not be accountable for your death to my King. However I'm not used to report him every rat I crush while in wilderness, someday I may find you there ! ^^{s10}"),
		##NEW:
		(call_script, "script_dplmc_store_troop_is_female", "$g_notification_menu_var1"),
		(assign, reg1, reg0),#Move to reg1, because reg0 will be overwritten below
        (store_faction_of_troop, ":faction_var", "$g_notification_menu_var2"),
		(try_begin),
		   (gt, ":faction_var", 0),
		   (faction_get_slot, ":faction_var", ":faction_var", slot_faction_leader),
		   (gt, ":faction_var", 0),
		   (call_script, "script_dplmc_store_troop_is_female", ":faction_var"),
		   (eq, reg0, 1),
		   (call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_notification_menu_var2", DPLMC_CULTURAL_TERM_KING_FEMALE, s11),
		   (assign, reg1, 1),#make sure the above didn't do anything funny with the register
		(else_try),
		   (call_script, "script_dplmc_print_cultural_word_to_sreg", "$g_notification_menu_var2", DPLMC_CULTURAL_TERM_KING, s11),
		   (assign, reg1, 0),#if there was no faction leader, reg0 might not have been initialized in the first place
		(try_end),
		#Aside from making the next line use the correct gender for the pronoun,
		#I made the wording a tiny bit less strange (although I left in "jiggery-pokery").
        (str_store_string, s11, "@{playername},^^ I've received a letter from {s9}, telling me about your disgraceful jiggery-pokery. In the present circumstances, {s9} could not provide evidence. But unlike you, {reg1?she:he} is a distinguished member of my family; and since all these years, I never had any reason to distrust {reg1?her:him}. I take {reg1?her:him} charges for granted. ^Hopefully, you failed to breakup my family unit. Hereby I reject your pledge : you are no longer related to my house. Each membership will retaliate against you in all conscience... ^I would be ashamed to confess how you maliciously fooled me, so I will not challenge you, to not be accountable for your death to my {s11}. However I'm not used to telling {reg0?her:him} about every rat I crush in the wilderness, and someday I may find you there ! ^^{s10}"),
        ##nested diplomacy end+
      (try_end),
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  ),
  (
    "dplmc_preferences",0,
    "All Options",## Hijacked this to be the consolidated options menu.
    "none",
    [],
    [
	  # XGM Mod Menu, contains most basic settings
      ("camp_mod_opition",[],"Main Settings", [(start_presentation, "prsnt_mod_option")]),
	  # Formations Mod Settings
      ("formation_mod_option",[],"Formations Mod Settings", [(start_presentation, "prsnt_formation_mod_option")]),
	  # Camera Hotkeys
      ("dplmc_deathcam_keys",[ (eq, "$g_dplmc_battle_continuation", 0),],"Camera Keys Settings",[(assign, "$g_presentation_next_presentation", "prsnt_redefine_keys"),(start_presentation, "prsnt_redefine_keys"),]),
      ("dplmc_back",[],"Return",
       [
           (jump_to_menu, "mnu_camp"),
        ]),
     ]
  ),

  ##diplomacy end
##diplomacy start+,
  ("dplmc_start_select_prejudice",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "In the traditional medieval society depicted in the game, war and politics are usually dominated by male members of the nobility.  Because of this, a female character can face initial prejudice, and some opportunities open to men will not be available (although a woman will also have some opportunities a man will not).  Some players might find distasteful, so if you want you can ignore that aspect of society in Calradia.^^You can later change your mind through the options in the Camp menu.",
    "none",
    [],
    [
      ("dplmc_start_prejudice_yes",[],"I do not mind encountering sexism.",
       [
         (assign, "$g_disable_condescending_comments", 0),#Default value
         (jump_to_menu,"mnu_start_character_1"),
        ]
       ),
      ("dplmc_start_prejudice_no",[],"I would prefer not to encounter as much sexism.",
       [
         (assign, "$g_disable_condescending_comments", 2),#Any value 2 or higher shuts off sexist setting elements
         (jump_to_menu, "mnu_start_character_1"),
       ]
       ),
	  ("go_back",[],"Go back",
       [
	     (jump_to_menu,"mnu_start_game_1"),
       ]),
    ]
  ),

  ##Economic report, currently just for debugging purposes,
  (
    "dplmc_choose_disguise", 0,
    "You are about to sneak into {s1}. Make sure you don't bring suspicious items or excess denars that might be confiscated. {s2}",
    "none",
    [

         (troop_get_inventory_capacity, ":inv_cap", "trp_random_town_sequence"),
         (assign, ":count", 0),
         (try_for_range, ":i_slot", ek_food + 1, ":inv_cap"),
           (troop_get_inventory_slot, ":cur_item", "trp_random_town_sequence", ":i_slot"),
           (gt, ":cur_item", -1),
           #(assign, reg3, ":cur_item"),
           #(display_message, "@{reg3}"),
           (val_add, ":count", 1),
         (try_end),
         # (assign, reg0, ":count"),
         # (assign, reg1, "$temp"),
         # (display_message, "@{reg0} , {reg1}"),
         (try_begin),
            (gt, ":count", "$temp"),
            #put stuff back
            (set_show_messages, 0), #move all gold
            (call_script, "script_move_inventory_and_gold", "trp_random_town_sequence", "trp_player", -1),
            (set_show_messages, 1),
            (display_message, "@You cannot bring that many items with you. Your items have been returned to your inventory."),
         (try_end),

        (str_store_party_name, s1, "$current_town"),
        #build text
        (try_begin),
          (eq, "$sneaked_into_town", disguise_none),
          (str_store_string, s2, "@Select a suitable disguise for this occasion."),
          (assign, "$temp", 0),
        (else_try),
          (eq, "$sneaked_into_town", disguise_pilgrim),
          (str_store_string, s2, "@As a poor pilgrim with a stout stick and a few tricks up your sleeve, you will be able to blend in with the crowds but not bring much of value with you."),
          (assign, "$temp", 6),
        (else_try),
          (eq, "$sneaked_into_town", disguise_farmer),
          (str_store_string, s2, "@As a farmer, you will be able to a wrangle livestock and smuggle articles of food through."),
          (assign, "$temp", 15),
        (else_try),
          (eq, "$sneaked_into_town", disguise_hunter),
          (str_store_string, s2, "@As a hunter, provisions and raw goods are expected as well as horseflesh."),
          (assign, "$temp", 12),
        (else_try),
          (eq, "$sneaked_into_town", disguise_guard),
          (str_store_string, s2, "@As a caravan guard, you will be able to bear weapons but bring only a few personal belongings."),
          (assign, "$temp", 6),
        (else_try),
          (eq, "$sneaked_into_town", disguise_merchant),
          (str_store_string, s2, "@As a merchant, you will be able to bring any assortment of goods."),
          (assign, "$temp", 32),
        (else_try),
          (eq, "$sneaked_into_town", disguise_bard),
          (str_store_string, s2, "@As a bard, you will be allowed some personal possessions and your instrument."),
          (assign, "$temp", 9),
        (try_end),
        (set_fixed_point_multiplier, 100),
        (init_position, pos0),
        (try_begin),
          (str_is_empty, s2),
          (position_set_x, pos0, 17),
          (position_set_y, pos0, 30),
          (position_set_z, pos0, 100),
        (else_try),
          (position_set_x, pos0, 60),
          (position_set_y, pos0, 20),
          (position_set_z, pos0, 100),
        (try_end),
        (set_game_menu_tableau_mesh, "tableau_game_inventory_window", "trp_player", pos0),
        (troop_get_slot, "$temp_2", "trp_player", slot_troop_player_disguise_sets),
    ],
    [
      ("continue",
      [(gt, "$temp", 0),
       (assign, reg1, "$temp"),],
      "Choose up to {reg1} items to bring.",
      [
        (change_screen_loot, "trp_random_town_sequence"),
      ]),

      ("continue",
      [(neq, "$sneaked_into_town", disguise_none)],
      "Select how much gold to carry.",
      [
        (assign, "$pool_troop", "trp_random_town_sequence"),
        (start_presentation, "prsnt_deposit_withdraw_money"),
      ]),

      ("continue",
      [(neq, "$sneaked_into_town", disguise_none)],
      "Attempt to sneak in...",
      [
        (set_show_messages, 0),

        #do inventory placeholder
        (troop_clear_inventory, "trp_temp_troop"),
        (call_script, "script_dplmc_copy_inventory", "trp_player", "trp_temp_troop"),
        (call_script, "script_dplmc_copy_inventory", "trp_random_town_sequence", "trp_player"),
        (call_script, "script_dplmc_copy_inventory", "trp_temp_troop", "trp_random_town_sequence"),
        #do gold swap
        (store_troop_gold, ":cur_amount", "trp_random_town_sequence"),
        (store_troop_gold, ":cur_gold", "trp_player"),
        (troop_remove_gold, "trp_player", ":cur_gold"),
        (troop_remove_gold, "trp_random_town_sequence", ":cur_amount"),
        (troop_add_gold, "trp_player", ":cur_amount"),
        (troop_add_gold, "trp_random_town_sequence", ":cur_gold"),

        (set_show_messages, 1),


        (faction_get_slot, ":player_alarm", "$g_encountered_party_faction", slot_faction_player_alarm),
        (party_get_num_companions, ":num_men", "p_main_party"),
        (party_get_num_prisoners, ":num_prisoners", "p_main_party"),
        (val_add, ":num_men", ":num_prisoners"),
        (val_mul, ":num_men", 2),
        (val_div, ":num_men", 3),
        (store_add, ":get_caught_chance", ":player_alarm", ":num_men"),
        (store_random_in_range, ":random_chance", 0, 100),
        (try_begin),
            (this_or_next|ge, "$cheat_mode", 1),
            (this_or_next|ge, ":random_chance", ":get_caught_chance"),
            (eq, "$g_last_defeated_bandits_town", "$g_encountered_party"),
            (assign, "$g_last_defeated_bandits_town", 0),
            (assign, "$town_entered", 1), #dckplmc
            (assign, "$g_mt_mode", tcm_disguised),
            (jump_to_menu, "mnu_sneak_into_town_suceeded"),
        (else_try),
            (jump_to_menu,"mnu_sneak_into_town_caught"),
        (try_end),
      ]),

      ("disguise_pilgrim",
      [
        (neq, "$sneaked_into_town", disguise_pilgrim),
      ], "Don the robes of a poor pilgrim.",
      [
        (assign, "$sneaked_into_town", disguise_pilgrim),
      ]),

      #SB : todo, add peasant woman variant
      ("disguise_farmer",
      [(store_and, ":disguise", "$temp_2", disguise_farmer),
       (eq, ":disguise", disguise_farmer),
       (neq, "$sneaked_into_town", disguise_farmer),],
      "Accept your fate as a downtrodden farmer.",
      [
        (assign, "$sneaked_into_town", disguise_farmer),
      ]),
      ("disguise_hunter",
      [(store_and, ":disguise", "$temp_2", disguise_hunter),
       (eq, ":disguise", disguise_hunter),
       (neq, "$sneaked_into_town", disguise_hunter),],
      "Disguise yourself as a skilled {huntsman/huntress}.",
      [
        (assign, "$sneaked_into_town", disguise_hunter),
      ]),
      ("disguise_guard",
      [(store_and, ":disguise", "$temp_2", disguise_guard),
       (eq, ":disguise", disguise_guard),
       (neq, "$sneaked_into_town", disguise_guard),],
      "Pass yourself off as a caravan guard.",
      [
        (assign, "$sneaked_into_town", disguise_guard),
      ]),
      ("disguise_merchant",
      [(store_and, ":disguise", "$temp_2", disguise_merchant),
       (eq, ":disguise", disguise_merchant),
       (neq, "$sneaked_into_town", disguise_merchant),],
      "Adopt the guise of a trader.",
      [
        (assign, "$sneaked_into_town", disguise_merchant),
      ]),
      ("disguise_bard",
      [(store_and, ":disguise", "$temp_2", disguise_bard),
       (eq, ":disguise", disguise_bard),
       (neq, "$sneaked_into_town", disguise_bard),],
      "Try your luck as a bard.",
      [
        (assign, "$sneaked_into_town", disguise_bard),
      ]),

      ("back",
      [],
      "Never mind...",
      [
        #put stuff back
        (set_show_messages, 0), #move all gold
        (call_script, "script_move_inventory_and_gold", "trp_random_town_sequence", "trp_player", -1),
        (set_show_messages, 1),

        (assign, "$sneaked_into_town", disguise_none),
        (jump_to_menu, "mnu_castle_outside"),
      ]),
    ]
  ),
]
