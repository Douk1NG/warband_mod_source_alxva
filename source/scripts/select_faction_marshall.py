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

select_faction_marshall_scripts = [
# script_calculate_hero_weekly_net_income_and_add_to_wealth
("select_faction_marshall",
   [
#     (store_script_param_1, ":faction_no"),
 #    (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
  #   (faction_get_slot, ":old_faction_marshall", ":faction_no", slot_faction_marshall),

   #  (assign, ":old_marshal_is_avaliable", 0),
    # (try_begin),
     #  (gt, ":old_faction_marshall", 0),
      # (troop_get_slot, ":old_marshal_party", ":old_faction_marshall", slot_troop_leaded_party),
     #  (party_is_active, ":old_marshal_party"),
    #   (assign, ":old_marshal_is_avaliable", 1),
   #  (try_end),

     #Ozan : I am adding some codes here because sometimes armies demobilize during last seconds of an
	 #important event like taking a castle, ext because of marshal change. When marshal changes during
	 #an important event occurs new marshal's followers become 0 and continueing siege attack seems less
	 #valuable then armies demobilize, faction ai become "do nothing", "I cannot think anything to do" ext.

   #  (assign, ":there_is_an_important_situation", 0),
   #  (faction_get_slot, ":current_ai_object", ":faction_no", slot_faction_ai_object),

   #  (try_begin), #do not demobilize during taking a castle/town (fighting in the castle)
   #    (is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
   #    (party_get_battle_opponent, ":besieger_party", ":current_ai_object"),
   #    (ge, ":besieger_party", 0),
   #    (party_is_active, ":besieger_party"),
   #    (store_faction_of_party, ":besieger_faction", ":besieger_party"),
   #    (this_or_next|eq, ":besieger_faction", ":faction_no"),
   #    (eq, ":besieger_faction", "fac_player_faction"),
   #    (assign, ":there_is_an_important_situation", 1),
   #  (try_end),

   #  (try_begin), #do not demobilize during raiding a village (holding around village)
   #    (is_between, ":current_ai_object", centers_begin, centers_end),
   #    (neg|is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
   #    (party_slot_eq, ":current_ai_object", slot_village_state, svs_being_raided),
   #    (assign, ":there_is_an_important_situation", 1),
   #  (try_end),

   #  (try_begin), #do not demobilize during besigning a siege (holding around castle)
   #    (is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
   #    #(str_store_party_name, s7, ":current_ai_object"),
   #    (party_get_slot, ":besieger_party", ":current_ai_object", slot_center_is_besieged_by),
   #    (ge, ":besieger_party", 0),
   #    (party_is_active, ":besieger_party"),
   #    #(str_store_party_name, s7, ":besieger_party"),
   #    (store_faction_of_party, ":besieger_faction", ":besieger_party"),
   #    (this_or_next|eq, ":besieger_faction", ":faction_no"),
   #    (eq, ":besieger_faction", "fac_player_faction"),
   #    (assign, ":there_is_an_important_situation", 1),
   #  (try_end),

   #  (try_begin),
   #    (this_or_next|eq, ":there_is_an_important_situation", 0),
   #    (eq, ":old_marshal_is_avaliable", 0),
       #end addition ozan


    #   (assign, ":total_renown", 0),
    #   (try_for_range, ":loop_var", active_npcs_including_player_begin, active_npcs_end),
    #     (assign, ":cur_troop", ":loop_var"),
    #     (assign, ":continue", 0),
    #     (try_begin),
    #       (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
    #       (assign, ":cur_troop", "trp_player"),
    #       (try_begin),
    #         (eq, ":faction_no", "$players_kingdom"),
    #         (assign, ":continue", 1),
    #       (try_end),
    #     (else_try),
    #       (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
    #       (store_troop_faction, ":cur_faction", ":cur_troop"),
    #       (eq, ":cur_faction", ":faction_no"),
    #       (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
    #       (gt, ":cur_party", 0),
    #       (party_is_active, ":cur_party"),
    #       (call_script, "script_party_count_fit_for_battle", ":cur_party"),
    #       (assign, ":party_fit_for_battle", reg0),
    #       (call_script, "script_party_get_ideal_size", ":cur_party"),
    #       (assign, ":ideal_size", reg0),
    #       (store_mul, ":relative_strength", ":party_fit_for_battle", 100),
    #       (val_div, ":relative_strength", ":ideal_size"),
    #       (ge, ":relative_strength", 25),
    #       (assign, ":continue", 1),
    #     (try_end),

     #    (eq, ":continue", 1),

    #     (troop_get_slot, ":renown", ":cur_troop", slot_troop_renown),
	#     (call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":faction_leader"),
	#     (store_mul, ":relation_modifier", reg0, 15),
	#     (val_add, ":renown", ":relation_modifier"),
	#     (val_max, ":renown", 1),
	#
    #     (try_begin),
    #       (eq, ":cur_troop", "trp_player"),
    #       (neq, ":old_faction_marshall", "trp_player"),
    #       (assign, ":renown", 0),
   #      (try_end),
    #     (try_begin),
    #       (eq, ":cur_troop", ":faction_leader"),
    #       (val_mul, ":renown", 3),
    #       (val_div, ":renown", 4),
    #     (try_end),
    #     (try_begin),
    #       (eq, ":cur_troop", ":old_faction_marshall"),
    #       (val_mul, ":renown", 1000),
    #     (try_end),
    #     (val_add, ":total_renown", ":renown"),
    #   (try_end),
    #   (assign, ":result", -1),
    #   (try_begin),
    #     (gt, ":total_renown", 0),
    #     (store_random_in_range, ":random_renown", 0, ":total_renown"),
    #     (try_for_range, ":loop_var", active_npcs_including_player_begin, active_npcs_end),
    #       (eq, ":result", -1),
    #       (assign, ":cur_troop", ":loop_var"),
    #       (assign, ":continue", 0),
    #       (try_begin),
    #         (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
    #         (assign, ":cur_troop", "trp_player"),
   #          (try_begin),
   #            (eq, ":faction_no", "$players_kingdom"),
   #            (assign, ":continue", 1),
   #          (try_end),
   #        (else_try),
   #          (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
   #          (store_troop_faction, ":cur_faction", ":cur_troop"),
   #          (eq, ":cur_faction", ":faction_no"),
   #          (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
   #          (gt, ":cur_party", 0),
   #          (party_is_active, ":cur_party"),
   #          (call_script, "script_party_count_fit_for_battle", ":cur_party"),
   #          (assign, ":party_fit_for_battle", reg0),
      #       (call_script, "script_party_get_ideal_size", ":cur_party"),
      #       (assign, ":ideal_size", reg0),
      #       (store_mul, ":relative_strength", ":party_fit_for_battle", 100),
      #       (val_div, ":relative_strength", ":ideal_size"),
      #       (ge, ":relative_strength", 25),
      #       (assign, ":continue", 1),
      #     (try_end),
      #     (eq, ":continue", 1),

		#   (troop_get_slot, ":renown", ":cur_troop", slot_troop_renown),
	    #   (call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":faction_leader"),
	    #   (store_mul, ":relation_modifier", reg0, 15),
	    #   (val_add, ":renown", ":relation_modifier"),
	    #   (val_max, ":renown", 1),
		#
        #   (try_begin),
        #     (eq, ":cur_troop", "trp_player"),
        #     (neq, ":old_faction_marshall", "trp_player"),
        #     (assign, ":renown", 0),
        #   (try_end),
        #   (try_begin),
        #     (eq, ":cur_troop", ":faction_leader"),
        #     (val_mul, ":renown", 3),
         #    (val_div, ":renown", 4),
         #  (try_end),
         #  (try_begin),
       #      (eq, ":cur_troop", ":old_faction_marshall"),
       #      (val_mul, ":renown", 1000),
       #    (try_end),
       #    (val_sub, ":random_renown", ":renown"),
       #    (lt, ":random_renown", 0),
       #    (assign, ":result", ":cur_troop"),
       #  (try_end),
      # (try_end),
      # (try_begin),
         #(eq, "$cheat_mode", 1),
        # (ge, ":result", 0),
       #  (str_store_troop_name, s1, ":result"),
      #   (str_store_faction_name, s2, ":faction_no"),
     #    (display_message, "@{!}{s1} is chosen as the marshall of {s2}."),
    #   (try_end),
   #  (else_try),
   #    (faction_get_slot, ":old_faction_marshall", ":faction_no", slot_faction_marshall),
   #    (assign, ":result", ":old_faction_marshall"),
   #  (try_end),

   #  (assign, reg0, ":result"),
     ])
]
