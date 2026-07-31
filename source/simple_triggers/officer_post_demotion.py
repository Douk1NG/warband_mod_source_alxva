# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *

officer_post_demotion_simple_triggers = [
(2,
   [
    (assign, ":has_walled_center", 0),
    (assign, ":has_fief", 0),
    (try_for_range, ":center_no", centers_begin, centers_end),
      (party_get_slot,  ":lord_troop_id", ":center_no", slot_town_lord),
      (eq, ":lord_troop_id", "trp_player"),
      (try_begin),
        (is_between, ":center_no", walled_centers_begin, walled_centers_end),
        (assign, ":has_walled_center", 1),
      (try_end),
      (assign, ":has_fief", 1),
    (try_end),

    (try_begin),
      (eq, ":has_walled_center", 0),
      (this_or_next|neq, "$g_player_constable", 0),
      (neq, "$g_player_chancellor", 0),
      (assign, "$g_player_constable", 0),
      (assign, "$g_player_chancellor", 0),
    (try_end),

    (try_begin),
      (eq, ":has_fief", 0),
      (neq, "$g_player_chamberlain", 0),
      (assign, "$g_player_chamberlain", 0),

      ##nested diplomacy start+
      #Adjust gold loss by difficulty
      (assign, ":save_reg0", reg0),
      (assign, ":save_reg1", reg1),

      (assign, ":loss_numerator", 2),
      (assign, ":loss_denominator", 3),

      (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
      (try_begin),
        (eq, ":reduce_campaign_ai", 0), #hard, lose 5/6
        (assign, ":loss_numerator", 5),
        (assign, ":loss_denominator", 6),
      (else_try),
        (eq, ":reduce_campaign_ai", 1), #medium, lose 2/3
        (assign, ":loss_numerator", 2),
        (assign, ":loss_denominator", 3),
      (else_try),
        (eq, ":reduce_campaign_ai", 2), #easy, lose 1/2
        (assign, ":loss_numerator", 1),
        (assign, ":loss_denominator", 2),
      (try_end),

      (store_troop_gold, ":cur_gold", "trp_household_possessions"),
      (try_begin),
        (gt, ":cur_gold", 0),
        #(call_script, "script_dplmc_withdraw_from_treasury", ":cur_gold"),
        #(val_div, ":cur_gold", 3),
        #(call_script, "script_troop_add_gold", "trp_player", ":cur_gold"),
        #(display_message, "@Your last fief was captured and you lost 2/3 of your treasury"),
        (store_mul, ":lost_gold", ":cur_gold", ":loss_numerator"),
        (val_div, ":lost_gold", ":loss_denominator"),
        (val_mul, ":lost_gold", -1),
        (call_script, "script_dplmc_withdraw_from_treasury", ":lost_gold"),
        (assign, reg0, ":loss_numerator"),
        (assign, reg1, ":loss_denominator"),
        #SB : colorize
        (display_message, "@Your last fief was captured and you lost {reg0}/{reg1} of your treasury", message_negative),
      (try_end),

      (assign, reg0, ":save_reg0"),
      (assign, reg1, ":save_reg1"),
      ##nested diplomacy end+
    (try_end),
    ]),
]
