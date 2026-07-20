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

update_villages_infested_by_bandits_scripts = [
#script_update_villages_infested_by_bandits
# INPUT: none
# OUTPUT: none
("update_villages_infested_by_bandits",
    [
    #SB : duration tweaks, remember that this is in a 72 hour slot
     (options_get_campaign_ai, ":reduce"),
     (val_add, ":reduce", 2), #default is 3
     (try_for_range, ":village_no", villages_begin, villages_end),
       (try_begin),
         (check_quest_active, "qst_eliminate_bandits_infesting_village"),
         (quest_slot_eq, "qst_eliminate_bandits_infesting_village", slot_quest_target_center, ":village_no"),
         (quest_get_slot, ":cur_state", "qst_eliminate_bandits_infesting_village", slot_quest_current_state),
         (val_add, ":cur_state", 1),
         (try_begin),
           (lt, ":cur_state", ":reduce"),
           (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_current_state, ":cur_state"),
         (else_try),
           (party_set_slot, ":village_no", slot_village_infested_by_bandits, 0),
           (call_script, "script_abort_quest", "qst_eliminate_bandits_infesting_village", 2),
         (try_end),
       (else_try),
         (check_quest_active, "qst_deal_with_bandits_at_lords_village"),
         (neg|check_quest_succeeded, "qst_deal_with_bandits_at_lords_village"), #prevent failing after succeeding
         (quest_slot_eq, "qst_deal_with_bandits_at_lords_village", slot_quest_target_center, ":village_no"),
         (quest_get_slot, ":cur_state", "qst_deal_with_bandits_at_lords_village", slot_quest_current_state),
         (val_add, ":cur_state", 1),
         (try_begin),
           (lt, ":cur_state", ":reduce"),
           (quest_set_slot, "qst_deal_with_bandits_at_lords_village", slot_quest_current_state, ":cur_state"),
         (else_try),
           (party_set_slot, ":village_no", slot_village_infested_by_bandits, 0),
           (call_script, "script_abort_quest", "qst_deal_with_bandits_at_lords_village", 2),
         (try_end),
       (else_try),
         (party_set_slot, ":village_no", slot_village_infested_by_bandits, 0),
         #SB : prosperity linked infestation
         (try_begin),
           (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
           (party_get_slot, ":prosperity", ":village_no", slot_town_prosperity),
           (val_div, ":prosperity", 2), #0 to 50
           (val_add, ":prosperity", 75), #75 to 125
           (store_random_in_range, ":random_no", 0, ":prosperity"),
         (else_try),
           (store_random_in_range, ":random_no", 0, 100),
         (try_end),
         # (assign, ":continue", 1),
         (try_begin),
           (check_quest_active, "qst_collect_taxes"),
           (quest_slot_eq, "qst_collect_taxes", slot_quest_target_center, ":village_no"),
           (assign, ":random_no", 100),
         (else_try),
           (check_quest_active, "qst_train_peasants_against_bandits"),
           (quest_slot_eq, "qst_train_peasants_against_bandits", slot_quest_target_center, ":village_no"),
           (assign, ":random_no", 100),
         (try_end),
         # (eq, ":continue", 1),
         ## SB : update bandit creation parameters
         (lt, ":random_no", 3),
         (call_script, "script_center_get_bandits", ":village_no", 0),
         (assign, ":bandit_troop", reg0),
         (party_set_slot, ":village_no", slot_village_infested_by_bandits, ":bandit_troop"),
         #Reduce prosperity of the village by 3: reduce to -1
         (call_script, "script_change_center_prosperity", ":village_no", -1),
         (val_add, "$newglob_total_prosperity_from_bandits", -1),
         (try_begin),
           (eq, "$cheat_mode", 2),
           (str_store_party_name, s1, ":village_no"),
           (display_message, "@{!}DEBUG --{s1} is infested by bandits."),
         (try_end),
       (try_end),
     (try_end),
     ])
]
