# ======================================================================
# SHARED DEPENDENCY
# Entity: remove_troop_from_prison (script)
# Called by menus in 2 domains: battle, town
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

remove_troop_from_prison_scripts = [
("remove_troop_from_prison",
    [
      (store_script_param, ":troop_no", 1),
      (troop_set_slot, ":troop_no", slot_troop_prisoner_of_party, -1),
      (troop_set_slot, ":troop_no", slot_troop_courtesan, -1),
      (try_begin),
        (eq, "$do_not_cancel_quest", 0),
        (check_quest_active, "qst_rescue_lord_by_replace"),
        (quest_slot_eq, "qst_rescue_lord_by_replace", slot_quest_target_troop, ":troop_no"),
        (call_script, "script_cancel_quest", "qst_rescue_lord_by_replace"),
      (try_end),
      (try_begin),
        (eq, "$do_not_cancel_quest", 0),
        (check_quest_active, "qst_rescue_prisoner"),
        (quest_slot_eq, "qst_rescue_prisoner", slot_quest_target_troop, ":troop_no"),
        (call_script, "script_cancel_quest", "qst_rescue_prisoner"),
        #SB : cancel companion missions
        (try_for_range, ":companions", companions_begin, companions_end),
          (troop_slot_eq, ":companions", slot_troop_current_mission, dplmc_npc_mission_rescue_prisoner),
          (troop_slot_eq, ":companions", slot_troop_mission_object, ":troop_no"),
          (troop_set_slot, ":companions", slot_troop_current_mission, npc_mission_rejoin_when_possible),
          (troop_set_slot, ":companions", slot_troop_days_on_mission, 1),
        (try_end),
        # also accrues debts
        (try_for_range, ":troop_no", heroes_begin, heroes_end),
          # (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (troop_get_slot, ":cur_debt", ":troop_no", slot_troop_player_debt),
          (gt, ":cur_debt", dplmc_ransom_debt_mask),
          (val_mod, ":cur_debt", dplmc_ransom_debt_mask),
          (troop_set_slot, ":troop_no", slot_troop_player_debt, ":cur_debt"),
        (try_end),
      (try_end),
      (try_begin),
        (check_quest_active, "qst_deliver_message_to_prisoner_lord"),
        (quest_slot_eq, "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop, ":troop_no"),
        (call_script, "script_cancel_quest", "qst_deliver_message_to_prisoner_lord"),
      (try_end),
      ])
]
