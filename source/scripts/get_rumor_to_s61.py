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

get_rumor_to_s61_scripts = [
("get_rumor_to_s61",
    [
     (store_script_param, ":base_rumor_id", 1), # the script returns the same rumor for the same rumor id, so that one cannot hear all rumors by
                                                # speaking to a single person.
     ##diplomacy start+ save reg4 in order to revert it at the end of the script
	 (assign, ":save_reg4", reg4),
	 ##diplomacy end+
     (store_current_hours, ":cur_hours"),
     (store_div, ":cur_day", ":cur_hours", 24),
     (assign, ":rumor_found", 0),
     (assign, ":num_tries", 3),
     (try_for_range, ":try_no", 0, ":num_tries"),
       (store_mul, ":rumor_id", ":try_no", 6781),
       (val_add, ":rumor_id", ":base_rumor_id"),
       (store_mod, ":rumor_type", ":rumor_id", 7),
       (val_add, ":rumor_id", ":cur_hours"),
       (try_begin),
         (eq,  ":rumor_type", 0),
         (try_begin),
           (store_sub, ":range", towns_end, towns_begin),
           (store_mod, ":random_center", ":rumor_id", ":range"),
           (val_add, ":random_center", towns_begin),
           (party_slot_ge, ":random_center", slot_town_has_tournament, 1),
           (neq, ":random_center", "$current_town"),
           (str_store_party_name, s62, ":random_center"),
           (str_store_string, s61, "@I heard that there will be a tournament in {s62} soon."),
           (assign, ":rumor_found", 1),
         (try_end),
       (else_try),
         (eq,  ":rumor_type", 1),
         (try_begin),
           (store_sub, ":range", active_npcs_end, original_kingdom_heroes_begin), #was reversed
           (store_mod, ":random_hero", ":rumor_id", ":range"),
           (val_add, ":random_hero", original_kingdom_heroes_begin),
		   (is_between, ":random_hero", active_npcs_begin, active_npcs_end),
           (troop_get_slot, ":personality", ":random_hero", slot_lord_reputation_type),
		   ##diplomacy start+ give rumors for non-noble personalities, and make pronouns gender-correct
		   (try_begin),
		      (ge, ":personality", lrep_roguish),
			  (try_begin),
			    (eq, ":personality", lrep_benefactor),#Ymira, Bunduk, Jeremus
				(assign, ":personality", lrep_goodnatured),#treats people living in his lands decently
			  (else_try),
			    (eq, ":personality", lrep_custodian),#Marnid, Artimenner, Deshavi, Katrin
				(assign, ":personality", lrep_goodnatured),#good to his followers, and rewards them if they work well
			  (else_try),
			    (call_script, "script_dplmc_get_troop_morality_value", ":random_hero", tmt_humanitarian),
				(lt, reg0, 0),#Klethi
				(assign, ":personality", lrep_debauched),#likes to torture his enemies
			  (try_end),
			  (ge, ":personality", lrep_roguish),
			  (assign, ":personality", 0),#zero out to avoid jumping to a nonsensical string
		   (try_end),
		   (call_script, "script_dplmc_store_troop_is_female_reg", ":random_hero", 4),#store gender to reg4 to make pronouns gender-correct
		   ##diplomacy end+
           (gt, ":personality", 0),
           (store_add, ":rumor_string", ":personality", "str_gossip_about_character_default"),
           (str_store_troop_name, s6, ":random_hero"),
           (str_store_string, s61, ":rumor_string"),
           (assign, ":rumor_found", 1),
         (try_end),
         ##diplomacy start+ Change the rumor string in some circumstances to avoid implying the hero is currently ruling a fief
         (try_begin),
           (neg|is_between, ":random_hero", heroes_begin, heroes_end),
         (else_try),
           #Dead
           (troop_slot_eq, ":random_hero", slot_troop_occupation, dplmc_slto_dead),
           (str_store_troop_name, s6, ":random_hero"),
           (str_store_string, s61, "@I heard some people say they don't believe {s6} is really dead."),#The doubters are wrong, like with Tupac or Elvis.
           (assign, ":rumor_found", 1),
         (else_try),
           #In exile
           (this_or_next|troop_slot_eq, ":random_hero", slot_troop_occupation, slto_retirement),
           (troop_slot_eq, ":random_hero", slot_troop_occupation, dplmc_slto_exile),
           (str_store_troop_name, s6, ":random_hero"),
           (str_store_string, s61, "@I heard a traveller say that he came across {s6} while journeying outside these lands."),
           (assign, ":rumor_found", 1),
         (else_try),
           #Inactive pretender
           (troop_slot_eq, ":random_hero", slot_troop_occupation, slto_inactive_pretender),
           (neq, ":random_hero", "$supported_pretender"),
           (troop_get_slot, reg4, ":random_hero", slot_troop_original_faction),
           (is_between, reg4, npc_kingdoms_begin, npc_kingdoms_end),
           (faction_slot_eq, reg4, slot_faction_state, sfs_active),
           (faction_get_slot, reg4, reg4, slot_faction_leader),
           (gt, reg4, -1),
           (str_store_troop_name, s61, reg4),
           (str_store_string, s6, ":random_hero"),
           (str_store_string, s61, "@I heard that {s6} intends to raise an army and seize the throne from {s61}."),
           (assign, ":rumor_found", 1),
         (try_end),
         ##diplomacy end+
       (else_try),
         (eq,  ":rumor_type", 2),
         (try_begin),
           (store_sub, ":range", trade_goods_end, trade_goods_begin),
           (store_add, ":random_trade_good", ":rumor_id", ":cur_day"),
           (store_mod, ":random_trade_good", ":random_trade_good", ":range"),
           (store_add, ":random_trade_good_slot", ":random_trade_good", slot_town_trade_good_prices_begin),
           (val_add, ":random_trade_good", trade_goods_begin),
           (store_mul, ":min_price", average_price_factor, 3),
           (val_div, ":min_price", 4),
           (assign, ":min_price_center", -1),
           (try_for_range, ":sub_try_no", 0, 10),
             (store_sub, ":range", towns_end, towns_begin),
             (store_add, ":center_rumor_id", ":rumor_id", ":sub_try_no"),
             (store_mod, ":random_center", ":center_rumor_id", ":range"),
             (val_add, ":random_center", towns_begin),
             (neq, ":random_center", "$g_encountered_party"),
             (party_get_slot, ":cur_price", ":random_center", ":random_trade_good_slot"),
             (lt, ":cur_price", ":min_price"),
             (assign, ":min_price", ":cur_price"),
             (assign, ":min_price_center", ":random_center"),
           (try_end),
           (ge, ":min_price_center", 0),
           (str_store_item_name, s62, ":random_trade_good"),
           (str_store_party_name, s63, ":min_price_center"),
           (str_store_string, s61, "@I heard that one can buy {s62} very cheap at {s63}."),
           (assign, ":rumor_found", 1),
         (try_end),
       (else_try),
         (eq,  ":rumor_type", 3),
         (try_begin),
           (store_sub, ":range", trade_goods_end, trade_goods_begin),
           (store_add, ":random_trade_good", ":rumor_id", ":cur_day"),
           (store_mod, ":random_trade_good", ":random_trade_good", ":range"),
           (store_add, ":random_trade_good_slot", ":random_trade_good", slot_town_trade_good_prices_begin),
           (val_add, ":random_trade_good", trade_goods_begin),
           (store_mul, ":max_price", average_price_factor, 5),
           (val_div, ":max_price", 4),
           (assign, ":max_price_center", -1),
           (try_for_range, ":sub_try_no", 0, 10),
             (store_sub, ":range", towns_end, towns_begin),
             (store_add, ":center_rumor_id", ":rumor_id", ":sub_try_no"),
             (store_mod, ":random_center", ":center_rumor_id", ":range"),
             (val_add, ":random_center", towns_begin),
             (neq, ":random_center", "$g_encountered_party"),
             (party_get_slot, ":cur_price", ":random_center", ":random_trade_good_slot"),
             (gt, ":cur_price", ":max_price"),
             (assign, ":max_price", ":cur_price"),
             (assign, ":max_price_center", ":random_center"),
           (try_end),
           (ge, ":max_price_center", 0),
           (str_store_item_name, s62, ":random_trade_good"),
           (str_store_party_name, s63, ":max_price_center"),
           (str_store_string, s61, "@I heard that they pay a very high price for {s62} at {s63}."),
           (assign, ":rumor_found", 1),
         (try_end),
       (try_end),
       (try_begin),
         (gt, ":rumor_found", 0),
         (assign, ":num_tries", 0),
       (try_end),
     (try_end),
     (assign, reg0, ":rumor_found"),
	 ##diplomacy start+ revert reg4
	 (assign, reg4, ":save_reg4"),
	 ##diplomacy end+
     ])
]
