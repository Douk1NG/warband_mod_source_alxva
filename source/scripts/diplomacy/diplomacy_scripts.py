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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

####################################################################################################################
# DIPLOMACY MOD SCRIPTS
# 
# This file contains all scripts added by the Diplomacy mod (dplmc_ prefix).
# Includes: treasury management, autoloot, recruiter sending, messengers, patrols,
# scouts, gender checks, pretender proposals, terrain battle calculations, etc.
####################################################################################################################

diplomacy_scripts = [
  ("dplmc_send_recruiter",
    [
    (store_script_param, ":number_of_recruits", 1),
#daedalus begin
   (store_script_param, ":faction_of_recruits", 2),
#daedalus end
   (assign, ":expenses", ":number_of_recruits"),
   (val_mul, ":expenses", 20),
   (val_add, ":expenses", 10),
   (call_script, "script_dplmc_withdraw_from_treasury", ":expenses"),
   (set_spawn_radius, 1),
    (spawn_around_party, "$current_town", "pt_dplmc_recruiter"),
    (assign,":spawned_party",reg0),
    (party_set_ai_behavior, ":spawned_party", ai_bhvr_hold),
    (party_set_slot, ":spawned_party", slot_party_type, dplmc_spt_recruiter),
    (party_set_slot, ":spawned_party", dplmc_slot_party_recruiter_needed_recruits, ":number_of_recruits"),
   #daedalus begin
   (party_set_slot, ":spawned_party", dplmc_slot_party_recruiter_needed_recruits_faction, ":faction_of_recruits"),
   #daedalus end
   (party_set_slot, ":spawned_party", dplmc_slot_party_recruiter_origin, "$current_town"),
   (assign, ":faction", "$players_kingdom"),
   (party_set_faction, ":spawned_party", ":faction"),
    ]),
#recruiter kit end

####################################################################################
#
# Autoloot Scripts begin
# ---------------------------------------------------
####################################################################################

  #### Autoloot improved by rubik begin
  # ("dplmc_init_item_difficulties", set_item_difficulty()),
  #### Autoloot improved by rubik end


###################################
   # Can a troop qualify to use this item?
   # Returns 1 = yes, 0 = no.
   ("dplmc_troop_can_use_item",
   [
      (store_script_param, ":troop", 1),
      (store_script_param, ":item", 2),
      (store_script_param, ":item_modifier", 3),

      # (item_get_slot, ":difficulty", ":item", dplmc_slot_item_difficulty),
      (item_get_difficulty, ":difficulty", ":item"),
      (item_get_type, ":type", ":item"),
      (try_begin),
        (eq, ":difficulty", 0), # don't apply imod modifiers if item has no requirement
      (else_try),
        (eq, ":item_modifier", imod_stubborn),
        (val_add, ":difficulty", 1),
      (else_try),
        (eq, ":item_modifier", imod_timid),
        (val_sub, ":difficulty", 1),
      (else_try),
        (eq, ":item_modifier", imod_heavy),
        (neq, ":type", itp_type_horse), #heavy horses don't increase difficulty
        (val_add, ":difficulty", 1),
      (else_try),
        (eq, ":item_modifier", imod_strong),
        (val_add, ":difficulty", 2),
      (else_try),
        (eq, ":item_modifier", imod_masterwork),
        (val_add, ":difficulty", 4),
      (try_end),

      (item_get_type, ":type", ":item"),
      (try_begin),
        (eq, ":type", itp_type_horse),
        (store_skill_level, ":skill", skl_riding, ":troop"),
      (else_try),
        (this_or_next|eq, ":type", itp_type_crossbow),
        (this_or_next|eq, ":type", itp_type_one_handed_wpn),
        (this_or_next|eq, ":type", itp_type_two_handed_wpn),
        (this_or_next|eq, ":type", itp_type_polearm),
        (this_or_next|eq, ":type", itp_type_head_armor),
        (this_or_next|eq, ":type", itp_type_body_armor),
        (this_or_next|eq, ":type", itp_type_foot_armor),
        (eq, ":type", itp_type_hand_armor),
        (store_attribute_level, ":skill", ":troop", ca_strength),
      (else_try),
        (eq, ":type", itp_type_shield),
        (store_skill_level, ":skill", skl_shield, ":troop"),
      (else_try),
        (eq, ":type", itp_type_bow),
        (store_skill_level, ":skill", skl_power_draw, ":troop"),
      (else_try),
        (eq, ":type", itp_type_thrown),
        (store_skill_level, ":skill", skl_power_throw, ":troop"),
      (try_end),

      (try_begin),
        (lt, ":skill", ":difficulty"),
        (assign, reg0, 0),
      (else_try),
        (assign, reg0, 1),
      (try_end),
   ]),

#####################################################################
# gets an item's value
# Param1: item ID
# Param2: item modifier
#####################################################################
("dplmc_get_item_value_with_imod", [  # returns the sell price based on the item's money value and its imod
	(store_script_param, ":item", 1),
	(store_script_param, ":imod", 2),
	(store_item_value, ":score", ":item"),
	(try_begin),
		(eq, ":imod", imod_plain),
		(val_mul, ":score", 100),
	(else_try),
		(eq, ":imod", imod_cracked),
		(val_mul, ":score", 50),
	(else_try),
		(eq, ":imod", imod_rusty),
		(val_mul, ":score", 55),
	(else_try),
		(eq, ":imod", imod_bent),
		(val_mul, ":score", 65),
	(else_try),
		(eq, ":imod", imod_chipped),
		(val_mul, ":score", 72),
	(else_try),
		(eq, ":imod", imod_battered),
		(val_mul, ":score", 75),
	(else_try),
		(eq, ":imod", imod_poor),
		(val_mul, ":score", 80),
	(else_try),
		(eq, ":imod", imod_crude),
		(val_mul, ":score", 83),
	(else_try),
		(eq, ":imod", imod_old),
		(val_mul, ":score", 86),
	(else_try),
		(eq, ":imod", imod_cheap),
		(val_mul, ":score", 90),
	(else_try),
		(eq, ":imod", imod_fine),
		(val_mul, ":score", 190),
	(else_try),
		(eq, ":imod", imod_well_made),
		(val_mul, ":score", 250),
	(else_try),
		(eq, ":imod", imod_sharp),
		(val_mul, ":score", 160),
	(else_try),
		(eq, ":imod", imod_balanced),
		(val_mul, ":score", 350),
	(else_try),
		(eq, ":imod", imod_tempered),
		(val_mul, ":score", 670),
	(else_try),
		(eq, ":imod", imod_deadly),
		(val_mul, ":score", 850),
	(else_try),
		(eq, ":imod", imod_exquisite),
		(val_mul, ":score", 1450),
	(else_try),
		(eq, ":imod", imod_masterwork),
		(val_mul, ":score", 1750),
	(else_try),
		(eq, ":imod", imod_heavy),
		(val_mul, ":score", 190),
	(else_try),
		(eq, ":imod", imod_strong),
		(val_mul, ":score", 490),
	(else_try),
		(eq, ":imod", imod_powerful),
		(val_mul, ":score", 320),
	(else_try),
		(eq, ":imod", imod_tattered),
		(val_mul, ":score", 50),
	(else_try),
		(eq, ":imod", imod_ragged),
		(val_mul, ":score", 70),
	(else_try),
		(eq, ":imod", imod_rough),
		(val_mul, ":score", 60),
	(else_try),
		(eq, ":imod", imod_sturdy),
		(val_mul, ":score", 170),
	(else_try),
		(eq, ":imod", imod_thick),
		(val_mul, ":score", 260),
	(else_try),
		(eq, ":imod", imod_hardened),
		(val_mul, ":score", 390),
	(else_try),
		(eq, ":imod", imod_reinforced),
		(val_mul, ":score", 650),
	(else_try),
		(eq, ":imod", imod_superb),
		(val_mul, ":score", 250),
	(else_try),
		(eq, ":imod", imod_lordly),
		(val_mul, ":score", 1150),
	(else_try),
		(eq, ":imod", imod_lame),
		(val_mul, ":score", 40),
	(else_try),
		(eq, ":imod", imod_swaybacked),
		(val_mul, ":score", 60),
	(else_try),
		(eq, ":imod", imod_stubborn),
		(val_mul, ":score", 90),
	(else_try),
		(eq, ":imod", imod_timid),
		(val_mul, ":score", 180),
	(else_try),
		(eq, ":imod", imod_meek),
		(val_mul, ":score", 180),
	(else_try),
		(eq, ":imod", imod_spirited),
		(val_mul, ":score", 650),
	(else_try),
		(eq, ":imod", imod_champion),
		(val_mul, ":score", 1450),
	(else_try),
		(eq, ":imod", imod_fresh),
		(val_mul, ":score", 100),
	(else_try),
		(eq, ":imod", imod_day_old),
		(val_mul, ":score", 100),
	(else_try),
		(eq, ":imod", imod_two_day_old),
		(val_mul, ":score", 90),
	(else_try),
		(eq, ":imod", imod_smelling),
		(val_mul, ":score", 40),
	(else_try),
		(eq, ":imod", imod_rotten),
		(val_mul, ":score", 5),
	(else_try),
		(eq, ":imod", imod_large_bag),
		(val_mul, ":score", 190),
	(try_end),

	(assign, reg0, ":score"),
]),

  #### Autoloot improved by rubik begin
  # ("dplmc_init_item_base_score", set_item_base_score()),

  ("dplmc_get_item_score_with_imod",
    [# returns the score on the item's base score and its imod
      (store_script_param, ":item", 1),
      (store_script_param, ":imod", 2),

      (item_get_type, ":type", ":item"),
      (assign, ":imod_effect", 0), #default modifier
      (try_begin),
        # horse score = horse_speed*horse_armor*horse_sell_price
        (eq, ":type", itp_type_horse),
        # (item_get_slot, ":horse_speed", ":item", dplmc_slot_item_horse_speed),
        # (item_get_slot, ":horse_armor", ":item", dplmc_slot_item_horse_armor),
        (item_get_horse_speed, ":horse_speed", ":item"),
        (item_get_body_armor, ":horse_armor", ":item"),
        # (call_script, "script_dplmc_get_item_value_with_imod", ":item", ":imod"),
        (item_get_value, ":i_score", ":item"),
        # (assign, ":i_score", reg0),

        ## SB : price now secondary (additive) instead of multiplicative with actual attributes
        (item_get_horse_speed, ":horse_speed", ":item"),
        (item_get_horse_maneuver, ":horse_manu", ":item"),
        (item_get_body_armor, ":horse_armor", ":item"),
        (item_get_horse_charge_damage, ":horse_charge", ":item"),
        (item_get_hit_points, ":horse_health", ":item"),

        #imodbits_horse_basic = imodbit_swaybacked|imodbit_lame|imodbit_spirited|imodbit_heavy|imodbit_stubborn
        #imodbits_horse_good = imodbit_spirited|imodbit_heavy
        (try_begin),
          (eq, ":imod", imod_swaybacked),
          (val_sub, ":horse_speed", 2),
          (val_sub, ":horse_manu", 2),
        (else_try), #do not pick lame horses at all other than last resort
          (eq, ":imod", imod_lame),
          (assign, ":horse_speed", 0),
        (else_try),
          (eq, ":imod", imod_heavy),
          (val_add, ":horse_armor", 3),
          (val_add, ":horse_charge", 4),
          (val_add, ":horse_health", 10),
        (else_try),
          (eq, ":imod", imod_stubborn),
          (val_add, ":horse_health", 5),
        (else_try),
          (eq, ":imod", imod_spirited),
          (val_add, ":horse_speed", 1),
          (val_add, ":horse_manu", 1),
          (val_add, ":horse_armor", 1),
          (val_add, ":horse_charge", 1),
        (else_try),
          (eq, ":imod", imod_champion),
          (val_add, ":horse_speed", 2),
          (val_add, ":horse_manu", 2),
          (val_add, ":horse_armor", 2),
          (val_add, ":horse_charge", 2),
        (try_end),

        (val_mul, ":horse_speed", ":horse_manu"),
        (val_add, ":i_score", ":horse_speed"),

        (val_mul, ":horse_charge", ":horse_armor"),
        (val_mul, ":horse_charge", ":horse_health"),
        (val_div, ":horse_charge", 100),#baseline hp
        (val_add, ":i_score", ":horse_charge"),
      (else_try),
        # shield score = shield_size*shield_armor
        (eq, ":type", itp_type_shield),
        # (item_get_slot, ":shield_size", ":item", dplmc_slot_item_shield_size),
        # (item_get_slot, ":shield_armor", ":item", dplmc_slot_item_shield_armor),

        ## SB : factor in speed and height
        (item_get_shield_height, ":shield_height", ":item"),
        (item_get_weapon_length, ":shield_width", ":item"),
        (item_get_body_armor, ":shield_armor", ":item"),
        (item_get_speed_rating, ":shield_speed", ":item"),
        (item_get_hit_points, ":shield_health", ":item"),

        (try_begin),
          (gt, ":shield_height", 0),
          (val_mul, ":shield_width",  ":shield_height"),
          (set_fixed_point_multiplier, 100),
          (store_mul, ":i_score", ":shield_width", 100),
          (store_sqrt, ":i_score", ":i_score"),
          (val_div, ":i_score", 100),
        (else_try),
          # (val_mul, ":shield_width", ":shield_width"),
          (assign, ":i_score", ":shield_width"),
        (try_end),


        #imodbits_shield  = imodbit_cracked | imodbit_battered |imodbit_thick | imodbit_reinforced
        (try_begin),
          # (eq, ":imod", imod_plain),
          # (assign, ":imod_effect", 0),
        # (else_try),
          (eq, ":imod", imod_cracked),
          (assign, ":imod_effect", -4),
          (val_sub, ":shield_health", 56),
        (else_try),
          (eq, ":imod", imod_battered),
          (assign, ":imod_effect", -2),
          (val_sub, ":shield_health", 26),
        (else_try),
          (eq, ":imod", imod_hardened),
          (assign, ":imod_effect", 3),
        (else_try),
          (eq, ":imod", imod_heavy),
          (assign, ":imod_effect", 3),
          (val_add, ":shield_health", 10),
        (else_try),
          (eq, ":imod", imod_thick),
          (assign, ":imod_effect", 2),
          (val_add, ":shield_health", 47),
        (else_try),
          (eq, ":imod", imod_reinforced),
          (assign, ":imod_effect", 4),
          (val_add, ":shield_health", 83),
        (else_try),
          (eq, ":imod", imod_lordly),
          (assign, ":imod_effect", 6),
          (val_add, ":shield_health", 155),
        (try_end),

        (val_add, ":shield_armor", ":imod_effect"),
        (val_add, ":shield_armor", 5), # add 5 to make sure shield_armor greater than 0
        (val_mul, ":i_score", ":shield_armor"),
        (val_mul, ":i_score", ":shield_speed"),
        (val_div, ":i_score", 92), #average speed of all Native's tableau
        (val_add, ":i_score", ":shield_health"), #tie-breaker
      (else_try),
        # armor score = head_armor + body_armor + foot_armor
        (this_or_next|eq, ":type", itp_type_head_armor),
        (this_or_next|eq, ":type", itp_type_body_armor),
        (this_or_next|eq, ":type", itp_type_foot_armor),
        (eq, ":type", itp_type_hand_armor),
        # (item_get_slot, ":head_armor", ":item", dplmc_slot_item_head_armor),
        # (item_get_slot, ":body_armor", ":item", dplmc_slot_item_body_armor),
        # (item_get_slot, ":leg_armor", ":item", dplmc_slot_item_leg_armor),
        (item_get_head_armor, ":head_armor", ":item"),
        (item_get_body_armor, ":body_armor", ":item"),
        (item_get_leg_armor, ":leg_armor", ":item"),
        (store_add, ":i_score", ":head_armor", ":body_armor"),
        (val_add, ":i_score", ":leg_armor"), # get total base score

        (try_begin),
          # (eq, ":imod", imod_plain),
          # (assign, ":imod_effect", 0),
        # (else_try),
          (eq, ":imod", imod_cracked),
          (assign, ":imod_effect", -4),
        (else_try),
          (eq, ":imod", imod_rusty),
          (assign, ":imod_effect", -3),
        (else_try),
          (eq, ":imod", imod_battered),
          (assign, ":imod_effect", -2),
        (else_try),
          (eq, ":imod", imod_crude),
          (assign, ":imod_effect", -1),
        (else_try),
          (eq, ":imod", imod_tattered),
          (assign, ":imod_effect", -3),
        (else_try),
          (eq, ":imod", imod_ragged),
          (assign, ":imod_effect", -2),
        (else_try),
          (eq, ":imod", imod_sturdy),
          (assign, ":imod_effect", 1),
        (else_try),
          (eq, ":imod", imod_thick),
          (assign, ":imod_effect", 2),
        (else_try),
          (eq, ":imod", imod_hardened),
          (assign, ":imod_effect", 3),
        (else_try),
          (eq, ":imod", imod_reinforced),
          (assign, ":imod_effect", 4),
        (else_try),
          (eq, ":imod", imod_lordly),
          (assign, ":imod_effect", 6),
        (try_end),

        (try_begin), # for armors have 2 or 3 defence of different part
          (neq, ":imod_effect", 0), # and item modifers that matter
          (assign, ":imod_effect_mul", 0),
          (try_begin), #do nothing if no armor part at all
            (gt, ":head_armor", 0),
            (store_add, ":temp_armor", ":head_armor", ":imod_effect"),
            (try_begin), #only calculate if imod degrades item's rating
              (gt, ":temp_armor", 0),
              (val_add, ":imod_effect_mul", 1),
            (else_try), #downgrade armor rating to 0 from bad armor instead of going negative
              (val_sub, ":i_score", ":head_armor"),
            (try_end),
          (try_end),
          (try_begin),
            (gt, ":body_armor", 0),
            (store_add, ":temp_armor", ":body_armor", ":imod_effect"),
            (try_begin),
              (gt, ":temp_armor", 0),
              (val_add, ":imod_effect_mul", 1),
            (else_try),
              (val_sub, ":i_score", ":body_armor"),
            (try_end),
          (try_end),
          (try_begin),
            (gt, ":leg_armor", 0),
            (store_add, ":temp_armor", ":leg_armor", ":imod_effect"),
            (try_begin),
              (gt, ":temp_armor", 0),
              (val_add, ":imod_effect_mul", 1),
            (else_try),
              (val_sub, ":i_score", ":leg_armor"),
            (try_end),
          (try_end),

          (val_mul, ":imod_effect", ":imod_effect_mul"),
          (val_add, ":i_score", ":imod_effect"),
        (try_end),
      (else_try),
        # weapon score = max(swing_damage , thrust_damage)
        (this_or_next|eq, ":type", itp_type_one_handed_wpn),
        (this_or_next|eq, ":type", itp_type_two_handed_wpn),
        (this_or_next|eq, ":type", itp_type_bow),
        (this_or_next|eq, ":type", itp_type_crossbow),
        ##diplomacy start+ add extra types
        #(this_or_next|eq, ":type", itp_type_pistol),
        #(this_or_next|eq, ":type", itp_type_musket),
        ##diplomacy end+
        (eq, ":type", itp_type_polearm),
        (item_get_swing_damage, ":swing_damage", ":item"),
        (item_get_thrust_damage, ":thrust_damage", ":item"),
        (assign, reg1, ":swing_damage"), #sb : debug
        (assign, reg2, ":thrust_damage"), #sb : debug
        # (item_get_slot, ":swing_damage", ":item", dplmc_slot_item_swing_damage),
        # (item_get_slot, ":thrust_damage", ":item", dplmc_slot_item_thrust_damage),
        (val_mod, ":swing_damage", 256), # get actual damage value
        (val_mod, ":thrust_damage", 256),
        (assign, ":i_score", ":swing_damage"),
        (val_max, ":i_score", ":thrust_damage"),

        ##SB : get additional parameters
        (item_get_speed_rating, ":item_speed", ":item"),
        (item_get_weapon_length, ":item_length", ":item"),
        #shootspeed?

        (try_begin),
          # (eq, ":imod", imod_plain),
          # (assign, ":imod_effect", 0),
        # (else_try),
          (eq, ":imod", imod_cracked),
          (assign, ":imod_effect", -5),
        (else_try),
          (eq, ":imod", imod_rusty),
          (assign, ":imod_effect", -3),
        (else_try),
          (eq, ":imod", imod_bent),
          (assign, ":imod_effect", -3),
          (val_sub, ":item_speed", 3),
        (else_try),
          (eq, ":imod", imod_chipped),
          (assign, ":imod_effect", -1),
        (else_try), #SB : add fine
          (eq, ":imod", imod_fine),
          (assign, ":imod_effect", 1),
        (else_try),
          (eq, ":imod", imod_balanced),
          (assign, ":imod_effect", 3),
          (val_add, ":item_speed", 3),
        (else_try),
          (eq, ":imod", imod_tempered),
          (assign, ":imod_effect", 4),
        (else_try),
          (eq, ":imod", imod_masterwork),
          (assign, ":imod_effect", 5),
          (val_add, ":item_speed", 1),
        (else_try),
          (eq, ":imod", imod_heavy),
          (assign, ":imod_effect", 2),
          (val_sub, ":item_speed", 2),
        (else_try),
          (eq, ":imod", imod_strong),
          (assign, ":imod_effect", 3),
          (val_sub, ":item_speed", 3),
        (try_end),

        (val_add, ":i_score", ":imod_effect"),
        (try_begin), #try to pre-filter civilian weapons that are improvised from being looted (clubs, scythes, etc that should be passed over)
          (call_script, "script_cf_melee_weapon_is_civilian", ":item"),
          (val_div, ":i_score", 3),
        (try_end),
        (try_begin), #item_get_missile_speed is technically an important rating for ranged weapons, but we'll pretend NPCs can't math
          (this_or_next|is_between, ":type", itp_type_bow, itp_type_thrown),
          (is_between, ":type", itp_type_pistol, itp_type_bullets),
          (val_mul, ":i_score", ":item_speed"),
        (else_try), #assume base of 100 speed, 100 length
          (this_or_next|eq, ":type", itp_type_one_handed_wpn),
          (eq, ":type", itp_type_two_handed_wpn),
          (val_mul, ":item_length", ":item_speed"),
          (val_mul, ":i_score", ":item_length"),
        (else_try), #length priority over speed
          (eq, ":type", itp_type_polearm),
          (try_begin), #unless they're slashing
            (gt, ":thrust_damage", ":swing_damage"),
            (item_has_property, ":item", itp_couchable),
            # (item_has_property, ":item", itp_cant_use_on_horseback),
            (ge, ":item_length", dplmc_pike_length_cutoff),
            (val_sub, ":item_length", 50), #offset
            #no penalty for war spear range
            (val_max, ":item_length", 100),
            (val_mul, ":item_length", 4),
            #item speed rounded off when we couch
            (val_add, ":item_speed", 25),
            (val_div, ":item_speed", 10),
            # (val_mul, ":item_speed", 2),
          (try_end),
          (val_mul, ":item_length", ":item_speed"),
          (val_mul, ":i_score", ":item_length"),
        (try_end),
      (else_try),
        # ammo score = (thrust_damage + imod_effect)*2
        # a_large_bag will make score added by 1 to discriminate the same ammo with the plain modifier
        (this_or_next|eq, ":type", itp_type_arrows),
        (this_or_next|eq, ":type", itp_type_bolts),
        (eq, ":type", itp_type_thrown),
        (item_get_thrust_damage, ":thrust_damage", ":item"),
        (val_mod, ":thrust_damage", 256), # get actual damage value
        (store_add, ":i_score", ":thrust_damage", 3), # SB : make sure imods do not reduce damage to 0

        #imodbits_missile   = imodbit_bent | imodbit_large_bag
        #imodbits_thrown   = imodbit_bent | imodbit_heavy| imodbit_balanced| imodbit_large_bag
        (try_begin),
          (eq, ":imod", imod_plain),
          (val_mul, ":i_score", 2),
        (else_try),
          (eq, ":imod", imod_large_bag),
          (val_mul, ":i_score", 2),
          (val_add, ":i_score", 1),
        (else_try),
          (eq, ":imod", imod_bent),
          (val_sub, ":i_score", 3),
          (val_mul, ":i_score", 2),
        (else_try),
          (eq, ":imod", imod_heavy),
          (val_add, ":i_score", 2),
          (val_mul, ":i_score", 2),
        (else_try),
          (eq, ":imod", imod_balanced),
          (val_add, ":i_score", 3),
          (val_mul, ":i_score", 2),
        (try_end),
      (try_end),

      (assign, reg0, ":i_score"),
    ]),
  #### Autoloot improved by rubik end

###################
# Used in conversations

("dplmc_print_wpn_upgrades_to_s0", [
	(store_script_param_1, ":troop"),

	(str_store_string, s0, "str_empty_string"),
	(troop_get_slot, ":upg", ":troop", dplmc_slot_upgrade_wpn_0),
	(troop_get_inventory_slot, ":item", ":troop", 0),
	(try_begin),
		(ge, ":item", 0),
		(str_store_item_name, s10, ":item"),
	(else_try),
		(str_store_string, s10, "str_dplmc_none"),
	(try_end),
	(val_add, ":upg", "str_dplmc_hero_wpn_slot_none"),
	(str_store_string, s1, ":upg"),
	(str_store_string, s0, "@{s0}^{s1}"),
	(troop_get_slot, ":upg", ":troop", dplmc_slot_upgrade_wpn_1),
	(troop_get_inventory_slot, ":item", ":troop", 1),
	(try_begin),
		(ge, ":item", 0),
		(str_store_item_name, s10, ":item"),
	(else_try),
		(str_store_string, s10, "str_dplmc_none"),
	(try_end),
	(val_add, ":upg", "str_dplmc_hero_wpn_slot_none"),
	(str_store_string, s1, ":upg"),
	(str_store_string, s0, "@{s0}^{s1}"),
	(troop_get_slot, ":upg", ":troop", dplmc_slot_upgrade_wpn_2),
	(troop_get_inventory_slot, ":item", ":troop", 2),
	(try_begin),
		(ge, ":item", 0),
		(str_store_item_name, s10, ":item"),
	(else_try),
		(str_store_string, s10, "str_dplmc_none"),
	(try_end),
	(val_add, ":upg", "str_dplmc_hero_wpn_slot_none"),
	(str_store_string, s1, ":upg"),
	(str_store_string, s0, "@{s0}^{s1}"),
	(troop_get_slot, ":upg", ":troop", dplmc_slot_upgrade_wpn_3),
	(troop_get_inventory_slot, ":item", ":troop", 3),
	(try_begin),
		(ge, ":item", 0),
		(str_store_item_name, s10, ":item"),
	(else_try),
		(str_store_string, s10, "str_dplmc_none"),
	(try_end),
	(val_add, ":upg", "str_dplmc_hero_wpn_slot_none"),
	(str_store_string, s1, ":upg"),
	(str_store_string, s0, "@{s0}^{s1}"),
]),

################################
# Copy this troop's upgrade options to everyone

# ("dplmc_copy_upgrade_to_all_heroes", [
	# (store_script_param_1, ":troop"),

	# (troop_get_slot,":upg_armor", ":troop",dplmc_slot_upgrade_armor),
	# (troop_get_slot,":upg_horse",":troop",dplmc_slot_upgrade_horse),
	# (troop_get_slot,":upg_wpn0",":troop",dplmc_slot_upgrade_wpn_0),
	# (troop_get_slot,":upg_wpn1",":troop",dplmc_slot_upgrade_wpn_1),
	# (troop_get_slot,":upg_wpn2",":troop",dplmc_slot_upgrade_wpn_2),
	# (troop_get_slot,":upg_wpn3",":troop",dplmc_slot_upgrade_wpn_3),

	# (try_for_range, ":hero", companions_begin, companions_end),
		# (troop_set_slot,":hero",dplmc_slot_upgrade_armor,":upg_armor"),
		# (troop_set_slot,":hero",dplmc_slot_upgrade_horse,":upg_horse"),
		# (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_0,":upg_wpn0"),
		# (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_1,":upg_wpn1"),
		# (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_2,":upg_wpn2"),
		# (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_3,":upg_wpn3"),
	# (try_end),
# ]),

####################################
# Let each hero loot from the pool

("dplmc_auto_loot_all", [
    (store_script_param_1, ":pool_troop"),
    (store_script_param_2, ":sreg"),
    # for all the NPCs, in order of party listing

    (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":this_hero","p_main_party",":i_stack"),
        #Allow your spouse(s) to auto loot if they are in your party
        (assign, ":is_spouse", 0),
        (try_begin),
          #Next line returns true for regular troops so need to make sure this is a hero
          (is_between, ":this_hero", heroes_begin, heroes_end),
          (troop_slot_eq, ":this_hero", slot_troop_spouse, "trp_player"),
          (assign, ":is_spouse", 1),
        (try_end),
        (this_or_next|eq, ":is_spouse", 1),
        #Letting claimants loot may be undesirable as they eventually leave, but players can always disable auto loot for them
        (this_or_next|is_between, ":this_hero", pretenders_begin, pretenders_end),
        (is_between, ":this_hero", companions_begin, companions_end),

        #SB : show strings for first iteration
        (call_script, "script_dplmc_auto_loot_troop", ":this_hero", ":pool_troop", ":sreg"),
        (val_add, ":sreg", 1),
    (try_end),

    #SB : get starting index once again
    (store_script_param_2, ":sreg"),
    # pick up any discards and format string
    (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":this_hero","p_main_party",":i_stack"),
        (assign, ":is_spouse", 0),
        (try_begin),
          (is_between, ":this_hero", heroes_begin, heroes_end),
          (troop_slot_eq, ":this_hero", slot_troop_spouse, "trp_player"),
          (assign, ":is_spouse", 1),
        (try_end),
        (this_or_next|eq, ":is_spouse", 1),
        (this_or_next|is_between, ":this_hero", pretenders_begin, pretenders_end),
        (is_between, ":this_hero", companions_begin, companions_end),
        (try_begin), #if first iteration picked up nothing
          (str_is_empty, ":sreg"),
          (call_script, "script_dplmc_auto_loot_troop", ":this_hero", ":pool_troop", ":sreg"),
        (else_try), #do not overwrite string from first iteration
          (call_script, "script_dplmc_auto_loot_troop", ":this_hero", ":pool_troop", -1),
        (try_end),
        (try_begin), #skip the first one
          (gt, ":sreg", dplmc_loot_string),
          (neg|str_is_empty, ":sreg"), # in case second hasn't picked up changes either
          (str_store_string_reg, s1, ":sreg"),
          (str_store_string_reg, s0, dplmc_loot_string),
          (str_store_string, dplmc_loot_string, "str_dplmc_s0_newline_s1"),
        (try_end),
        (val_add, ":sreg", 1), #go to next string register
    (try_end),

    #Done. Now sort the remainder
    (troop_sort_inventory, ":pool_troop"),

]),


####################################
# let this troop take its pick from the loot pool

("dplmc_auto_loot_troop", [
	# (try_begin),
		(store_script_param, ":troop", 1),
		(store_script_param, ":pool", 2),
		(store_script_param, ":sreg", 3), #SB : new param for storing changes

		(troop_get_slot,":upg_armor", ":troop",dplmc_slot_upgrade_armor),
		(troop_get_slot,":upg_horses",":troop",dplmc_slot_upgrade_horse),

		# dump whatever rubbish is in the main inventory
		(troop_get_inventory_capacity, ":inv_cap", ":troop"),
		(try_for_range, ":i_slot", dplmc_ek_alt_items_end, ":inv_cap"), #SB raise from 10, skip over civilian stuff
			(troop_get_inventory_slot, ":item", ":troop", ":i_slot"),
			(ge, ":item", 0),
			(troop_get_inventory_slot_modifier, ":imod", ":troop", ":i_slot"),
			(troop_add_item, ":pool", ":item", ":imod"), #put it back in the pool
			(troop_set_inventory_slot, ":troop", ":i_slot", -1), # delete it
		(try_end),

        #clear slot
        # (try_for_range, ":slot_no", dplmc_slot_upgrade_wpn_0, dplmc_slot_upgrade_wpn_3 + 1),
          # (troop_slot_eq, ":troop", ":slot_no", 0), #0 is keep
          # (troop_set_slot, "trp_heroes_end", ":slot_no", 999999),
        # (else_try), #otherwise we reset to default
          # (troop_set_slot, "trp_heroes_end", ":slot_no", -1),
        # (try_end),

        #SB : loop, calculate current item's score
        # (assign, ":slot_no", dplmc_slot_upgrade_wpn_0 - 1),
        (try_for_range, ":item_slot", ek_item_0, ek_head),
          #SB : clear the pool troop's ek_slots
          (troop_set_inventory_slot, ":pool", ":item_slot", -1), #delete it
          (store_add, ":slot_no", dplmc_slot_upgrade_wpn_0, ":item_slot"), #pre-increment
          (troop_get_slot, ":item_preference", ":troop", ":slot_no"),
          (gt, ":item_preference", 0), #0 is keep
          (troop_get_inventory_slot, ":item", ":troop", ":item_slot"),
          (ge, ":item", 0), #initial item check
          (troop_get_inventory_slot_modifier, ":imod", ":troop", ":item_slot"),

          (try_begin),
            (store_mod, ":item_type", ":item_preference", meta_itp_mask),
            (item_get_type, ":itp", ":item"),
            (neq, ":itp", ":item_type"),
            (troop_set_inventory_slot, ":troop", ":item_slot", -1), #delete it
            (troop_add_item, ":pool", ":item", ":imod"), # chuck it in the pool
            (assign, ":item", -1), #so we fail this loop
          (try_end),
          (ge, ":item", 0),
          #SB : cache the original equipment to see changes
          (troop_set_inventory_slot, ":pool", ":item_slot", ":item"),
          (troop_set_inventory_slot_modifier, ":pool", ":item_slot", ":imod"),

          (call_script, "script_dplmc_get_item_score_with_imod", ":item", ":imod"),
          (assign, ":cur_value", reg0),
          #check to see whether damage is preferred
          (try_begin),
            (call_script, "script_cf_item_type_has_advanced_autoloot", ":item_type"),
            (store_div, ":dmg_type", ":item_preference", meta_dmg_mask),
            (neq, ":dmg_type", 0),
            (item_get_swing_damage, ":swing_damage", ":item"),
            (item_get_thrust_damage, ":thrust_damage", ":item"),
            (try_begin),
              (ge, ":swing_damage", ":thrust_damage"),
              (item_get_swing_damage_type, ":item_dmg_type", ":item"),
            (else_try),
              (lt, ":swing_damage", ":thrust_damage"),
              (item_get_thrust_damage_type, ":item_dmg_type", ":item"),
            (try_end),
            #check if it matches preference
            (val_add, ":item_dmg_type", 1),
            (eq, ":dmg_type", ":item_dmg_type"),
            (val_mul, ":cur_value", 4),
          (try_end),
          (troop_set_slot, "trp_heroes_end", ":slot_no", ":cur_value"),
        (else_try),
          (eq, ":item_preference", 0), #0 is keep
          (troop_set_slot, "trp_heroes_end", ":slot_no", 999999),
        (else_try), #whether no item or discarded
          (lt, ":item", 0),
          (troop_set_slot, "trp_heroes_end", ":slot_no", 0),
        (try_end),

        # (try_for_range, ":slot_no", dplmc_slot_upgrade_wpn_0, dplmc_slot_upgrade_wpn_3 + 1),
          # (troop_get_slot, reg0, ":troop", ":slot_no"),
          # (troop_get_slot, reg1, "trp_heroes_end", ":slot_no"),
          # (store_sub, reg2, ":slot_no", dplmc_slot_upgrade_wpn_0),
          # (troop_get_inventory_slot, ":item", ":troop", reg2),
          # (try_begin),
            # (eq, ":item", -1),
            # (str_store_string, s1, "str_dplmc_none"),
          # (else_try),
            # (str_store_item_name, s1, ":item"),
          # (try_end),

          # (display_message, "@upgrading slot {reg2} with {reg0}, cur score for {s1}: {reg1}"),
        # (try_end),

		(try_for_range, ":i_slot", ek_head, ek_food),
			(troop_get_inventory_slot, ":item", ":troop", ":i_slot"),
            (troop_set_inventory_slot, ":pool", ":i_slot", -1), #delete it
			(ge, ":item", 0),
            (troop_set_inventory_slot, ":pool", ":i_slot", ":item"), #store it
			(troop_get_inventory_slot_modifier, ":imod", ":troop", ":i_slot"),
            (troop_set_inventory_slot_modifier, ":pool", ":i_slot", ":imod"), #store it
			(try_begin),
				(neq, ":upg_armor", 0), # we're upgrading armors
				(is_between, ":i_slot", ek_head, ek_horse), # it's an armor slot
				(troop_set_inventory_slot, ":troop", ":i_slot", -1), #delete it
				(troop_add_item, ":pool", ":item", ":imod"), # chuck it in the pool
			(else_try),
				(neq, ":upg_horses", 0), # we're upgrading horses
				(eq, ":i_slot", ek_horse), # it's a horse slot
				(troop_set_inventory_slot, ":troop", ":i_slot", -1), #delete it
				(troop_add_item, ":pool", ":item", ":imod"), # chuck it in the pool
			(try_end),
		(try_end),

		# clear best matches
		(assign, ":best_helmet_slot", -1),
		(assign, ":best_helmet_val", 0),
		(assign, ":best_body_slot", -1),
		(assign, ":best_body_val", 0),
		(assign, ":best_boots_slot", -1),
		(assign, ":best_boots_val", 0),
		(assign, ":best_gloves_slot", -1),
		(assign, ":best_gloves_val", 0),
		(assign, ":best_horse_slot", -1),
		(assign, ":best_horse_val", 0),

		# Now search through the pool for the best items
		(troop_get_inventory_capacity, ":inv_cap", ":pool"),
		(try_for_range, ":i_slot", ek_food + 1, ":inv_cap"), #SB: skip cached items
			(troop_get_inventory_slot, ":item", ":pool", ":i_slot"),
			(ge, ":item", 0),
			(troop_get_inventory_slot_modifier, ":imod", ":pool", ":i_slot"),
			(call_script, "script_dplmc_troop_can_use_item", ":troop", ":item", ":imod"),
			(eq, reg0, 1), # can use
			#(call_script, "script_get_item_value_with_imod", ":item", ":imod"),  # use the following instead

			#### Autoloot improved by rubik begin
			# get item_score instead of price
			(call_script, "script_dplmc_get_item_score_with_imod", ":item", ":imod"),
			#### Autoloot improved by rubik end
			(assign, ":score", reg0),
			(item_get_type, ":item_type", ":item"),

			(try_begin),
				(eq, ":item_type", itp_type_horse), #it's a horse
				(eq, ":upg_horses", 1), # we're upgrading horses
				(gt, ":score", ":best_horse_val"),
				(assign, ":best_horse_slot", ":i_slot"),
				(assign, ":best_horse_val", ":score"),
			(else_try), #SB : move armor checks here
				(is_between, ":item_type", itp_type_head_armor, itp_type_hand_armor + 1), # we're checking armor
				(eq, ":upg_armor", 1), # we're upgrading armor
				(try_begin),
					(eq, ":item_type", itp_type_head_armor),
					(gt, ":score", ":best_helmet_val"),
					(assign, ":best_helmet_slot", ":i_slot"),
					(assign, ":best_helmet_val", ":score"),
				(else_try),
					(eq, ":item_type", itp_type_body_armor),
					(gt, ":score", ":best_body_val"),
					(assign, ":best_body_slot", ":i_slot"),
					(assign, ":best_body_val", ":score"),
				(else_try),
					(eq, ":item_type", itp_type_foot_armor),
					(gt, ":score", ":best_boots_val"),
					(assign, ":best_boots_slot", ":i_slot"),
					(assign, ":best_boots_val", ":score"),
				(else_try),
					(eq, ":item_type", itp_type_hand_armor),
					(gt, ":score", ":best_gloves_val"),
					(assign, ":best_gloves_slot", ":i_slot"),
					(assign, ":best_gloves_val", ":score"),
				(try_end),
            (else_try), #SB : move weapon checks back here
              (assign, ":limit", dplmc_slot_upgrade_wpn_3 + 1),
              (try_begin), #check for denying use on horseback
                  (this_or_next|gt, ":best_horse_val", 0),
                  (eq, ":upg_horses", 1), # we're upgrading horses
                  (this_or_next|item_has_property, ":item", itp_cant_use_on_horseback),
                  (this_or_next|item_has_property, ":item", itp_cant_reload_on_horseback),
                  (item_has_property, ":item", itp_cant_reload_while_moving_mounted),
                  (assign, ":limit", 0),
              (try_end),
              (try_for_range, ":slot_no", dplmc_slot_upgrade_wpn_0, ":limit"),
                (troop_get_slot, ":item_preference", ":troop", ":slot_no"),
                (neq, ":item_preference", 0), #not keep current
                (store_div, ":damage_type", ":item_preference", meta_dmg_mask),
                (val_mod, ":item_preference", meta_dmg_mask), #get the itp + meta
                (call_script, "script_item_get_type_aux", ":item"),
                (this_or_next|eq, ":item_preference", reg0), #either same meta-type
                (eq, ":item_preference", ":item_type"), #or matching base itp

                #check to see whether damage is preferred
                (try_begin),
                  (neq, ":damage_type", 0),
                  (item_get_swing_damage, ":swing_damage", ":item"),
                  (item_get_thrust_damage, ":thrust_damage", ":item"),
                  (try_begin),
                    (ge, ":swing_damage", ":thrust_damage"),
                    (item_get_swing_damage_type, ":item_dmg_type", ":item"),
                  (else_try),
                    (lt, ":swing_damage", ":thrust_damage"),
                    (item_get_thrust_damage_type, ":item_dmg_type", ":item"),
                  (try_end),
                  #check if it matches preference
                  (val_add, ":item_dmg_type", 1),
                  (eq, ":damage_type", ":item_dmg_type"),
                  (val_mul, ":score", 4),
                (try_end),
                #if current score is not ge, replace item and score
                (neg|troop_slot_ge, "trp_heroes_end", ":slot_no", ":score"),
                (troop_set_slot, "trp_heroes_end", ":slot_no", ":score"),
                (assign, ":limit", -1), #loop break
                (store_sub, ":item_slot", ":slot_no", dplmc_slot_upgrade_wpn_0), #ek item slots
                (troop_get_inventory_slot, ":item_no", ":troop", ":item_slot"),
                (try_begin),
                  (eq, ":item_no", -1),
                  (troop_set_inventory_slot, ":pool", ":i_slot", -1),
                (else_try), #replace into pool
                  (troop_get_inventory_slot_modifier, ":imod_no", ":troop", ":item_slot"),
                  (troop_set_inventory_slot, ":pool", ":i_slot", ":item_no"),
                  (troop_set_inventory_slot_modifier, ":pool", ":i_slot", ":imod_no"),
                (try_end),
                (troop_set_inventory_slot, ":troop", ":item_slot", ":item"),
                (troop_set_inventory_slot_modifier, ":troop", ":item_slot", ":imod"),
                # (try_begin),
                  # (str_store_item_name, s1, ":item"),
                  # (try_begin),
                    # (eq, ":item_no", -1),
                    # (str_store_string, s2, "str_dplmc_none"),
                  # (else_try),
                    # (str_store_item_name, s2, ":item_no"),
                  # (try_end),
                  # (assign, reg1, ":score"),
                  # (display_message, "@{s1} better than {s2}, score of {reg1}"),
                # (try_end),
              (try_end),
            (try_end),
        (try_end),

		# Now we know which ones are the best. Give them to the troop.
		(try_begin),
			(assign, ":best_slot", ":best_helmet_slot"),
			(ge, ":best_slot", 0),
			(troop_get_inventory_slot, ":item", ":pool", ":best_slot"),
			(ge, ":item", 0),
			(troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
			(troop_set_inventory_slot, ":troop", ek_head, ":item"),
			(troop_set_inventory_slot_modifier, ":troop", ek_head, ":imod"),
			(troop_set_inventory_slot, ":pool", ":best_slot", -1),
		(try_end),

		(try_begin),
			(assign, ":best_slot", ":best_body_slot"),
			(ge, ":best_slot", 0),
			(troop_get_inventory_slot, ":item", ":pool", ":best_slot"),
			(ge, ":item", 0),
			(troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
			(troop_set_inventory_slot, ":troop", ek_body, ":item"),
			(troop_set_inventory_slot_modifier, ":troop", ek_body, ":imod"),
			(troop_set_inventory_slot, ":pool", ":best_slot", -1),
		(try_end),

		(try_begin),
			(assign, ":best_slot", ":best_boots_slot"),
			(ge, ":best_slot", 0),
			(troop_get_inventory_slot, ":item", ":pool", ":best_slot"),
			(ge, ":item", 0),
			(troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
			(troop_set_inventory_slot, ":troop", ek_foot, ":item"),
			(troop_set_inventory_slot_modifier, ":troop", ek_foot, ":imod"),
			(troop_set_inventory_slot, ":pool", ":best_slot", -1),
		(try_end),

		(try_begin),
			(assign, ":best_slot", ":best_gloves_slot"),
			(ge, ":best_slot", 0),
			(troop_get_inventory_slot, ":item", ":pool", ":best_slot"),
			(ge, ":item", 0),
			(troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
			(troop_set_inventory_slot, ":troop", ek_gloves, ":item"),
			(troop_set_inventory_slot_modifier, ":troop", ek_gloves, ":imod"),
			(troop_set_inventory_slot, ":pool", ":best_slot", -1),
		(try_end),

		(try_begin),
			(assign, ":best_slot", ":best_horse_slot"),
			(ge, ":best_slot", 0),
			(troop_get_inventory_slot, ":item", ":pool", ":best_slot"),
			(ge, ":item", 0),
			(troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
			(troop_set_inventory_slot, ":troop", ek_horse, ":item"),
			(troop_set_inventory_slot_modifier, ":troop", ek_horse, ":imod"),
			(troop_set_inventory_slot, ":pool", ":best_slot", -1),
		(try_end),

		# (try_for_range, ":i_slot", ek_item_0, ek_head),
			# (store_add, ":trp_slot", ":i_slot", dplmc_slot_upgrade_wpn_0),
			# (troop_get_slot, ":type", ":troop", ":trp_slot"),
			# (gt, ":type", 0), #we're upgrading for this slot
			# (call_script, "script_dplmc_scan_for_best_item_of_type", ":pool", ":type", ":troop"), #search for the best
			# (assign, ":best_slot", reg0),
			# (neq, ":best_slot", -1), #got something
			# (troop_get_inventory_slot, ":item", ":pool", ":best_slot"), #get it
			# (ge, ":item", 0),
			# (troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
			# (troop_set_inventory_slot, ":pool", ":best_slot", -1), #remove from pool
			# (troop_set_inventory_slot, ":troop", ":i_slot", ":item"), #add to slot
			# (troop_set_inventory_slot_modifier, ":troop", ":i_slot", ":imod"),
		# (try_end),

        #SB : string storage
        (try_begin),
          (neq, ":sreg", -1),
          (str_store_troop_name, ":sreg", ":troop"),
          (assign, ":num_changes", 0),
          (assign, ":last_change", 0),
          #three cases : discarded item -1, no change 0, change 1 (upgraded/swapped depending on item flags)
          (try_for_range, ":i_slot", ek_item_0, ek_food),
            (troop_get_inventory_slot, ":old_item", ":pool", ":i_slot"),
            (troop_get_inventory_slot, ":new_item", ":troop", ":i_slot"),
            (try_begin),
              (gt, ":old_item", -1),
              (troop_get_inventory_slot_modifier, ":old_imod", ":pool", ":i_slot"),
              (store_add, ":imod_no", ":old_imod", "str_imod_plain"),
              # (str_store_string, s10, ":imod_no"),
              # (str_store_item_name, s20, ":old_item"),
              # (display_message, "@old:{s10}{s20}"),
            (else_try),
              (assign, ":old_imod", imod_plain),
            (try_end),
            (try_begin),
              (gt, ":new_item", -1),
              (troop_get_inventory_slot_modifier, ":new_imod", ":troop", ":i_slot"),
              (store_add, ":imod_no", ":new_imod", "str_imod_plain"),
              # (str_store_string, s10, ":imod_no"),
              # (str_store_item_name, s20, ":new_item"),
              # (display_message, "@new:{s10}{s20}"),
            (else_try),
              (assign, ":new_imod", imod_plain),
            (try_end),

            # #placeholder swap strings
            # (str_clear, s0), #sreg
            # (str_clear, s1), #new string
            # (str_clear, s10), #imod
            # (str_clear, s20), #item

            (try_begin), #keep current
              (is_between, ":i_slot", ek_item_0, ek_head),
              (store_add, ":upgrade_slot", ":i_slot", dplmc_slot_upgrade_wpn_0),
              (troop_slot_eq, ":troop", ":upgrade_slot", 0),
              (assign, ":item_changed", 0),
            (else_try), #same
              (eq, ":new_item", ":old_item"),
              (eq, ":old_imod", ":new_imod"),
              (assign, ":item_changed", 0),
            (else_try), #discarded
              (eq, ":new_item", -1),
              (gt, ":old_item", -1),
              (assign, ":item_changed", 2),
              (assign, ":item_no", ":old_item"),
              (assign, ":imod_no", ":old_imod"),
            (else_try), #swapped/equipped
              (gt, ":new_item", -1),
              (assign, ":item_changed", 1),
              (assign, ":item_no", ":new_item"),
              (assign, ":imod_no", ":new_imod"),
            (try_end),

            #build string
            (try_begin),
              (gt, ":item_changed", 0),
              (val_add, ":imod_no", "str_imod_plain"),
              (str_store_string, s10, ":imod_no"), #this comes with a space
              (str_store_item_name, s20, ":item_no"),

              (try_begin),
                (neq, ":last_change", 1),
                (eq, ":item_changed", 1),
                (str_store_string, s1, "@equipped {s10}{s20}"),
              (else_try),
                (neq, ":last_change", 2),
                (eq, ":item_changed", 2),
                (str_store_string, s1, "@discarded {s10}{s20}"),
              (else_try), #same as before, no need to qualify
                (str_store_string, s1, "@{s10}{s20}"),
              (try_end),
              (str_store_string_reg, s0, ":sreg"),
              (try_begin), #no comma for first part
                (eq, ":num_changes", 0),
                (str_store_string, ":sreg", "str_s0_s1"),
              (else_try),
                (str_store_string, ":sreg", "str_dplmc_s0_comma_s1"),
              (try_end),
              # (assign, reg1, ":num_changes"),
              # (display_message, "@{reg1} : {s1}"),
              (val_add, ":num_changes", ":item_changed"),
              (assign, ":last_change", ":item_changed"),
            (try_end),
          (try_end),
          (try_begin), #discard if we didn't touch the inventory at all
            (le, ":num_changes", 0), #this is a flag, not a count
            (str_clear, ":sreg"),
          (try_end),
        (try_end),

    # (try_end),
]),

#######################
# Search for the most expensive item of a specified type

##diplomacy start+
#"script_dplmc_scan_for_best_item_of_type"
#
#INPUT:
#   arg1 :troop
#   arg2 :item_type
#   arg3 :troop_using
#
#OUTPUT:
#   reg0 index of best item (-1 if not found)
##diplomacy end+
("dplmc_scan_for_best_item_of_type", [
	(store_script_param, ":troop",1),
	(store_script_param, ":item_type",2),
	(store_script_param, ":troop_using", 3),


    #SB : parse damage type and meta type (if any)
    # (store_div, ":dmg_type", ":item_type", meta_dmg_mask),
    (store_mod, ":meta_type", ":item_type", meta_dmg_mask), #use this instead
    (store_mod, ":item_type", ":meta_type", meta_itp_mask), #base type

    (assign, ":best_slot", -1),
    (assign, ":best_value", -1),
    # iterate through the list of items
    (troop_get_inventory_capacity, ":inv_cap", ":troop"),
    (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":item", ":troop", ":i_slot"),
        (ge, ":item", 0),
        (troop_get_inventory_slot_modifier, ":imod", ":troop", ":i_slot"),
        #(item_get_type, ":this_item_type", ":item"),  use the following instead

        # #### Autoloot improved by rubik begin
        # (try_begin),
            # # (item_slot_eq, ":item", dplmc_slot_two_handed_one_handed, 1),
            # (item_has_property, ":item", itp_type_two_handed_wpn),
            # (neg|item_has_property, ":item", itp_two_handed),
            # (assign, ":this_item_type", 11), # type 11 = two-handed/one-handed
        # (else_try),
            # (item_get_type, ":this_item_type", ":item"),
        # (try_end),
        # #### Autoloot improved by rubik end
        (call_script, "script_item_get_type_aux", ":item"), #SB : compare metatype
        (eq, ":meta_type", reg0), # it's one of the kind we're looking for (meta-type holds itp if none exists)
        (call_script, "script_dplmc_troop_can_use_item", ":troop_using", ":item", ":imod"),
        (eq, reg0, 1), # can use
        #(call_script, "script_get_item_value_with_imod", ":item", ":imod"),  # use the following instead

        #### Autoloot improved by rubik begin
        # get item_score instead of price
        (call_script, "script_dplmc_get_item_score_with_imod", ":item", ":imod"),
        #### Autoloot improved by rubik end
        (assign, ":cur_value", reg0),
        #SB : adjust value here for damage preference
        # (try_begin),
          # (call_script, "script_cf_item_type_has_advanced_autoloot", ":item_type"),
          # (item_get_swing_damage, ":swing_damage", ":item"),
          # (item_get_thrust_damage, ":thrust_damage", ":item"),
          # (try_begin),
            # (ge, ":swing_damage", ":thrust_damage"),
            # (item_get_swing_damage_type, ":item_dmg_type", ":item"),
          # (else_try),
            # (lt, ":swing_damage", ":thrust_damage"),
            # (item_get_thrust_damage_type, ":item_dmg_type", ":item"),
          # (try_end),
          # #check if it matches preference
          # (eq, ":dmg_type", ":item_dmg_type"),
          # (val_mul, ":cur_value", 3),
        # (try_end),
        (gt, ":cur_value", ":best_value"), # best one we've seen yet
        (assign, ":best_slot", ":i_slot"),
        (assign, ":best_value", ":cur_value"),
    (try_end),



    # return the slot of the best one
    (assign, reg0, ":best_slot"),
]),

##diplomacy start+
#"script_dplmc_count_better_items_of_same_type"
#
#INPUT:
#   arg1 :inventory_troop
#   arg2 :item
#   arg2 :item_imod
#   arg3 :troop_using
#
#OUTPUT:
#   reg0 number of items of same type
("dplmc_count_better_items_of_same_type", [
	(store_script_param, ":inventory_troop",1),
	(store_script_param, ":base_item",2),
	(store_script_param, ":base_imod",3),
	(store_script_param, ":troop_using", 4),

	(assign, ":number_better_of_type", 0),
	#(assign, ":total_items_of_type", 0),

	# (item_get_type, ":main_item_type", ":base_item"),
	# (try_begin),
		# (item_has_property, ":item", itp_type_two_handed_wpn),
		# (neg|item_has_property, ":item", itp_two_handed),
		# (assign, ":main_item_type", 11), # type 11 = two-handed/one-handed
	# (try_end),
    #SB : metatype
    (call_script, "script_item_get_type_aux", ":base_item"),
    (assign, ":main_item_type", reg0),

	(call_script, "script_dplmc_get_item_score_with_imod", ":base_item", ":base_imod"),
	(assign, ":primary_score", reg0),

	(call_script, "script_dplmc_troop_can_use_item", ":troop_using", ":base_item", ":base_imod"),
	(assign, ":can_use", 1),
	(try_begin),
		(neq, reg0, 1),
		(assign, ":primary_score", -1000),
		(assign, ":can_use", 0),
	(try_end),
	(assign, ":exact_matches_found", 0),

	(troop_get_inventory_capacity, ":inv_cap", ":inventory_troop"),
	(try_for_range, ":i_slot", 0, ":inv_cap"),
		(troop_get_inventory_slot, ":item", ":inventory_troop", ":i_slot"),
		(ge, ":item", 0),
        # SB : metatype
        (call_script, "script_item_get_type_aux", ":item"),
		(eq, ":main_item_type", reg0),
		#(val_add, ":total_items_of_type", 1),
		(troop_get_inventory_slot_modifier, ":imod", ":inventory_troop", ":i_slot"),
		(call_script, "script_dplmc_troop_can_use_item", ":troop_using", ":item", ":imod"),
		(this_or_next|eq, ":can_use", 0),
			(ge, reg0, 1),
		(try_begin),
			(eq, ":item", ":base_item"),
			(eq, ":imod", ":base_imod"),
			(val_add, ":exact_matches_found", 1),
		(try_end),
		(this_or_next|neq, ":item", ":base_item"),
		(this_or_next|neq, ":imod", ":base_imod"),
			(ge, ":exact_matches_found", 2),
		(call_script, "script_dplmc_get_item_score_with_imod", ":item", ":imod"),
		(ge, reg0, ":primary_score"),#deliberately ge instead of gt because of what I want this for
		(val_add, ":number_better_of_type", 1),
	(try_end),

	(assign, reg0, ":number_better_of_type"),
	#(assign, reg1, ":total_items_of_type"),
]),
##diplomacy end+
("dplmc_get_current_item_for_autoloot",
  [
    (store_script_param_1, ":slot_no"),

    #(try_begin),
      (assign, ":dest_slot", ":slot_no"),
      (troop_get_inventory_slot, ":item", "$temp", ":dest_slot"),
    #(else_try),
    #  (store_sub, ":dest_slot", "$temp", companions_begin),
    #  (val_mul, ":dest_slot", 4),
    #  (val_add, ":dest_slot", 10),
    #  (val_add, ":dest_slot", ":slot_no"),
    #  (troop_get_inventory_slot, ":item", "trp_merchants_end", ":dest_slot"),
    #(try_end),
    (try_begin),
      (ge, ":item", 0),
      (str_store_item_name, s10, ":item"),
    (else_try),
      (str_store_string, s10, "str_dplmc_none"),
    (try_end),
  ]),

  ("dplmc_get_troop_max_hp",
   [
    (store_script_param_1, ":troop"),

    (store_skill_level, ":skill", skl_ironflesh, ":troop"),
    (store_attribute_level, ":attrib", ":troop", ca_strength),
    (val_mul, ":skill", 2),
    (val_add, ":skill", ":attrib"),
    (val_add, ":skill", 35),
    (assign, reg0, ":skill"),
  ]),
  #cc end
("dplmc_pay_into_treasury",
    [
      (store_script_param_1, ":amount"),
      (troop_add_gold, "trp_household_possessions", ":amount"),
      (assign, reg0, ":amount"),
      (play_sound, "snd_money_received"),
      (display_message, "@{reg0} denars added to treasury."),
  ]),

  ("dplmc_withdraw_from_treasury",
    [
      (store_script_param_1, ":amount"),
      (troop_remove_gold, "trp_household_possessions", ":amount"),
      (assign, reg0, ":amount"),
      (play_sound, "snd_money_paid"),
      (display_message, "@{reg0} denars removed from treasury."),
  ]),

  ("dplmc_describe_tax_rate_to_s50",
    [
      (store_script_param_1, ":tax_rate"),
      (val_div, ":tax_rate", 25),
      (store_add, ":str_id","str_dplmc_tax_normal", ":tax_rate"),
      (str_store_string, s50, ":str_id"),
  ]),


  ("dplmc_player_troops_leave",
   [
    (store_script_param_1, ":percent"),

    (try_begin),#debug
     (eq, "$cheat_mode", 1),
     (assign, reg0, ":percent"),
     (display_message, "@{!}DEBUG : removing player troops: {reg0}%"),
    (try_end),

    (assign, ":deserters", 0),
    (try_for_parties, ":party_no"),
      (assign, ":remove_troops", 0),
      (try_begin),
        (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_town),
        (party_slot_eq, ":party_no", slot_party_type, spt_castle),
        (party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
        (assign, ":remove_troops", 1),
      (else_try),
         (eq, "p_main_party", ":party_no"),
         (assign, ":remove_troops", 1),
      (try_end),

      (eq, ":remove_troops", 1),
      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
        (val_mul, ":stack_size", ":percent"),
        (val_div, ":stack_size", 100),
        (party_stack_get_troop_id, ":troop_id", ":party_no", ":i_stack"),
        (party_remove_members, ":party_no", ":troop_id", ":stack_size"),
        (val_add, ":deserters", ":stack_size"),
      (try_end),
    (try_end),
    (assign, reg0, ":deserters"),
   ]
  ),

  ("dplmc_party_calculate_strength",
    [
      (store_script_param_1, ":party"), #Party_id
      (store_script_param_2, ":exclude_leader"), #Party_id

      (assign, reg0,0),
      (party_get_num_companion_stacks, ":num_stacks", ":party"),
      (assign, ":first_stack", 0),
      (try_begin),
        (neq, ":exclude_leader", 0),
        (assign, ":first_stack", 1),
      (try_end),

      (assign, ":sum", 0),
      (try_for_range, ":i_stack", ":first_stack", ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party", ":i_stack"),

        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size",":party",":i_stack"),
        (try_end),
        (val_add, ":sum", ":stack_size"),
      (try_end),
      (assign, reg0, ":sum"),

      (try_begin), #debug
        (eq, "$cheat_mode", 1),
        (display_message, "@{!}DEBUG : sum: {reg0}"),
      (try_end),
  ]),

#script_dplmc_start_alliance_between_kingdoms, 20 days alliance, 40 days truce after that
  # Input: arg1 = kingdom_1, arg2 = kingdom_2, arg3 = initializing_war_peace_cond
  # Output: none
  ("dplmc_start_alliance_between_kingdoms", #sets relations between two kingdoms
    [
      (store_script_param, ":kingdom_a", 1),
      (store_script_param, ":kingdom_b", 2),
      (store_script_param, ":initializing_war_peace_cond", 3),
	  ##diplomacy start+
	  #Since "fac_player_supporters_faction" is used as a shorthand for the faction
	  #run by the player, intercept that here instead of the various places this is
	  #called from.
	  (assign, ":save_reg1", reg1),
	  (call_script, "script_dplmc_translate_inactive_player_supporter_faction_2", ":kingdom_a", ":kingdom_b"),
	  (assign, ":kingdom_a", reg0),
	  (assign, ":kingdom_b", reg1),
	  (assign, reg1, ":save_reg1"),
	  ##diplomacy end+

      (store_relation, ":relation", ":kingdom_a", ":kingdom_b"),
      (val_add, ":relation", 15),
      (val_max, ":relation", 40),
      (set_relation, ":kingdom_a", ":kingdom_b", ":relation"),
      (call_script, "script_exchange_prisoners_between_factions", ":kingdom_a", ":kingdom_b"),

      (try_begin),
        (eq, "$players_kingdom", ":kingdom_a"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_b"),
        (val_add, ":relation", 15),
        (val_max, ":relation", 40),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_b", ":relation"),
        #(call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", "fac_player_supporters_faction"), #event cancels certain quests
      (else_try),
        (eq, "$players_kingdom", ":kingdom_b"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_a"),
        (val_add, ":relation", 15),
        (val_max, ":relation", 40),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_a", ":relation"),
        #(call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", "fac_player_supporters_faction"), #event cancels certain quests
      (try_end),

      (try_begin),
        (eq, ":initializing_war_peace_cond", 1),
        (str_store_faction_name_link, s1, ":kingdom_a"),
        (str_store_faction_name_link, s2, ":kingdom_b"),
		##diplomacy start+ #Due to complaints about the wording
        #(display_log_message, "@{s1} and {s2} have concluded an alliance with each other."),
		(display_log_message, "@{s1} and {s2} have entered into an alliance with each other."),
		##diplomacy end+

        (call_script, "script_add_notification_menu", "mnu_dplmc_notification_alliance_declared", ":kingdom_a", ":kingdom_b"), #stability penalty for early peace is in the menu

        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", ":kingdom_b"), #cancels quests
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", ":kingdom_a"), #cancels quests
        (assign, "$g_recalculate_ais", 1),


      (try_end),

	  (try_begin), #add truce
		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
	    ##nested diplomacy start+ replace 80 with a named constant
	    #(faction_set_slot, ":kingdom_b", ":truce_slot", 80),
	    (faction_set_slot, ":kingdom_b", ":truce_slot", dplmc_treaty_alliance_days_initial),
	    ##nested diplomacy end+

		(store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
	    ##nested diplomacy start+ replace 80 with a named constant
	    #(faction_set_slot, ":kingdom_a", ":truce_slot", 80),
	    (faction_set_slot, ":kingdom_a", ":truce_slot", dplmc_treaty_alliance_days_initial),
	    ##nested diplomacy end+

		(store_add, ":slot_war_damage_inflicted_on_b", ":kingdom_b", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_b", kingdoms_begin),
		(faction_get_slot, ":damage_inflicted_by_a", ":kingdom_a", ":slot_war_damage_inflicted_on_b"),
		(try_begin),
			(lt, ":damage_inflicted_by_a", 100),
			#controversial policy
		(try_end),
		(faction_set_slot, ":kingdom_a", ":slot_war_damage_inflicted_on_b", 0),

		(store_add, ":slot_war_damage_inflicted_on_a", ":kingdom_a", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_a", kingdoms_begin),
		(faction_get_slot, ":damage_inflicted_by_b", ":kingdom_b", ":slot_war_damage_inflicted_on_a"),
		(try_begin),
			(lt, ":damage_inflicted_by_b", 100),
			#controversial policy
		(try_end),
		(faction_set_slot, ":kingdom_b", ":slot_war_damage_inflicted_on_a", 0),

	  (try_end),

    # share wars
    (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
      (neq, ":kingdom_a", ":faction_no"),
      (neq, ":kingdom_b", ":faction_no"),
      (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction",":kingdom_a", ":faction_no"),
      #result: -1 faction_1 has a casus belli against faction_2. 1, faction_1 has a truce with faction_2, -2, the two factions are at war
      (eq, reg0, -2),
      (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction",":kingdom_b", ":faction_no"),
      (ge, reg0, -1),
      (call_script, "script_diplomacy_start_war_between_kingdoms", ":kingdom_b", ":faction_no", 2),
    (try_end),
    (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
      (neq, ":kingdom_a", ":faction_no"),
      (neq, ":kingdom_b", ":faction_no"),
      (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction",":kingdom_b", ":faction_no"),
      #result: -1 faction_1 has a casus belli against faction_2. 1, faction_1 has a truce with faction_2, -2, the two factions are at war
      (eq, reg0, -2),
      (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction",":kingdom_a", ":faction_no"),
      (ge, reg0, -1),
      (call_script, "script_diplomacy_start_war_between_kingdoms", ":kingdom_a", ":faction_no", 2),
    (try_end),
  ]),

#script_dplmc_start_defensive_between_kingdoms, 20 days defensive: 20 days trade aggreement, 20 days non-aggression after that
  # Input: arg1 = kingdom_1, arg2 = kingdom_2, arg3 = initializing_war_peace_cond
  # Output: none
  ("dplmc_start_defensive_between_kingdoms", #sets relations between two kingdoms
    [
      (store_script_param, ":kingdom_a", 1),
      (store_script_param, ":kingdom_b", 2),
      (store_script_param, ":initializing_war_peace_cond", 3),
	  ##diplomacy start+
	  #Since "fac_player_supporters_faction" is used as a shorthand for the faction
	  #run by the player, intercept that here instead of the various places this is
	  #called from.
	  (assign, ":save_reg1", reg1),
	  (call_script, "script_dplmc_translate_inactive_player_supporter_faction_2", ":kingdom_a", ":kingdom_b"),
	  (assign, ":kingdom_a", reg0),
	  (assign, ":kingdom_b", reg1),
	  (assign, reg1, ":save_reg1"),
	  ##diplomacy end+

      (store_relation, ":relation", ":kingdom_a", ":kingdom_b"),
      (val_add, ":relation", 10),
      (val_max, ":relation", 30),
      (set_relation, ":kingdom_a", ":kingdom_b", ":relation"),
      (call_script, "script_exchange_prisoners_between_factions", ":kingdom_a", ":kingdom_b"),

      (try_begin),
        (eq, "$players_kingdom", ":kingdom_a"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_b"),
        (val_add, ":relation", 10),
        (val_max, ":relation", 30),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_b", ":relation"),
        #(call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", "fac_player_supporters_faction"), #event cancels certain quests
      (else_try),
        (eq, "$players_kingdom", ":kingdom_b"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_a"),
        (val_add, ":relation", 10),
        (val_max, ":relation", 30),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_a", ":relation"),
        #(call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", "fac_player_supporters_faction"), #event cancels certain quests
      (try_end),

      (try_begin),
        (eq, ":initializing_war_peace_cond", 1),
        (str_store_faction_name_link, s1, ":kingdom_a"),
        (str_store_faction_name_link, s2, ":kingdom_b"),
        (display_log_message, "@{s1} and {s2} have concluded a defensive pact with each other."),

        (call_script, "script_add_notification_menu", "mnu_dplmc_notification_defensive_declared", ":kingdom_a", ":kingdom_b"), #stability penalty for early peace is in the menu

        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", ":kingdom_b"), #cancels quests
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", ":kingdom_a"), #cancels quests
        (assign, "$g_recalculate_ais", 1),


      (try_end),

	  (try_begin), #add truce
		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
	    ##diplomacy start+ replace 60 with named variable
	    #(faction_set_slot, ":kingdom_b", ":truce_slot", 60),
	    (faction_set_slot, ":kingdom_b", ":truce_slot", dplmc_treaty_defense_days_initial),
	    ##diplomacy end+

		(store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
	    ##diplomacy start+ replace 60 with named variable
	    #(faction_set_slot, ":kingdom_a", ":truce_slot", 60),
	    (faction_set_slot, ":kingdom_a", ":truce_slot", dplmc_treaty_defense_days_initial),
	    ##diplomacy end+

		(store_add, ":slot_war_damage_inflicted_on_b", ":kingdom_b", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_b", kingdoms_begin),
		(faction_get_slot, ":damage_inflicted_by_a", ":kingdom_a", ":slot_war_damage_inflicted_on_b"),
		(try_begin),
			(lt, ":damage_inflicted_by_a", 100),
			#controversial policy
		(try_end),
		(faction_set_slot, ":kingdom_a", ":slot_war_damage_inflicted_on_b", 0),

		(store_add, ":slot_war_damage_inflicted_on_a", ":kingdom_a", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_a", kingdoms_begin),
		(faction_get_slot, ":damage_inflicted_by_b", ":kingdom_b", ":slot_war_damage_inflicted_on_a"),
		(try_begin),
			(lt, ":damage_inflicted_by_b", 100),
			#controversial policy
		(try_end),
		(faction_set_slot, ":kingdom_b", ":slot_war_damage_inflicted_on_a", 0),

	  (try_end),
  ]),

#script_dplmc_start_trade_between_kingdoms, 20 days trade aggreement, 20 days non-aggression after that
  # Input: arg1 = kingdom_1, arg2 = kingdom_2, arg3 = initializing_war_peace_cond
  # Output: none
  ("dplmc_start_trade_between_kingdoms", #sets relations between two kingdoms
    [
      (store_script_param, ":kingdom_a", 1),
      (store_script_param, ":kingdom_b", 2),
      (store_script_param, ":initializing_war_peace_cond", 3),
	  ##diplomacy start+
	  #Since "fac_player_supporters_faction" is used as a shorthand for the faction
	  #run by the player, intercept that here instead of the various places this is
	  #called from.
	  (assign, ":save_reg1", reg1),
	  (call_script, "script_dplmc_translate_inactive_player_supporter_faction_2", ":kingdom_a", ":kingdom_b"),
	  (assign, ":kingdom_a", reg0),
	  (assign, ":kingdom_b", reg1),
	  (assign, reg1, ":save_reg1"),
	  ##diplomacy end+

      (store_relation, ":relation", ":kingdom_a", ":kingdom_b"),
      (val_add, ":relation", 5),
      (val_max, ":relation", 20),
      (set_relation, ":kingdom_a", ":kingdom_b", ":relation"),
      (call_script, "script_exchange_prisoners_between_factions", ":kingdom_a", ":kingdom_b"),

      (try_begin),
        (eq, "$players_kingdom", ":kingdom_a"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_b"),
        (val_add, ":relation", 5),
        (val_max, ":relation", 20),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_b", ":relation"),
        #(call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", "fac_player_supporters_faction"), #event cancels certain quests
      (else_try),
        (eq, "$players_kingdom", ":kingdom_b"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_a"),
        (val_add, ":relation", 5),
        (val_max, ":relation", 20),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_a", ":relation"),
        #(call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", "fac_player_supporters_faction"), #event cancels certain quests
      (try_end),

      (try_begin),
        (eq, ":initializing_war_peace_cond", 1),
        (str_store_faction_name_link, s1, ":kingdom_a"),
        (str_store_faction_name_link, s2, ":kingdom_b"),
        (display_log_message, "@{s1} and {s2} have concluded a trade agreement with each other."),

        (call_script, "script_add_notification_menu", "mnu_dplmc_notification_trade_declared", ":kingdom_a", ":kingdom_b"), #stability penalty for early peace is in the menu

        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", ":kingdom_b"), #cancels quests
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", ":kingdom_a"), #cancels quests
        (assign, "$g_recalculate_ais", 1),


      (try_end),

	  (try_begin), #add truce
		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
	    ##nested diplomacy start+ replace hardcoded number of days with a variable
	    #(faction_set_slot, ":kingdom_b", ":truce_slot", 40),
	    (faction_set_slot, ":kingdom_b", ":truce_slot", dplmc_treaty_trade_days_initial),
	    ##nested diplomacy end+

		(store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
	    ##nested diplomacy start+ replace hardcoded number of days with a variable
	    #(faction_set_slot, ":kingdom_a", ":truce_slot", 40),
	    (faction_set_slot, ":kingdom_a", ":truce_slot", dplmc_treaty_trade_days_initial),
	    ##nested diplomacy end+

		(store_add, ":slot_war_damage_inflicted_on_b", ":kingdom_b", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_b", kingdoms_begin),
		(faction_get_slot, ":damage_inflicted_by_a", ":kingdom_a", ":slot_war_damage_inflicted_on_b"),
		(try_begin),
			(lt, ":damage_inflicted_by_a", 100),
			#controversial policy
		(try_end),
		(faction_set_slot, ":kingdom_a", ":slot_war_damage_inflicted_on_b", 0),

		(store_add, ":slot_war_damage_inflicted_on_a", ":kingdom_a", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_a", kingdoms_begin),
		(faction_get_slot, ":damage_inflicted_by_b", ":kingdom_b", ":slot_war_damage_inflicted_on_a"),
		(try_begin),
			(lt, ":damage_inflicted_by_b", 100),
			#controversial policy
		(try_end),
		(faction_set_slot, ":kingdom_b", ":slot_war_damage_inflicted_on_a", 0),

	  (try_end),
  ]),

#script_dplmc_start_nonaggression_between_kingdoms, 20 days non-aggression
  # Input: arg1 = kingdom_1, arg2 = kingdom_2, arg3 = initializing_war_peace_cond
  # Output: none
  ("dplmc_start_nonaggression_between_kingdoms", #sets relations between two kingdoms
    [
      (store_script_param, ":kingdom_a", 1),
      (store_script_param, ":kingdom_b", 2),
      (store_script_param, ":initializing_war_peace_cond", 3),
	  ##diplomacy start+
	  #Since "fac_player_supporters_faction" is used as a shorthand for the faction
	  #run by the player, intercept that here instead of the various places this is
	  #called from.
	  (assign, ":save_reg1", reg1),
	  (call_script, "script_dplmc_translate_inactive_player_supporter_faction_2", ":kingdom_a", ":kingdom_b"),
	  (assign, ":kingdom_a", reg0),
	  (assign, ":kingdom_b", reg1),
	  (assign, reg1, ":save_reg1"),
	  ##diplomacy end+

      (store_relation, ":relation", ":kingdom_a", ":kingdom_b"),
      (val_add, ":relation", 3),
      (val_max, ":relation", 10),
      (set_relation, ":kingdom_a", ":kingdom_b", ":relation"),
      (call_script, "script_exchange_prisoners_between_factions", ":kingdom_a", ":kingdom_b"),

      (try_begin),
        (eq, "$players_kingdom", ":kingdom_a"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_b"),
        (val_add, ":relation", 3),
        (val_max, ":relation", 10),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_b", ":relation"),
        #(call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", "fac_player_supporters_faction"), #event cancels certain quests
      (else_try),
        (eq, "$players_kingdom", ":kingdom_b"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_a"),
        (val_add, ":relation", 3),
        (val_max, ":relation", 10),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_a", ":relation"),
        #(call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", "fac_player_supporters_faction"), #event cancels certain quests
      (try_end),

      (try_begin),
        (eq, ":initializing_war_peace_cond", 1),
        (str_store_faction_name_link, s1, ":kingdom_a"),
        (str_store_faction_name_link, s2, ":kingdom_b"),
        (display_log_message, "@{s1} and {s2} have concluded a non aggression pact with each other."),

        (call_script, "script_add_notification_menu", "mnu_dplmc_notification_nonaggression_declared", ":kingdom_a", ":kingdom_b"), #stability penalty for early peace is in the menu

        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", ":kingdom_b"), #cancels quests
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", ":kingdom_a"), #cancels quests
        (assign, "$g_recalculate_ais", 1),


      (try_end),

	  (try_begin), #add truce
		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
	    ##nested diplomacy start+ replace hardcoded number with a variable
	    #(faction_set_slot, ":kingdom_b", ":truce_slot", 20),
	    (faction_set_slot, ":kingdom_b", ":truce_slot", dplmc_treaty_truce_days_initial),
	    ##nested diplomacy end+

		(store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
	    ##nested diplomacy start+ replace hardcoded number with a variable
	    #(faction_set_slot, ":kingdom_a", ":truce_slot", 20),
	    (faction_set_slot, ":kingdom_a", ":truce_slot", dplmc_treaty_truce_days_initial),
	    ##nested diplomacy end+

		(store_add, ":slot_war_damage_inflicted_on_b", ":kingdom_b", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_b", kingdoms_begin),
		(faction_get_slot, ":damage_inflicted_by_a", ":kingdom_a", ":slot_war_damage_inflicted_on_b"),
		(try_begin),
			(lt, ":damage_inflicted_by_a", 100),
			#controversial policy
		(try_end),
		(faction_set_slot, ":kingdom_a", ":slot_war_damage_inflicted_on_b", 0),

		(store_add, ":slot_war_damage_inflicted_on_a", ":kingdom_a", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_a", kingdoms_begin),
		(faction_get_slot, ":damage_inflicted_by_b", ":kingdom_b", ":slot_war_damage_inflicted_on_a"),
		(try_begin),
			(lt, ":damage_inflicted_by_b", 100),
			#controversial policy
		(try_end),
		(faction_set_slot, ":kingdom_b", ":slot_war_damage_inflicted_on_a", 0),

	  (try_end),
  ]),



# Input: arg1 = faction_no_1, arg2 = faction_no_2
("dplmc_send_messenger_to_troop",
  [
    (store_script_param, ":target_troop", 1),
    (store_script_param, ":message", 2),
    (store_script_param, ":orders_object", 3),

    #SB : correcting destination for lords waiting to respawn
    (troop_get_slot, ":target_party", ":target_troop", slot_troop_leaded_party),
    (try_begin),
      (le, ":target_party", 0),
      (call_script, "script_lord_get_home_center", ":target_troop"),
      (assign, ":target_party", reg0),
    (try_end),

    (set_spawn_radius, 1),
    (spawn_around_party, "$current_town", "pt_messenger_party"),
    (assign,":spawned_party",reg0),
    #SB : factionalized messenger
    (store_faction_of_party, ":faction_no", ":target_party"),
    (try_begin),
      (eq, ":faction_no", "fac_player_supporters_faction"),
      (is_between, "$g_player_culture", npc_kingdoms_begin, kingdoms_end),
      (assign, ":faction_no", "$g_player_culture"),
    (try_end),
    (try_begin),
      (is_between, ":faction_no", npc_kingdoms_begin, kingdoms_end),
      (faction_get_slot, ":messenger_troop", ":faction_no", slot_faction_messenger_troop),
    (else_try),
      (assign, ":messenger_troop", "trp_dplmc_messenger"),
    (try_end),
    (party_add_members, ":spawned_party", ":messenger_troop", 1),


    (try_begin),
      (eq, ":message", spai_accompanying_army),
      (assign, ":orders_object", "p_main_party"),
    (try_end),

    # (party_add_members, ":spawned_party", "trp_dplmc_messenger", 1),
    (store_faction_of_troop, ":player_faction", "trp_player"),
    (party_set_faction, ":spawned_party", ":player_faction"),
    (party_set_slot, ":spawned_party", slot_party_type, spt_messenger),
    (party_set_slot, ":spawned_party", dplmc_slot_party_mission_diplomacy, ":message"),
    (party_set_slot, ":spawned_party", slot_party_home_center, "$current_town"),

    (party_set_ai_behavior, ":spawned_party", ai_bhvr_travel_to_party),
    (party_set_ai_object, ":spawned_party", ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_object, ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_orders_object, ":orders_object"),
    #SB : cache the actual troop while going towards known center
    (party_set_slot, ":spawned_party", dplmc_slot_party_origin, ":target_troop"),

    (try_begin), #debug
      (eq, "$cheat_mode", 1),
      (str_store_party_name, s13, ":target_party"),
      (display_message, "@{!}DEBUG - Send message to {s13}"),
    (try_end),
  ]
  ),

  ("dplmc_send_messenger_to_party",
  [
    (store_script_param, ":target_party", 1),
    (store_script_param, ":message", 2),
    (store_script_param, ":orders_object", 3),

    (set_spawn_radius, 1),
    (spawn_around_party, "$current_town", "pt_messenger_party"),
    (assign, ":spawned_party", reg0),

    #SB : factionalized messenger
    (store_faction_of_party, ":faction_no", ":target_party"),
    (try_begin),
      (eq, ":faction_no", "fac_player_supporters_faction"),
      (is_between, "$g_player_culture", npc_kingdoms_begin, kingdoms_end),
      (assign, ":faction_no", "$g_player_culture"),
    (try_end),

    (try_begin),
      (is_between, ":faction_no", npc_kingdoms_begin, kingdoms_end),
      (faction_get_slot, ":messenger_troop", ":faction_no", slot_faction_messenger_troop),
    (else_try),
      (assign, ":messenger_troop", "trp_dplmc_messenger"),
    (try_end),
    (party_add_members, ":spawned_party", ":messenger_troop", 1),
    (party_set_faction, ":spawned_party", "fac_player_faction"),
    (party_set_slot, ":spawned_party", slot_party_type, spt_messenger),
    (party_set_slot, ":spawned_party", dplmc_slot_party_mission_diplomacy, ":message"),
    (party_set_slot, ":spawned_party", slot_party_home_center, "$current_town"),

    (party_set_ai_behavior, ":spawned_party", ai_bhvr_travel_to_party),
    (party_set_ai_object, ":spawned_party", ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_object, ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_orders_object, ":orders_object"),

    (try_begin), #debug
      (eq, "$cheat_mode", 1),
      (str_store_party_name, s13, ":target_party"),
      (display_message, "@{!}DEBUG - Send message to {s13}"),
    (try_end),
  ]
  ),

  ("dplmc_send_gift",
    [
    (store_script_param, ":target_troop", 1),
    (store_script_param, ":gift", 2),
    (store_script_param, ":amount", 3),

    (try_begin),
      (troop_slot_eq, ":target_troop", slot_troop_occupation, slto_kingdom_hero),
      (troop_get_slot, ":target_party", ":target_troop", slot_troop_leaded_party),
    (else_try),
      (troop_slot_eq, ":target_troop", slot_troop_occupation, slto_kingdom_lady),
      (troop_get_slot, ":target_party", ":target_troop", slot_troop_cur_center),
    (try_end),


    (try_begin), #debug
      (eq, "$cheat_mode", 1),
      (str_store_item_name, s12, ":gift"),
      (str_store_party_name, s13, ":target_party"),
      (display_message, "@{!}DEBUG - Bring {s12} to {s13}"),
    (try_end),

    (try_begin),
       #Guard against this being called without an explicit amount
       (lt, ":amount", 1),
       (display_message, "@{!} ERROR: Bad gift amount {reg0}.  (Tell the mod writer he needs to update his code.)  Using a safe default."),
       (assign, ":amount", 1),
       (troop_slot_eq, ":target_troop", slot_troop_occupation, slto_kingdom_hero),
       (assign, ":amount", 150),
    (try_end),
    (assign, ":original_amount", ":amount"),#Save this here because amount gets modified below!

    (call_script, "script_dplmc_withdraw_from_treasury", 50),
    (troop_get_inventory_capacity, ":capacity", "trp_household_possessions"),

  	  (try_for_range, ":inventory_slot", 0, ":capacity"),
  	    (gt, ":amount", 0),
  		  (troop_get_inventory_slot, ":item", "trp_household_possessions", ":inventory_slot"),
  		  (eq, ":item", ":gift"),
  		  (troop_inventory_slot_get_item_amount, ":tmp_amount", "trp_household_possessions", ":inventory_slot"),
  		  (try_begin),
  		    (le, ":tmp_amount", ":amount"),
  		    (troop_inventory_slot_set_item_amount, "trp_household_possessions", ":inventory_slot", 0),
  		    (val_sub, ":amount", ":tmp_amount"),
  		  (else_try),
  		    (val_sub, ":tmp_amount", ":amount"),
  		    (troop_inventory_slot_set_item_amount, "trp_household_possessions", ":inventory_slot", ":tmp_amount"),
  		    (assign, ":amount", 0),
  		  (try_end),
  	  (try_end),

    (set_spawn_radius, 1),
    (spawn_around_party, "$current_town", "pt_dplmc_gift_caravan"),
    (assign,":spawned_party",reg0),
    (party_set_slot, ":spawned_party", slot_party_type, dplmc_spt_gift_caravan),
    (party_set_slot, ":spawned_party", dplmc_slot_party_mission_diplomacy, ":gift"),
    (party_set_slot, ":spawned_party",  slot_party_orders_object,  ":target_troop"),

    (party_set_ai_behavior, ":spawned_party", ai_bhvr_travel_to_party),
    (party_set_ai_object, ":spawned_party", ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_object, ":target_party"),
    (party_stack_get_troop_id, ":caravan_master", ":spawned_party", 0),
    (troop_set_slot, ":caravan_master", slot_troop_leaded_party, ":spawned_party"),
    (party_set_slot, ":spawned_party", dplmc_slot_party_mission_parameter_1, ":original_amount"),
    ]),

  ("dplmc_send_patrol",
  [
    (store_script_param, ":start_party", 1),
    (store_script_param, ":target_party", 2),
    (store_script_param, ":size", 3), #0 small, 1 medium, 2, big, 3 elite
    (store_script_param, ":template_faction", 4),
    (store_script_param, ":order_troop", 5),

    (set_spawn_radius, 1),
    (spawn_around_party, ":start_party", "pt_patrol_party"),
    (assign,":spawned_party",reg0),
    (party_set_faction, ":spawned_party", ":template_faction"),
    (party_set_slot, ":spawned_party", slot_party_type, spt_patrol),
    (party_set_slot, ":spawned_party", slot_party_home_center, ":start_party"),
    (party_set_slot, ":spawned_party", dplmc_slot_party_mission_diplomacy, ":order_troop"),
    (str_store_party_name, s5, ":target_party"),
    (party_set_name, ":spawned_party", "str_s5_patrol"),

    (party_set_ai_behavior, ":spawned_party", ai_bhvr_travel_to_party),
    (party_set_ai_object, ":spawned_party", ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_object, ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_state, spai_patrolling_around_center),

    (try_begin),
      (neg|is_between, ":template_faction", npc_kingdoms_begin, npc_kingdoms_end),

      (party_get_slot, ":template_faction", ":start_party", slot_center_original_faction),
      (try_begin),
        (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
        (assign, ":template_faction", "$g_player_culture"),
      (else_try),
        (party_get_slot, ":town_lord", ":start_party", slot_town_lord),
        (gt, ":town_lord", 0),
        (troop_get_slot, ":template_faction", ":town_lord", slot_troop_original_faction),
      (try_end),

      (try_begin),
        (eq, ":size", 0),
        (call_script, "script_dplmc_withdraw_from_treasury", 1000),
      (else_try),
        (this_or_next|eq, ":size", 1),
        (eq, ":size", 3),
        (call_script, "script_dplmc_withdraw_from_treasury", 2000),
      (else_try),
        (eq, ":size", 2),
        (call_script, "script_dplmc_withdraw_from_treasury", 3000),
      (try_end),
    (try_end),

    (faction_get_slot, ":party_template_a", ":template_faction", slot_faction_reinforcements_a),
    (faction_get_slot, ":party_template_b", ":template_faction", slot_faction_reinforcements_b),
    (faction_get_slot, ":party_template_c", ":template_faction", slot_faction_reinforcements_c),

    (try_begin),
      (eq, ":size", 3),
      (party_add_template, ":spawned_party", ":party_template_c"),
      (party_add_template, ":spawned_party", ":party_template_c"),
    (else_try),
      (val_add, ":size", 1),
      (val_mul, ":size", 2),
      (try_for_range, ":cur_i", 0, ":size"),
        (store_random_in_range, ":random", 0, 3),
        (try_begin),
          (eq, ":random", 0),
          (party_add_template, ":spawned_party", ":party_template_a"),
        (else_try),
          (eq, ":random", 1),
          (party_add_template, ":spawned_party", ":party_template_b"),
        (else_try),
          (party_add_template, ":spawned_party", ":party_template_c"),
        (try_end),

        (try_begin), #debug
          (eq, "$cheat_mode", 1),
          (assign, reg0, ":cur_i"),
          (str_store_faction_name, s7, ":template_faction"),
          (display_message, "@{!}DEBUG - Added {reg0}.template of faction {s7} to patrol."),
        (try_end),
      (try_end),
    (try_end),


    (try_begin), #debug
      (eq, "$cheat_mode", 1),
      (str_store_party_name, s13, ":target_party"),
      (str_store_faction_name, s14, ":template_faction"),
      (str_store_party_name, s15, ":start_party"),
      (display_message, "@{!}DEBUG - Send {s14} patrol from {s15} to {s13}"),
    (try_end),
  ]),

  ("dplmc_send_patrol_party",
  [
    (store_script_param, ":start_party", 1),
    (store_script_param, ":target_party", 2),
    (store_script_param, ":party_no", 3),
    (store_script_param, ":template_faction", 4),

    (set_spawn_radius, 1),
    (spawn_around_party, ":start_party", "pt_patrol_party"),
    (assign,":spawned_party",reg0),
    (party_set_faction, ":spawned_party", ":template_faction"),
    (party_set_slot, ":spawned_party", slot_party_type, spt_patrol),
    (party_set_slot, ":spawned_party", slot_party_home_center, ":start_party"),
    (str_store_party_name, s5, ":target_party"),
    (party_set_name, ":spawned_party", "str_s5_patrol"),

    (party_set_ai_behavior, ":spawned_party", ai_bhvr_travel_to_party),
    (party_set_ai_object, ":spawned_party", ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_object, ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_state, spai_patrolling_around_center),

    (call_script, "script_party_add_party", ":spawned_party", ":party_no"),
  ]),

  ("dplmc_move_troops_party",
  [
    (store_script_param, ":start_party", 1),
    (store_script_param, ":target_party", 2),
    (store_script_param, ":party_no", 3),
    (store_script_param, ":template_faction", 4),

    (set_spawn_radius, 1),
    (spawn_around_party, ":start_party", "pt_patrol_party"),
    (assign,":spawned_party",reg0),
    (party_set_faction, ":spawned_party", ":template_faction"),
    (party_set_slot, ":spawned_party", slot_party_type, spt_patrol),
    (party_set_slot, ":spawned_party", slot_party_home_center, ":start_party"),
    (str_store_party_name, s5, ":target_party"),
    #SB : fixed string
    (party_set_name, ":spawned_party", "str_s5_transfer"),

    (party_set_ai_behavior, ":spawned_party", ai_bhvr_travel_to_party),
    (party_set_ai_object, ":spawned_party", ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_object, ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_state, spai_retreating_to_center),
    (party_set_aggressiveness, ":spawned_party", 0),
    (party_set_courage, ":spawned_party", 3),
    (party_set_ai_initiative, ":spawned_party", 100),

    (call_script, "script_party_add_party", ":spawned_party", ":party_no"),
  ]),

  ("dplmc_send_scout_party",
  [
    (store_script_param, ":start_party", 1),
    (store_script_param, ":target_party", 2),
    (store_script_param, ":faction", 3),

    (set_spawn_radius, 1),
    (spawn_around_party, ":start_party", "pt_scout_party"),
    (assign,":spawned_party",reg0),
    (party_set_faction, ":spawned_party", ":faction"),
    (party_set_slot, ":spawned_party", slot_party_type, spt_scout),
    (party_set_slot, ":spawned_party", slot_party_home_center, ":start_party"),
    (str_store_party_name, s5, ":target_party"),
    (party_set_name, ":spawned_party", "str_s5_scout"),

    (party_add_members, ":spawned_party", "trp_dplmc_scout", 1),

    (party_get_position, pos1, ":target_party"),
    (map_get_random_position_around_position, pos2, pos1, 1),
    (party_set_ai_behavior, ":spawned_party", ai_bhvr_travel_to_point),
    (party_set_ai_target_position, ":spawned_party", pos2),
    (party_set_slot, ":spawned_party", slot_party_ai_object, ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_orders_object, ":target_party"),
    (party_set_aggressiveness, ":spawned_party", 0),
    (party_set_courage, ":spawned_party", 3),
    (party_set_ai_initiative, ":spawned_party", 100),
  ]),

  ("dplmc_affiliate_end",
  [
    (store_script_param, ":cause", 1),

    (assign, "$g_player_affiliated_troop", 0),

    (try_begin),
      (eq, ":cause", 1),
      (assign, ":max_penalty", -16),
      (assign, ":term", 20),
      (assign, ":honor_val", 10),
    (else_try),
      (assign, ":max_penalty", -12),
      (assign, ":honor_val", 5),
      (assign, ":term", 15),
    (try_end),

    (try_for_range, ":family_member", lords_begin, kingdom_ladies_end),
      (call_script, "script_dplmc_is_affiliated_family_member", ":family_member"),
      (gt, reg0, 0),

      (store_skill_level, ":value", "skl_persuasion", "trp_player"),
      (store_random_in_range, ":value", 0, ":value"),
      ##nested diplomacy start+   Fix mistake.
      ##
      ##OLD:
      #(val_add, ":value", ":max_penalty", ":value"),
      #
      #NEW:
      #I'm pretty sure this is what was intended.
      (val_add, ":value", ":max_penalty"),
      ##nested diplomacy end+
      (val_min, ":value", 0),
      (call_script, "script_change_player_relation_with_troop", ":family_member", ":value"),
    (try_end),

    (try_begin),
      (gt, "$player_honor", ":honor_val"),
      (val_add, ":term", ":honor_val"),
    (else_try),
      (val_add, ":term", "$player_honor"),
    (try_end),

    (store_current_hours, ":cur_hours"),
    (store_sub, ":affiliated_hours", ":cur_hours", "$g_player_affiliated_time"),
    (store_div, ":affiliated_days", ":affiliated_hours", 24),
    (val_sub, ":term", ":affiliated_days"),
    (val_max, ":term", 0),
    (val_min, ":term", 40),


    (troop_get_slot, ":controversy", "trp_player", slot_troop_controversy),
    (val_add, ":controversy", ":term"),
    (val_min, ":controversy", 100),
    (troop_set_slot, "trp_player", slot_troop_controversy, ":controversy"),

  ]),

  
##diplomacy start+
#Importing a script used in Custom Commander.  The inventory copying is used
#as a clever way to make "unmodifiable" views of others' equipment (both the
#PC and NPC have their inventory copied before viewing, and after the window
#closes the copies are written back over the originals).
  ("dplmc_copy_inventory",
    [
      (store_script_param_1, ":source"),
      (store_script_param_2, ":target"),

      (troop_clear_inventory, ":target"),
      (troop_get_inventory_capacity, ":inv_cap", ":source"),
      (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":item", ":source", ":i_slot"),
        (troop_set_inventory_slot, ":target", ":i_slot", ":item"),
        (troop_get_inventory_slot_modifier, ":imod", ":source", ":i_slot"),
        (troop_set_inventory_slot_modifier, ":target", ":i_slot", ":imod"),
        (troop_inventory_slot_get_item_amount, ":amount", ":source", ":i_slot"),
        (gt, ":amount", 0),
        (troop_inventory_slot_set_item_amount, ":target", ":i_slot", ":amount"),
      (try_end),
    ]),


#Decide whether an NPC wants to exchange a fief or not.
#
# param#1 is NPC being asked
# param#2 is that NPC's fief being asked for
# param#3 is the one asking (usually the player)
# param#4 is the fief being offered in exchange
#
# Result is returned in reg0.  Negative means "no", zero means "yes",
# positive means "yes but you have to pay me this amount".
# If the result is negative, the response string is stored in s14.
  ("dplmc_evaluate_fief_exchange",
    [
      (store_script_param, ":target_npc", 1),
      (store_script_param, ":target_fief", 2),
      (store_script_param, ":asker", 3),
      (store_script_param, ":offered_fief", 4),

      (assign, ":result", -1),
      (assign, reg0, ":result"),
      (str_store_string, s14, "str_ERROR_string"),

      (try_begin),
          #Both NPCs are valid, and are not same character.  One can be the player.
          (neq, ":target_npc", ":asker"),
          (is_between, ":target_npc", heroes_begin, heroes_end),
          (this_or_next|is_between, ":asker", heroes_begin, heroes_end),
             (eq,":asker","trp_player"),
          #Both fiefs are valid and owned by the lords in the arguments
          (is_between, ":target_fief", centers_begin, centers_end),
          (party_slot_eq, ":target_fief", slot_town_lord, ":target_npc"),
          (is_between, ":offered_fief", centers_begin, centers_end),
          (party_slot_eq, ":offered_fief", slot_town_lord, ":asker"),
          #The lords are in the same faction
          (store_troop_faction, ":target_faction", ":target_npc"),
          (store_troop_faction, ":asker_faction", ":asker"),
          (try_begin),
             #Special handling needed for player faction
             (eq, ":asker", "trp_player"),
             (neg|eq, ":target_faction", ":asker_faction"),
             (assign, ":asker_faction", "$players_kingdom"),
          (try_end),
          (this_or_next|eq, ":target_faction", ":asker_faction"),
             (this_or_next|faction_slot_eq,":target_faction",slot_faction_leader,":asker"),
             (faction_slot_eq,":asker_faction",slot_faction_leader,":target_npc"),
          #Get prosperity for use in later tests
          (party_get_slot, ":target_prosperity", ":target_fief", slot_town_prosperity),
          (party_get_slot, ":offered_prosperity", ":offered_fief", slot_town_prosperity),
          (store_div, ":min_prosperity", ":target_prosperity", 10),
          (val_mul, ":min_prosperity", 10),
          #...take into account relation
          (call_script, "script_troop_get_relation_with_troop", ":target_npc", ":asker"),
          (store_div, ":relation_div_10", reg0, 10),
          (val_sub, ":min_prosperity", ":relation_div_10"),
          #...take into account persuasion
          (store_skill_level, ":asker_persuasion", "skl_persuasion", ":asker"),
          (val_sub, ":min_prosperity", ":asker_persuasion"),
          #...take into account personal (not party) trade skill
          (store_skill_level, ":asker_trade", "skl_trade", ":asker"),
          (val_sub, ":min_prosperity", ":asker_trade"),
          #...don't let it rise above original's prosperity.
          (val_min, ":min_prosperity", ":target_prosperity"),
          #target_type 1 = village, 2 = castle, 3 = town
		  (assign, ":target_type", 0),
          (try_begin),
            (party_slot_eq, ":target_fief", slot_party_type, spt_town),
            (assign, ":target_type", 3),
          (else_try),
            (party_slot_eq, ":target_fief", slot_party_type, spt_castle),
            (assign, ":target_type", 2),
          (else_try),
  		    (party_slot_eq, ":target_fief", slot_party_type, spt_village),
            (assign, ":target_type", 1),
          (try_end),
		  (ge, ":target_type", 1),#break with error if the type was bad
          #offered_type: 1 = village, 2 = castle, 3 = town
		  (assign, ":offered_type", 0),
          (try_begin),
            (party_slot_eq, ":offered_fief", slot_party_type, spt_town),
            (assign, ":offered_type", 3),
          (else_try),
            (party_slot_eq, ":offered_fief", slot_party_type, spt_castle),
            (assign, ":offered_type", 2),
          (else_try),
			(party_slot_eq, ":offered_fief", slot_party_type, spt_village),
            (assign, ":offered_type", 1),
          (try_end),
		  (ge, ":offered_type", 1),#break with error if the type was bad
          #Now execute comparison logic:
          (try_begin),
            #refuse to trade town for a castle or village
            (lt, ":offered_type", ":target_type"),
            (eq, ":target_type", 3),
            (str_store_string, s14, "str_dplmc_fief_exchange_refuse_town"),
          (else_try),
            #refuse to trade any better type for a worse type
            (lt, ":offered_type", ":target_type"),
            (str_store_string, s14, "str_dplmc_fief_exchange_refuse_castle"),
          (else_try),
            #refuse to trade for something under siege or being raided
            (this_or_next|party_slot_eq, ":offered_fief", slot_village_state, svs_under_siege),
            (party_slot_eq, ":offered_fief", slot_village_state, svs_being_raided),
            (str_store_party_name, s14, ":offered_fief"),
            (str_store_string, s14, "str_dplmc_fief_exchange_refuse_s14_attack"),
          (else_try),
            #accept a trade if the offered type is better
            (lt, ":target_type", ":offered_type"),
            (str_store_string, s14, "str_dplmc_fief_exchange_accept"),
            (assign, ":result", 0),
		  (else_try),
			#refuse to trade away home center (unless trading up for a better type)
			#Target fief is home of NPC...
			(this_or_next|party_slot_eq, ":target_fief", dplmc_slot_center_original_lord, ":target_npc"),
			   (troop_slot_eq, ":target_npc", slot_troop_home, ":target_fief"),
			(neg|party_slot_eq, ":offered_fief", dplmc_slot_center_original_lord, ":target_npc"),
			#...and offered fief is not.
			(neg|troop_slot_eq, ":target_npc", slot_troop_home, ":offered_fief"),
			(this_or_next|neg|is_between, ":target_npc", companions_begin, companions_end),
				(neg|troop_slot_eq, ":target_npc", slot_troop_town_with_contacts, ":offered_fief"),
			(str_store_party_name, s14, ":target_fief"), #Line added by zerilius
			(str_store_string, s14, "str_dplmc_fief_exchange_refuse_home"),
          (else_try),
            #refuse trade if prosperity is too low
            (lt, ":offered_prosperity", ":min_prosperity"),
            (str_store_string, s14, "str_dplmc_fief_exchange_refuse_rich"),
          (else_try),
            #accept trade for 0 or more denars
            (store_sub, ":result", ":target_prosperity", ":offered_prosperity"),
            (val_mul, ":result", ":target_type"),
            (val_mul, ":result", 36),#Should probably be 60 instead
            #(val_div, ":result", 100),
            (val_add, ":result", 2000),
            (val_max, ":result", 0),
            (try_begin),
               (ge, ":result", 1),
               (assign, reg3, ":result"),
               (str_store_string, s14, "str_dplmc_fief_exchange_accept_reg3_denars"),
            (else_try),
               (str_store_string, s14, "str_dplmc_fief_exchange_accept"),
            (try_end),
          (try_end),
      (try_end),
      (assign, reg0, ":result"),
    ]),

  # script_dplmc_time_sorted_heroes_for_center_aux
    # INPUT: arg1 = troop_id, arg2 = morality type
    # OUTPUT: reg0 has morality value, or 0 if inapplicable
    ("dplmc_get_troop_morality_value",
	[
		(store_script_param, ":troop_id", 1),
		(store_script_param, ":morality_type", 2),

		(assign, reg0, 0),
		(try_begin),
			(neg|is_between, ":troop_id", companions_begin, companions_end),#<-- result is 0 for non-companions
		(else_try),
			(troop_slot_eq, ":troop_id", slot_troop_morality_type, ":morality_type"),
			(troop_get_slot, reg0, ":troop_id", slot_troop_morality_value),
		(else_try),
			(troop_slot_eq, ":troop_id", slot_troop_2ary_morality_type, ":morality_type"),
			(troop_get_slot, reg0, ":troop_id", slot_troop_2ary_morality_value),
		(try_end),

	]),

    #script_dplmc_print_subordinate_says_sir_madame_to_s0
    #
    #In a number of circumstances a subordinate (a soldier in the player's employ) will refer
    #to him as "sir" or "madame".  This is intended as a sign of respect, but becomes
    #unintentionally disrespectful if the player would ordinarily merit a higher title.
    #
    #This function does not take into account the personal characteristics of the speaker in
    #any way.  That logic should occur elsewhere.
    #
    #input: none
    #output: reg0 gets a number corresponding to the title used
    ("dplmc_print_subordinate_says_sir_madame_to_s0",
        [
        (assign, ":highest_honor", 1),#{sir/madame}
        #1: str_dplmc_sirmadame
        #2: str_dplmc_my_lordlady
        #3: str_dplmc_your_highness
        (try_begin),
            #disable extra honors when the player is not recognized
            (gt, "$sneaked_into_town", disguise_none),
            (assign, ":highest_honor", 1),
        (else_try),
            #initialize variables for following steps
            (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
            (troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
            #check if the player is the spouse of one of a widely recognized monarch,
            #or if the player is the ruler of one of the starting kingdoms (this can't happen but check anyway)
            (ge, ":player_spouse", 1),
            (try_for_range, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
                (this_or_next|faction_slot_eq, ":faction_no", slot_faction_leader, "trp_player"),
                (faction_slot_eq, ":faction_no", slot_faction_leader, ":player_spouse"),
                (val_max, ":highest_honor", 3),
            (try_end),
            (this_or_next|is_between, ":player_spouse", kings_begin, kings_end),
            (this_or_next|is_between, ":player_spouse", pretenders_begin, pretenders_end),
                (ge, ":highest_honor", 3),
            (val_max, ":highest_honor", 3),
            #Do not continue, since you've already used the highest available honor.
        (else_try),
            #the player is head of his own faction
            (ge, "$players_kingdom", 0),
            #faction leader is player, or faction leader is spouse and spouse is valid
            (this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
                (faction_slot_eq, "$players_kingdom", slot_faction_leader, ":player_spouse"),
            (this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
                (ge, ":player_spouse", 1),

            (faction_slot_eq, "$players_kingdom", slot_faction_state, sfs_active),
            (try_begin),
                #If you have sufficient right-to-rule and renown, your subjects
                #will call you "highness".
                (ge, "$player_right_to_rule", 10),
                (store_sub, reg0, 75 + 75, "$player_right_to_rule"),
                (val_mul, reg0, 1200 // 75),#minimum required renown (as an aside, 1200 is evenly divisibly by 75)
                #examples: at right to rule 50, renown must be at least 1600
                #          at right to rule 99, renown must be at least 816
                #          at right to rule 10, renown must be at least 2240
                (ge, ":player_renown", reg0),
                (val_max, ":highest_honor", 3),
            (else_try),
                #"Highness" is also used if the player's kingdom holds meaningful territory.
                (try_begin),
                    #Recalculate the cached value if it's suspicious
                    (faction_slot_eq, "$players_kingdom", slot_faction_num_castles, 0),
                    (faction_slot_eq, "$players_kingdom", slot_faction_num_towns, 0),
                    (call_script, "script_faction_recalculate_strength", "$players_kingdom"),
                (else_try),
                    #Recalculate the cached value if it's obviously wrong
                    (this_or_next|neg|faction_slot_ge, "$players_kingdom", slot_faction_num_castles, 0),
                    (neg|faction_slot_ge, "$players_kingdom", slot_faction_num_towns, 0),
                    (call_script, "script_faction_recalculate_strength", "$players_kingdom"),
                (try_end),
                #Territory points: castles = 2, towns = 3 (ignore villages)
                (faction_get_slot, ":territory_points", "$players_kingdom", slot_faction_num_towns),
                (val_mul, ":territory_points", 3),
                (faction_get_slot, reg0, "$players_kingdom", slot_faction_num_castles),
                (val_add, ":territory_points", reg0),
                (val_add, ":territory_points", reg0),
                #If the player owns even a single center, that's worth at least "my lord" from his followers
                (ge, ":territory_points", 1),
                (val_max, ":highest_honor", 2),
                #By default there are around 48 castles and 22 towns on the map, for a total of 70
                #centers, and 162 "points" if weighting castles = 2 and towns = 3.
                (store_sub, ":global_points", towns_end, towns_begin),
                (val_mul, ":global_points", 3),
                (store_sub, reg0, castles_end, castles_begin),
                (val_add, ":global_points", reg0),
                (val_add, ":global_points", reg0),
                #By default there are 6 NPC kingdoms, averaging 8 castles and 3.66... towns or
                #27 points each (although the initial distribution of territory is not even).
                (store_sub, ":number_kingdoms", npc_kingdoms_end, npc_kingdoms_begin),
                (val_max,  ":number_kingdoms", 1),
                #Territory must be at least 3/4 the total points divided by number of initial kingdoms.
                #Right to rule applied as a percentage bonus, scaled so that you gain recognition with
                #75% right to rule and a 50% size kingdom.

                #What I want is: ( (RtR * 2/3) + 100 ) * territory * kingdoms >= globe * 3/4
                #This is equivalent to: (RtR * 2 + 300) * territory * kingdoms * 4 >= globe * 9
                #The re-ordering is because of rounding.
                (store_mul, ":target_points", ":global_points", 9),
                (store_mul, reg0, "$player_right_to_rule", 2),
                (val_add, reg0, 300),
                (val_mul, reg0, ":territory_points"),
                (val_mul, reg0, ":number_kingdoms"),
                (val_mul, reg0, 4),
                (ge, reg0, ":target_points"),
                (val_max, ":highest_honor", 3),
            (try_end),
            #stop evaluation if you reached highest honor
            (ge, ":highest_honor", 3),
        (else_try),
            #the player is a vassal of one of the initial kingdoms
            (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
            (val_max, ":highest_honor", 1),
            (eq, "$player_has_homage", 1),#<- can fail
            (val_max, ":highest_honor", 2),
        (try_end),

        (try_begin),
           (ge, ":highest_honor", 3),
           (str_store_string, s0, "str_dplmc_your_highness"),
        (else_try),
           (eq, ":highest_honor", 2),
           (str_store_string, s0, "str_dplmc_my_lordlady"),
        (else_try),
           (str_store_string, s0, "str_dplmc_sirmadam"),
        (try_end),

          ##Special cases
        (try_begin),
          (eq, "$sneaked_into_town", disguise_none),
          (is_between, "$g_talk_troop", companions_begin, companions_end),
          (ge, ":highest_honor", 1),
          (neg|troop_slot_eq, "$g_talk_troop", slot_troop_met, 0),
          (this_or_next|neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_inactive),
          (neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, 0),
          (neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
          (troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
          (ge, ":honorific", "str_npc1_honorific"),
          (str_store_string, s0, ":honorific"),
        (else_try),
          (eq, ":highest_honor", 1),
          (is_between, "$g_talk_troop", heroes_begin, heroes_end),
          (str_store_string, s0, "str_dplmc_sirmadame"),
        (try_end),

        (assign, reg0, ":highest_honor"),
    ]),


	#"script_dplmc_print_commoner_at_arg1_says_sir_madame_to_s0"
	#
	#In a number of circumstances a commoner, who might or might not be a subject of
	#the player, will refer to him as "sir" or "madame."  This script determines whether
	#a different title would be warranted.
	#
	#input: party_no (usually a village or town)
	#output: reg0 gets a number corresponding to the title used
	("dplmc_print_commoner_at_arg1_says_sir_madame_to_s0", [
		(store_script_param_1, ":party_no"),

		(assign, ":title_level", 1),
		(str_store_string, s0, "str_dplmc_sirmadam"),
		(store_faction_of_party, ":party_faction"),

		(try_begin),
			(eq, "$sneaked_into_town", disguise_none),#disable extra honors when the player is not recognized
			(ge, ":party_no", 0),

			#This is used in various conditions below, so I am calling it once
			#for simplicity.
			(assign, ":save_g_talk_troop", "$g_talk_troop"),
			(assign, ":save_g_encountered_party", "$g_encountered_party"),
            (try_begin),
              (neq, ":party_no", "$g_encountered_party"),
              (assign, "$g_encountered_party", -1),
              (assign, "$g_talk_troop", -1),
            (try_end),
			(call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
			(assign, ":title_level", reg0),
			(assign, "$g_encountered_party", ":save_g_encountered_party"),
			(assign, "$g_talk_troop", ":save_g_talk_troop"),

			(try_begin),
				#The player is a full member of the faction: use full honors
				(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":party_faction"),
				(ge, reg0, DPLMC_FACTION_STANDING_DEPENDENT),
				#(nothing more needs to be done)
			(else_try),
				#the faction has recognized him formally: use full honors
				(this_or_next|eq, ":party_no", "p_main_party"),
				(this_or_next|eq, ":party_faction", "fac_player_supporters_faction"),
				   (faction_slot_ge, ":party_faction", slot_faction_recognized_player, 1),
				#(nothing more needs to be done)
			(else_try),
				#The player is the lord of the town: keep result from script_dplmc_print_subordinate_says_sir_madame_to_s0
				(is_between, ":party_no", centers_begin, centers_end),
				(party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
				#(nothing more needs to be done)
			(else_try),
				#Subjects of neutral kingdoms will use titles up to "my lord".
				(store_relation, ":relation", "fac_player_supporters_faction", ":party_faction"),
				(ge, ":relation", 0),
				(try_begin),
					(ge, ":title_level", 3),
					(assign, ":title_level", 2),
					(str_store_string, s0, "str_dplmc_my_lordlady"),
				(try_end),
			(else_try),
				#Subjects of kingdoms at war (that do not recognize the player) and all cases not
				#yet mentioned will reduce the "level" of the title awarded to the player by 1, to
				#a minimum of 1.
				(try_begin),
					(ge, ":title_level", 3),
					(assign, ":title_level", 2),
					(str_store_string, s0, "str_dplmc_my_lordlady"),
				(else_try),
					(eq, ":title_level", 2),
					(assign, ":title_level", 1),
				   (str_store_string, s0, "str_dplmc_sirmadam"),
				(try_end),
			(try_end),
		(try_end),

		##Special cases
		(try_begin),
			(neq, ":party_no", "$g_encountered_party"),
		(else_try),
			(eq, "$sneaked_into_town", disguise_none),
			(ge, ":title_level", 1),
			(is_between, "$g_talk_troop", companions_begin, companions_end),
			(neg|troop_slot_eq, "$g_talk_troop", slot_troop_met, 0),
			(this_or_next|neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_inactive),
				(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, 0),
			(neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
			(troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
			(ge, ":honorific", "str_npc1_honorific"),
			(str_store_string, s0, ":honorific"),
		(else_try),
			(eq, ":title_level", 1),
			(is_between, "$g_talk_troop", heroes_begin, heroes_end),
			(assign, ":title_level", "str_dplmc_sirmadame"),
		(try_end),

		(assign, reg0, ":title_level"),

		##Switch to cultural equivalents
      #(try_begin),
		#   (eq, ":party_no", "$g_encountered_party"),
		#   (is_between, "$g_talk_troop", heroes_begin, heroes_end),
	   #   (troop_get_slot, ":culture_faction", "$g_talk_troop", slot_troop_original_faction),
		#   (is_between, ":culture_faction", npc_kingdoms_begin, npc_kingdoms_end),
		#(else_try),
		#   (eq, ":party_no", "$g_encountered_party"),
		#   (ge, "$g_talk_troop", soldiers_begin),
		#   (store_faction_of_troop, ":culture_faction", "$g_talk_troop"),
		#	(is_between, ":culture_faction", npc_kingdoms_begin, npc_kingdoms_end),
		#(else_try),
      #   (is_between, ":party_no", centers_begin, centers_end),
      #   (party_get_slot, ":culture_faction", ":party_no", slot_center_original_faction),
  		#	(is_between, ":culture_faction", npc_kingdoms_begin, npc_kingdoms_end),
		#(else_try),
		#   (assign, ":culture_faction", ":party_faction"),
		#(try_end),
		#(try_begin),
		#   (is_between, "$g_talk_troop", companions_begin, companions_end),#do not switch
		#(else_try),
		#  (eq, ":title_level", 1),
		#	(eq, ":culture_faction", "fac_kingdom_6"),
		#	(str_store_string, s0, "@{!}{sahib/sahiba}"),
		#(try_end),
	]),

  ##script_cf_dplmc_troop_is_female
  #
  #This exists to make it easy to modify this to work with mods that redefine the troop types.
  #See script_dplmc_store_troop_is_female
  #
  #INPUT: arg1: troop_no
  #OUTPUT: none
  ("cf_dplmc_troop_is_female",
  [
	(store_script_param_1, ":troop_no"),
	(assign, ":is_female", 0),
	(ge, ":troop_no", 0),#Undefined behavior when the arguments are invalid.
	(try_begin),
	   (eq, ":troop_no", active_npcs_including_player_begin),
	   (assign, ":troop_no", "trp_player"),
	(try_end),
  	(troop_get_type, ":is_female", ":troop_no"),
	(val_mod, ":is_female", 2), # Makes even number skins "0" odd number "1" - tf_female is eqal to 1
	(eq, ":is_female", tf_female),
  ]),

  ##script_dplmc_store_troop_is_female
  #
  #This exists to make it easy to modify this to work with mods that redefine the troop types.
  #
  #If you change this, remember to also change script_cf_dplmc_troop_is_female and
  #script_dplmc_store_is_female_troop_1_troop_2
  #
  #INPUT: arg1: troop_no
  #
  #OUTPUT:
  #       reg0: 1 is yes, 0 is no
  ("dplmc_store_troop_is_female",
  [
    (store_script_param_1, ":troop_no"),
	(ge, ":troop_no", 0),
    (try_begin),
       (eq, ":troop_no", active_npcs_including_player_begin),
       (assign, ":troop_no", "trp_player"),
    (try_end),
    (troop_get_type, ":is_female", ":troop_no"),
	(val_mod, ":is_female", 2), # Makes even number skins "0" odd number "1" - tf_female is eqal to 1
	(assign, reg0, ":is_female"),
  ]),

  ("dplmc_store_troop_is_female_reg",
  [
    (store_script_param_1, ":troop_no"),
    (store_script_param_2, ":reg_no"),
    (ge, ":troop_no", 0),
    (troop_get_type, ":is_female", ":troop_no"),
	(val_mod, ":is_female", 2), # Makes even number skins "0" odd number "1" - tf_female is eqal to 1
        ##Can asign to registers 0,1,2,3, 65, or 4
    (try_begin),
      (eq, ":reg_no", 4),
      (assign, reg4, ":is_female"),
    (else_try),
      (eq, ":reg_no", 3),
      (assign, reg3, ":is_female"),
    (else_try),
      (eq, ":reg_no", 2),
      (assign, reg2, ":is_female"),
    (else_try),
      (eq, ":reg_no", 1),
      (assign, reg1, ":is_female"),
    (else_try),
      (eq, ":reg_no", 0),
      (assign, reg0, ":is_female"),
    (else_try),
      (eq, ":reg_no", 65),
      (assign, reg65, ":is_female"),
    (else_try),
      ##default to reg4
      (assign, reg4, ":reg_no"),
      (display_message, "@{!} ERROR: called script dplmc-store-troop-is-female-reg with bad argument {reg4}"),
      (assign, reg4, ":is_female"),
    (try_end),
  ]),

  ##script_dplmc_store_is_female_troop_1_troop_2
  #
  #This exists to make it easy to modify this to work with mods that redefine the troop types.
  #See script_dplmc_store_troop_is_female
  #
  #INPUT:
  #      arg1: troop_1
  #      arg2: troop_2
  #OUTPUT:
  #       reg0: 0 for not female, 1 for female
  #       reg1: 0 for not female, 1 for female
  ("dplmc_store_is_female_troop_1_troop_2",
  [
	(store_script_param_1, ":troop_1"),
	(store_script_param_2, ":troop_2"),
    (ge, ":troop_1", 0),
    (ge, ":troop_1", 0),
    (troop_get_type, ":is_female_1", ":troop_1"),
    (troop_get_type, ":is_female_2", ":troop_2"),
	(val_mod, ":is_female_1", 2), # Makes even number skins "0" odd number "1" - tf_female is eqal to 1
	(val_mod, ":is_female_2", 2), # Makes even number skins "0" odd number "1" - tf_female is eqal to 1
	(assign, reg0, ":is_female_1"),
	(assign, reg1, ":is_female_2"),
  ]),

  #script_cf_dplmc_evaluate_pretender_proposal
  # INPUT: arg1 = troop_id for pretender
  # OUTPUT: reg0 = answer
  #
  # Writes reason to s14
  # May clobber s0, s1
  #
  ("cf_dplmc_evaluate_pretender_proposal",
    [
      (store_script_param_1, ":pretender"),
	  (assign, ":answer", -1),
	  (assign, ":save_reg1", reg1),
	  (assign, ":save_reg65", reg65),
	  (call_script, "script_dplmc_store_troop_is_female", ":pretender"),
	  (assign, reg65, reg0),

	  (str_store_string, s14, "str_ERROR_string"),

	  (is_between, ":pretender", pretenders_begin, pretenders_end),
	  (troop_slot_eq, ":pretender", slot_troop_occupation, slto_kingdom_hero),

	  (store_troop_faction, ":pretender_faction", ":pretender"),
	  (is_between, ":pretender_faction", npc_kingdoms_begin, npc_kingdoms_end),
	  (troop_slot_eq, ":pretender", slot_troop_original_faction, ":pretender_faction"),
	  (faction_slot_eq, ":pretender_faction", slot_faction_leader, ":pretender"),
	  (faction_slot_eq, ":pretender_faction", slot_faction_state, sfs_active),

	  (troop_slot_eq, ":pretender", slot_troop_spouse, -1),
	  (troop_slot_eq, ":pretender", slot_troop_betrothed, -1),

	  (troop_get_slot, ":pretender_renown", ":pretender", slot_troop_renown),
	  (val_max, ":pretender_renown", 1),

	  #There, we've covered the preliminaries: this should be a standard post-rebellion
	  #setup.  Now verify that the player is in a correct state.

	  (eq, "$players_kingdom", ":pretender_faction"),
	  (eq, "$player_has_homage", 1),
    (this_or_next|eq, "$g_polygamy", 1),
	  (troop_slot_eq, "trp_player", slot_troop_spouse, -1),
	  (troop_slot_eq, "trp_player", slot_troop_betrothed, -1),

	  (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
	  (call_script, "script_troop_get_player_relation", ":pretender"),
	  (assign, ":player_relation", reg0),

	  #Find competitors
	  (assign, ":b", -1),
	  (assign, ":b_relation", -101),
	  (assign, ":c", -1),
	  (assign, ":c_renown", -1),

	  (store_add, ":faction_renown", ":pretender_renown", ":player_renown"),
	  (assign, ":faction_lords", 2),#the player and the pretender

	  (troop_set_slot, ":pretender", slot_troop_temp_slot, 0),#clear
	  (troop_set_slot, "trp_player", slot_troop_temp_slot, 0),#clear

      (try_for_range_backwards, ":competitor", heroes_begin, heroes_end),
        (troop_slot_eq, ":competitor", slot_troop_occupation, slto_kingdom_hero),
        (store_faction_of_troop, ":competitor_faction", ":competitor"),
        (eq, ":competitor_faction", ":pretender_faction"),
        (try_begin),
          (is_between, ":competitor", kings_begin, kings_end), #SB : exclude former monarchs
          (troop_slot_eq, ":competitor", slot_troop_original_faction, ":pretender_faction"),
          (troop_set_slot, ":competitor", slot_troop_temp_slot, -99999),#low value
          (assign, ":competitor_renown", 0), #do not factor in
        (else_try),
          (troop_set_slot, ":competitor", slot_troop_temp_slot, 0),#clear
          (troop_get_slot, ":competitor_renown", ":competitor", slot_troop_renown),
        (try_end),

        (neq, ":competitor", active_npcs_including_player_begin),
        (neq, ":competitor", ":pretender"),

        (call_script, "script_troop_get_relation_with_troop", ":competitor", ":pretender"),
        (assign, ":competitor_relation", reg0),

        (val_add, ":faction_renown", ":competitor_renown"),
        (val_add, ":faction_lords", 1),

        (try_begin),
           (ge, ":competitor_relation", ":b_relation"),
           (neg|troop_slot_eq, ":competitor", slot_troop_spouse, "trp_player"),
           (neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":competitor"),
           (assign, ":b", ":competitor"),
           (assign, ":b_relation", ":competitor_relation"),
        (try_end),
        (try_begin),
           (ge, ":competitor_renown", ":c_renown"),
           (assign, ":c", ":competitor"),
           (assign, ":c_renown", ":competitor_renown"),
        (try_end),
      (try_end),

      (assign, ":pretender_towns", 0),
      (assign, ":pretender_castles", 0),
      (assign, ":pretender_villages", 0),

      (assign, ":player_towns", 0),
      (assign, ":player_castles", 0),
      (assign, ":player_villages", 0),

      (assign, ":faction_towns", 0),
      (assign, ":faction_castles", 0),
      (assign, ":faction_villages", 0),

      (assign, ":original_towns", 0),
      (assign, ":original_castles", 0),
      (assign, ":original_villages", 0),

   	  #(store_sub, ":global_towns", towns_end, towns_begin),
	  #(store_sub, ":global_castles", castles_end, castles_begin),
	  #(store_sub, ":global_villages", villages_end, villages_begin),

	  (assign, ":highest_score", -1),
	  (assign, ":highest_score_lord", -1),

	  (try_for_range, ":center_no", towns_begin, towns_end),
		(store_faction_of_party, ":center_faction", ":center_no"),
		(try_begin),
			(party_slot_eq, ":center_no", slot_town_lord, ":pretender"),
			(val_add, ":pretender_towns", 1),
			(val_add, ":faction_towns", 1),
		(else_try),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(val_add, ":player_towns", 1),
			(val_add, ":faction_towns", 1),
		(else_try),
			(this_or_next|eq, ":center_faction", ":pretender_faction"),
				(eq, ":center_faction", "fac_player_supporters_faction"),
			(val_add, ":faction_towns", 1),
			(party_get_slot, ":town_lord", ":center_no", slot_town_lord),
			(this_or_next|eq, ":town_lord", "trp_player"),
				(is_between, ":town_lord", heroes_begin, heroes_end),
			(troop_get_slot, ":local_temp", ":town_lord", slot_troop_temp_slot),
			(val_add, ":local_temp", 3),
			(troop_set_slot, ":town_lord", slot_troop_temp_slot, ":local_temp"),
			(ge, ":local_temp", ":highest_score"),
			(assign, ":highest_score", ":local_temp"),
			(assign, ":highest_score_lord", ":town_lord"),
		(try_end),
		(try_begin),
			(party_slot_eq, ":center_no", slot_center_original_faction, ":pretender_faction"),
			(val_add, ":original_towns", 1),
		(try_end),
	  (try_end),

	  (try_for_range, ":center_no", castles_begin, castles_end),
		(store_faction_of_party, ":center_faction", ":center_no"),
		(try_begin),
			(party_slot_eq, ":center_no", slot_town_lord, ":pretender"),
			(val_add, ":pretender_castles", 1),
			(val_add, ":faction_castles", 1),
		(else_try),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(val_add, ":player_castles", 1),
			(val_add, ":faction_castles", 1),
		(else_try),
			(this_or_next|eq, ":center_faction", ":pretender_faction"),
				(eq, ":center_faction", "fac_player_supporters_faction"),
			(val_add, ":faction_castles", 1),
			(party_get_slot, ":town_lord", ":center_no", slot_town_lord),
			(this_or_next|eq, ":town_lord", "trp_player"),
				(is_between, ":town_lord", heroes_begin, heroes_end),
			(troop_get_slot, ":local_temp", ":town_lord", slot_troop_temp_slot),
			(val_add, ":local_temp", 2),
			(troop_set_slot, ":town_lord", slot_troop_temp_slot, ":local_temp"),
			(ge, ":local_temp", ":highest_score"),
			(assign, ":highest_score", ":local_temp"),
			(assign, ":highest_score_lord", ":town_lord"),
		(try_end),
		(try_begin),
			(party_slot_eq, ":center_no", slot_center_original_faction, ":pretender_faction"),
			(val_add, ":original_castles", 1),
		(try_end),
	  (try_end),

	  (try_for_range, ":center_no", villages_begin, villages_end),
		(store_faction_of_party, ":center_faction", ":center_no"),
		(try_begin),
			(party_slot_eq, ":center_no", slot_town_lord, ":pretender"),
			(val_add, ":pretender_villages", 1),
			(val_add, ":faction_villages", 1),
		(else_try),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(val_add, ":player_villages", 1),
			(val_add, ":faction_villages", 1),
		(else_try),
			(this_or_next|eq, ":center_faction", ":pretender_faction"),
				(eq, ":center_faction", "fac_player_supporters_faction"),
			(val_add, ":faction_villages", 1),
			(party_get_slot, ":town_lord", ":center_no", slot_town_lord),
			(this_or_next|eq, ":town_lord", "trp_player"),
				(is_between, ":town_lord", heroes_begin, heroes_end),
			(troop_get_slot, ":local_temp", ":town_lord", slot_troop_temp_slot),
			(val_add, ":local_temp", 1),
			(troop_set_slot, ":town_lord", slot_troop_temp_slot, ":local_temp"),
			(ge, ":local_temp", ":highest_score"),
			(assign, ":highest_score", ":local_temp"),
			(assign, ":highest_score_lord", ":town_lord"),
		(try_end),
		(try_begin),
			(party_slot_eq, ":center_no", slot_center_original_faction, ":pretender_faction"),
			(val_add, ":original_villages", 1),
		(try_end),
	  (try_end),

	  #Update stats
	  (faction_set_slot, ":pretender_faction", slot_faction_num_castles, ":faction_castles"),
	  (faction_set_slot, ":pretender_faction", slot_faction_num_towns, ":faction_towns"),

	  #Point totals used below
	  #Faction Score A: (4 * towns) + (2 * castles) + villages
	  (store_mul, ":faction_score_a", ":faction_towns", 4),
	  (val_add, ":faction_score_a", ":faction_castles"),
	  (val_add, ":faction_score_a", ":faction_castles"),
	  (val_add, ":faction_score_a", ":faction_villages"),

	  #Faction Score B: (3 * towns) + (2 * castles) + villages
	  (store_sub, ":faction_score_b", ":faction_score_a", ":faction_towns"),

	  #Original Score A: (4 * towns) + (2 * castles) + villages
	  (store_mul, ":original_score_a", ":original_towns", 4),
	  (val_add, ":original_score_a", ":original_castles"),
	  (val_add, ":original_score_a", ":original_castles"),
	  (val_add, ":original_score_a", ":original_villages"),

	  #Original Score B: (3 * towns) + (2 * castles) + villages
	  (store_sub, ":original_score_b", ":faction_score_b", ":faction_towns"),

	  #The first fail-condition encountered will be the explanation used,
	  #so make sure the most pressing ones go first.
	  (try_begin),
	      #relation low: using the same cutoff normally used for becoming a vassal
		  (lt, ":player_relation", 0),
		  (assign, ":answer", -1),
		  (str_store_string, s14, "@Given the way things stand between us at the moment, {playername}, I would not consider it prudent to enter into such an arrangement."),
	  (else_try),
         #check player right to rule
		 (store_add, ":player_score", "$player_right_to_rule", ":player_relation"),
		 (this_or_next|lt, "$player_right_to_rule", 20),#the level required for your spouse to join a rebellion
			(lt, ":player_score", 100),
		 (assign, ":answer", -1),
		 (str_store_string, s14, "@{playername}, I am grateful to you, but in the eyes of the people you do not have sufficient legitimacy as a potential co-ruler.  Marrying you would undermine my own claim to the throne."),
	  (else_try),
         #check player renown
		 (store_mul, ":min_score", ":pretender_renown", 2),
		 (val_div, ":min_score", 3),#2/3 pretender renown, 750 by default
		 (val_clamp, ":min_score", 500, 1200),#500 is the minimum to begin the claimant quest; 1200 is the initial value for original lords #SB fixed comment

		 (lt, ":player_renown", ":min_score"),
		 (assign, ":answer", -1),
		 (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":player_renown"),
			(assign, reg1, ":min_score"),
			(display_message, "@{!}DEBUG - player renown {reg0}, required renown {reg1}"),
		  (try_end),
		 (str_store_string, s14, "@{playername}, I know that if it were not for you I would not sit on this throne, but your name is little renowned in Calradia.  Marrying you would be perceived as an uneven match and would call into question my own claim to the throne."),
	  (else_try),
		  #check player has sufficient fiefs
		  (store_mul, ":player_score", ":player_towns", 3),
		  (val_add, ":player_score", ":player_castles"),
		  (val_add, ":player_score", ":player_castles"),
		  (val_add, ":player_score", ":player_villages"),# player_score = (3 * towns) + (2 * castles) + villages

		  (assign, ":min_score", 6),#A town, a castle, and a village; two towns; three castles; six villages; etc...

		  (try_begin),
			#Ensure the minimum is not unreasonable on small maps.
			(lt, ":original_score_b", 18),
			(lt, ":faction_score_b", 18),
			(assign, reg0, ":original_score_b"),
			(val_max, reg0, ":faction_score_b"),
			(store_div, ":min_score", reg0, 3),
		  (try_end),

		  (troop_get_slot, ":two_thirds_pretender_score", ":pretender", slot_troop_temp_slot),
		  (val_mul, ":two_thirds_pretender_score", 2),
		  (val_add, ":two_thirds_pretender_score", 1),
		  (val_div, ":two_thirds_pretender_score", 3),
		  (val_max, ":min_score", ":two_thirds_pretender_score"),

		  (lt, ":player_score", ":min_score"),
		  (assign, ":answer", -1),
		  (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":player_score"),
			(assign, reg1, ":min_score"),
			(display_message, "@{!}DEBUG - player score {reg0} out of a required {reg1}"),
		  (try_end),
		  (str_store_string, s14, "@{playername}, I am grateful for your assistance in regaining my rightful throne, but you do not have sufficient personal holdings to be a suitable match for me.  It would be an uneven partnership."),
     (else_try),
	      #does the player have as much renown as competitors?
		  (lt, ":player_renown", ":c_renown"),
	      (assign, ":answer", -1),
		  (str_store_troop_name, s14, ":c"),
		  (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":player_renown"),
			(assign, reg1, ":c_renown"),
			(display_message, "@{!}DEBUG - player score {reg0}, competitor score {reg1}"),
		  (try_end),
		  (str_store_string_reg, s0, s15),#clobber s0, save s15
		  (call_script, "script_troop_describes_troop_to_s15", ":pretender", ":c"),
		  (str_store_string, s14, "@{playername}, I am grateful to you, but if I were to accept at this time I would risk offending powerful lords such as {s15}, who may consider themselves to have honor equal to or greater than your own."),
		  (str_store_string_reg, s15, s0),#revert s15
	 (else_try),
	      #is the player outfieffed by a competitor?
          (gt, ":highest_score_lord", "trp_player"),
          (neq, ":highest_score_lord", ":pretender"),

		  (store_mul, ":player_score", ":player_towns", 3),
		  (val_add, ":player_score", ":player_castles"),
		  (val_add, ":player_score", ":player_castles"),
		  (val_add, ":player_score", ":player_villages"),# player_score = (3 * towns) + (2 * castles) + villages
             (lt, ":player_score", ":highest_score"),

		  (store_mul, reg0, ":highest_score", 3),#allow small differences
		  (val_add, reg0, 2),
		  (val_div, reg0, 4),
		  (gt, reg0, ":player_score"),

	     (assign, ":answer", -1),
		  (str_store_troop_name, s14, ":highest_score_lord"),
		  (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":player_score"),
			(assign, reg1, ":highest_score"),
			(display_message, "@{!}DEBUG - player score {reg0}, competitor score {reg1}"),
		  (try_end),
		  (str_store_string_reg, s0, s15),#clobber s0, save s15
		  (call_script, "script_troop_describes_troop_to_s15", ":pretender", ":highest_score_lord"),
		  (str_store_string, s14, "@{playername}, I am grateful to you, but if I were to accept at this time I would risk offending great lords such as {s15}, who may consider themselves to have honor equal to or greater than your own."),
		  (str_store_string_reg, s15, s0),#revert s15
      (else_try),
		  #does the player have as much relation as competitors?
		  (lt, ":player_relation", ":b_relation"),
		  (ge, ":b_relation", 5),
		  (assign, ":answer", -1),
		 (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":player_relation"),
			(assign, reg1, ":b_relation"),
			(display_message, "@{!}DEBUG - player relation {reg0}, rival relation {reg1}"),
		  (try_end),
		  (str_store_string_reg, s0, s15),#clobber s0, save s15
		  (call_script, "script_troop_describes_troop_to_s15", ":pretender", ":b"),
		  (str_store_string, s14, "@{playername}, while I am grateful to you, I must confess I am fond of {s15}."),
		  (str_store_string_reg, s15, s0),#revert s15
	  (else_try),
		  #check: sufficient lords?
		  (assign, ":needed_lords", 1),
		  (try_for_range, ":troop_no", lords_begin, lords_end),
			(troop_slot_eq, ":troop_no", slot_troop_original_faction, ":pretender_faction"),
			(val_add, ":needed_lords", 1),
		  (try_end),
		  #Must be at least 75% of original size
		  (val_mul, ":needed_lords", 3),
		  (val_div, ":needed_lords", 4),

		  (lt, ":faction_lords", ":needed_lords"),
		  (assign, ":answer", -1),
		  (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":faction_lords"),
			(assign, reg1, ":needed_lords"),
			(display_message, "@{!}DEBUG - lords in faction {reg0}, required lords {reg1}"),
		  (try_end),

		  (str_store_string, s14, "@Our realm has too few vassals.  In the current precarious state of the affairs I must use the lure of a potential political alliance to attract new vassals, and cannot yet be seen to commit to any single {reg65?suitor:candidate}."),
	  (else_try),
		  #check: pretender has enough fiefs?
		  #Must not be exceeded in fiefs by anyone in the faction.
		  (store_mul, ":pretender_score", ":pretender_towns", 3),
		  (val_add, ":pretender_score", ":pretender_castles"),
		  (val_add, ":pretender_score", ":pretender_castles"),
		  (val_add, ":pretender_score", ":pretender_villages"),
		  (troop_set_slot, ":pretender", slot_troop_temp_slot, ":pretender_score"),

		  (store_mul, reg0, ":highest_score", 3),#allow small differences
		  (val_add, reg0, 2),
		  (val_div, reg0, 4),

		  (gt, reg0, ":pretender_score"),

		  (assign, ":answer", -1),
		  (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg1, reg0),
			(assign, reg0, ":pretender_score"),
			(display_message, "@{!}DEBUG - liege has {reg0} center points, needs at least {reg1}"),
		  (try_end),
		  (str_store_string_reg, s0, s15),#clobber s0, save s15
		  (call_script, "script_troop_describes_troop_to_s15", ":pretender", ":highest_score_lord"),
		  (str_store_string, s14, "@Because I have insufficient personal holdings compared to {s15}, if I entered into such an arrangement I would risk appearing to be a puppet, throwing the stability of the realm into jeopardy."),
		  (str_store_string_reg, s15, s0),#revert s15
	 (else_try),
		  #Check if pretender has enough fiefs, part 2.
		  #Must not have fewer fief points than the number of faction points divided by the
		  #number of lords (so this condition can't be bypassed by just failing to assign
		  #centers to anyone during the rebellion)
		  (store_mul, ":points_per_lord", ":faction_towns", 3),
		  (val_add, ":points_per_lord", ":faction_castles"),
		  (val_add, ":points_per_lord", ":faction_castles"),
		  (val_add, ":points_per_lord", ":faction_villages"),
		  (val_div, ":points_per_lord", ":faction_lords"),#includes pretender so cannot be zero

		  (gt, ":points_per_lord", ":pretender_score"),

		  (assign, ":answer", -1),
		  (try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":pretender_score"),
			(assign, reg1, ":points_per_lord"),
			(display_message, "@{!}DEBUG - liege has {reg0} center points, needs at least {reg1}"),
		  (try_end),
		  (str_store_faction_name, s14, ":pretender_faction"),
		  (str_store_string, s14, "@Because my personal holdings are insufficiently large compared to other lords of the {s14}, if I entered into such an arrangement I would risk appearing to be a puppet, throwing the stability of the realm into jeopardy."),
	  (else_try),
		  #check if player is widely hated in faction
		  (assign, ":total_negative", 0),
		  (assign, ":total_enemies", 0),
		  (assign, ":total_positive", 0),
		  (assign, ":total_friends", 0),
		  (try_for_range, ":troop_no", heroes_begin, heroes_end),
		     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (store_troop_faction, reg0, ":troop_no"),
			 (eq, reg0, ":pretender_faction"),
			 (call_script, "script_troop_get_player_relation", ":troop_no"),
			 (try_begin),
				(lt, reg0, 0),
				(val_add, ":total_negative", 1),
				(lt, reg0, -19),
				(val_add, ":total_enemies", 1),
			 (else_try),
				(gt, reg0, 0),
				(val_add, ":total_positive", 1),
				(gt, reg0, 19),
				(val_add, ":total_friends", 1),
			 (try_end),
		  (try_end),
		  #Must not have a "disapproval rating" of over 33%
		  (val_mul, ":total_enemies", 2),
		  (val_mul, ":total_negative", 2),
		  (this_or_next|gt, ":total_enemies", ":total_friends"),
		     (gt, ":total_negative", ":total_positive"),

		  (assign, ":answer", -1),
		  (str_store_faction_name, s14, ":pretender_faction"),
		  (str_store_string, s14, "@I am grateful to you, {playername}, but you have too many enemies among the lords of the {s14} for your proposal to be politically viable.  If I were to accept, there might be a revolt."),
	  (else_try),
		  #controversy must be less than 25, and less than half the relation with the liege
		  (troop_get_slot, ":controversy_2", "trp_player", slot_troop_controversy),
		  (ge, ":controversy_2", 1),
		  (val_mul, ":controversy_2", 2),
		  (this_or_next|ge, ":controversy_2", 50),
		     (ge, ":controversy_2", ":player_relation"),
		  (assign, ":answer", -1),
		  (str_store_faction_name, s14, ":pretender_faction"),
		  (str_store_string, s14, "@You have engendered too much controversy recently, {playername} .  If I were to accept at this time, there might be a revolt among the lords of the {s14}.  Let us speak of this later when the furor has died down."),
	  (else_try),
		  #check is marshall
		  (neg|faction_slot_eq, ":pretender_faction", slot_faction_marshall, "trp_player"),
		  (assign, ":answer", -2),#<-- negative two, not -1
		  (str_store_faction_name, s14, ":pretender_faction"),
		  (str_store_string, s14, "@If you desire to lead the {s14} alongside me, gather support among my vassals to become marshall, and demonstrate to them your abilities as a war leader."),
	  (else_try),
		  #player is marshall: is the territory sufficient?

		  #The faction must have at least 80% of its former territory under scoring system A or scoring system B.
		  (store_mul, ":four_fifths_original_score_a", ":original_score_a", 4),
		  (val_div, ":four_fifths_original_score_a", 5),

		  (store_mul, ":four_fifths_original_score_b", ":original_score_b", 4),
		  (val_div, ":four_fifths_original_score_b", 5),

		  (lt, ":faction_score_a", ":four_fifths_original_score_a"),
		  (lt, ":faction_score_b", ":four_fifths_original_score_b"),
		  (assign, ":answer", -3),

		  (call_script, "script_dplmc_print_centers_in_numbers_to_s0", ":original_towns", ":original_castles", ":original_villages"),
		  (str_store_string_reg, s1, s0),
		  (call_script, "script_dplmc_print_centers_in_numbers_to_s0", ":faction_towns", ":faction_castles", ":faction_villages"),

		  (str_store_faction_name, s14, ":pretender_faction"),
		  (str_store_string, s14, "@Our realm has lost too much territory.  We once held {s1} but now only hold {s0}.  In the current precarious state of affairs I must retain the possibility of a political alliance to use as a bargaining chip with the other sovereigns, so I yet be seen to commit to any single {reg65?suitor:candidate}.  Restore the {s14} to its former glory, and I will gladly have you rule beside me as my {husband/wife}."),
	  (else_try),
		 #player is marshall: are any native centers lost?

		 (str_clear, s0),
		 (str_clear, s1),
		 (assign, ":num_lost_towns_and_castles", 0),

		 (try_for_range, ":center_no", centers_begin, centers_end),
			(party_slot_eq, ":center_no", slot_center_original_faction, ":pretender_faction"),
			(store_faction_of_party, ":center_faction", ":center_no"),
			(neq, ":center_faction", ":pretender_faction"),
			(neq, ":center_faction", "fac_player_supporters_faction"),
			(try_begin),
				(eq, ":num_lost_towns_and_castles", 0),
				(str_store_party_name, s0, ":center_no"),
			(else_try),
				(eq, ":num_lost_towns_and_castles", 1),
				(str_store_party_name, s1, ":center_no"),
			(else_try),
				(str_store_string, s0, "str_dplmc_s0_comma_s1"),
				(str_store_party_name, s1, ":center_no"),
			(try_end),
			(val_add, ":num_lost_towns_and_castles", 1),
		 (try_end),
		 #post-loop cleanup
		 (try_begin),
			(ge, ":num_lost_towns_and_castles", 2),
			(str_store_string, s0, "str_dplmc_s0_and_s1"),
		 (try_end),
		 #native towns lost
		 (ge, ":num_lost_towns_and_castles", 1),
		 (store_sub, reg0, ":num_lost_towns_and_castles", 1),
		 (str_store_faction_name, s14, ":pretender_faction"),
		 (str_store_string, s14, "@{s0} {reg0?have:has} been lost to foreign hands.  Restore the {s14} to its rightful boundaries, and I will gladly have you rule beside me as my {husband/wife}."),
		 (assign, ":answer", -3),
	  (else_try),
	  #Timer answer
	     (lt, "$g_player_days_as_marshal", 14),
		  (assign, reg0, "$g_player_days_as_marshal"),
		  (store_sub, reg1, reg0, 1),
		  (str_store_faction_name, s14, ":pretender_faction"),
		  (str_store_string, s14, "@You have only been marshall for {reg0} {reg1?days:day}.  Let us speak of this after you have held the post for at least two weeks."),
		  (assign, ":answer", -4),
	  (else_try),
		#In the future we may need a proper quest of some kind, or at least a timer, but this will do for now.
		(assign, ":answer", 1),
		(str_store_faction_name, s14, ":pretender_faction"),
		(str_store_string, s14, "@If not for you I would not sit on this throne, {playername}.  When we started our long walk, few people had the courage to support me.  And fewer still would be willing to put their lives at risk for my cause.  But you didn't hesitate for a moment in throwing yourself at my enemies. We have gone through a lot together, and with God's help, we prevailed.  I will gladly accept you as both my {husband/wife} and co-ruler of the {s14}."),
	  (try_end),

	  (assign, reg65, ":save_reg65"),
	  (assign, reg1, ":save_reg1"),
	  (assign, reg0, ":answer"),
  ]),

  #script_dplmc_center_point_calc
  #
  # Gets the terrain code for a battle between two parties, which
  # is usually a value like rt_desert, but can instead be two
  # special values: -1 for
  #
  # INPUT: arg1 = attacker_party
  #        arg2 = defender_party
  # OUTPUT: reg0 = terrain code (-1 for invalid, -2 for siege)
  ("dplmc_get_terrain_code_for_battle",
   [
      (store_script_param, ":attacker_party", 1),
      (store_script_param, ":defender_party", 2),

      (assign, reg0, dplmc_terrain_code_unknown), #Terrain code, defined in header_terrain_types.py

	  (try_begin),
		#Check for village missions
         (this_or_next|eq, ":attacker_party", "p_main_party"),
			(eq, ":defender_party", "p_main_party"),
		 (ge, "$g_encounter_is_in_village", 1),
		 (assign, reg0, dplmc_terrain_code_village),#defined in header_terrain_types.py
      (else_try),
		#If the attacker party is a town, a castle, a village, a bandit lair, or a ship,
		#set the terrain code to "none" since we don't have any specific ideas for modifying
		#the unit-type performance in scenarios of that type (whatever they are).
         (ge, ":attacker_party", 0),
         (this_or_next|party_slot_eq, ":attacker_party", slot_party_type, spt_town),#no modifier for being attacked by garrisoned troops
         (this_or_next|party_slot_eq, ":attacker_party", slot_party_type, spt_castle),
         (this_or_next|party_slot_eq, ":attacker_party", slot_party_type, spt_village),
         (this_or_next|party_slot_eq, ":attacker_party", slot_party_type, spt_bandit_lair),
			(party_slot_eq, ":attacker_party", slot_party_type, spt_ship),#no modifier for being attacked by a ship
         (assign, reg0, dplmc_terrain_code_unknown),#no terrain options, defined in header_terrain_types.py
	  (else_try),
		#If the attacker party is *attached* to a town/castle/village, a bandit lair, or a ship,
		#set the terrain code to "none" since we don't have any specific ideas for modifying
		#the unit-type performance in scenarios of that type (whatever they are).
	     (ge, ":attacker_party", 0),
	     (party_get_attached_to, ":attachment", ":attacker_party"),
		 (ge, ":attachment", 0),
		 (party_is_active, ":attachment"),
		 (this_or_next|party_slot_eq, ":attachment", slot_party_type, spt_town),#no modifier for being attacked by garrisoned troops
         (this_or_next|party_slot_eq, ":attachment", slot_party_type, spt_castle),
         (this_or_next|party_slot_eq, ":attachment", slot_party_type, spt_village),
         (this_or_next|party_slot_eq, ":attachment", slot_party_type, spt_bandit_lair),
			(party_slot_eq, ":attachment", slot_party_type, spt_ship),#no modifier for being attacked by a ship
         (assign, reg0, dplmc_terrain_code_unknown),#no terrain modifiers
      (else_try),
		#If the attacker party isn't a weird type, the terrain is entirely based on the
		#defender (unless the defender is invalid).
         (ge, ":defender_party", 0),
         (try_begin),
			#If the defender is a walled center, use siege mode.
            (this_or_next|party_slot_eq, ":defender_party", slot_party_type, spt_town),
            (party_slot_eq, ":defender_party", slot_party_type, spt_castle),
            (assign, reg0, dplmc_terrain_code_siege),#siege mode, defined in header_terrain_types.py
		 (else_try),
			#If the defender is a village
			(party_slot_eq, ":defender_party", slot_party_type, spt_village),
			(assign, reg0, dplmc_terrain_code_village),
         (else_try),
			#If the defender is a bandit lair or a ship, use no terrain modifier.
            (this_or_next|party_slot_eq, ":defender_party", slot_party_type, spt_bandit_lair),
				(party_slot_eq, ":defender_party", slot_party_type, spt_ship),
            (assign, reg0, dplmc_terrain_code_unknown),#no terrain modifiers
 		 (else_try),
			#If the defender is attached, do the same checks but for the attachment.
		    (party_get_attached_to, ":attachment", ":defender_party"),
			(ge, ":attachment", 0),
			(party_is_active, ":attachment"),
			(assign, ":attachment_value", -100),
			(try_begin),
				#Walled centers use siege modifiers
			   (this_or_next|party_slot_eq, ":attachment", slot_party_type, spt_town),
			      (party_slot_eq, ":attachment", slot_party_type, spt_castle),
			   (assign, ":attachment_value", dplmc_terrain_code_siege),
			(else_try),
				#Villages
			   (party_slot_eq, ":attachment", slot_party_type, spt_village),
			   (assign, ":attachment_value", dplmc_terrain_code_village),
			(else_try),
				#bandit-lairs and ships have no modifiers currently
			   (this_or_next|party_slot_eq, ":attachment", slot_party_type, spt_bandit_lair),
				(party_slot_eq, ":attachment", slot_party_type, spt_ship),
			   (assign, ":attachment_value", dplmc_terrain_code_unknown),#no terrain modifiers
			(try_end),
			#If neither of the above apply, fall through to the next condition.
			(neq, ":attachment_value", -100),
			(assign, reg0, ":attachment_value"),
         (else_try),
			#Use the terrain under the defender.
			#In the future I might want to change this so there's a tactics contest
			#between the attacker and defender to choose the more favorable ground
			#from their immediate surroundings.  I would also have to change the actual
			#terrain-type code.
            (party_get_current_terrain, reg0, ":defender_party"),
		 (try_end),
      (else_try),
		 #If we get here, it means the defender was invalid, so use the terrain under
		 #the attacker.
         (ge, ":attacker_party", 0),
         (party_get_current_terrain, reg0, ":attacker_party"),#terrain under attacker
      (try_end),
   ]),

  #script_dplmc_party_calculate_strength_in_terrain
  # INPUT: arg1 = party_id
  #        arg2 = terrain (from header_terrain_types.py)
  #        arg3 = exclude leader (0 for do-not-exclude, 1 for exclude)
  #        arg4 = cache policy (1 is use terrain, 2 is use non-terrain, 0 is do not use)
  # OUTPUT: reg0 = strength with terrain
  #         reg1 = strength ignoring terrain
  ("dplmc_party_calculate_strength_in_terrain",
    [
      (store_script_param, ":party", 1), #Party_id
      (store_script_param, ":terrain_type", 2),#a value from header_terrain_types.py
      (store_script_param, ":exclude_leader", 3),#(0 for do-not-exclude, 1 for exclude)
      (store_script_param, ":cache_policy", 4),#1 is use terrain, 2 is use non-terrain, 0 is do not use)

      (assign, ":total_strength_terrain", 0),
      (assign, ":total_strength_no_terrain", 0),

      (party_get_num_companion_stacks, ":num_stacks", ":party"),
      (assign, ":first_stack", 0),
      (try_begin),
        (neq, ":exclude_leader", 0),
        (assign, ":first_stack", 1),
      (try_end),
	  #Bonus for heroes on top of the rest
	  (assign, ":hero_percent", 110),
	  ##Moved setting the multipliers out of the loop...
	  (assign, ":guaranteed_horse_percent", 100),
	  (assign, ":guaranteed_ranged_percent", 100),
	  (assign, ":guaranteed_neither_percent", 100),
	  #First, test for some special codes:
	  (try_begin),
	     (eq, ":terrain_type", dplmc_terrain_code_none),#Apply no modifiers
		 (assign, ":hero_percent", 100),
	  (else_try),
	  	(eq, ":terrain_type", dplmc_terrain_code_village),#A dismounted fight at a village (apply hero modifier, nothing else)
      (else_try),
        (eq, ":terrain_type", dplmc_terrain_code_siege),#A siege battle, not including sorties.
        (assign, ":guaranteed_ranged_percent", 120),
	  #The rest are ordinary rt_* codes.
	  #I changed the balance of these to make the variations less extreme (e.g. 150% mounted strength on rt_steppe).
	  #I believe that the version from ArcherOS is trying to create certain map results, rather than solely
	  #make autocalc strength more accurate in terms of "what would happen if they fought the player".
	  (else_try),
        (eq, ":terrain_type", rt_steppe),
		#The 150% increase in the steppe strikes me as excessive.
		#Since the NPC cost increase for mounted troops is 20%, and the PC cost is 65%,
		#it isn't entirely implausible.
	    #(assign, ":guaranteed_horse_percent", 150),
		#Archer uses 150%, Custom Commander uses a flat 125%.
		(assign, ":guaranteed_horse_percent", 120),
	  (else_try),
		#I am unaware of any game mechanic in live battles that gives any disadvantage
		#to horses on snow or sand as opposed to a plain.
		(this_or_next|eq, ":terrain_type", rt_snow),
		(this_or_next|eq, ":terrain_type", rt_desert),
			(eq, ":terrain_type", rt_plain),
		(assign, ":guaranteed_horse_percent", 120),
     (else_try),
		#I suspect that the 120% mounted bonus for steppe forests is inaccurate,
		#but I haven't checked it out yet.
	    (eq, ":terrain_type", rt_steppe_forest),
        (assign, ":guaranteed_horse_percent", 120),
     (else_try),
        (this_or_next|eq, ":terrain_type", rt_forest),
        (this_or_next|eq, ":terrain_type", rt_mountain_forest),
		     (eq, ":terrain_type", rt_snow_forest),
        #(assign, ":guaranteed_neither_percent", 120),
		(assign, ":guaranteed_neither_percent", 110),
	 (try_end),

      (try_for_range, ":i_stack", ":first_stack", ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party", ":i_stack"),
        (store_character_level, ":stack_strength", ":stack_troop"),
        (val_add, ":stack_strength", 4), #new was 12 (patch 1.125)
        (val_mul, ":stack_strength", ":stack_strength"),
        (val_mul, ":stack_strength", 2), #new (patch 1.125)
        #move the next two lines to after terrain advantage
        #(val_div, ":stack_strength", 100),
        #(val_max, ":stack_strength", 1), #new (patch 1.125)
        (assign, ":terrain_free_strength", ":stack_strength"),
        ##use Arch3r's terrain advantage code (bug-fix changes 2011-04-13; other changes 2011-04-25)
        (try_begin),
           ##AotE terrain advantages
           (assign, ":hero_horse", 0),#added for heroes (any positive number = has a horse)
           (try_begin),
		      (this_or_next|eq, "trp_player", ":stack_troop"),
				(troop_is_hero, ":stack_troop"),
		      (gt, ":guaranteed_horse_percent", ":hero_percent"),#don't bother if we wouldn't use the result
              (neg|troop_is_guarantee_horse, ":stack_troop"),#don't bother if we already know the troop has a horse
			  (store_skill_level, reg0, "skl_riding", ":stack_troop"),
			  (ge, reg0, 2),#don't bother if the troop has no/minimal riding skill
			  #Just checking ek_horse may not work for non-companions, so check the inventory
			  (troop_get_inventory_capacity, ":inv_cap", ":stack_troop"),
			  (ge, ":inv_cap", 1),
			  (val_min, ":inv_cap", dplmc_ek_alt_items_begin + 8),#Don't check too much of the inventory
			  (try_for_range, ":inv_slot", 0, ":inv_cap"),
				(troop_inventory_slot_get_item_amount, reg1, ":stack_troop", ":inv_slot"),
				(ge, reg1, 1),#quantity must be greater than zero
				(troop_get_inventory_slot, reg0, ":stack_troop", ":inv_slot"),
				(ge, reg0, 1),#must be a valid item
				(item_get_type, reg1, reg0),#check if the item is a horse
				(eq, reg1, itp_type_horse),
				(assign, ":inv_cap", ":inv_slot"),#break loop
			  (try_end),
			  #If no horse found, set to zero
              (neg|is_between, ":hero_horse", horses_begin, horses_end),
              (assign, ":hero_horse", 0),
           (try_end),
		   (assign, ":stack_strength_multiplier", 100),#<-- percent multiplier
           (try_begin),#Mounted troops
			  (this_or_next|ge, ":hero_horse", 1),
              (troop_is_guarantee_horse, ":stack_troop"),
              (assign, ":stack_strength_multiplier", ":guaranteed_horse_percent"),
		   (else_try),#Ranged troops
              (troop_is_guarantee_ranged, ":stack_troop"),
              (assign, ":stack_strength_multiplier", ":guaranteed_ranged_percent"),
           (else_try),#Infantry
              (assign, ":stack_strength_multiplier", ":guaranteed_neither_percent"),
           (try_end),

		   #Use hero/player modifiers if a better one didn't apply
		   (try_begin),
		      (this_or_next|eq, ":stack_troop", "trp_player"),
			     (troop_is_hero, ":stack_troop"),
			  (val_max, ":stack_strength_multiplier", ":hero_percent"),#hero bonus
		   (try_end),

		   (val_mul, ":stack_strength", ":stack_strength_multiplier"),
		   (val_add, ":stack_strength", 50),#add this before division for correct rounding
           (val_div, ":stack_strength", 100),
           ##AotE terrain advantages
        (try_end),
        #moved the next two lines here from above
        (val_div, ":stack_strength", 100),#<- moved here from above
        (val_max, ":stack_strength", 1), #new (patch 1.125) #<- moved here from above
        (val_div, ":terrain_free_strength", 100),
        (val_max, ":terrain_free_strength", 1),
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":stack_size", ":num_wounded"),
          (val_mul, ":stack_strength", ":stack_size"),
          (val_mul, ":terrain_free_strength", ":stack_size"),
        (else_try),
          (troop_is_wounded, ":stack_troop"), #hero & wounded
          (assign, ":stack_strength", 0),
          (assign, ":terrain_free_strength", 0),
        (try_end),
        (val_add, ":total_strength_terrain", ":stack_strength"),
        (val_add, ":total_strength_no_terrain", ":terrain_free_strength"),
      (try_end),
	  #Load results into registers and cache if appropriate
	  (assign, reg0, ":total_strength_terrain"),
	  (assign, reg1, ":total_strength_no_terrain"),
      (try_begin),
         (eq, ":cache_policy", 1),
         (party_set_slot, ":party", slot_party_cached_strength, reg0),
      (else_try),
         (eq, ":cache_policy", 2),
         (party_set_slot, ":party", slot_party_cached_strength, reg1),
      (try_end),
  ]),


  #script_dplmc_player_can_give_troops_to_troop  (Warning, clobbers {s11}!)
  #
  # INPUT: arg1 = troop_id
  # OUTPUT: reg0 = 1 or more is yes, 0 or less is no
  #
  # This script does not take into account things like whether the troop
  # is a prisoner of a party, so it can be used for checking whether troops
  # can be added to a garrison.
  #
  # The general logic is that you can give troops to a member of your
  # own faction if any of the following are true:
  #   - You are the faction leader or marshall
  #   - You are the spouse of the faction leader, and the faction
  #     leader is not on bad terms with you
  #   - The troop is an affiliated family member
  #   - The troop is your spouse, and is either pliable or not on bad terms
  #   - The troop is a former companion with whom you are on good terms
  #   - The troop is related to you by marriage and you are on good terms
  #
  # For allied factions, the conditions are similar to the above.
  # However, being the marshall or leader of your own faction does not
  # guarantee cooperation from lords who dislike you.
  #
  # For non-allied other factions, the check for faction leader or
  # marshall are not relevant, and the faction must not be at war
  # with the player's faction.
  ("dplmc_player_can_give_troops_to_troop",
  [
	(store_script_param, ":troop_id", 1), #Party_id
	(assign, ":can_give_troops", 0),
	(assign, ":save_reg1", reg1),

	(try_begin),
		(this_or_next|eq, ":troop_id", "trp_kingdom_heroes_including_player_begin"),
		(eq, ":troop_id", "trp_player"),
		(assign, ":can_give_troops", 1),
	(else_try),
		(lt, ":troop_id", 1),
		(assign, ":can_give_troops", 0),
	(else_try),
		(store_faction_of_troop, ":troop_faction", ":troop_id"),

		(call_script, "script_troop_get_player_relation", ":troop_id"),
		(assign, ":troop_relation", reg0),
		(troop_get_slot, ":troop_reputation", ":troop_id", slot_lord_reputation_type),

		(try_begin),
			#Troop is member of player supporters faction
			(eq, ":troop_faction", "fac_player_supporters_faction"),
			##Always yes in Native, but if centralization is negative allow non-compliance
			(faction_get_slot, reg0, ":troop_faction", dplmc_slot_faction_centralization),
			(try_begin),
				(ge, reg0, 0),
				(assign, reg0, -200),
			(else_try),
				(val_mul, reg0, -10),
				(val_add, reg0, -35),#Centralization -1 has -25, -2 has -15, and -3 has -5
			(try_end),
			(gt, ":troop_relation", reg0),
			(assign, ":can_give_troops", 1),
		(else_try),
			#Troop is a member of the same faction as the player
			(eq, ":troop_faction", "$players_kingdom"),
			(faction_get_slot, ":troop_faction_leader", ":troop_faction", slot_faction_leader),
			(try_begin),
				#Leader or marshall
				(this_or_next|eq, ":troop_faction_leader", "trp_player"),
					(faction_slot_eq, ":troop_faction", slot_faction_marshall, "trp_player"),
				#If centralization is negative allow non-compliance
				(faction_get_slot, reg0, ":troop_faction", dplmc_slot_faction_centralization),
				(try_begin),
					(ge, reg0, 0),
					(assign, reg0, -200),
				(else_try),
					(val_mul, reg0, -10),
					(val_add, reg0, -35),#Centralization -1 has -25, -2 has -15, and -3 has -5
				(try_end),
				(gt, ":troop_relation", reg0),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Spouse of leader
				(gt, ":troop_faction_leader", 1),
				(neg|troop_slot_eq, "trp_player", slot_troop_spouse, -1),
				(this_or_next|troop_slot_eq, ":troop_faction_leader", slot_troop_spouse, "trp_player"),
					(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_faction_leader"),
				(call_script, "script_troop_get_player_relation", ":troop_faction_leader"),
				(ge, reg0, 0),
				#If centralization is negative allow non-compliance
				(faction_get_slot, reg0, ":troop_faction", dplmc_slot_faction_centralization),
				(try_begin),
					(ge, reg0, 0),
					(assign, reg0, -200),
				(else_try),
					(val_mul, reg0, -10),
					(val_add, reg0, -35),#Centralization -1 has -25, -2 has -15, and -3 has -5
				(try_end),
				(gt, ":troop_relation", reg0),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Spouse of troop
				(neg|troop_slot_eq, "trp_player", slot_troop_spouse, -1),
				(this_or_next|troop_slot_eq, ":troop_id", slot_troop_spouse, "trp_player"),
					(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_id"),
				(this_or_next|ge, ":troop_relation", 0),
				(this_or_next|eq, ":troop_reputation", lrep_conventional),
				(this_or_next|eq, ":troop_reputation", lrep_moralist),
					(eq, ":troop_reputation", lrep_otherworldly),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Affiliated family member
				(call_script, "script_dplmc_is_affiliated_family_member", ":troop_id"),
				(ge, reg0, 1),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Close companion previously under arms
				(this_or_next|is_between, ":troop_id", companions_begin, companions_end),
					(is_between, ":troop_id", pretenders_begin, pretenders_end),
				(neg|troop_slot_eq, ":troop_id", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
				(ge, ":troop_relation", 20),
				(assign, ":can_give_troops", 1),
			(else_try),
				#In-law (or hypothetically a blood relative) who is close with the player
				(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":troop_id", "trp_player"),
				(ge, reg0, 2),#<-- deliberately set the cutoff to 2, not 1
				(ge, ":troop_relation", 14),
				(this_or_next|ge, reg0, 10),
					(ge, ":troop_relation", 20),
				(assign, ":can_give_troops", 1),
			(try_end),
		(else_try),
			#Troop is member of a faction allied with the player's
			(call_script, "script_dplmc_get_faction_truce_length_with_faction", "$players_kingdom", ":troop_faction"),
			(gt, reg0, dplmc_treaty_defense_days_expire),
			(faction_get_slot, ":player_faction_leader", "$players_kingdom", slot_faction_leader),
			(try_begin),
				#Leader or marshall
				(this_or_next|eq, ":player_faction_leader", "trp_player"),
					(faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
				(ge, ":troop_relation", 0),#only for allied factions, not for the player's own faction
				(assign, ":can_give_troops", 1),
			(else_try),
				#Spouse of leader
				(gt, ":player_faction_leader", 1),
				(neg|troop_slot_eq, "trp_player", slot_troop_spouse, -1),
				(this_or_next|troop_slot_eq, ":player_faction_leader", slot_troop_spouse, "trp_player"),
					(troop_slot_eq, "trp_player", slot_troop_spouse, ":player_faction_leader"),
				(ge, ":troop_relation", 0),#only for allied factions, not for the player's own faction
				(call_script, "script_troop_get_player_relation", ":player_faction_leader"),
				(ge, reg0, 0),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Spouse of troop
				(neg|troop_slot_eq, "trp_player", slot_troop_spouse, -1),
				(this_or_next|troop_slot_eq, ":troop_id", slot_troop_spouse, "trp_player"),
					(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_id"),
				(this_or_next|ge, ":troop_relation", 0),
				(this_or_next|eq, ":troop_reputation", lrep_conventional),
				(this_or_next|eq, ":troop_reputation", lrep_moralist),
					(eq, ":troop_reputation", lrep_otherworldly),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Affiliated family member
				(call_script, "script_dplmc_is_affiliated_family_member", ":troop_id"),
				(ge, reg0, 1),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Close companion previously under arms
				(this_or_next|is_between, ":troop_id", companions_begin, companions_end),
					(is_between, ":troop_id", pretenders_begin, pretenders_end),
				(neg|troop_slot_eq, ":troop_id", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
				(ge, ":troop_relation", 20),
				(assign, ":can_give_troops", 1),
			(else_try),
				#In-law (or hypothetically a blood relative) who is close with the player
				(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":troop_id", "trp_player"),
				(ge, reg0, 2),#<-- deliberately set the cutoff to 2, not 1
				(ge, ":troop_relation", 14),
				(this_or_next|ge, reg0, 10),
					(ge, ":troop_relation", 20),
				(assign, ":can_give_troops", 1),
			(try_end),
		(else_try),
			#Troop is a member of a faction that isn't hostile to the player's
			(store_relation, reg0, ":troop_faction", "fac_player_faction"),
			(ge, reg0, 0),
			(store_relation, reg0, ":troop_faction", "$players_kingdom"),
			(ge, reg0, 0),
			(try_begin),
				#Spouse of troop
				(neg|troop_slot_eq, "trp_player", slot_troop_spouse, -1),
				(this_or_next|troop_slot_eq, ":troop_id", slot_troop_spouse, "trp_player"),
					(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_id"),
				(this_or_next|ge, ":troop_relation", 0),
				(this_or_next|eq, ":troop_reputation", lrep_conventional),
				(this_or_next|eq, ":troop_reputation", lrep_moralist),
					(eq, ":troop_reputation", lrep_otherworldly),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Affiliated family member
				(call_script, "script_dplmc_is_affiliated_family_member", ":troop_id"),
				(ge, reg0, 1),
				(assign, ":can_give_troops", 1),
			(else_try),
				#Close companion previously under arms
				(this_or_next|is_between, ":troop_id", companions_begin, companions_end),
					(is_between, ":troop_id", pretenders_begin, pretenders_end),
				(neg|troop_slot_eq, ":troop_id", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
				(ge, ":troop_relation", 20),
				(assign, ":can_give_troops", 1),
			(else_try),
				#In-law (or hypothetically a blood relative) who is close with the player
				(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":troop_id", "trp_player"),
				(ge, reg0, 2),#<-- deliberately set the cutoff to 2, not 1
				(ge, ":troop_relation", 14),
				(this_or_next|ge, reg0, 10),
					(ge, ":troop_relation", 20),
				(assign, ":can_give_troops", 1),
			(try_end),
		(try_end),
	(try_end),

	(assign, reg1, ":save_reg1"),
	(assign, reg0, ":can_give_troops"),
  ]),

  #script_dplmc_print_centers_in_numbers_to_s0
  #
  # Input: arg1 = target_center
   ("dplmc_prepare_hero_center_points_ignoring_center",[
	  (store_script_param, ":target_center", 1),

	  (troop_set_slot, "trp_player", slot_troop_temp_slot, 0),
	  (troop_set_slot, "trp_player", dplmc_slot_troop_temp_slot, 0),

	  (try_for_range, ":troop_no", heroes_begin, heroes_end),
		(troop_set_slot, ":troop_no", slot_troop_temp_slot, 0),
		(troop_set_slot, ":troop_no", dplmc_slot_troop_temp_slot, 0),
	  (try_end),

	  (try_for_range, ":center_no", centers_begin, centers_end),
	    #Skip "target center"
		(neq, ":center_no", ":target_center"),

		#Lord is player or a hero
		(party_get_slot, ":troop_no", ":center_no", slot_town_lord),
		(this_or_next|eq, ":troop_no", "trp_player"),
			(is_between, ":troop_no", heroes_begin, heroes_end),

		#Update lord point total
		(assign, ":center_points", 1),
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_town),
			(assign, ":center_points", 3),
		(else_try),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
			(assign, ":center_points", 2),
		(try_end),

		(troop_get_slot, ":slot_value", ":troop_no", slot_troop_temp_slot),
		(val_add, ":slot_value", ":center_points"),
		(troop_set_slot, ":troop_no", slot_troop_temp_slot, ":slot_value"),

		#Update distance from closest owned center to target
		(is_between, ":target_center", centers_begin, centers_end),
		(troop_get_slot, ":slot_value", ":troop_no", dplmc_slot_troop_temp_slot),
		(store_distance_to_party_from_party, ":cur_distance", ":target_center", ":center_no"),
		(val_max, ":cur_distance", 1),
		(try_begin),
			(eq, ":slot_value", 0),
			(assign, ":slot_value", ":cur_distance"),
		(try_end),
		(val_min, ":slot_value", ":cur_distance"),
		(troop_set_slot, ":troop_no", dplmc_slot_troop_temp_slot, ":slot_value"),
	  (try_end),
	  ##Update cached totals
	  (try_for_range, ":troop_no", heroes_begin, heroes_end),
		(troop_get_slot, reg0, ":troop_no", slot_troop_temp_slot),
		(val_add, reg0, 1),
		(troop_set_slot, ":troop_no", dplmc_slot_troop_center_points_plus_one, reg0),
          (try_end),
          (troop_get_slot, reg0, "trp_player", slot_troop_temp_slot),
          (val_add, reg0, 1),
          (troop_set_slot, "trp_player", dplmc_slot_troop_center_points_plus_one, reg0),
          #Since the target center was omitted from the point totals, handle it here
	  (try_begin),
		(is_between, ":target_center", centers_begin, centers_end),
		(party_get_slot, ":troop_no", ":target_center", slot_town_lord),
		#Only perform this update for a troop whose center point value was updated above
		(this_or_next|is_between, ":troop_no", heroes_begin, heroes_end),
		(eq, ":troop_no", "trp_player"),
		(troop_get_slot, reg0, ":troop_no", dplmc_slot_troop_center_points_plus_one),
		(val_add, reg0, 1),#1 point for villages
		(try_begin),
		   (is_between, ":target_center", walled_centers_begin, walled_centers_end),
		   (val_add, reg0, 1),#2 points for castles
		   (is_between, ":target_center", towns_begin, towns_end),
		   (val_add, reg0, 1),#3 points for towns
		(try_end),
		(troop_set_slot, ":troop_no", dplmc_slot_troop_center_points_plus_one, reg0),
	  (try_end),
   ]),


  # script_dplmc_calculate_troop_score_for_center_aux
  #auto sell credit rubik (CC) begin:
  #
  # script_dplmc_auto_sell
  # INPUTS:
  #    arg1 :customer (the one selling the stuff)
  #    arg2 :merchant (the one buying the stuff)
  #    arg3 :auto_sell_price_limit (only sell stuff less expensive than this)
  #    arg4 :valid_items_begin (use this to only sell a limited range of things)
  #    arg5 :valid_items_end   (use this to only sell a limited range of things)
  #    arg6 :actually_sell_items (set to 0 for a "dry run"; set to 2 to print a descriptive message;
  #          set to 4 for center autosell cleanup that skips backup-equipment protection)
  #
  # OUTPUTS:
  #    reg0 amount of gold gained by customer (not actually gained if this was a dry run)
  #    reg1 number of items sold by customer (not actually sold if this was a dry run)
  ("dplmc_auto_sell", [
	#This script has various changes from the CC version.
	#In particular, all parameters other than "customer" and "merchant",
	#and reporting the number of items & gold change.
	(store_script_param, ":customer", 1),
	(store_script_param, ":merchant", 2),
	#dplmc+ start added parameters
	(store_script_param, ":auto_sell_price_limit", 3),
	(store_script_param, ":valid_items_begin", 4),
	(store_script_param, ":valid_items_end", 5),
	(store_script_param, ":actually_sell_items", 6),
	#dplmc+ end added parameters

	#dplmc+ added section begin
	(assign, ":save_reg2", reg2),
	(assign, ":save_reg3", reg3),
	(assign, ":save_reg65", reg65),
	(assign, ":save_talk_troop", "$g_talk_troop"),
	#The talk troop is used for price information, but it's possible for this to be called
	#from other contexts (like a menu).
	(assign, "$g_talk_troop", ":merchant"),

	(assign, ":gold_gained", 0),
	(assign, ":items_sold", 0),
	#(assign, ":most_expensive_sold_item", -1),
	#(assign, ":most_expensive_sold_imod", -1),
	#(assign, ":most_expensive_sold_price", -1),
	#dplmc+ added section end

    (troop_get_inventory_capacity, ":inv_cap", ":customer"),
    (assign, ":first_sell_slot", dplmc_ek_alt_items_end),
    (try_begin),
      (eq, ":actually_sell_items", 4),
      (assign, ":first_sell_slot", dplmc_ek_alt_items_begin),
    (try_end),
	(set_show_messages, 0),#<-dplmc+ added
    (try_for_range_backwards, ":i_slot", ":first_sell_slot", ":inv_cap"),#conservative autosell reserves several "safe" slots in the beginning of the inventory
      (troop_get_inventory_slot, ":item", ":customer", ":i_slot"),
      (troop_get_inventory_slot_modifier, ":imod", ":customer", ":i_slot"),
      (gt, ":item", -1),
      (item_get_type, ":type", ":item"),
      (item_slot_eq, ":type", dplmc_slot_item_type_not_for_sell, 0),
	  #dplmc+ begin added constraints
	  (is_between, ":item", ":valid_items_begin", ":valid_items_end"),
	  (neg|is_between, ":type", books_begin, books_end),
	  (this_or_next|neg|is_between, ":item", food_begin, food_end),
	     (eq, ":imod", imod_rotten),
	  (neg|is_between, ":item", trade_goods_begin, trade_goods_end),
	  (neq, ":imod", imod_lordly),#dplmc+: never sell "lordly" items
	  #dplmc+ end added constraints

      (call_script, "script_dplmc_get_item_value_with_imod", ":item", ":imod"),
      (assign, ":score", reg0),
      (val_div, ":score", 100),
      (call_script, "script_game_get_item_sell_price_factor", ":item"),
      (assign, ":sell_price_factor", reg0),
      (val_mul, ":score", ":sell_price_factor"),
      (val_div, ":score", 100),
      (val_max, ":score",1),

	  #dplmc+ start changed section
	  (le, ":score", ":auto_sell_price_limit"),

	  #For equipment, in general don't sell the item unless you have a better one,
	  #or the item is useless to you.  (The idea is to stop from accidentally
	  #selling the player's own equipment.)
	  (item_get_type, ":this_item_type", ":item"),

	  #Normally, we would do the following:

	  #(try_begin),
	  #   (item_slot_eq, ":item", dplmc_slot_two_handed_one_handed, 1),
	  #	 (assign, ":this_item_type", 11), # type 11 = two-handed/one-handed
	  #(try_end),

	  #However, we are delaying that step until later, because type 11 is the
	  #same as itp_type_goods.


	  #Don't sell items if there's a reasonable chance that they might
	  #be the player's alternate personal equipment.  It goes without saying
	  #that items the player can't use aren't counted.
	  #
	  #(Items the player has equipped will not even be considered for sale,
	  #but it is common for players to have a variety of items they use in
	  #different circumstances, which might not all be equipped.)
	  #
	  #For melee weapons: don't sell the best weapon or the second-best of a type
	  #   (it might be a backup, or there might be a variety of weapons of
	  #   the same type in situational use)
	  #For shields: don't sell the best or second-best shield
	  #For thrown weapons: don't sell the best three thrown weapons
	  #For ammunition: don't sell the best three of the ammunition kind (arrows,
	  #   bolts) unless you lack a weapon that uses the ammunition.
	  #For armor: don't sell the best armor of a kind.
	  #For horses: don't sell the best or second-best horse
	  #For bows and crossbows: don't sell the best item of a kind (all bows are
	  #   very similar, so there's little chance someone would carry an alternate)
	  #For muskets and pistols: don't sell the best or second-best weapon of
	  #   a kind.

	  (assign, ":can_sell", 1),

	  (try_begin),
		 (eq, ":actually_sell_items", 4),
	  (else_try),
		 #Damaged or low-quality inventory items should not be preserved as backup gear.
	     (this_or_next|eq, ":imod", imod_cracked),
	     (this_or_next|eq, ":imod", imod_rusty),
	     (this_or_next|eq, ":imod", imod_bent),
	     (this_or_next|eq, ":imod", imod_chipped),
	     (this_or_next|eq, ":imod", imod_battered),
	     (this_or_next|eq, ":imod", imod_poor),
	     (this_or_next|eq, ":imod", imod_crude),
	     (this_or_next|eq, ":imod", imod_old),
	     (eq, ":imod", imod_cheap),
	  (else_try),
		 #Ammunition type: arrows (if you have a bow you can use, don't sell the best 3 arrow packs you have)
	     (eq, ":this_item_type", itp_type_arrows),
		 (call_script, "script_dplmc_scan_for_best_item_of_type", ":customer", itp_type_bow, ":customer"),
		 (try_begin),
			(ge, reg0, 0),
			(call_script, "script_dplmc_count_better_items_of_same_type", ":customer", ":item", ":imod", ":customer"),
			(lt, reg0, 3),#must not be best (0), second-best (1), or third-best (2)
			(assign, ":can_sell", 0),
		 (try_end),
	  (else_try),
		#Ammunition type: bolts (if you have a crossbow you can use, don't sell the best 3 bolt packs you have)
	     (eq, ":this_item_type", itp_type_bolts),
		 (call_script, "script_dplmc_scan_for_best_item_of_type", ":customer", itp_type_crossbow, ":customer"),
		 (try_begin),
			(ge, reg0, 0),
			(call_script, "script_dplmc_count_better_items_of_same_type", ":customer", ":item", ":imod", ":customer"),
			(lt, reg0, 3),#must not be best (0), second-best (1), or third-best (2)
			(assign, ":can_sell", 0),
		 (try_end),
	  (else_try),
		#Ammunition type: bullets (if you have a pistol or musket you can use, don't sell the best 3 bullet packs you have)
	     (eq, ":this_item_type", itp_type_bullets),
		 #Do muskets and pistols both use bullets?  I'll assume so.
		 (call_script, "script_dplmc_scan_for_best_item_of_type", ":customer", itp_type_musket, ":customer"),
		 (assign, reg1, reg0),
		 (call_script, "script_dplmc_scan_for_best_item_of_type", ":customer", itp_type_pistol, ":customer"),
		 (try_begin),
			(this_or_next|ge, reg0, 0),
				(ge, reg1, 0),
			(call_script, "script_dplmc_count_better_items_of_same_type", ":customer", ":item", ":imod", ":customer"),
			(lt, reg0, 3),
			(assign, ":can_sell", 0),
		 (try_end),
	  (else_try),
		#Catch: all non-usable equipment
		(is_between, ":this_item_type", itp_type_horse, itp_type_musket + 1),
		(neq, ":this_item_type", itp_type_goods),
		(call_script, "script_dplmc_troop_can_use_item", ":customer", ":item", ":imod"),
		(eq, reg0, 0),#Past here, we don't have to check for usability
	  (else_try),
		#Thrown weapons: don't sell best 3 you can use
		(eq, ":this_item_type", itp_type_thrown),
		(call_script, "script_dplmc_count_better_items_of_same_type", ":customer", ":item", ":imod", ":customer"),
		(store_sub, ":can_sell", reg0, 2),#must not be best (0) or second-best (1) or third-best (2)
	  (else_try),
		#Types where both the best and the second-best aren't sold
		#Horses, shields, melee weapons, and firearms
		(this_or_next|is_between, ":this_item_type", itp_type_horse, itp_type_polearm + 1),
		(this_or_next|eq, ":this_item_type", itp_type_shield),
		(this_or_next|eq, ":this_item_type", itp_type_pistol),
			(eq, ":this_item_type", itp_type_musket),
		(call_script, "script_dplmc_count_better_items_of_same_type", ":customer", ":item", ":imod", ":customer"),
		(store_sub, ":can_sell", reg0, 1),#must not be best (0) or second best (1)
 	  (else_try),
		#Types where the best isn't sold (armor, not including shields)
		(is_between, ":this_item_type", itp_type_head_armor, itp_type_hand_armor + 1),
		(call_script, "script_dplmc_count_better_items_of_same_type", ":customer", ":item", ":imod", ":customer"),
		(assign, ":can_sell", reg0),#must not be best (0)
	  (try_end),

	  #(try_begin),
	  #   (lt, ":can_sell", 1),
	  #	 (gt, "$cheat_mode", 0),
	  #	 (call_script, "script_dplmc_count_better_items_of_same_type", ":customer", ":item", ":imod", ":customer"),
 	  #	 (assign, reg1, ":i_slot"),
	  #	 (str_store_item_name, s0, ":item"),
	  #	 (display_message, "@{!} DEBUG - Will not sell item {s0} at slot {reg1}.  Better items of same kind: {reg0}"),
	  #(try_end),

	  (ge, ":can_sell", 1),

	  #(try_begin),
	  #	(ge, ":score", ":most_expensive_sold_price"),
	  #	(assign, ":most_expensive_sold_item", ":item"),
	  #	(assign, ":most_expensive_sold_imod", ":imod"),
	  #	(assign, ":most_expensive_sold_price", ":score"),
	  #(try_end),

	  #Log the transaction even if in dry run mode
	  (val_add, ":gold_gained", ":score"),
	  (val_add, ":items_sold", 1),

	  #If not a dry run, apply the transaction
	  (neq, ":actually_sell_items", 0),
	  (troop_set_inventory_slot, ":customer", ":i_slot", -1),
	  (troop_add_gold, ":customer", ":score"),
      #dplmc+ end changed section
    (try_end),

	(set_show_messages, 1),#<- dplmc+ added

	#dplmc+ added section begin
	#Print a message if appropriate
	(try_begin),
		(is_between, ":actually_sell_items", 2, 5),#2, 3, or 4
		(this_or_next|ge, ":items_sold", 1),
			(eq, ":actually_sell_items", 3),
		(assign, reg0, ":gold_gained"),
		(assign, reg1, ":items_sold"),
		(store_sub, reg3, reg1, 1),
		(str_store_troop_name, s0, ":merchant"),
		(try_begin),
			(this_or_next|is_between, ":merchant", quick_battle_troops_begin, quick_battle_troops_end),
			(this_or_next|is_between, ":merchant", heroes_begin, heroes_end),
			(this_or_next|is_between, ":merchant", dplmc_employees_begin, dplmc_employees_end),
			(is_between, ":merchant", walkers_end, tournament_champions_end),
			(display_message, "@You sold {reg1} {reg3?items:item} to {s0} and gained {reg0} {reg3?denars:denar}."),
		(else_try),
			(display_message, "@You sold {reg1} {reg3?items:item} to the {s0} and gained {reg0} {reg3?denars:denar}."),
		(try_end),
	(try_end),

	#Revert variables
	(assign, reg2, ":save_reg2"),
	(assign, reg3, ":save_reg3"),
	(assign, reg65, ":save_reg65"),
	(assign, "$g_talk_troop", ":save_talk_troop"),

	#Return diagnostics
	(assign, reg0, ":gold_gained"),
	(assign, reg1, ":items_sold"),
	#dplmc+ added section end
  ]),
  #auto sell credit rubik (CC) end

  ##For use with autosell
  #Input: center_no
  #Output: none
  ("dplmc_player_auto_sell_at_center", [
     (store_script_param, ":center_no", 1),
	 (assign, ":save_reg0", reg0),
	 (assign, ":save_reg1", reg1),
	 (try_begin),
	    ##For Towns:
		(is_between, ":center_no", towns_begin, towns_end),
		(try_begin),
			#1. Selling weapons, shields, and ranged weapons to the weaponsmith
		    (party_get_slot, ":merchant_troop", ":center_no", slot_town_weaponsmith),
			(ge, ":merchant_troop", 1),
			(call_script, "script_dplmc_auto_sell", "trp_player", ":merchant_troop", "$g_dplmc_auto_sell_price_limit", weapons_begin, ranged_weapons_end, 4),
		(try_end),
		(try_begin),
			#2. Selling armor to the armorer
			(party_get_slot, ":merchant_troop", ":center_no", slot_town_armorer),
			(ge, ":merchant_troop", 1),
			(call_script, "script_dplmc_auto_sell", "trp_player", ":merchant_troop", "$g_dplmc_auto_sell_price_limit", armors_begin, armors_end, 4),
 		(try_end),
		(try_begin),
			#3. Selling horses to the horse merchant
			(party_get_slot, ":merchant_troop", ":center_no", slot_town_horse_merchant),
			(ge, ":merchant_troop", 1),
			(call_script, "script_dplmc_auto_sell", "trp_player", ":merchant_troop", "$g_dplmc_auto_sell_price_limit", horses_begin, horses_end, 4),
		(try_end),
		(try_begin),
			#4. Selling whatever may remain to the general merchant
			(party_get_slot, ":merchant_troop", ":center_no", slot_town_merchant),
			(ge, ":merchant_troop", 1),
			(call_script, "script_dplmc_auto_sell", "trp_player", ":merchant_troop", "$g_dplmc_auto_sell_price_limit", all_items_begin, all_items_end, 4),
		(try_end),
	 (else_try),
		##For Villages:
		(is_between, ":center_no", villages_begin, villages_end),
		(party_get_slot, ":merchant_troop", ":center_no", slot_town_elder),
		(ge, ":merchant_troop", 1),
		(call_script, "script_dplmc_auto_sell", "trp_player", ":merchant_troop", "$g_dplmc_auto_sell_price_limit", all_items_begin, all_items_end, 4),
	 (else_try),
        #Don't show an error for castles, since we wouldn't expect this to work there
        (neg|is_between, ":center_no", castles_begin, castles_end),
	    ##Error
		(assign, reg0, ":center_no"),
		(display_message, "@{!} ERROR FOR AUTOSELL for town ID {reg0}: Bad town or merchant was missing"),
	 (try_end),
	 (assign, reg0, ":save_reg0"),
	 (assign, reg1, ":save_reg1"),
  ]),

##Adapted Auto-Buy-Food from rubik's Custom Commander
#Changed to parameterize merchant and customer, but did not finish expanding
#the script to work with non-player arguments.  (There is currently no need,
#but I can imagine using it for NPCs sent on item-purchasing missions, or if
#NPC parties had to buy food.)
#
##OLD: Overwrites: reg1, reg2, reg3, reg4
##NEW: Overwrite reg0
#
#INPUT:
#      arg1 :customer
#      arg2 :merchant_troop
  ("dplmc_auto_buy_food", [
    (store_script_param, ":customer", 1),
    (store_script_param, ":merchant_troop", 2),
    ##added section begin, preserve registers
    (assign, ":save_reg1", reg1),
    (assign, ":save_reg2", reg2),
    (assign, ":save_reg3", reg3),
    (assign, ":save_reg4", reg4),
    ##added section end

    (assign, ":customer_in_player_party", 0),#Always assumed true... re-write if you need to use for others

    (store_troop_gold, ":begin_gold", ":customer"),
    (store_free_inventory_capacity, ":begin_space", ":customer"),
    (troop_get_inventory_capacity, ":inv_cap", ":merchant_troop"),
    (set_show_messages, 0),
    (try_for_range, ":i_slot", 10, ":inv_cap"),
      (troop_get_inventory_slot, ":item", ":merchant_troop", ":i_slot"),
      (gt, ":item", -1),
      (is_between, ":item", itm_raw_date_fruit, food_end),
      (neq, ":item", "itm_furs"),
      (troop_inventory_slot_get_item_amount, ":amount", ":merchant_troop", ":i_slot"),
      ##dplmc+: The next line required making a change to header_operations.py
      (troop_inventory_slot_get_item_max_amount, ":max_amount", ":merchant_troop", ":i_slot"),
      (eq, ":amount", ":max_amount"),

      (item_get_slot, ":food_portion", ":item", dplmc_slot_item_food_portion),
      (val_max, ":food_portion", 0),#dplmc+ added
      (store_item_kind_count, ":food_count", ":item", ":customer"),
      (lt, ":food_count", ":food_portion"),
      (store_free_inventory_capacity, ":free_inv_cap", ":customer"),
      (gt, ":free_inv_cap", 0),

      (call_script, "script_game_get_item_buy_price_factor", ":item"),
      (assign, ":buy_price_factor", reg0),
      (store_item_value,":score",":item"),
      (val_mul, ":score", ":buy_price_factor"),
      (val_div, ":score", 100),
      (val_max, ":score",1),
      (store_troop_gold, ":customer_gold", ":customer"),
      (ge, ":customer_gold", ":score"),

      (troop_add_item, ":customer", ":item"),
      (troop_set_inventory_slot, ":merchant_troop", ":i_slot", -1),
      (troop_remove_gold, ":customer", ":score"),
      (troop_add_gold, ":merchant_troop", ":score"),
    (try_end),
    (set_show_messages, 1),
    (store_troop_gold, ":end_gold", ":customer"),
    (store_free_inventory_capacity, ":end_space", ":customer"),
    (try_begin),
      (neq, ":end_gold", ":begin_gold"),
      (store_sub, reg1, ":begin_gold", ":end_gold"),
      (store_sub, reg2, ":begin_space", ":end_space"),
      (store_sub, reg3, reg1, 1),
      (store_sub, reg4, reg2, 1),
      (eq, ":customer_in_player_party", 1),#<- added
      (display_message, "@You have bought {reg2} {reg4?kinds:kind} of food and lost {reg1} {reg3?denars:denar}."),
    (try_end),

    # sell rotten food
    (store_troop_gold, ":begin_gold", ":customer"),
    (store_free_inventory_capacity, ":begin_space", ":customer"),
    (troop_get_inventory_capacity, ":inv_cap", ":customer"),
    (set_show_messages, 0),
    (try_for_range, ":i_slot", 10, ":inv_cap"),
      (troop_get_inventory_slot, ":item", ":customer", ":i_slot"),
      (gt, ":item", -1),
      (is_between, ":item", food_begin, food_end),
      (troop_get_inventory_slot_modifier, ":imod", ":customer", ":i_slot"),
      (eq, ":imod", imod_rotten),
      (store_free_inventory_capacity, ":free_inv_cap", ":merchant_troop"),
      (gt, ":free_inv_cap", 0),

      (call_script, "script_dplmc_get_item_value_with_imod", ":item", ":imod"),
      (assign, ":score", reg0),
      (val_div, ":score", 100),
      (call_script, "script_game_get_item_sell_price_factor", ":item"),
      (assign, ":sell_price_factor", reg0),
      (val_mul, ":score", ":sell_price_factor"),
      (troop_inventory_slot_get_item_amount, ":amount", ":customer", ":i_slot"),
      (troop_inventory_slot_get_item_max_amount, ":max_amount", ":customer", ":i_slot"),
      (val_mul, ":score", ":amount"),
      (val_div, ":score", ":max_amount"),
      (val_div, ":score", 100),
      (val_max, ":score",1),
      (store_troop_gold, ":merchant_gold", ":merchant_troop"),
      (ge, ":merchant_gold", ":score"),

      #(troop_add_item, ":merchant_troop", ":item", ":imod"),
      (troop_set_inventory_slot, ":customer", ":i_slot", -1),
      (troop_remove_gold, ":merchant_troop", ":score"),
      (troop_add_gold, ":customer", ":score"),
    (try_end),
    (set_show_messages, 1),
    (store_troop_gold, ":end_gold", ":customer"),
    (store_free_inventory_capacity, ":end_space", ":customer"),
    (try_begin),
      (neq, ":end_gold", ":begin_gold"),
      (store_sub, reg1, ":end_gold", ":begin_gold"),
      (store_sub, reg2, ":end_space", ":begin_space"),
      (store_sub, reg3, reg1, 1),
      (store_sub, reg4, reg2, 1),
      (eq, ":customer_in_player_party", 1), #<- added
      (display_message, "@You sold {reg2} {reg4?kinds:kind} of rotten food and gained {reg1} {reg3?denars:denar}."),
    (try_end),
    ##added section begin, preserve registers
    (assign, reg1, ":save_reg1"),
    (assign, reg2, ":save_reg2"),
    (assign, reg3, ":save_reg3"),
    (assign, reg4, ":save_reg4"),
    ##added section end
  ]),
##Auto-Buy-Food from rubik's Custom Commander end
##INPUTS:
#  arg1  - speaker troop
#  arg2  - which word/phrase to retrieve (arbitrary code)
#  arg3  - string register
#OUTPUTS:
#  writes result to string register
   ("dplmc_print_cultural_word_to_sreg", [
     (store_script_param, ":speaker", 1),
     (store_script_param, ":context", 2),
     (store_script_param, ":string_register", 3),

     #Right now this is entirely faction-based, but you could give different
     #results for individual lords.
	 #(Note: Now certain parts of it do vary for heroes, to mimic the behavior in Native
	 #feast dialogs for the word for wine.)

     (assign, ":speaker_faction", -1),
     (try_begin),
		#Player faction
		(this_or_next|eq, ":speaker", "trp_player"),
			(eq, ":speaker", "trp_kingdom_heroes_including_player_begin"),
		(assign, ":speaker_faction", "fac_player_supporters_faction"),#<- This will potentially get translated later
	 (else_try),
		#Hero original faction
        (is_between, ":speaker", heroes_begin, heroes_end),
        (troop_get_slot, ":speaker_faction", ":speaker", slot_troop_original_faction),
	 (else_try),
		#Hero original faction
		(gt, ":speaker", -1),
		(troop_is_hero, ":speaker"),
		(troop_slot_ge, ":speaker", slot_troop_original_faction, npc_kingdoms_begin),
		(neg|troop_slot_ge, ":speaker", slot_troop_original_faction, npc_kingdoms_end),
		(troop_get_slot, ":speaker_faction", ":speaker", slot_troop_original_faction),
     (else_try),
		#Troop current faction
        (gt, ":speaker", -1),
        (store_troop_faction, ":speaker_faction", ":speaker"),
     (try_end),

	 (try_begin),
      (lt, ":speaker", 1),
     (else_try),
	   ##Only continue if the current faction isn't associated with a distinctive culture
	   (lt, ":speaker_faction", dplmc_non_generic_factions_begin),
	   ##This will work unless the order of the first factions gets changed
	 (else_try),
	   #Translate raiders into the equivalent kingdoms
	   (is_between, ":speaker", bandits_begin, bandits_end),
         (try_begin),
			(eq, ":speaker", "trp_mountain_bandit"),#Mountain bandits
			(assign, ":speaker_faction", "fac_kingdom_5"),#Rhodoks
		 (else_try),
			(eq, ":speaker", "trp_forest_bandit"),#Forest bandits
			(assign, ":speaker_faction", "fac_kingdom_1"),#Swadian
		 (else_try),
			(eq, ":speaker", "trp_sea_raider"),#Sea raiders
			(assign, ":speaker_faction", "fac_kingdom_4"),#Nords
		 (else_try),
			(eq, ":speaker", "trp_steppe_bandit"),#Steppe bandits
			(assign, ":speaker_faction", "fac_kingdom_3"),#Khergits
		 (else_try),
			(eq, ":speaker", "trp_taiga_bandit"),#Taiga bandits
			(assign, ":speaker_faction", "fac_kingdom_2"),#Vaegir
		 (else_try),
			(eq, ":speaker", "trp_desert_bandit"),#Desert bandits
			(assign, ":speaker_faction", "fac_kingdom_6"),#Sarranid
		 (try_end),
		 (ge, ":speaker_faction", dplmc_non_generic_factions_begin),
    (else_try),
		#For companions without default initial cultures, infer one from their home.
		#(Actually, don't limit this to companions, since there's a chance that others
		#could have a valid home slot.)
		#(is_between, ":speaker", companions_begin, companions_end),
		#(is_between, ":speaker", heroes_begin, heroes_end),
		(troop_is_hero, ":speaker"),
		(troop_get_slot, ":home_center", ":speaker", slot_troop_home),
		(is_between, ":home_center", centers_begin, centers_end),
		(party_get_slot, ":speaker_faction", ":home_center", slot_center_original_faction),
	 (else_try),
		#For villagers, merchants, etc.
		(eq, ":speaker", "$g_talk_troop"),
		(neg|is_between, ":speaker", heroes_begin, heroes_end),#Not a character that might have an explicitly-set faction
		(neg|is_between, ":speaker", training_ground_trainers_begin, tavern_minstrels_end),#Not a trainer, ransom broker, traveler, bookseller, or minstrel
		(ge, "$g_encountered_party", 0),
		(try_begin),
			#For towns / castles / villages, use the original faction
			(is_between, "$g_encountered_party", centers_begin, centers_end),
			(party_get_slot, ":speaker_faction", "$g_encountered_party", slot_center_original_faction),
		(else_try),
			#Use faction of encountered party
			(party_is_active, "$g_encountered_party"),
			(store_faction_of_party, ":speaker_faction", "$g_encountered_party"),
			#For generic factions, use the closest center
			(lt, ":speaker_faction", dplmc_non_generic_factions_begin),
			(assign, ":speaker_faction", reg0),#save register
			(call_script, "script_get_closest_center", "$g_encountered_party"),
			(assign, ":home_center", reg0),
			(assign, reg0, ":speaker_faction"),#revert register
			(party_get_slot, ":speaker_faction", ":home_center", slot_center_original_faction),
		(try_end),
	 (try_end),

    #Translate for player's kingdom
	 (try_begin),
		(ge, "$players_kingdom", dplmc_non_generic_factions_begin),
		(this_or_next|eq, ":speaker_faction", "fac_player_faction"),
		(this_or_next|eq, ":speaker_faction", "fac_player_supporters_faction"),
		(eq, ":speaker_faction", "$players_kingdom"),
		(assign, ":speaker_faction", "$players_kingdom"),
		(neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(this_or_next|is_between, "$g_player_culture", cultures_begin, cultures_end),
		(is_between,"$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
		(assign, ":speaker_faction", "$g_player_culture"),
	 (try_end),

     #Store variant
     (try_begin),
        #Iconic cultural weapon that can be used metonymously for force of arms.
		#Native equivalent is "sword".
		#Non-Warband example: "He who lives by the {sword}, dies by the {sword}."
		#Example usage: "My {sword} is at the disposal of my liege."
		(eq, ":context", DPLMC_CULTURAL_TERM_WEAPON),
        (try_begin),
           (this_or_next|eq, ":speaker_faction", "fac_kingdom_4"),#Nords
           (eq, ":speaker_faction", "fac_kingdom_2"),#Vaegirs
           (str_store_string, ":string_register", "@axe"),
        (else_try),
           (eq, ":speaker_faction", "fac_kingdom_5"),#Rhodoks
           (str_store_string, ":string_register", "@spear"),
        (else_try),
           (eq, ":speaker_faction", "fac_kingdom_3"),#Khergits
           (str_store_string, ":string_register", "@bow"),
        (else_try),
			#Default: Swadia, Sarranid, others
           (str_store_string, ":string_register", "@sword"),
        (try_end),
    (else_try),
        #Plural version of iconic cultural weapon that can be used metonymously for force of arms.
		#Native equivalent is "swords".
		(eq, ":context", DPLMC_CULTURAL_TERM_WEAPON_PLURAL),
        (try_begin),
           (this_or_next|eq, ":speaker_faction", "fac_kingdom_4"),#Nords
           (eq, ":speaker_faction", "fac_kingdom_2"),#Vaegirs
           (str_store_string, ":string_register", "@axes"),
        (else_try),
           (eq, ":speaker_faction", "fac_kingdom_5"),#Rhodoks
           (str_store_string, ":string_register", "@spears"),
        (else_try),
           (eq, ":speaker_faction", "fac_kingdom_3"),#Khergits
           (str_store_string, ":string_register", "@bows"),
        (else_try),
			#Default: Swadia, Sarranid, others
           (str_store_string, ":string_register", "@swords"),
        (try_end),
	 (else_try),
		#Cultural phrase that means "fight" (first person singular)
		#Native equivalent is "swing my sword."
		#Example usage: "I want to be able to {swing my sword} with a good conscience."
        (eq, ":context", DPLMC_CULTURAL_TERM_USE_MY_WEAPON),
        (try_begin),
           (eq, ":speaker_faction", "fac_kingdom_4"),#Nords
           (eq, ":speaker_faction", "fac_kingdom_2"),#Vaegirs
           (str_store_string, ":string_register", "@swing my axe"),
        (else_try),
           (eq, ":speaker_faction", "fac_kingdom_5"),#Rhodoks
           (str_store_string, ":string_register", "@lift my spear"),
        (else_try),
           (eq, ":speaker_faction", "fac_kingdom_3"),#Khergits
           (str_store_string, ":string_register", "@loose my arrows"),
        (else_try),
			#Default: Swadia, Sarranid, others
           (str_store_string, ":string_register", "@swing my sword"),
        (try_end),
	(else_try),
		#equivalent to lowercase "king" or "queen"
		(this_or_next|eq, ":context", DPLMC_CULTURAL_TERM_KING_FEMALE),
		(eq, ":context", DPLMC_CULTURAL_TERM_KING),
		(try_begin),
		   (eq, ":speaker_faction", "fac_kingdom_3"),#Khergit
		   (str_store_string, ":string_register", "str_khan"),
		(else_try),
		   (eq, ":speaker_faction", "fac_kingdom_6"),#Sarranid
		   (str_store_string, ":string_register", "@sultan"),
		(else_try),
		   #Default: Swadia, Rhodok, Nord, Vaegir, others
		   (str_store_string, ":string_register", "str_king"),
		   (eq, ":context", DPLMC_CULTURAL_TERM_KING_FEMALE),
		   (str_store_string, ":string_register", "str_queen"),
		(try_end),
	(else_try),
		#equivalent to lowercase "kings"
		(eq, ":context", DPLMC_CULTURAL_TERM_KING_PLURAL),
		(try_begin),
		   (eq, ":speaker_faction", "fac_kingdom_3"),#Khergit
		   (str_store_string, ":string_register", "@khans"),
		(else_try),
		   (eq, ":speaker_faction", "fac_kingdom_6"),#Sarranid
		   (str_store_string, ":string_register", "@sultans"),
		(else_try),
 		   #Default: Swadia, Rhodok, Nord, Vaegir, others
		   (str_store_string, ":string_register", "@kings"),
		(try_end),
	(else_try),
		#equivalent to lowercase "lord"
		(eq, ":context", DPLMC_CULTURAL_TERM_LORD),
		(str_store_string, ":string_register", "@lord"),
	(else_try),
		#equivalent to lowercase "lords"
		(eq, ":context", DPLMC_CULTURAL_TERM_LORD_PLURAL),
		(str_store_string, ":string_register", "@lords"),
	(else_try),
		#As in, "I shall tell my {swineherd} about your sweet promises" or "Any {swineherd} can claim to be king".
		(eq, ":context", DPLMC_CULTURAL_TERM_SWINEHERD),
		(assign, ":mode", ":speaker"),
		(try_begin),
		   (gt, ":speaker", 0),
		   (neg|troop_is_hero, ":speaker"),
		   (store_current_hours, ":mode"),
		   (val_add, ":mode", "$g_encountered_party"),
		(try_end),
		(val_max, ":mode", 0),#Default to mode 0 for negative speakers
		(val_mod, ":mode", 2),
		(try_begin),
           (eq, ":speaker_faction", "fac_kingdom_2"),#Vaegirs
		   (try_begin),
		      (eq, ":mode", 0),
              (str_store_string, ":string_register", "@goatherd"),
		   (else_try),
		       (str_store_string, ":string_register", "@swineherd"),
		   (try_end),
        (else_try),
		   (eq, ":speaker_faction", "fac_kingdom_3"),#Khergits
		   (try_begin),
		      (eq, ":mode", 0),
              (str_store_string, ":string_register", "@stable {boy/girl}"),
        (else_try),
		      (str_store_string, ":string_register", "@shepherd {boy/girl}"),
		   (try_end),
		(else_try),
		   (eq, ":speaker_faction", "fac_kingdom_6"),#Sarranids
		   (try_begin),
		      (eq, ":mode", 0),
		      (str_store_string, ":string_register", "@goatherd"),
		   (else_try),
		      (str_store_string, ":string_register", "@shepherd {boy/girl}"),
		   (try_end),
        (else_try),
           #Swadia, Rhodok, Nord, others
           (str_store_string, ":string_register", "@swineherd"),
        (try_end),
	(else_try),
		#As in, "I'd like to buy every man who comes in here tonight a jar of your best wine."
		(this_or_next|eq, ":context", DPLMC_CULTURAL_TERM_TAVERNWINE),
		#Follow the pattern used in Native for lords in feasts
		#(c.f. "str_flagon_of_mead", "str_skin_of_kumis", "str_mug_of_kvass", "str_cup_of_wine")

		(try_begin),
			#For lords, use "mode" so it works the same as in feast dialogs
			(is_between, ":speaker", heroes_begin, heroes_end),
			(this_or_next|neg|is_between, ":speaker", companions_begin, companions_end),
				(neg|troop_slot_eq, ":speaker", slot_troop_original_faction, ":speaker_faction"),
			(store_mod, ":mode", ":speaker", 2),
		(else_try),
			#Otherwise set mode to 0, to always use the cultural alternative
			(assign, ":mode", 0),
		(try_end),

		(try_begin),
			(eq, ":speaker_faction", "fac_kingdom_2"),
			(eq, ":mode", 0),#From feast: 50% chance of falling through to "wine"
			(str_store_string, ":string_register", "@kvass"),#Vaegirs: kvass
		(else_try),
			(eq, ":speaker_faction", "fac_kingdom_3"),
			(eq, ":mode", 0),#From feast: 50% chance of falling through to "wine"
			(str_store_string, ":string_register", "@kumis"),#Khergits: kumis
		(else_try),
			(eq, ":speaker_faction", "fac_kingdom_4"),
			(str_store_string, ":string_register", "@mead"),#Nords: mead
		(else_try),
			(str_store_string, ":string_register", "@wine"),#Default: wine
		(try_end),
    (else_try),
	#Error string
        (assign, ":save_reg0", reg0),
		(assign, reg0, ":context"),
		(display_message, "@{!}ERROR - dplmc_print_cultural_word_to_sreg called for bad context {reg0}"),
		(str_store_string, ":string_register", "str_ERROR_string"),
		(assign, reg0, ":save_reg0"),
    (try_end),

   ]),


  #script_dplmc_print_player_spouse_says_my_husband_wife_to_s0
  ##
  ##Only needs to be called once, but it's safe to call multiple times
  ##(it uses "$g_autoloot" to store the version)
  ##
  ##Inputs: arg1: 1 to force this to run
  ##Outputs: None
  ("dplmc_initialize_autoloot",
  [
	(store_script_param_1, ":force_to_run"),

	(try_begin),
		#Check if there is anything to do
		(this_or_next|eq, ":force_to_run", 1),
			(neq, "$g_autoloot", 2),
      (try_begin),
		   #Print a message to make it obvious when this is happening more than it should.
		   (ge, "$cheat_mode", 1),
		   (store_current_hours, ":hours"),
		   (gt, ":hours", 0),
		   (display_message, "@{!}Initializing auto-loot.  This message should not appear more than once."),
      (try_end),
		#Initialize
		(try_for_range, ":cur_food", "itm_raw_date_fruit", food_end),
			(neq, ":cur_food", "itm_furs"),
			(item_set_slot, ":cur_food", dplmc_slot_item_food_portion, 1),
		(try_end),

		# #deprecated due to 1.165 operations
		# (call_script, "script_dplmc_init_item_difficulties"),
		# (call_script, "script_dplmc_init_item_base_score"),

		(assign, "$g_dplmc_auto_sell_price_limit", 50),
		(assign, "$g_dplmc_sell_items_when_leaving", 0),
		(assign, "$g_dplmc_buy_food_when_leaving", 0),

		(item_set_slot, itp_type_book, dplmc_slot_item_type_not_for_sell, 1),
		(item_set_slot, itp_type_goods, dplmc_slot_item_type_not_for_sell, 1),
		(item_set_slot, itp_type_animal, dplmc_slot_item_type_not_for_sell, 1),

		(assign, "$g_autoloot", 2),
	(try_end),
  ]),


##"script_dplmc_get_troop_standing_in_faction"
 ("dplmc_store_troop_is_eligible_for_affiliate_messages",
 [
	(store_script_param_1, ":troop_no"),
	(assign, ":is_eligible", 0),
	(assign, ":save_reg1", reg1),
	(try_begin),
		(lt, ":troop_no", 1),
	(else_try),
		(neg|troop_is_hero, ":troop_no"),
	(else_try),
		#Initialize :faction_no and :faction_relation
		(store_faction_of_troop, ":faction_no", ":troop_no"),
		(store_relation, ":faction_relation", ":faction_no", "fac_player_supporters_faction"),
		(try_begin),
			(eq, ":faction_no", "$players_kingdom"),
			(val_max, ":faction_relation", 1),
		(try_end),
		#Companion
		(gt, ":faction_relation", -1),
		(is_between, ":troop_no", companions_begin, companions_end),
		(neg|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
		(troop_slot_ge, ":troop_no", slot_troop_player_relation, 20),
		(assign, ":is_eligible", 1),
	(else_try),
		#Faction marshall (if the player is the faction leader)
		#Faction leader (if the player is the faction marshall)
		(eq, ":faction_no", "$players_kingdom"),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_MARSHALL),
		(call_script, "script_dplmc_get_troop_standing_in_faction", ":troop_no", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_MARSHALL),
		(assign, ":is_eligible", 1),
	(else_try),
		#Spouse / relatives / in-laws
		(gt, ":faction_relation", -1),
		#(is_between, ":troop_no", heroes_begin, heroes_end),## should be safe even for non-heroes
		(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":troop_no", "trp_player"),
		(ge, reg0, 2),
		(troop_get_slot, reg1, ":troop_no", slot_troop_player_relation),
		(val_add, reg0, reg1),
		(ge, reg0, 20),
		(assign, ":is_eligible", 1),
	(else_try),
		#Affiliates
		(call_script, "script_dplmc_is_affiliated_family_member", ":troop_no"),
		(ge, reg0, 1),
		(assign, ":is_eligible", 1),
	(else_try),
		#Cheat mode: add faction leaders to test this out
		(gt, "$cheat_mode", 0),
		(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
		(faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),
		(assign, ":is_eligible", 1),
	(try_end),
	(assign, reg1, ":save_reg1"),
	(assign, reg0, ":is_eligible"),
 ]),

# "script_dplmc_sell_all_prisoners"
#
# Taken from rubik's Custom Commander, and altered to have parameters
# and return feedback.
#
#INPUT:
#Arg 1: actually remove (positive for yes, zero or negative for no)
#Arg 2: if positive, use this as a fixed price instead of calculating dynamically
#OUTPUT:
#reg0: amount of gold gained (or would have been gained if the sale occurred)
#reg1: number of prisoners sold (or would have been sold if the sale occurred)
  ("dplmc_sell_all_prisoners",
   [
    (store_script_param_1, ":actually_remove"),
    (store_script_param_2, ":fixed_price"),
    (call_script, "script_dplmc_sell_all_prisoners_from_party", "p_main_party", ":actually_remove", ":fixed_price"),
  ]),

# "script_dplmc_sell_all_prisoners_from_party"
#
#INPUT:
#Arg 1: party to sell regular prisoners from
#Arg 2: actually remove (positive for yes, zero or negative for no)
#Arg 3: if positive, use this as a fixed price instead of calculating dynamically
#OUTPUT:
#reg0: amount of gold gained (or would have been gained if the sale occurred)
#reg1: number of prisoners sold (or would have been sold if the sale occurred)
  ("dplmc_sell_all_prisoners_from_party",
   [
    (store_script_param_1, ":source_party"),
    (store_script_param_2, ":actually_remove"),
    (store_script_param, ":fixed_price", 3),

    (assign, ":total_removed", 0),
    (assign, ":total_income", 0),
    (party_get_num_prisoner_stacks, ":num_stacks", ":source_party"),
    (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
      (party_prisoner_stack_get_troop_id, ":troop_no", ":source_party", ":i_stack"),
      #SB : correction to use game script
      (call_script, "script_game_check_prisoner_can_be_sold", ":troop_no"),
      (eq, reg0, 1),
      # (neg|troop_is_hero, ":troop_no"),
      (party_prisoner_stack_get_size, ":stack_size", ":source_party", ":i_stack"),
      (try_begin),
         (gt, ":fixed_price", 0),
         (assign, ":sell_price", ":fixed_price"),
      (else_try),
         (call_script, "script_game_get_prisoner_price", ":troop_no"),
         (assign, ":sell_price", reg0),
      (try_end),
      (store_mul, ":stack_total_price", ":sell_price", ":stack_size"),
      (val_add, ":total_income", ":stack_total_price"),
      (val_add, ":total_removed", ":stack_size"),
      (gt, ":actually_remove", 0),#Stop short if this is a dry run
      (party_remove_prisoners, ":source_party", ":troop_no", ":stack_size"),
    (try_end),
    (try_begin),
      (gt, ":actually_remove", 0),#Stop short if this is a dry run
      (troop_add_gold, "trp_player", ":total_income"),
    (try_end),
    (assign, reg0, ":total_income"),
    (assign, reg1, ":total_removed"),
  ]),

# "script_dplmc_recruit_all_prisoners_to_garrison"
#
#INPUT:
#Arg 1: center party
#Arg 2: actually recruit (positive for yes, zero or negative for no)
#OUTPUT:
#reg0: number of prisoners recruited (or would have been recruited if dry run)
  ("dplmc_recruit_all_prisoners_to_garrison",
   [
    (store_script_param_1, ":center_party"),
    (store_script_param_2, ":actually_recruit"),

    (assign, ":total_recruited", 0),
    (party_get_num_prisoner_stacks, ":num_stacks", ":center_party"),
    (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
      (party_prisoner_stack_get_troop_id, ":troop_no", ":center_party", ":i_stack"),
      (call_script, "script_game_check_prisoner_can_be_sold", ":troop_no"),
      (eq, reg0, 1),
      (party_prisoner_stack_get_size, ":stack_size", ":center_party", ":i_stack"),
      (val_add, ":total_recruited", ":stack_size"),
      (gt, ":actually_recruit", 0),
      (party_remove_prisoners, ":center_party", ":troop_no", ":stack_size"),
      (party_add_members, ":center_party", ":troop_no", ":stack_size"),
    (try_end),
    (assign, reg0, ":total_recruited"),
  ]),

#"script_dplmc_translate_inactive_player_supporter_faction_2"
##
#
#INPUT:
#   None
#OUTPUT:
#   reg0   -1 means there are no companions and skill is too low
#           0 means there are companions and skill is too low
#           1 means skill is high enough but there are no companions
#           2 means skill is high enough and there are companions
#
# Will fail if it does not set reg0 to 2.
##
("cf_dplmc_player_party_meets_autoloot_conditions",
[
	  (store_skill_level, ":best_loot_skill", "skl_looting", "trp_player"),
	  (store_skill_level, ":player_inv_skill", "skl_inventory_management", "trp_player"),
	  (assign, ":best_inv_skill", ":player_inv_skill"),
	  (assign, ":num_companions", 0),
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
         (party_stack_get_troop_id,   ":stack_troop", "p_main_party", ":stack_no"),
		 (ge, ":stack_troop", 0),
		 #Check skill
		 (is_between, ":stack_troop", heroes_begin, heroes_end),
		 (store_skill_level, ":hero_skill", "skl_inventory_management", ":stack_troop"),
		 (val_max, ":best_inv_skill", ":hero_skill"),

		 (store_skill_level, ":hero_skill", "skl_looting", ":stack_troop"),
		 (val_max, ":best_loot_skill", ":hero_skill"),
		 #Check is companion
         (is_between, ":stack_troop", companions_begin, companions_end),
         (val_add, ":num_companions", 1),
      (try_end),

	  (try_begin),
	    (lt, ":player_inv_skill", 2),
		(lt, ":best_inv_skill", 3),
		(lt, ":best_loot_skill", 2),
		(assign, reg0, 0),
		(try_begin),
			(lt, ":num_companions", 1),#change 2011-06-07
			(assign, reg0, -1),
		(try_end),
	  (else_try),
		(assign, reg0, 1),
		(gt, ":num_companions", 0),
		(assign, reg0, 2),
	  (try_end),

	  (eq, reg0, 2),
]),


##"script_dplmc_troop_get_family_relation_to_troop"
("cf_dplmc_faction_has_bias_against_gender", [
	(store_script_param_1, ":faction_no"),
	(store_script_param_2, ":test_gender"),#Special: 1 is female

    (assign, reg0, 0),
	(lt, "$g_disable_condescending_comments", 2),#If bias is disabled, do not continue
	(is_between, ":test_gender", 0, 2),#valid genders are 0 and 1

	(try_begin),
		(eq, ":faction_no", "fac_player_supporters_faction"),
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(assign, ":faction_no", "$players_kingdom"),
	(try_end),

	(try_begin),
		#For a-typical factions, nothing by default.
		(neg|is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
	(else_try),
		#If the leader has that gender, no prejudice.
		(faction_get_slot, ":active_npc", ":faction_no", slot_faction_leader),
		(gt, ":active_npc", -1),
		(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
		(eq, reg0, ":test_gender"),
		(assign, reg0, 0),
	(else_try),
		#Traditional gender prejudice if both are true:
		#1.  The faction has no original members of the specified gender.
		#2.  The faction has original members with non-accepting lord personalities.

		(assign, ":num_closeminded", 0),
		(assign, ":end_cond", active_npcs_end),

		(try_for_range, ":active_npc", active_npcs_begin, ":end_cond"),#Deliberately do not include kingdom ladies
			#Also deliberately exclude companions and pretenders
			#(Pretenders are marginalized at the start of the game, and
			#companions don't necessarily start in positions of power either)
			(this_or_next|is_between, ":active_npc", kings_begin, kings_end),
				(is_between, ":active_npc", lords_begin, lords_end),
			(troop_slot_eq, ":active_npc", slot_troop_original_faction, ":faction_no"),

			(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
			(try_begin),
				(eq, reg0, ":test_gender"),
				(assign, ":num_closeminded", -1000),
				(assign, ":end_cond", ":active_npc"),
			(else_try),
				(troop_get_slot, reg0, ":active_npc", slot_lord_reputation_type),
				(is_between, reg0, lrep_none + 1, lrep_roguish),#Lord (non-commoner, non-liege, non-lady) personality type
				(neq, reg0, lrep_cunning),
				(neq, reg0, lrep_goodnatured),
				(val_add, ":num_closeminded", 1),
			(try_end),
		(try_end),

		(store_sub, reg0, ":num_closeminded", 1),#Needs at least one
		(val_clamp, reg0, 0, 2),
	(try_end),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(assign, ":end_cond", reg1),#just save reg1 and reg2 (ignore the normal meaning of the variable names)
		(assign, ":active_npc", reg2),
		(assign, reg1, ":faction_no"),
		(assign, reg2, ":test_gender"),
		(display_message, "@{!} Checked if faction {reg1} is prejudiced against {reg2?women:men}: {reg0?true:false}"),
		(assign, reg1, ":end_cond"),#revert reg1 and reg2 (ignore the normal meaning of the variable names)
		(assign, reg2, ":active_npc"),
	(try_end),
	(gt, reg0, 0),
]),

#"script_dplmc_store_troop_personality_caution_level"
#
# INPUT:
#   arg1 :troop_no
# OUTPUT:
#   reg0 -1 for aggressive
#         0 for neither
#         1 for cautious
("dplmc_store_troop_personality_caution_level", [
	#Used a number of places to determine whether a lord is cautious
	#or aggressive.  The standard is something like:
	#
	#For cautious:
	#(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
    #    (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
    #    (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
    #    (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
	#
	#For aggressive:
	#(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
    #    (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
    #    (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
	#
	#I've expanded this for companion/lady personalities.
	#The result can be either:
	# -1  =  aggressive
	#  0  =  neutral
	#  1  =  cautious
	(store_script_param_1, ":troop_no"),

	(try_begin),
		(neg|is_between, ":troop_no", heroes_begin, heroes_end),#The player or troops that don't have slot_lord_reputation_type
		(assign, reg0, 0),#neither cautious nor aggressive
	(else_try),
		(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_aristocratic),
		(lt, reg0, 0),#compliments when the player retreats
		(assign, reg0, 1),#cautious
	(else_try),
		(gt, reg0, 0),#complains when the player retreats
		(assign, reg0, -1),#aggressive
	(else_try),
		(troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
		(this_or_next|eq, ":reputation", lrep_adventurous),
		(this_or_next|eq, ":reputation", lrep_martial),
		(this_or_next|eq, ":reputation", lrep_quarrelsome),
			(eq, ":reputation", lrep_selfrighteous),
		(assign, reg0, -1),#aggressive
	(else_try),
		(this_or_next|ge, ":reputation", lrep_conventional),
		(this_or_next|eq, ":reputation", lrep_upstanding),
		(this_or_next|eq, ":reputation", lrep_debauched),
		(this_or_next|eq, ":reputation", lrep_goodnatured),
			(eq, ":reputation", lrep_cunning),
		(assign, reg0, 1),#cautious
	(else_try),
		(assign, reg0, 0),#neither cautious nor aggressive
	(try_end),
]),

##"script_dplmc_cap_troop_describes_troop_to_troop_s1"
#
# e.g.
#
#(call_script, "script_dplmc_cap_troop_describes_troop_to_troop_s1", 1, "trp_player", ":third_lord", "$g_talk_troop"),
#
#INPUT:
#        arg1  :capitalization (0 if middle of sentence, 1 if sentence start)
#        arg2  :speaker (the one doing the talking)
#        arg3  :described (the one being named)
#        arg4  :listener (the one being spoken to)
#
#OUTPUT:
#        Writes result to s1, clobbers s0
#
#Similar to "script_troop_describes_troop_to_s15", except
#it takes into account the perspective of the one being
#spoken to, and writes to s1
  ("dplmc_cap_troop_describes_troop_to_troop_s1",
  [
	(store_script_param, ":capitalization", 1),
	(store_script_param, ":speaker", 2),
	(store_script_param, ":described", 3),
	(store_script_param, ":listener", 4),

	(assign, ":save_reg0", reg0),
	(assign, ":save_reg1", reg1),

	(str_store_troop_name, s0, ":described"),

	(assign, reg0, ":capitalization"),
	(try_begin),
		(eq, ":described", ":listener"),
		(neq, ":speaker", ":listener"),
		(str_store_string, s0, "@{reg0?Y:y}ou"),
		(assign, reg0, 1),
	(else_try),
		(eq, ":described", ":speaker"),
		(str_store_string, s0, "@{reg0?M:m}yself"),
		(assign, reg0, 1),
	(else_try),
		(this_or_next|eq, ":described", "trp_player"),#only calculate family relationships for the player and heroes
			(is_between, ":described", heroes_begin, heroes_end),
		(assign, ":speaker_relation", 0),
		(assign, ":speaker_relation_string", 0),
		(try_begin),
			(this_or_next|eq, ":speaker", "trp_player"),#only calculate family relationships for the player and heroes
				(is_between, ":speaker", heroes_begin, heroes_end),
			(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":described", ":speaker"),
			(assign, ":speaker_relation", reg0),
			(assign, ":speaker_relation_string", reg1),
		(try_end),
		(assign, reg0, 0),
		(try_begin),
			(this_or_next|eq, ":described", "trp_player"),#only calculate family relationships for the player and heroes
				(is_between, ":described", heroes_begin, heroes_end),
			(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":described", ":listener"),
		(try_end),
		(this_or_next|ge, ":speaker_relation", 1),
			(ge, reg0, 1),
		(try_begin),
			(eq, ":speaker_relation", reg0),
			(eq, reg1, ":speaker_relation_string"),
			(neq, ":speaker", ":listener"),
			(assign, reg0, ":capitalization"),
			(str_store_string, s1, ":speaker_relation_string"),
			(str_store_string, s1, "@{reg0?O:o}ur {s1} {s0}"),
		(else_try),
			(ge, ":speaker_relation", reg0),
			(assign, reg0, ":capitalization"),
			(str_store_string, s1, ":speaker_relation_string"),
			(str_store_string, s1, "@{reg0?M:m}y {s1} {s0}"),
		(else_try),
			(assign, reg0, ":capitalization"),
			(str_store_string, s1, reg1),
			(str_store_string, s1, "@{reg0?Y:y}our {s1} {s0}"),
		(try_end),
	###Disable "marshall/liege", because that's done elsewhere anyway
	#(else_try),
	#	(store_faction_of_troop, ":speaker_faction", ":speaker"),
	#	(try_begin),
	#		(eq, ":speaker", "trp_player"),
	#		(assign, ":speaker_faction", "$players_kingdom"),
	#	(try_end),
	#
	#	(store_faction_of_troop, ":listener_faction", ":listener"),
	#	(try_begin),
	#		(eq, ":listener", "trp_player"),
	#		(assign, ":listener_faction", "$players_kingdom"),
	#	(try_end),
	#
	#	(faction_slot_eq, ":speaker_faction", slot_faction_leader, ":described"),
	#	(this_or_next|is_between, ":speaker_faction", npc_kingdoms_begin, npc_kingdoms_end),
	#		(faction_slot_eq, ":speaker_faction", slot_faction_state, sfs_active),
	#	(this_or_next|neq, ":described", "trp_player"),
	#		(eq, ":speaker_faction", "$players_kingdom"),
	#	(assign, reg0, ":capitalization"),
	#	(try_begin),
	#		(eq, ":speaker_faction", ":listener_faction"),
	#		(neq, ":speaker", ":listener"),
	#		(str_store_string, s1, "@{reg0?O:o}ur liege {s0}"),
	#	(else_try),
	#		(str_store_string, s1, "@{reg0?M:m}y liege {s0}"),
	#	(try_end),
	#(else_try),
	#	(faction_slot_eq, ":speaker_faction", slot_faction_marshall, ":described"),
	#	(this_or_next|is_between, ":speaker_faction", npc_kingdoms_begin, npc_kingdoms_end),
	#		(faction_slot_eq, ":speaker_faction", slot_faction_state, sfs_active),
	#	(this_or_next|neq, ":described", "trp_player"),
	#		(eq, ":speaker_faction", "$players_kingdom"),
	#	(try_begin),
	#		(eq, ":speaker_faction", ":listener_faction"),
	#		(neq, ":speaker", ":listener"),
	#		(str_store_string, s1, "@{reg0?O:o}ur marshall {s0}"),
	#	(else_try),
	#		(str_store_string, s1, "@{reg0?M:m}y marshall {s0}"),
	#	(try_end),
	#(else_try),
	#	(this_or_next|is_between, ":listener_faction", npc_kingdoms_begin, npc_kingdoms_end),
	#		(faction_slot_eq, ":listener_faction", slot_faction_state, sfs_active),
	#	(faction_slot_eq, ":listener_faction", slot_faction_leader, ":described"),
	#	(this_or_next|neq, ":described", "trp_player"),
	#		(eq, ":listener_faction", "$players_kingdom"),
	#	(assign, reg0, ":capitalization"),
	#	(str_store_string, s1, "@{reg0?Y:y}our liege {s0}"),

	###Disable "friend", because it gets really spammy.  (It looks really stupid to have
	###a list of fifty names, all of them starting with "Your Friend So-and-So".)
	#(else_try),
	#	(call_script, "script_troop_get_relation_with_troop", ":described", ":listener"),
	#	(ge, reg0, 20),
	#	(this_or_next|neq, ":listener", "trp_player"),
	#		(ge, reg0, 50),
	#	(call_script, "script_troop_get_relation_with_troop", ":described", ":speaker"),
	#	(this_or_next|neq, ":listener", "trp_player"),
	#		(neq, ":speaker_trp_player"),
	#	(try_begin),
	#		(ge, reg0, 20),
	#		(this_or_next|neq, ":speaker", "trp_player"),
	#			(ge, reg0, 50),
	#		(assign, reg0, ":capitalization"),
	#		(str_store_string, s1, "@{reg0?O:o}ur friend {s0}"),
	#	(else_try),
	#		(assign, reg0, ":capitalization"),
	#		(str_store_string, s1, "@{reg0?Y:y}our friend {s0}"),
	#	(try_end),
	#(else_try),
	#	(call_script, "script_troop_get_relation_with_troop", ":described", ":speaker"),
	#	(ge, reg0, 20),
	#	(this_or_next|neq, ":speaker", "trp_player"),
	#		(ge, reg0, 50),
	#	(assign, reg0, ":capitalization"),
	#	(str_store_string, s1, "@{reg0?M:m}y friend {s0}"),

	###The "<Jarl Aedin> of <Tihr>" condition works fine, but I'm not particularly impressed.
	###I'm not sure it's an improvement over just using their name, so I'm disabling it for now.
	#(else_try),
	#	#Did not use relation string: name by owned town.
	#	#Do not use names of castles, due to potential absurdities like "Count Harringoth of Harringoth Castle".
	#	#Skip kings and pretenders because of "Lady Isolla of Suno of Suno" and similar things.
	#	(neg|is_between, ":described", kings_begin, kings_end),
	#	(neg|is_between, ":described", pretenders_begin, pretenders_end),
	#	(this_or_next|eq, ":described", "trp_player"),
	#		(is_between, ":described", heroes_begin, heroes_end),
	#
	#	(assign, ":owned_town", -1),
	#	(assign, ":owned_town_score", -1),
	#	(troop_get_slot, ":original_faction", ":described", slot_troop_original_faction),
	#	(try_for_range, ":town_no", towns_begin, towns_end),
	#		(party_get_slot, ":town_lord", ":town_no", slot_town_lord),
	#		(ge, ":town_lord", 0),
	#		(assign, reg0, 0),
	#		(try_begin),
	#			(eq, ":town_lord", ":described"),
	#			(assign, reg0, 10),
	#		(else_try),
	#			(this_or_next|troop_slot_eq, ":town_lord", slot_troop_spouse, ":described"),
	#				(troop_slot_eq, ":described", slot_troop_spouse, ":town_lord"),
	#			(this_or_next|is_between, ":described", kingdom_ladies_begin, kingdom_ladies_end),
	#				(troop_slot_eq, ":described", slot_troop_occupation, slto_kingdom_lady),
	#			(assign, reg0, 1),
	#		(else_try),
	#			(assign, reg0, 0),
	#		(try_end),
	#		(gt, reg0, 0),
	#		(try_begin),
	#			(party_slot_eq, ":town_no", slot_center_original_faction, ":original_faction"),
	#			(val_add, reg0, 1),
	#		(try_end),
	#		(try_begin),
	#			(this_or_next|party_slot_eq, ":town_no", dplmc_slot_center_original_lord, ":described"),
	#				(party_slot_eq, ":town_no", dplmc_slot_center_original_lord, ":town_lord"),
	#			(val_add, reg0, 2),
	#		(try_end),
	#		(try_begin),
	#			(this_or_next|troop_slot_eq, ":town_lord", slot_troop_home, ":town_no"),
	#				(troop_slot_eq, ":town_lord", slot_troop_home, ":town_no"),
	#			(val_add, reg0, 2),
	#		(try_end),
	#		(gt, reg0, ":owned_town_score"),
	#		(assign, ":owned_town_score", reg0),
	#		(assign, ":owned_town", ":town_no"),
	#	(try_end),
	#	(is_between, ":owned_town", towns_begin, towns_end),
	#	(str_store_party_name, s1, ":owned_town"),
	#	(str_store_string, s1, "@{s0} of {s1}"),
	(else_try),
		(str_store_string, s1, "str_s0"),
	(try_end),

	(assign, reg0, ":save_reg0"),
	(assign, reg1, ":save_reg1"),
	(str_store_string_reg, s0, s1),
	]),

##"script_dplmc_helper_get_troop1_troop2_family_slot_aux"
	#
	#  INPUT:  arg1   :center_no
	# OUTPUT:  reg0   estimated value of weekly income
	#
	#TODO: Add a better explanation for why this function does not include tarrifs.
	("dplmc_estimate_center_weekly_income", [
		(store_script_param_1, ":center_no"),
		(party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
		(try_begin),
		  #If there is some sort of aberration, assign to 50 instead of
		  #clamping, on the assumption that the value bears no relation
		  #to the true prosperity at all.
		  (neg|is_between, ":prosperity", 0, 101),
		  (assign, ":prosperity", 50),
		(try_end),
		(store_add, reg0, 20, ":prosperity"),
		(val_mul, reg0, 1200),
		(val_div, reg0, 120),
		(try_begin),
		  (party_slot_eq, ":center_no", slot_party_type, spt_town),
		  #Towns have higher base rent than castles and villages
		  (val_mul, reg0, 2),
		  #Include town garrison allowance
		  (val_mul, ":prosperity", 15),
		  (val_add, ":prosperity", 700),
		  (val_mul, ":prosperity", 3),
		  (val_div, ":prosperity", 2),
		  (val_add, reg0, ":prosperity"),
		(else_try),
		  (party_slot_eq, ":center_no", slot_party_type, spt_castle),
		  #Include castle garrison allowance
		  (val_mul, ":prosperity", 15),
		  (val_add, ":prosperity", 700),
		  (val_add, reg0, ":prosperity"),
		(try_end),
		#At this point, the final result is in reg0.
	]),

  # "script_dplmc_get_closest_center_or_two"

#"script_dplmc_save_civilian_clothing"
##Save civilian clothing so it will still appear later
#
#INPUT: troop number
#OUTPUT: none
   ("dplmc_save_civilian_clothing", [
     (store_script_param, ":troop_no", 1),
     #SB : this interferes with auto-loot
     (try_begin),
        (gt, ":troop_no", 0),#deliberately exclude player
        (troop_is_hero, ":troop_no"),#only applies to unique characters
        (try_for_range, ":dest_slot", dplmc_ek_alt_items_begin, min(dplmc_ek_alt_items_end, dplmc_ek_alt_items_begin + 4)),
           (store_add, ":source_slot", ":dest_slot", ek_head - dplmc_ek_alt_items_begin),
           (troop_get_inventory_slot, ":item_id", ":troop_no", ":dest_slot"),
           (lt, ":item_id", 1),#do not overwrite an existing item in the destination slot
           (troop_get_inventory_slot, ":item_id", ":troop_no", ":source_slot"),
           (troop_set_inventory_slot, ":troop_no", ":dest_slot", ":item_id"),
        (try_end),
     (try_end),
   ]),
##diplomacy end+
  #new camera setup scripts, setting up other calls

  ("cf_dplmc_battle_continuation", [
    (eq, "$g_dplmc_battle_continuation", 0),
    (assign, ":num_allies", 0),
    (try_for_agents, ":agent"),
      (agent_is_ally, ":agent"),
      (agent_is_alive, ":agent"),
      (val_add, ":num_allies", 1),
    (try_end),
    (gt, ":num_allies", 0),
    (try_begin),
      (eq, "$g_dplmc_cam_activated", 0),
      #(store_mission_timer_a, "$g_dplmc_main_hero_fallen_seconds"),
      (assign, "$g_dplmc_cam_activated", "$g_dplmc_cam_default"),

      (display_message, "@You have been knocked out by the enemy. Watch your men continue the fight without you or press Tab to retreat."),
      (store_add, ":string", "$g_dplmc_cam_activated", "str_camera_keyboard"),
      (val_sub, ":string", 1),
      (display_message, ":string"),
      # (display_message, "@To watch the fight you can use 'w, a, s, d, numpad_+/numpad_-' to move and 'numpad_1,2,3,4,6,8' to rotate the cam."),

      (try_begin), #http://forums.taleworlds.com/index.php/topic,322343.0.html
        (eq, "$g_dplmc_charge_when_dead", 1),
        (get_player_agent_no, ":player_agent"),
        (agent_get_team, ":player_team", ":player_agent"),
        (set_show_messages, 0),
        (team_give_order, ":player_team", grc_everyone, mordr_charge),
        (team_give_order, ":player_team", grc_everyone, mordr_use_any_weapon),
        (team_give_order, ":player_team", grc_everyone, mordr_fire_at_will),
        (set_show_messages, 1),
      (try_end),

      (mission_cam_get_position, pos1), #Death pos
      (position_get_rotation_around_z, ":rot_z", pos1),

      (init_position, pos47),
      (position_copy_origin, pos47, pos1), #Copy X,Y,Z pos
      (position_rotate_z, pos47, ":rot_z"), #Copying X-Rotation is likely possible, but I haven't figured it out yet

      (mission_cam_set_mode, 1, 0, 0), #Manual?

      (try_begin), #auto-assign the closest agent
        (eq, "$g_dplmc_cam_activated", camera_follow),
        (call_script, "script_dmod_closest_agent"),
      (try_end),

      (mission_cam_set_position, pos47),
    (try_end),
    ]),

      # INPUT:

(
	"diplomacy_faction_get_diplomatic_status_with_faction",
	#result: -1 faction_1 has a casus belli against faction_2. 1, faction_1 has a truce with faction_2, -2, the two factions are at war
	[
	(store_script_param, ":actor_faction", 1),
	(store_script_param, ":target_faction", 2),
	##diplomacy start+
	#Since "fac_player_supporters_faction" is used as a shorthand for the faction
	#run by the player, intercept that here instead of the various places this is
	#called from.
	(call_script, "script_dplmc_translate_inactive_player_supporter_faction_2", ":actor_faction", ":target_faction"),
	(assign, ":actor_faction", reg0),
	(assign, ":target_faction", reg1),
	##diplomacy end+

	(store_add, ":truce_slot", ":target_faction", slot_faction_truce_days_with_factions_begin),
	(store_add, ":provocation_slot", ":target_faction", slot_faction_provocation_days_with_factions_begin),
	(val_sub, ":truce_slot", kingdoms_begin),
	(val_sub, ":provocation_slot", kingdoms_begin),

	(assign, ":result", 0),
	(assign, ":duration", 0),

	(try_begin),
		(store_relation, ":relation", ":actor_faction", ":target_faction"),
		(lt, ":relation", 0),
		(assign, ":result", -2),
	(else_try),
		(faction_slot_ge, ":actor_faction", ":truce_slot", 1),
		(assign, ":result", 1),

		(faction_get_slot, ":duration", ":actor_faction", ":truce_slot"),
	(else_try),
		(faction_slot_ge, ":actor_faction", ":provocation_slot", 1),
		(assign, ":result", -1),

		(faction_get_slot, ":duration", ":actor_faction", ":provocation_slot"),
	(try_end),

	(assign, reg0, ":result"),
	(assign, reg1, ":duration"),
	]),

("make_kingdom_hostile_to_player",
    [
      (store_script_param_1, ":kingdom_no"),
      (store_script_param_2, ":difference"),

      (try_begin),
        (lt, ":difference", 0),
        (store_relation, ":player_relation", ":kingdom_no", "fac_player_supporters_faction"),
        (val_min, ":player_relation", 0),
        (val_add, ":player_relation", ":difference"),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_no", ":player_relation"),
      (try_end),
  ]),

("diplomacy_start_war_between_kingdoms", #sets relations between two kingdoms and their vassals.
    [
      (store_script_param, ":kingdom_a", 1),
      (store_script_param, ":kingdom_b", 2),
      (store_script_param, ":initializing_war_peace_cond", 3), #1 = after start of game

	  (call_script, "script_npc_decision_checklist_peace_or_war", ":kingdom_a", ":kingdom_b", -1),
	  (assign, ":explainer_string", reg1),

	  #
    ##diplomacy begin
    (try_begin),
      (lt, ":initializing_war_peace_cond", 2),
    ##diplomacy end
	  (try_begin),
	    (eq, ":kingdom_a", "fac_player_supporters_faction"),
		(assign, ":war_event", logent_player_faction_declares_war),
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_declared_war_to_control_calradia"),
		(assign, ":war_event", logent_player_faction_declares_war), #for savegame compatibility, this event stands in for the attempt to declare war on all of calradia
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_considers_s16_to_be_dangerous_and_untrustworthy_and_shehe_wants_to_bring_s16_down"),
		(assign, ":war_event", logent_faction_declares_war_out_of_personal_enmity),
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_is_anxious_to_reclaim_old_lands_such_as_s18_now_held_by_s16"),
		(assign, ":war_event", logent_faction_declares_war_to_regain_territory),
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_faces_too_much_internal_discontent_to_feel_comfortable_ignoring_recent_provocations_by_s16s_subjects"),
		(assign, ":war_event", logent_faction_declares_war_to_respond_to_provocation),
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_is_alarmed_by_the_growing_power_of_s16"),
		(assign, ":war_event", logent_faction_declares_war_to_curb_power),
	  (try_end),
	  (call_script, "script_add_log_entry", ":war_event", ":kingdom_a", 0, 0, ":kingdom_b"),



	  (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":kingdom_a", ":kingdom_b"),
	  (assign, ":current_diplomatic_status", reg0),
	  (try_begin), #effects of policy only after the start of the game
	    (eq, ":initializing_war_peace_cond", 1),
		(eq, ":current_diplomatic_status", -1),
		(call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_declares_war_with_justification),
	  (else_try),
	    (eq, ":initializing_war_peace_cond", 1),
		(eq, ":current_diplomatic_status", 0),
		(call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_attacks_without_provocation),
	  (else_try),
		(eq, ":current_diplomatic_status", 1),
		(call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_breaks_truce),
	  (try_end),
	  ##diplomacy begin
    (else_try),
      (assign, ":war_event", logent_faction_declares_war_to_fulfil_pact),
      (call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_declares_war_with_justification),
      (assign, ":initializing_war_peace_cond", 1),
	  (try_end),
	  ##diplomacy end

      (store_relation, ":relation", ":kingdom_a", ":kingdom_b"),
      (val_min, ":relation", -10),
      (val_add, ":relation", -30),
      (set_relation, ":kingdom_a", ":kingdom_b", ":relation"),

      (try_begin),
        (eq, "$players_kingdom", ":kingdom_a"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_b"),
        (val_min, ":relation", -30),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_b", ":relation"),
      (else_try),
        (eq, "$players_kingdom", ":kingdom_b"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_a"),
        (val_min, ":relation", -30),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_a", ":relation"),
      (try_end),

      (try_begin),
        (eq, ":initializing_war_peace_cond", 1),

		#Remove this -- this scrambles who declares war on whom
#        (try_begin),
 #         (store_random_in_range, ":random_no", 0, 2),
  #        (this_or_next|eq, ":kingdom_a", "fac_player_supporters_faction"),
	#		(eq, ":random_no", 0),
     #     (assign, ":local_temp", ":kingdom_a"),
      #    (assign, ":kingdom_a", ":kingdom_b"),
       #   (assign, ":kingdom_b", ":local_temp"),
        #(try_end),

        (str_store_faction_name_link, s1, ":kingdom_a"),
        #SB : don't colorize message, if it's relevant script_set_player_relation_with_faction calls will show it
        # (faction_get_color, ":color", ":kingdom_a"),
        (str_store_faction_name_link, s2, ":kingdom_b"),
        (display_log_message, "@{s1} has declared war against {s2}.", message_alert),

		(store_current_hours, ":hours"),
		(faction_set_slot, ":kingdom_a", slot_faction_ai_last_decisive_event, ":hours"),
		(faction_set_slot, ":kingdom_b", slot_faction_ai_last_decisive_event, ":hours"),

		#set provocation and truce days
		(store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
		(store_add, ":provocation_slot", ":kingdom_b", slot_faction_provocation_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
		(val_sub, ":provocation_slot", kingdoms_begin),
		(faction_set_slot, ":kingdom_a", ":truce_slot", 0),
		(faction_set_slot, ":kingdom_a", ":provocation_slot", 0),

		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
		(store_add, ":provocation_slot", ":kingdom_a", slot_faction_provocation_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
		(val_sub, ":provocation_slot", kingdoms_begin),
		(faction_set_slot, ":kingdom_b", ":truce_slot", 0),
		(faction_set_slot, ":kingdom_b", ":provocation_slot", 0),

        (call_script, "script_add_notification_menu", "mnu_notification_war_declared", ":kingdom_a", ":kingdom_b"),

        (call_script, "script_update_faction_notes", ":kingdom_a"),
        (call_script, "script_update_faction_notes", ":kingdom_b"),
        (assign, "$g_recalculate_ais", 1),
      (try_end),

	  (try_begin),
		(check_quest_active, "qst_cause_provocation"),
	    (neg|check_quest_succeeded, "qst_cause_provocation"),
		(this_or_next|eq, "$players_kingdom", ":kingdom_a"),
			(eq, "$players_kingdom", ":kingdom_b"),
		(call_script, "script_abort_quest", "qst_cause_provocation", 0),
	  (try_end),
    ##diplomacy begin
    #check for defensive
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (neq, ":cur_kingdom", ":kingdom_a"),
      (neq, ":cur_kingdom", ":kingdom_b"),

      (store_relation, ":cur_relation", ":cur_kingdom", ":kingdom_a"),
			(ge, ":cur_relation", 0), #AT PEACE

      (store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
  		(val_sub, ":truce_slot", kingdoms_begin),
  		(faction_get_slot, ":truce_days", ":cur_kingdom", ":truce_slot"),
  		##nested diplomacy start+ replace "40" with a named constant
  		#(gt, ":truce_days", 40),
  		(gt, ":truce_days", dplmc_treaty_defense_days_expire),
  		##nested diplomacy end+
  		(try_begin),
  		  (lt, ":initializing_war_peace_cond", 2), #only if war was not caused by defensive or alliance pact
  		  (call_script, "script_diplomacy_start_war_between_kingdoms", ":cur_kingdom", ":kingdom_a", 2),
  		(try_end),
    (try_end),

    #check for alliance
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (neq, ":cur_kingdom", ":kingdom_a"),
      (neq, ":cur_kingdom", ":kingdom_b"),

      (store_relation, ":cur_relation", ":cur_kingdom", ":kingdom_b"),
			(ge, ":cur_relation", 0), #AT PEACE

  		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
  		(val_sub, ":truce_slot", kingdoms_begin),
  		(faction_get_slot, ":truce_days", ":cur_kingdom", ":truce_slot"),
  		##nested diplomacy start+ replace "60" with a named constant
  		#(gt, ":truce_days", 60),
  		(gt, ":truce_days", dplmc_treaty_alliance_days_expire),
  		##nested diplomacy end+
  		(call_script, "script_diplomacy_start_war_between_kingdoms", ":cur_kingdom", ":kingdom_b", 3),
    (try_end),
    ##diplomacy end
  ]),

("diplomacy_party_attacks_neutral", #called from game_menus (plundering a village, raiding a village),  from dialogs: surprise attacking a neutral lord, any attack on caravan or villagers
#Has no effect if factions are already at war
    [
      (store_script_param, ":attacker_party", 1),
      (store_script_param, ":defender_party", 2),

	  (store_faction_of_party, ":attacker_faction", ":attacker_party"),
	  (store_faction_of_party, ":defender_faction", ":defender_party"),

	  (party_stack_get_troop_id, ":attacker_leader", ":attacker_party", 0),

	  (try_begin),
		(eq, ":attacker_party", "p_main_party"),
		(neq, ":attacker_faction", "fac_player_supporters_faction"),
		(assign, ":attacker_faction", "$players_kingdom"),
	  (else_try),
		(eq, ":attacker_party", "p_main_party"),
		(eq, ":attacker_faction", "fac_player_supporters_faction"),
	  (try_end),

	  (try_begin),
	    (eq, ":attacker_party", "p_main_party"),
		(store_relation, ":relation", ":attacker_faction", ":defender_faction"),
	    (ge, ":relation", 0),
		(call_script, "script_change_player_honor", -2),
	  (try_end),


	  (try_begin),
		(check_quest_active, "qst_cause_provocation"),
		(quest_slot_eq, "qst_cause_provocation", slot_quest_target_faction, ":defender_faction"),
		(quest_get_slot, ":giver_troop", "qst_cause_provocation", slot_quest_giver_troop),
		(store_faction_of_troop, ":attacker_faction", ":giver_troop"),
		(call_script, "script_succeed_quest", "qst_cause_provocation"),
	  (try_end),

	  (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":attacker_faction", ":defender_faction"),
	  (assign, ":diplomatic_status", reg0),

	  (try_begin),
	    (eq, ":attacker_faction", "fac_player_supporters_faction"),
		(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
		#player faction inactive, no effect
	  (else_try),
		(eq, ":diplomatic_status", -2),
	    #war, no effect
	  (else_try),

	    (eq, ":attacker_faction", "fac_player_supporters_faction"),
		(faction_slot_eq, ":attacker_faction", slot_faction_leader, "trp_player"),
		(call_script, "script_faction_follows_controversial_policy", "fac_player_supporters_faction",logent_policy_ruler_attacks_without_provocation),
	  (else_try),
		(eq, ":diplomatic_status", 1),
		#truce
		(party_stack_get_troop_id, ":defender_party_leader", ":defender_party", 0),
		(try_begin),
			##diplomacy start+ add support for promoted kingdom ladies
			#(i.e. verify not a promoted kingdom lady, since they exist)
			(this_or_next|neg|is_between, ":defender_party_leader", kingdom_ladies_begin, kingdom_ladies_end),
				(neg|troop_slot_eq, ":defender_party_leader", slot_troop_occupation, slto_kingdom_hero),
			##diplomacy end+
			(neg|is_between, ":defender_party_leader", active_npcs_begin, active_npcs_end),
			(store_faction_of_party, ":defender_party_faction", ":defender_party"),
			(faction_get_slot, ":defender_party_leader", ":defender_party_faction", slot_faction_leader),
		(try_end),

		(call_script, "script_add_log_entry", logent_border_incident_troop_breaks_truce, ":attacker_leader", -1, ":defender_party_leader", ":attacker_faction"),
	  (else_try),
		#truce
		(call_script, "script_add_log_entry", logent_border_incident_troop_attacks_neutral, ":attacker_leader", -1, ":defender_party_leader", ":attacker_faction"),
	  (try_end),

	  (try_begin),
	    (is_between, ":defender_party", villages_begin, villages_end),
	    (call_script, "script_add_log_entry", logent_village_raided, ":attacker_leader",  ":defender_party", -1, ":defender_faction"),
        #SB : add quest cancellation when raiding villages
        (try_begin),
          (eq, ":attacker_party", "p_main_party"),
          (party_get_slot, ":elder", ":defender_party", slot_town_elder),
          (gt, ":elder", 0),
          (try_for_range, ":quest_no", village_elder_quests_begin, village_elder_quests_end),
            (quest_slot_eq, ":quest_no", slot_quest_giver_troop, ":elder"),
            (call_script, "script_abort_quest", ":quest_no", 1),
          (try_end),
        (try_end),
	  (else_try),
	    (party_get_template_id, ":template", ":defender_party"),
	    # (neq, ":template", "pt_kingdom_hero_party"),
	    (eq, ":template", "pt_kingdom_caravan_party"), #SB: fix this to specifically apply to caravans
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_faction_name, s5, ":defender_faction"),
			(display_message, "@{!}Debug - {s5} caravan attacked"),
		(try_end),

	    (call_script, "script_add_log_entry", logent_caravan_accosted, ":attacker_leader",  -1, -1, ":defender_faction"),
	  (try_end),

	  (store_add, ":slot_truce_days", ":attacker_faction", slot_faction_provocation_days_with_factions_begin),
	  (val_sub, ":slot_truce_days", kingdoms_begin),
	  (faction_set_slot, ":defender_faction", ":slot_truce_days", 0),

	  (store_add, ":slot_provocation_days", ":attacker_faction", slot_faction_provocation_days_with_factions_begin),
	  (val_sub, ":slot_provocation_days", kingdoms_begin),
	  (try_begin),
	    (neq, ":diplomatic_status", -2),
		(faction_slot_eq, ":defender_faction", ":slot_provocation_days", 0),
		(faction_set_slot, ":defender_faction", ":slot_provocation_days", 30),
	  (try_end),
	]),

("diplomacy_start_peace_between_kingdoms", #sets relations between two kingdoms
    [
      (store_script_param, ":kingdom_a", 1),
      (store_script_param, ":kingdom_b", 2),
      (store_script_param, ":initializing_war_peace_cond", 3), #set to 1 if not the start of the game

      (store_relation, ":relation", ":kingdom_a", ":kingdom_b"),
      (val_max, ":relation", 0),
      (set_relation, ":kingdom_a", ":kingdom_b", ":relation"),
      (call_script, "script_exchange_prisoners_between_factions", ":kingdom_a", ":kingdom_b"),

      (try_begin),
        (eq, "$players_kingdom", ":kingdom_a"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_b"),
        (val_max, ":relation", 0),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_b", ":relation"),
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", "fac_player_supporters_faction"), #event cancels certain quests
      (else_try),
        (eq, "$players_kingdom", ":kingdom_b"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_a"),
        (val_max, ":relation", 0),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_a", ":relation"),
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", "fac_player_supporters_faction"), #event cancels certain quests
      (try_end),

      (try_for_range, ":cur_center", centers_begin, centers_end),
        (store_faction_of_party, ":faction_no", ":cur_center"),
        (this_or_next|eq, ":faction_no", ":kingdom_a"),
        (eq, ":faction_no", ":kingdom_b"),
        (party_get_slot, ":besieger_party", ":cur_center", slot_center_is_besieged_by),
        (ge, ":besieger_party", 0), #town is under siege
        (party_is_active, ":besieger_party"),
        (store_faction_of_party, ":besieger_party_faction_no", ":besieger_party"),
        (this_or_next|eq, ":besieger_party_faction_no", ":kingdom_a"),
        (eq, ":besieger_party_faction_no", ":kingdom_b"),
        (call_script, "script_lift_siege", ":cur_center", 0),
      (try_end),

      (try_begin),
        (this_or_next|eq, "$players_kingdom", ":kingdom_a"),
        (eq, "$players_kingdom", ":kingdom_b"),

        (ge, "$g_player_besiege_town", 0),
        (party_is_active, "$g_player_besiege_town"),

        (store_faction_of_party, ":besieged_center_faction_no", "$g_player_besiege_town"),

        (this_or_next|eq, ":besieged_center_faction_no", ":kingdom_a"),
        (eq, ":besieged_center_faction_no", ":kingdom_b"),

        (call_script, "script_lift_siege", "$g_player_besiege_town", 0),
        (assign, "$g_player_besiege_town", -1),
      (try_end),

      (try_begin),
        (eq, ":initializing_war_peace_cond", 1),
        (str_store_faction_name_link, s1, ":kingdom_a"),
        (str_store_faction_name_link, s2, ":kingdom_b"),
        (display_log_message, "@{s1} and {s2} have made peace with each other.", message_alert),
        (call_script, "script_add_notification_menu", "mnu_notification_peace_declared", ":kingdom_a", ":kingdom_b"), #stability penalty for early peace is in the menu
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", ":kingdom_b"), #cancels quests
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", ":kingdom_a"), #cancels quests
        (assign, "$g_recalculate_ais", 1),
      (try_end),

	  (try_begin), #add truce
		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
		##diplomacy begin
	    #(faction_set_slot, ":kingdom_b", ":truce_slot", 40),
        ##nested diplomacy start+ replace "20" with constant for truce length
#        (faction_set_slot, ":kingdom_b", ":truce_slot", 20),
        (faction_set_slot, ":kingdom_b", ":truce_slot", dplmc_treaty_truce_days_initial),
        ##nested diplomacy end+
	    ##diplomacy end
		(store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
	    ##diplomacy begin
	    #(faction_set_slot, ":kingdom_a", ":truce_slot", 40),
        ##nested diplomacy start+ replace "20" with constant for truce length
        #(faction_set_slot, ":kingdom_a", ":truce_slot", 20),
        (faction_set_slot, ":kingdom_a", ":truce_slot", dplmc_treaty_truce_days_initial),
        ##nested diplomacy end+
        ##diplomacy end
		(store_add, ":slot_war_damage_inflicted_on_b", ":kingdom_b", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_b", kingdoms_begin),
		#(faction_get_slot, ":damage_inflicted_by_a", ":kingdom_a", ":slot_war_damage_inflicted_on_b"),
		(faction_set_slot, ":kingdom_a", ":slot_war_damage_inflicted_on_b", 0),
		(store_add, ":slot_war_damage_inflicted_on_a", ":kingdom_a", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_a", kingdoms_begin),
		#(faction_get_slot, ":damage_inflicted_by_b", ":kingdom_b", ":slot_war_damage_inflicted_on_a"),
		(faction_set_slot, ":kingdom_b", ":slot_war_damage_inflicted_on_a", 0),
	  (try_end),
  ]),

("event_kingdom_make_peace_with_kingdom",
    [
      (store_script_param_1, ":source_kingdom"),
      (store_script_param_2, ":target_kingdom"),
      (try_begin),
        (check_quest_active, "qst_capture_prisoners"),
        (try_begin),
          (eq, "$players_kingdom", ":source_kingdom"),
          (quest_slot_eq, "qst_capture_prisoners", slot_quest_target_faction, ":target_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_prisoners"),
        (else_try),
          (eq, "$players_kingdom", ":target_kingdom"),
          (quest_slot_eq, "qst_capture_prisoners", slot_quest_target_faction, ":source_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_prisoners"),
        (try_end),
      (try_end),

      (try_begin),
        (check_quest_active, "qst_capture_enemy_hero"),
        (try_begin),
          (eq, "$players_kingdom", ":source_kingdom"),
          (quest_slot_eq, "qst_capture_enemy_hero", slot_quest_target_faction, ":target_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_enemy_hero"),
        (else_try),
          (eq, "$players_kingdom", ":target_kingdom"),
          (quest_slot_eq, "qst_capture_enemy_hero", slot_quest_target_faction, ":source_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_enemy_hero"),
        (try_end),
      (try_end),



      (try_begin),
        (check_quest_active, "qst_persuade_lords_to_make_peace"),
        (quest_get_slot, ":lord_1", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
        (quest_get_slot, ":lord_2", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),

        (try_begin),
            (lt, ":lord_1", 0),
            (val_mul, ":lord_1", -1),
        (try_end),
        (try_begin),
            (lt, ":lord_2", 0),
            (val_mul, ":lord_2", -1),
        (try_end),


        (store_faction_of_troop, ":lord_1_faction", ":lord_1"),
        (store_faction_of_troop, ":lord_2_faction", ":lord_2"),

        (this_or_next|eq, ":lord_1_faction", ":source_kingdom"),
            (eq, ":lord_2_faction", ":source_kingdom"),

        (this_or_next|eq, ":lord_1_faction", ":target_kingdom"),
            (eq, ":lord_2_faction", ":target_kingdom"),

        (call_script, "script_cancel_quest", "qst_persuade_lords_to_make_peace"),

      (try_end),

      #Rescue prisoners cancelled in simple_triggers

      (try_begin),
        #SB : better checking, also adds rtr for co-ruler
        (this_or_next|eq, "$players_kingdom", ":source_kingdom"),
        (eq, "$players_kingdom", ":target_kingdom"),
        (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
        (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
        (call_script, "script_change_player_right_to_rule", 3),
      (try_end),

  ]),
]
