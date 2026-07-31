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



   #Accumulate taxes
   

refresh_cattle_in_villages_simple_triggers = [
(24 * 7,
   [
      #Adding earnings to town lords' wealths.
      #Moved to troop does business
      #(try_for_range, ":center_no", centers_begin, centers_end),
      #  (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
      #  (neq, ":town_lord", "trp_player"),
      #  (is_between, ":town_lord", active_npcs_begin, active_npcs_end),
      #  (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
      #  (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
      #  (troop_get_slot, ":troop_wealth", ":town_lord", slot_troop_wealth),
      #  (val_add, ":troop_wealth", ":accumulated_rents"),
      #  (val_add, ":troop_wealth", ":accumulated_tariffs"),
      #  (troop_set_slot, ":town_lord", slot_troop_wealth, ":troop_wealth"),
      #  (party_set_slot, ":center_no", slot_center_accumulated_rents, 0),
      #  (party_set_slot, ":center_no", slot_center_accumulated_tariffs, 0),
      #  (try_begin),
      #    (eq, "$cheat_mode", 1),
      #    (assign, reg1, ":troop_wealth"),
      #    (add_troop_note_from_sreg, ":town_lord", 1, "str_current_wealth_reg1", 0),
      #  (try_end),
      #(try_end),

      #Collect taxes for another week
      (game_get_reduce_campaign_ai, ":reduce_campaign_ai"), #SB : moved to top
      (try_for_range, ":center_no", centers_begin, centers_end),
        (try_begin),
          (party_slot_ge, ":center_no", slot_town_lord, 0), #unassigned centers do not accumulate rents

          (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),

          (assign, ":cur_rents", 0),
          (try_begin),
            (party_slot_eq, ":center_no", slot_party_type, spt_village),
            (try_begin),
              (party_slot_eq, ":center_no", slot_village_state, svs_normal),
              (assign, ":cur_rents", 1200),
            (try_end),
          (else_try),
            (party_slot_eq, ":center_no", slot_party_type, spt_castle),
            (assign, ":cur_rents", 1200),
          (else_try),
            (party_slot_eq, ":center_no", slot_party_type, spt_town),
            (assign, ":cur_rents", 2400),
          (try_end),

          (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity), #prosperty changes between 0..100
          (store_add, ":multiplier", 20, ":prosperity"), #multiplier changes between 20..120
          (val_mul, ":cur_rents", ":multiplier"),
          (val_div, ":cur_rents", 120),#Prosperity of 100 gives the default values

          (try_begin),
            (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),

            # (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
            (try_begin),
              (eq, ":reduce_campaign_ai", 0), #hard (less money from rents)
              (val_mul, ":cur_rents", 3),
              (val_div, ":cur_rents", 4),
            (else_try),
              (eq, ":reduce_campaign_ai", 1), #medium (normal money from rents)
              #same
            (else_try),
              (eq, ":reduce_campaign_ai", 2), #easy (more money from rents)
              (val_mul, ":cur_rents", 4),
              (val_div, ":cur_rents", 3),
            (try_end),
          (try_end),

          (val_add, ":accumulated_rents", ":cur_rents"), #cur rents changes between 23..1000

          ##diplomacy begin
          (try_begin),
            (str_store_party_name, s6, ":center_no"),

            (party_get_slot, ":tax_rate", ":center_no", dplmc_slot_center_taxation),
            (neq, ":tax_rate", 0),
            (store_div, ":rent_change", ":accumulated_rents", 100),
            (val_mul, ":rent_change", ":tax_rate"),

            (try_begin), #debug
              (eq, "$cheat_mode", 1),
              (assign, reg0, ":tax_rate"),
              (display_message, "@{!}DEBUG : tax rate in {s6}: {reg0}"),
              (assign, reg0, ":accumulated_rents"),
              (display_message, "@{!}DEBUG : accumulated_rents  in {s6}: {reg0}"),
              (assign, reg0, ":rent_change"),
              (display_message, "@{!}DEBUG : rent_change in {s6}: {reg0}  in {s6}"),
            (try_end),

            (val_add, ":accumulated_rents", ":rent_change"),

            (val_div, ":tax_rate", -25),

            (call_script, "script_change_center_prosperity", ":center_no", ":tax_rate"),

            (try_begin),
              (lt, ":tax_rate", 0), #double negative values
              (val_mul, ":tax_rate", 2),

              (try_begin), #debug
                (eq, "$cheat_mode", 1),
                (assign, reg0, ":tax_rate"),
                (display_message, "@{!}DEBUG : tax rate after modi in {s6}: {reg0}"),
              (try_end),

              (try_begin),
                (this_or_next|is_between, ":center_no", villages_begin, villages_end),
                (is_between, ":center_no", towns_begin, towns_end),
                #SB : can't have a revolt right when player is in center
                (neq, ":center_no", "$g_last_rest_center"),
                (party_get_slot, ":center_relation", ":center_no", slot_center_player_relation),

                (try_begin), #debug
                  (eq, "$cheat_mode", 1),
                  (assign, reg0, ":center_relation"),
                  (display_message, "@{!}DEBUG : center relation: {reg0}"),
                (try_end),

                (le, ":center_relation", -5),
                (store_random_in_range, ":random",-100, 0),
                (gt, ":random", ":center_relation"),

                (neg|party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
                (display_log_message, "@There has been a riot in {s6}!", message_negative), #SB : log message, colorize
                (party_set_slot, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"), #trp_peasant_woman used to simulate riot
                (call_script, "script_change_center_prosperity", ":center_no", -1),
                (call_script, "script_add_notification_menu", "mnu_dplmc_notification_riot", ":center_no", 0),

                #add additional troops
                (store_character_level, ":player_level", "trp_player"),
                (store_div, ":player_leveld2", ":player_level", 2),
                (store_mul, ":player_levelx2", ":player_level", 2),
                (try_begin),
                  (is_between, ":center_no", villages_begin, villages_end),
                  (store_random_in_range, ":random",0, ":player_level"),
                  (party_add_members, ":center_no", "trp_mercenary_swordsman", ":random"),
                  (store_random_in_range, ":random", 0, ":player_leveld2"),
                  (party_add_members, ":center_no", "trp_hired_blade", ":random"),
                (else_try),
                  (party_set_banner_icon, ":center_no", 0),
                  (party_get_num_companion_stacks, ":num_stacks",":center_no"),
                  (try_for_range, ":i_stack", 0, ":num_stacks"),
                    (party_stack_get_size, ":stack_size",":center_no",":i_stack"),
                    (val_div, ":stack_size", 2),
                    (party_stack_get_troop_id, ":troop_id", ":center_no", ":i_stack"),
                    (party_remove_members, ":center_no", ":troop_id", ":stack_size"),
                  (try_end),
                  (store_random_in_range, ":random",":player_leveld2", ":player_levelx2"),
                  (party_add_members, ":center_no", "trp_townsman", ":random"),
                  (store_random_in_range, ":random",0, ":player_level"),
                  (party_add_members, ":center_no", "trp_watchman", ":random"),
                (try_end),
              (end_try),
            (try_end),
            (call_script, "script_change_player_relation_with_center", ":center_no", ":tax_rate"),
          (try_end),

          (try_begin), #no taxes for infested villages and towns
            (party_slot_ge, ":center_no", slot_village_infested_by_bandits, 1),
            (assign,":accumulated_rents", 0),
          (try_end),
          ##diplomacy end
          (party_set_slot, ":center_no", slot_center_accumulated_rents, ":accumulated_rents"),
        (try_end),

		(try_begin),
		  (is_between, ":center_no", villages_begin, villages_end),
		  (party_get_slot, ":bound_castle", ":center_no", slot_village_bound_center),
		  (party_slot_ge, ":bound_castle", slot_town_lord, 0), #unassigned centers do not accumulate rents
		  (is_between, ":bound_castle", castles_begin, castles_end),
		  (party_get_slot, ":accumulated_rents", ":bound_castle", slot_center_accumulated_rents), #castle's accumulated rents
		  (val_add, ":accumulated_rents", ":cur_rents"), #add village's rent to castle rents
		  (party_set_slot, ":bound_castle", slot_center_accumulated_rents, ":accumulated_rents"),
		(try_end),
      (try_end),
    ]),
]
