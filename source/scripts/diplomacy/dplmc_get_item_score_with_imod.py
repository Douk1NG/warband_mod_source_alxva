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

dplmc_get_item_score_with_imod_scripts = [
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
    ])
]
