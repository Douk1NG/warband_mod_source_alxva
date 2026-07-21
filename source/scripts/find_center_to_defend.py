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

find_center_to_defend_scripts = [
(
    "find_center_to_defend",
    [
      (store_script_param, ":troop_no", 1),

	  (store_faction_of_troop, ":faction_no", ":troop_no"),

      (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
      (faction_get_slot, ":current_ai_state", ":faction_no", slot_faction_ai_state),
      (assign, ":marshal_party", -1),
      (try_begin),
        (gt, ":faction_marshal", 0),
        (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
      (try_end),

      (assign, ":most_threatened_center", -1),
      (assign, ":maximum_threat_score", 0),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (store_faction_of_party, ":center_faction", ":cur_center"),
        (eq, ":center_faction", ":faction_no"),

        (party_get_slot, ":exact_enemy_strength", ":cur_center", slot_center_sortie_enemy_strength),
		#Distort this to account for questionable intelligence
		#(call_script, "script_reduce_exact_number_to_estimate", ":exact_enemy_strength"),
		#(assign, ":enemy_strength_nearby", reg0),
		(assign, ":enemy_strength_nearby", ":exact_enemy_strength"),

        (assign, ":threat_importance", 0),
        (try_begin),
          (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
          (party_slot_ge, ":cur_center", slot_center_is_besieged_by, 0),

          (call_script, "script_find_total_prosperity_score", ":cur_center"),
          (assign, ":total_prosperity_score", reg0),

          (party_get_slot, ":cur_center_strength", ":cur_center", slot_party_cached_strength),
          (val_mul, ":cur_center_strength", 4),
          (val_div, ":cur_center_strength", 3), #give 33% bonus to insiders because they are inside a castle

          #I removed below line and assigned ":cur_center_nearby_strength" to 0, because if not when defender army comes to help
          #threat become less because of high defence power but not yet enemy cleared.
          #(party_get_slot, ":cur_center_nearby_strength", ":cur_center", slot_party_nearby_friend_strength),
          (assign, ":cur_center_nearby_strength", 0),

          (val_add, ":cur_center_strength", ":cur_center_nearby_strength"), #add nearby friends and find ":cur_center_strength"

          (store_mul, ":power_ratio", ":enemy_strength_nearby", 100),
          (val_add, ":cur_center_strength", 1),
		  (val_max, ":cur_center_strength", 1),
          (val_div, ":power_ratio", ":cur_center_strength"),

          (assign, ":player_is_attacking", 0),
          (party_get_slot, ":besieger_party", ":cur_center", slot_center_is_besieged_by),
          (try_begin),
            (party_is_active, ":besieger_party"),
            (try_begin),
              (eq, ":besieger_party", "p_main_party"),
              (assign, ":player_is_attacking", 1),
              #(display_message, "@{!}DEBUG : player is attacking a center (1)"),
            (else_try),
              (store_faction_of_party, ":besieger_faction", ":besieger_party"),
              (eq, ":besieger_faction", "fac_player_faction"),
              (assign, ":player_is_attacking", 1),
              #(display_message, "@{!}DEBUG : player is attacking a center (2)"),
            (else_try),
              (party_get_attached_to, ":player_is_attached_to", "p_main_party"),
              (ge, ":player_is_attached_to", 0),
              (eq, ":player_is_attached_to", ":besieger_party"),
              (assign, ":player_is_attacking", 1),
              #(display_message, "@{!}DEBUG : player is attacking a center (3)"),
            (try_end),
          (try_end),

          (try_begin),
            (eq, ":player_is_attacking", 0),

            (try_begin),
              (lt, ":power_ratio", 40), #changes between 1..1
              (assign, ":threat_importance", 1),
            (else_try),
              (lt, ":power_ratio", 80), #changes between 1..7
              (store_sub, ":threat_importance", ":power_ratio", 40),
              (val_div, ":threat_importance", 5),
              (val_add, ":threat_importance", 1), #1
            (else_try),
              (lt, ":power_ratio", 120), #changes between 7..17
              (store_sub, ":threat_importance", ":power_ratio", 80),
              (val_div, ":threat_importance", 4),
              (val_add, ":threat_importance", 7), #1 + 6
            (else_try),
              (lt, ":power_ratio", 200),
              (store_sub, ":threat_importance", ":power_ratio", 120),
              (val_div, ":threat_importance", 10),
              (val_add, ":threat_importance", 17), #1 + 6 + 10
            (else_try),
              (assign, ":threat_importance", 25),
            (try_end),
          (else_try),
            (try_begin),
              (lt, ":power_ratio", 200), #changes between 5..25
              (store_div, ":threat_importance", ":power_ratio", 10),    #MOTO correction (thanks MOTO:) (mexxico))
              (val_add, ":threat_importance", 6 ),
            (else_try),
              (assign, ":threat_importance", 26),
            (try_end),
          (try_end),
        (else_try),
          (is_between, ":cur_center", villages_begin, villages_end),
          (party_slot_eq, ":cur_center", slot_village_state, svs_being_raided),

          (gt, ":enemy_strength_nearby", 0),

          (call_script, "script_find_total_prosperity_score", ":cur_center"),
          (assign, ":power_ratio", 100), #useless
          (assign, ":total_prosperity_score", reg0),
          (assign, ":threat_importance", 10), #if faction village is looted they lose money for shorter time period. So importance is something low (6-8).
        (try_end),

        (gt, ":threat_importance", 0),

        (try_begin),
          (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
          (assign, ":enemy_strength_nearby_score", 120),

          (try_begin),
            (ge, ":marshal_party", 0),
            (party_is_active, ":marshal_party"),
            (store_distance_to_party_from_party, ":marshal_dist_to_cur_center", ":marshal_party", ":cur_center"),
          (else_try),
            (assign, ":marshal_dist_to_cur_center", 100),
          (try_end),

          (try_begin),
            #if currently our target is ride to break a siege then
            #divide marshal_distance for other center's to "2" instead of "4" and add some small more distance to avoid easily
            #changing mind during siege because of small score differences.

	        #(faction_get_slot, ":current_ai_state", ":faction_no", slot_faction_ai_state),
            (eq, ":current_ai_state", sfai_attacking_enemies_around_center),
            (faction_get_slot, ":current_ai_object", ":faction_no", slot_faction_ai_object),
            (is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
            (neq, ":current_ai_object", ":cur_center"),
            (val_mul, ":marshal_dist_to_cur_center", 2),
            (val_add, ":marshal_dist_to_cur_center", 20),
          (try_end),

          (val_mul, ":marshal_dist_to_cur_center", 2), #standard multipication (1.5x) to adjust distance scoring same with formula at find_center_to_attack
          #(val_div, ":marshal_dist_to_cur_center", 2),

          (try_begin),
            (lt, ":marshal_dist_to_cur_center", 10), #very close (100p)
            (assign, ":distance_score", 100),
          (else_try),
            (lt, ":marshal_dist_to_cur_center", 160), #close (50p-100p)
            (store_sub, ":distance_score", ":marshal_dist_to_cur_center", 10),
            (val_div, ":distance_score", 3),
            (store_sub, ":distance_score", 100, ":distance_score"),
          (else_try),
            (lt, ":marshal_dist_to_cur_center", 360), #far (10p-50p)
            (store_sub, ":distance_score", ":marshal_dist_to_cur_center", 250),
            (val_div, ":distance_score", 5),
            (store_sub, ":distance_score", 50, ":distance_score"),
          (else_try),
            (assign, ":distance_score", 10), #very far
          (try_end),
        (else_try),
          (store_add, ":enemy_strength_nearby_score", ":enemy_strength_nearby", 20000),
          (val_div, ":enemy_strength_nearby_score", 200),
          (assign, ":distance_score", 70), #not related to marshal's position, because everybody is going same place (no gathering in most village raids)
        (try_end),

		##diplomacy start+
		(try_begin),
			#AI changes LOW: Give priority to defending centers with lords
			(le, DPLMC_AI_CHANGES_LOW, "$g_dplmc_ai_changes"),
			(party_slot_ge, ":cur_center", slot_town_lord, 0),
			(val_mul, ":threat_importance", 120),
			(val_div, ":threat_importance", 100),
		(try_end),
		##diplomacy end+
        (store_mul, ":threat_score", ":enemy_strength_nearby_score", ":total_prosperity_score"),
        (val_mul, ":threat_score", ":threat_importance"),
        (val_mul, ":threat_score", ":distance_score"),
        (val_div, ":threat_score", 10000),

        (try_begin),
		  (ge, "$cheat_mode", 1),
          (gt, ":threat_score", 0),
          (eq, ":faction_no", "fac_kingdom_6"),
          (assign, reg0, ":threat_score"),
          (str_store_party_name, s32, ":cur_center"),
          (assign, reg1,  ":total_prosperity_score"),
          (assign, reg2, ":enemy_strength_nearby_score"),
          (assign, reg3, ":threat_importance"),
          (assign, reg4, ":distance_score"),
          #(display_message, "@{!}DEBUG : defend of {s32} is {reg0}, prosperity:{reg1}, enemy nearby:{reg2}, threat importance:{reg3}, distance: {reg4}"),
        (try_end),

        (gt, ":threat_score", ":maximum_threat_score"),

        (assign, ":most_threatened_center", ":cur_center"),
        (assign, ":maximum_threat_score", ":threat_score"),
        (assign, ":enemy_strength_near_most_threatened_center", ":enemy_strength_nearby"),
      (try_end),

      (val_mul, ":maximum_threat_score", 3),
      (val_div, ":maximum_threat_score", 2),

      (assign, reg0, ":most_threatened_center"),
      (assign, reg1, ":maximum_threat_score"),
      (assign, reg2, ":enemy_strength_near_most_threatened_center"),
    ])
]
