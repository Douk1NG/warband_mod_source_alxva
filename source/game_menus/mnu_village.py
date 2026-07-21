# ======================================================================
# SHARED DEPENDENCY
# Entity: village (menu)
# Called by menus in 6 domains: cheats, dickplomacy, diplomacy, reports, taxes, village
# ======================================================================

# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

village_menu = [
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
  )
]
