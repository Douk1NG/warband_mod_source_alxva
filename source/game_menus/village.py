# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

village_menus = [
  (
    "village",mnf_enable_hot_keys,
    "{s10} {s12}^{s11}^{s6}{s7}",
    "none",
    [
       (try_begin),
        (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
        (ge, ":center_lord", 0),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos1, 70),
        (position_set_y, pos1, 5),
        (position_set_z, pos1, 75),
        (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":center_lord", pos1),
        (try_end),
        (assign, "$current_town", "$g_encountered_party"),
        (call_script, "script_update_center_recon_notes", "$current_town"),

        (assign, "$g_defending_against_siege", 0), #required for bandit check
        (assign, "$g_battle_result", 0),
        (assign, "$qst_collect_taxes_currently_collecting", 0),
        (assign, "$qst_train_peasants_against_bandits_currently_training", 0),

        (try_begin),
          (gt, "$auto_enter_menu_in_center", 0),
          (jump_to_menu, "$auto_enter_menu_in_center"),
          (assign, "$auto_enter_menu_in_center", 0),
        (try_end),

        (try_begin),
          (neq, "$g_player_raiding_village",  "$current_town"),
          (assign, "$g_player_raiding_village", 0),
        (else_try),
          (jump_to_menu, "mnu_village_loot_continue"),
        (try_end),

        (try_begin),#Fix for collecting taxes
          (eq, "$g_town_visit_after_rest", 1),
          (assign, "$g_town_visit_after_rest", 0),
        (try_end),

        (str_store_party_name,s2, "$current_town"),
        (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
        (store_faction_of_party, ":center_faction", "$current_town"),
        (str_store_faction_name,s9,":center_faction"),
        (try_begin),
          (ge, ":center_lord", 0),
          (str_store_troop_name,s8,":center_lord"),
          (str_store_string,s7,"@{s8} of {s9}"),
        (try_end),

        (str_clear, s10),
        (str_clear, s12),

        (try_begin),
          (neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
          (str_store_string, s60, s2),

          (party_get_slot, ":prosperity", "$current_town", slot_town_prosperity),
		  (try_begin),
			(eq, "$cheat_mode", 1),
			(assign, reg4, ":prosperity",),
			(display_message, "@{!}Prosperity: {reg4}"),
		  (try_end),

		  #(val_add, ":prosperity", 5),
          (store_div, ":str_id", ":prosperity", 10),
		  (val_min, ":str_id", 9),
		  (val_add, ":str_id", "str_village_prosperity_0"),
          (str_store_string, s10, ":str_id"),


          (store_div, ":str_id", ":prosperity", 20),
		  (val_min, ":str_id", 4),
		  (try_begin),
			(is_between, "$current_town", "p_village_91", villages_end),
			(val_add, ":str_id", "str_oasis_village_alt_prosperity_0"),
		  (else_try),
			(val_add, ":str_id", "str_village_alt_prosperity_0"),
		  (try_end),

          (str_store_string, s12, ":str_id"),
        (try_end),

        (str_clear, s11),
        ##diplomacy start+
		(assign, ":save_reg0", reg0),#save variables
		(assign, ":save_reg4", reg4),
		(assign, reg0, 0),
		(assign, reg4, 0),
		(try_begin),#If there's a relation of some kind, write it to s11 (which we'll overwrite below)
			(lt, ":center_lord", 1),
		(else_try),
			#your relative
			(call_script, "script_troop_get_family_relation_to_troop", ":center_lord", "trp_player"),#outputs to s11, reg0, and reg4
			(ge, reg0, 1),#Fall through if this not a relative
		(else_try),
			#your current liege
			(eq, ":center_faction", "$players_kingdom"),
			(is_between, ":center_faction", kingdoms_begin, kingdoms_end),#include fac_player_supporters_faction for claimant quest
			(faction_slot_eq, ":center_faction", slot_faction_leader, ":center_lord"),
			(str_store_string, s11, "@liege"),
			(assign, reg0, 1),
		(else_try),
			#your former liege if you renounced a kingdom
			(eq, ":center_faction", "$players_oath_renounced_against_kingdom"),
			(is_between, ":center_faction", npc_kingdoms_begin, npc_kingdoms_end),
			(faction_slot_eq, ":center_faction", slot_faction_leader, ":center_lord"),
			(str_store_string, s11, "@former liege"),
			(assign, reg0, 1),
		(else_try),
			#stop here for lords you haven't met, or non-hero troops
			(this_or_next|neg|troop_is_hero, ":center_lord"),
			(troop_slot_eq, ":center_lord", slot_troop_met, 0),
		(else_try),
			#check for affiliates
			(call_script, "script_dplmc_is_affiliated_family_member", ":center_lord"),
			(ge, reg0, 1),
			(try_begin),
				(ge, "$g_encountered_party_relation", 0),#don't say "ally" when you might fight them, as that's confusing
				(str_store_string, s11, "str_dplmc_ally"),
			(else_try),
				(str_store_string, s11, "@affiliate"),
			(try_end),
		(else_try),
			#check for former companions
			(call_script, "script_troop_get_player_relation", ":center_lord"),
			(is_between, ":center_lord", companions_begin, companions_end),
			(neg|troop_slot_eq, ":center_lord", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
			(try_begin),
			   (ge, "$g_encountered_party_relation", 0),#don't say "ally" when you might fight them, as that's confusing
			   (ge, reg0, 50),
			   (str_store_string, s11, "str_dplmc_ally"),
			(else_try),
				(ge, "$g_encountered_party_relation", 0),
				(ge, reg0, 20),
				(str_store_string, s11, "str_dplmc_friend"),
			(else_try),
				(str_store_string, s11, "@former companion"),
			(try_end),
			(assign, reg0, 1),
		(else_try),
			#don't print "friend" if you might fight them
			(lt, "$g_encountered_party_relation", 0),
			(assign, reg0, 0),
		(else_try), #SB : local instead of reg
			#check for friends
            (call_script, "script_troop_get_player_relation", ":center_lord"),
			(store_div, ":relation", reg0, 50),#right now reg0 holds the relation with the player
			(gt, ":relation", 1),
			(str_store_string, s11, "str_dplmc_friend"),
            (assign, reg0, 1),
		(else_try),
			#check for marshall
			(eq, ":center_faction", "$players_kingdom"),
			(faction_slot_eq, ":center_faction", slot_faction_marshall, ":center_lord"),
			(str_store_string, s11, "@marshall"),
		(else_try),
			#check for vassal of player if nothing else to say
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":center_faction"),
			(val_add, reg0, 1),
			(val_sub, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(ge, reg0, 1),
			(str_store_string, s11, "@vassal"),
		(else_try),
			(assign, reg0, 0),
		(try_end),
		##diplomacy end+
        (try_begin),
          # (party_slot_eq, "$current_town", slot_village_state, svs_looted),
          # #SB : cancel string clear
          # (str_clear, s11),
        # (else_try),
          (eq, ":center_lord", "trp_player"),
          (str_store_string,s11,"@ This village and the surrounding lands belong to you."),
		##diplomacy start+ If reg0 > 0, a relation string has been written into s11
		(else_try),
		  (ge, reg0, 1),
		  (str_store_string,s11,"@ You remember that this village and the surrounding lands belong to your {s11} {s7}."),
		##diplomacy end+
        (else_try),
          (ge, ":center_lord", 0),
          (str_store_string,s11,"@ You remember that this village and the surrounding lands belong to {s7}."),
        (else_try),
          (str_store_string,s11,"@ These lands belong to no one."),
        (try_end),
		##diplomacy start+
		(assign, reg0, ":save_reg0"),#revert registers
		(assign, reg4, ":save_reg4"),
		##diplomacy end+

        (str_clear, s7),
        (try_begin),
          (neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
          (party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
          (call_script, "script_describe_center_relation_to_s3", ":center_relation"),
          (assign, reg9, ":center_relation"),
          (str_store_string, s7, "@{!} {s3} ({reg9})."),
        (try_end),
        (str_clear, s6),
        (try_begin),
          (party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
          (party_get_slot, ":bandit_troop", "$current_town", slot_village_infested_by_bandits),
          (store_character_level, ":player_level", "trp_player"),
          (val_min, ":player_level", 63),
          ## SB : adjust bandit levels to manageable levels, reinforcements based on party size - fuck off
          (store_add, "$qst_eliminate_bandits_infesting_village_num_bandits", ":player_level", 10),
          #(val_div, "$qst_eliminate_bandits_infesting_village_num_bandits", 2), literally for babies
          (faction_get_slot, ":limit", ":center_faction", dplmc_slot_faction_serfdom),
          #(options_get_campaign_ai, ":reduced"),
          #(val_mul, ":reduced", 3), #poor ai = more base bandits  terrible
          #(val_sub, ":reduced", ":limit"),
          (store_sub, ":limit", 6, ":limit"),
          (val_mul, ":limit", 2),
          (val_add, "$qst_eliminate_bandits_infesting_village_num_bandits", ":limit"),
          (val_mul, "$qst_eliminate_bandits_infesting_village_num_bandits", 120),
          (val_div, "$qst_eliminate_bandits_infesting_village_num_bandits", 100),
          (val_max, "$qst_eliminate_bandits_infesting_village_num_bandits", 10), #dckplmc - no less than 10 bandits

          # (party_get_num_companions, ":party_size", "$current_town"), #ideal size is 50
          (call_script, "script_party_count_fit_regulars", "$current_town"),
          (assign, ":party_size", reg0),
          (store_div, ":lower_size", ":party_size", 3), #about 2/3rd stay back
          (store_div, ":limit", ":center_relation", 5),
          (val_add, ":limit", 60),
          (store_random_in_range, "$qst_eliminate_bandits_infesting_village_num_villagers", ":lower_size", ":limit"),
          (val_min, "$qst_eliminate_bandits_infesting_village_num_villagers", ":party_size"),
          (assign, reg8, "$qst_eliminate_bandits_infesting_village_num_bandits"),
          (str_store_troop_name_by_count, s35, ":bandit_troop", "$qst_eliminate_bandits_infesting_village_num_bandits"),
          (str_store_string, s6, "@ The village is infested by {reg8} {s35}."),

          (assign, "$g_enemy_party", -1), #new, no known enemy party while saving village from bandits
          (assign, "$g_ally_party", -1), #new, no known enemy party while saving village from bandits

          ## SB : adjust meshes as well
          (try_begin),
            (eq, ":bandit_troop", "trp_forest_bandit"),
            (set_background_mesh, "mesh_pic_forest_bandits"),
          (else_try),
            (this_or_next|eq, ":bandit_troop", "trp_steppe_bandit"),
            (eq, ":bandit_troop", "trp_desert_bandit"),
            (set_background_mesh, "mesh_pic_steppe_bandits"),
          (else_try),
            (this_or_next|eq, ":bandit_troop", "trp_steppe_bandit"),
            (eq, ":bandit_troop", "trp_taiga_bandit"),
            (set_background_mesh, "mesh_pic_mountain_bandits"),
          (else_try),
            (eq, ":bandit_troop", "trp_sea_raider"),
            (set_background_mesh, "mesh_pic_sea_raiders"),
          (else_try),
            (store_faction_of_troop, ":faction_no", ":bandit_troop"),
            (this_or_next|is_between, ":faction_no", kingdoms_begin, kingdoms_end),
            (eq, ":faction_no", "fac_deserters"),
            (set_background_mesh, "mesh_pic_deserters"),
          (else_try),
           ##diplmacy begin
            (eq, ":bandit_troop", "trp_peasant_woman"),
            #SB : preview actual amount of mercs
            (party_get_num_companions, reg8, "$current_town"),
            (party_count_members_of_type, ":amount", "$current_town", "trp_farmer"),
            (val_sub, reg8, ":amount"),
            (party_count_members_of_type, ":amount", "$current_town", "trp_peasant_woman"),
            (val_sub, reg8, ":amount"),
            (str_store_string, s6, "@ The peasants {reg8?hired {reg8} mercenaries and :}are rebelling against you."),
            (set_background_mesh, "mesh_pic_villageriot"),
          (else_try),
           ##diplomacy end
            (set_background_mesh, "mesh_pic_bandits"),
          (try_end),
        (else_try),
          (this_or_next|party_slot_eq, "$current_town", slot_village_state, svs_looted),
          (party_slot_eq, "$current_town", slot_village_state, svs_deserted),
          (str_store_string, s6, "@ The village has been looted. A handful of souls scatter as you pass through the burnt out houses."),
          (try_begin),
            (neq, "$g_player_raid_complete", 1),
            (play_track, "track_empty_village", 1),
          (try_end),
          (set_background_mesh, "mesh_pic_looted_village"),
        (else_try),
          (party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
          (str_store_string, s6, "@ The village is being raided."),
        (else_try), #SB : script call
          (call_script, "script_set_town_picture"),
        (try_end),

        (try_begin),
          (eq, "$g_player_raid_complete", 1),
          (try_begin), #SB : branching menu
            (party_slot_eq, "$current_town", slot_village_state, svs_looted),
            (jump_to_menu, "mnu_village_loot_complete"),
          (else_try), #stay on this menu
            (party_slot_eq, "$current_town", slot_village_state, svs_deserted),
            (jump_to_menu, "mnu_village_enslave_complete"),
          (try_end),
          (assign, "$g_player_raid_complete", 0),
          #SB : reinforce quest state
          (try_begin),
            (check_quest_active, "qst_hunt_down_fugitive"),
            (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
            (quest_set_slot, "qst_hunt_down_fugitive", slot_quest_current_state, 3),
          (try_end),
        (else_try),
          (party_get_slot, ":raider_party", "$current_town", slot_village_raided_by),
          (gt, ":raider_party", 0),
        # Process here...
        (try_end),

        (try_begin),
          (eq,"$g_leave_town",1),
          (assign,"$g_leave_town",0),
          (change_screen_return),
        (try_end),

        (try_begin),
          (store_time_of_day, ":cur_hour"),
          (ge, ":cur_hour", 5),
          (lt, ":cur_hour", 21),
          (assign, "$town_nighttime", 0),
        (else_try),
          (assign, "$town_nighttime", 1),
        (try_end),
    ],
    [
      ("village_manage",
      [
        (call_script, "script_cf_village_normal_cond", "$current_town"), #SB : script condition
        (party_slot_eq, "$current_town", slot_town_lord, "trp_player")
        ]
       ,"Manage this village.",
       [
           (assign, "$g_next_menu", "mnu_village"),
           (jump_to_menu, "mnu_center_manage"),
        ]),

     ("recruit_volunteers_dickplo",
     [
     (call_script, "script_cf_village_recruit_volunteers_cond"),
     ],
     "Recruit Volunteers.",
     [
     (jump_to_menu, "mnu_recruit_volunteers_dickplo_main")
     ]),
     # ("recruit_volunteers",
     # [
     #    (call_script, "script_cf_village_recruit_volunteers_cond"),
     #  ]
     #  ,"Recruit Volunteers.",
     #  [
     #    (try_begin),
     # (call_script, "script_cf_enter_center_location_bandit_check"),
     #     (else_try),
     #       (jump_to_menu, "mnu_recruit_volunteers"),
     #     (try_end),
     #    ]),
      ("village_center",[(call_script, "script_cf_village_normal_cond", "$current_town"), #SB : script condition
       ]
       ,"Go to the village center.",
       [
          (try_begin),
            (call_script, "script_cf_enter_center_location_bandit_check"),
          (else_try),
            (party_get_slot, ":village_scene", "$current_town", slot_castle_exterior),
            (modify_visitors_at_site,":village_scene"),
            (reset_visitors),
            (party_get_slot, ":village_elder_troop", "$current_town",slot_town_elder),
            (set_visitor, 11, ":village_elder_troop"),
            ##diplomacy begin
            (try_begin),
              (gt, "$g_player_chamberlain", 0),
              (call_script, "script_dplmc_appoint_chamberlain"),  #fix for wrong troops after update
              (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
              (eq, ":town_lord", "trp_player"),
              (set_visitor, 9, "$g_player_chamberlain"),
            (try_end),
            ##diplomacy end


           (call_script, "script_init_town_walkers"),

           (try_begin),
             (check_quest_active, "qst_hunt_down_fugitive"),
             (neg|is_currently_night),
             (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
             (neg|check_quest_concluded, "qst_hunt_down_fugitive"), #SB : other condition
             (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
             (neg|check_quest_failed, "qst_hunt_down_fugitive"),
             (set_visitor, 45, "trp_fugitive"),
           (try_end),

           (set_jump_mission,"mt_village_center"),
           (jump_to_scene,":village_scene"),
           (change_screen_mission),
         (try_end),
        ],"Door to the village center."),
       ##diplomacy begin
      ("dplmc_village_elder_meeting",[
         (call_script, "script_cf_village_normal_cond", "$current_town"), #SB : conditional check
	   ##diplomacy start+
		#rubik had a good idea: only enable this after having met the village elder
		(party_get_slot, ":village_elder_troop", "$current_town",slot_town_elder),
		(gt, ":village_elder_troop", 0),
		(this_or_next|eq, "$cheat_mode", 0),#Always can jump to village elder in cheat mode, modified by Lily to always meat regardless of cheat mode.
		(this_or_next|eq, "$players_kingdom", "$g_encountered_party_faction"), #allow when member
        (troop_slot_ge,":village_elder_troop", slot_troop_met, 1),
		##diplomacy end+
       ]
       ,"Meet the Village Elder.",
       [
         (try_begin),
           (call_script, "script_cf_enter_center_location_bandit_check"),
         (else_try),
           (party_get_slot, ":village_scene", "$current_town", slot_castle_exterior),
           (modify_visitors_at_site,":village_scene"),
           (reset_visitors),
           (party_get_slot, ":village_elder_troop", "$current_town",slot_town_elder),
           (set_visitor, 11, ":village_elder_troop"),
           (try_begin), #SB : supporting village_elder_found_chamberlain dialog option
              (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
              (eq, "$g_player_chamberlain", "trp_dplmc_chamberlain"),
              (set_visitor, 9, "$g_player_chamberlain"),
           (try_end),

           (set_jump_mission,"mt_village_center"),
           (jump_to_scene,":village_scene"),
           (change_screen_map_conversation, ":village_elder_troop"),
         (try_end),
        ]),
      ##diplomacy end
	##diplomacy start+
	#I commented this out so that it doens't duplicate in the menu ~ Lily
#    ("dplmc_village_elder_meeting_denied",
#	[
#		#Only show this when the player would get the rest of the village menus
#        (call_script, "script_cf_village_normal_cond", "$current_town"), #SB : script condition
#	    #There is a valid village elder, and you haven't met him,
#		#and there isn't another condition that enables the jump.
#		(party_get_slot, ":village_elder_troop", "$current_town",slot_town_elder),
#		(gt, ":village_elder_troop", 0),
#		(eq, "$cheat_mode", 0),
#		(troop_slot_eq, ":village_elder_troop", slot_troop_met, 0),
#		(disable_menu_option),
#		],
#       "You have not met the village elder yet.",
#       [
#     ]),
	 ##diplomacy end+
      ("village_buy_food",[(party_slot_eq, "$current_town", slot_village_state, svs_normal),
                           (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
                           ],"Buy supplies from the peasants.",
       [
         (try_begin),
           (call_script, "script_cf_enter_center_location_bandit_check"),
         (else_try),
           (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),

      #(try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
        #(store_sub, ":cur_good_price_slot", ":cur_goods", trade_goods_begin),
        #(val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
		#(party_get_slot, ":cur_price", "$current_town", ":cur_good_price_slot"),
	    #(call_script, "script_center_get_production", "$current_town", ":cur_goods"),
        #(assign, reg13, reg0),
	    #(call_script, "script_center_get_consumption", "$current_town", ":cur_goods"),
        #(str_store_party_name, s1, "$current_town"),
        #(str_store_item_name, s2, ":cur_goods"),
		#(assign, reg16, ":cur_price"),
        #(display_log_message, "@DEBUG:{s1}-{s2}, prd: {reg13}, con: {reg0}, raw: {reg1}, cns: {reg2}, fee: {reg16}"),
	  #(try_end),

           (change_screen_trade, ":merchant_troop"),
         (try_end),
         ]),
##diplomacy start+
#Import rubik's Auto-Sell options from Custom Commander
      ("dplmc_village_auto_sell",
        [
        (party_slot_eq, "$current_town", slot_village_state, svs_normal),
        (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
        (party_get_slot, ":village_elder_troop", "$current_town", slot_town_elder),
        (ge, ":village_elder_troop", 0),
        ],
       "Sell items automatically.",
       [
          (assign, "$g_next_menu", "mnu_village"),
          (jump_to_menu,"mnu_dplmc_trade_auto_sell_begin"),
        ]),

      ("dplmc_village_auto_buy_food",
        [
        (party_slot_eq, "$current_town", slot_village_state, svs_normal),
        (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
        (party_get_slot, ":village_elder_troop", "$current_town", slot_town_elder),
        (ge, ":village_elder_troop", 0),
        ],
       "Buy food automatically.",
       [
          (assign, "$g_next_menu", "mnu_village"),
          (jump_to_menu,"mnu_dplmc_trade_auto_buy_food_begin"),
        ]),
##diplomacy end+
      ("village_attack_bandits",[
        (party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
        ##diplomacy begin
        (neg|party_slot_eq, "$current_town", slot_village_infested_by_bandits, "trp_peasant_woman"),
        ##diplmacy end
        ],
       "Attack the bandits.",
       [(party_get_slot, ":bandit_troop", "$current_town", slot_village_infested_by_bandits),
        (party_get_slot, ":scene_to_use", "$current_town", slot_castle_exterior),
        (modify_visitors_at_site,":scene_to_use"),
        (reset_visitors),
        (set_visitors, 0, ":bandit_troop", "$qst_eliminate_bandits_infesting_village_num_bandits"),
        (set_visitors, 2, "trp_farmer", "$qst_eliminate_bandits_infesting_village_num_villagers"),
        (set_party_battle_mode),
        (set_battle_advantage, 0),
        (assign, "$g_battle_result", 0),
        (set_jump_mission,"mt_village_attack_bandits"),
        (jump_to_scene, ":scene_to_use"),
        (assign, "$g_next_menu", "mnu_village_infest_bandits_result"),
        (jump_to_menu, "mnu_battle_debrief"),
        (assign, "$g_mt_mode", vba_normal),
        (change_screen_mission),
        ]),

      ("village_wait",
       [(party_slot_eq, "$current_town", slot_center_has_manor, 1),
        (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
        ],
         "Wait here for some time.",
         [
           (assign,"$auto_enter_town","$current_town"),
           (assign, "$g_last_rest_center", "$current_town"),

           (try_begin),
             (party_is_active, "p_main_party"),
             (party_get_current_terrain, ":cur_terrain", "p_main_party"),
             (try_begin),
               (eq, ":cur_terrain", rt_desert),
               (unlock_achievement, ACHIEVEMENT_SARRANIDIAN_NIGHTS),
             (try_end),
           (try_end),

           (rest_for_hours_interactive, 24 * 7, 5, 1), #rest while attackable

           (change_screen_return),
          ]),

       ##diplomacy begin
      ("dplmc_village_counter_insurgency",[
        (party_slot_eq, "$current_town", slot_village_infested_by_bandits, "trp_peasant_woman"),
        ],
       "Counter the insurgency.",
       [
          (store_random_in_range, ":enmity", -10, -5),
          (call_script, "script_change_player_relation_with_center", "$current_town", ":enmity"),
          (call_script, "script_calculate_battle_advantage"),
          (set_battle_advantage, reg0),
          (set_party_battle_mode),
          (assign, "$g_battle_result", 0),
          (assign, "$g_village_raid_evil", 1), #check
          (set_jump_mission,"mt_village_raid"),
          (party_get_slot, ":scene_to_use", "$current_town", slot_castle_exterior),
          (jump_to_scene, ":scene_to_use"),
          (assign, "$g_next_menu", "mnu_dplmc_village_riot_result"),

          # (call_script, "script_objectionable_action", tmt_humanitarian, "str_loot_village"),
          #SB : more appropriate message for tax rebels
          (call_script, "script_objectionable_action", tmt_humanitarian, "str_repress_farmers"),
          (jump_to_menu, "mnu_battle_debrief"),
          (change_screen_mission),
        ]),

      ("dplmc_village_negotiate",[
        (party_slot_eq, "$current_town", slot_village_infested_by_bandits, "trp_peasant_woman"),
        ],
       "Begin negotiations.",
       [
          (jump_to_menu, "mnu_dplmc_riot_negotiate"),
        ]),
        ##diplomacy end

      ("collect_taxes_qst",[(party_slot_eq, "$current_town", slot_village_state, svs_normal),
                            (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
                            (check_quest_active, "qst_collect_taxes"),
                            (quest_get_slot, ":quest_giver_troop", "qst_collect_taxes", slot_quest_giver_troop),
                            (quest_slot_eq, "qst_collect_taxes", slot_quest_target_center, "$current_town"),
                            (neg|quest_slot_eq, "qst_collect_taxes", slot_quest_current_state, 4),
                            (str_store_troop_name, s1, ":quest_giver_troop"),
                            (quest_get_slot, reg5, "qst_collect_taxes", slot_quest_current_state),
                            ], "{reg5?Continue collecting taxes:Collect taxes} due to {s1}.",
       [(jump_to_menu, "mnu_collect_taxes"),]),

      ("train_peasants_against_bandits_qst",
       [
         (party_slot_eq, "$current_town", slot_village_state, svs_normal),
         (check_quest_active, "qst_train_peasants_against_bandits"),
         (neg|check_quest_concluded, "qst_train_peasants_against_bandits"),
         (quest_slot_eq, "qst_train_peasants_against_bandits", slot_quest_target_center, "$current_town"),
         ], "Train the peasants.",
       [(jump_to_menu, "mnu_train_peasants_against_bandits"),]),

      ("village_hostile_action",[(party_slot_eq, "$current_town", slot_village_state, svs_normal),
                                 (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
                                 (party_slot_ge, "$current_town", slot_center_player_relation, -1), #relationship check, non-negative
                                 (check_quest_active, "qst_hunt_down_fugitive"),
                                 (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
                                 (neg|check_quest_concluded, "qst_hunt_down_fugitive"), #SB : other condition
                                 (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
                                 (neg|check_quest_failed, "qst_hunt_down_fugitive"),
                                 (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
                                 (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
								 ], "Demand to meet the family of {s50}.",
       [
       (call_script, "script_get_max_skill_of_player_party", "skl_persuasion"),
       (store_random_in_range, ":random_no", reg0, 100),
       #persuasion instead of straight out murdering everyone
       (call_script, "script_party_count_members_with_full_health","p_main_party"),
       (assign, ":player_party_size", reg0),
       (call_script, "script_party_count_members_with_full_health","$current_town"),
       (store_mul, ":villagers_party_size", reg0, 2), #twice the effective size
       (try_begin),
         (this_or_next|gt, ":random_no", 40),
         (gt, ":player_party_size", ":villagers_party_size"),
         (jump_to_menu, "mnu_village_hunt_down_fugitive_persuaded"),
       (else_try),
         (jump_to_menu,"mnu_village_start_attack"),
       (try_end),
           ]),

      ("village_hostile_action",[(party_slot_eq, "$current_town", slot_village_state, svs_normal),
                                 (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
								 (neq, "$players_kingdom", "$g_encountered_party_faction"),
								 ], "Take a hostile action.",
       [(jump_to_menu,"mnu_village_hostile_action"),
           ]),

      # ("village_reports",[(eq, "$cheat_mode", 1),], "{!}CHEAT! Show reports.",
       # [(jump_to_menu,"mnu_center_reports"),
           # ]),
      ("village_leave",[],"Leave...",[(change_screen_return,0),
	  ##diplomacy start+
	  ##Importing auto-purchase of food from rubik's Custom Commander
	  (try_begin),
		 (party_slot_eq, "$current_town", slot_village_state, svs_normal),
		 (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
		 (party_get_slot, ":merchant_troop", "$current_town",slot_town_elder),
		 (gt, ":merchant_troop", 0),
		 (call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
		 (try_begin),
			(eq, "$g_dplmc_buy_food_when_leaving", 1),
			(call_script, "script_dplmc_auto_buy_food", "trp_player", ":merchant_troop"),
		 (try_end),
		 (try_begin),
			(eq, "$g_dplmc_sell_items_when_leaving", 1),
			(call_script, "script_dplmc_auto_sell", "trp_player", ":merchant_troop", "$g_dplmc_auto_sell_price_limit", all_items_begin, all_items_end, 4),
		 (try_end),
      #Automatically buy and sell with village elder, if enabled
      (try_begin),
        (eq, "$g_auto_trade_items_when_leaving", 1),
        #Villages tend to not have much coin, so we buy first to make sure they can afford the player's goods
        (call_script, "script_auto_trade_buy_from_merchant", ":merchant_troop"),
        (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
      (try_end),
      #AutoTrade End
	  (try_end),
	  ##diplomacy end+
        
	  ]),
      #SB : consolidated cheats
      ("village_cheat", [(ge, "$cheat_mode", 1),],
      "Use cheats.",
      [(jump_to_menu, "mnu_town_cheats"),
      ]),
    ],
  ),
  (
    "village_hostile_action",0,
    "What action do you have in mind?",
    "none",
    [],
    [
      ("village_take_food",[
          (party_slot_eq, "$current_town", slot_village_state, svs_normal),
          (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
          (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
          #SB : loop break
          (assign, ":town_stores_not_empty", max_inventory_items + num_equipment_kinds),
          (try_for_range, ":slot_no", num_equipment_kinds, ":town_stores_not_empty"),
            (troop_get_inventory_slot, ":slot_item", ":merchant_troop", ":slot_no"),
            (ge, ":slot_item", 0),
            (assign, ":town_stores_not_empty", -1),
          (try_end),
          (eq, ":town_stores_not_empty", -1),
          ],"Force the peasants to give you supplies.",
       [
           (jump_to_menu, "mnu_village_take_food_confirm")
        ]),
      ("village_steal_cattle",
       [
          (party_slot_eq, "$current_town", slot_village_state, svs_normal),
          (party_slot_eq, "$current_town", slot_village_player_can_not_steal_cattle, 0),
          (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
          (party_get_slot, ":num_cattle", "$current_town", slot_village_number_of_cattle),
          (neg|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
          (gt, ":num_cattle", 0),
          ],"Steal cattle.",
       [
           (jump_to_menu, "mnu_village_steal_cattle_confirm")
        ]),
      ("village_loot",[(party_slot_eq, "$current_town", slot_village_state, svs_normal),
                       (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
                       (store_faction_of_party, ":center_faction", "$current_town"),
                       (store_relation, ":reln", "fac_player_supporters_faction", ":center_faction"),
                       (lt, ":reln", 0),
                       ],
       "Loot and burn this village.",
       [
#           (party_clear, "$current_town"),
#           (party_add_template, "$current_town", "pt_villagers_in_raid"),
           (jump_to_menu, "mnu_village_start_attack"),
           ]),
      ("forget_it",[],
      "Forget it.",[(jump_to_menu,"mnu_village")]),
    ],
  ),
#Dickplomacy Volunteer menu
(
  "recruit_volunteers_dickplo_main",0,
  "How would you like to recruit volunteers?",
  "none",
  [
  #Floris tableau_troop_note_mesh for menus
         (try_begin),
          (party_get_slot, ":center_lord", "$current_town", slot_town_lord),
          (ge, ":center_lord", 0),
          (set_fixed_point_multiplier, 100),
          (position_set_x, pos1, 70),
          (position_set_y, pos1, 5),
          (position_set_z, pos1, 75),
          (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":center_lord", pos1),
          (try_end),
  #End tableau mesh
  ],
  [
      #Force Recruit by Topper, heavily moddified by LilyModzStuff
      ("forced_recruits",
      [
        # Standard check
        (neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
        (neg|party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
        (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
        # Check if party have enough free slots
        (assign, ":mod_amount", 7),
        (party_get_free_companions_capacity, ":mod_capacity", "p_main_party"),
        (ge, ":mod_capacity", ":mod_amount"),
       ]
       ,"Force villagers to join your army.",
       [
        (assign, ":mod_amount", 7),
        #Center relation check
        (try_begin),
        (assign, ":mod_rel_change", -15),
        (party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
        (ge, ":mod_rel_change", ":center_relation"),
        (display_message, "@The villagers have decided to revolt!"),
        (jump_to_menu, "mnu_village_start_attack"),
        (else_try),
        (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
        (val_min, ":mod_amount", ":free_capacity"),
        (party_get_slot, ":mod_troop", "$current_town", slot_center_volunteer_troop_type),
        (party_add_members, "p_main_party", ":mod_troop", 7), #the original script used 30 but that was way to high.
        # Change relation and subtract honor, and companion objections
        (call_script, "script_change_player_relation_with_center", "$current_town", -15),
        (call_script, "script_change_player_honor", -3), #Should be an honor loss as well
        (display_message, "@You have forced the villigers to join your army by force."),
        (call_script, "script_objectionable_action", tmt_humanitarian, "str_force_into_party"), #humanitarian don't like it when you steal.
        (try_end),
        ]),
        #End force recruit
              ("recruit_normal_volunteers",
               [
               ],
               "Recruit volunteers.",
               [
               (jump_to_menu,"mnu_recruit_volunteers"),
              ]),
        ("recruit_normal_volunteers",
        [
        ],
        "Return to village.",
        [
        (jump_to_menu,"mnu_village"),
    ]),
  ]),

#End volunteer menu,
  (
    "recruit_volunteers",0,
    "{s18}",
    "none",
    [
		 (start_presentation, "prsnt_recruit_volunteers"),
    ],
    [


      ("continue",
      [
        (eq, reg7, 0),
        (eq, reg5, 0),
      ], #noone willing to join
      "Continue...",
      [
        (party_set_slot, "$current_town", slot_center_volunteer_troop_amount, -1),
        (jump_to_menu,"mnu_village"),
      ]),

      ("recruit_them",
      [
        (eq, reg7, 0),
        (gt, reg5, 0),
      ],
      "Recruit them ({reg6} denars).",
      [
        (call_script, "script_village_recruit_volunteers_recruit"),

        (jump_to_menu,"mnu_village"),
      ]),

      #SB : disable_menu_option
      ("continue_not_enough_gold",
      [
        (eq, reg7, 1),
        (disable_menu_option),
      ],
      "I don't have enough money...",
      [
        (jump_to_menu,"mnu_village"),
      ]),

      ("forget_it",
      [
      #SB : conditions now not applied
        # (eq, reg7, 0),
        # (gt, reg5, 0),
      ],
      "Forget it.",
      [
        (jump_to_menu,"mnu_village"),
      ]),
    ],
  ),
  (
    "village_hunt_down_fugitive_defeated",0,
    "A heavy blow from the fugitive sends you to the ground, and your vision spins and goes dark.\
 Time passes. When you open your eyes again you find yourself battered and bloody,\
 but luckily none of the wounds appear to be lethal.",
    "none",
    [
      (call_script, "script_fail_quest", "qst_hunt_down_fugitive"),
    ],
    [
      ("continue",[],"Continue...",[(jump_to_menu, "mnu_village"),
      #SB : renown loss for single target
      (call_script, "script_change_troop_renown", "trp_player", -2),
      # (party_remove_members, "$current_town", "trp_fugitive", 1),
      ]),
    ],
  ),
  (
    "village_hunt_down_fugitive_persuaded",0,
 "As the party member with the highest persuasion, {reg3?you:{s3}} managed to cajole the location of {s50} from his tight-lipped relatives. Backed with superior force of arms, your just argument seemed to take effect and the villagers grudgingly participate in the manhunt for the fugitive.\
 {reg4?But word of you arrival has reached the fugitive and he appears to have taken his own life:Within the hour, you've secured the fugitive on behalf of {s4}}.",
    "none",
    [   (call_script, "script_get_max_skill_of_player_party", "skl_persuasion"),
        (assign, ":max_skill_owner", reg1),
        (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
        (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),

         #SB : tableau at bottom
         (try_begin),
           (eq, ":max_skill_owner", "trp_player"),
           (assign, reg3, 1),
         (else_try),
           (assign, reg3, 0),
           (str_store_troop_name, s3, ":max_skill_owner"),
           (call_script, "script_change_troop_renown", ":max_skill_owner", dplmc_companion_skill_renown),
         (try_end),

        (set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 70),
        (position_set_y, pos0, 5),
        (position_set_z, pos0, 75),
        (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":max_skill_owner", pos0),
        (store_random_in_range, reg4, 0, 2), #TODO add some conditions, renown, time of day, etc
        (try_begin),
          (eq, reg4, 0),
          (party_force_add_prisoners, "p_main_party", "trp_fugitive", 1),
          (quest_get_slot, ":quest_giver_troop", "qst_hunt_down_fugitive", slot_quest_giver_troop),
          (str_store_troop_name, s4, ":quest_giver_troop"),
          (quest_set_slot, "qst_hunt_down_fugitive", slot_quest_current_state, 2),
        (else_try), #killed, player can claim credit
          (quest_set_slot, "qst_hunt_down_fugitive", slot_quest_current_state, 1),
        (try_end),
    ],

    [
      ("continue",[],"Continue...",[
        (call_script, "script_succeed_quest", "qst_hunt_down_fugitive"),
        (jump_to_menu, "mnu_village"),

      ]),
    ],
  ),
  (
    "village_infest_bandits_result",mnf_scale_picture,
    "{s9}",
    "none",
    [(try_begin),
       (eq, "$g_battle_result", 1),
       (jump_to_menu, "mnu_village_infestation_removed"),
     (else_try),
       (str_store_string, s9, "@Try as you might, you could not defeat the bandits.\
 Infuriated, they raze the village to the ground to punish the peasants,\
 and then leave the burning wasteland behind to find greener pastures to plunder."),
       (set_background_mesh, "mesh_pic_looted_village"),
     (try_end),
    ],
    [
      ("continue",[],"Continue...",
       [(party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
        (call_script, "script_village_set_state",  "$current_town", svs_looted),
        (party_set_slot, "$current_town", slot_village_raid_progress, 0),
        (party_set_slot, "$current_town", slot_village_recover_progress, 0),
        (try_begin),
          (check_quest_active, "qst_eliminate_bandits_infesting_village"),
          (quest_slot_eq, "qst_eliminate_bandits_infesting_village", slot_quest_target_center, "$g_encountered_party"),
          (call_script, "script_change_player_relation_with_center", "$g_encountered_party", -5),
          (call_script, "script_fail_quest", "qst_eliminate_bandits_infesting_village"),
          (call_script, "script_end_quest", "qst_eliminate_bandits_infesting_village"),
        (else_try),
          (check_quest_active, "qst_deal_with_bandits_at_lords_village"),
          (quest_slot_eq, "qst_deal_with_bandits_at_lords_village", slot_quest_target_center, "$g_encountered_party"),
          (call_script, "script_change_player_relation_with_center", "$g_encountered_party", -4),
          (call_script, "script_fail_quest", "qst_deal_with_bandits_at_lords_village"),
          (call_script, "script_end_quest", "qst_deal_with_bandits_at_lords_village"),
        (else_try),
          (call_script, "script_change_player_relation_with_center", "$g_encountered_party", -3),
        (try_end),
        (jump_to_menu, "mnu_village"),]),
    ],
  ),
  (
    "village_infestation_removed",mnf_disable_all_keys,
    "In a battle worthy of song, you and your men drive the bandits out of the village, making it safe once more.\
 The villagers have little left in the way of wealth after their ordeal, but they offer you {reg10?all they can find:a few heads of cattle}.",
    "none",
    [(party_get_slot, ":bandit_troop", "$g_encountered_party", slot_village_infested_by_bandits),
     (party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
     (party_clear, "p_temp_party"),
     (party_add_members, "p_temp_party", ":bandit_troop", "$qst_eliminate_bandits_infesting_village_num_bandits"),
     #SB : tweaked player contribution by whether village is the same faction
     (try_begin),
       (eq, "$players_kingdom", "$g_encountered_party_faction"),
       (assign, "$g_strength_contribution_of_player", 65),
     (else_try),
       (assign, "$g_strength_contribution_of_player", 50),
     (try_end),
     (call_script, "script_party_give_xp_and_gold", "p_temp_party"),
     (try_begin),
       (check_quest_active, "qst_eliminate_bandits_infesting_village"),
       (quest_slot_eq, "qst_eliminate_bandits_infesting_village", slot_quest_target_center, "$g_encountered_party"),
       (call_script, "script_end_quest", "qst_eliminate_bandits_infesting_village"),
       #Add quest reward
       (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 5),
     (else_try),
       (check_quest_active, "qst_deal_with_bandits_at_lords_village"),
       (quest_slot_eq, "qst_deal_with_bandits_at_lords_village", slot_quest_target_center, "$g_encountered_party"),
       (call_script, "script_succeed_quest", "qst_deal_with_bandits_at_lords_village"),
       (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 3),
     (else_try),
     #Add normal reward
       (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 4),
     (try_end),

     (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
     #SB : calculate amount of merchandise remaining
     (assign, ":num_items", 0),
     (try_for_range, ":slot_no", num_equipment_kinds, max_inventory_items + num_equipment_kinds),
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", 70),
        (troop_set_inventory_slot, ":merchant_troop", ":slot_no", -1),
     (else_try),
        (troop_get_inventory_slot, ":item_no", ":merchant_troop", ":slot_no"),
        (gt, ":item_no", 0),
        (item_get_type, ":itp", ":item_no"),
        (eq, ":itp", itp_type_goods),
        (val_add, ":num_items", 1),
     (try_end),
     #SB : check before we disappoint the player
       # (store_free_inventory_capacity, ":capacity", ":merchant_troop"),
       # (eq, ":capacity", max_inventory_items),
     (assign, reg10, ":num_items"),
     #SB : background mesh
     #(set_background_mesh, "mesh_pic_mb_warrior_3"), #dckplmc - obscures text
    ],
    [
    #SB : add other option
      # ("village_bandits_defeated_accept_cattle",[(eq, reg10, 1)],"Looks like meat's back on the menu.",[(jump_to_menu, "mnu_village"),
                                                                         # (call_script, "script_create_cattle_herd", "$current_town", 1),
                                                                       # ]),
      ("village_bandits_defeated_accept",[],"Take it as your just due.",[(jump_to_menu, "mnu_village"),
                                                                         (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
                                                                         (troop_sort_inventory, ":merchant_troop"),
                                                                         (try_begin),
                                                                           (gt, reg10, 0),
                                                                           (change_screen_loot, ":merchant_troop"),
                                                                         (else_try), #arbitrary amount
                                                                           (store_random_in_range, reg10, 2, 5),
                                                                           (call_script, "script_create_cattle_herd", "$current_town", reg10),
                                                                         (try_end),
                                                                       ]),

      ("village_bandits_defeated_cont",[],  "Refuse, stating that they need these items more than you do.",
      [
        (call_script, "script_change_player_relation_with_center", "$g_encountered_party", 3),
        (call_script, "script_change_player_honor", 1),
        (jump_to_menu, "mnu_village")]),
    ],
  ),
  (
    "village_steal_cattle",mnf_disable_all_keys,
    "{s1}",
    "none",
    [
      (call_script, "script_calculate_amount_of_cattle_can_be_stolen", "$current_town"),
      (assign, ":max_value", reg0),
      (val_add, ":max_value", 1),
      (store_random_in_range, ":random_value", 0, ":max_value"),
      (party_set_slot, "$current_town", slot_village_player_can_not_steal_cattle, 1),
      (party_get_slot, ":lord", "$current_town", slot_town_lord),
      (try_begin),
        (le, ":random_value", 0),
        (call_script, "script_change_player_relation_with_center", "$current_town", -3),
        (str_store_string, s1, "@You fail to steal any cattle."),
      (else_try),
        (assign, reg17, ":random_value"),
        (store_sub, reg12, ":random_value", 1),
        (try_begin),
          (gt, ":lord", 0),
          (call_script, "script_change_player_relation_with_troop", ":lord", -3),
          (call_script, "script_add_log_entry", logent_player_stole_cattles_from_village, "trp_player",  "$current_town", ":lord", "$g_encountered_party_faction"),
        (try_end),
        (call_script, "script_change_player_relation_with_center", "$current_town", -5),
        (str_store_string, s1, "@You drive away {reg17} {reg12?heads:head} of cattle from the village's herd."),

        (try_begin),
          (eq, ":random_value", 3),
          (unlock_achievement, ACHIEVEMENT_GOT_MILK),
        (try_end),

        (call_script, "script_create_cattle_herd", "$current_town", ":random_value"),
        (party_get_slot, ":num_cattle", "$current_town", slot_village_number_of_cattle),
        (val_sub, ":num_cattle", ":random_value"),
        (party_set_slot, "$current_town", slot_village_number_of_cattle, ":num_cattle"),

        #SB : add lesser renown bonus
        (try_begin),
          (call_script, "script_get_max_skill_of_player_party", "skl_looting"),
          (neq, reg1, "trp_player"),
          (call_script, "script_change_troop_renown", reg1, dplmc_companion_skill_renown / 2),
        (try_end),
      (try_end),
    ],
    [
      ("continue",[],"Continue...",
       [
         (change_screen_return),
         ]),
    ],
  ),


   (
    "village_take_food_confirm",0,
    "It will be difficult to force and threaten the peasants into giving their precious supplies. You think you will need at least one hour.",
    #TODO: mention looting skill?
    "none",
    [],
    [
      ("village_take_food_confirm",[],"Go ahead.",
       [
         (rest_for_hours_interactive, 1, 5, 0), #rest while not attackable
         (assign, "$auto_enter_town", "$current_town"),
         (assign, "$g_town_visit_after_rest", 1),
         (assign, "$auto_enter_menu_in_center", "mnu_village_take_food"),
         (change_screen_return),
         ]),
      ("forget_it",[],"Forget it.",[(jump_to_menu, "mnu_village_hostile_action")]),
    ],
  ),
  (
    "village_take_food",0,
    "The villagers grudgingly bring out what they have for you.",
    "none",
    [
       (call_script, "script_party_count_members_with_full_health","p_main_party"),
       (assign, ":player_party_size", reg0),
       (call_script, "script_party_count_members_with_full_health","$current_town"),
       (assign, ":villagers_party_size", reg0),
       (try_begin),
         (lt, ":player_party_size", 6),
         (ge, ":villagers_party_size", 40),
         (neg|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
         (jump_to_menu, "mnu_village_start_attack"),
       (try_end),
    ],
    [
      ("take_supplies",[],"Take the supplies.",
       [
         (try_begin),
           (party_slot_ge, "$current_town", slot_center_player_relation, -55),
           (try_begin),
             (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
             (call_script, "script_change_player_relation_with_center", "$current_town", -1),
           (else_try),
             (call_script, "script_change_player_relation_with_center", "$current_town", -3),
           (try_end),
         (try_end),
         (party_get_slot, ":village_lord", "$current_town", slot_town_lord),
         (try_begin),
           (gt,  ":village_lord", 1),
           (call_script, "script_change_player_relation_with_troop", ":village_lord", -1),
          (try_end),
         (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
         (party_get_skill_level, ":player_party_looting", "p_main_party", "skl_looting"),
         (val_mul, ":player_party_looting", 3),
         (store_sub, ":random_chance", 70, ":player_party_looting"), #Increases the chance of looting by 3% per skill level
         (try_for_range, ":slot_no", num_equipment_kinds ,max_inventory_items + num_equipment_kinds),
           (store_random_in_range, ":rand", 0, 100),
           (lt, ":rand", ":random_chance"),
           (troop_set_inventory_slot, ":merchant_troop", ":slot_no", -1),
         (try_end),

###NPC companion changes begin
         (call_script, "script_objectionable_action", tmt_humanitarian, "str_steal_from_villagers"),
#NPC companion changes end
#Troop commentary changes begin
          (call_script, "script_add_log_entry", logent_village_extorted, "trp_player",  "$current_town", -1, -1),
          (store_faction_of_party,":village_faction",  "$current_town"),
          #SB : this war penalty should be lower for accosting farmers instead of raiding outright
          (call_script, "script_faction_inflict_war_damage_on_faction", "$players_kingdom", ":village_faction", 3),
#Troop commentary changes end

         #SB : sometimes this will actually be empty
         (jump_to_menu, "mnu_village"),
         (troop_sort_inventory, ":merchant_troop"),
         (change_screen_loot, ":merchant_troop"),
         ]),
      ("let_them_keep_it",[],"Let them keep it.",[(jump_to_menu, "mnu_village")]),
    ],
  ),

  ( #SB : added fugitive related strings
    "village_start_attack",mnf_disable_all_keys|mnf_scale_picture,
    "Some of the angry villagers grab their tools and prepare to resist you.\
 It looks like you'll have a fight on your hands if you continue.{s1}",
    "none",
    [
       (set_background_mesh, "mesh_pic_villageriot"),
       (call_script, "script_party_count_members_with_full_health","p_main_party"),
       (assign, ":player_party_size", reg0),
       (call_script, "script_party_count_members_with_full_health","$current_town"),
       (assign, ":villagers_party_size", reg0),

       (try_begin), #SB : tweak fight avoidance parameters
         #also if we lost but reduced their numbers, don't allow this condition to be true
         (neq, "$g_battle_result", -1),
         (this_or_next|le, ":villagers_party_size", 30),
         (gt, ":player_party_size", ":villagers_party_size"),
         (jump_to_menu, "mnu_village_loot_no_resist"),
       (else_try),
         (this_or_next|eq, ":villagers_party_size", 0),
         (eq, "$g_battle_result", 1),
         (try_begin),
           (eq, "$g_battle_result", 1),
           (store_random_in_range, ":enmity", -30, -15),
           (call_script, "script_change_player_relation_with_center", "$current_town", ":enmity"),
           (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
           (gt, ":town_lord", 0),
           (call_script, "script_change_player_relation_with_troop", ":town_lord", -3),
         (try_end),
         (jump_to_menu, "mnu_village_loot_no_resist"),
       (else_try),
         (eq, "$g_battle_result", -1),
         (try_begin), #if we did not knock him out or kill him, he escapes
           (check_quest_active, "qst_hunt_down_fugitive"),
           (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
           (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
           (jump_to_menu, "mnu_village_hunt_down_fugitive_defeated"),
         (else_try),
           (jump_to_menu, "mnu_village_loot_defeat"),
         (try_end),
       (try_end),

       #SB : display string indicating fugitive is here
      (try_begin), #if we did not knock him out or kill him, he escapes
        (check_quest_active, "qst_hunt_down_fugitive"),
        (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
        (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
        (quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
        (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
        (str_store_string, s1, "@ From your vantage point you see a man matching the description of {s50} arming himself with a sword during the commotion. If you do not press on the fugitive will slip away!"),
      (else_try),
        (str_clear, s1),
      (try_end),
    ],
    [
      ("village_raid_attack",[],"Charge them.",[
          (store_random_in_range, ":enmity", -10, -5),
          (call_script, "script_change_player_relation_with_center", "$current_town", ":enmity"),
          (try_begin),
            (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
            (gt, ":town_lord", 0),
            (call_script, "script_change_player_relation_with_troop", ":town_lord", -3),
          (try_end),
          #SB : add fugitive as defender here
          (try_begin),
            (check_quest_active, "qst_hunt_down_fugitive"),
            (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
            (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
            (neg|check_quest_failed, "qst_hunt_down_fugitive"),
            (quest_set_slot, "qst_hunt_down_fugitive", slot_quest_current_state, 1), #normally this is activated in dialogs
            (party_add_members, "$current_town", "trp_fugitive", 1),
          (try_end),
          (call_script, "script_calculate_battle_advantage"),
          (set_battle_advantage, reg0),
          (set_party_battle_mode),
          (assign, "$g_battle_result", 0),
          (assign, "$g_village_raid_evil", 1),
          (set_jump_mission,"mt_village_raid"),
          (party_get_slot, ":scene_to_use", "$current_town", slot_castle_exterior),
          (jump_to_scene, ":scene_to_use"),
          (assign, "$g_next_menu", "mnu_village_start_attack"),

          (call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$g_encountered_party"),
###NPC companion changes begin
          (call_script, "script_objectionable_action", tmt_humanitarian, "str_loot_village"),
#NPC companion changes end

          (jump_to_menu, "mnu_battle_debrief"),
          (change_screen_mission),
          ]),
      ("village_raid_leave",[],"Leave this village alone.",[(change_screen_return),
      #SB : fail fugitive quest if player backs away from demands
      (try_begin),
        (check_quest_active, "qst_hunt_down_fugitive"),
        (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, "$current_town"),
        (neg|check_quest_concluded, "qst_hunt_down_fugitive"),
        (call_script, "script_fail_quest", "qst_hunt_down_fugitive"),
      (try_end),

      ]),
    ],
  ),
  (
    "village_loot_no_resist",0,
    "The villagers here are few and frightened, and they quickly scatter and run before you.\
 The village is at your mercy.",
    "none",
    [
    #SB : if we just wanted to steal food, return to doing that instead of plundering
    (try_begin),
      (eq, "$auto_enter_menu_in_center", "mnu_village_take_food"),
      (jump_to_menu, "$auto_enter_menu_in_center"),
    (try_end),

    ],
    [
      ("village_loot",[], "Plunder the village, then raze it.",
        [
          (call_script, "script_village_set_state", "$current_town", svs_being_raided),
          (party_set_slot, "$current_town", slot_village_raided_by, "p_main_party"),
          (assign,"$g_player_raiding_village","$current_town"),

          (try_begin),
            (store_faction_of_party, ":village_faction", "$current_town"),
            (store_relation, ":relation", "$players_kingdom", ":village_faction"),
            (ge, ":relation", 0),
            (call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$current_town"),
          (try_end),

          (rest_for_hours_interactive, 3, 5, 1), #rest while attackable (3 hours will be extended by the trigger)
          (party_set_slot, "$current_town", slot_town_last_nearby_fire_time, 1), #raiding mode
          # (assign, "$g_village_raid_evil", 1), #SB : to differentiate between raiding
          (change_screen_return),
        ]),

        #SB : alternative option if that's your thing
      ("village_enslave", [
          (party_get_num_companions, ":amount", "$current_town"),
          (gt, ":amount", 0), #if we haven't killed them all in the first charge
          # (party_get_free_prisoners_capacity, ":capacity", "p_main_party"), #be slightly wary of this operation
          # (gt, ":capacity", 0), #if we have room
          (troops_can_join_as_prisoner, 1),
        ], "Chase after the remaining villagers and enslave them.",
        [
          (call_script, "script_village_set_state", "$current_town", svs_being_raided), #target is deserted, not looted
          (party_set_slot, "$current_town", slot_village_raided_by, "p_main_party"),
          (assign,"$g_player_raiding_village","$current_town"),

          (try_begin),
            (store_faction_of_party, ":village_faction", "$current_town"),
            (store_relation, ":relation", "$players_kingdom", ":village_faction"),
            (ge, ":relation", 0),
            (call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$current_town"),
          (try_end),

          #add a party template to represent hiding villagers so we don't go empty-handed
          (party_add_template, "$current_town", "pt_women"),
          (party_add_template, "$current_town", "pt_women"),
          #(party_add_template, "$current_town", "pt_village_defenders"),
          #add some smoke right away
          # (party_add_particle_system, "$current_town", "psys_map_village_fire"),

          (rest_for_hours, 3, 5, 1), #rest while attackable
          # (assign, "$g_village_raid_evil", 2),
          (party_set_slot, "$current_town", slot_town_last_nearby_fire_time, 2), #enslavement mode
          (assign, "$qst_eliminate_bandits_infesting_village_num_villagers", 0),
          (change_screen_return),
        ]),
      ("village_raid_leave",[],"Leave this village alone.",[(change_screen_return)]),
    ],
  ),
  (
    "village_loot_complete",mnf_disable_all_keys,
    "On your orders your troops sack the village, pillaging everything of any value,\
 and then put the buildings to the torch. From the coins and valuables that are found, you get your share of {reg1} denars.",
    "none",
    [
        (get_achievement_stat, ":number_of_village_raids", ACHIEVEMENT_THE_BANDIT, 0),
        (get_achievement_stat, ":number_of_caravan_raids", ACHIEVEMENT_THE_BANDIT, 1),
        (val_add, ":number_of_village_raids", 1),
        (set_achievement_stat, ACHIEVEMENT_THE_BANDIT, 0, ":number_of_village_raids"),

        (try_begin),
          (ge, ":number_of_village_raids", 3),
          (ge, ":number_of_caravan_raids", 3),
          (unlock_achievement, ACHIEVEMENT_THE_BANDIT),
        (try_end),

        (party_get_slot, ":village_lord", "$current_town", slot_town_lord),
        (try_begin),
          (gt,  ":village_lord", 0),
          (call_script, "script_change_player_relation_with_troop", ":village_lord", -5),
        (try_end),
        (store_random_in_range, ":enmity", -35, -25),
        (call_script, "script_change_player_relation_with_center", "$current_town", ":enmity"),

        (store_faction_of_party, ":village_faction", "$current_town"),
        (store_relation, ":relation", ":village_faction", "fac_player_supporters_faction"),
        (try_begin),
          (lt, ":relation", 0),
          (call_script, "script_change_player_relation_with_faction", ":village_faction", -3),
        (try_end),

        (assign, ":money_gained", 50), #SB : change this to be somewhat based on actual wealth
        (party_get_slot, ":village_elder", "$current_town",slot_town_elder),
        (try_begin),
          (gt, ":village_elder", 0),
          (store_troop_gold, ":money_gained", ":village_elder"),
          (troop_remove_gold, ":village_elder", ":money_gained"),
          (val_div, ":money_gained", 2),
        (try_end),
        (val_max, ":money_gained", 50),
        (party_get_slot, ":prosperity", "$current_town", slot_town_prosperity),
        (store_mul, ":prosperity_of_village_mul_5", ":prosperity", 5),
        (val_add, ":money_gained", ":prosperity_of_village_mul_5"),
        (call_script, "script_troop_add_gold", "trp_player", ":money_gained"),

        (assign, ":morale_increase", 3),
        (store_div, ":money_gained_div_100", ":money_gained", 100),
        (val_add, ":morale_increase", ":money_gained_div_100"),
        (call_script, "script_change_player_party_morale", ":morale_increase"),


        # (faction_get_slot, ":faction_morale", ":village_faction",  slot_faction_morale_of_player_troops),
        (store_mul, ":morale_decrease", ":morale_increase", -200),
        (call_script, "script_change_faction_troop_morale", ":village_faction", ":morale_decrease", 1), #SB : script call
        # (val_sub, ":faction_morale", ":morale_increase_mul_2"),
        # (faction_set_slot, ":village_faction",  slot_faction_morale_of_player_troops, ":faction_morale"),



#NPC companion changes begin
        (call_script, "script_objectionable_action", tmt_humanitarian, "str_loot_village"),
#NPC companion changes end
        (assign, reg1, ":money_gained"),
      ],
    [
      ("continue",[], "Continue...",
       [
       (jump_to_menu, "mnu_close"),
          (call_script, "script_calculate_amount_of_cattle_can_be_stolen", "$current_town"),
          (assign, ":max_cattle", reg0),
          (val_mul, ":max_cattle", 3),
          (val_div, ":max_cattle", 2),
          (party_get_slot, ":num_cattle", "$current_town", slot_village_number_of_cattle),
          (val_min, ":max_cattle", ":num_cattle"),
          (val_add, ":max_cattle", 1),
          (store_random_in_range, ":random_value", 0, ":max_cattle"),
          (try_begin),
            (gt, ":random_value", 0),
            (call_script, "script_create_cattle_herd", "$current_town", ":random_value"),
            (val_sub, ":num_cattle", ":random_value"),
            (party_set_slot, "$current_town", slot_village_number_of_cattle, ":num_cattle"),
          (try_end),

          #below line changed with below lines to make plunder result more realistic. Now only items produced in bound town can be stolen after raid.
          #(reset_item_probabilities,100),

          #begin of changes
          (party_get_slot, ":bound_town", "$current_town", slot_village_market_town),
          #the above line is the culprit for divide by zero
          # (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
          (assign, ":item_to_price_slot", slot_town_trade_good_prices_begin),
          (reset_item_probabilities,100),
          (assign, ":total_probability", 0),
          (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
            (party_get_slot, ":cur_price", ":bound_town", ":item_to_price_slot"),
            (val_add, ":item_to_price_slot", 1),
            (call_script, "script_center_get_production", ":bound_town", ":cur_goods"),
            (assign, ":cur_probability", reg0),
            (call_script, "script_center_get_consumption", ":bound_town", ":cur_goods"),
            (val_div, reg0, 3),
            (val_add, ":cur_probability", reg0),
            (val_mul, ":cur_probability", 4),
            (try_begin),
              (neq, ":cur_price", 0),
              (val_mul, ":cur_probability", average_price_factor),
              (val_div, ":cur_probability", ":cur_price"), #divide by zero error here
            (try_end),
            #first only simulation
            #(set_item_probability_in_merchandise,":cur_goods",":cur_probability"),
            (val_add, ":total_probability", ":cur_probability"),
            # (assign, reg1, ":total_probability"),
            # (assign, reg2, ":cur_price"),
            # (assign, reg3, ":cur_probability"),
            # (assign, reg4, ":item_to_price_slot"),
            # (str_store_item_name, s1, ":cur_goods"),
            # (display_message, "@{s1} price : {reg2} in slot {reg4}, probability: {reg3};{reg1} total"),
          (try_end),
          (val_max, ":total_probability", 1),
          (assign, ":item_to_price_slot", slot_town_trade_good_prices_begin),
          (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
            (party_get_slot, ":cur_price", ":bound_town", ":item_to_price_slot"),
            (val_add, ":item_to_price_slot", 1),
            (call_script, "script_center_get_production", ":bound_town", ":cur_goods"),
            (assign, ":cur_probability", reg0),
            (call_script, "script_center_get_consumption", ":bound_town", ":cur_goods"),
            (val_div, reg0, 3),
            (val_add, ":cur_probability", reg0),
            (val_mul, ":cur_probability", 4),
            (try_begin),
              (neq, ":cur_price", 0),
              (val_mul, ":cur_probability", average_price_factor),
              (val_div, ":cur_probability", ":cur_price"), #divide by zero error here
            (try_end),

            (val_mul, ":cur_probability", num_merchandise_goods),
            (val_mul, ":cur_probability", 100),
            (val_div, ":cur_probability", ":total_probability"),

            (set_item_probability_in_merchandise,":cur_goods",":cur_probability"),
          (try_end),
          #end of changes

          (troop_add_merchandise,"trp_temp_troop",itp_type_goods,30),
          (troop_sort_inventory, "trp_temp_troop"),
          (change_screen_loot, "trp_temp_troop"),
        ]),
    ],
  ),
  (
    "village_enslave_complete",mnf_disable_all_keys,
    "On your orders your troops rampage through the village, dragging peasants from their hovels and stripping them of all possessions.\
 In the span of a few hours you've rounded up {reg1} prisoners, leaving the infirm and the younglings behind. As you march the trussed-up villagers away from the cooling ember of their broken hearths, you hear a distant howl...",
    "none",
    [
        (get_achievement_stat, ":number_of_village_raids", ACHIEVEMENT_THE_BANDIT, 0),
        (get_achievement_stat, ":number_of_caravan_raids", ACHIEVEMENT_THE_BANDIT, 1),
        (val_add, ":number_of_village_raids", 1),
        (set_achievement_stat, ACHIEVEMENT_THE_BANDIT, 0, ":number_of_village_raids"),

        (try_begin),
          (ge, ":number_of_village_raids", 3),
          (ge, ":number_of_caravan_raids", 3),
          (unlock_achievement, ACHIEVEMENT_THE_BANDIT),
        (try_end),

        (set_background_mesh, "mesh_pic_prisoner_wilderness"),
        (call_script, "script_objectionable_action", tmt_humanitarian, "str_sell_slavery"),

        # (party_get_slot, ":village_lord", "$current_town", slot_town_lord),
        # (try_begin),
          # (gt,  ":village_lord", 0),
          # (call_script, "script_change_player_relation_with_troop", ":village_lord", -5),
        # (try_end),
        (store_random_in_range, ":enmity", -35, -25),
        (call_script, "script_change_player_relation_with_center", "$current_town", ":enmity"),

        (party_add_particle_system, "$current_town", "psys_map_village_looted_smoke"),
        (store_faction_of_party, ":village_faction", "$current_town"),
        (store_relation, ":relation", ":village_faction", "fac_player_supporters_faction"),
        (try_begin),
          (lt, ":relation", 0),
          (call_script, "script_change_player_relation_with_faction", ":village_faction", -2),
        (try_end),

        (store_mul, ":morale_decrease", "$qst_eliminate_bandits_infesting_village_num_villagers", -150),
        (call_script, "script_change_faction_troop_morale", ":village_faction", ":morale_decrease", 1), #SB : script call
        (assign, reg1, "$qst_eliminate_bandits_infesting_village_num_villagers"),
      ],
    [
      ("continue",[], "Continue...",
       [
            (assign, "$g_leave_town", 1),
            (jump_to_menu, "mnu_village"),
        ]),
    ],
  ),
  (
    "village_loot_defeat",mnf_scale_picture,
    "Fighting with courage and determination, the villagers manage to hold together and drive off your forces.",
    "none",
    [
        (set_background_mesh, "mesh_pic_villageriot"),
    ],
    [
      ("continue",[],"Continue...",[(change_screen_return),
      #SB : renown loss
      (call_script, "script_change_troop_renown", "trp_player", -3),
      ]),
    ],
  ),
  (
    "village_loot_continue",0,
    "Do you wish to continue looting this village?",
    "none",
    [
    (set_background_mesh, "mesh_pic_looted_village"),
    ],
    [
      ("loot_yes",[],"Yes.",[ (rest_for_hours_interactive, 3, 5, 1), #rest while attackable (3 hours will be extended by the trigger)
                              #SB : resume hostilities
                              (call_script, "script_diplomacy_party_attacks_neutral", "p_main_party", "$current_town"),
                              (change_screen_return),
                              ]),
      ("loot_no",[],"No.",[(call_script, "script_village_set_state", "$current_town", 0),
                            (party_set_slot, "$current_town", slot_village_raided_by, -1),
                            (assign, "$g_player_raiding_village", 0),
                            (assign, "$g_village_raid_evil", 0), #SB : reset global
                            (party_set_slot, "$current_town", slot_town_last_nearby_fire_time, 0),
                            (change_screen_return)]),
    ],
  ),
  (
    "close",0,
    "Nothing.",
    "none",
    [
        (change_screen_return),
      ],
    [],
  ),
]
