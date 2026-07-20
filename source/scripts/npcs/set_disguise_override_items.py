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

set_disguise_override_items_scripts = [
("set_disguise_override_items", [
      (store_script_param, ":mission_template", 1),
      (store_script_param, ":entry_no", 2),
      (store_script_param, ":with_weapon", 3),

      (mission_tpl_entry_clear_override_items, ":mission_template", ":entry_no"),
      (try_begin),
        (eq, "$sneaked_into_town", disguise_pilgrim),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_pilgrim_disguise"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_pilgrim_hood"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_wrapping_boots"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_practice_staff"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_throwing_daggers"),
        (try_end),
      (else_try),
        (eq, "$sneaked_into_town", disguise_farmer),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_felt_hat"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_coarse_tunic"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_nomad_boots"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_battle_fork"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_cleaver"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_stones"),
        (try_end),
      (else_try),
        (eq, "$sneaked_into_town", disguise_hunter),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_black_hood"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_leather_gloves"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_light_leather"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_light_leather_boots"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_sword_khergit_1"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_hunting_bow"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_barbed_arrows"),
        (try_end),
      (else_try),
        (eq, "$sneaked_into_town", disguise_merchant),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_leather_jacket"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_woolen_hose"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_felt_steppe_cap"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_dagger"),
        (try_end),
      (else_try),
        (eq, "$sneaked_into_town", disguise_guard),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_footman_helmet"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_mail_mittens"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_mail_shirt"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_leather_jerkin"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_mail_chausses"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_fighting_pick"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_tab_shield_round_c"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_war_spear"),
        (try_end),
      (else_try),
        (eq, "$sneaked_into_town", disguise_bard),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_linen_tunic"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_leather_boots"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_winged_mace"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_lyre"),
        (try_end),
      (try_end),
   ])
]
