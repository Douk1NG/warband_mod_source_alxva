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

recruit_troop_as_companion_scripts = [
# script_create_kingdom_party_if_below_limit
# Input: arg1 = troop_no,
# Output: none
("recruit_troop_as_companion",
    [
      (store_script_param_1, ":troop_no"),
      ##diplomacy start+
      ##Save civilian clothing of companions (and ladies, etc.)
      (try_begin),
         (troop_is_hero, ":troop_no"),
         (neg|troop_slot_ge, ":troop_no", slot_troop_playerparty_history, 1),#only call this the first time they join
         (call_script, "script_dplmc_save_civilian_clothing", ":troop_no"),#although, redundant calls should be save
         (call_script, "script_change_troop_renown", ":troop_no", 1),#although, redundant calls should be save
      (try_end),
      ##Preserve former occupations enfeoffed companions
      (try_begin),
          (troop_is_hero, ":troop_no"),
          (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (neg|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
          (troop_set_slot, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
      (try_end),
      ##diplomacy end+
      (try_begin), #SB :  spouse scripts
        (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
        (troop_set_slot, ":troop_no", slot_troop_occupation, slto_player_companion),
        (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
      (else_try), #SB : store that lady was recruited as companion
        (troop_set_slot, ":troop_no", slot_troop_first_encountered, "$current_town"),
        (troop_set_slot, ":troop_no", slot_troop_cur_center, -1), #dckplmc
      (try_end),
      (troop_set_auto_equip, ":troop_no", 0),
      (troop_set_slot, ":troop_no", slot_troop_not_auto_equip, 1),
      (party_add_members, "p_main_party", ":troop_no", 1),
      (str_store_troop_name_link, s6, ":troop_no"),
      (display_log_message, "@{s6} has joined your party.", message_alert), #SB : colourize
      (play_sound, "snd_tutorial_2"), #SB : chime sound
      (troop_set_note_available, ":troop_no", 1),

      (try_begin),
        (is_between, ":troop_no", companions_begin, companions_end),
        (store_sub, ":companion_number", ":troop_no", companions_begin),

        (set_achievement_stat, ACHIEVEMENT_KNIGHTS_OF_THE_ROUND, ":companion_number", 1),

        (assign, ":number_of_companions_hired", 0),
        (try_for_range, ":cur_companion", 0, 16),
          (get_achievement_stat, ":is_hired", ACHIEVEMENT_KNIGHTS_OF_THE_ROUND, ":cur_companion"),
          (eq, ":is_hired", 1),
          (val_add, ":number_of_companions_hired", 1),
        (try_end),

        (try_begin),
          (ge, ":number_of_companions_hired", 6),
          (unlock_achievement, ACHIEVEMENT_KNIGHTS_OF_THE_ROUND),
        (try_end),
      (try_end),
  ])
]
