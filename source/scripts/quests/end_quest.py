# ======================================================================
# SHARED DEPENDENCY
# Entity: end_quest (script)
# Called by menus in 3 domains: kingdom_management, siege, village
# ======================================================================

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

end_quest_scripts = [
#script_end_quest
# INPUT: arg1 = quest_no
# OUTPUT: none
("end_quest",
    [
      (store_script_param, ":quest_no", 1),
      (str_clear, s1),
      (add_quest_note_from_sreg, ":quest_no", 0, s1, 0),
      (add_quest_note_from_sreg, ":quest_no", 1, s1, 0),
      (add_quest_note_from_sreg, ":quest_no", 2, s1, 0),
      (add_quest_note_from_sreg, ":quest_no", 3, s1, 0),
      (add_quest_note_from_sreg, ":quest_no", 4, s1, 0),
      (add_quest_note_from_sreg, ":quest_no", 5, s1, 0),
      (add_quest_note_from_sreg, ":quest_no", 6, s1, 0),
      (add_quest_note_from_sreg, ":quest_no", 7, s1, 0),
      (try_begin),
        (neg|check_quest_failed, ":quest_no"),
        (val_add, "$g_total_quests_completed", 1),
      (try_end),
      (complete_quest, ":quest_no"),
      (try_begin),
        (eq, ":quest_no", "qst_consult_with_minister"),
        (assign, "$g_minister_notification_quest", 0),
      (else_try), #SB : finish clearing ransom debts
        (eq, ":quest_no", "qst_rescue_prisoner"),
        (try_for_range, ":troop_no", heroes_begin, heroes_end),
          (troop_slot_ge, ":troop_no", slot_troop_player_debt, dplmc_ransom_debt_mask),
          (troop_set_slot, ":troop_no", slot_troop_player_debt, 0),
        (try_end),
      # (else_try), #SB : clean up fugitive troop
        # (eq, ":quest_no", "qst_hunt_down_fugitive"),
        # (try_for_parties, ":party_no"),
          # (party_is_active, ":party_no"),
          # (party_remove_prisoners, ":party_no", "trp_fugitive", 1),
          # (party_remove_members, ":party_no", "trp_fugitive", 1),
        # (try_end),
      (else_try),
        (is_between, ":quest_no", mayor_quests_begin, mayor_quests_end),
        (assign, "$merchant_quest_last_offerer", -1),
        (assign, "$merchant_offered_quest", -1),
      (try_end),
    ])
]
